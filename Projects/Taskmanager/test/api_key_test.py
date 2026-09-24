from pathlib import Path
import json


def get_key(var_name:str,key_path:str)-> str|None:
    if not key_path.exists():
        return None
    
    with open(key_path,'r',encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and '=' in line:
                key, val = line.split("=",1)
                if key.strip() == var_name:
                    api = val.strip().strip("'\"")
                    return api

    return None


