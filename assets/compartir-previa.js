(() => {
  const canonical = document.querySelector('link[rel="canonical"]')?.href || location.href;
  const status = document.querySelector('[data-estado-compartir]');
  const shareButton = document.querySelector('[data-compartir-previa]');
  const copyButton = document.querySelector('[data-copiar-previa]');
  const announce = message => {
    if (status) status.textContent = message;
  };
  async function copyLink() {
    try {
      await navigator.clipboard.writeText(canonical);
      announce('Enlace copiado.');
    } catch {
      const field = document.createElement('textarea');
      field.value = canonical;
      field.setAttribute('readonly', '');
      field.style.position = 'fixed';
      field.style.opacity = '0';
      document.body.append(field);
      field.select();
      const copied = document.execCommand('copy');
      field.remove();
      announce(copied ? 'Enlace copiado.' : 'Copia el enlace desde la barra del navegador.');
    }
  }
  copyButton?.addEventListener('click', copyLink);
  shareButton?.addEventListener('click', async () => {
    if (navigator.share) {
      try {
        await navigator.share({ title: document.title, url: canonical });
        announce('Enlace compartido.');
      } catch (error) {
        if (error.name !== 'AbortError') announce('No se pudo abrir el menú de compartir.');
      }
    } else {
      await copyLink();
    }
  });
})();
