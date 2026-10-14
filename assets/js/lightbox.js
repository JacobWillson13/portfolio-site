// Minimal figure lightbox for project cards.
// Any <a class="lightbox" href="image" data-gallery="name" data-description="...">
// opens in a modal; links sharing a data-gallery value page together in
// document order (hidden links included). No dependencies.
(function () {
  "use strict";

  const links = Array.from(document.querySelectorAll("a.lightbox[href]"));
  if (!links.length || typeof HTMLDialogElement === "undefined") return;

  const dialog = document.createElement("dialog");
  dialog.className = "lb";
  dialog.setAttribute("aria-label", "Figure viewer");
  dialog.innerHTML =
    '<figure class="lb-figure">' +
    '<img class="lb-img" alt="">' +
    '<figcaption class="lb-caption"><span class="lb-text"></span><span class="lb-count"></span></figcaption>' +
    "</figure>" +
    '<button type="button" class="lb-btn lb-close" aria-label="Close">&times;</button>' +
    '<button type="button" class="lb-btn lb-prev" aria-label="Previous figure">&#8249;</button>' +
    '<button type="button" class="lb-btn lb-next" aria-label="Next figure">&#8250;</button>';
  document.body.appendChild(dialog);

  const img = dialog.querySelector(".lb-img");
  const text = dialog.querySelector(".lb-text");
  const count = dialog.querySelector(".lb-count");
  const prev = dialog.querySelector(".lb-prev");
  const next = dialog.querySelector(".lb-next");

  let group = [];
  let index = 0;

  function altFor(link) {
    const inner = link.querySelector("img");
    return (inner && inner.alt) || link.dataset.description || "";
  }

  function show(i) {
    index = (i + group.length) % group.length;
    const link = group[index];
    img.src = link.getAttribute("href");
    img.alt = altFor(link);
    text.textContent = link.dataset.description || "";
    const many = group.length > 1;
    count.textContent = many ? index + 1 + " / " + group.length : "";
    prev.hidden = !many;
    next.hidden = !many;
  }

  function open(link) {
    const name = link.dataset.gallery;
    group = name ? links.filter((l) => l.dataset.gallery === name) : [link];
    show(group.indexOf(link));
    dialog.showModal();
  }

  links.forEach((link) => {
    link.addEventListener("click", (event) => {
      if (event.metaKey || event.ctrlKey || event.shiftKey || event.button !== 0) return;
      event.preventDefault();
      open(link);
    });
  });

  dialog.querySelector(".lb-close").addEventListener("click", () => dialog.close());
  prev.addEventListener("click", () => show(index - 1));
  next.addEventListener("click", () => show(index + 1));

  // Click on the backdrop (outside the figure and buttons) closes.
  dialog.addEventListener("click", (event) => {
    if (event.target === dialog) dialog.close();
  });

  dialog.addEventListener("keydown", (event) => {
    if (group.length < 2) return;
    if (event.key === "ArrowLeft") show(index - 1);
    if (event.key === "ArrowRight") show(index + 1);
  });

  dialog.addEventListener("close", () => {
    img.removeAttribute("src");
  });

  // Horizontal swipe on touch screens.
  let startX = null;
  dialog.addEventListener("touchstart", (event) => {
    startX = event.touches[0].clientX;
  }, { passive: true });
  dialog.addEventListener("touchend", (event) => {
    if (startX === null || group.length < 2) return;
    const dx = event.changedTouches[0].clientX - startX;
    if (Math.abs(dx) > 50) show(index + (dx < 0 ? 1 : -1));
    startX = null;
  });
})();
