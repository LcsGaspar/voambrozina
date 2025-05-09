import { dadosOriginais } from './dataProcessor.js';

/**
 * Exporta os dados filtrados como arquivo Excel.
 */
export function exportarDadosFiltrados() {
  const mesSelecionado = document.getElementById('mesSelecionado').value;
  const anoSelecionado = document.getElementById('anoSelecionado').value;
  let dados = dadosOriginais;

  if (mesSelecionado !== '0' || anoSelecionado !== '0') {
    dados = dadosOriginais.filter(item => {
      if (!item.Data) return false;
      const data = new Date(item.Data);
      const mesValido = mesSelecionado === '0' || data.getMonth() + 1 === parseInt(mesSelecionado);
      const anoValido = anoSelecionado === '0' || data.getFullYear() === parseInt(anoSelecionado);
      return mesValido && anoValido;
    });
  }

  const worksheet = XLSX.utils.json_to_sheet(dados);
  const workbook = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(workbook, worksheet, 'Dados');
  XLSX.writeFile(workbook, 'dados_filtrados.xlsx');
}