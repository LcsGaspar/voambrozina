document.addEventListener('DOMContentLoaded', () => {
    const themeToggle = document.getElementById('appearance-toggle');
    const menu = document.getElementById('appearance-menu');
  
    // Alternar visibilidade do menu
    themeToggle.addEventListener('click', () => {
      const isHidden = menu.classList.toggle('hidden');
      themeToggle.setAttribute('aria-expanded', !isHidden);
    });
  
    // Tema
    menu.querySelectorAll('[data-theme]').forEach(button => {
      button.addEventListener('click', () => {
        const theme = button.getAttribute('data-theme');
        if (theme === 'system') {
          const systemTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
          document.documentElement.setAttribute('data-theme', systemTheme);
          localStorage.setItem('theme', 'system');
        } else {
          document.documentElement.setAttribute('data-theme', theme);
          localStorage.setItem('theme', theme);
        }
      });
    });
  
    // Fonte
    menu.querySelectorAll('[data-font]').forEach(button => {
      button.addEventListener('click', () => {
        const font = button.getAttribute('data-font');
        document.documentElement.setAttribute('data-font', font);
        localStorage.setItem('font-size', font);
      });
    });
  
    // Restaurar preferências
    const savedTheme = localStorage.getItem('theme');
    const savedFont = localStorage.getItem('font-size');
  
    if (savedTheme) {
      if (savedTheme === 'system') {
        const systemTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
        document.documentElement.setAttribute('data-theme', systemTheme);
      } else {
        document.documentElement.setAttribute('data-theme', savedTheme);
      }
    }
  
    if (savedFont) {
      document.documentElement.setAttribute('data-font', savedFont);
    }
  });

  