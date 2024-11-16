import os
from config import Config

class FileService:
    @staticmethod
    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

    @staticmethod
    def save_file(file):
        if file and FileService.allowed_file(file.filename):
            filepath = os.path.join(Config.UPLOAD_FOLDER, file.filename)
            file.save(filepath)
            return True
        return False

    @staticmethod
    def delete_file(filename):
        filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
        return False

    @staticmethod
    def list_files():
        """
        Lista todos os arquivos PDF do diretório de upload.
        Lança FileNotFoundError se o diretório não existir.
        """
        if not os.path.exists(Config.UPLOAD_FOLDER) or not os.path.isdir(Config.UPLOAD_FOLDER):
            raise FileNotFoundError(f"Diretório não encontrado: {Config.UPLOAD_FOLDER}")
            
        return [f for f in os.listdir(Config.UPLOAD_FOLDER) if f.endswith('.pdf')]