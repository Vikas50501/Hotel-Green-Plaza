/* ==========================================================================
   Hotel Green Plaza — site behaviour
   No jQuery. Only the interactions the design calls for:
   header state, mobile panel, scroll reveal, gallery filter + lightbox,
   enquiry form validation, deferred map load.
   ========================================================================== */

(function () {
  'use strict';

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

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
     Mobile panel
     ---------------------------------------------------------------------- */

  var burger = $('.gp-burger');
  var panel = $('.gp-mobile-panel');
  var panelClose = $('.gp-panel-close');
  var lastFocusedBeforePanel = null;

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
    // Following a link inside the panel should close it
    $$('a', panel).forEach(function (link) {
      link.addEventListener('click', function () { closePanel(); });
    });
  }

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

    // Safety net: never let the first screen stay blank. If anything above the
    // fold has not been revealed by load, show it outright.
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

      // Keep the lightbox sequence in step with what is on screen
      buildLightboxSet();
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
     Deferred map — the embed only loads once the guest asks for it
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
     Enquiry form — honeypot, required fields, date sanity, async submit
     ---------------------------------------------------------------------- */

  $$('.gp-form').forEach(function (form) {
    var status = $('.gp-form__status', form);

    function setError(field, message) {
      var wrap = field.closest('.gp-field');
      if (!wrap) return;
      var slot = $('.gp-error', wrap);
      wrap.classList.toggle('has-error', Boolean(message));
      field.setAttribute('aria-invalid', message ? 'true' : 'false');
      if (slot) slot.textContent = message || '';
    }

    function validateField(field) {
      var value = (field.value || '').trim();
      var label = field.getAttribute('data-label') || 'This field';

      if (field.required && !value) {
        setError(field, label + ' is required.');
        return false;
      }
      if (value && field.type === 'email' && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(value)) {
        setError(field, 'Enter a valid email address.');
        return false;
      }
      if (value && field.type === 'tel' && !/^[+]?[\d\s()-]{7,20}$/.test(value)) {
        setError(field, 'Enter a valid phone number.');
        return false;
      }
      setError(field, '');
      return true;
    }

    $$('input, select, textarea', form).forEach(function (field) {
      if (field.closest('.gp-hp')) return;
      field.addEventListener('blur', function () { validateField(field); });
      field.addEventListener('input', function () {
        if (field.closest('.gp-field') && field.closest('.gp-field').classList.contains('has-error')) {
          validateField(field);
        }
      });
    });

    form.addEventListener('submit', function (event) {
      event.preventDefault();

      // Honeypot: a real guest never fills this in
      var hp = $('.gp-hp input', form);
      if (hp && hp.value) return;

      var fields = $$('input, select, textarea', form).filter(function (f) { return !f.closest('.gp-hp'); });
      var firstBad = null;

      fields.forEach(function (field) {
        if (!validateField(field) && !firstBad) firstBad = field;
      });

      // Check-out cannot precede check-in
      var checkIn = $('#gp-enq-checkin', form);
      var checkOut = $('#gp-enq-checkout', form);
      if (checkIn && checkOut && checkIn.value && checkOut.value && checkOut.value < checkIn.value) {
        setError(checkOut, 'Check-out date must be after the check-in date.');
        if (!firstBad) firstBad = checkOut;
      }

      if (firstBad) {
        firstBad.focus();
        return;
      }

      var submitBtn = $('button[type="submit"]', form);
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.dataset.label = submitBtn.textContent;
        submitBtn.textContent = 'Sending…';
      }

      function finish(message, ok) {
        if (status) {
          status.textContent = message;
          status.hidden = false;
          status.setAttribute('role', ok ? 'status' : 'alert');
        }
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.textContent = submitBtn.dataset.label || 'Send Enquiry';
        }
        if (ok) form.reset();
      }

      fetch(form.getAttribute('action'), {
        method: 'POST',
        body: new FormData(form),
        headers: { 'X-Requested-With': 'fetch' }
      })
        .then(function (response) {
          if (!response.ok) throw new Error('Request failed');
          return response.json().catch(function () { return { ok: true }; });
        })
        .then(function (data) {
          if (data && data.ok === false) throw new Error(data.message || 'Request failed');
          finish('Thank you for contacting Hotel Green Plaza. Our team will get back to you shortly.', true);
        })
        .catch(function () {
          finish('We could not send your enquiry just now. Please call us or email us directly and we will help you straight away.', false);
        });
    });
  });

  /* ----------------------------------------------------------------------
     Footer year
     ---------------------------------------------------------------------- */

  $$('.gp-year').forEach(function (el) {
    el.textContent = String(new Date().getFullYear());
  });
})();
