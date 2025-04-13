from flask import Blueprint, render_template, request, redirect, url_for, abort
from services.file_service import FileService
from utils.decorators import login_required

pdf = Blueprint('pdf', __name__)

@pdf.route('/upload_pdf', methods=['GET', 'POST'])
@login_required
def upload_pdf():
    if request.method == 'POST':
        if 'file' not in request.files:
            return '', 204
        # Adicionado o ano e passando-o como paramtro no form
        ano = request.form.get('ano')
        file = request.files['file']
        if FileService.save_file(file, ano=ano):
            return redirect(url_for('pdf.upload_pdf'))
        return '', 204

    arquivos = FileService.list_files()
    return render_template('upload_pdf.html', arquivos=arquivos)

@pdf.route('/delete_pdf/<ano>/<filename>', methods=['POST'])
@login_required
def delete_pdf(ano, filename):
    FileService.delete_file(filename, ano)
    return redirect(url_for('pdf.upload_pdf'))

@pdf.route('/listar_pdfs')
def listar_pdfs():
    try:
        arquivos = FileService.list_files()
        return render_template('listar_pdfs.html', arquivos=arquivos)
    except FileNotFoundError:
        abort(404)