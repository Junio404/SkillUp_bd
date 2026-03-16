(function() {
  const API_URL = 'http://localhost:8000';

  // ── COMUNICAÇÃO ────────────────────────────────────────────
  const SQL_MAP = {
    'POST /candidatos/': "INSERT INTO candidato (id, nome, cpf, email, senha_hash, areaInteresse, nivelFormacao, curriculo_url) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
    'GET /candidatos/cpf/': "SELECT * FROM candidato WHERE cpf = ?",
    'GET /candidatos/email/': "SELECT * FROM candidato WHERE email = ?",
    'GET /candidatos/id/': "SELECT * FROM candidato WHERE id = ?",
    'GET /candidatos/': "SELECT * FROM candidato",
    'POST /candidaturas/': "INSERT INTO candidatura (id, dataCandidatura, status, candidato_id, vaga_id) VALUES (?, ?, ?, ?, ?)",
    'PATCH /candidaturas/': "UPDATE candidatura SET status = ? WHERE id = ?",
    'GET /candidaturas/filtro': "SELECT * FROM candidatura WHERE status = ? AND dataCandidatura BETWEEN ? AND ?",
    'GET /candidaturas/candidato/': "SELECT * FROM candidatura WHERE candidato_id = ?",
    'GET /candidaturas/': "SELECT * FROM candidatura",
    'POST /competencias-candidato/': "INSERT INTO competencia_candidato (candidato_id, competencia_id, nivel) VALUES (?, ?, ?)",
    'GET /competencias-candidato/': "SELECT * FROM competencia_candidato",
    'GET /vagas/': "SELECT * FROM vaga",
    'POST /vagas/': "INSERT INTO vaga (id, titulo, empresa_id, modalidade, tipo, prazo_inscricao, localidade, jornada, descricao) VALUES (...)",
    'POST /inscricoes-curso/': "INSERT INTO inscricao_curso (id, candidato_id, curso_id, data_inscricao, status) VALUES (?, ?, ?, ?, ?)",
    'GET /inscricoes-curso/': "SELECT * FROM inscricao_curso WHERE candidato_id = ?",
    'POST /instituicoes-area-ensino/': "INSERT INTO instituicao_area_ensino (instituicao_ensino_id, area_ensino_id) VALUES (?, ?)",
    'GET /instituicoes-area-ensino/': "SELECT * FROM instituicao_area_ensino",
    'POST /empresas/': "INSERT INTO empresa (id, razao_social, nome_fantasia, cnpj, senha_hash) VALUES (?, ?, ?, ?, ?)",
    'GET /empresas/cnpj/': "SELECT * FROM empresa WHERE cnpj = ?",
    'GET /empresas/': "SELECT * FROM empresa",
    'POST /instituicoes-ensino/': "INSERT INTO instituicao_ensino (id, razao_social, nome_fantasia, cnpj, registro_educacional, tipo) VALUES (...)",
    'GET /instituicoes-ensino/registro/': "SELECT * FROM instituicao_ensino WHERE registro_educacional = ?",
    'GET /instituicoes-ensino/': "SELECT * FROM instituicao_ensino",
    'POST /cursos/': "INSERT INTO curso (id, nome, modalidade, instituicao_ensino_id, area, carga_horaria, capacidade, prazo_inscricao, empresa_id) VALUES (...)",
    'GET /cursos/': "SELECT * FROM curso",
    'POST /areas-ensino/': "INSERT INTO area_ensino (id, nome) VALUES (?, ?)",
    'GET /areas-ensino/': "SELECT * FROM area_ensino",
    'POST /competencias/': "INSERT INTO competencia (id, nome, descricao) VALUES (?, ?, ?)",
    'GET /competencias/': "SELECT * FROM competencia",
  };

  function logSql(method, path) {
    const monitor = document.getElementById('sql-content');
    if (!monitor) return;
    
    // Remove query params and normalize slashes for matching
    let purePath = path.split('?')[0];
    if (!purePath.endsWith('/')) purePath += '/';
    
    let sql = "-- SQL Simulado: SELECT * FROM table"; 
    
    // Find BEST match (longest key)
    let bestMatch = "";
    for (const key in SQL_MAP) {
      let [m, p] = key.split(' ');
      if (!p.endsWith('/')) p += '/';
      
      if (method === m && purePath.startsWith(p)) {
        if (p.length > bestMatch.length) {
          bestMatch = p;
          sql = SQL_MAP[key];
        }
      }
    }

    const time = new Date().toLocaleTimeString();
    monitor.innerHTML = `<div style="margin-bottom:12px; border-bottom:1px solid #1a1a1a; padding-bottom:8px;"><div style="display:flex; align-items:center; gap:8px; margin-bottom:4px;"><span style="color:var(--muted); font-size:10px; flex-shrink:0;">[${time}]</span><span style="color:var(--accent-c); font-weight:bold; font-size:10px; background:#111; padding:1px 5px; border-radius:3px; flex-shrink:0;">${method}</span><span style="color:var(--muted); font-size:10px; font-family:var(--font-mono); word-break:break-all; line-height:1.2;">${escHtml(path)}</span></div><code style="color:#aaccff; font-size:11px; font-family:var(--font-mono); display:block; background:#0a0a0c; padding:6px; border-radius:4px; border:1px solid #1a1a1a; white-space:pre-wrap; word-break:break-word; line-height:1.3;">${escHtml(sql)}</code></div>` + monitor.innerHTML;
  }

  async function apiRequest(method, path, body) {
    logSql(method, path);
    try {
      const opts = { method, headers: { 'Content-Type': 'application/json' } };
      if (body) opts.body = JSON.stringify(body);
      const response = await fetch(API_URL + path, opts);
      if (!response.ok) {
        let errorData;
        try { errorData = await response.json(); } catch (e) { errorData = { detail: `Erro ${response.status}` }; }
        const msg = errorData.detail || 'Erro desconhecido';
        if (msg.includes('duplicate key')) throw new Error('Já existe um registro com estes dados.');
        if (msg.includes('foreign key')) throw new Error('Operação inválida: dependência entre registros.');
        if (msg.includes('check constraint')) throw new Error('Dados violam as regras do sistema.');
        throw new Error(msg);
      }
      return response.status === 204 ? null : response.json();
    } catch(e) {
      console.error(`[API] ${method} ${path}:`, e);
      throw e;
    }
  }

  function showToast(msg, type = 'success') {
    const t = document.getElementById('toast');
    if (!t) return;
    t.textContent = msg;
    t.className = `show ${type}`;
    setTimeout(() => t.className = '', 3200);
  }

  function escHtml(s) {
    if (s == null) return '—';
    return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
  }

  function openModal(id) { document.getElementById(id)?.classList.add('open'); }
  function closeModal(id) { document.getElementById(id)?.classList.remove('open'); }

  // ── CONSTANTES ────────────────────────────────────────────
  const STATUS_CAND = ['Enviado','Em análise','Aceito','Recusado','Cancelado'];
  const STATUS_INS  = ['Deferido','Indeferido'];
  const MODALIDADE  = ['Presencial','Remoto','Híbrido'];
  const TIPO_VAGA   = ['Emprego','Estágio','Trainee'];
  const NIVEL       = ['Baixa','Média','Alta'];

  function badgeCand(s) {
    const cls = ['badge-gray','badge-purple','badge-green','badge-orange','badge-gray'][s] || 'badge-gray';
    return `<span class="badge ${cls}">${STATUS_CAND[s] ?? s}</span>`;
  }

  // ── TABELA GENÉRICA ───────────────────────────────────────
  function uiTable(container, { headers, data, rowMapper }) {
    if (!container) return;
    if (!data || !data.length) { container.innerHTML = emptyHtml(); return; }
    container.innerHTML = `<div class="table-wrap"><table>
      <thead><tr>${headers.map(h => `<th>${h}</th>`).join('')}</tr></thead>
      <tbody>${data.map(rowMapper).join('')}</tbody>
    </table></div>`;
  }

  // ── FORM DATA (prefixo até primeiro hífen vira _) ─────────
  function getFormData(containerId) {
    const data = {};
    const container = document.getElementById(containerId);
    if (!container) return data;
    container.querySelectorAll('input,select,textarea').forEach(el => {
      if (!el.id) return;
      const parts = el.id.split('-');
      const key = parts.slice(1).join('_');
      let val = el.value;
      if (el.tagName === 'SELECT') {
        const parsed = parseInt(val);
        val = isNaN(parsed) ? val : parsed;
      } else if (el.type === 'number') {
        const parsed = parseInt(val);
        val = val === '' ? null : (isNaN(parsed) ? null : parsed);
      } else {
        val = val.trim() || null;
      }
      if (key) data[key] = val;
    });
    return data;
  }

  async function checkApiHealth() {
    try {
      await fetch(API_URL + '/candidatos/', { signal: AbortSignal.timeout(2000) });
      document.getElementById('api-dot')?.classList.add('online');
      const s = document.getElementById('api-status');
      if (s) s.textContent = 'API online';
    } catch {
      const s = document.getElementById('api-status');
      if (s) s.textContent = 'API offline';
    }
  }

  // ── ESTADO ────────────────────────────────────────────────
  const PROFILES = {
    candidato: {
      accent: 'c',
      nav: [
        { id: 'meu-perfil',       icon: '◈', label: 'Cadastrar candidato' },
        { id: 'candidaturas',     icon: '◎', label: 'Candidaturas' },
        { id: 'competencias-meu', icon: '◆', label: 'Minhas competências' },
        { id: 'inscricoes',       icon: '◉', label: 'Cursos inscritos' },
        { id: 'vagas',            icon: '◐', label: 'Buscar vagas' },
        { id: 'todos-candidatos', icon: '▣', label: 'Todos candidatos' },
      ]
    },
    empresa: {
      accent: 'e',
      nav: [
        { id: 'empresa-perfil',   icon: '◈', label: 'Cadastrar empresa' },
        { id: 'minhas-vagas',     icon: '◎', label: 'Vagas por empresa' },
        { id: 'nova-vaga',        icon: '◆', label: 'Nova vaga' },
        { id: 'candidatos-vaga',  icon: '◉', label: 'Filtrar candidaturas' },
        { id: 'todas-empresas',   icon: '▣', label: 'Todas empresas' },
      ]
    },
    instituicao: {
      accent: 'i',
      nav: [
        { id: 'inst-perfil',   icon: '◈', label: 'Cadastrar instituição' },
        { id: 'meus-cursos',   icon: '◎', label: 'Cursos por instituição' },
        { id: 'novo-curso',    icon: '◆', label: 'Novo curso' },
        { id: 'areas-ensino',  icon: '◉', label: 'Áreas de ensino' },
        { id: 'todas-inst',    icon: '▣', label: 'Todas instituições' },
      ]
    },
    dashboard: {
      accent: 'd',
      nav: [
        { id: 'dash-main', icon: '◫', label: 'Checklist Projeto' },
        { id: 'dash-sql',  icon: '◈', label: 'Esquema Relacional' },
      ]
    }
  };

  let currentProfile = 'candidato';
  let currentNav = 'meu-perfil';

  function switchProfile(p) {
    currentProfile = p;
    document.querySelectorAll('.profile-tab').forEach(t => t.classList.toggle('active', t.dataset.profile === p));
    renderSidebar();
    navigateTo(PROFILES[p].nav[0].id);
  }

  function renderSidebar() {
    const { accent, nav } = PROFILES[currentProfile];
    const aside = document.getElementById('sidebar');
    if (!aside) return;
    aside.innerHTML = `<div class="section-label">${currentProfile.toUpperCase()}</div>`;
    nav.forEach(item => {
      const div = document.createElement('div');
      div.className = 'nav-item' + (item.id === currentNav ? ' active' : '');
      div.dataset.accent = accent;
      div.innerHTML = `<span class="nav-icon">${item.icon}</span>${item.label}`;
      div.onclick = () => navigateTo(item.id);
      aside.appendChild(div);
    });
  }

  const REQUIREMENTS = {
    'meu-perfil': 'Requisito: Inserção em tabela simples',
    'competencias-meu': 'Requisito: Inserção em tabela associativa (N:N)',
    'inscricoes': 'Requisito: Inserção em tabela associativa (N:N)',
    'vagas': 'Requisito: Consulta parametrizável',
    'minhas-vagas': 'Requisito: Consulta parametrizável',
    'candidatos-vaga': 'Requisito: Consulta com múltiplos parâmetros (Status + Datas)',
    'candidaturas': 'Requisito: Atualização de registro (Status)',
    'areas-ensino': 'Requisito: Inserção N:N (Instituição x Área)',
  };

  function navigateTo(id) {
    currentNav = id;
    renderSidebar();
    const pages = {
      'meu-perfil': pageCadastrarCandidato, 'candidaturas': pageCandidaturas,
      'competencias-meu': pageCompetenciasCandidato, 'inscricoes': pageInscricoes,
      'vagas': pageVagas, 'todos-candidatos': pageTodosCandidatos,
      'empresa-perfil': pageCadastrarEmpresa, 'minhas-vagas': pageMinhasVagas,
      'nova-vaga': pageCadastrarVaga, 'candidatos-vaga': pageCandidatosPorVaga,
      'todas-empresas': pageTodasEmpresas,
      'inst-perfil': pageCadastrarInstituicao, 'meus-cursos': pageMeusCursos,
      'novo-curso': pageCadastrarCurso, 'areas-ensino': pageAreasEnsino,
      'todas-inst': pageTodasInstituicoes,
      'dash-main': pageDashboard, 'dash-sql': pageEsquema,
    };
    const main = document.getElementById('main-content');
    if (!main) return;
    main.innerHTML = '';
    const fn = pages[id];
    if (fn) fn(main);
  }

  function pageWrap(container, title, subtitle, html) {
    const req = REQUIREMENTS[currentNav];
    container.innerHTML = `<div class="page active">
      <div class="page-header"><div>
        <div class="page-title">${title}</div>
        <div class="page-sub">${subtitle}</div>
        ${req ? `<div class="req-badge" style="margin-top:8px">${req}</div>` : ''}
      </div></div>${html}</div>`;
  }

  function loadingHtml() { return `<div class="loading"><div class="spinner"></div>Carregando...</div>`; }
  function emptyHtml(msg = 'Nenhum registro encontrado') {
    return `<div class="empty"><div class="empty-icon">◫</div>${msg}</div>`;
  }
  const getAccent = () => PROFILES[currentProfile].accent;

  // ══════════════════════════════════════════════════════════
  //  DASHBOARD
  // ══════════════════════════════════════════════════════════

  function pageDashboard(container) {
    pageWrap(container, 'Dashboard do Professor', 'Verificação de requisitos do TP2', `
      <div class="card">
        <div class="card-title">Resumo de Requisitos</div>
        <div style="display:grid;gap:16px">
          ${renderReqItem('Inserção em ≥3 tabelas', 'Candidato, Empresa, Vaga, etc.', true)}
          ${renderReqItem('Inserção em tabela associativa (N:N)', 'Competência Candidato, Inscrição Curso.', true)}
          ${renderReqItem('≥6 Consultas distintas', 'Busca por CPF, CNPJ, Vagas por Empresa, etc.', true)}
          ${renderReqItem('≥3 Consultas parametrizáveis', 'Busca por CPF, Registro, ID de Empresa.', true)}
          ${renderReqItem('1 Consulta com múltiplos parâmetros', 'Filtro de Candidaturas (Status + Intervalo de Datas).', true)}
          ${renderReqItem('Atualização em ≥1 tabela', 'Atualização de status de candidatura.', true)}
        </div>
      </div>
      <div class="card">
        <div class="card-title">Ações Rápidas</div>
        <div style="display:flex;gap:10px">
          <button class="btn btn-primary" onclick="window.location.reload()">Resetar UI</button>
          <button class="btn btn-ghost" onclick="abrirDocs()">Ver Especificação</button>
        </div>
      </div>
    `);
  }

  function renderReqItem(label, desc, ok) {
    return `<div class="req-card">
      <div class="req-icon">${ok ? '✔' : '○'}</div>
      <div class="req-info">
        <div style="font-size:13px;font-weight:600">${label}</div>
        <div style="font-size:11px;color:var(--muted)">${desc}</div>
      </div>
      <div class="req-status ${ok ? '' : 'pending'}">${ok ? 'IMPLEMENTADO' : 'PENDENTE'}</div>
    </div>`;
  }

  function pageEsquema(container) {
    pageWrap(container, 'Esquema do Banco', 'Modelagem Relacional (3FN)', `
      <div class="card">
        <div class="card-title">Estrutura de Tabelas</div>
        <div style="font-size:12px;color:var(--muted);line-height:1.6;margin-bottom:20px">
          O projeto segue as normas de integridade referencial com Chaves Primárias (UUID) e Chaves Estrangeiras.<br>
          Todas as operações utilizam <b>SQL Puro</b> via repositórios Python.
        </div>
        
        <div style="display:flex; flex-direction:column; gap:24px">
          <div>
            <div class="card-title" style="font-size:11px; margin-bottom:8px">Modelo Entidade-Relacionamento (MER)</div>
            <img src="diagrams/mer_skillup.png" style="width:100%; border-radius:4px; border:1px solid var(--border)" 
                 onerror="this.parentElement.innerHTML='<div class=\'empty\'>Imagem MER não encontrada em diagrams/mer_skillup.png</div>'">
          </div>
          
          <div>
            <div class="card-title" style="font-size:11px; margin-bottom:8px">Diagrama Entidade-Relacionamento (DER)</div>
            <img src="diagrams/der-novo (2)_page-0001.jpg" style="width:100%; border-radius:4px; border:1px solid var(--border)"
                 onerror="this.parentElement.innerHTML='<div class=\'empty\'>Imagem DER não encontrada em diagrams/der-novo (2)_page-0001.jpg</div>'">
          </div>
        </div>
      </div>
    `);
  }

  function abrirDocs() {
    const specs = `
REQUISITOS DO TRABALHO:
1. SQL Puro: Repositórios em infrastructure/repositories/*.py
2. Inserção: ≥3 tabelas (Candidato, Empresa, Vaga...)
3. Inserção N:N: CompetenciaCandidato, InscricaoCurso...
4. Consulta: ≥6 distintas
5. Consulta Parametrizável: CPF, CNPJ, ID...
6. Consulta Multi-Parâmetro: Filtro Candidaturas (status + datas)
7. Atualização: Status de Candidatura
    `;
    alert(specs);
  }


  // ══════════════════════════════════════════════════════════
  //  CANDIDATO
  // ══════════════════════════════════════════════════════════

  function pageCadastrarCandidato(container) {
    pageWrap(container, 'Cadastrar candidato', 'Inserção em candidato', `
      <div class="card">
        <div class="card-title">Novo candidato</div>
        <div class="form-grid" id="form-candidato">
          <div class="field"><label>Nome *</label><input id="c-nome" placeholder="Nome completo"></div>
          <div class="field"><label>CPF * (11 dígitos)</label><input id="c-cpf" placeholder="00000000000" maxlength="11"></div>
          <div class="field"><label>Email *</label><input id="c-email" type="email" placeholder="email@exemplo.com"></div>
          <div class="field"><label>Senha * (mín. 8 caracteres)</label><input id="c-senha" type="password" placeholder="Senha de acesso"></div>
          <div class="field"><label>Área de interesse</label><input id="c-area_interesse" placeholder="Ex: Desenvolvimento Web"></div>
          <div class="field"><label>Nível de formação</label><input id="c-nivel_formacao" placeholder="Ex: Bacharel"></div>
          <div class="field"><label>URL do currículo</label><input id="c-curriculo_url" placeholder="https://..."></div>
        </div>
        <div class="form-actions">
          <button class="btn btn-primary" data-accent="${getAccent()}" onclick="criarCandidato()">Cadastrar</button>
          <button class="btn btn-ghost" onclick="limparForm('form-candidato')">Limpar</button>
        </div>
      </div>
      <div class="card">
        <div class="card-title">Buscar por CPF</div>
        <div class="search-row">
          <input id="busca-cpf" placeholder="CPF (11 dígitos)">
          <button class="btn btn-ghost" onclick="buscarPorCpf()">Buscar</button>
        </div>
        <div id="resultado-cpf"></div>
      </div>
    `);
  }

  async function criarCandidato() {
    const body = getFormData('form-candidato');
    if (!body.nome || !body.cpf || !body.email || !body.senha)
      return showToast('Preencha nome, CPF, email e senha', 'error');
    try {
      await apiRequest('POST', '/candidatos/', body);
      showToast('Candidato cadastrado!');
      limparForm('form-candidato');
    } catch(e) { showToast(e.message, 'error'); }
  }

  function limparForm(id) {
    document.getElementById(id)?.querySelectorAll('input,textarea').forEach(el => el.value = '');
  }

  async function buscarPorCpf() {
    const cpf = document.getElementById('busca-cpf').value.trim();
    if (!cpf) return;
    const div = document.getElementById('resultado-cpf');
    div.innerHTML = loadingHtml();
    try {
      // Rota correta: /candidatos/cpf/{cpf}
      const data = await apiRequest('GET', `/candidatos/cpf/${cpf}`);
      uiTable(div, {
        headers: ['Nome','CPF','Email','Área de interesse','Formação'],
        data: [data],
        rowMapper: c => `<tr>
          <td>${escHtml(c.nome)}</td><td>${escHtml(c.cpf)}</td><td>${escHtml(c.email)}</td>
          <td>${escHtml(c.area_interesse)}</td><td>${escHtml(c.nivel_formacao)}</td></tr>`
      });
    } catch(e) { div.innerHTML = emptyHtml(e.message); }
  }

  // ── CANDIDATURAS ──────────────────────────────────────────
  function pageCandidaturas(container) {
    pageWrap(container, 'Candidaturas', 'Criar candidatura e acompanhar status', `
      <div class="card">
        <div class="card-title">Nova candidatura</div>
        <div class="form-grid" id="form-candidatura">
          <div class="field"><label>ID do candidato</label><input id="cand-candidato_id" placeholder="UUID do candidato"></div>
          <div class="field"><label>ID da vaga</label><input id="cand-vaga_id" placeholder="UUID da vaga"></div>
          <div class="field"><label>Status inicial</label>
            <select id="cand-status"><option value="0">Enviado</option><option value="1">Em análise</option></select>
          </div>
        </div>
        <div class="form-actions">
          <button class="btn btn-primary" data-accent="${getAccent()}" onclick="criarCandidatura()">Criar candidatura</button>
        </div>
      </div>
      <div class="card">
        <div class="card-title">Candidaturas por candidato</div>
        <div class="search-row">
          <input id="busca-cand-id" placeholder="UUID do candidato">
          <button class="btn btn-ghost" onclick="buscarCandidaturas()">Buscar</button>
          <button class="btn btn-ghost" onclick="carregarTodasCandidaturas()">Listar todas</button>
        </div>
        <div id="lista-candidaturas">${loadingHtml()}</div>
      </div>
    `);
    carregarTodasCandidaturas();
  }

  async function criarCandidatura() {
    const body = getFormData('form-candidatura');
    body.data_candidatura = new Date().toISOString();
    if (!body.candidato_id || !body.vaga_id) return showToast('Preencha os IDs', 'error');
    try {
      await apiRequest('POST', '/candidaturas/', body);
      showToast('Candidatura criada!');
      carregarTodasCandidaturas();
    } catch(e) { showToast(e.message, 'error'); }
  }

  async function carregarTodasCandidaturas() {
    const div = document.getElementById('lista-candidaturas');
    if (!div) return;
    div.innerHTML = loadingHtml();
    try {
      const data = await apiRequest('GET', '/candidaturas/');
      renderListaCandidaturas(div, data);
    } catch(e) { div.innerHTML = emptyHtml(e.message); }
  }

  async function buscarCandidaturas() {
    const id = document.getElementById('busca-cand-id').value.trim();
    if (!id) { carregarTodasCandidaturas(); return; }
    const div = document.getElementById('lista-candidaturas');
    div.innerHTML = loadingHtml();
    try {
      // Rota correta: /candidaturas/candidato/{candidato_id}
      const data = await apiRequest('GET', `/candidaturas/candidato/${id}`);
      renderListaCandidaturas(div, data);
    } catch(e) { div.innerHTML = emptyHtml(e.message); }
  }

  function renderListaCandidaturas(div, data) {
    uiTable(div, {
      headers: ['ID','Data','Status','Vaga ID','Ação'],
      data: data,
      rowMapper: c => `<tr>
        <td style="font-size:11px;color:var(--muted)">${c.id.slice(0,8)}…</td>
        <td>${new Date(c.data_candidatura).toLocaleDateString('pt-BR')}</td>
        <td>${badgeCand(c.status)}</td>
        <td style="font-size:11px;color:var(--muted)">${c.vaga_id.slice(0,8)}…</td>
        <td><button class="btn btn-ghost" style="font-size:11px;padding:4px 10px"
          onclick="abrirModalStatus('${c.id}',${c.status})">Atualizar</button></td></tr>`
    });
  }

  let editandoCandidaturaId = null;
  function abrirModalStatus(id, statusAtual) {
    editandoCandidaturaId = id;
    const sel = document.getElementById('modal-status-select');
    if (sel) sel.value = statusAtual;
    openModal('modal-status');
  }

  async function confirmStatusUpdate() {
    const novo = parseInt(document.getElementById('modal-status-select').value);
    try {
      await apiRequest('PATCH', `/candidaturas/${editandoCandidaturaId}/status?novo_status=${novo}`);
      showToast('Status atualizado!');
      closeModal('modal-status');
      carregarTodasCandidaturas();
    } catch(e) { showToast(e.message, 'error'); }
  }

  // ── COMPETÊNCIAS ──────────────────────────────────────────
  function pageCompetenciasCandidato(container) {
    pageWrap(container, 'Competências do candidato', 'Inserção N:N candidato × competência', `
      <div class="card">
        <div class="card-title">Associar competência</div>
        <div class="form-grid" id="form-comp-cand">
          <div class="field"><label>ID do candidato</label><input id="cc-candidato_id" placeholder="UUID do candidato"></div>
          <div class="field"><label>ID da competência</label><input id="cc-competencia_id" placeholder="UUID da competência"></div>
          <div class="field"><label>Nível</label>
            <select id="cc-nivel"><option value="0">Baixa</option><option value="1">Média</option><option value="2">Alta</option></select>
          </div>
        </div>
        <div class="form-actions">
          <button class="btn btn-primary" data-accent="${getAccent()}" onclick="criarCompetenciaCandidato()">Associar</button>
        </div>
      </div>
      <div class="card">
        <div class="card-title">Competências cadastradas</div>
        <div class="search-row">
          <input id="busca-cc-id" placeholder="UUID do candidato">
          <button class="btn btn-ghost" onclick="buscarCompetenciasCandidato()">Buscar por candidato</button>
          <button class="btn btn-ghost" onclick="listarTodasCompetencias()">Listar todas</button>
        </div>
        <div id="lista-comp-cand">${emptyHtml('Use os botões acima para carregar')}</div>
      </div>
    `);
  }

  async function criarCompetenciaCandidato() {
    const body = getFormData('form-comp-cand');
    if (!body.candidato_id || !body.competencia_id) return showToast('Preencha os IDs', 'error');
    try {
      await apiRequest('POST', '/competencias-candidato/', body);
      showToast('Competência associada!');
    } catch(e) { showToast(e.message, 'error'); }
  }

  async function buscarCompetenciasCandidato() {
    const id = document.getElementById('busca-cc-id').value.trim();
    if (!id) return showToast('Informe o ID do candidato', 'error');
    const div = document.getElementById('lista-comp-cand');
    div.innerHTML = loadingHtml();
    try {
      const data = await apiRequest('GET', `/competencias-candidato/${id}`);
      renderListaCompCand(div, data);
    } catch(e) { div.innerHTML = emptyHtml(e.message); }
  }

  async function listarTodasCompetencias() {
    const div = document.getElementById('lista-comp-cand');
    div.innerHTML = loadingHtml();
    try {
      const data = await apiRequest('GET', '/competencias-candidato/');
      renderListaCompCand(div, data);
    } catch(e) { div.innerHTML = emptyHtml(e.message); }
  }

  function renderListaCompCand(div, data) {
    uiTable(div, {
      headers: ['Competência ID','Candidato ID','Nível'],
      data: data,
      rowMapper: c => `<tr>
        <td style="font-size:11px">${c.competencia_id.slice(0,8)}…</td>
        <td style="font-size:11px">${c.candidato_id.slice(0,8)}…</td>
        <td><span class="badge badge-purple">${NIVEL[c.nivel] ?? c.nivel}</span></td></tr>`
    });
  }

  // ── INSCRIÇÕES ────────────────────────────────────────────
  function pageInscricoes(container) {
    pageWrap(container, 'Inscrições em cursos', 'Inserção N:N candidato × curso', `
      <div class="card">
        <div class="card-title">Nova inscrição</div>
        <div class="form-grid" id="form-inscricao">
          <div class="field"><label>ID do candidato</label><input id="ic-candidato_id" placeholder="UUID do candidato"></div>
          <div class="field"><label>ID do curso</label><input id="ic-curso_id" placeholder="UUID do curso"></div>
          <div class="field"><label>Status</label>
            <select id="ic-status"><option value="0">Deferido</option><option value="1">Indeferido</option></select>
          </div>
        </div>
        <div class="form-actions">
          <button class="btn btn-primary" data-accent="${getAccent()}" onclick="criarInscricao()">Inscrever</button>
        </div>
      </div>
      <div class="card">
        <div class="card-title">Inscrições por candidato</div>
        <div class="search-row">
          <input id="busca-ic-id" placeholder="UUID do candidato">
          <button class="btn btn-ghost" onclick="buscarInscricoes()">Buscar</button>
        </div>
        <div id="lista-inscricoes">${emptyHtml('Informe o UUID acima')}</div>
      </div>
    `);
  }

  async function criarInscricao() {
    const body = getFormData('form-inscricao');
    body.data_inscricao = new Date().toISOString().slice(0,10);
    if (!body.candidato_id || !body.curso_id) return showToast('Preencha os IDs', 'error');
    try {
      await apiRequest('POST', '/inscricoes-curso/', body);
      showToast('Inscrição realizada!');
    } catch(e) { showToast(e.message, 'error'); }
  }

  async function buscarInscricoes() {
    const id = document.getElementById('busca-ic-id').value.trim();
    if (!id) return;
    const div = document.getElementById('lista-inscricoes');
    div.innerHTML = loadingHtml();
    try {
      const data = await apiRequest('GET', `/inscricoes-curso/${id}`);
      uiTable(div, {
        headers: ['Curso ID','Data inscrição','Status'],
        data: data,
        rowMapper: i => `<tr>
          <td style="font-size:11px">${i.curso_id.slice(0,8)}…</td>
          <td>${i.data_inscricao}</td>
          <td><span class="badge ${i.status===0?'badge-green':'badge-orange'}">${STATUS_INS[i.status] ?? i.status}</span></td></tr>`
      });
    } catch(e) { div.innerHTML = emptyHtml(e.message); }
  }

  // ── VAGAS ─────────────────────────────────────────────────
  function pageVagas(container) {
    pageWrap(container, 'Buscar vagas', 'Consulta parametrizável', `
      <div class="card">
        <div class="search-row">
          <input id="busca-empresa-vagas" placeholder="UUID da empresa (opcional)">
          <button class="btn btn-ghost" onclick="buscarVagas()">Buscar por empresa</button>
          <button class="btn btn-ghost" onclick="listarTodasVagas()">Listar todas</button>
        </div>
        <div id="lista-vagas">${loadingHtml()}</div>
      </div>
    `);
    listarTodasVagas();
  }

  async function listarTodasVagas() {
    const div = document.getElementById('lista-vagas');
    if (!div) return;
    div.innerHTML = loadingHtml();
    try {
      const data = await apiRequest('GET', '/vagas/');
      renderListaVagas(div, data);
    } catch(e) { div.innerHTML = emptyHtml(e.message); }
  }

  async function buscarVagas() {
    const eid = document.getElementById('busca-empresa-vagas').value.trim();
    const div = document.getElementById('lista-vagas');
    div.innerHTML = loadingHtml();
    try {
      // /vagas/{empresa_id} retorna list_by_empresa
      const data = await apiRequest('GET', eid ? `/vagas/${eid}` : '/vagas/');
      renderListaVagas(div, Array.isArray(data) ? data : [data]);
    } catch(e) { div.innerHTML = emptyHtml(e.message); }
  }

  function renderListaVagas(div, data) {
    uiTable(div, {
      headers: ['Título','Modalidade','Tipo','Prazo','Empresa ID'],
      data: data,
      rowMapper: v => `<tr>
        <td>${escHtml(v.titulo)}</td>
        <td><span class="badge badge-gray">${MODALIDADE[v.modalidade] ?? v.modalidade}</span></td>
        <td><span class="badge badge-purple">${TIPO_VAGA[v.tipo] ?? v.tipo}</span></td>
        <td>${escHtml(v.prazo_inscricao)}</td>
        <td style="font-size:11px;color:var(--muted)">${v.empresa_id.slice(0,8)}…</td></tr>`
    });
  }

  // ── TODOS OS CANDIDATOS ───────────────────────────────────
  function pageTodosCandidatos(container) {
    pageWrap(container, 'Todos os candidatos', 'Consulta geral', `
      <div class="card"><div id="lista-todos-cand">${loadingHtml()}</div></div>
    `);
    (async () => {
      const div = document.getElementById('lista-todos-cand');
      if (!div) return;
      try {
        const data = await apiRequest('GET', '/candidatos/');
        uiTable(div, {
          headers: ['Nome','CPF','Email','Área de interesse','Formação'],
          data: data,
          rowMapper: c => `<tr>
            <td>${escHtml(c.nome)}</td><td>${escHtml(c.cpf)}</td><td>${escHtml(c.email)}</td>
            <td>${escHtml(c.area_interesse)}</td><td>${escHtml(c.nivel_formacao)}</td></tr>`
        });
      } catch(e) { div.innerHTML = emptyHtml(e.message); }
    })();
  }

  // ══════════════════════════════════════════════════════════
  //  EMPRESA
  // ══════════════════════════════════════════════════════════

  function pageCadastrarEmpresa(container) {
    pageWrap(container, 'Cadastrar empresa', 'Inserção em empresa', `
      <div class="card">
        <div class="card-title">Nova empresa</div>
        <div class="form-grid" id="form-empresa">
          <div class="field"><label>Razão social *</label><input id="e-razao_social" placeholder="Razão social"></div>
          <div class="field"><label>Nome fantasia *</label><input id="e-nome_fantasia" placeholder="Nome fantasia"></div>
          <div class="field"><label>CNPJ * (14 dígitos)</label><input id="e-cnpj" placeholder="00000000000000" maxlength="14"></div>
          <div class="field"><label>Senha * (mín. 8 caracteres)</label><input id="e-senha" type="password" placeholder="Senha de acesso"></div>
        </div>
        <div class="form-actions">
          <button class="btn btn-primary" data-accent="${getAccent()}" onclick="criarEmpresa()">Cadastrar</button>
          <button class="btn btn-ghost" onclick="limparForm('form-empresa')">Limpar</button>
        </div>
      </div>
      <div class="card">
        <div class="card-title">Buscar por CNPJ</div>
        <div class="search-row">
          <input id="busca-cnpj" placeholder="CNPJ (14 dígitos)">
          <button class="btn btn-ghost" onclick="buscarEmpresaCnpj()">Buscar</button>
        </div>
        <div id="resultado-cnpj"></div>
      </div>
    `);
  }

  async function criarEmpresa() {
    const body = getFormData('form-empresa');
    if (!body.razao_social || !body.nome_fantasia || !body.cnpj || !body.senha)
      return showToast('Preencha todos os campos obrigatórios', 'error');
    try {
      await apiRequest('POST', '/empresas/', body);
      showToast('Empresa cadastrada!');
      limparForm('form-empresa');
    } catch(e) { showToast(e.message, 'error'); }
  }

  async function buscarEmpresaCnpj() {
    const cnpj = document.getElementById('busca-cnpj').value.trim();
    if (!cnpj) return;
    const div = document.getElementById('resultado-cnpj');
    div.innerHTML = loadingHtml();
    try {
      // Rota correta: /empresas/cnpj/{cnpj}
      const data = await apiRequest('GET', `/empresas/cnpj/${cnpj}`);
      uiTable(div, {
        headers: ['Razão social','Nome fantasia','CNPJ'],
        data: [data],
        rowMapper: e => `<tr>
          <td>${escHtml(e.razao_social)}</td><td>${escHtml(e.nome_fantasia)}</td><td>${escHtml(e.cnpj)}</td></tr>`
      });
    } catch(e) { div.innerHTML = emptyHtml(e.message); }
  }

  // ── VAGAS POR EMPRESA ─────────────────────────────────────
  function pageMinhasVagas(container) {
    pageWrap(container, 'Vagas por empresa', 'Consulta parametrizada', `
      <div class="card">
        <div class="search-row">
          <input id="busca-eid-vagas" placeholder="UUID da empresa">
          <button class="btn btn-ghost" onclick="buscarVagasEmpresa()">Buscar</button>
        </div>
        <div id="lista-minhas-vagas">${emptyHtml('Informe o UUID da empresa')}</div>
      </div>
    `);
  }

  async function buscarVagasEmpresa() {
    const id = document.getElementById('busca-eid-vagas').value.trim();
    if (!id) return;
    const div = document.getElementById('lista-minhas-vagas');
    div.innerHTML = loadingHtml();
    try {
      const data = await apiRequest('GET', `/vagas/${id}`);
      renderListaVagas(div, Array.isArray(data) ? data : [data]);
    } catch(e) { div.innerHTML = emptyHtml(e.message); }
  }

  // ── NOVA VAGA ─────────────────────────────────────────────
  function pageCadastrarVaga(container) {
    pageWrap(container, 'Nova vaga', 'Inserção em vaga', `
      <div class="card">
        <div class="card-title">Publicar vaga</div>
        <div class="form-grid" id="form-vaga">
          <div class="field"><label>Título *</label><input id="v-titulo" placeholder="Ex: Dev Fullstack"></div>
          <div class="field"><label>Empresa ID *</label><input id="v-empresa_id" placeholder="UUID da empresa"></div>
          <div class="field"><label>Modalidade</label>
            <select id="v-modalidade"><option value="0">Presencial</option><option value="1">Remoto</option><option value="2">Híbrido</option></select>
          </div>
          <div class="field"><label>Tipo</label>
            <select id="v-tipo"><option value="0">Emprego</option><option value="1">Estágio</option><option value="2">Trainee</option></select>
          </div>
          <div class="field"><label>Prazo de inscrição *</label><input id="v-prazo_inscricao" type="date"></div>
          <div class="field"><label>Localidade</label><input id="v-localidade" placeholder="Ex: Juazeiro do Norte - CE"></div>
          <div class="field"><label>Jornada</label><input id="v-jornada" placeholder="Ex: 40h semanais"></div>
          <div class="field" style="grid-column:1/-1">
            <label>Descrição</label>
            <textarea id="v-descricao" rows="3" placeholder="Descrição da vaga..." style="resize:vertical"></textarea>
          </div>
        </div>
        <div class="form-actions">
          <button class="btn btn-primary" data-accent="${getAccent()}" onclick="criarVaga()">Publicar</button>
        </div>
      </div>
    `);
  }

  async function criarVaga() {
    const body = getFormData('form-vaga');
    if (!body.titulo || !body.empresa_id || !body.prazo_inscricao)
      return showToast('Preencha os campos obrigatórios', 'error');
    try {
      await apiRequest('POST', '/vagas/', body);
      showToast('Vaga publicada!');
      limparForm('form-vaga');
    } catch(e) { showToast(e.message, 'error'); }
  }

  // ── FILTRAR CANDIDATURAS (múltiplos parâmetros) ───────────
  function pageCandidatosPorVaga(container) {
    pageWrap(container, 'Filtrar candidaturas', 'Consulta com múltiplos parâmetros: status + datas', `
      <div class="card">
        <div class="card-title">Filtro (status + intervalo de datas)</div>
        <div class="form-grid" id="form-filtro-cand">
          <div class="field"><label>Status</label>
            <select id="f-status">
              <option value="0">Enviado</option><option value="1">Em análise</option>
              <option value="2">Aceito</option><option value="3">Recusado</option><option value="4">Cancelado</option>
            </select>
          </div>
          <div class="field"><label>Data início</label><input id="f-data_inicio" type="datetime-local"></div>
          <div class="field"><label>Data fim</label><input id="f-data_fim" type="datetime-local"></div>
        </div>
        <div class="form-actions">
          <button class="btn btn-primary" data-accent="${getAccent()}" onclick="filtrarCandidaturas()">Filtrar</button>
        </div>
        <div id="lista-filtro" style="margin-top:16px"></div>
      </div>
    `);
  }

  async function filtrarCandidaturas() {
    const f = getFormData('form-filtro-cand');
    if (!f.data_inicio || !f.data_fim) return showToast('Informe as datas', 'error');
    const div = document.getElementById('lista-filtro');
    div.innerHTML = loadingHtml();
    // Rota correta: /candidaturas/filtro?status=&data_inicio=&data_fim=
    const params = new URLSearchParams({
      status: f.status,
      data_inicio: f.data_inicio.replace('T',' ') + ':00',
      data_fim: f.data_fim.replace('T',' ') + ':00',
    });
    try {
      const data = await apiRequest('GET', `/candidaturas/filtro?${params}`);
      renderListaCandidaturas(div, data);
    } catch(e) { div.innerHTML = emptyHtml(e.message); }
  }

  // ── TODAS AS EMPRESAS ─────────────────────────────────────
  function pageTodasEmpresas(container) {
    pageWrap(container, 'Todas as empresas', 'Consulta geral', `
      <div class="card"><div id="lista-todas-emp">${loadingHtml()}</div></div>
    `);
    (async () => {
      const div = document.getElementById('lista-todas-emp');
      if (!div) return;
      try {
        const data = await apiRequest('GET', '/empresas/');
        uiTable(div, {
          headers: ['Razão social','Nome fantasia','CNPJ'],
          data: data,
          rowMapper: e => `<tr>
            <td>${escHtml(e.razao_social)}</td><td>${escHtml(e.nome_fantasia)}</td><td>${escHtml(e.cnpj)}</td></tr>`
        });
      } catch(e) { div.innerHTML = emptyHtml(e.message); }
    })();
  }

  // ══════════════════════════════════════════════════════════
  //  INSTITUIÇÃO
  // ══════════════════════════════════════════════════════════

  function pageCadastrarInstituicao(container) {
    pageWrap(container, 'Cadastrar instituição', 'Inserção em instituicao_ensino', `
      <div class="card">
        <div class="card-title">Nova instituição</div>
        <div class="form-grid" id="form-inst">
          <div class="field"><label>Razão social *</label><input id="i-razao_social" placeholder="Razão social"></div>
          <div class="field"><label>Registro educacional *</label><input id="i-registro_educacional" placeholder="MEC-12345"></div>
          <div class="field"><label>Nome fantasia</label><input id="i-nome_fantasia" placeholder="Nome fantasia"></div>
          <div class="field"><label>CNPJ (14 dígitos)</label><input id="i-cnpj" placeholder="00000000000000" maxlength="14"></div>
          <div class="field"><label>Tipo</label><input id="i-tipo" placeholder="Ex: Federal, Privada"></div>
        </div>
        <div class="form-actions">
          <button class="btn btn-primary" data-accent="${getAccent()}" onclick="criarInstituicao()">Cadastrar</button>
          <button class="btn btn-ghost" onclick="limparForm('form-inst')">Limpar</button>
        </div>
      </div>
      <div class="card">
        <div class="card-title">Buscar por registro educacional</div>
        <div class="search-row">
          <input id="busca-reg" placeholder="Código do registro">
          <button class="btn btn-ghost" onclick="buscarInstituicaoPorRegistro()">Buscar</button>
        </div>
        <div id="resultado-inst"></div>
      </div>
    `);
  }

  async function criarInstituicao() {
    const body = getFormData('form-inst');
    if (!body.razao_social || !body.registro_educacional)
      return showToast('Preencha os campos obrigatórios', 'error');
    try {
      await apiRequest('POST', '/instituicoes-ensino/', body);
      showToast('Instituição cadastrada!');
      limparForm('form-inst');
    } catch(e) { showToast(e.message, 'error'); }
  }

  async function buscarInstituicaoPorRegistro() {
    const reg = document.getElementById('busca-reg').value.trim();
    if (!reg) return;
    const div = document.getElementById('resultado-inst');
    div.innerHTML = loadingHtml();
    try {
      const data = await apiRequest('GET', `/instituicoes-ensino/registro/${reg}`);
      uiTable(div, {
        headers: ['Razão social','Registro','CNPJ','Tipo'],
        data: [data],
        rowMapper: i => `<tr>
          <td>${escHtml(i.razao_social)}</td><td>${escHtml(i.registro_educacional)}</td>
          <td>${escHtml(i.cnpj)}</td><td>${escHtml(i.tipo)}</td></tr>`
      });
    } catch(e) { div.innerHTML = emptyHtml(e.message); }
  }

  // ── CURSOS ────────────────────────────────────────────────
  function pageMeusCursos(container) {
    pageWrap(container, 'Cursos por instituição', 'Consulta parametrizada', `
      <div class="card">
        <div class="search-row">
          <input id="busca-iid-cursos" placeholder="UUID da instituição">
          <button class="btn btn-ghost" onclick="buscarCursosInstituicao()">Buscar</button>
          <button class="btn btn-ghost" onclick="listarTodosCursos()">Listar todos</button>
        </div>
        <div id="lista-cursos">${emptyHtml('Informe o UUID ou liste todos')}</div>
      </div>
    `);
  }

  async function buscarCursosInstituicao() {
    const id = document.getElementById('busca-iid-cursos').value.trim();
    if (!id) return;
    const div = document.getElementById('lista-cursos');
    div.innerHTML = loadingHtml();
    try {
      // /cursos/{instituicao_id} bate na rota list_by_instituicao (primeira da lista)
      const data = await apiRequest('GET', `/cursos/${id}`);
      renderListaCursos(div, Array.isArray(data) ? data : [data]);
    } catch(e) { div.innerHTML = emptyHtml(e.message); }
  }

  async function listarTodosCursos() {
    const div = document.getElementById('lista-cursos');
    if (!div) return;
    div.innerHTML = loadingHtml();
    try {
      const data = await apiRequest('GET', '/cursos/');
      renderListaCursos(div, data);
    } catch(e) { div.innerHTML = emptyHtml(e.message); }
  }

  function renderListaCursos(div, data) {
    uiTable(div, {
      headers: ['Nome','Modalidade','Área','Carga horária','Prazo'],
      data: data,
      rowMapper: c => `<tr>
        <td>${escHtml(c.nome)}</td>
        <td><span class="badge badge-gray">${MODALIDADE[c.modalidade] ?? c.modalidade}</span></td>
        <td>${escHtml(c.area)}</td>
        <td>${c.carga_horaria ? c.carga_horaria+'h' : '—'}</td>
        <td>${escHtml(c.prazo_inscricao)}</td></tr>`
    });
  }

  function pageCadastrarCurso(container) {
    pageWrap(container, 'Novo curso', 'Inserção em curso', `
      <div class="card">
        <div class="card-title">Publicar curso</div>
        <div class="form-grid" id="form-curso">
          <div class="field"><label>Nome *</label><input id="cu-nome" placeholder="Nome do curso"></div>
          <div class="field"><label>Instituição ID *</label><input id="cu-instituicao_ensino_id" placeholder="UUID da instituição"></div>
          <div class="field"><label>Modalidade</label>
            <select id="cu-modalidade"><option value="0">Presencial</option><option value="1">Remoto</option><option value="2">Híbrido</option></select>
          </div>
          <div class="field"><label>Área</label><input id="cu-area" placeholder="Ex: TI, Saúde"></div>
          <div class="field"><label>Carga horária (h)</label><input id="cu-carga_horaria" type="number" placeholder="40"></div>
          <div class="field"><label>Capacidade</label><input id="cu-capacidade" type="number" placeholder="30"></div>
          <div class="field"><label>Prazo de inscrição</label><input id="cu-prazo_inscricao" type="date"></div>
          <div class="field"><label>Empresa parceira (ID)</label><input id="cu-empresa_id" placeholder="UUID (opcional)"></div>
        </div>
        <div class="form-actions">
          <button class="btn btn-primary" data-accent="${getAccent()}" onclick="criarCurso()">Publicar</button>
        </div>
      </div>
    `);
  }

  async function criarCurso() {
    const body = getFormData('form-curso');
    if (!body.nome || !body.instituicao_ensino_id)
      return showToast('Preencha os campos obrigatórios', 'error');
    try {
      await apiRequest('POST', '/cursos/', body);
      showToast('Curso publicado!');
      limparForm('form-curso');
    } catch(e) { showToast(e.message, 'error'); }
  }

  // ── ÁREAS DE ENSINO ───────────────────────────────────────
  function pageAreasEnsino(container) {
    pageWrap(container, 'Áreas de ensino', 'Gerenciar e associar áreas (N:N)', `
      <div class="card">
        <div class="card-title">Nova área de ensino</div>
        <div class="form-grid" id="form-nova-area">
          <div class="field"><label>Nome *</label><input id="ae-nome" placeholder="Ex: Tecnologia da Informação"></div>
        </div>
        <div class="form-actions">
          <button class="btn btn-primary" data-accent="${getAccent()}" onclick="criarAreaEnsino()">Cadastrar</button>
        </div>
      </div>
      <div class="card">
        <div class="card-title">Associar área à instituição (N:N)</div>
        <div class="form-grid" id="form-assoc-area">
          <div class="field"><label>Instituição ID</label><input id="ae-instituicao_ensino_id" placeholder="UUID da instituição"></div>
          <div class="field"><label>Área de ensino ID</label><input id="ae-area_ensino_id" placeholder="UUID da área"></div>
        </div>
        <div class="form-actions">
          <button class="btn btn-primary" data-accent="${getAccent()}" onclick="associarAreaInstituicao()">Associar</button>
        </div>
      </div>
      <div class="card">
        <div class="card-title">Todas as áreas</div>
        <div id="lista-areas">${loadingHtml()}</div>
      </div>
    `);
    carregarAreas();
  }

  async function criarAreaEnsino() {
    const body = getFormData('form-nova-area');
    if (!body.nome) return showToast('Informe o nome', 'error');
    try {
      await apiRequest('POST', '/areas-ensino/', body);
      showToast('Área cadastrada!');
      carregarAreas();
    } catch(e) { showToast(e.message, 'error'); }
  }

  async function associarAreaInstituicao() {
    const body = getFormData('form-assoc-area');
    if (!body.instituicao_ensino_id || !body.area_ensino_id)
      return showToast('Preencha os IDs', 'error');
    try {
      await apiRequest('POST', '/instituicoes-area-ensino/', body);
      showToast('Associação criada!');
    } catch(e) { showToast(e.message, 'error'); }
  }

  async function carregarAreas() {
    const div = document.getElementById('lista-areas');
    if (!div) return;
    try {
      const data = await apiRequest('GET', '/areas-ensino/');
      uiTable(div, {
        headers: ['ID','Nome'],
        data: data,
        rowMapper: a => `<tr>
          <td style="font-size:11px;color:var(--muted);font-family:monospace">${a.id}</td>
          <td>${escHtml(a.nome)}</td></tr>`
      });
    } catch(e) { div.innerHTML = emptyHtml(e.message); }
  }

  // ── TODAS AS INSTITUIÇÕES ─────────────────────────────────
  function pageTodasInstituicoes(container) {
    pageWrap(container, 'Todas as instituições', 'Consulta geral', `
      <div class="card"><div id="lista-todas-inst">${loadingHtml()}</div></div>
    `);
    (async () => {
      const div = document.getElementById('lista-todas-inst');
      if (!div) return;
      try {
        const data = await apiRequest('GET', '/instituicoes-ensino/');
        uiTable(div, {
          headers: ['Razão social','Registro','CNPJ','Tipo'],
          data: data,
          rowMapper: i => `<tr>
            <td>${escHtml(i.razao_social)}</td><td>${escHtml(i.registro_educacional)}</td>
            <td>${escHtml(i.cnpj)}</td><td>${escHtml(i.tipo)}</td></tr>`
        });
      } catch(e) { div.innerHTML = emptyHtml(e.message); }
    })();
  }

  // ── EXPORTS ───────────────────────────────────────────────
  Object.assign(window, {
    switchProfile, navigateTo,
    criarCandidato, limparForm, buscarPorCpf,
    criarCandidatura, buscarCandidaturas, carregarTodasCandidaturas,
    abrirModalStatus, confirmStatusUpdate, closeModal,
    criarCompetenciaCandidato, buscarCompetenciasCandidato, listarTodasCompetencias,
    criarInscricao, buscarInscricoes,
    buscarVagas, listarTodasVagas,
    criarEmpresa, buscarEmpresaCnpj, buscarVagasEmpresa,
    criarVaga, filtrarCandidaturas,
    criarInstituicao, buscarInstituicaoPorRegistro,
    buscarCursosInstituicao, listarTodosCursos,
    criarCurso, criarAreaEnsino, associarAreaInstituicao,
    abrirDocs
  });

  checkApiHealth();
  switchProfile('candidato');
})();