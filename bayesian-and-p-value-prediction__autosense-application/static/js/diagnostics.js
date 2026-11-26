/* Live Diagnostics JavaScript Controller for AutoSense Nexus */

let latestDiagnosisPayload = null;

document.addEventListener('DOMContentLoaded', () => {
    setupSliderListeners();
    setupFormSubmission();
    setupResetDefaults();
    setupPDFDownload();
});

function setupSliderListeners() {
    const sliders = [
        { id: 'battery_voltage', displayId: 'bat-val-display', unit: 'V', format: val => `${parseFloat(val).toFixed(1)} V` },
        { id: 'alternator_voltage', displayId: 'alt-val-display', unit: 'V', format: val => `${parseFloat(val).toFixed(1)} V` },
        { id: 'engine_rpm', displayId: 'rpm-val-display', unit: 'RPM', format: val => `${parseInt(val)} RPM` },
        { id: 'engine_temperature', displayId: 'engtemp-val-display', unit: '°C', format: val => `${parseFloat(val).toFixed(1)} °C` },
        { id: 'coolant_temperature', displayId: 'coolant-val-display', unit: '°C', format: val => `${parseFloat(val).toFixed(1)} °C` },
        { id: 'oil_pressure', displayId: 'oil-val-display', unit: 'PSI', format: val => `${parseFloat(val).toFixed(1)} PSI` }
    ];

    sliders.forEach(s => {
        const sliderEl = document.getElementById(s.id);
        const displayEl = document.getElementById(s.displayId);
        if (sliderEl && displayEl) {
            sliderEl.addEventListener('input', (e) => {
                displayEl.innerText = s.format(e.target.value);
            });
        }
    });
}

function setupResetDefaults() {
    const btn = document.getElementById('reset-form-btn');
    if (btn) {
        btn.addEventListener('click', () => {
            document.getElementById('battery_voltage').value = 10.7;
            document.getElementById('bat-val-display').innerText = '10.7 V';

            document.getElementById('alternator_voltage').value = 11.2;
            document.getElementById('alt-val-display').innerText = '11.2 V';

            document.getElementById('engine_rpm').value = 720;
            document.getElementById('rpm-val-display').innerText = '720 RPM';

            document.getElementById('engine_temperature').value = 91.0;
            document.getElementById('engtemp-val-display').innerText = '91.0 °C';

            document.getElementById('coolant_temperature').value = 92.0;
            document.getElementById('coolant-val-display').innerText = '92.0 °C';

            document.getElementById('oil_pressure').value = 29.0;
            document.getElementById('oil-val-display').innerText = '29.0 PSI';

            document.getElementById('slow_cranking').checked = true;
            document.getElementById('hard_starting').checked = true;
            document.getElementById('dim_headlights').checked = true;
            document.getElementById('engine_noise').checked = false;
            document.getElementById('overheating_indicator').checked = false;

            document.getElementById('diagnostic-results').classList.add('hidden');
        });
    }
}

function setupFormSubmission() {
    const form = document.getElementById('diagnostic-form');
    if (!form) return;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const payload = {
            battery_voltage: parseFloat(document.getElementById('battery_voltage').value),
            alternator_voltage: parseFloat(document.getElementById('alternator_voltage').value),
            engine_rpm: parseInt(document.getElementById('engine_rpm').value),
            engine_temperature: parseFloat(document.getElementById('engine_temperature').value),
            coolant_temperature: parseFloat(document.getElementById('coolant_temperature').value),
            oil_pressure: parseFloat(document.getElementById('oil_pressure').value),
            slow_cranking: document.getElementById('slow_cranking').checked ? 1 : 0,
            hard_starting: document.getElementById('hard_starting').checked ? 1 : 0,
            dim_headlights: document.getElementById('dim_headlights').checked ? 1 : 0,
            engine_noise: document.getElementById('engine_noise').checked ? 1 : 0,
            overheating_indicator: document.getElementById('overheating_indicator').checked ? 1 : 0
        };

        latestDiagnosisPayload = payload;

        // Hide old results and show multi-step animated loader
        document.getElementById('diagnostic-results').classList.add('hidden');
        const loader = document.getElementById('diagnostic-loading');
        loader.classList.remove('hidden');

        // Play 5-step animation
        await runPipelineAnimation();

        try {
            const response = await fetch('/api/diagnose', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            const data = await response.json();
            loader.classList.add('hidden');

            if (!data.success) {
                alert('Diagnostic Error: ' + data.error);
                return;
            }

            renderDiagnosticResults(data);

        } catch (err) {
            loader.classList.add('hidden');
            alert('Failed to connect to diagnostic server: ' + err);
        }
    });
}

async function runPipelineAnimation() {
    const steps = [
        { title: 'VALIDATING SENSOR DATA', desc: 'Sanitizing values and binning continuous variables...', elementId: 'pipe-step-1' },
        { title: 'RUNNING STATISTICAL ANALYSIS', desc: 'Executing SciPy t-tests, Mann-Whitney U, and Chi-Square tests...', elementId: 'pipe-step-2' },
        { title: 'EVALUATING SIGNIFICANT VARIABLES', desc: 'Filtering variables with p-value < 0.05 threshold...', elementId: 'pipe-step-3' },
        { title: 'PROPAGATING BAYESIAN EVIDENCE', desc: 'Querying pgmpy VariableElimination engine...', elementId: 'pipe-step-4' },
        { title: 'CALCULATING POSTERIOR PROBABILITIES', desc: 'Sorting hypotheses and computing evidence map...', elementId: 'pipe-step-5' }
    ];

    // Reset step styles
    for (let i = 1; i <= 5; i++) {
        const el = document.getElementById(`pipe-step-${i}`);
        el.className = 'pipeline-step p-2.5 rounded-lg bg-slate-900 border border-slate-800 text-slate-500 flex items-center justify-between';
        el.querySelector('.step-icon').className = 'step-icon fa-solid fa-clock';
    }

    for (let i = 0; i < steps.length; i++) {
        const s = steps[i];
        document.getElementById('step-title').innerText = s.title;
        document.getElementById('step-desc').innerText = s.desc;

        const el = document.getElementById(s.elementId);
        el.className = 'pipeline-step active p-2.5 rounded-lg border flex items-center justify-between';
        el.querySelector('.step-icon').className = 'step-icon fa-solid fa-circle-notch animate-spin text-cyan-400';

        await new Promise(r => setTimeout(r, 280));

        el.className = 'pipeline-step completed p-2.5 rounded-lg border flex items-center justify-between';
        el.querySelector('.step-icon').className = 'step-icon fa-solid fa-circle-check text-emerald-400';
    }
}

function renderDiagnosticResults(data) {
    const resultsContainer = document.getElementById('diagnostic-results');
    resultsContainer.classList.remove('hidden');

    // 1. Top Fault Title & Probability
    document.getElementById('res-top-fault-title').innerText = data.top_fault_label;
    document.getElementById('res-top-prob').innerText = `${data.top_probability}%`;

    // Draw Radial Gauge
    drawRadialGauge(data.top_probability_raw);

    // 2. Render Alternative Hypotheses
    const altListEl = document.getElementById('res-alt-hypotheses-list');
    altListEl.innerHTML = '';

    const sortedFaults = Object.entries(data.posteriors).sort((a, b) => b[1] - a[1]);

    sortedFaults.forEach(([fault, prob]) => {
        const label = fault.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
        const isTop = fault === data.top_fault;

        const itemEl = document.createElement('div');
        itemEl.className = `p-3 rounded-xl border flex items-center justify-between ${isTop ? 'bg-cyan-500/10 border-cyan-500/40 text-cyan-300' : 'bg-slate-900/60 border-slate-800 text-slate-300'}`;

        itemEl.innerHTML = `
            <div class="flex items-center gap-3">
                <span class="w-6 h-6 rounded-full ${isTop ? 'bg-cyan-500 text-black' : 'bg-slate-800 text-slate-400'} flex items-center justify-center font-bold text-[10px]">
                    ${isTop ? '★' : '•'}
                </span>
                <span class="font-semibold">${label}</span>
            </div>
            <div class="flex items-center gap-3">
                <div class="w-24 bg-slate-800 h-2 rounded-full overflow-hidden">
                    <div class="h-full ${isTop ? 'bg-cyan-400' : 'bg-slate-600'}" style="width: ${prob}%"></div>
                </div>
                <span class="font-bold w-12 text-right ${isTop ? 'text-cyan-400' : 'text-slate-400'}">${prob}%</span>
            </div>
        `;
        altListEl.appendChild(itemEl);
    });

    // 3. Render Explainable AI Section
    const factsEl = document.getElementById('res-obs-facts');
    factsEl.innerHTML = '';
    data.explanations.observational_facts.forEach(fact => {
        const li = document.createElement('li');
        li.innerText = fact;
        factsEl.appendChild(li);
    });

    document.getElementById('res-stat-rationale').innerText = data.explanations.statistical_rationale;
    document.getElementById('res-bayes-rationale').innerText = data.explanations.bayesian_rationale;

    // 4. Render Evidence Map
    const evMapEl = document.getElementById('res-evidence-map-bars');
    evMapEl.innerHTML = '';

    data.evidence_map.forEach(item => {
        const barEl = document.createElement('div');
        barEl.className = 'space-y-1';
        barEl.innerHTML = `
            <div class="flex justify-between text-[11px] font-mono">
                <span class="text-slate-300">${item.label} (${item.state})</span>
                <span class="text-cyan-400 font-bold">${item.importance_percent}%</span>
            </div>
            <div class="w-full bg-slate-800 h-2.5 rounded-full overflow-hidden border border-slate-700">
                <div class="h-full bg-gradient-to-r from-cyan-500 to-blue-500 rounded-full" style="width: ${item.importance_percent}%"></div>
            </div>
        `;
        evMapEl.appendChild(barEl);
    });

    // Scroll smoothly to results
    resultsContainer.scrollIntoView({ behavior: 'smooth' });
}

function drawRadialGauge(probability) {
    const canvas = document.getElementById('top-prob-gauge');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;
    const centerX = width / 2;
    const centerY = height / 2;
    const radius = 80;

    ctx.clearRect(0, 0, width, height);

    // Background track
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius, 0.75 * Math.PI, 2.25 * Math.PI, false);
    ctx.lineWidth = 12;
    ctx.strokeStyle = '#1e293b';
    ctx.stroke();

    // Foreground probability arc
    const endAngle = 0.75 * Math.PI + (probability * (1.5 * Math.PI));
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius, 0.75 * Math.PI, endAngle, false);
    ctx.lineWidth = 12;
    ctx.lineCap = 'round';

    const grad = ctx.createLinearGradient(0, 0, width, height);
    grad.addColorStop(0, '#06b6d4');
    grad.addColorStop(1, '#10b981');
    ctx.strokeStyle = grad;
    ctx.stroke();
}

function setupPDFDownload() {
    const btn = document.getElementById('download-pdf-btn');
    if (!btn) return;

    btn.addEventListener('click', async () => {
        if (!latestDiagnosisPayload) {
            alert('Please run a diagnostic first.');
            return;
        }

        try {
            const response = await fetch('/api/generate-report', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(latestDiagnosisPayload)
            });

            if (!response.ok) {
                alert('Error generating PDF report.');
                return;
            }

            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'AutoSense_Nexus_Diagnostic_Report.pdf';
            document.body.appendChild(a);
            a.click();
            a.remove();
        } catch (err) {
            alert('Failed to download PDF report: ' + err);
        }
    });
}
