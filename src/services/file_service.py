import os
from config import Config

class FileService:
    @staticmethod
    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

    @staticmethod
    def save_file(file, ano=None):
        if file and FileService.allowed_file(file.filename):
            # Se o ano for válido, monta o caminho da subpasta com o ano
            if ano and str(ano).isdigit():
                ano = str(ano)
                ano_folder = os.path.join(Config.UPLOAD_FOLDER, ano)
                os.makedirs(ano_folder, exist_ok=True)  # Cria se não existir
            else:
                ano_folder = Config.UPLOAD_FOLDER

            filepath = os.path.join(ano_folder, file.filename)
            file.save(filepath)
            return True
        return False

    @staticmethod
    def delete_file(filename, ano=None):
        if ano:
            filepath = os.path.join(Config.UPLOAD_FOLDER, ano, filename)
        else:
            filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
        
        if os.path.exists(filepath):
            os.remove(filepath)
            # Remove a pasta do ano se estiver vazia
            if ano:
                year_dir = os.path.join(Config.UPLOAD_FOLDER, ano)
                if not os.listdir(year_dir):
                    os.rmdir(year_dir)
            return True
        return False

    @staticmethod
    def list_files():
        files_by_year = {}
        if not os.path.exists(Config.UPLOAD_FOLDER) or not os.path.isdir(Config.UPLOAD_FOLDER):
            raise FileNotFoundError(f"Diretório não encontrado: {Config.UPLOAD_FOLDER}")
        
        for item in os.listdir(Config.UPLOAD_FOLDER):
            year_dir = os.path.join(Config.UPLOAD_FOLDER, item)
            if os.path.isdir(year_dir) and item.isdigit() and len(item) == 4:
                pdfs = [f for f in os.listdir(year_dir) if f.endswith('.pdf')]
                if pdfs:
                    files_by_year[item] = pdfs
        return files_by_year