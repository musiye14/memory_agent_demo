
def load_file(path:str)->str:
    try:
        with open(path,"r",encoding='utf-8') as f:
            data  = f.read().strip()
            return data
    except Exception as e:
        print(f"获取提示词失败{e}")
        return ""