import { processarArquivo } from './dataProcessor.js';
import { filtrarPorMesEAno } from './filters.js';
import { exportarDadosFiltrados } from './export.js';

// Exporta funções para uso em outros módulos
export { filtrarPorMesEAno, exportarDadosFiltrados };

// Verifica se as bibliotecas externas carregaram corretamente
window.addEventListener('load', () => {
  if (!window.XLSX || !window.Plotly) {
    exibirErro("Erro ao carregar bibliotecas externas. Verifique sua conexão e tente novamente.");
  }
});

// Adiciona evento ao input de arquivo
document.getElementById('inputExcel').addEventListener('change', processarArquivo);

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

window.filtrarPorMesEAno = filtrarPorMesEAno;