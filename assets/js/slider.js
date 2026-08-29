/* ==========================================================================
   Hotel Green Plaza — slider / carousel
   Drives arrow buttons and the progress bar on .gp-carousel elements.
   Native scroll-snap handles drag/swipe; this is progressive enhancement.
   ========================================================================== */

(function () {
  'use strict';

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function $(sel, ctx) { return (ctx || document).querySelector(sel); }
  function $$(sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); }

  $$('.gp-carousel').forEach(function (root) {
    var viewport = $('.gp-carousel__viewport', root);
    var track = $('.gp-carousel__track', root);
    var prevBtn = $('.gp-carousel__btn--prev', root);
    var nextBtn = $('.gp-carousel__btn--next', root);
    var bar = $('.gp-carousel__progress-bar', root);
    if (!viewport || !track) return;

    function step() {
      var first = track.children[0];
      if (!first) return viewport.clientWidth;
      var gap = parseFloat(getComputedStyle(track).columnGap || getComputedStyle(track).gap || '0') || 0;
      return first.getBoundingClientRect().width + gap;
    }

    function refresh() {
      var max = track.scrollWidth - viewport.clientWidth;
      var pos = viewport.scrollLeft;

      if (prevBtn) prevBtn.disabled = pos <= 8;
      if (nextBtn) nextBtn.disabled = pos >= max - 8;

      if (bar) {
        if (max <= 0) {
          bar.style.width = '100%';
          bar.style.transform = 'translateX(0)';
        } else {
          var visible = Math.min(1, viewport.clientWidth / track.scrollWidth);
          var trackWidth = bar.parentElement.clientWidth;
          bar.style.width = (visible * 100) + '%';
          bar.style.transform = 'translateX(' + ((pos / max) * trackWidth * (1 - visible)) + 'px)';
        }
      }
    }

    function go(direction) {
      viewport.scrollBy({ left: direction * step(), behavior: reduceMotion ? 'auto' : 'smooth' });
    }

    if (prevBtn) prevBtn.addEventListener('click', function () { go(-1); });
    if (nextBtn) nextBtn.addEventListener('click', function () { go(1); });

    viewport.addEventListener('scroll', refresh, { passive: true });
    window.addEventListener('resize', refresh);
    refresh();
  });
})();
