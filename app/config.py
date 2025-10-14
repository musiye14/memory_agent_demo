import os
from xxlimited import Null
from dotenv import load_dotenv
from dataclasses import dataclass

load_dotenv()

@dataclass
class AppConfig:
    openai_api:str
    openai_key:str
    chat_model:str
    embeding_api:str
    embeding_key:str
    embeding_model:str
    embedding_dimention:int
    db_url:str
    fact_prompt_path:str
    system_prompt_path:str

    def print_info(self):
        print("==配置信息==")
        print(f"openai_api              :{self.openai_api}")
        print(f"openai_key              :{self.openai_key}")
        print(f"chat_model              :{self.chat_model}")
        print(f"embeding_api            :{self.embeding_api}")
        print(f"embeding_key            :{self.embeding_key}")
        print(f"embeding_model          :{self.embeding_model}")
        print(f"embeding_dimention      :{self.embedding_dimention}")
        print(f"db_url                  :{self.db_url}")
        print(f"fact_prompt_path        :{self.fact_prompt_path}")
        print(f"system_prompt_path      :{self.system_prompt_path}")


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
    
    


    return AppConfig(
        openai_api=openai_api,
        openai_key=openai_key,
        chat_model=chat_model,
        embeding_api=embedding_api,
        embeding_key=embedding_key,
        embedding_model=embedding_model,
        embedding_dimention=embedding_dimention,
        db_url=db_url,
        fact_prompt_path=fact_prompt_path,
        system_prompt_path=system_prompt_path
    )
    return config


