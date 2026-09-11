const API_BASE = "";
const HISTORY_KEY = "gearoptimizer_history";
const HISTORY_LIMIT = 3;

const SELECT_IDS = ["cpu-select", "gpu-select", "ram-select", "resolution-select"];

let hardwareData = { cpus: [], gpus: [], rams: [], resolutions: [] };

window.addEventListener("load", async () => {
    await loadHardwareOptions();
    renderHistory();
    document.getElementById("analyze-btn").addEventListener("click", runAnalysis);
    document.getElementById("history-clear-btn").addEventListener("click", clearHistory);
});

function escapeHtml(value) {
    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;");
}

function showAlert(message) {
    const box = document.getElementById("alert-box");
    box.textContent = `! ${message}`;
    box.hidden = false;
}

function clearAlert() {
    const box = document.getElementById("alert-box");
    box.hidden = true;
    box.textContent = "";
}

function setFormEnabled(enabled) {
    document.getElementById("analyze-btn").disabled = !enabled;
    SELECT_IDS.forEach(id => { document.getElementById(id).disabled = !enabled; });
    document.getElementById("purpose-select").disabled = !enabled;
}

async function loadHardwareOptions() {
    try {
        const responses = await Promise.all([
            fetch(`${API_BASE}/hardware/cpus`),
            fetch(`${API_BASE}/hardware/gpus`),
            fetch(`${API_BASE}/hardware/rams`),
            fetch(`${API_BASE}/hardware/resolutions`),
        ]);

        const failed = responses.find(r => !r.ok);
        if (failed) throw new Error(`Sunucu ${failed.status} döndü`);

        const [cpus, gpus, rams, resolutions] = await Promise.all(responses.map(r => r.json()));
        hardwareData = { cpus, gpus, rams, resolutions };

        populateSelect("cpu-select", cpus, c => `${c.brand} ${c.model} (${c.cores} Core)`);
        populateSelect("gpu-select", gpus, g => `${g.brand} ${g.model} (${g.vram_gb} GB)`);
        populateSelect("ram-select", rams, r => `${r.capacity_gb}GB - (${r.speed_mhz} MHz)`);
        populateSelect("resolution-select", resolutions, r => r.name);

        clearAlert();
        setFormEnabled(true);
    } catch (err) {
        console.error("Hardware data load failed:", err);
        SELECT_IDS.forEach(id => {
            document.getElementById(id).innerHTML = `<option value="">-YÜKLENEMEDİ-</option>`;
        });
        setFormEnabled(false);
        showAlert("Donanım listesi yüklenemedi. Sunucuya ulaşılamıyor — sayfayı yenilemeyi dene.");
    }
}

function populateSelect(id, items, labelFn) {
    const select = document.getElementById(id);
    select.innerHTML = items
        .map(item => `<option value="${item.id}">${escapeHtml(labelFn(item))}</option>`)
        .join("");
}

async function runAnalysis() {
    const btn = document.getElementById("analyze-btn");

    const payload = {
        cpu_id: parseInt(document.getElementById("cpu-select").value),
        gpu_id: parseInt(document.getElementById("gpu-select").value),
        ram_id: parseInt(document.getElementById("ram-select").value),
        resolution_id: parseInt(document.getElementById("resolution-select").value),
        usage_purpose: document.getElementById("purpose-select").value,
    };

    if (Object.values(payload).some(value => Number.isNaN(value))) {
        showAlert("Analiz için tüm donanım alanlarını seç.");
        return;
    }

    clearAlert();
    btn.textContent = "> ANALYZING... PLEASE WAIT";
    btn.disabled = true;

    try {
        const requestBody = JSON.stringify(payload);
        const [analyzeResponse, adviceResponse] = await Promise.all([
            fetch(`${API_BASE}/optimizer/analyze`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: requestBody,
            }),
            fetch(`${API_BASE}/optimizer/upgrade-advice`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: requestBody,
            }),
        ]);

        if (!analyzeResponse.ok) throw new Error(await readErrorMessage(analyzeResponse));

        const data = await analyzeResponse.json();
        showResult(data);
        saveToHistory(payload, data);

        if (adviceResponse.ok) {
            showUpgradeAdvice(await adviceResponse.json());
        } else {
            console.error("Upgrade advice failed:", adviceResponse.status);
            document.getElementById("upgrade-panel").hidden = true;
        }
    } catch (err) {
        console.error("Analysis error:", err);
        document.getElementById("result").hidden = true;
        document.getElementById("upgrade-panel").hidden = true;
        showAlert(err.message || "Analiz başarısız oldu, tekrar dene.");
    } finally {
        btn.textContent = "> RUN_ANALYSIS [ ENTER ]";
        btn.disabled = false;
    }
}

async function readErrorMessage(response) {
    try {
        const body = await response.json();
        if (typeof body.detail === "string") return body.detail;
        if (Array.isArray(body.detail)) return "Gönderilen değerler geçersiz.";
    } catch (err) {
        console.error("Error body parse failed:", err);
    }
    return `Sunucu hatası (${response.status}). Birazdan tekrar dene.`;
}

function showResult(data) {
    const result = document.getElementById("result");
    const detail = data.detail;

    document.getElementById("score-value").textContent = data.score;
    document.getElementById("score-level").textContent = data.level;
    document.getElementById("advice").textContent = data.advice;
    document.getElementById("bottleneck").textContent = detail.bottleneck;

    renderBreakdown(detail);
    renderResolutionNote(detail);

    result.hidden = false;
    result.scrollIntoView({ behavior: "smooth" });
}

function renderBreakdown(detail) {
    const rows = [
        {
            label: "CPU",
            name: detail.cpu,
            score: detail.cpu_score,
            weight: detail.cpu_weight,
        },
        {
            label: "GPU",
            name: detail.gpu,
            score: detail.gpu_score_adjusted,
            weight: detail.gpu_weight,
        },
        {
            label: "RAM",
            name: detail.ram,
            score: detail.ram_score,
            weight: detail.ram_weight,
        },
    ];

    document.getElementById("breakdown").innerHTML = rows.map(row => {
        const contribution = (row.score * row.weight).toFixed(1);
        const percent = Math.min(row.score, 100);
        return `
            <div class="breakdown-row">
                <div class="breakdown-head">
                    <span class="breakdown-label">${row.label}</span>
                    <span class="breakdown-name">${escapeHtml(row.name)}</span>
                </div>
                <div class="bar"><div class="bar-fill" style="width:${percent}%"></div></div>
                <div class="breakdown-meta">
                    <span>güç ${row.score}/100</span>
                    <span>ağırlık %${Math.round(row.weight * 100)}</span>
                    <span class="breakdown-contribution">katkı ${contribution} puan</span>
                </div>
            </div>
        `;
    }).join("");
}

function renderResolutionNote(detail) {
    const note = document.getElementById("resolution-note");
    const multiplier = detail.demand_multiplier;

    if (multiplier <= 1) {
        note.textContent = `${detail.resolution} referans çözünürlük — GPU skoruna düzeltme uygulanmadı.`;
        return;
    }

    note.textContent =
        `${detail.resolution} çözünürlükte GPU yükü ${multiplier}× artıyor: ` +
        `${detail.gpu_score_raw} olan ham GPU gücü, hesaba ${detail.gpu_score_adjusted} olarak giriyor.`;
}

const COMPONENT_LABELS = { cpu: "CPU", gpu: "GPU", ram: "RAM" };

function showUpgradeAdvice(advice) {
    const panel = document.getElementById("upgrade-panel");
    const bestBox = document.getElementById("upgrade-best");
    const optionsBox = document.getElementById("upgrade-options");

    bestBox.innerHTML = advice.best_pick
        ? `<span class="upgrade-best-label">EN VERİMLİ SEÇİM</span>
           <span class="upgrade-best-text">${COMPONENT_LABELS[advice.best_pick.component]} → ${escapeHtml(advice.best_pick.suggested)}
           (+${advice.best_pick.score_gain} puan)</span>`
        : `<span class="upgrade-best-text">Zaten dengeli bir sistemdesin — tek parça değişimi skoru belirgin artırmıyor.</span>`;

    optionsBox.innerHTML = advice.options.map(option => {
        const isBest = advice.best_pick?.component === option.component;
        const body = option.suggested
            ? `${escapeHtml(option.current)} → ${escapeHtml(option.suggested)}`
            : escapeHtml(option.current);

        return `
            <div class="upgrade-option${isBest ? " upgrade-option-best" : ""}">
                <div class="upgrade-option-head">
                    <span class="upgrade-option-label">${COMPONENT_LABELS[option.component]}</span>
                    ${isBest ? '<span class="upgrade-option-badge">ÖNERİLEN</span>' : ""}
                </div>
                <div class="upgrade-option-body">${body}</div>
                <div class="upgrade-option-meta">
                    <span>+${option.score_gain} puan</span>
                    <span>verimlilik ${option.efficiency}</span>
                </div>
                <div class="upgrade-option-note">${escapeHtml(option.note)}</div>
            </div>
        `;
    }).join("");

    panel.hidden = false;
}

function findLabel(list, id, labelFn) {
    const item = list.find(i => i.id === id);
    return item ? labelFn(item) : "?";
}

function saveToHistory(payload, result) {
    const entry = {
        ...payload,
        cpuLabel: findLabel(hardwareData.cpus, payload.cpu_id, c => `${c.brand} ${c.model}`),
        gpuLabel: findLabel(hardwareData.gpus, payload.gpu_id, g => `${g.brand} ${g.model}`),
        score: result.score,
        level: result.level,
    };

    const history = [entry, ...getHistory()].slice(0, HISTORY_LIMIT);
    localStorage.setItem(HISTORY_KEY, JSON.stringify(history));
    renderHistory();
}

function getHistory() {
    try {
        const stored = JSON.parse(localStorage.getItem(HISTORY_KEY));
        return Array.isArray(stored) ? stored : [];
    } catch (err) {
        console.error("History parse failed:", err);
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
            <div class="history-item-title">${escapeHtml(entry.cpuLabel)}<br>${escapeHtml(entry.gpuLabel)}</div>
            <div class="history-item-meta"><span>${escapeHtml(entry.level)}</span><span>${entry.score}/100</span></div>
        </div>
    `).join("");

    container.querySelectorAll(".history-item").forEach(el => {
        el.addEventListener("click", () => loadFromHistory(parseInt(el.dataset.index)));
    });
}

function loadFromHistory(index) {
    const entry = getHistory()[index];
    if (!entry) return;

    document.getElementById("cpu-select").value = entry.cpu_id;
    document.getElementById("gpu-select").value = entry.gpu_id;
    document.getElementById("ram-select").value = entry.ram_id;
    document.getElementById("resolution-select").value = entry.resolution_id;
    document.getElementById("purpose-select").value = entry.usage_purpose;

    runAnalysis();
}
