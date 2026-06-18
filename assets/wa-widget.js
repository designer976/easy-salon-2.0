/*!
 * Easy Salon — WhatsApp floating widget
 * FAB verde + toast auto-popup com som + modal expandido com chat-like UI.
 * Click no input/send → abre wa.me/<PHONE>?text=<msg>.
 *
 * Customizar: PHONE, NAME, GREETING, AUTO_POPUP_DELAY, SOUND_URL, AVATAR_URL.
 */
(function () {
  'use strict';

  var PHONE = '5541991044112';
  var NAME = 'Raissa';
  var GREETING = 'Oi, tudo bem 👋 ? ' + NAME + ' da Easy Salon aqui!';
  var DEFAULT_MSG = 'Oi! Vim pelo site da Easy Salon, quero saber mais.';
  var AUTO_POPUP_DELAY = 5000;
  var TOAST_COOLDOWN_MS = 6 * 60 * 60 * 1000; // 6h — não repete se já mostrou
  var STORAGE_KEY = 'wa-widget-toast-next';
  var SOUND_URL = '/assets/wpp.mp3';
  var AVATAR_URL = '/assets/raissa.jpg';

  var WA_ICON = '<svg viewBox="0 0 24 24" fill="white" aria-hidden="true"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 0 1-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 0 1-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 0 1 2.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0 0 12.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 0 0 5.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 0 0-3.48-8.413z"/></svg>';
  var SEND_ICON = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M3.4 20.4 20.85 12.92a1 1 0 0 0 0-1.84L3.4 3.6a1 1 0 0 0-1.39 1.1l1.36 5.55a1 1 0 0 0 .77.74l8.27 1.66a.25.25 0 0 1 0 .49l-8.27 1.66a1 1 0 0 0-.77.74L2 19.3a1 1 0 0 0 1.4 1.1Z"/></svg>';

  function waLink(text) {
    var msg = encodeURIComponent(text || DEFAULT_MSG);
    return 'https://api.whatsapp.com/send/?phone=' + PHONE + '&text=' + msg + '&type=phone_number&app_absent=0';
  }

  function avatar(small) {
    var cls = 'wa-avatar' + (small ? ' wa-avatar--sm' : '');
    return '<div class="' + cls + '">' +
      '<span class="wa-avatar-fallback">R</span>' +
      '<img src="' + AVATAR_URL + '" alt="" onerror="this.remove()">' +
      '</div>';
  }

  function init() {
    if (document.getElementById('wa-widget')) return;

    var root = document.createElement('div');
    root.id = 'wa-widget';
    root.innerHTML =
      '<aside class="wa-toast" hidden role="dialog" aria-label="Mensagem de ' + NAME + '">' +
        '<button class="wa-toast-close" type="button" aria-label="Fechar">&times;</button>' +
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
              '<span class="wa-online"><i></i>Online</span>' +
            '</div>' +
          '</div>' +
          '<button class="wa-modal-close" type="button" aria-label="Fechar conversa">&times;</button>' +
        '</header>' +
        '<div class="wa-modal-body">' +
          '<div class="wa-msg">' +
            '<p>' + GREETING + '</p>' +
            '<span class="wa-meta">Agora</span>' +
          '</div>' +
          '<div class="wa-typing" aria-hidden="true"><span></span><span></span><span></span></div>' +
        '</div>' +
        '<form class="wa-modal-input" novalidate>' +
          '<input type="text" placeholder="Digite uma mensagem..." aria-label="Mensagem para ' + NAME + '" autocomplete="off">' +
          '<button type="submit" aria-label="Enviar pelo WhatsApp">' + SEND_ICON + '</button>' +
        '</form>' +
      '</section>' +

      '<button class="wa-fab" type="button" aria-label="Fale conosco pelo WhatsApp">' + WA_ICON + '</button>';

    document.body.appendChild(root);

    var toast = root.querySelector('.wa-toast');
    var modal = root.querySelector('.wa-modal');
    var fab = root.querySelector('.wa-fab');
    var input = modal.querySelector('input');

    var audio = null;
    try { audio = new Audio(SOUND_URL); audio.preload = 'auto'; audio.volume = 0.6; }
    catch (e) { /* sem áudio */ }

    function openModal() {
      hideToast(true);
      modal.hidden = false;
      requestAnimationFrame(function () { modal.classList.add('is-open'); });
      setTimeout(function () { try { input.focus({ preventScroll: true }); } catch (e) {} }, 280);
    }
    function closeModal() {
      modal.classList.remove('is-open');
      setTimeout(function () { modal.hidden = true; }, 260);
    }
    function showToast() {
      try {
        var nextAt = parseInt(localStorage.getItem(STORAGE_KEY) || '0', 10);
        if (Date.now() < nextAt) return;
      } catch (e) {}
      try { localStorage.setItem(STORAGE_KEY, String(Date.now() + TOAST_COOLDOWN_MS)); } catch (e) {}
      toast.hidden = false;
      requestAnimationFrame(function () { toast.classList.add('is-open'); });
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
    toast.addEventListener('click', function (e) {
      if (e.target.closest('.wa-toast-close')) { hideToast(); return; }
      openModal();
    });
    modal.querySelector('.wa-modal-close').addEventListener('click', closeModal);
    modal.querySelector('form').addEventListener('submit', function (e) {
      e.preventDefault();
      var text = input.value.trim();
      window.open(waLink(text), '_blank', 'noopener');
      input.value = '';
    });

    setTimeout(showToast, AUTO_POPUP_DELAY);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
