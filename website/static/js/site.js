// BYLD site: menu, mega dropdown, reveal-on-scroll, contact form. No dependencies.
(() => {
  const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];

  // Mobile menu
  const burger = $('.burger'), mnav = $('#mnav');
  burger?.addEventListener('click', () => {
    const open = !mnav.hasAttribute('data-open');
    mnav.toggleAttribute('data-open', open);
    burger.setAttribute('aria-expanded', open);
    document.body.style.overflow = open ? 'hidden' : '';
  });

  // Platform mega menu: hover on desktop, click and keyboard everywhere
  $$('.dd').forEach(dd => {
    const btn = $('button', dd);
    let t;
    const set = v => { dd.toggleAttribute('data-open', v); btn.setAttribute('aria-expanded', v); };
    dd.addEventListener('mouseenter', () => { clearTimeout(t); set(true); });
    dd.addEventListener('mouseleave', () => { t = setTimeout(() => set(false), 120); });
    btn.addEventListener('click', () => set(!dd.hasAttribute('data-open')));
    document.addEventListener('keydown', ev => { if (ev.key === 'Escape') set(false); });
    document.addEventListener('click', ev => { if (!dd.contains(ev.target)) set(false); });
  });

  // Reveal on scroll
  const rv = $$('.rv');
  if ('IntersectionObserver' in window && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
    const io = new IntersectionObserver(es => es.forEach(en => {
      if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
    }), { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    rv.forEach(el => io.observe(el));
  } else rv.forEach(el => el.classList.add('in'));

  // Contact form: POST to data-endpoint when configured, otherwise open a pre-filled email.
  const form = $('#contact');
  form?.addEventListener('submit', async ev => {
    ev.preventDefault();
    const data = Object.fromEntries(new FormData(form));
    const endpoint = form.dataset.endpoint;
    const btn = $('button[type=submit]', form);
    if (endpoint) {
      btn.disabled = true; btn.textContent = 'Sending…';
      try {
        const r = await fetch(endpoint, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) });
        if (!r.ok) throw new Error(String(r.status));
        form.innerHTML = '<h3>Thank you.</h3><p style="margin-top:10px;color:var(--muted)">We\'ll be in touch within one business day.</p>';
        return;
      } catch (err) { btn.disabled = false; btn.textContent = 'Request my revenue review'; }
    }
    const body = Object.entries(data).map(([k, v]) => k[0].toUpperCase() + k.slice(1) + ': ' + v).join('\n');
    const subject = 'Revenue review request: ' + (data.name || '');
    location.href = 'mailto:' + form.dataset.to + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
  });
})();
