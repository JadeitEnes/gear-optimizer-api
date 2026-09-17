const API_BASE = "";
const HISTORY_KEY = "gearoptimizer_history";
const HISTORY_LIMIT = 3;
const THEME_KEY = "gearoptimizer_theme";

const SELECT_IDS = ["cpu-select", "gpu-select", "ram-select", "resolution-select"];
const SELECT_IDS_B = ["cpu-select-b", "gpu-select-b", "ram-select-b", "resolution-select-b"];

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
    compareToggleShow: { retro: "> KARŞILAŞTIR", modern: "Karşılaştır" },
    compareToggleHide: { retro: "> KARŞILAŞTIRMAYI GİZLE", modern: "Karşılaştırmayı Gizle" },
    compareConfigTitle: { retro: "[ SİSTEM B ]", modern: "Sistem B" },
    compareIdle: { retro: "> ANALİZ ET VE KIYASLA", modern: "Analiz Et ve Kıyasla" },
    compareBusy: { retro: "> ANALİZ EDİLİYOR...", modern: "Analiz ediliyor..." },
    compareResultTitle: { retro: "[ KARŞILAŞTIRMA SONUCU ]", modern: "Karşılaştırma Sonucu" },
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
    document.getElementById("compare-toggle-btn").addEventListener("click", toggleCompare);
    document.getElementById("run-compare-btn").addEventListener("click", runComparison);

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

    document.getElementById("cpu-label-b").textContent = THEME_LABELS.cpuLabel[theme];
    document.getElementById("gpu-label-b").textContent = THEME_LABELS.gpuLabel[theme];
    document.getElementById("ram-label-b").textContent = THEME_LABELS.ramLabel[theme];
    document.getElementById("resolution-label-b").textContent = THEME_LABELS.resolutionLabel[theme];
    document.getElementById("purpose-label-b").textContent = THEME_LABELS.purposeLabel[theme];
    document.getElementById("compare-config-title").textContent = THEME_LABELS.compareConfigTitle[theme];
    document.getElementById("compare-result-title").textContent = THEME_LABELS.compareResultTitle[theme];

    const compareToggleBtn = document.getElementById("compare-toggle-btn");
    const compareConfigHidden = document.getElementById("compare-config-panel").hidden;
    compareToggleBtn.textContent = (compareConfigHidden ? THEME_LABELS.compareToggleShow : THEME_LABELS.compareToggleHide)[theme];

    const runCompareBtn = document.getElementById("run-compare-btn");
    if (!runCompareBtn.disabled) runCompareBtn.textContent = THEME_LABELS.compareIdle[theme];

    document.querySelectorAll("#purpose-select option[data-retro], #purpose-select-b option[data-retro]").forEach(option => {
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
    document.getElementById("compare-toggle-btn").disabled = !enabled;
    document.getElementById("run-compare-btn").disabled = !enabled;
    SELECT_IDS.forEach(id => { document.getElementById(id).disabled = !enabled; });
    SELECT_IDS_B.forEach(id => { document.getElementById(id).disabled = !enabled; });
    document.getElementById("purpose-select").disabled = !enabled;
    document.getElementById("purpose-select-b").disabled = !enabled;
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

        populateSelect("cpu-select-b", cpus, c => `${c.brand} ${c.model} (${c.cores} Core)`);
        populateSelect("gpu-select-b", gpus, g => `${g.brand} ${g.model} (${g.vram_gb} GB)`);
        populateSelect("ram-select-b", rams, r => `${r.capacity_gb}GB - (${r.speed_mhz} MHz)`);
        populateSelect("resolution-select-b", resolutions, r => r.name);

        clearAlert();
        setFormEnabled(true);
    } catch (err) {
        console.error("Hardware data load failed:", err);
        [...SELECT_IDS, ...SELECT_IDS_B].forEach(id => {
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

function gearPayload(suffix) {
    return {
        cpu_id: parseInt(document.getElementById(`cpu-select${suffix}`).value),
        gpu_id: parseInt(document.getElementById(`gpu-select${suffix}`).value),
        ram_id: parseInt(document.getElementById(`ram-select${suffix}`).value),
        resolution_id: parseInt(document.getElementById(`resolution-select${suffix}`).value),
        usage_purpose: document.getElementById(`purpose-select${suffix}`).value,
    };
}

function currentGearPayload() {
    return gearPayload("");
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
        document.getElementById("compare-result-panel").hidden = true;
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
    applyBottleneckStyle(document.getElementById("bottleneck"), detail);

    renderBreakdown(detail);
    renderResolutionNote(detail);

    document.getElementById("share-row").hidden = true;
    document.getElementById("compare-result-panel").hidden = true;
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

function toggleCompare() {
    const panel = document.getElementById("compare-config-panel");
    panel.hidden = !panel.hidden;
    document.documentElement.toggleAttribute("data-compare-open", !panel.hidden);
    document.getElementById("compare-toggle-btn").textContent =
        (panel.hidden ? THEME_LABELS.compareToggleShow : THEME_LABELS.compareToggleHide)[currentTheme()];
}

async function runComparison() {
    const btn = document.getElementById("run-compare-btn");
    const buildA = currentGearPayload();
    const buildB = gearPayload("-b");

    if (Object.values(buildA).some(value => Number.isNaN(value)) || Object.values(buildB).some(value => Number.isNaN(value))) {
        showAlert("Karşılaştırma için her iki sistemin de tüm alanlarını seç.");
        return;
    }

    clearAlert();
    btn.disabled = true;
    btn.textContent = THEME_LABELS.compareBusy[currentTheme()];

    try {
        const response = await fetch(`${API_BASE}/optimizer/compare`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ build_a: buildA, build_b: buildB }),
        });

        if (!response.ok) throw new Error(await readErrorMessage(response));

        showComparisonResult(await response.json());
    } catch (err) {
        console.error("Comparison failed:", err);
        document.getElementById("compare-result-panel").hidden = true;
        showAlert(err.message || "Karşılaştırma başarısız oldu, tekrar dene.");
    } finally {
        btn.disabled = false;
        btn.textContent = THEME_LABELS.compareIdle[currentTheme()];
    }
}

function showComparisonResult(comparison) {
    document.getElementById("compare-explanation").textContent = comparison.explanation;

    renderCompareSide("a", comparison.build_a.result);
    renderCompareSide("b", comparison.build_b.result);

    document.getElementById("compare-table").innerHTML = renderCompareTable(comparison);

    document.getElementById("upgrade-panel").hidden = true;
    document.getElementById("share-row").hidden = true;

    const panel = document.getElementById("compare-result-panel");
    panel.hidden = false;
    panel.scrollIntoView({ behavior: "smooth" });
}

function renderCompareSide(side, result) {
    document.getElementById(`compare-side-${side}-score`).textContent = `${result.score}/100 — ${result.level}`;
    applyBottleneckStyle(document.getElementById(`compare-side-${side}-bottleneck`), result.detail);
    document.getElementById(`compare-side-${side}-breakdown`).innerHTML = buildBreakdownHtml(result.detail);
}

function applyBottleneckStyle(el, detail) {
    el.textContent = detail.bottleneck;
    el.classList.toggle("bottleneck-ok", !detail.has_bottleneck);
}

function renderCompareTable(comparison) {
    const detailA = comparison.build_a.result.detail;
    const detailB = comparison.build_b.result.detail;

    const rows = [
        {
            label: "CPU",
            a: `${detailA.cpu} (${detailA.cpu_score})`,
            b: `${detailB.cpu} (${detailB.cpu_score})`,
            winner: comparison.cpu_winner,
        },
        {
            label: "GPU",
            a: `${detailA.gpu} (${detailA.gpu_score_adjusted})`,
            b: `${detailB.gpu} (${detailB.gpu_score_adjusted})`,
            winner: comparison.gpu_winner,
        },
        {
            label: "RAM",
            a: `${detailA.ram} (${detailA.ram_score})`,
            b: `${detailB.ram} (${detailB.ram_score})`,
            winner: comparison.ram_winner,
        },
    ];

    const rowsHtml = rows.map(row => `
        <div class="compare-row">
            <span class="compare-row-label">${row.label}</span>
            <span class="compare-cell${row.winner === "a" ? " compare-winner" : ""}">${escapeHtml(row.a)}</span>
            <span class="compare-cell${row.winner === "b" ? " compare-winner" : ""}">${escapeHtml(row.b)}</span>
        </div>
    `).join("");

    return `
        <div class="compare-header">
            <span></span>
            <span>Sistem A</span>
            <span>Sistem B</span>
        </div>
        ${rowsHtml}
        <div class="compare-row compare-row-total">
            <span class="compare-row-label">TOPLAM</span>
            <span class="compare-cell${comparison.winner === "a" ? " compare-winner" : ""}">${comparison.build_a.result.score}/100</span>
            <span class="compare-cell${comparison.winner === "b" ? " compare-winner" : ""}">${comparison.build_b.result.score}/100</span>
        </div>
    `;
}

function buildBreakdownHtml(detail) {
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

    return rows.map(row => {
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

function renderBreakdown(detail) {
    document.getElementById("breakdown").innerHTML = buildBreakdownHtml(detail);
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

function isSameBuild(a, b) {
    return a.cpu_id === b.cpu_id
        && a.gpu_id === b.gpu_id
        && a.ram_id === b.ram_id
        && a.resolution_id === b.resolution_id
        && a.usage_purpose === b.usage_purpose;
}

function saveToHistory(payload, result) {
    const entry = {
        ...payload,
        cpuLabel: findLabel(hardwareData.cpus, payload.cpu_id, c => `${c.brand} ${c.model}`),
        gpuLabel: findLabel(hardwareData.gpus, payload.gpu_id, g => `${g.brand} ${g.model}`),
        score: result.score,
        level: result.level,
    };

    const remaining = getHistory().filter(existing => !isSameBuild(existing, payload));
    const history = [entry, ...remaining].slice(0, HISTORY_LIMIT);
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
