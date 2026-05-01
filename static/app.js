const API_BASE = "";

window.addEventListener("load", () => {
    loadHardwareOptions();
    document.getElementById("analyze-btn").addEventListener("click",runAnalysis);
});

async function loadHardwareOptions() {
    try{
        const [cpus, gpus, rams, resolutions] = await Promise.all([
            fetch(`${API_BASE}/hardware/cpus`).then (r => r.json()),
            fetch(`${API_BASE}/hardware/gpus`).then (r => r.json()),
            fetch(`${API_BASE}/hardware/rams`).then (r => r.json()),
            fetch(`${API_BASE}/hardware/resolutions`).then (r => r.json()),
        ]);

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