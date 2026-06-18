/*!
 * Easy Salon — WhatsApp floating widget
 * FAB verde + toast auto-popup com som + modal expandido com chat-like UI.
 * Click no input/send → abre wa.me/<PHONE>?text=<msg>.
 *
 * Customizar: PHONE, NAME, GREETING, AUTO_POPUP_DELAY, SOUND_URL, AVATAR_URL.
 */
(function () {
  'use strict';

  var PHONE = '554123913300';
  var NAME = 'Dani';
  var GREETING = 'Oi, tudo bem 👋 ? ' + NAME + ' da Easy Salon aqui!';
  var SECOND_MSG = 'Procurando um sistema de gestão para o seu <strong>salão de beleza</strong>, <strong>barbearia</strong> ou <strong>estúdio</strong>?';
  var SECOND_MSG_DELAY = 2500;      // delay do "digitando" até a 2ª mensagem
  var DEFAULT_MSG = 'Oi! Vim pelo site da Easy Salon, quero saber mais.';
  var DELAY_AFTER_GESTURE = 3000;   // mostra 3s depois do 1º clique/scroll/tecla
  var FALLBACK_DELAY = 12000;       // se ninguém interagir, mostra (sem som) em 12s
  var BADGE_KEY = 'wa-widget-badge-on';       // sessionStorage: badge "1" persiste entre páginas
  var SOUND_URL = '/assets/wpp.mp3';
  var AVATAR_URL = '/assets/raissa.jpg';

  var WA_ICON = '<svg viewBox="0 0 24 24" fill="white" aria-hidden="true"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 0 1-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 0 1-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 0 1 2.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0 0 12.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 0 0 5.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 0 0-3.48-8.413z"/></svg>';
  // Lucide icons (lucide.dev) — stroke based, currentColor
  var SEND_ICON = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-send" aria-hidden="true"><path d="M14.536 21.686a.5.5 0 0 0 .937-.024l6.5-19a.496.496 0 0 0-.635-.635l-19 6.5a.5.5 0 0 0-.024.937l7.93 3.18a2 2 0 0 1 1.112 1.11z"/><path d="m21.854 2.147-10.94 10.939"/></svg>';
  var X_ICON = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-x" aria-hidden="true"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>';

  function waLink(text) {
    var msg = encodeURIComponent(text || DEFAULT_MSG);
    return 'https://api.whatsapp.com/send/?phone=' + PHONE + '&text=' + msg + '&type=phone_number&app_absent=0';
  }

  function avatar(small) {
    var cls = 'wa-avatar' + (small ? ' wa-avatar--sm' : '');
    return '<div class="' + cls + '">' +
      '<span class="wa-avatar-fallback">' + NAME.charAt(0).toUpperCase() + '</span>' +
      '<img src="' + AVATAR_URL + '" alt="" onerror="this.remove()">' +
      '</div>';
  }

  function init() {
    if (document.getElementById('wa-widget')) return;

    var root = document.createElement('div');
    root.id = 'wa-widget';
    root.innerHTML =
      '<aside class="wa-toast" hidden role="dialog" aria-label="Mensagem de ' + NAME + '">' +
        '<button class="wa-toast-close" type="button" aria-label="Fechar">' + X_ICON + '</button>' +
        '<div class="wa-toast-row">' +
          avatar(false) +
          '<div class="wa-toast-body">' +
            '<strong>' + NAME + '</strong>' +
            '<p>' + GREETING + '</p>' +
            '<span class="wa-meta">Agora</span>' +
          '</div>' +
        '</div>' +
      '</aside>' +

      '<section class="wa-modal" hidden role="dialog" aria-label="Conversa com ' + NAME + '" aria-modal="false">' +
        '<header class="wa-modal-header">' +
          '<div class="wa-modal-id">' +
            avatar(true) +
            '<div>' +
              '<strong>' + NAME + '</strong>' +
              '<span class="wa-online">Online</span>' +
            '</div>' +
          '</div>' +
          '<button class="wa-modal-close" type="button" aria-label="Fechar conversa">' + X_ICON + '</button>' +
        '</header>' +
        '<div class="wa-modal-body">' +
          '<div class="wa-msg">' +
            '<p>' + GREETING + '</p>' +
            '<span class="wa-meta">Agora</span>' +
          '</div>' +
          '<div class="wa-typing" aria-hidden="true"><span></span><span></span><span></span></div>' +
          '<div class="wa-msg wa-msg--late" hidden>' +
            '<p>' + SECOND_MSG + '</p>' +
            '<span class="wa-meta">Agora</span>' +
          '</div>' +
        '</div>' +
        '<form class="wa-modal-input" novalidate>' +
          '<input type="text" placeholder="Digite uma mensagem..." aria-label="Mensagem para ' + NAME + '" autocomplete="off">' +
          '<button type="submit" aria-label="Enviar pelo WhatsApp">' + SEND_ICON + '</button>' +
        '</form>' +
      '</section>' +

      '<button class="wa-fab" type="button" aria-label="Fale conosco pelo WhatsApp">' + WA_ICON +
        '<span class="wa-fab-badge" hidden>1</span>' +
      '</button>';

    document.body.appendChild(root);

    var toast = root.querySelector('.wa-toast');
    var modal = root.querySelector('.wa-modal');
    var fab = root.querySelector('.wa-fab');
    var input = modal.querySelector('input');

    var audio = null;
    try { audio = new Audio(SOUND_URL); audio.preload = 'auto'; audio.volume = 0.6; }
    catch (e) { /* sem áudio */ }

    var secondShown = false;
    function showSecondMessage() {
      if (secondShown) return;
      secondShown = true;
      var typing = modal.querySelector('.wa-typing');
      var late = modal.querySelector('.wa-msg--late');
      if (typing) typing.hidden = true;
      if (late) {
        late.hidden = false;
        requestAnimationFrame(function () { late.classList.add('is-in'); });
      }
      var body = modal.querySelector('.wa-modal-body');
      if (body) body.scrollTop = body.scrollHeight;
    }
    var badge = null; // setado depois que o root for criado
    function setBadge(visible) {
      if (!badge) badge = root.querySelector('.wa-fab-badge');
      if (!badge) return;
      badge.hidden = !visible;
      try {
        if (visible) sessionStorage.setItem(BADGE_KEY, '1');
        else sessionStorage.removeItem(BADGE_KEY);
      } catch (e) {}
    }
    // Badge não aparece sozinho no init — sempre acompanha o toast (showToast)
    // para evitar "1" piscando antes da notificação chegar.
    function openModal() {
      hideToast(true);
      setBadge(false);
      modal.hidden = false;
      requestAnimationFrame(function () { modal.classList.add('is-open'); });
      setTimeout(function () { try { input.focus({ preventScroll: true }); } catch (e) {} }, 280);
      if (!secondShown) setTimeout(showSecondMessage, SECOND_MSG_DELAY);
    }
    function closeModal() {
      modal.classList.remove('is-open');
      setTimeout(function () { modal.hidden = true; }, 260);
    }
    function showToast() {
      toast.hidden = false;
      requestAnimationFrame(function () { toast.classList.add('is-open'); });
      setBadge(true);
      if (audio) audio.play().catch(function () { /* navegador bloqueou autoplay; ok */ });
    }
    function hideToast(instant) {
      toast.classList.remove('is-open');
      if (instant) { toast.hidden = true; return; }
      setTimeout(function () { toast.hidden = true; }, 260);
    }

    // Listeners
    fab.addEventListener('click', function () {
      if (modal.classList.contains('is-open')) closeModal();
      else openModal();
    });
    // Close: listener direto, com pointerdown E click pra cobrir touch + mouse
    var toastCloseBtn = toast.querySelector('.wa-toast-close');
    function handleClose(e) {
      e.preventDefault();
      e.stopPropagation();
      hideToast();
    }
    toastCloseBtn.addEventListener('click', handleClose);
    toastCloseBtn.addEventListener('pointerdown', function (e) { e.stopPropagation(); });
    // Click no corpo do toast (avatar, nome, mensagem) abre a conversa
    var toastRow = toast.querySelector('.wa-toast-row');
    if (toastRow) toastRow.addEventListener('click', function () { openModal(); });
    modal.querySelector('.wa-modal-close').addEventListener('click', closeModal);
    modal.querySelector('form').addEventListener('submit', function (e) {
      e.preventDefault();
      var text = input.value.trim();
      window.open(waLink(text), '_blank', 'noopener');
      input.value = '';
    });

    // Auto-popup respeitando a política de autoplay: aguarda o 1º gesto
    // do usuário, libera o áudio com um play+pause silencioso e mostra
    // o toast 3s depois. Fallback: 12s sem gesto, mostra sem som.
    (function () {
      var armed = false;
      var events = ['pointerdown', 'touchstart', 'keydown', 'mousemove', 'wheel'];
      var fallback = setTimeout(function () {
        if (armed) return;
        armed = true; cleanup();
        showToast();
      }, FALLBACK_DELAY);
      function cleanup() {
        events.forEach(function (e) {
          window.removeEventListener(e, onGesture, true);
        });
      }
      function onGesture() {
        if (armed) return;
        armed = true; cleanup(); clearTimeout(fallback);
        // Unlock audio com play+pause silencioso (browser libera porque o
        // gesto está no stack atual)
        if (audio) {
          var p = audio.play();
          if (p && p.then) {
            p.then(function () { audio.pause(); audio.currentTime = 0; })
             .catch(function () { /* deu ruim, segue sem som */ });
          }
        }
        setTimeout(showToast, DELAY_AFTER_GESTURE);
      }
      events.forEach(function (e) {
        window.addEventListener(e, onGesture, { capture: true, passive: true });
      });
    })();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
