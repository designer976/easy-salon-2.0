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
 *  - Dispara só com mouse fino (desktop) — em touch não há "saída de mouse".
 *  - Aparece no máximo uma vez por sessão (sessionStorage).
 *  - Só arma depois de alguns segundos, evitando disparo acidental no load.
 *  - Fecha no X, no clique fora (backdrop) ou com Esc.
 */
(function () {
  'use strict';

  var SHOWN_KEY = 'exit-intent-shown';   // sessionStorage: já exibido nesta sessão
  var ARM_DELAY = 4000;                   // só arma 4s após o load
  var TOP_THRESHOLD = 8;                  // px: considera "saiu pelo topo" quando clientY <= isso

  function alreadyShown() {
    try { return sessionStorage.getItem(SHOWN_KEY) === '1'; } catch (e) { return false; }
  }
  function markShown() {
    try { sessionStorage.setItem(SHOWN_KEY, '1'); } catch (e) {}
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
          '<span class="exit-modal-placeholder">BANNER · 500px de largura · altura variável</span>' +
        '</div>' +
      '</div>';
    document.body.appendChild(root);
    return root;
  }

  function init() {
    if (alreadyShown()) return;
    // Só desktop com mouse fino
    if (window.matchMedia && !window.matchMedia('(pointer: fine)').matches) return;

    var root = null, armed = false, open = false;

    function ensureRoot() {
      if (root) return root;
      root = build();
      var backdrop = root.querySelector('.exit-backdrop');
      var closeBtn = root.querySelector('.exit-modal-close');
      backdrop.addEventListener('click', close);
      closeBtn.addEventListener('click', close);
      return root;
    }

    function show() {
      if (open || alreadyShown()) return;
      open = true;
      markShown();
      ensureRoot();
      // força reflow antes de animar
      root.offsetHeight; // eslint-disable-line no-unused-expressions
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

    function onMouseOut(e) {
      if (!armed || open) return;
      // saiu de fato da janela (sem destino dentro do doc) pelo topo
      if (e.relatedTarget || e.toElement) return;
      if ((e.clientY || 0) <= TOP_THRESHOLD) show();
    }

    setTimeout(function () { armed = true; }, ARM_DELAY);
    document.addEventListener('mouseout', onMouseOut);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
