/* ==========================================================================
   Hotel Green Plaza — enquiry form
   Honeypot spam guard, real-time field validation, async submit.
   ========================================================================== */

(function () {
  'use strict';

  function $(sel, ctx) { return (ctx || document).querySelector(sel); }
  function $$(sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); }

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

      var hp = $('.gp-hp input', form);
      if (hp && hp.value) return;

      var fields = $$('input, select, textarea', form).filter(function (f) { return !f.closest('.gp-hp'); });
      var firstBad = null;

      fields.forEach(function (field) {
        if (!validateField(field) && !firstBad) firstBad = field;
      });

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
})();
