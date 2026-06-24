/*!
 * Easy Salon — Exit-intent modal
 * Quando o mouse sai pela parte superior da janela (intenção de sair do
 * site), abre um modal com um espaço para banner. Largura fixa de 500px;
 * a altura acompanha o conteúdo do banner.
 *
 * Para colocar o banner real: troque o conteúdo de .exit-modal-banner por
 * <img src="..." alt="..." style="width:100%;display:block"> (ou um <a><img></a>).
 *
 * Comportamento:
 *  - Vale em todas as páginas (script incluído no site todo).
 *  - Dispara só com mouse fino (desktop) — em touch não há "saída de mouse".
 *  - Depois de aparecer uma vez, só volta a aparecer após 2h (localStorage,
 *    compartilhado entre páginas e abas).
 *  - Só arma alguns segundos após o load, evitando disparo acidental.
 *  - Fecha no X, no clique fora (backdrop) ou com Esc.
 */
(function () {
  'use strict';

  var STORE_KEY = 'exit-intent-last';     // localStorage: timestamp (ms) da última exibição
  var COOLDOWN = 2 * 60 * 60 * 1000;      // 2 horas
  var ARM_DELAY = 3000;                   // só arma 3s após o load
  var TOP_THRESHOLD = 0;                  // saiu pelo topo quando clientY <= isso
  var WA_PHONE = '554123913300';
  var WA_MSG = 'Olá! Eu estava no site e vi que estou a um passo de transformar a rotina do meu salão. Gostaria de saber mais sobre o sistema!';
  var WA_LINK = 'https://api.whatsapp.com/send/?phone=' + WA_PHONE + '&text=' + encodeURIComponent(WA_MSG) + '&type=phone_number&app_absent=0';

  // Banner por negócio: cada página de negócio usa o seu; as demais usam o -geral
  var BANNER_VER = '20260724';
  function bannerUrl() {
    var p = location.pathname;
    var key = 'geral';
    if (p.indexOf('barbearia') !== -1) key = 'barbearia';
    else if (p.indexOf('estudio-de-beleza') !== -1) key = 'estudio-de-beleza';
    else if (p.indexOf('salao-de-beleza') !== -1) key = 'salao-de-beleza';
    return '/assets/b-molda-saida-' + key + '.png?v=' + BANNER_VER;
  }

  function recentlyShown() {
    try {
      var last = parseInt(localStorage.getItem(STORE_KEY) || '0', 10);
      return last > 0 && (Date.now() - last) < COOLDOWN;
    } catch (e) { return false; }
  }
  function markShown() {
    try { localStorage.setItem(STORE_KEY, String(Date.now())); } catch (e) {}
  }

  function build() {
    var root = document.createElement('div');
    root.id = 'exit-intent';
    root.innerHTML =
      '<div class="exit-backdrop" data-exit-close></div>' +
      '<div class="exit-modal" role="dialog" aria-modal="true" aria-label="Oferta ao sair">' +
        '<button type="button" class="exit-modal-close" aria-label="Fechar">' +
          '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>' +
        '</button>' +
        '<div class="exit-modal-banner">' +
          '<a href="' + WA_LINK + '" target="_blank" rel="noopener noreferrer" aria-label="Falar com um especialista no WhatsApp">' +
            '<img src="' + bannerUrl() + '" alt="Oferta Easy Salon ao sair">' +
          '</a>' +
        '</div>' +
      '</div>';
    document.body.appendChild(root);
    return root;
  }

  function init() {
    // Só desktop com mouse fino
    if (window.matchMedia && !window.matchMedia('(pointer: fine)').matches) return;
    if (recentlyShown()) return;

    var root = null, armed = false, open = false;

    function ensureRoot() {
      if (root) return root;
      root = build();
      root.querySelector('.exit-backdrop').addEventListener('click', close);
      root.querySelector('.exit-modal-close').addEventListener('click', close);
      return root;
    }

    function show() {
      if (open || recentlyShown()) return;
      open = true;
      markShown();
      ensureRoot();
      root.offsetHeight; // reflow antes de animar
      root.classList.add('is-open');
      document.addEventListener('keydown', onKey);
    }

    function close() {
      if (!open) return;
      open = false;
      if (root) root.classList.remove('is-open');
      document.removeEventListener('keydown', onKey);
    }

    function onKey(e) {
      if (e.key === 'Escape' || e.keyCode === 27) close();
    }

    // Saída pelo topo da janela (intenção de fechar / ir pra barra do navegador)
    function onMouseOut(e) {
      if (!armed || open) return;
      if (e.relatedTarget || e.toElement) return;   // foi para outro elemento, não saiu
      if ((e.clientY || 0) <= TOP_THRESHOLD) show();
    }

    setTimeout(function () { armed = true; }, ARM_DELAY);
    document.addEventListener('mouseout', onMouseOut);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
