/**
 * Atualiza o dashboard com os dados fornecidos.
 * @param {Object[]} dados - Array de objetos com os dados.
 */
export function atualizarDashboard(dados) {
    if (dados.length === 0) {
      exibirErro("Nenhum dado encontrado para o filtro selecionado.");
      return;
    }
    atualizarCards(dados);
    criarGraficoIdade(dados);
    criarGraficoSexo(dados);
    criarGraficoOficina(dados);
  }
  
  /**
   * Atualiza os cards com informações agregadas.
   * @param {Object[]} dados - Array de objetos com os dados.
   */
  function atualizarCards(dados) {
    document.getElementById('totalPessoas').innerText = dados.length;
    const homens = dados.filter(p => p.Sexo === 'masculino').length;
    const mulheres = dados.filter(p => p.Sexo === 'feminino').length;
    const oficinas = new Set(dados.map(p => p.Oficinas));
  
    document.getElementById('totalHomens').innerText = homens;
    document.getElementById('totalMulheres').innerText = mulheres;
    document.getElementById('totalOficinas').innerText = oficinas.size;
  }
  
  /**
   * Cria o gráfico de distribuição de idade.
   * @param {Object[]} dados - Array de objetos com os dados.
   */
  function criarGraficoIdade(dados) {
    const idades = dados.map(item => item.Idade);
    const trace = {
      x: idades,
      type: 'histogram',
      marker: {
        color: '#3b82f6',
        line: { color: '#1e3a8a', width: 1.5 },
        gradient: {
          type: 'vertical',
          color: ['#3b82f6', '#1e40af']
        }
      },
      xbins: { size: 5 },
      hovertemplate: "Idade: %{x}<br>Pessoas: %{y}<extra></extra>",
    };
    const layout = {
      title: {
        text: 'Distribuição de Idade',
        font: { size: 20, family: 'Inter', weight: 600, color: '#1f2937' },
        x: 0.5,
        xanchor: 'center'
      },
      xaxis: {
        title: { text: 'Idade', font: { size: 14 } },
        tickfont: { size: 12 },
        gridcolor: '#e5e7eb'
      },
      yaxis: {
        title: { text: 'Número de Pessoas', font: { size: 14 } },
        tickfont: { size: 12 },
        tickformat: 'd',
        gridcolor: '#e5e7eb'
      },
      margin: { t: 60, b: 80, l: 60, r: 60 },
      paper_bgcolor: 'rgba(0,0,0,0)',
      plot_bgcolor: 'rgba(0,0,0,0)',
      showlegend: false,
      hovermode: 'closest',
      transition: { duration: 500, easing: 'cubic-in-out' },
      height: 400
    };
    const config = {
      responsive: true,
      displayModeBar: true,
      modeBarButtonsToRemove: ['toImage', 'lasso2d', 'select2d'],
      displaylogo: false
    };
    Plotly.react('grafico_idade', [trace], layout, config);
  }
  
  /**
   * Cria o gráfico de distribuição por sexo.
   * @param {Object[]} dados - Array de objetos com os dados.
   */
  function criarGraficoSexo(dados) {
    const sexoCounts = {};
    dados.forEach(item => {
      sexoCounts[item.Sexo] = (sexoCounts[item.Sexo] || 0) + 1;
    });
    const trace = {
      x: Object.keys(sexoCounts),
      y: Object.values(sexoCounts),
      type: 'bar',
      marker: {
        color: ['#10b981', '#f472b6'],
        line: { color: '#1f2937', width: 1 }
      },
      width: 0.4,
      text: Object.values(sexoCounts),
      textposition: 'auto',
      hovertemplate: "Sexo: %{x}<br>Pessoas: %{y}<extra></extra>",
    };
    const layout = {
      title: {
        text: 'Distribuição por Sexo',
        font: { size: 20, family: 'Inter', weight: 600, color: '#1f2937' },
        x: 0.5,
        xanchor: 'center'
      },
      xaxis: {
        title: { text: 'Sexo', font: { size: 14 } },
        tickfont: { size: 12 }
      },
      yaxis: {
        title: { text: 'Número de Pessoas', font: { size: 14 } },
        tickfont: { size: 12 },
        tickformat: 'd',
        gridcolor: '#e5e7eb'
      },
      margin: { t: 60, b: 80, l: 60, r: 60 },
      paper_bgcolor: 'rgba(0,0,0,0)',
      plot_bgcolor: 'rgba(0,0,0,0)',
      showlegend: false,
      hovermode: 'closest',
      transition: { duration: 500, easing: 'cubic-in-out' },
      height: 400
    };
    const config = {
      responsive: true,
      displayModeBar: true,
      modeBarButtonsToRemove: ['toImage', 'lasso2d', 'select2d'],
      displaylogo: false
    };
    Plotly.react('grafico_sexo', [trace], layout, config);
  }
  
  /**
   * Cria o gráfico de distribuição por oficina (barras horizontais).
   * @param {Object[]} dados - Array de objetos com os dados.
   */
  function criarGraficoOficina(dados) {
    const oficinaCounts = {};
    dados.forEach(item => {
      oficinaCounts[item.Oficinas] = (oficinaCounts[item.Oficinas] || 0) + 1;
    });
    const sortedOficinas = Object.keys(oficinaCounts).sort((a, b) => oficinaCounts[b] - oficinaCounts[a]);
    const trace = {
      y: sortedOficinas,
      x: sortedOficinas.map(key => oficinaCounts[key]),
      type: 'bar',
      orientation: 'h',
      marker: {
        color: ['#f97316', '#3b82f6', '#10b981', '#f472b6', '#8b5cf6', '#f43f5e', '#eab308'],
        line: { color: '#1f2937', width: 1 }
      },
      text: sortedOficinas.map(key => oficinaCounts[key]),
      textposition: 'auto',
      hovertemplate: "Oficina: %{y}<br>Pessoas: %{x}<extra></extra>",
    };
    const layout = {
      title: {
        text: 'Distribuição por Oficina',
        font: { size: 20, family: 'Inter', weight: 600, color: '#1f2937' },
        x: 0.5,
        xanchor: 'center'
      },
      xaxis: {
        title: { text: 'Número de Pessoas', font: { size: 14 } },
        tickfont: { size: 12 },
        tickformat: 'd',
        gridcolor: '#e5e7eb'
      },
      yaxis: {
        title: { text: 'Oficina', font: { size: 14 } },
        tickfont: { size: 12 },
        automargin: true
      },
      margin: { t: 60, b: 80, l: 150, r: 60 },
      paper_bgcolor: 'rgba(0,0,0,0)',
      plot_bgcolor: 'rgba(0,0,0,0)',
      showlegend: false,
      hovermode: 'closest',
      transition: { duration: 500, easing: 'cubic-in-out' },
      height: 400
    };
    const config = {
      responsive: true,
      displayModeBar: true,
      modeBarButtonsToRemove: ['toImage', 'lasso2d', 'select2d'],
      displaylogo: false
    };
    Plotly.react('grafico_oficina', [trace], layout, config);
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