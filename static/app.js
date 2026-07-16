const API_BASE = "";
const HISTORY_KEY = "gearoptimizer_history";
const HISTORY_LIMIT = 3;

let hardwareData = { cpus: [], gpus: [], rams: [], resolutions: [] };

window.addEventListener("load", async () => {
    await loadHardwareOptions();
    renderHistory();
    document.getElementById("analyze-btn").addEventListener("click", runAnalysis);
    document.getElementById("history-clear-btn").addEventListener("click", clearHistory);
});

async function loadHardwareOptions() {
    try{
        const [cpus, gpus, rams, resolutions] = await Promise.all([
            fetch(`${API_BASE}/hardware/cpus`).then (r => r.json()),
            fetch(`${API_BASE}/hardware/gpus`).then (r => r.json()),
            fetch(`${API_BASE}/hardware/rams`).then (r => r.json()),
            fetch(`${API_BASE}/hardware/resolutions`).then (r => r.json()),
        ]);

        hardwareData = { cpus, gpus, rams, resolutions };

        populateSelect("cpu-select", cpus, c => `${c.brand} ${c.model} (${c.cores} Core)`);
        populateSelect("gpu-select", gpus, g => `${g.brand} ${g.model} (${g.vram_gb} GB)`);
        populateSelect("ram-select", rams, r => `${r.capacity_gb}GB - (${r.speed_mhz} MHz)`);
        populateSelect("resolution-select", resolutions, r => r.name);
    } catch (err) {
        console.error ("Hardware data load failed:", err );
    }
}

function populateSelect(id, items, labelFn) {
    const select = document.getElementById(id);
    select.innerHTML = items.map(item =>
     `<option value="${item.id}">${labelFn(item)}</option>`
    ).join("");
}

async function runAnalysis() {
    const btn = document.getElementById("analyze-btn");
    btn.textContent = "> ANALYZING... PLEASE WAIT";
    btn.disabled = true;


    const payload = {
    cpu_id: parseInt(document.getElementById("cpu-select").value),
    gpu_id: parseInt(document.getElementById("gpu-select").value),
    ram_id: parseInt(document.getElementById("ram-select").value),
    resolution_id: parseInt(document.getElementById("resolution-select").value),
    usage_purpose: document.getElementById("purpose-select").value,
    };


    try {
    const response = await fetch(`${API_BASE}/optimizer/analyze`,{
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(payload),
    });

    if (!response.ok) throw new Error ("Analysis failed");

   const data = await response.json();
    showResult(data);
    saveToHistory(payload, data);
  } catch (err) {
    console.error("Analysis error:", err);
  } finally {
    btn.textContent = "> RUN_ANALYSIS [ ENTER ]";
    btn.disabled = false;
  }
}

function showResult(data) {
  const result = document.getElementById("result");
  result.style.display = "block";

  document.getElementById("score-value").textContent = data.score;
  document.getElementById("score-level").textContent = data.level;
  document.getElementById("advice").textContent = data.advice;

  const detail = document.getElementById("detail-grid");
  detail.innerHTML = Object.entries(data.detail).map(([key, value]) =>
    `<p><span style="color:#4a7a4a">${key.toUpperCase()}:</span> <span>${value}</span></p>`
  ).join("");

  result.scrollIntoView({ behavior: "smooth" });
}

function findLabel(list, id, labelFn) {
    const item = list.find(i => i.id === id);
    return item ? labelFn(item) : "?";
}

function saveToHistory(payload, result) {
    const cpuLabel = findLabel(hardwareData.cpus, payload.cpu_id, c => `${c.brand} ${c.model}`);
    const gpuLabel = findLabel(hardwareData.gpus, payload.gpu_id, g => `${g.brand} ${g.model}`);

    const entry = {
        ...payload,
        cpuLabel,
        gpuLabel,
        score: result.score,
        level: result.level,
    };

    let history = getHistory();
    history.unshift(entry);
    history = history.slice(0, HISTORY_LIMIT);
    localStorage.setItem(HISTORY_KEY, JSON.stringify(history));
    renderHistory();
}

function getHistory() {
    try {
        return JSON.parse(localStorage.getItem(HISTORY_KEY)) || [];
    } catch (err) {
        return [];
    }
}

function clearHistory() {
    localStorage.removeItem(HISTORY_KEY);
    renderHistory();
}

function renderHistory() {
    const container = document.getElementById("history-list");
    const history = getHistory();

    if (history.length === 0) {
        container.innerHTML = `<p class="history-empty">Henüz analiz yapılmadı.</p>`;
        return;
    }

    container.innerHTML = history.map((entry, index) => `
        <div class="history-item" data-index="${index}">
            <div class="history-item-title">${entry.cpuLabel}<br>${entry.gpuLabel}</div>
            <div class="history-item-meta"><span>${entry.level}</span><span>${entry.score}/100</span></div>
        </div>
    `).join("");

    container.querySelectorAll(".history-item").forEach(el => {
        el.addEventListener("click", () => loadFromHistory(parseInt(el.dataset.index)));
    });
}

function loadFromHistory(index) {
    const history = getHistory();
    const entry = history[index];
    if (!entry) return;

    document.getElementById("cpu-select").value = entry.cpu_id;
    document.getElementById("gpu-select").value = entry.gpu_id;
    document.getElementById("ram-select").value = entry.ram_id;
    document.getElementById("resolution-select").value = entry.resolution_id;
    document.getElementById("purpose-select").value = entry.usage_purpose;

    runAnalysis();
}
