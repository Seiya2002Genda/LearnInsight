(() => {
  const uptimeEl = document.getElementById("uptime");
  const activeUsersEl = document.getElementById("activeUsers");
  const saveBtn = document.getElementById("savePermBtn");
  const msg = document.getElementById("systemMsg");

  let seconds = 0;

  function pad(n) {
    return String(n).padStart(2, "0");
  }

  setInterval(() => {
    seconds += 1;
    const h = Math.floor(seconds / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    const s = seconds % 60;
    if (uptimeEl) uptimeEl.textContent = `${pad(h)}:${pad(m)}:${pad(s)}`;
    if (activeUsersEl) activeUsersEl.textContent = String(1 + (seconds % 7));
  }, 1000);

  if (saveBtn && msg) {
    saveBtn.addEventListener("click", () => {
      msg.textContent = "Saved (Demo). Backend integration pending.";
    });
  }
})();