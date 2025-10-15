from .embedding import Embedder
from sqlalchemy import create_engine,text
from sqlalchemy.engine import Engine
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
    def __init__(self,db:Engine, embedder:Embedder) -> None:
        self.db=db
        self.embedder=embedder
    
    # 写入记忆
    def store(self,thread_id:str,content:str):
        if not self.embedder.available:
            return
        try:
            vector=self.embedder.embed(content)
            
            if vector is None:
                return

            with self.db.begin() as conn:
                conn.execute(
                    text("INSERT INTO facts (thread_id, content, embedding) VALUES (:thread_id, :content, :embedding)"),
                    {"thread_id":thread_id,"content":content,"embedding":vector}
                )
        except Exception as e:
            print(f"写入数据失败{e}")


    # 向量检索 相似度匹配 返回前3
    def retrieve(self,thread_id:str,query:str,k:int = 10 )->list[str]:
        if not self.embedder.available:
            return []
        
        try:
            with self.db.begin() as conn:
                row = conn.execute(
                    text("""
                        SELECT content
                        FROM facts 
                        WHERE thread_id = :thread_id 
                        ORDER BY embedding <=> CAST(:e AS vector) ASC 
                        LIMIT :k
                    """),
                    {"thread_id":thread_id,"e":self.embedder.embed(query),"k":k}
                ).fetchall()

                seen=set()
                result = []

                for r in row:
                    if not r or not r[0]:
                        continue

                    c = str(r[0]).strip()
                    if c and c not in seen:
                        result.append(c)
                        seen.add(c)

                return result
        except Exception as e:
            print(f"读取长期记忆失败 跳过{e}")
            return []

       



