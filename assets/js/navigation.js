/* ==========================================================================
   Hotel Green Plaza — navigation
   Header scroll state, mobile panel open/close, focus trap.
   ========================================================================== */

(function () {
  'use strict';

  function $(sel, ctx) { return (ctx || document).querySelector(sel); }
  function $$(sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); }

  /* ----------------------------------------------------------------------
     Header — transparent over the hero, solid on scroll
     ---------------------------------------------------------------------- */

  var header = $('.gp-header');

  if (header) {
    var applyHeaderState = function () {
      header.classList.toggle('is-stuck', window.pageYOffset > 40);
    };
    applyHeaderState();
    window.addEventListener('scroll', applyHeaderState, { passive: true });
  }

  /* ----------------------------------------------------------------------
     Focus trap — shared by panel and exposed for lightbox in main.js
     ---------------------------------------------------------------------- */

  function focusables(root) {
    return $$('a[href], button:not([disabled]), input, select, textarea, [tabindex]:not([tabindex="-1"])', root)
      .filter(function (el) { return el.offsetParent !== null || el === document.activeElement; });
  }

  function trapFocus(event, root) {
    if (event.key !== 'Tab') return;
    var items = focusables(root);
    if (!items.length) return;
    var first = items[0];
    var last = items[items.length - 1];
    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    }
  }

  /* Expose so main.js lightbox can reuse without duplication */
  window.gp = window.gp || {};
  window.gp.trapFocus = trapFocus;

  /* ----------------------------------------------------------------------
     Mobile panel
     ---------------------------------------------------------------------- */

  var burger = $('.gp-burger');
  var panel = $('.gp-mobile-panel');
  var panelClose = $('.gp-panel-close');
  var lastFocusedBeforePanel = null;

  function openPanel() {
    if (!panel) return;
    lastFocusedBeforePanel = document.activeElement;
    panel.classList.add('is-open');
    panel.setAttribute('aria-hidden', 'false');
    if (burger) burger.setAttribute('aria-expanded', 'true');
    document.body.classList.add('gp-no-scroll');
    if (panelClose) panelClose.focus();
  }

  function closePanel() {
    if (!panel) return;
    panel.classList.remove('is-open');
    panel.setAttribute('aria-hidden', 'true');
    if (burger) burger.setAttribute('aria-expanded', 'false');
    document.body.classList.remove('gp-no-scroll');
    if (lastFocusedBeforePanel) lastFocusedBeforePanel.focus();
  }

  if (burger) burger.addEventListener('click', openPanel);
  if (panelClose) panelClose.addEventListener('click', closePanel);

  if (panel) {
    panel.addEventListener('keydown', function (event) {
      if (event.key === 'Escape') closePanel();
      trapFocus(event, panel);
    });
    $$('a', panel).forEach(function (link) {
      link.addEventListener('click', function () { closePanel(); });
    });
  }
})();
