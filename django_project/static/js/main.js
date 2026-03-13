document.addEventListener('DOMContentLoaded', () => {
  const root = document.documentElement;
  const spotlight = document.querySelector('[data-spotlight]');
  const revealTargets = document.querySelectorAll('[data-reveal]');
  const counters = document.querySelectorAll('[data-count-to]');

  if (spotlight) {
    window.addEventListener('pointermove', (event) => {
      const x = (event.clientX / window.innerWidth) * 100;
      const y = (event.clientY / window.innerHeight) * 100;
      root.style.setProperty('--pointer-x', `${x}%`);
      root.style.setProperty('--pointer-y', `${y}%`);
    });
  }

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.16 }
  );

  revealTargets.forEach((target) => observer.observe(target));

  const animateCounter = (element) => {
    const targetValue = Number(element.dataset.countTo || '0');
    const duration = 1400;
    const start = performance.now();

    const step = (timestamp) => {
      const progress = Math.min((timestamp - start) / duration, 1);
      const current = Math.round(progress * targetValue);
      element.textContent = current.toLocaleString();
      if (progress < 1) {
        window.requestAnimationFrame(step);
      }
    };

    window.requestAnimationFrame(step);
  };

  const counterObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          animateCounter(entry.target);
          counterObserver.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.45 }
  );

  counters.forEach((counter) => counterObserver.observe(counter));
});
