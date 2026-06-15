(() => {
  function escapeHtml(value) {
    return String(value).replace(
      /[&<>'"]/g,
      (character) => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        "'": "&#39;",
        '"': "&quot;",
      })[character],
    );
  }

  function renderDownloadLinks(target, downloads = {}) {
    const links = [];
    if (downloads.log) links.push(`<a href="${downloads.log}">Download output log</a>`);
    if (downloads.report) links.push(`<a href="${downloads.report}">Download JSON report</a>`);
    target.innerHTML = links.join(" · ");
  }

  function statCard(label, value, help) {
    return `<div class="stat"><small>${label}</small><strong>${value ?? 0}</strong><small>${help || ""}</small></div>`;
  }

  window.UiCommon = {
    escapeHtml,
    renderDownloadLinks,
    statCard,
  };
})();
