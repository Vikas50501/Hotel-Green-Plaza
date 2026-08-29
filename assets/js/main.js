/* ==========================================================================
   Hotel Green Plaza — core interactions
   Scroll reveal, gallery filter + lightbox, menu filter, deferred map,
   footer year. Navigation is in navigation.js, carousel in slider.js,
   form handling in enquiry.js.
   ========================================================================== */

(function () {
  'use strict';

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function $(sel, ctx) { return (ctx || document).querySelector(sel); }
  function $$(sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); }

  /* ----------------------------------------------------------------------
     Scroll reveal — fade and rise, 18px, once, staggered across siblings
     ---------------------------------------------------------------------- */

  var revealItems = $$('.gp-reveal');

  if (reduceMotion || !('IntersectionObserver' in window)) {
    revealItems.forEach(function (el) { el.classList.add('is-visible'); });
  } else {
    var observer = new IntersectionObserver(function (entries, obs) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var el = entry.target;
        var siblings = el.parentElement ? $$(':scope > .gp-reveal', el.parentElement) : [el];
        var index = siblings.indexOf(el);
        el.style.transitionDelay = (Math.min(index < 0 ? 0 : index, 5) * 80) + 'ms';
        el.classList.add('is-visible');
        obs.unobserve(el);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 });

    revealItems.forEach(function (el) { observer.observe(el); });

    window.addEventListener('load', function () {
      revealItems.forEach(function (el) {
        if (el.classList.contains('is-visible')) return;
        var box = el.getBoundingClientRect();
        if (box.top < window.innerHeight && box.bottom > 0) {
          el.classList.add('is-visible');
          observer.unobserve(el);
        }
      });
    });
  }

  /* ----------------------------------------------------------------------
     Gallery filter
     ---------------------------------------------------------------------- */

  var filterBar = $('.gp-filter');

  if (filterBar) {
    var items = $$('.gp-masonry__item');

    filterBar.addEventListener('click', function (event) {
      var btn = event.target.closest('.gp-filter__btn');
      if (!btn) return;

      var wanted = btn.getAttribute('data-filter');

      $$('.gp-filter__btn', filterBar).forEach(function (b) {
        b.setAttribute('aria-pressed', String(b === btn));
      });

      items.forEach(function (item) {
        var cats = (item.getAttribute('data-category') || '').split(/\s+/);
        var show = wanted === 'all' || cats.indexOf(wanted) !== -1;
        item.hidden = !show;
      });

      buildLightboxSet();
    });
  }

  /* ----------------------------------------------------------------------
     Menu course filter
     ---------------------------------------------------------------------- */

  var menuNav = $('[data-menu-nav]');

  if (menuNav) {
    var menuGroups = $$('.gp-menu__group');

    menuNav.addEventListener('click', function (event) {
      var btn = event.target.closest('.gp-filter__btn');
      if (!btn) return;

      var wanted = btn.getAttribute('data-filter');

      $$('.gp-filter__btn', menuNav).forEach(function (b) {
        b.setAttribute('aria-pressed', String(b === btn));
      });

      menuGroups.forEach(function (group) {
        var cat = group.getAttribute('data-category') || '';
        var show = wanted === 'all' || cat === wanted;
        group.hidden = !show;
        if (show) group.classList.add('is-visible');
      });

      var section = document.getElementById('menu');
      if (section) {
        var top = section.getBoundingClientRect().top + window.pageYOffset - 92;
        if (window.pageYOffset > top) {
          window.scrollTo({ top: top, behavior: reduceMotion ? 'auto' : 'smooth' });
        }
      }
    });
  }

  /* ----------------------------------------------------------------------
     Lightbox
     ---------------------------------------------------------------------- */

  var lightbox = $('.gp-lightbox');
  var lbImage = $('.gp-lightbox__image');
  var lbCaption = $('.gp-lightbox__caption');
  var lbSet = [];
  var lbIndex = 0;
  var lastFocusedBeforeLb = null;

  /* Uses window.gp.trapFocus exposed by navigation.js */
  function trapFocus(event, root) {
    if (window.gp && window.gp.trapFocus) {
      window.gp.trapFocus(event, root);
    }
  }

  function buildLightboxSet() {
    lbSet = $$('.gp-masonry__item').filter(function (item) { return !item.hidden; })
      .map(function (item) { return $('.gp-thumb', item); })
      .filter(Boolean);
  }

  function showLightbox(index) {
    if (!lightbox || !lbSet.length) return;
    lbIndex = (index + lbSet.length) % lbSet.length;
    var trigger = lbSet[lbIndex];
    var img = $('img', trigger);
    if (!img) return;

    lbImage.setAttribute('src', img.getAttribute('data-full') || img.currentSrc || img.src);
    lbImage.setAttribute('alt', img.getAttribute('alt') || '');
    lbCaption.textContent = img.getAttribute('alt') || '';
    lbCaption.textContent += ' (' + (lbIndex + 1) + ' of ' + lbSet.length + ')';
  }

  function openLightbox(trigger) {
    buildLightboxSet();
    var index = lbSet.indexOf(trigger);
    if (index < 0) return;
    lastFocusedBeforeLb = document.activeElement;
    showLightbox(index);
    lightbox.classList.add('is-open');
    lightbox.setAttribute('aria-hidden', 'false');
    document.body.classList.add('gp-no-scroll');
    var closeBtn = $('.gp-lightbox__close', lightbox);
    if (closeBtn) closeBtn.focus();
  }

  function closeLightbox() {
    if (!lightbox) return;
    lightbox.classList.remove('is-open');
    lightbox.setAttribute('aria-hidden', 'true');
    document.body.classList.remove('gp-no-scroll');
    if (lastFocusedBeforeLb) lastFocusedBeforeLb.focus();
  }

  if (lightbox) {
    buildLightboxSet();

    document.addEventListener('click', function (event) {
      var thumb = event.target.closest('.gp-thumb');
      if (thumb) {
        event.preventDefault();
        openLightbox(thumb);
      }
    });

    lightbox.addEventListener('click', function (event) {
      if (event.target.closest('.gp-lightbox__close')) return closeLightbox();
      if (event.target.closest('.gp-lightbox__prev')) return showLightbox(lbIndex - 1);
      if (event.target.closest('.gp-lightbox__next')) return showLightbox(lbIndex + 1);
      if (!event.target.closest('.gp-lightbox__figure')) closeLightbox();
    });

    lightbox.addEventListener('keydown', function (event) {
      if (event.key === 'Escape') return closeLightbox();
      if (event.key === 'ArrowLeft') return showLightbox(lbIndex - 1);
      if (event.key === 'ArrowRight') return showLightbox(lbIndex + 1);
      trapFocus(event, lightbox);
    });
  }

  /* ----------------------------------------------------------------------
     Deferred map — loads iframe only on click
     ---------------------------------------------------------------------- */

  $$('.gp-map__poster').forEach(function (poster) {
    poster.addEventListener('click', function () {
      var wrap = poster.parentElement;
      var src = poster.getAttribute('data-src');
      if (!src) return;
      var frame = document.createElement('iframe');
      frame.setAttribute('src', src);
      frame.setAttribute('title', poster.getAttribute('data-title') || 'Map showing Hotel Green Plaza, Bhilwara');
      frame.setAttribute('loading', 'lazy');
      frame.setAttribute('referrerpolicy', 'no-referrer-when-downgrade');
      frame.setAttribute('allowfullscreen', '');
      wrap.appendChild(frame);
      poster.remove();
    });
  });

  /* ----------------------------------------------------------------------
     Footer year
     ---------------------------------------------------------------------- */

  $$('.gp-year').forEach(function (el) {
    el.textContent = String(new Date().getFullYear());
  });
})();
