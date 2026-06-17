from dotenv import dotenv_values

class Config:
    def __init__(self, dot_env_file: str = ".env"):
        self.config_dict = dotenv_values(dot_env_file)


    def get_value(self, key: str) -> str:
        if key in self.config_dict:
            return self.config_dict[key]
        
        raise KeyError(f"Key {key} not in config")
    
    def set_value(self, key: str, value: str):
        self.config_dict[key] = value
    