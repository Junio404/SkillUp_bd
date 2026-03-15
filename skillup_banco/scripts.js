const API = 'http://localhost:8000';

// Utils
async function api(method, path, body) {
  try {
    const opts = { method, headers: { 'Content-Type': 'application/json' } };
    if (body) opts.body = JSON.stringify(body);
    const r = await fetch(API + path, opts);
    if (!r.ok) {
      const err = await r.json().catch(() => ({}));
      throw new Error(err.detail || `Erro ${r.status}`);
    }
    return r.status === 204 ? null : r.json();
  } catch(e) {
    throw e;
  }
}

function toast(msg, type='success') {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.className = `show ${type}`;
  setTimeout(() => t.className = '', 3000);
}

function escHtml(s) {
  if (s == null) return '—';
  return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

function openModal(id) { document.getElementById(id).classList.add('open'); }
function closeModal(id) { document.getElementById(id).classList.remove('open'); }

// Status Helpers
const STATUS_CAND = ['Enviado','Em análise','Aceito','Recusado','Cancelado'];
const STATUS_INS  = ['Deferido','Indeferido'];
const MODALIDADE  = ['Presencial','Remoto','Híbrido'];
const TIPO_VAGA   = ['Emprego','Estágio','Trainee'];
const NIVEL       = ['Baixa','Média','Alta'];

function badgeCand(s) {
  const cls = ['badge-gray','badge-purple','badge-green','badge-orange','badge-gray'][s] || 'badge-gray';
  return `<span class="badge ${cls}">${STATUS_CAND[s] || s}</span>`;
}

// Check API
async function checkApi() {
  try {
    await fetch(API + '/candidatos/', { signal: AbortSignal.timeout(2000) });
    document.getElementById('api-dot').classList.add('online');
    document.getElementById('api-status').textContent = 'API online';
  } catch {
    const apiStatus = document.getElementById('api-status');
    if (apiStatus) apiStatus.textContent = 'API offline';
  }
}
checkApi();

// Profiles
const PROFILES = {
  candidato: {
    accent: 'c',
    nav: [
      { id: 'meu-perfil',       icon: '◈', label: 'Meu perfil' },
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
      { id: 'empresa-perfil',   icon: '◈', label: 'Perfil da empresa' },
      { id: 'minhas-vagas',     icon: '◎', label: 'Minhas vagas' },
      { id: 'nova-vaga',        icon: '◆', label: 'Nova vaga' },
      { id: 'candidatos-vaga',  icon: '◉', label: 'Candidatos por vaga' },
      { id: 'todas-empresas',   icon: '▣', label: 'Todas empresas' },
    ]
  },
  instituicao: {
    accent: 'i',
    nav: [
      { id: 'inst-perfil',      icon: '◈', label: 'Perfil' },
      { id: 'meus-cursos',      icon: '◎', label: 'Meus cursos' },
      { id: 'novo-curso',       icon: '◆', label: 'Novo curso' },
      { id: 'areas-ensino',     icon: '◉', label: 'Áreas de ensino' },
      { id: 'todas-inst',       icon: '▣', label: 'Todas instituições' },
    ]
  }
};

let currentProfile = 'candidato';
let currentNav = 'meu-perfil';

function switchProfile(p) {
  currentProfile = p;
  document.querySelectorAll('.profile-tab').forEach(t => {
    t.classList.toggle('active', t.dataset.profile === p);
  });
  const first = PROFILES[p].nav[0].id;
  renderSidebar();
  navigateTo(first);
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

function navigateTo(id) {
  currentNav = id;
  renderSidebar();
  renderPage(id);
}

// Page Router
function renderPage(id) {
  const pages = {
    // CANDIDATO
    'meu-perfil':       pageCadastrarCandidato,
    'candidaturas':     pageCandidaturas,
    'competencias-meu': pageCompetenciasCandidato,
    'inscricoes':       pageInscricoes,
    'vagas':            pageVagas,
    'todos-candidatos': pageTodosCandidatos,
    // EMPRESA
    'empresa-perfil':   pageCadastrarEmpresa,
    'minhas-vagas':     pageMinhasVagas,
    'nova-vaga':        pageCadastrarVaga,
    'candidatos-vaga':  pageCandidatosPorVaga,
    'todas-empresas':   pageTodasEmpresas,
    // INSTITUICAO
    'inst-perfil':      pageCadastrarInstituicao,
    'meus-cursos':      pageMeusCursos,
    'novo-curso':       pageCadastrarCurso,
    'areas-ensino':     pageAreasEnsino,
    'todas-inst':       pageTodasInstituicoes,
  };
  const fn = pages[id];
  const main = document.getElementById('main-content');
  if (!main) return;
  main.innerHTML = '';
  if (fn) fn(main);
}

// Helpers UI
function pageWrap(container, title, subtitle, html) {
  container.innerHTML = `
    <div class="page active">
      <div class="page-header">
        <div>
          <div class="page-title">${title}</div>
          <div class="page-sub">${subtitle}</div>
        </div>
      </div>
      ${html}
    </div>`;
}

function loadingHtml() {
  return `<div class="loading"><div class="spinner"></div>Carregando...</div>`;
}

function emptyHtml(msg='Nenhum registro encontrado') {
  return `<div class="empty"><div class="empty-icon">◫</div>${msg}</div>`;
}

const accent = () => PROFILES[currentProfile].accent;

//  Candidato Pages

function pageCadastrarCandidato(container) {
  pageWrap(container, 'Cadastrar candidato', 'Inserção em candidato', `
    <div class="card">
      <div class="card-title">Novo candidato</div>
      <div class="form-grid" id="form-candidato">
        <div class="field"><label>Nome *</label><input id="c-nome" placeholder="Nome completo"></div>
        <div class="field"><label>CPF * (11 dígitos)</label><input id="c-cpf" placeholder="00000000000" maxlength="11"></div>
        <div class="field"><label>Email *</label><input id="c-email" type="email" placeholder="email@exemplo.com"></div>
        <div class="field"><label>Área de interesse</label><input id="c-area" placeholder="Ex: Desenvolvimento Web"></div>
        <div class="field"><label>Nível de formação</label><input id="c-nivel" placeholder="Ex: Bacharel"></div>
        <div class="field"><label>URL do currículo</label><input id="c-curriculo" placeholder="https://..."></div>
      </div>
      <div class="form-actions">
        <button class="btn btn-primary" data-accent="${accent()}" onclick="criarCandidato()">Cadastrar</button>
        <button class="btn btn-ghost" onclick="limparCandidato()">Limpar</button>
      </div>
    </div>
    <div class="card">
      <div class="card-title">Buscar por CPF</div>
      <div class="search-row">
        <input id="busca-cpf" placeholder="Digite o CPF (11 dígitos)">
        <button class="btn btn-ghost" onclick="buscarPorCpf()">Buscar</button>
      </div>
      <div id="resultado-cpf"></div>
    </div>
  `);
}

async function criarCandidato() {
  const body = {
    nome: document.getElementById('c-nome').value,
    cpf: document.getElementById('c-cpf').value,
    email: document.getElementById('c-email').value,
    area_interesse: document.getElementById('c-area').value || null,
    nivel_formacao: document.getElementById('c-nivel').value || null,
    curriculo_url: document.getElementById('c-curriculo').value || null,
  };
  if (!body.nome || !body.cpf || !body.email) return toast('Preencha os campos obrigatórios', 'error');
  try {
    await api('POST', '/candidatos/', body);
    toast('Candidato cadastrado!');
    limparCandidato();
  } catch(e) { toast(e.message, 'error'); }
}

function limparCandidato() {
  ['c-nome','c-cpf','c-email','c-area','c-nivel','c-curriculo'].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.value = '';
  });
}

async function buscarPorCpf() {
  const cpf = document.getElementById('busca-cpf').value.trim();
  if (!cpf) return;
  const div = document.getElementById('resultado-cpf');
  div.innerHTML = loadingHtml();
  try {
    const data = await api('GET', `/candidatos/${cpf}`);
    div.innerHTML = `
      <table><thead><tr>
        <th>Nome</th><th>CPF</th><th>Email</th><th>Área</th><th>Formação</th>
      </tr></thead><tbody><tr>
        <td>${escHtml(data.nome)}</td>
        <td>${escHtml(data.cpf)}</td>
        <td>${escHtml(data.email)}</td>
        <td>${escHtml(data.area_interesse)}</td>
        <td>${escHtml(data.nivel_formacao)}</td>
      </tr></tbody></table>`;
  } catch(e) { div.innerHTML = emptyHtml(e.message); }
}

// Candidaturas
function pageCandidaturas(container) {
  pageWrap(container, 'Candidaturas', 'Criar candidatura e acompanhar status', `
    <div class="card">
      <div class="card-title">Nova candidatura</div>
      <div class="form-grid">
        <div class="field"><label>ID do candidato</label><input id="cand-cid" placeholder="UUID do candidato"></div>
        <div class="field"><label>ID da vaga</label><input id="cand-vid" placeholder="UUID da vaga"></div>
        <div class="field"><label>Status inicial</label>
          <select id="cand-status">
            <option value="0">Enviado</option>
            <option value="1">Em análise</option>
          </select>
        </div>
      </div>
      <div class="form-actions">
        <button class="btn btn-primary" data-accent="${accent()}" onclick="criarCandidatura()">Cadastrar candidatura</button>
      </div>
    </div>
    <div class="card">
      <div class="card-title">Candidaturas por candidato</div>
      <div class="search-row">
        <input id="busca-cand-id" placeholder="UUID do candidato">
        <button class="btn btn-ghost" onclick="buscarCandidaturas()">Buscar</button>
      </div>
      <div id="lista-candidaturas">${loadingHtml()}</div>
    </div>
  `);
  carregarTodasCandidaturas();
}

async function criarCandidatura() {
  const body = {
    candidato_id: document.getElementById('cand-cid').value,
    vaga_id: document.getElementById('cand-vid').value,
    status: parseInt(document.getElementById('cand-status').value),
    data_candidatura: new Date().toISOString(),
  };
  if (!body.candidato_id || !body.vaga_id) return toast('Preencha ID do candidato e da vaga', 'error');
  try {
    await api('POST', '/candidaturas/', body);
    toast('Candidatura criada!');
    carregarTodasCandidaturas();
  } catch(e) { toast(e.message, 'error'); }
}

async function carregarTodasCandidaturas() {
  const div = document.getElementById('lista-candidaturas');
  if (!div) return;
  div.innerHTML = loadingHtml();
  try {
    const data = await api('GET', '/candidaturas/');
    renderTabelaCandidaturas(div, data);
  } catch(e) { div.innerHTML = emptyHtml(e.message); }
}

async function buscarCandidaturas() {
  const id = document.getElementById('busca-cand-id').value.trim();
  if (!id) { carregarTodasCandidaturas(); return; }
  const div = document.getElementById('lista-candidaturas');
  div.innerHTML = loadingHtml();
  try {
    const data = await api('GET', `/candidaturas/${id}`);
    renderTabelaCandidaturas(div, data);
  } catch(e) { div.innerHTML = emptyHtml(e.message); }
}

let editandoCandidaturaId = null;

function renderTabelaCandidaturas(div, data) {
  if (!data || !data.length) { div.innerHTML = emptyHtml(); return; }
  div.innerHTML = `<div class="table-wrap"><table><thead><tr>
    <th>ID</th><th>Data</th><th>Status</th><th>Vaga ID</th><th>Ação</th>
  </tr></thead><tbody>${data.map(c => `
    <tr>
      <td style="font-size:11px;color:var(--muted)">${c.id.slice(0,8)}…</td>
      <td>${new Date(c.data_candidatura).toLocaleDateString('pt-BR')}</td>
      <td>${badgeCand(c.status)}</td>
      <td style="font-size:11px;color:var(--muted)">${c.vaga_id.slice(0,8)}…</td>
      <td><button class="btn btn-ghost" style="font-size:11px;padding:4px 10px"
        onclick="abrirModalStatus('${c.id}', ${c.status})">Atualizar status</button></td>
    </tr>`).join('')}</tbody></table></div>`;
}

function abrirModalStatus(id, statusAtual) {
  editandoCandidaturaId = id;
  const modalSelect = document.getElementById('modal-status-select');
  if (modalSelect) modalSelect.value = statusAtual;
  openModal('modal-status');
}

async function confirmStatusUpdate() {
  const novo = parseInt(document.getElementById('modal-status-select').value);
  try {
    await api('PATCH', `/candidaturas/${editandoCandidaturaId}/status?novo_status=${novo}`);
    toast('Status atualizado!');
    closeModal('modal-status');
    carregarTodasCandidaturas();
  } catch(e) { toast(e.message, 'error'); }
}

// Competências do candidato
function pageCompetenciasCandidato(container) {
  pageWrap(container, 'Minhas competências', 'Inserção N:N: candidato × competência', `
    <div class="card">
      <div class="card-title">Associar competência a candidato</div>
      <div class="form-grid">
        <div class="field"><label>ID do candidato</label><input id="cc-cid" placeholder="UUID do candidato"></div>
        <div class="field"><label>ID da competência</label><input id="cc-compid" placeholder="UUID da competência"></div>
        <div class="field"><label>Nível</label>
          <select id="cc-nivel">
            <option value="0">Baixa</option><option value="1">Média</option><option value="2">Alta</option>
          </select>
        </div>
      </div>
      <div class="form-actions">
        <button class="btn btn-primary" data-accent="${accent()}" onclick="criarCompetenciaCandidato()">Associar</button>
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
  const body = {
    candidato_id: document.getElementById('cc-cid').value,
    competencia_id: document.getElementById('cc-compid').value,
    nivel: parseInt(document.getElementById('cc-nivel').value),
  };
  if (!body.candidato_id || !body.competencia_id) return toast('Preencha os IDs', 'error');
  try {
    await api('POST', '/competencias-candidato/', body);
    toast('Competência associada!');
  } catch(e) { toast(e.message, 'error'); }
}

async function buscarCompetenciasCandidato() {
  const id = document.getElementById('busca-cc-id').value.trim();
  if (!id) return toast('Informe o ID do candidato', 'error');
  const div = document.getElementById('lista-comp-cand');
  div.innerHTML = loadingHtml();
  try {
    const data = await api('GET', `/competencias-candidato/${id}`);
    renderTabelaCompCand(div, data);
  } catch(e) { div.innerHTML = emptyHtml(e.message); }
}

async function listarTodasCompetencias() {
  const div = document.getElementById('lista-comp-cand');
  div.innerHTML = loadingHtml();
  try {
    const data = await api('GET', '/competencias-candidato/');
    renderTabelaCompCand(div, data);
  } catch(e) { div.innerHTML = emptyHtml(e.message); }
}

function renderTabelaCompCand(div, data) {
  if (!data || !data.length) { div.innerHTML = emptyHtml(); return; }
  div.innerHTML = `<div class="table-wrap"><table><thead><tr>
    <th>Competência ID</th><th>Candidato ID</th><th>Nível</th>
  </tr></thead><tbody>${data.map(c => `<tr>
    <td style="font-size:11px">${c.competencia_id.slice(0,8)}…</td>
    <td style="font-size:11px">${c.candidato_id.slice(0,8)}…</td>
    <td><span class="badge badge-purple">${NIVEL[c.nivel]||c.nivel}</span></td>
  </tr>`).join('')}</tbody></table></div>`;
}

// Inscrições em cursos
function pageInscricoes(container) {
  pageWrap(container, 'Cursos inscritos', 'Inscrição em cursos disponíveis', `
    <div class="card">
      <div class="card-title">Nova inscrição</div>
      <div class="form-grid">
        <div class="field"><label>ID do candidato</label><input id="ic-cid" placeholder="UUID do candidato"></div>
        <div class="field"><label>ID do curso</label><input id="ic-curid" placeholder="UUID do curso"></div>
        <div class="field"><label>Status</label>
          <select id="ic-status"><option value="0">Deferido</option><option value="1">Indeferido</option></select>
        </div>
      </div>
      <div class="form-actions">
        <button class="btn btn-primary" data-accent="${accent()}" onclick="criarInscricao()">Inscrever</button>
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
  const body = {
    candidato_id: document.getElementById('ic-cid').value,
    curso_id: document.getElementById('ic-curid').value,
    status: parseInt(document.getElementById('ic-status').value),
    data_inscricao: new Date().toISOString().slice(0,10),
  };
  if (!body.candidato_id || !body.curso_id) return toast('Preencha os IDs', 'error');
  try {
    await api('POST', '/inscricoes-curso/', body);
    toast('Inscrição realizada!');
  } catch(e) { toast(e.message, 'error'); }
}

async function buscarInscricoes() {
  const id = document.getElementById('busca-ic-id').value.trim();
  if (!id) return;
  const div = document.getElementById('lista-inscricoes');
  div.innerHTML = loadingHtml();
  try {
    const data = await api('GET', `/inscricoes-curso/${id}`);
    if (!data || !data.length) { div.innerHTML = emptyHtml(); return; }
    div.innerHTML = `<div class="table-wrap"><table><thead><tr>
      <th>Curso ID</th><th>Data inscrição</th><th>Status</th>
    </tr></thead><tbody>${data.map(i => `<tr>
      <td style="font-size:11px">${i.curso_id.slice(0,8)}…</td>
      <td>${i.data_inscricao}</td>
      <td><span class="badge ${i.status===0?'badge-green':'badge-orange'}">${STATUS_INS[i.status]||i.status}</span></td>
    </tr>`).join('')}</tbody></table></div>`;
  } catch(e) { div.innerHTML = emptyHtml(e.message); }
}

// Vagas (busca)
function pageVagas(container) {
  pageWrap(container, 'Buscar vagas', 'Consulta parametrizável de vagas', `
    <div class="card">
      <div class="card-title">Filtrar vagas</div>
      <div class="search-row">
        <input id="busca-empresa-vagas" placeholder="UUID da empresa (opcional)">
        <button class="btn btn-ghost" onclick="buscarVagas()">Buscar</button>
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
    const data = await api('GET', '/vagas/');
    renderTabelaVagas(div, data);
  } catch(e) { div.innerHTML = emptyHtml(e.message); }
}

async function buscarVagas() {
  const eid = document.getElementById('busca-empresa-vagas').value.trim();
  const div = document.getElementById('lista-vagas');
  div.innerHTML = loadingHtml();
  try {
    const data = await api('GET', eid ? `/vagas/${eid}` : '/vagas/');
    renderTabelaVagas(div, Array.isArray(data) ? data : [data]);
  } catch(e) { div.innerHTML = emptyHtml(e.message); }
}

function renderTabelaVagas(div, data) {
  if (!data || !data.length) { div.innerHTML = emptyHtml(); return; }
  div.innerHTML = `<div class="table-wrap"><table><thead><tr>
    <th>Título</th><th>Modalidade</th><th>Tipo</th><th>Prazo</th><th>Empresa</th>
  </tr></thead><tbody>${data.map(v => `<tr>
    <td>${escHtml(v.titulo)}</td>
    <td><span class="badge badge-gray">${MODALIDADE[v.modalidade]||v.modalidade}</span></td>
    <td><span class="badge badge-purple">${TIPO_VAGA[v.tipo]||v.tipo}</span></td>
    <td>${escHtml(v.prazo_inscricao)}</td>
    <td style="font-size:11px;color:var(--muted)">${v.empresa_id.slice(0,8)}…</td>
  </tr>`).join('')}</tbody></table></div>`;
}

// Todos os candidatos
function pageTodosCandidatos(container) {
  pageWrap(container, 'Todos os candidatos', 'Consulta geral', `
    <div class="card">
      <div id="lista-todos-cand">${loadingHtml()}</div>
    </div>
  `);
  (async () => {
    const div = document.getElementById('lista-todos-cand');
    if (!div) return;
    try {
      const data = await api('GET', '/candidatos/');
      if (!data || !data.length) { div.innerHTML = emptyHtml(); return; }
      div.innerHTML = `<div class="table-wrap"><table><thead><tr>
        <th>Nome</th><th>CPF</th><th>Email</th><th>Área</th><th>Formação</th>
      </tr></thead><tbody>${data.map(c => `<tr>
        <td>${escHtml(c.nome)}</td>
        <td>${escHtml(c.cpf)}</td>
        <td>${escHtml(c.email)}</td>
        <td>${escHtml(c.area_interesse)}</td>
        <td>${escHtml(c.nivel_formacao)}</td>
      </tr>`).join('')}</tbody></table></div>`;
    } catch(e) { div.innerHTML = emptyHtml(e.message); }
  })();
}

//  Empresa Pages

function pageCadastrarEmpresa(container) {
  pageWrap(container, 'Cadastrar empresa', 'Inserção em empresa', `
    <div class="card">
      <div class="card-title">Nova empresa</div>
      <div class="form-grid">
        <div class="field"><label>Razão social *</label><input id="e-razao" placeholder="Razão social"></div>
        <div class="field"><label>Nome fantasia *</label><input id="e-fantasia" placeholder="Nome fantasia"></div>
        <div class="field"><label>CNPJ * (14 dígitos)</label><input id="e-cnpj" placeholder="00000000000000" maxlength="14"></div>
      </div>
      <div class="form-actions">
        <button class="btn btn-primary" data-accent="${accent()}" onclick="criarEmpresa()">Cadastrar</button>
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
  const body = {
    razao_social: document.getElementById('e-razao').value,
    nome_fantasia: document.getElementById('e-fantasia').value,
    cnpj: document.getElementById('e-cnpj').value,
  };
  if (!body.razao_social || !body.nome_fantasia || !body.cnpj) return toast('Preencha todos os campos', 'error');
  try {
    await api('POST', '/empresas/', body);
    toast('Empresa cadastrada!');
    ['e-razao','e-fantasia','e-cnpj'].forEach(id => {
      const el = document.getElementById(id);
      if (el) el.value = '';
    });
  } catch(e) { toast(e.message, 'error'); }
}

async function buscarEmpresaCnpj() {
  const cnpj = document.getElementById('busca-cnpj').value.trim();
  if (!cnpj) return;
  const div = document.getElementById('resultado-cnpj');
  div.innerHTML = loadingHtml();
  try {
    const data = await api('GET', `/empresas/${cnpj}`);
    div.innerHTML = `<table><thead><tr><th>Razão social</th><th>Nome fantasia</th><th>CNPJ</th></tr></thead>
      <tbody><tr>
        <td>${escHtml(data.razao_social)}</td>
        <td>${escHtml(data.nome_fantasia)}</td>
        <td>${escHtml(data.cnpj)}</td>
      </tr></tbody></table>`;
  } catch(e) { div.innerHTML = emptyHtml(e.message); }
}

// ── Minhas vagas ──────────────────────────────────────────
function pageMinhasVagas(container) {
  pageWrap(container, 'Minhas vagas', 'Vagas por empresa', `
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
    const data = await api('GET', `/vagas/${id}`);
    renderTabelaVagas(div, Array.isArray(data) ? data : [data]);
  } catch(e) { div.innerHTML = emptyHtml(e.message); }
}

// Nova vaga
function pageCadastrarVaga(container) {
  pageWrap(container, 'Nova vaga', 'Inserção em vaga', `
    <div class="card">
      <div class="card-title">Publicar vaga</div>
      <div class="form-grid">
        <div class="field"><label>Título *</label><input id="v-titulo" placeholder="Ex: Dev Fullstack"></div>
        <div class="field"><label>Empresa ID *</label><input id="v-eid" placeholder="UUID da empresa"></div>
        <div class="field"><label>Modalidade</label>
          <select id="v-mod"><option value="0">Presencial</option><option value="1">Remoto</option><option value="2">Híbrido</option></select>
        </div>
        <div class="field"><label>Tipo</label>
          <select id="v-tipo"><option value="0">Emprego</option><option value="1">Estágio</option><option value="2">Trainee</option></select>
        </div>
        <div class="field"><label>Prazo de inscrição *</label><input id="v-prazo" type="date"></div>
        <div class="field"><label>Localidade</label><input id="v-local" placeholder="Ex: Juazeiro do Norte - CE"></div>
        <div class="field"><label>Jornada</label><input id="v-jornada" placeholder="Ex: 40h semanais"></div>
        <div class="field" style="grid-column: 1 / -1"><label>Descrição</label>
          <textarea id="v-desc" rows="3" placeholder="Descrição da vaga..." style="resize:vertical"></textarea>
        </div>
      </div>
      <div class="form-actions">
        <button class="btn btn-primary" data-accent="${accent()}" onclick="criarVaga()">Publicar vaga</button>
      </div>
    </div>
  `);
}

async function criarVaga() {
  const body = {
    titulo: document.getElementById('v-titulo').value,
    empresa_id: document.getElementById('v-eid').value,
    modalidade: parseInt(document.getElementById('v-mod').value),
    tipo: parseInt(document.getElementById('v-tipo').value),
    prazo_inscricao: document.getElementById('v-prazo').value,
    localidade: document.getElementById('v-local').value || null,
    jornada: document.getElementById('v-jornada').value || null,
    descricao: document.getElementById('v-desc').value || null,
  };
  if (!body.titulo || !body.empresa_id || !body.prazo_inscricao) return toast('Preencha os campos obrigatórios', 'error');
  try {
    await api('POST', '/vagas/', body);
    toast('Vaga publicada!');
  } catch(e) { toast(e.message, 'error'); }
}

// Candidatos por vaga
function pageCandidatosPorVaga(container) {
  pageWrap(container, 'Candidatos por vaga', 'Consulta com múltiplos parâmetros: status + datas', `
    <div class="card">
      <div class="card-title">Filtrar candidaturas (múltiplos parâmetros)</div>
      <div class="form-grid">
        <div class="field"><label>Status</label>
          <select id="filtro-status">
            <option value="0">Enviado</option><option value="1">Em análise</option>
            <option value="2">Aceito</option><option value="3">Recusado</option><option value="4">Cancelado</option>
          </select>
        </div>
        <div class="field"><label>Data início</label><input id="filtro-di" type="datetime-local"></div>
        <div class="field"><label>Data fim</label><input id="filtro-df" type="datetime-local"></div>
      </div>
      <div class="form-actions">
        <button class="btn btn-primary" data-accent="${accent()}" onclick="filtrarCandidaturas()">Filtrar</button>
      </div>
      <div id="lista-filtro" style="margin-top:16px"></div>
    </div>
  `);
}

async function filtrarCandidaturas() {
  const s = document.getElementById('filtro-status').value;
  const di = document.getElementById('filtro-di').value;
  const df = document.getElementById('filtro-df').value;
  if (!di || !df) return toast('Informe as datas', 'error');
  const div = document.getElementById('lista-filtro');
  div.innerHTML = loadingHtml();
  const params = new URLSearchParams({ status: s, data_inicio: di+':00', data_fim: df+':00' });
  try {
    const data = await api('GET', `/candidaturas?${params}`);
    renderTabelaCandidaturas(div, data);
  } catch(e) { div.innerHTML = emptyHtml(e.message); }
}

// Todas as empresas
function pageTodasEmpresas(container) {
  pageWrap(container, 'Todas as empresas', 'Consulta geral', `
    <div class="card">
      <div id="lista-todas-emp">${loadingHtml()}</div>
    </div>
  `);
  (async () => {
    const div = document.getElementById('lista-todas-emp');
    if (!div) return;
    try {
      const data = await api('GET', '/empresas/');
      if (!data || !data.length) { div.innerHTML = emptyHtml(); return; }
      div.innerHTML = `<div class="table-wrap"><table><thead><tr>
        <th>Razão social</th><th>Nome fantasia</th><th>CNPJ</th>
      </tr></thead><tbody>${data.map(e => `<tr>
        <td>${escHtml(e.razao_social)}</td>
        <td>${escHtml(e.nome_fantasia)}</td>
        <td>${escHtml(e.cnpj)}</td>
      </tr>`).join('')}</tbody></table></div>`;
    } catch(e) { div.innerHTML = emptyHtml(e.message); }
  })();
}

//  Instituição Pages

function pageCadastrarInstituicao(container) {
  pageWrap(container, 'Cadastrar instituição', 'Inserção em instituicao_ensino', `
    <div class="card">
      <div class="card-title">Nova instituição</div>
      <div class="form-grid">
        <div class="field"><label>Razão social *</label><input id="i-razao" placeholder="Razão social"></div>
        <div class="field"><label>Registro educacional *</label><input id="i-reg" placeholder="MEC-12345"></div>
        <div class="field"><label>Nome fantasia</label><input id="i-fantasia" placeholder="Nome fantasia"></div>
        <div class="field"><label>CNPJ (14 dígitos)</label><input id="i-cnpj" placeholder="00000000000000" maxlength="14"></div>
        <div class="field"><label>Tipo</label><input id="i-tipo" placeholder="Ex: Federal, Privada"></div>
      </div>
      <div class="form-actions">
        <button class="btn btn-primary" data-accent="${accent()}" onclick="criarInstituicao()">Cadastrar</button>
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
  const body = {
    razao_social: document.getElementById('i-razao').value,
    registro_educacional: document.getElementById('i-reg').value,
    nome_fantasia: document.getElementById('i-fantasia').value || null,
    cnpj: document.getElementById('i-cnpj').value || null,
    tipo: document.getElementById('i-tipo').value || null,
  };
  if (!body.razao_social || !body.registro_educacional) return toast('Preencha os campos obrigatórios', 'error');
  try {
    await api('POST', '/instituicoes-ensino/', body);
    toast('Instituição cadastrada!');
    ['i-razao','i-reg','i-fantasia','i-cnpj','i-tipo'].forEach(id => {
      const el = document.getElementById(id);
      if (el) el.value = '';
    });
  } catch(e) { toast(e.message, 'error'); }
}

async function buscarInstituicaoPorRegistro() {
  const reg = document.getElementById('busca-reg').value.trim();
  if (!reg) return;
  const div = document.getElementById('resultado-inst');
  div.innerHTML = loadingHtml();
  try {
    const data = await api('GET', `/instituicoes-ensino/registro/${reg}`);
    div.innerHTML = `<table><thead><tr><th>Razão social</th><th>Registro</th><th>CNPJ</th><th>Tipo</th></tr></thead>
      <tbody><tr>
        <td>${escHtml(data.razao_social)}</td>
        <td>${escHtml(data.registro_educacional)}</td>
        <td>${escHtml(data.cnpj)}</td>
        <td>${escHtml(data.tipo)}</td>
      </tr></tbody></table>`;
  } catch(e) { div.innerHTML = emptyHtml(e.message); }
}

// Cursos
function pageMeusCursos(container) {
  pageWrap(container, 'Meus cursos', 'Cursos por instituição', `
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
    const data = await api('GET', `/cursos/${id}`);
    renderTabelaCursos(div, Array.isArray(data) ? data : [data]);
  } catch(e) { div.innerHTML = emptyHtml(e.message); }
}

async function listarTodosCursos() {
  const div = document.getElementById('lista-cursos');
  if (!div) return;
  div.innerHTML = loadingHtml();
  try {
    const data = await api('GET', '/cursos/');
    renderTabelaCursos(div, data);
  } catch(e) { div.innerHTML = emptyHtml(e.message); }
}

function renderTabelaCursos(div, data) {
  if (!data || !data.length) { div.innerHTML = emptyHtml(); return; }
  div.innerHTML = `<div class="table-wrap"><table><thead><tr>
    <th>Nome</th><th>Modalidade</th><th>Área</th><th>Carga horária</th><th>Prazo</th>
  </tr></thead><tbody>${data.map(c => `<tr>
    <td>${escHtml(c.nome)}</td>
    <td><span class="badge badge-gray">${MODALIDADE[c.modalidade]||c.modalidade}</span></td>
    <td>${escHtml(c.area)}</td>
    <td>${c.carga_horaria ? c.carga_horaria+'h' : '—'}</td>
    <td>${escHtml(c.prazo_inscricao)}</td>
  </tr>`).join('')}</tbody></table></div>`;
}

function pageCadastrarCurso(container) {
  pageWrap(container, 'Novo curso', 'Inserção em curso', `
    <div class="card">
      <div class="card-title">Publicar curso</div>
      <div class="form-grid">
        <div class="field"><label>Nome *</label><input id="cu-nome" placeholder="Nome do curso"></div>
        <div class="field"><label>Instituição ID *</label><input id="cu-iid" placeholder="UUID da instituição"></div>
        <div class="field"><label>Modalidade</label>
          <select id="cu-mod"><option value="0">Presencial</option><option value="1">Remoto</option><option value="2">Híbrido</option></select>
        </div>
        <div class="field"><label>Área</label><input id="cu-area" placeholder="Ex: TI, Saúde"></div>
        <div class="field"><label>Carga horária (h)</label><input id="cu-ch" type="number" placeholder="40"></div>
        <div class="field"><label>Capacidade (vagas)</label><input id="cu-cap" type="number" placeholder="30"></div>
        <div class="field"><label>Prazo de inscrição</label><input id="cu-prazo" type="date"></div>
        <div class="field"><label>Empresa parceira (ID)</label><input id="cu-eid" placeholder="UUID (opcional)"></div>
      </div>
      <div class="form-actions">
        <button class="btn btn-primary" data-accent="${accent()}" onclick="criarCurso()">Publicar curso</button>
      </div>
    </div>
  `);
}

async function criarCurso() {
  const body = {
    nome: document.getElementById('cu-nome').value,
    instituicao_ensino_id: document.getElementById('cu-iid').value,
    modalidade: parseInt(document.getElementById('cu-mod').value),
    area: document.getElementById('cu-area').value || null,
    carga_horaria: parseInt(document.getElementById('cu-ch').value) || null,
    capacidade: parseInt(document.getElementById('cu-cap').value) || null,
    prazo_inscricao: document.getElementById('cu-prazo').value || null,
    empresa_id: document.getElementById('cu-eid').value || null,
  };
  if (!body.nome || !body.instituicao_ensino_id) return toast('Preencha os campos obrigatórios', 'error');
  try {
    await api('POST', '/cursos/', body);
    toast('Curso publicado!');
  } catch(e) { toast(e.message, 'error'); }
}

// Áreas de ensino
function pageAreasEnsino(container) {
  pageWrap(container, 'Áreas de ensino', 'Gerenciar e associar áreas', `
    <div class="card">
      <div class="card-title">Nova área de ensino</div>
      <div class="form-grid">
        <div class="field"><label>Nome *</label><input id="ae-nome" placeholder="Ex: Tecnologia da Informação"></div>
      </div>
      <div class="form-actions">
        <button class="btn btn-primary" data-accent="${accent()}" onclick="criarAreaEnsino()">Cadastrar</button>
      </div>
    </div>
    <div class="card">
      <div class="card-title">Associar área a instituição (N:N)</div>
      <div class="form-grid">
        <div class="field"><label>Instituição ID</label><input id="ae-iid" placeholder="UUID da instituição"></div>
        <div class="field"><label>Área de ensino ID</label><input id="ae-aid" placeholder="UUID da área"></div>
      </div>
      <div class="form-actions">
        <button class="btn btn-primary" data-accent="${accent()}" onclick="associarAreaInstituicao()">Associar</button>
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
  const nome = document.getElementById('ae-nome').value;
  if (!nome) return toast('Informe o nome', 'error');
  try {
    await api('POST', '/areas-ensino/', { nome });
    toast('Área cadastrada!');
    const el = document.getElementById('ae-nome');
    if (el) el.value = '';
    carregarAreas();
  } catch(e) { toast(e.message, 'error'); }
}

async function associarAreaInstituicao() {
  const body = {
    instituicao_ensino_id: document.getElementById('ae-iid').value,
    area_ensino_id: document.getElementById('ae-aid').value,
  };
  if (!body.instituicao_ensino_id || !body.area_ensino_id) return toast('Preencha os IDs', 'error');
  try {
    await api('POST', '/instituicoes-area-ensino/', body);
    toast('Associação criada!');
  } catch(e) { toast(e.message, 'error'); }
}

async function carregarAreas() {
  const div = document.getElementById('lista-areas');
  if (!div) return;
  try {
    const data = await api('GET', '/areas-ensino/');
    if (!data || !data.length) { div.innerHTML = emptyHtml(); return; }
    div.innerHTML = `<div class="table-wrap"><table><thead><tr>
      <th>ID</th><th>Nome</th>
    </tr></thead><tbody>${data.map(a => `<tr>
      <td style="font-size:11px;color:var(--muted)">${a.id.slice(0,8)}…</td>
      <td>${escHtml(a.nome)}</td>
    </tr>`).join('')}</tbody></table></div>`;
  } catch(e) { div.innerHTML = emptyHtml(e.message); }
}

// Todas as instituições
function pageTodasInstituicoes(container) {
  pageWrap(container, 'Todas as instituições', 'Consulta geral', `
    <div class="card">
      <div id="lista-todas-inst">${loadingHtml()}</div>
    </div>
  `);
  (async () => {
    const div = document.getElementById('lista-todas-inst');
    if (!div) return;
    try {
      const data = await api('GET', '/instituicoes-ensino/');
      if (!data || !data.length) { div.innerHTML = emptyHtml(); return; }
      div.innerHTML = `<div class="table-wrap"><table><thead><tr>
        <th>Razão social</th><th>Registro</th><th>CNPJ</th><th>Tipo</th>
      </tr></thead><tbody>${data.map(i => `<tr>
        <td>${escHtml(i.razao_social)}</td>
        <td>${escHtml(i.registro_educacional)}</td>
        <td>${escHtml(i.cnpj)}</td>
        <td>${escHtml(i.tipo)}</td>
      </tr>`).join('')}</tbody></table></div>`;
    } catch(e) { div.innerHTML = emptyHtml(e.message); }
  })();
}

// Init
switchProfile('candidato');