import { atualizarDashboard } from './charts.js';
import { dadosOriginais } from './dataProcessor.js';

/**
 * Atualiza o select de anos com base nos dados.
 * @param {Object[]} dados - Array de objetos com os dados.
 */
export function atualizarFiltroAno(dados) {
  const anos = [...new Set(dados.map(item => item.Data ? new Date(item.Data).getFullYear() : null))].filter(Boolean).sort();
  const selectAno = document.getElementById('anoSelecionado');
  selectAno.innerHTML = '<option value="0">Todos os Anos</option>';
  anos.forEach(ano => {
    const option = document.createElement('option');
    option.value = ano;
    option.textContent = ano;
    selectAno.appendChild(option);
  });
}

/**
 * Filtra os dados por mês e ano selecionados.
 */
export function filtrarPorMesEAno() {
  const mesSelecionado = parseInt(document.getElementById('mesSelecionado').value);
  const anoSelecionado = parseInt(document.getElementById('anoSelecionado').value);

  let dadosFiltrados = dadosOriginais;
  if (mesSelecionado !== 0) {
    dadosFiltrados = dadosFiltrados.filter(item => {
      if (!item.Data) return false;
      const data = new Date(item.Data);
      return data.getMonth() + 1 === mesSelecionado;
    });
  }
  if (anoSelecionado !== 0) {
    dadosFiltrados = dadosFiltrados.filter(item => {
      if (!item.Data) return false;
      const data = new Date(item.Data);
      return data.getFullYear() === anoSelecionado;
    });
  }

  atualizarDashboard(dadosFiltrados);
}