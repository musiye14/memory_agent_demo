from typing import Sequence
from .config import AppConfig
from volcenginesdkarkruntime import Ark
class Embedder:
    def __init__(self,cfg:AppConfig):
        self.api = cfg.embedding_api
        self.key = cfg.embedding_key
        self.model = cfg.embedding_model
        self.dim = cfg.embedding_dimention

        try:
            self.client = Ark(api_key=self.key)
        except Exception as e:
            print(f"[warn]connecting embedding error!:{e}")
            self.client = None
    
    def embed(self,content:str)->Sequence[float]:
        if not self.client:
            print("embedding not connect")
            return
        res = self.client.embeddings.create(input = content,model = self.model,encoding_format="float")
        return res.data[0].embedding

    @property
    def available(self)->bool:
        return self.client is not None
