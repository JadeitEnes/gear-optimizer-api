const API_BASE = "";
const HISTORY_KEY = "gearoptimizer_history";
const HISTORY_LIMIT = 3;
const THEME_KEY = "gearoptimizer_theme";

const SELECT_IDS = ["cpu-select", "gpu-select", "ram-select", "resolution-select"];

const THEME_LABELS = {
    headerSub: { retro: "// Hardware Performance Analyzer", modern: "Hardware Performance Analyzer" },
    configTitle: { retro: "[ SYSTEM CONFIGURATION ]", modern: "Sistem Yapılandırması" },
    cpuLabel: { retro: "> CPU_SELECT:", modern: "CPU" },
    gpuLabel: { retro: "> GPU_SELECT:", modern: "GPU" },
    ramLabel: { retro: "> RAM_SELECT:", modern: "RAM" },
    resolutionLabel: { retro: "> RESOLUTION:", modern: "Çözünürlük" },
    purposeLabel: { retro: "> USAGE_PURPOSE:", modern: "Kullanım Amacı" },
    analyzeIdle: { retro: "> RUN_ANALYSIS [ ENTER ]", modern: "Analizi Başlat" },
    analyzeBusy: { retro: "> ANALYZING... PLEASE WAIT", modern: "Analiz ediliyor..." },
    resultTitle: { retro: "[ ANALYSIS RESULT ]", modern: "Analiz Sonucu" },
    shareIdle: { retro: "> SONUCU PAYLAŞ", modern: "Sonucu Paylaş" },
    shareBusy: { retro: "> LİNK OLUŞTURULUYOR...", modern: "Link oluşturuluyor..." },
    copyIdle: { retro: "KOPYALA", modern: "Kopyala" },
    copySuccess: { retro: "✓ KOPYALANDI", modern: "✓ Kopyalandı" },
    copyFallback: { retro: "KOPYALA (Ctrl+C)", modern: "Kopyala (Ctrl+C)" },
    upgradeTitle: { retro: "[ UPGRADE ADVISOR ]", modern: "Yükseltme Önerisi" },
    historyTitle: { retro: "[ SON 3 SİSTEM ]", modern: "Son 3 Sistem" },
    historyClear: { retro: "> GEÇMİŞİ TEMİZLE", modern: "Geçmişi Temizle" },
    footer: { retro: "// GEAR OPTIMIZER © 2026 — jadeIT — ALL SYSTEMS OPERATIONAL", modern: "Gear Optimizer © 2026 — jadeIT" },
};

let hardwareData = { cpus: [], gpus: [], rams: [], resolutions: [] };

window.addEventListener("load", async () => {
    applyStaticLabels();
    document.getElementById("theme-toggle").addEventListener("click", toggleTheme);

    await loadHardwareOptions();
    renderHistory();
    document.getElementById("analyze-btn").addEventListener("click", runAnalysis);
    document.getElementById("history-clear-btn").addEventListener("click", clearHistory);
    document.getElementById("share-btn").addEventListener("click", shareResult);
    document.getElementById("share-copy-btn").addEventListener("click", copyShareUrl);

    await loadFromShareLink();
});

function currentTheme() {
    return document.documentElement.dataset.theme === "modern" ? "modern" : "retro";
}

function applyStaticLabels() {
    const theme = currentTheme();

    document.getElementById("header-sub").textContent = THEME_LABELS.headerSub[theme];
    document.getElementById("config-title").textContent = THEME_LABELS.configTitle[theme];
    document.getElementById("cpu-label").textContent = THEME_LABELS.cpuLabel[theme];
    document.getElementById("gpu-label").textContent = THEME_LABELS.gpuLabel[theme];
    document.getElementById("ram-label").textContent = THEME_LABELS.ramLabel[theme];
    document.getElementById("resolution-label").textContent = THEME_LABELS.resolutionLabel[theme];
    document.getElementById("purpose-label").textContent = THEME_LABELS.purposeLabel[theme];
    document.getElementById("result-title").textContent = THEME_LABELS.resultTitle[theme];
    document.getElementById("upgrade-title").textContent = THEME_LABELS.upgradeTitle[theme];
    document.getElementById("history-title").textContent = THEME_LABELS.historyTitle[theme];
    document.getElementById("history-clear-btn").textContent = THEME_LABELS.historyClear[theme];
    document.getElementById("footer-text").textContent = THEME_LABELS.footer[theme];
    document.getElementById("theme-toggle").textContent = theme === "modern" ? "Retro Görünüm" : "Modern Görünüm";

    const analyzeBtn = document.getElementById("analyze-btn");
    if (!analyzeBtn.disabled) analyzeBtn.textContent = THEME_LABELS.analyzeIdle[theme];

    const shareBtn = document.getElementById("share-btn");
    if (!shareBtn.disabled) shareBtn.textContent = THEME_LABELS.shareIdle[theme];

    document.getElementById("share-copy-btn").textContent = THEME_LABELS.copyIdle[theme];

    document.querySelectorAll("#purpose-select option[data-retro]").forEach(option => {
        option.textContent = theme === "modern" ? option.dataset.modern : option.dataset.retro;
    });
}

function toggleTheme() {
    const next = currentTheme() === "modern" ? "retro" : "modern";
    document.documentElement.dataset.theme = next;
    localStorage.setItem(THEME_KEY, next);
    applyStaticLabels();
}

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

function currentGearPayload() {
    return {
        cpu_id: parseInt(document.getElementById("cpu-select").value),
        gpu_id: parseInt(document.getElementById("gpu-select").value),
        ram_id: parseInt(document.getElementById("ram-select").value),
        resolution_id: parseInt(document.getElementById("resolution-select").value),
        usage_purpose: document.getElementById("purpose-select").value,
    };
}

function applyGearToForm(gear) {
    document.getElementById("cpu-select").value = gear.cpu_id;
    document.getElementById("gpu-select").value = gear.gpu_id;
    document.getElementById("ram-select").value = gear.ram_id;
    document.getElementById("resolution-select").value = gear.resolution_id;
    document.getElementById("purpose-select").value = gear.usage_purpose;
}

async function runAnalysis() {
    const btn = document.getElementById("analyze-btn");
    const payload = currentGearPayload();

    if (Object.values(payload).some(value => Number.isNaN(value))) {
        showAlert("Analiz için tüm donanım alanlarını seç.");
        return;
    }

    clearAlert();
    btn.textContent = THEME_LABELS.analyzeBusy[currentTheme()];
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
        document.getElementById("share-row").hidden = true;
        showAlert(err.message || "Analiz başarısız oldu, tekrar dene.");
    } finally {
        btn.textContent = THEME_LABELS.analyzeIdle[currentTheme()];
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

    document.getElementById("share-row").hidden = true;
    result.hidden = false;
    result.scrollIntoView({ behavior: "smooth" });
}

async function shareResult() {
    const btn = document.getElementById("share-btn");
    const payload = currentGearPayload();

    btn.disabled = true;
    btn.textContent = THEME_LABELS.shareBusy[currentTheme()];

    try {
        const response = await fetch(`${API_BASE}/optimizer/share`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload),
        });

        if (!response.ok) throw new Error(await readErrorMessage(response));

        const { slug } = await response.json();
        const url = `${window.location.origin}${window.location.pathname}?share=${slug}`;

        const urlInput = document.getElementById("share-url");
        urlInput.value = url;
        document.getElementById("share-row").hidden = false;
        urlInput.select();

        await copyShareUrl();
    } catch (err) {
        console.error("Share failed:", err);
        showAlert(err.message || "Paylaşım linki oluşturulamadı, tekrar dene.");
    } finally {
        btn.disabled = false;
        btn.textContent = THEME_LABELS.shareIdle[currentTheme()];
    }
}

async function copyShareUrl() {
    const urlInput = document.getElementById("share-url");
    const copyBtn = document.getElementById("share-copy-btn");

    try {
        await navigator.clipboard.writeText(urlInput.value);
        copyBtn.textContent = THEME_LABELS.copySuccess[currentTheme()];
    } catch (err) {
        console.error("Clipboard write failed:", err);
        urlInput.select();
        copyBtn.textContent = THEME_LABELS.copyFallback[currentTheme()];
    }
    setTimeout(() => { copyBtn.textContent = THEME_LABELS.copyIdle[currentTheme()]; }, 2000);
}

async function loadFromShareLink() {
    const slug = new URLSearchParams(window.location.search).get("share");
    if (!slug) return;

    try {
        const response = await fetch(`${API_BASE}/optimizer/share/${encodeURIComponent(slug)}`);
        if (!response.ok) throw new Error(await readErrorMessage(response));

        applyGearToForm(await response.json());
        await runAnalysis();
    } catch (err) {
        console.error("Share link load failed:", err);
        showAlert("Bu paylaşım linki geçersiz veya bulunamadı. Kendi analizini yapabilirsin.");
    }
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

    applyGearToForm(entry);
    runAnalysis();
}
