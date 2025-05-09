import { atualizarDashboard } from './charts.js';
import { atualizarFiltroAno } from './filters.js';

let dadosOriginais = [];

/**
 * Sanitiza os dados, removendo entradas inválidas e normalizando valores.
 * @param {Object[]} dados - Array de objetos com os dados do Excel.
 * @returns {Object[]} Dados sanitizados.
 */
export function sanitizarDados(dados) {
  return dados.filter(item => {
    return (
      item.Idade != null && !isNaN(item.Idade) && item.Idade >= 0 &&
      item.Sexo && typeof item.Sexo === 'string' &&
      item.Oficinas && typeof item.Oficinas === 'string' &&
      item.Data && !isNaN(new Date(item.Data).getTime())
    );
  }).map(item => ({
    ...item,
    Sexo: item.Sexo.trim().toLowerCase(),
    Oficinas: item.Oficinas.trim(),
    Idade: parseInt(item.Idade, 10)
  }));
}

/**
 * Processa o arquivo Excel carregado pelo usuário.
 * @param {Event} event - Evento de input do arquivo.
 */
export function processarArquivo(event) {
  const file = event.target.files[0];
  if (!file) return;
  if (!file.name.match(/\.(xlsx|xls|csv)$/)) {
    exibirErro("Por favor, selecione um arquivo .xlsx, .xls ou .csv.");
    return;
  }
  if (file.size > 5 * 1024 * 1024) {
    exibirErro("O arquivo é muito grande. O tamanho máximo é 5MB.");
    return;
  }

  const reader = new FileReader();
  const loader = document.getElementById('loader');
  loader.style.display = 'block';

  reader.onload = function (e) {
    try {
      const data = new Uint8Array(e.target.result);
      const workbook = XLSX.read(data, { type: 'array' });
      const sheetName = workbook.SheetNames[0];
      if (!sheetName) throw new Error("Nenhuma planilha encontrada no arquivo.");
      const sheet = workbook.Sheets[sheetName];
      const jsonData = XLSX.utils.sheet_to_json(sheet);

      if (jsonData.length === 0) throw new Error("O arquivo está vazio.");

      // Validação de colunas
      const requiredColumns = ['Idade', 'Sexo', 'Oficinas', 'Data'];
      const columns = Object.keys(jsonData[0] || {});
      const missingColumns = requiredColumns.filter(col => !columns.includes(col));
      if (missingColumns.length > 0) {
        throw new Error(`Colunas obrigatórias ausentes: ${missingColumns.join(', ')}`);
      }

      dadosOriginais = sanitizarDados(jsonData);
      if (dadosOriginais.length === 0) {
        throw new Error("Nenhum dado válido encontrado no arquivo.");
      }

      document.getElementById('mesSelecionado').style.display = 'inline-block';
      document.getElementById('anoSelecionado').style.display = 'inline-block';
      document.getElementById('exportarDados').style.display = 'inline-block';
      atualizarFiltroAno(dadosOriginais);
      atualizarDashboard(dadosOriginais);

      // Mensagem de sucesso
      const successMessage = document.createElement('div');
      successMessage.textContent = 'Dados carregados com sucesso!';
      successMessage.className = 'success-message';
      document.querySelector('.upload-section').appendChild(successMessage);
      setTimeout(() => successMessage.remove(), 3000);

    } catch (error) {
      exibirErro(`Erro ao processar o arquivo: ${error.message}`);
    } finally {
      loader.style.display = 'none';
    }
  };

  reader.onerror = () => {
    exibirErro("Erro ao ler o arquivo. Tente novamente.");
    loader.style.display = 'none';
  };

  reader.readAsArrayBuffer(file);
}

/**
 * Exibe uma mensagem de erro para o usuário.
 * @param {string} mensagem - Mensagem de erro a ser exibida.
 */
function exibirErro(mensagem) {
  const errorMessage = document.createElement('div');
  errorMessage.textContent = mensagem;
  errorMessage.className = 'error-message';
  document.querySelector('.upload-section').appendChild(errorMessage);
  setTimeout(() => errorMessage.remove(), 5000);
}

export { dadosOriginais };