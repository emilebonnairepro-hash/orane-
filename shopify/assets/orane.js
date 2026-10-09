/* ORANE — interactions de la page d'accueil
   - la bouille suit le curseur des yeux et rit quand on clique dessus
   - les stickers de la bannière se décollent et se déplacent
   - le manifeste s'allume mot après mot au défilement
   - le quiz « ta peau, là, maintenant ? »
   - l'étagère produits défile avec les flèches
   - le grand « orane » du bas glisse au défilement
   - fiche produit : la barre d'achat qui suit
   - panier : les sections ORANE se redessinent quand le panier change,
     et un ajout depuis n'importe où ouvre le panier en tiroir à jour
   - v4 : apparitions au défilement, chiffres qui comptent, barre de progression, curseur,
     explorateur d'actifs, cartes valeurs, bouille qui parle, formulaire de contact */
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
  let frame = null;
  window.addEventListener('pointermove', (e) => {
    if (frame) return;
    frame = requestAnimationFrame(() => {
      frame = null;
      document.querySelectorAll('.o-bouille').forEach((b) => {
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

  document.addEventListener('click', (e) => {
    const b = e.target.closest('.o-bouille');
    if (!b) return;
    b.classList.remove('is-happy');
    void b.getBoundingClientRect();
    b.classList.add('is-happy');
    burst(e.clientX, e.clientY);
    clearTimeout(b._t);
    b._t = setTimeout(() => b.classList.remove('is-happy'), 900);
  });

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
  const onCartPage = !!document.querySelector('main[data-template="cart"]');
  document.addEventListener('submit', async (e) => {
    const form = e.target.closest('.o-prod__form');
    if (!form || !window.fetch || !form.action.includes('/cart/add')) return;
    e.preventDefault();
    const btn = form.querySelector('button[type="submit"]');
    const label = btn.textContent;
    btn.disabled = true;
    // Avec le panier en tiroir : on demande aussi le tiroir redessiné, puis on l'ouvre (comme Dawn)
    const drawer = onCartPage ? null : document.querySelector('cart-drawer');
    const body = new FormData(form);
    if (drawer) { body.append('sections', 'cart-drawer,cart-icon-bubble'); body.append('sections_url', location.pathname); }
    try {
      const res = await fetch(form.action, { method: 'POST', headers: { Accept: 'application/json', 'X-Requested-With': 'XMLHttpRequest' }, body });
      const json = await res.json();
      if (!res.ok || json.status) throw new Error(json.description || json.message);
      const r = btn.getBoundingClientRect();
      burst(r.left + r.width / 2, r.top);
      if (onCartPage) { setTimeout(() => location.reload(), 450); return; }
      if (drawer && json.sections && typeof drawer.renderContents === 'function') {
        drawer.renderContents(json);
        if (btn.isConnected) { btn.disabled = false; }
        return;
      }
      if (btn.classList.contains('o-add')) btn.textContent = 'dans le panier ✦';
      btn.classList.add('is-added');
      document.dispatchEvent(new CustomEvent('orane:cart-updated'));
      fetch('/cart.js').then((c) => c.json()).then((cart) => {
        document.querySelectorAll('.cart-count-bubble span[aria-hidden="true"]').forEach((s) => { s.textContent = cart.item_count; });
      }).catch(() => {});
    } catch {
      form.submit();
      return;
    }
    setTimeout(() => { btn.textContent = label; btn.classList.remove('is-added'); btn.disabled = false; }, 2200);
  });

  // Sections ORANE qui dépendent du panier : on les redessine quand il change
  const refreshCartSections = () => {
    document.querySelectorAll('[data-o-refresh]').forEach(async (el) => {
      const id = el.dataset.oRefresh;
      el.classList.add('is-refreshing');
      try {
        const res = await fetch(`${location.pathname}?section_id=${encodeURIComponent(id)}`);
        const html = await res.text();
        const fresh = new DOMParser().parseFromString(html, 'text/html').querySelector(`[data-o-refresh="${id}"]`);
        if (fresh) el.replaceWith(fresh); else el.classList.remove('is-refreshing');
      } catch { el.classList.remove('is-refreshing'); }
    });
  };
  if (document.querySelector('[data-o-refresh]')) {
    if (typeof subscribe === 'function' && typeof PUB_SUB_EVENTS !== 'undefined') {
      subscribe(PUB_SUB_EVENTS.cartUpdate, refreshCartSections);
    }
    document.addEventListener('orane:cart-updated', refreshCartSections);
  }

  // Fiche produit : barre d'achat qui apparaît quand le vrai bouton sort de l'écran
  const sticky = document.querySelector('[data-o-sticky]');
  const realBtn = document.querySelector('product-form .product-form__submit, .product-form__submit');
  if (sticky && realBtn && 'IntersectionObserver' in window) {
    sticky.hidden = false;
    new IntersectionObserver(([entry]) => {
      const passed = !entry.isIntersecting && entry.boundingClientRect.top < 0;
      sticky.classList.toggle('is-on', passed);
    }).observe(realBtn);
    sticky.querySelector('[data-o-sticky-buy]')?.addEventListener('click', (e) => {
      realBtn.click();
      burst(e.clientX, e.clientY);
    });
    // Dawn remplace le bloc prix quand on change de variante : on suit toute la colonne
    const info = document.querySelector('.product__info-container');
    const target = sticky.querySelector('.o-sticky__price');
    if (info && target && 'MutationObserver' in window) {
      const sync = () => {
        const price = info.querySelector('.price--on-sale .price-item--sale, .price:not(.price--on-sale) .price__regular .price-item--regular');
        if (price && price.textContent.trim()) target.textContent = price.textContent.trim();
      };
      new MutationObserver(sync).observe(info, { subtree: true, childList: true });
    }
  }

  // ===== v4 : effets de tout le site =====
  const main = document.querySelector('main') || document.body;
  const inView = (el, cb, opts) => {
    if (!('IntersectionObserver' in window)) { cb(el); return; }
    const io = new IntersectionObserver((entries) => entries.forEach((en) => {
      if (en.isIntersecting) { io.unobserve(en.target); cb(en.target); }
    }), opts || { rootMargin: '0px 0px -12% 0px' });
    io.observe(el);
  };

  // Apparitions au défilement : seulement ce qui est encore sous l'écran (pas de clignotement en haut de page)
  if (!reduceMotion && 'IntersectionObserver' in window) {
    document.documentElement.classList.add('o-js');
    const RISE = '.o-title, .o-prod, .o-uni__tile, .o-stat, .o-val, .o-vedette__stage, .o-vedette__info, .o-actifs__panel, .o-actif-chip,'
      + ' .o-promises__list > *, .o-step, .o-q, .o-contact__card, .o-meet__stage, .o-wall > li, .o-howto, .o-actives, .o-duo, .o-pfaq__buddy, .o-match';
    // Un seul écouteur de défilement : tout ce qui est passé au-dessus du bas de l'écran apparaît (même après un saut d'ancre)
    let pending = [];
    main.querySelectorAll(RISE).forEach((el) => {
      if (el.closest('.o-drag, cart-drawer') || el.getBoundingClientRect().top < innerHeight) return;
      const i = el.parentElement ? [...el.parentElement.children].indexOf(el) : 0;
      el.style.setProperty('--rd', `${(i % 4) * 0.08}s`);
      el.classList.add('o-rise');
      pending.push(el);
    });
    let ticking = false;
    const reveal = () => {
      ticking = false;
      const limit = innerHeight * .9;
      pending = pending.filter((el) => {
        if (el.getBoundingClientRect().top < limit) { el.classList.add('is-in'); return false; }
        return true;
      });
      if (!pending.length) window.removeEventListener('scroll', onScroll);
    };
    const onScroll = () => { if (!ticking) { ticking = true; requestAnimationFrame(reveal); } };
    if (pending.length) { window.addEventListener('scroll', onScroll, { passive: true }); window.addEventListener('resize', onScroll); }
  }
  document.querySelectorAll('.o-never__item').forEach((el) => inView(el, (t) => t.classList.add('is-in')));

  // Les chiffres qui comptent
  document.querySelectorAll('[data-o-count]').forEach((el) => {
    const target = parseFloat(el.dataset.oCount);
    if (!isFinite(target) || reduceMotion) return;
    el.textContent = '0';
    inView(el, () => {
      const t0 = performance.now();
      const tick = (t) => {
        const k = Math.min(1, (t - t0) / 1400);
        el.textContent = String(Math.round(target * (1 - Math.pow(1 - k, 3))));
        if (k < 1) requestAnimationFrame(tick);
      };
      requestAnimationFrame(tick);
    });
  });

  // Barre de progression de lecture
  if (document.documentElement.scrollHeight > innerHeight * 2.2) {
    const bar = document.createElement('div');
    bar.className = 'o-progress';
    bar.setAttribute('aria-hidden', 'true');
    document.body.appendChild(bar);
    const upd = () => {
      const max = document.documentElement.scrollHeight - innerHeight;
      bar.style.setProperty('--p', max > 0 ? (scrollY / max).toFixed(4) : 0);
    };
    window.addEventListener('scroll', upd, { passive: true });
    upd();
  }

  // Curseur ORANE (souris uniquement) + boutons aimantés
  if (!reduceMotion && matchMedia('(hover: hover) and (pointer: fine)').matches) {
    const cur = document.createElement('div');
    cur.className = 'o-cursor';
    cur.setAttribute('aria-hidden', 'true');
    cur.dataset.label = 'voir ✦';
    document.body.appendChild(cur);
    let x = -100, y = -100, cx = -100, cy = -100, running = false;
    const loop = () => {
      cx += (x - cx) * .22; cy += (y - cy) * .22;
      cur.style.transform = `translate3d(${cx}px, ${cy}px, 0)`;
      if (Math.abs(x - cx) > .3 || Math.abs(y - cy) > .3) requestAnimationFrame(loop); else running = false;
    };
    window.addEventListener('pointermove', (e) => {
      if (e.pointerType !== 'mouse') return;
      x = e.clientX; y = e.clientY;
      cur.classList.add('is-on');
      const t = e.target instanceof Element ? e.target : null;
      const prod = t && t.closest('.o-prod__media, .o-uni__link, .o-vedette__media, .o-actifs__prod a, .card__media');
      cur.classList.toggle('is-prod', !!prod);
      cur.classList.toggle('is-link', !prod && !!(t && t.closest('a, button, summary, label, [role="tab"]')));
      if (!running) { running = true; requestAnimationFrame(loop); }
    }, { passive: true });
    document.addEventListener('pointerleave', () => cur.classList.remove('is-on'));

    document.addEventListener('pointermove', (e) => {
      const b = e.target instanceof Element && e.target.closest('.o-btn, .o-round-btn, .o-uni__go');
      document.querySelectorAll('.is-magnet').forEach((m) => { if (m !== b) { m.style.translate = ''; m.classList.remove('is-magnet'); } });
      if (!b) return;
      const r = b.getBoundingClientRect();
      b.classList.add('is-magnet');
      b.style.translate = `${(e.clientX - r.left - r.width / 2) * .18}px ${(e.clientY - r.top - r.height / 2) * .25}px`;
    }, { passive: true });
  }

  // Explorateur d'actifs
  document.querySelectorAll('[data-o-actifs]').forEach((root) => {
    const chips = [...root.querySelectorAll('[data-actif]')];
    const pick = (chip, e) => {
      const h = chip.dataset.actif;
      chips.forEach((c) => c.setAttribute('aria-selected', String(c === chip)));
      root.querySelectorAll('[data-why]').forEach((w) => w.classList.toggle('is-on', w.dataset.why === h));
      root.querySelectorAll('[data-actifs]').forEach((p) => p.classList.toggle('is-on', p.dataset.actifs.includes(`|${h}|`)));
      if (e && e.clientX) burst(e.clientX, e.clientY);
    };
    chips.forEach((chip, i) => {
      chip.addEventListener('click', (e) => pick(chip, e));
      chip.addEventListener('keydown', (e) => {
        if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return;
        e.preventDefault();
        const next = chips[(i + (e.key === 'ArrowRight' ? 1 : chips.length - 1)) % chips.length];
        next.focus(); pick(next);
      });
    });
  });

  // Cartes valeurs qui se retournent (clic ou clavier)
  document.addEventListener('click', (e) => {
    const card = e.target.closest('.o-val__card');
    if (card) card.setAttribute('aria-pressed', String(card.getAttribute('aria-pressed') !== 'true'));
  });

  // La bouille qui parle
  document.querySelectorAll('[data-o-meet]').forEach((root) => {
    const bubble = root.querySelector('[data-o-meet-bubble]');
    const count = root.querySelector('[data-o-meet-count]');
    const tpl = root.querySelector('[data-o-meet-lines]');
    const lines = tpl ? [...tpl.content.querySelectorAll('span')].map((s) => s.textContent.trim()).filter(Boolean) : [];
    let n = 0;
    root.querySelector('[data-o-meet-btn]')?.addEventListener('click', () => {
      n += 1;
      if (count) count.textContent = n;
      if (bubble && lines.length) {
        bubble.textContent = lines[n % lines.length];
        bubble.classList.remove('is-new'); void bubble.offsetWidth; bubble.classList.add('is-new');
      }
    });
  });

  // Contact : le sujet change la bulle et affiche le n° de commande si besoin ; la jauge suit le message
  document.querySelectorAll('[data-o-contact]').forEach((root) => {
    const bubble = root.querySelector('[data-o-contact-bubble]');
    const order = root.querySelector('[data-o-order]');
    const sync = (r, animate) => {
      if (!r) return;
      if (order) order.hidden = !r.hasAttribute('data-order');
      if (bubble && r.dataset.bubble && animate) {
        bubble.textContent = r.dataset.bubble;
        bubble.classList.remove('is-new'); void bubble.offsetWidth; bubble.classList.add('is-new');
      }
    };
    root.querySelectorAll('input[name="contact[sujet]"]').forEach((r) => r.addEventListener('change', () => sync(r, true)));
    sync(root.querySelector('input[name="contact[sujet]"]:checked'), false);
    const msg = root.querySelector('[data-o-msg]');
    const meter = root.querySelector('[data-o-meter]');
    if (msg && meter) {
      const m = () => meter.style.setProperty('--m', `${Math.min(100, msg.value.trim().length / 1.6)}%`);
      msg.addEventListener('input', m); m();
    }
    root.querySelector('form')?.addEventListener('submit', (e) => {
      const btn = e.target.querySelector('button[type="submit"]');
      if (btn) { const r = btn.getBoundingClientRect(); burst(r.left + r.width / 2, r.top); }
    });
    const done = root.querySelector('[data-o-contact-done]');
    if (done) { done.scrollIntoView({ block: 'center' }); done.focus({ preventScroll: true }); const b = done.querySelector('.o-bouille'); b?.classList.add('is-happy'); }
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
