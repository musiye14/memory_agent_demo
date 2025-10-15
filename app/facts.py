
from typing import List,Tuple,Optional
from langchain_openai import ChatOpenAI

import json,re

from .prompt import load_file

def _extract_json(text: str) -> Optional[dict]:
    try:
        return json.loads(text)
    except Exception:
        pass
    m = re.search(r"\{[\s\S]*\}", text)
    if m:
        try:
            return json.loads(m.group(0))
        except Exception:
            return None
    return None

def extract_facts_via_llm(txt:str,llm:ChatOpenAI,path:str):

    prompt:List[Tuple[str,str]] = []

    system_prompt = load_file(path).format(text=txt,input=txt)

    prompt.append(("system",system_prompt))
    prompt.append(("user",txt))

    resp = llm.invoke(prompt)
    content =  getattr(resp, "content", "") or ""
    data = _extract_json(content)

    if isinstance(data,dict) and isinstance(data.get("facts"),list):
        seen = set()
        res = []

        for fact in data["facts"]:
            if fact is not None and fact not in seen:
                seen.add(fact)
                res.append(fact)
        return res
    return []