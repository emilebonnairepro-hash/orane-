// ORANE — petites interactions

document.documentElement.classList.add('js');

// Menu mobile
const toggle = document.querySelector('.nav__toggle');
const menu = document.querySelector('#menu');

toggle.addEventListener('click', () => {
  const open = toggle.getAttribute('aria-expanded') === 'true';
  toggle.setAttribute('aria-expanded', String(!open));
  toggle.setAttribute('aria-label', open ? 'Ouvrir le menu' : 'Fermer le menu');
  menu.classList.toggle('is-open', !open);
});

menu.querySelectorAll('a').forEach((link) => {
  link.addEventListener('click', () => {
    toggle.setAttribute('aria-expanded', 'false');
    toggle.setAttribute('aria-label', 'Ouvrir le menu');
    menu.classList.remove('is-open');
  });
});

// Apparition des blocs au défilement
const reveals = document.querySelectorAll('.reveal');
if ('IntersectionObserver' in window) {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-in');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.15 });
  reveals.forEach((el) => observer.observe(el));
} else {
  reveals.forEach((el) => el.classList.add('is-in'));
}

// Toast
const toast = document.querySelector('.toast');
let toastTimer;
function showToast(message) {
  toast.textContent = message;
  toast.classList.add('is-visible');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toast.classList.remove('is-visible'), 2600);
}

// Panier (démo)
let cartCount = 0;
document.querySelectorAll('.btn--add').forEach((btn) => {
  btn.addEventListener('click', () => {
    cartCount += 1;
    showToast(`${btn.dataset.name} file dans ton panier ✦ (${cartCount})`);
  });
});

// Newsletter (démo, aucun envoi)
const form = document.querySelector('.club__form');
const msg = document.querySelector('.club__msg');
form.addEventListener('submit', (event) => {
  event.preventDefault();
  const email = form.email.value.trim();
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    msg.textContent = 'Hmm, cette adresse a une drôle de bouille. Tu vérifies ?';
    form.email.focus();
    return;
  }
  msg.textContent = 'Bienvenue dans la bande ! Ton code -10 % arrive dans ta boîte.';
  form.reset();
});

// Année du footer
document.querySelector('#year').textContent = new Date().getFullYear();
