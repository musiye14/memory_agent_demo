from .embedding import Embedder
from sqlalchemy import create_engine,text
# 初始化连接
def init_db(url:str,dim:int):
    engine = create_engine(url)

    with engine.begin() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        conn.execute(text(f"""
            CREATE TABLE IF NOT EXISTS facts(
                id SERIAL PRIMARY KEY,
                thread_id TEXT,
                content TEXT,
                embedding vector({dim})
            )
        """))

    return engine

class FactStore:
    def __init__(self) -> None:
        pass
    
    # 写入记忆
    def store(self,content:str):
        pass

    # 向量检索 相似度匹配 返回前3
    def retrieve(self,content:str):
        pass



