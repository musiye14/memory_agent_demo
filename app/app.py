from langgraph.checkpoint.postgres import PostgresSaver
from langchain.schema import HumanMessage

from .config import get_appconfig
from .embedding import Embedder
from .llm import build_graph,llm
from .db import FactStore,init_db
def run():
    config  = get_appconfig()
    config.print_info()
    embed = Embedder(config)
    db = init_db(config.sa_conn_str,config.embedding_dimention)
    fact = FactStore(db,embed)
    ai = llm(config,fact)
    builder = build_graph(ai)
    
    with PostgresSaver.from_conn_string(config.pg_conn_str) as checkpoint:
        checkpoint.setup()
        graph = builder.compile(checkpointer=checkpoint)
        thread_id = "test_session_123"
        config1 = {"configurable":{"thread_id":thread_id}}

        # 接受cmd输入 
        while True:
            user_input = input("You:")
            if user_input.lower() == "exit":
                print("程序退出")
                return
            input_data = {"messages": [HumanMessage(content=user_input)]}
            for event in graph.stream(input_data, config=config1):
                for value in event.values():
                    print("AI:", value["messages"][-1].content)
            