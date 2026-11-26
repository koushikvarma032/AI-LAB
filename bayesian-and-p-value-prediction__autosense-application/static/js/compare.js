/* Repair Comparison JavaScript Controller for AutoSense Nexus */

document.addEventListener('DOMContentLoaded', () => {
    const btn = document.getElementById('run-compare-btn');
    if (btn) {
        btn.addEventListener('click', runComparison);
    }
});

async function runComparison() {
    const getVal = (prefix, id, isBool) => {
        const el = document.getElementById(`${prefix}-${id}`);
        if (!el) return isBool ? 0 : 0;
        return isBool ? (el.checked ? 1 : 0) : parseFloat(el.value);
    };

    const beforeData = {
        battery_voltage: getVal('b', 'battery_voltage'),
        alternator_voltage: getVal('b', 'alternator_voltage'),
        engine_rpm: getVal('b', 'engine_rpm'),
        engine_temperature: getVal('b', 'engine_temperature'),
        coolant_temperature: getVal('b', 'coolant_temperature'),
        oil_pressure: getVal('b', 'oil_pressure'),
        slow_cranking: getVal('b', 'slow_cranking', true),
        hard_starting: getVal('b', 'hard_starting', true),
        dim_headlights: getVal('b', 'dim_headlights', true),
        engine_noise: 0,
        overheating_indicator: 0
    };

    const afterData = {
        battery_voltage: getVal('a', 'battery_voltage'),
        alternator_voltage: getVal('a', 'alternator_voltage'),
        engine_rpm: getVal('a', 'engine_rpm'),
        engine_temperature: getVal('a', 'engine_temperature'),
        coolant_temperature: getVal('a', 'coolant_temperature'),
        oil_pressure: getVal('a', 'oil_pressure'),
        slow_cranking: getVal('a', 'slow_cranking', true),
        hard_starting: getVal('a', 'hard_starting', true),
        dim_headlights: getVal('a', 'dim_headlights', true),
        engine_noise: 0,
        overheating_indicator: 0
    };

    try {
        const response = await fetch('/api/compare', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ before: beforeData, after: afterData })
        });

        const data = await response.json();
        if (!data.success) {
            alert('Comparison Error: ' + data.error);
            return;
        }

        renderComparisonResults(data);
    } catch (err) {
        alert('Failed to execute comparative analysis: ' + err);
    }
}

function renderComparisonResults(data) {
    const container = document.getElementById('compare-results-container');
    const listEl = document.getElementById('compare-shifts-list');
    if (!container || !listEl) return;

    container.classList.remove('hidden');
    listEl.innerHTML = '';

    data.shifts.forEach(item => {
        const isReduction = item.shift < 0;
        const colorClass = isReduction ? 'text-emerald-400' : (item.shift > 0 ? 'text-rose-400' : 'text-slate-400');
        const icon = isReduction ? 'fa-circle-arrow-down text-emerald-400' : (item.shift > 0 ? 'fa-circle-arrow-up text-rose-400' : 'fa-minus text-slate-500');

        const card = document.createElement('div');
        card.className = 'p-4 rounded-xl bg-slate-900 border border-slate-800 flex items-center justify-between';

        card.innerHTML = `
            <div class="space-y-1">
                <div class="font-bold text-slate-200 text-sm">${item.label}</div>
                <div class="text-[11px] text-slate-400 flex items-center gap-4">
                    <span>Before Repair: <strong class="text-rose-400">${item.before_prob}%</strong></span>
                    <span>&rarr;</span>
                    <span>After Repair: <strong class="text-emerald-400">${item.after_prob}%</strong></span>
                </div>
            </div>

            <div class="flex items-center gap-2 font-bold text-sm ${colorClass}">
                <i class="fa-solid ${icon}"></i>
                <span>${item.shift > 0 ? '+' : ''}${item.shift}%</span>
            </div>
        `;
        listEl.appendChild(card);
    });

    container.scrollIntoView({ behavior: 'smooth' });
}
