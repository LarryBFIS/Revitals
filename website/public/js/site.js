// BYLD site behaviour. No dependencies. Every effect degrades gracefully and respects reduced motion.
(() => {
  const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const fine = matchMedia('(pointer: fine)').matches;
  const money = n => '$' + Math.round(n).toLocaleString('en-US');
  const onView = (el, fn, opts = { threshold: 0.25 }) => {
    if (!('IntersectionObserver' in window)) return fn(true);
    const io = new IntersectionObserver(es => es.forEach(en => fn(en.isIntersecting, io)), opts);
    io.observe(el);
    return io;
  };

  /* ---------- header, menus ---------- */
  const hdr = $('.hdr');
  addEventListener('scroll', () => hdr && hdr.classList.toggle('scrolled', scrollY > 8), { passive: true });

  const burger = $('.burger'), mnav = $('#mnav');
  burger?.addEventListener('click', () => {
    const open = !mnav.hasAttribute('data-open');
    mnav.toggleAttribute('data-open', open);
    burger.setAttribute('aria-expanded', open);
    document.body.style.overflow = open ? 'hidden' : '';
  });
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

  /* ---------- reveal on scroll ---------- */
  const rv = $$('.rv');
  if ('IntersectionObserver' in window && !reduce) {
    const io = new IntersectionObserver(es => es.forEach(en => {
      if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
    }), { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    rv.forEach(el => io.observe(el));
  } else rv.forEach(el => el.classList.add('in'));

  /* ---------- number tweening ---------- */
  const tween = (el, from, to, { dur = 1400, dec = 0, fmt } = {}) => {
    if (reduce) { el.textContent = fmt ? fmt(to) : to.toFixed(dec); return; }
    const t0 = performance.now();
    const step = now => {
      const k = Math.min(1, (now - t0) / dur), ease = 1 - Math.pow(1 - k, 4);
      const v = from + (to - from) * ease;
      el.textContent = fmt ? fmt(v) : v.toFixed(dec);
      if (k < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  };

  // Stats: HTML holds the real value (for search engines); animate up to it when visible.
  $$('[data-count]').forEach(el => {
    const m = el.textContent.trim().match(/^([^\d]*)([\d.,]+)(.*)$/);
    if (!m) return;
    const [, pre, num, suf] = m, to = parseFloat(num.replace(/,/g, '')), dec = (num.split('.')[1] || '').length;
    onView(el, (vis, io) => {
      if (!vis) return;
      io && io.disconnect();
      tween(el, 0, to, { dur: 1800, fmt: v => pre + v.toFixed(dec) + suf });
    }, { threshold: 0.6 });
  });

  /* ---------- hero: WebGL aurora + pointer light ---------- */
  const hero = $('[data-hero]');
  if (hero) {
    hero.addEventListener('pointermove', ev => {
      const r = hero.getBoundingClientRect();
      hero.style.setProperty('--mx', ((ev.clientX - r.left) / r.width * 100) + '%');
      hero.style.setProperty('--my', ((ev.clientY - r.top) / r.height * 100) + '%');
    });
    const cv = $('.aurora', hero);
    const gl = cv && !reduce && cv.getContext('webgl', { antialias: false, premultipliedAlpha: false, alpha: true });
    if (gl) {
      const vs = 'attribute vec2 p;void main(){gl_Position=vec4(p,0.,1.);}';
      const fs = `precision mediump float;uniform vec2 r;uniform float t;uniform vec2 m;
        float h(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}
        float n(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);return mix(mix(h(i),h(i+vec2(1,0)),f.x),mix(h(i+vec2(0,1)),h(i+vec2(1,1)),f.x),f.y);}
        float fbm(vec2 p){float v=0.,a=.5;for(int i=0;i<5;i++){v+=a*n(p);p*=2.02;a*=.5;}return v;}
        void main(){vec2 uv=gl_FragCoord.xy/r;vec2 q=uv*vec2(r.x/r.y,1.)*1.6;
          float a=fbm(q+vec2(t*.04,t*.02));float b=fbm(q*1.4+a*1.6-vec2(t*.03,-t*.05));
          vec3 night=vec3(.031,.043,.122),sky=vec3(.36,.75,1.),ind=vec3(.49,.55,1.),mint=vec3(.24,.86,.59);
          vec3 c=mix(night,ind,smoothstep(.45,.95,b)*.55);c=mix(c,sky,smoothstep(.55,1.,a*b*1.9)*.6);c+=mint*smoothstep(.78,1.,b)*.08;
          float d=distance(uv,m);c+=sky*.16*exp(-d*d*9.);
          float v=smoothstep(1.25,.15,distance(uv,vec2(.65,.95)));c=mix(night,c,v*.9);
          gl_FragColor=vec4(c,1.);}`;
      const sh = (type, src) => { const s = gl.createShader(type); gl.shaderSource(s, src); gl.compileShader(s); return s; };
      const pr = gl.createProgram();
      gl.attachShader(pr, sh(gl.VERTEX_SHADER, vs)); gl.attachShader(pr, sh(gl.FRAGMENT_SHADER, fs)); gl.linkProgram(pr);
      if (gl.getProgramParameter(pr, gl.LINK_STATUS)) {
        gl.useProgram(pr);
        gl.bindBuffer(gl.ARRAY_BUFFER, gl.createBuffer());
        gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
        const loc = gl.getAttribLocation(pr, 'p');
        gl.enableVertexAttribArray(loc); gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);
        const uR = gl.getUniformLocation(pr, 'r'), uT = gl.getUniformLocation(pr, 't'), uM = gl.getUniformLocation(pr, 'm');
        let mx = .7, my = .7, tx = .7, ty = .7, running = false, raf;
        hero.addEventListener('pointermove', ev => { const r = hero.getBoundingClientRect(); tx = (ev.clientX - r.left) / r.width; ty = 1 - (ev.clientY - r.top) / r.height; });
        const size = () => { const s = 0.5; cv.width = cv.clientWidth * s; cv.height = cv.clientHeight * s; gl.viewport(0, 0, cv.width, cv.height); };
        size(); addEventListener('resize', size);
        const t0 = performance.now();
        const frame = now => {
          mx += (tx - mx) * .04; my += (ty - my) * .04;
          gl.uniform2f(uR, cv.width, cv.height); gl.uniform1f(uT, (now - t0) / 1000); gl.uniform2f(uM, mx, my);
          gl.drawArrays(gl.TRIANGLES, 0, 3);
          if (running) raf = requestAnimationFrame(frame);
        };
        onView(hero, vis => { if (vis && !running) { running = true; raf = requestAnimationFrame(frame); } else if (!vis) { running = false; cancelAnimationFrame(raf); } }, { threshold: 0 });
        requestAnimationFrame(() => cv.classList.add('ready'));
      }
    }
  }

  /* ---------- hero command center: auto-cycling tabs ---------- */
  $$('[data-cc]').forEach(cc => {
    const tabs = $$('.cc-tab', cc), panels = $$('.cc-panel', cc);
    const DUR = 6500;
    let idx = 0, timer, left = DUR, started = 0, visible = true;
    const show = i => {
      idx = (i + tabs.length) % tabs.length;
      tabs.forEach((t, k) => t.setAttribute('aria-selected', k === idx));
      panels.forEach((p, k) => {
        p.classList.remove('on');
        if (k === idx) { void p.offsetWidth; p.classList.add('on'); }
      });
      $$('[data-tick]', panels[idx]).forEach(el => tween(el, +el.dataset.from, +el.dataset.to, { dur: 1300, dec: +(el.dataset.dec || 0) }));
      // restart the progress bar
      const bar = $('.cc-prog', tabs[idx]); bar.style.animation = 'none'; void bar.offsetWidth; bar.style.animation = '';
      schedule(DUR);
    };
    const schedule = ms => { clearTimeout(timer); left = ms; started = performance.now(); if (!reduce && visible) timer = setTimeout(() => show(idx + 1), ms); };
    tabs.forEach((t, k) => t.addEventListener('click', () => show(k)));
    cc.addEventListener('mouseenter', () => { clearTimeout(timer); left -= performance.now() - started; cc.classList.add('paused'); });
    cc.addEventListener('mouseleave', () => { cc.classList.remove('paused'); schedule(Math.max(600, left)); });
    onView(cc, vis => { visible = vis; if (vis) schedule(left); else clearTimeout(timer); }, { threshold: 0.2 });
    show(0);
  });

  /* ---------- 3D tilt ---------- */
  if (fine && !reduce) $$('[data-tilt]').forEach(el => {
    const inner = el.firstElementChild;
    el.addEventListener('pointermove', ev => {
      const r = el.getBoundingClientRect(), x = (ev.clientX - r.left) / r.width - .5, y = (ev.clientY - r.top) / r.height - .5;
      inner.style.transform = `rotateY(${x * 8}deg) rotateX(${-y * 8}deg)`;
    });
    el.addEventListener('pointerleave', () => { inner.style.transform = ''; });
  });

  /* ---------- card spotlight ---------- */
  if (fine) document.addEventListener('pointermove', ev => {
    const c = ev.target.closest && ev.target.closest('.card,.feat,.tile');
    if (!c) return;
    const r = c.getBoundingClientRect();
    c.style.setProperty('--mx', (ev.clientX - r.left) + 'px'); c.style.setProperty('--my', (ev.clientY - r.top) + 'px');
  }, { passive: true });

  /* ---------- magnetic buttons ---------- */
  if (fine && !reduce) $$('[data-magnetic]').forEach(b => {
    b.addEventListener('pointermove', ev => {
      const r = b.getBoundingClientRect();
      b.style.transform = `translate(${(ev.clientX - r.left - r.width / 2) * .18}px,${(ev.clientY - r.top - r.height / 2) * .3}px)`;
    });
    b.addEventListener('pointerleave', () => { b.style.transform = ''; });
  });

  /* ---------- range inputs: filled track ---------- */
  const fill = i => i.style.setProperty('--p', ((i.value - i.min) / (i.max - i.min) * 100) + '%');
  $$('input[type=range]').forEach(i => { fill(i); i.addEventListener('input', () => fill(i)); });

  /* ---------- franchise fee calculator ---------- */
  $$('[data-calc]').forEach(c => {
    const v = id => +$('#' + id, c).value;
    const out = k => $(`[data-r="${k}"]`, c);
    let last = { rev: 0, fee: 0, ten: 0 };
    const calc = () => {
      $$('input', c).forEach(i => { const o = $(`[data-out="${i.id}"]`, c); o.textContent = (i.dataset.pre || '') + (+i.value).toLocaleString('en-US') + (i.dataset.suf || ''); });
      const rev = v('c-rooms') * v('c-adr') * v('c-occ') / 100 * 365, fee = rev * v('c-fee') / 100, ten = fee * 10;
      tween(out('rev'), last.rev, rev, { dur: 500, fmt: money });
      tween(out('fee'), last.fee, fee, { dur: 500, fmt: money });
      tween(out('ten'), last.ten, ten, { dur: 500, fmt: money });
      out('bar').style.width = Math.min(100, v('c-fee') / 20 * 100) + '%';
      last = { rev, fee, ten };
    };
    $$('input', c).forEach(i => i.addEventListener('input', calc));
    calc();
  });

  /* ---------- pricing simulator ---------- */
  $$('[data-sim]').forEach(s => {
    const FLOOR = 99, CEIL = 189, MIN = 80, MAX = 200;
    const g = k => $(`[data-s="${k}"]`, s), val = id => +$('#' + id, s).value;
    const pct = x => ((x - MIN) / (MAX - MIN) * 100) + '%';
    const band = $('.g-band', s); band.style.left = pct(FLOOR); band.style.right = (100 - parseFloat(pct(CEIL))) + '%';
    $$('.gauge span', s)[0].style.left = pct(FLOOR); $$('.gauge span', s)[1].style.left = pct(CEIL);
    let last = 154, rate = 154;
    const calc = () => {
      const pace = val('s-pace'), comp = val('s-comp'), dem = val('s-dem');
      $('[data-out="s-pace"]', s).textContent = (pace > 0 ? '+' : '') + pace + ' rooms';
      $('[data-out="s-comp"]', s).textContent = '$' + comp;
      $('[data-out="s-dem"]', s).textContent = dem + ' of 5';
      const paceAdj = Math.round(pace * 1.25), demAdj = (dem - 3) * 6, raw = comp + paceAdj + demAdj;
      rate = Math.max(FLOOR, Math.min(CEIL, raw));
      tween(g('rate'), last, rate, { dur: 400 }); last = rate;
      g('clamp').textContent = raw > CEIL ? 'Ceiling applied' : raw < FLOOR ? 'Floor applied' : '';
      g('needle').style.left = pct(Math.max(MIN, Math.min(MAX, raw)));
      const sign = n => (n >= 0 ? '+$' : '−$') + Math.abs(n);
      g('why').innerHTML = `<li><span>Comp set median</span><b>$${comp}</b></li><li><span>Pace ${pace >= 0 ? 'ahead of' : 'behind'} curve</span><b>${sign(paceAdj)}</b></li><li><span>Demand pressure ${dem}/5</span><b>${sign(demAdj)}</b></li>`;
      g('chat').hidden = true;
    };
    $$('input', s).forEach(i => i.addEventListener('input', calc));
    g('send').addEventListener('click', () => {
      const chat = g('chat');
      chat.hidden = false;
      chat.innerHTML = '<div class="av">RM</div><div><b>Your revenue manager</b><span class="typing"><i></i><i></i><i></i></span></div>';
      setTimeout(() => {
        chat.innerHTML = `<div class="av">RM</div><div><b>Your revenue manager</b>Checked the pace and the comp set. Approved: Friday King at $${rate}, live on all channels ✅</div>`;
      }, reduce ? 0 : 1100);
    });
    calc();
  });

  /* ---------- scrollytelling ---------- */
  $$('[data-story]').forEach(st => {
    const steps = $$('.story-step', st), vis = $$('.story-vis', st), dots = $$('.story-dots i', st);
    const set = i => {
      steps.forEach((s, k) => s.classList.toggle('on', k === i));
      vis.forEach((v, k) => v.classList.toggle('on', k === i));
      dots.forEach((d, k) => d.classList.toggle('on', k === i));
    };
    if (!('IntersectionObserver' in window)) return set(0);
    const io = new IntersectionObserver(es => es.forEach(en => { if (en.isIntersecting) set(+en.target.dataset.step); }), { rootMargin: '-45% 0px -45% 0px' });
    steps.forEach(s => io.observe(s));
    set(0);
  });

  /* ---------- WhatsApp chat playback ---------- */
  $$('[data-chat]').forEach(body => {
    if (reduce) return;
    const msgs = $$('.msg', body);
    body.classList.add('armed');
    let played = false;
    onView(body, (vis, io) => {
      if (!vis || played) return;
      played = true; io && io.disconnect();
      let t = 300;
      msgs.forEach(m => {
        if (!m.classList.contains('me')) {
          const ty = document.createElement('div');
          ty.className = 'typing-msg'; ty.innerHTML = '<span class="typing"><i></i><i></i><i></i></span>';
          setTimeout(() => body.insertBefore(ty, m), t);
          t += 900;
          setTimeout(() => { ty.remove(); m.classList.add('show'); }, t);
        } else { t += 500; setTimeout(() => m.classList.add('show'), t); }
        t += 450;
      });
    }, { threshold: 0.5 });
  });

  /* ---------- video ---------- */
  $$('video[data-autoplay]').forEach(v => {
    if (reduce) return;
    onView(v, vis => { if (vis) { v.play().catch(() => {}); } else v.pause(); }, { threshold: 0.35 });
  });
  const modal = $('#vmodal');
  if (modal) {
    const mv = $('video', modal);
    $$('[data-video-open]').forEach(b => b.addEventListener('click', () => {
      if (typeof modal.showModal === 'function') modal.showModal(); else modal.setAttribute('open', '');
      mv.currentTime = 0; mv.muted = false; mv.play().catch(() => {});
    }));
    const close = () => { mv.pause(); modal.close ? modal.close() : modal.removeAttribute('open'); };
    $('[data-video-close]', modal).addEventListener('click', close);
    modal.addEventListener('click', ev => { if (ev.target === modal) close(); });
    modal.addEventListener('close', () => mv.pause());
  }

  /* ---------- contact form ---------- */
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
    location.href = 'mailto:' + form.dataset.to + '?subject=' + encodeURIComponent('Revenue review request: ' + (data.name || '')) + '&body=' + encodeURIComponent(body);
  });
})();
