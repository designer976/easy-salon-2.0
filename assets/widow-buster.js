/*!
 * Easy Salon — Widow buster
 * Cola as duas últimas palavras de cada bloco de texto com um espaço
 * inquebrável (NBSP), evitando uma palavra sozinha na última linha
 * ("viúva" tipográfica). Vale mobile e desktop, em qualquer largura.
 * Reaplica no painel de metodologia, cujo texto é trocado por JS ao
 * mudar de passo.
 */
(function () {
  'use strict';

  var NBSP = String.fromCharCode(160);

  // Cola a última palavra na penúltima (NBSP). Só age quando o último nó
  // do elemento é texto com ao menos duas palavras — assim ignora blocos
  // que terminam em <strong>, <a>, <span>, etc.
  function glue(el) {
    if (!el) return;
    var last = el.lastChild;
    if (!last || last.nodeType !== 3) return;
    var t = last.nodeValue;
    if (!/\S\s+\S/.test(t)) return;
    // [ \t\n\r\f] (sem NBSP) garante idempotência: não re-casa um glue feito.
    var nt = t.replace(/[ \t\n\r\f]+(\S+)(\s*)$/, function (_, w, tail) {
      return NBSP + w + tail;
    });
    if (nt !== t) last.nodeValue = nt;
  }

  // Só conteúdo dentro de .page (não mexe no widget de WhatsApp, que vive
  // direto no body).
  var SEL = '.page p, .page li';

  function run(root) {
    var nodes = (root || document).querySelectorAll(SEL);
    for (var i = 0; i < nodes.length; i++) glue(nodes[i]);
  }

  function init() {
    run();
    // Metodologia: o <p> do painel é reescrito ao trocar de passo → reaplica.
    var panel = document.getElementById('h2-method-panel');
    if (panel && window.MutationObserver) {
      var mo = new MutationObserver(function () {
        glue(panel.querySelector('.h2-method-panel-text p'));
      });
      mo.observe(panel, { childList: true, subtree: true });
    }
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
