from os import path
import json

class Config:
    BASE_DIR = path.dirname(path.abspath(__file__))
    UPLOAD_FOLDER = path.join(BASE_DIR, 'static/relatorios')
    CONFIG_FILE = path.join(BASE_DIR, 'config.json')
    ALLOWED_EXTENSIONS = {'pdf'}

    @staticmethod
    def get_db_config():
        try:
            with open(Config.CONFIG_FILE, 'r') as config_file:
                config = json.load(config_file)
                return config["db_config"]
        except FileNotFoundError:
            raise FileNotFoundError(f"Arquivo de configuração não encontrado em: {Config.CONFIG_FILE}")
        except json.JSONDecodeError:
            raise ValueError(f"Erro ao decodificar o arquivo JSON em: {Config.CONFIG_FILE}")
        except KeyError:
            raise KeyError("A chave 'db_config' não foi encontrada no arquivo de configuração")

    @staticmethod
    def get_secret_key():
        try:
            with open(Config.CONFIG_FILE, 'r') as config_file:
                config = json.load(config_file)
                return config["secret_key"]
        except FileNotFoundError:
            raise FileNotFoundError(f"Arquivo de configuração não encontrado em: {Config.CONFIG_FILE}")
        except json.JSONDecodeError:
            raise ValueError(f"Erro ao decodificar o arquivo JSON em: {Config.CONFIG_FILE}")
        except KeyError:
            raise KeyError("A chave 'secret_key' não foi encontrada no arquivo de configuração")

if __name__ == '__main__':
    print(f"BASE_DIR: {Config.BASE_DIR}")
    print(f"CONFIG_FILE path: {Config.CONFIG_FILE}")
    print(f"UPLOAD_FOLDER path: {Config.UPLOAD_FOLDER}")