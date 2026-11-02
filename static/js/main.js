// تبديل قائمة الجوال
const burger = document.getElementById('burger');
const nav = document.getElementById('navLinks');
if (burger && nav) {
  burger.addEventListener('click', () => nav.classList.toggle('open'));
  nav.querySelectorAll('a').forEach(a => a.addEventListener('click', () => nav.classList.remove('open')));
}

// فلترة القائمة
const chips = document.querySelectorAll('.chip');
const dishes = document.querySelectorAll('.dish-card');
chips.forEach(chip => {
  chip.addEventListener('click', () => {
    chips.forEach(c => c.classList.remove('active'));
    chip.classList.add('active');
    const cat = chip.dataset.cat;
    dishes.forEach(d => {
      d.style.display = (cat === 'all' || d.dataset.cat === cat) ? '' : 'none';
    });
  });
});
