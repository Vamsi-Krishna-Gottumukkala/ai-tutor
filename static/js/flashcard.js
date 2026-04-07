// ── Flashcard JS ────────────────────────────────────────────

document.addEventListener('DOMContentLoaded', () => {
  const cards = document.querySelectorAll('.flashcard-scene');
  let currentIndex = 0;
  const total = cards.length;
  const counter = document.getElementById('card-counter');

  const endScene = document.querySelector('.flashcard-end-scene');

  function showCard(index) {
    if (index === total && endScene) {
      cards.forEach(c => c.style.display = 'none');
      endScene.style.display = 'block';
      if (counter) counter.textContent = 'Completed ✨';
      if (prevBtn) prevBtn.style.display = 'none';
      if (nextBtn) nextBtn.style.display = 'none';
      return;
    }

    if (endScene) endScene.style.display = 'none';
    if (prevBtn) prevBtn.style.display = 'inline-flex';
    if (nextBtn) nextBtn.style.display = 'inline-flex';

    cards.forEach((c, i) => {
      c.style.display = i === index ? 'block' : 'none';
      c.classList.remove('flipped');
    });
    if (counter) counter.textContent = `${index + 1} / ${total}`;
  }

  cards.forEach(card => {
    card.addEventListener('click', () => card.classList.toggle('flipped'));
  });

  const prevBtn = document.getElementById('prev-card');
  const nextBtn = document.getElementById('next-card');

  if (prevBtn) {
    prevBtn.addEventListener('click', () => {
      if (currentIndex > 0) {
        currentIndex = currentIndex - 1;
        showCard(currentIndex);
      }
    });
  }

  if (nextBtn) {
    nextBtn.addEventListener('click', () => {
      if (currentIndex < total) {
        currentIndex = currentIndex + 1;
        showCard(currentIndex);
      }
    });
  }

  const restartBtn = document.getElementById('restart-cards');
  if (restartBtn) {
    restartBtn.addEventListener('click', () => {
      currentIndex = 0;
      showCard(currentIndex);
    });
  }

  if (total > 0) showCard(0);
});
