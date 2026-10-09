/* ORANE — interactions de la page d'accueil
   - la bouille suit le curseur des yeux et rit quand on clique dessus
   - les stickers de la bannière se décollent et se déplacent
   - le manifeste s'allume mot après mot au défilement
   - le quiz « ta peau, là, maintenant ? »
   - l'étagère produits défile avec les flèches
   - le grand « orane » du bas glisse au défilement */
(() => {
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const SPARK = '<path d="M20 2 C22 14 26 18 38 20 C26 22 22 26 20 38 C18 26 14 22 2 20 C14 18 18 14 20 2 Z" stroke="#2A1240" stroke-width="2.5" stroke-linejoin="round"/>';
  const BURST_COLORS = ['#D4F23A', '#FF5FA8', '#FFF3E3', '#2CC8F5'];

  function burst(x, y) {
    if (reduceMotion) return;
    for (let i = 0; i < 8; i++) {
      const s = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
      s.setAttribute('viewBox', '0 0 40 40');
      s.setAttribute('class', 'o-burst');
      s.setAttribute('fill', BURST_COLORS[i % BURST_COLORS.length]);
      s.innerHTML = SPARK;
      const a = (Math.PI * 2 * i) / 8 + Math.random() * .4;
      const d = 60 + Math.random() * 50;
      s.style.left = `${x - 13}px`;
      s.style.top = `${y - 13}px`;
      s.style.setProperty('--dx', `${Math.cos(a) * d}px`);
      s.style.setProperty('--dy', `${Math.sin(a) * d}px`);
      document.body.appendChild(s);
      s.addEventListener('animationend', () => s.remove());
    }
  }

  // La bouille : l'œil ouvert suit le curseur, un clic la fait rire
  const bouilles = [...document.querySelectorAll('.o-bouille')];
  if (bouilles.length) {
    let frame = null;
    window.addEventListener('pointermove', (e) => {
      if (frame) return;
      frame = requestAnimationFrame(() => {
        frame = null;
        bouilles.forEach((b) => {
          const eye = b.querySelector('.o-eye-open');
          if (!eye) return;
          const r = b.getBoundingClientRect();
          if (r.bottom < 0 || r.top > innerHeight) return;
          const dx = e.clientX - (r.left + r.width * .35);
          const dy = e.clientY - (r.top + r.height * .4);
          const len = Math.hypot(dx, dy) || 1;
          const k = Math.min(1, len / 300) * 4;
          eye.style.transform = `translate(${(dx / len) * k}px, ${(dy / len) * k}px)`;
        });
      });
    }, { passive: true });

    bouilles.forEach((b) => {
      b.addEventListener('click', (e) => {
        b.classList.remove('is-happy');
        void b.getBoundingClientRect();
        b.classList.add('is-happy');
        burst(e.clientX, e.clientY);
        clearTimeout(b._t);
        b._t = setTimeout(() => b.classList.remove('is-happy'), 900);
      });
    });
  }

  // Stickers qu'on décolle
  document.querySelectorAll('.o-drag').forEach((el) => {
    let start = null;
    const base = { x: 0, y: 0 };
    el.addEventListener('pointerdown', (e) => {
      start = { x: e.clientX - base.x, y: e.clientY - base.y };
      el.setPointerCapture(e.pointerId);
      el.classList.add('is-dragging');
    });
    el.addEventListener('pointermove', (e) => {
      if (!start) return;
      base.x = e.clientX - start.x;
      base.y = e.clientY - start.y;
      el.style.translate = `${base.x}px ${base.y}px`;
    });
    const stop = () => { start = null; el.classList.remove('is-dragging'); };
    el.addEventListener('pointerup', stop);
    el.addEventListener('pointercancel', stop);
  });

  // Manifeste : on découpe en mots, puis on les allume au défilement
  document.querySelectorAll('[data-o-reveal]').forEach((root) => {
    if (reduceMotion) { root.closest('.o-manifesto')?.classList.add('is-static'); return; }
    const words = [];
    [...root.childNodes].forEach((node) => {
      if (node.nodeType === Node.TEXT_NODE) {
        const frag = document.createDocumentFragment();
        node.textContent.split(/(\s+)/).forEach((part) => {
          if (!part) return;
          if (/^\s+$/.test(part)) { frag.appendChild(document.createTextNode(part)); return; }
          const w = document.createElement('span');
          w.className = 'o-w';
          w.textContent = part;
          frag.appendChild(w);
          words.push(w);
        });
        node.replaceWith(frag);
      } else if (node.nodeType === Node.ELEMENT_NODE) {
        node.classList.add('o-w');
        words.push(node);
      }
    });
    const update = () => {
      const r = root.getBoundingClientRect();
      const p = Math.min(1, Math.max(0, (innerHeight * .85 - r.top) / (r.height + innerHeight * .35)));
      const n = Math.round(p * words.length);
      words.forEach((w, i) => w.classList.toggle('is-on', i < n));
    };
    window.addEventListener('scroll', update, { passive: true });
    window.addEventListener('resize', update);
    update();
  });

  // Quiz
  document.querySelectorAll('[data-o-quiz]').forEach((quiz) => {
    const answer = quiz.querySelector('.o-quiz__answer');
    const moods = quiz.querySelectorAll('.o-mood');
    moods.forEach((btn) => {
      btn.addEventListener('click', (e) => {
        moods.forEach((m) => m.setAttribute('aria-pressed', String(m === btn)));
        quiz.querySelectorAll('.o-match').forEach((m) => m.classList.toggle('is-on', m.id === btn.dataset.target));
        answer.classList.add('has-match');
        const b = answer.querySelector('.o-match.is-on .o-bouille');
        if (b) { b.classList.add('is-happy'); setTimeout(() => b.classList.remove('is-happy'), 900); }
        burst(e.clientX, e.clientY);
        if (innerWidth < 990) answer.scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth', block: 'center' });
      });
    });
  });

  // Étagère : flèches
  document.querySelectorAll('[data-o-shelf]').forEach((shelf) => {
    const track = shelf.querySelector('.o-shelf__track');
    shelf.querySelectorAll('[data-dir]').forEach((btn) => {
      btn.addEventListener('click', () => {
        const card = track.querySelector('.o-prod');
        const step = card ? card.getBoundingClientRect().width + 32 : 320;
        track.scrollBy({ left: step * Number(btn.dataset.dir), behavior: reduceMotion ? 'auto' : 'smooth' });
      });
    });
  });

  // Ajout au panier sans quitter la page (sinon, le formulaire s'envoie normalement)
  document.querySelectorAll('.o-prod__form').forEach((form) => {
    form.addEventListener('submit', async (e) => {
      if (!window.fetch || !form.action.includes('/cart/add')) return;
      e.preventDefault();
      const btn = form.querySelector('.o-add');
      const label = btn.textContent;
      try {
        const res = await fetch(form.action, { method: 'POST', headers: { Accept: 'application/json' }, body: new FormData(form) });
        if (!res.ok) throw new Error();
        btn.textContent = 'dans le panier ✦';
        btn.classList.add('is-added');
        const r = btn.getBoundingClientRect();
        burst(r.left + r.width / 2, r.top);
        document.dispatchEvent(new CustomEvent('orane:cart-updated'));
        fetch('/cart.js').then((c) => c.json()).then((cart) => {
          document.querySelectorAll('.cart-count-bubble span[aria-hidden="true"]').forEach((s) => { s.textContent = cart.item_count; });
        }).catch(() => {});
      } catch {
        form.submit();
        return;
      }
      setTimeout(() => { btn.textContent = label; btn.classList.remove('is-added'); }, 2200);
    });
  });

  // Le grand « orane » du bas glisse au défilement
  const outro = document.querySelector('.o-outro__word');
  if (outro && !reduceMotion) {
    const move = () => {
      const r = outro.getBoundingClientRect();
      const p = (innerHeight - r.top) / (innerHeight + r.height);
      outro.style.transform = `translateX(${(0.5 - p) * 16}%)`;
    };
    window.addEventListener('scroll', move, { passive: true });
    move();
  }
})();
