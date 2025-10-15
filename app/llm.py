from typing import Dict, Any, List, Tuple
from langgraph.graph import StateGraph,MessagesState, START, END
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI

from langchain.schema import SystemMessage,HumanMessage

from .config import AppConfig
from .db import FactStore
from .prompt import load_file
from .facts import extract_facts_via_llm

class llm:
    def __init__(self,cfg:AppConfig,fact_store:FactStore) -> None:
        self.model=cfg.chat_model
        self.api = cfg.openai_api
        self.key = cfg.openai_key
        self.fact_store=fact_store
        self.cfg = cfg

        try:
            self.llm = ChatOpenAI(api_key=self.key,base_url=self.api,model=self.model)
        except Exception as e:
            print(f"连接llm失败{e}")
    
    def call_llm(self, state:MessagesState)->Dict[str,Any]:

        # 
        thread_id = state.get("configurable",{}).get("thread_id", "default")
        last_message = state["messages"][-1]
        txt = last_message.content

        prompt = []
        system_prompt = load_file(self.cfg.system_prompt_path)

        # 信息提取
        facts_extracted  = extract_facts_via_llm(txt,self.llm,self.cfg.fact_prompt_path)
        for f in facts_extracted:
            # 信息存入长期记忆
            self.fact_store.store(thread_id, f)

        # 将当前询问相关的长期记忆全部找到
        facts = self.fact_store.retrieve(thread_id, txt)


        prompt.append(SystemMessage(content=system_prompt))
        prompt.append(HumanMessage(content=last_message.content))
        if facts:
           facts_text = "\n".join(f"- {fact}" for fact in facts)
           prompt.append(SystemMessage(content=f"以下是我记住的一些相关信息：\n{facts_text}"))

        print("\n--- 本轮实际发送给 LLM 的上下文 ---")
        for msg in prompt:
            print(msg.type, ":", msg.content)
        print("---------------------\n")

        resp = self.llm.invoke(prompt)
        return {"messages":[resp]}


def build_graph(server:llm) -> StateGraph:
    graph = StateGraph(state_schema=MessagesState)
    graph.add_node("llm",server.call_llm)
    graph.add_edge(START,"llm")
    graph.add_edge("llm",END)
    return graph