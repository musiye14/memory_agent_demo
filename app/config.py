import os
from pathlib import Path
from dotenv import load_dotenv
from dataclasses import dataclass

load_dotenv()

@dataclass
class AppConfig:
    openai_api:str
    openai_key:str
    chat_model:str
    embedding_api:str
    embedding_key:str
    embedding_model:str
    embedding_dimention:int
    db_url:str
    sa_conn_str:str
    pg_conn_str:str
    fact_prompt_path:str
    system_prompt_path:str

    def print_info(self):
        print("==配置信息==")
        print(f"openai_api              :{self.openai_api}")
        print(f"openai_key              :{self.openai_key}")
        print(f"chat_model              :{self.chat_model}")
        print(f"embedding_api            :{self.embedding_api}")
        print(f"embedding_key            :{self.embedding_key}")
        print(f"embedding_model          :{self.embedding_model}")
        print(f"embedding_dimention      :{self.embedding_dimention}")
        print(f"db_url                  :{self.db_url}")
        print(f"sa_conn_str                  :{self.sa_conn_str}")
        print(f"pg_conn_str                  :{self.pg_conn_str}")
        print(f"fact_prompt_path        :{self.fact_prompt_path}")
        print(f"system_prompt_path      :{self.system_prompt_path}")

def normalize_path(path: str) -> str:
    """规范化路径，避免转义字符问题"""
    if path:
        # 使用 Path 对象自动处理路径
        return str(Path(path).resolve())
    return path

def _normalize_pg_uri(uri: str):
    """Return SQLAlchemy and psycopg styles: (sa_conn, pg_conn)."""
    if not uri:
        return uri, uri
    
    # 第一步：统一格式，去掉所有的 driver 标识，得到标准的 postgresql://
    # 处理 postgres:// → postgresql://
    if uri.startswith("postgres://"):
        pg_conn = "postgresql://" + uri[len("postgres://"):]
    # 处理 postgresql+任意driver:// → postgresql://
    elif uri.startswith("postgresql+"):
        # 找到 :// 的位置，去掉中间的 +driver 部分
        idx = uri.find("://")
        if idx != -1:
            pg_conn = "postgresql://" + uri[idx + 3:]
        else:
            pg_conn = uri
    # 已经是 postgresql://
    elif uri.startswith("postgresql://"):
        pg_conn = uri
    else:
        pg_conn = uri
    
    # 第二步：基于标准格式生成 SQLAlchemy 格式
    if pg_conn.startswith("postgresql://"):
        sa_conn = "postgresql+psycopg://" + pg_conn[len("postgresql://"):]
    else:
        sa_conn = pg_conn
    
    return sa_conn, pg_conn


def get_appconfig()->AppConfig:
    openai_api = os.getenv("OPENAI_API")
    openai_key = os.getenv("OPENAI_KEY")
    chat_model = os.getenv("CHAT_MODEL")
    embedding_api = os.getenv("EMBEDDING_API")
    embedding_key = os.getenv("EMBEDDING_KEY")
    embedding_model = os.getenv("EMBEDDING_MODEL")
    embedding_dimention = os.getenv("EMBEDDING_DIMENTION")
    db_url = os.getenv("DB_URL")
    fact_prompt_path = os.getenv("FACT_PROMPT_PATH")
    system_prompt_path = os.getenv("STSTEM_PROMPT_PATH")
    if fact_prompt_path:
        fact_prompt_path = normalize_path(fact_prompt_path)
    if system_prompt_path:
        system_prompt_path = normalize_path(system_prompt_path)
    
    if not openai_api:
        print("请先设置OPENAI_API")
    if not openai_key:
        print("请先设置OPENAI_API")
    if not embedding_api:
        print("请先设置EMBEDDING_API")
    if not embedding_key:
        print("请先设置EMBEDDING_KEY")
    if not db_url:
        print("请先设置DB_URL")
    
    sa_conn_str, pg_conn_str = _normalize_pg_uri(db_url)


    return AppConfig(
        openai_api=openai_api,
        openai_key=openai_key,
        chat_model=chat_model,
        embedding_api=embedding_api,
        embedding_key=embedding_key,
        embedding_model=embedding_model,
        embedding_dimention=embedding_dimention,
        db_url=db_url,
        sa_conn_str=sa_conn_str,
        pg_conn_str=pg_conn_str,
        fact_prompt_path=fact_prompt_path,
        system_prompt_path=system_prompt_path
    )
    return config


