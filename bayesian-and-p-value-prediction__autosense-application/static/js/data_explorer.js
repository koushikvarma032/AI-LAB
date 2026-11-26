/* Data Explorer JavaScript Controller for AutoSense Nexus */

document.addEventListener('DOMContentLoaded', () => {
    initFaultDistributionChart();
    initSensorMeansChart();
    loadDatasetTable();

    const searchInput = document.getElementById('data-search-input');
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            filterTableRows(e.target.value.toLowerCase());
        });
    }
});

let allRecords = [];

function initFaultDistributionChart() {
    const ctx = document.getElementById('fault-dist-chart');
    if (!ctx || !datasetSummaryData) return;

    const faultCounts = datasetSummaryData.fault_counts || {};
    const labels = Object.keys(faultCounts).map(k => k.replace(/_/g, ' '));
    const dataVals = Object.values(faultCounts);

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Sample Count',
                data: dataVals,
                backgroundColor: 'rgba(6, 182, 212, 0.6)',
                borderColor: '#06b6d4',
                borderWidth: 1,
                borderRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                x: { ticks: { color: '#94a3b8', font: { family: 'JetBrains Mono', size: 10 } }, grid: { color: '#1e293b' } },
                y: { ticks: { color: '#94a3b8', font: { family: 'JetBrains Mono' } }, grid: { color: '#1e293b' } }
            }
        }
    });
}

function initSensorMeansChart() {
    const ctx = document.getElementById('sensor-means-chart');
    if (!ctx || !datasetSummaryData) return;

    const stats = datasetSummaryData.numeric_stats || {};
    const sensors = ['battery_voltage', 'alternator_voltage', 'oil_pressure', 'engine_temperature'];
    const means = sensors.map(s => stats[s] ? stats[s].mean : 0);

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: sensors.map(s => s.replace(/_/g, ' ').toUpperCase()),
            datasets: [{
                label: 'Mean Value Across Dataset',
                data: means,
                borderColor: '#10b981',
                backgroundColor: 'rgba(16, 185, 129, 0.15)',
                fill: true,
                tension: 0.3,
                pointRadius: 6,
                pointBackgroundColor: '#10b981'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                x: { ticks: { color: '#94a3b8', font: { family: 'JetBrains Mono', size: 10 } }, grid: { color: '#1e293b' } },
                y: { ticks: { color: '#94a3b8', font: { family: 'JetBrains Mono' } }, grid: { color: '#1e293b' } }
            }
        }
    });
}

async function loadDatasetTable() {
    try {
        const response = await fetch('/api/dataset-records?limit=100');
        const data = await response.json();
        if (!data.success) return;

        allRecords = data.records;
        renderTableRows(allRecords);
    } catch (err) {
        console.error('Failed to load dataset records:', err);
    }
}

function renderTableRows(records) {
    const tbody = document.getElementById('dataset-table-body');
    if (!tbody) return;

    tbody.innerHTML = '';

    records.forEach(r => {
        const tr = document.createElement('tr');
        tr.className = 'hover:bg-slate-800/40 transition-colors';

        tr.innerHTML = `
            <td class="p-2.5 font-bold text-slate-200">${r.fault.replace(/_/g, ' ')}</td>
            <td class="p-2.5 text-right ${r.battery_voltage < 12.0 ? 'text-rose-400 font-bold' : 'text-slate-300'}">${r.battery_voltage} V</td>
            <td class="p-2.5 text-right ${r.alternator_voltage < 13.2 ? 'text-amber-400 font-bold' : 'text-slate-300'}">${r.alternator_voltage} V</td>
            <td class="p-2.5 text-right text-slate-300">${r.engine_rpm}</td>
            <td class="p-2.5 text-right ${r.engine_temperature > 100.0 ? 'text-rose-400 font-bold' : 'text-slate-300'}">${r.engine_temperature} °C</td>
            <td class="p-2.5 text-right ${r.coolant_temperature > 95.0 ? 'text-rose-400 font-bold' : 'text-slate-300'}">${r.coolant_temperature} °C</td>
            <td class="p-2.5 text-right ${r.oil_pressure < 25.0 ? 'text-rose-400 font-bold' : 'text-slate-300'}">${r.oil_pressure} PSI</td>
            <td class="p-2.5 text-center">${r.slow_cranking ? 'YES' : 'NO'}</td>
            <td class="p-2.5 text-center">${r.hard_starting ? 'YES' : 'NO'}</td>
            <td class="p-2.5 text-center">${r.dim_headlights ? 'YES' : 'NO'}</td>
        `;
        tbody.appendChild(tr);
    });
}

function filterTableRows(query) {
    if (!query) {
        renderTableRows(allRecords);
        return;
    }

    const filtered = allRecords.filter(r => {
        return r.fault.toLowerCase().includes(query) ||
               String(r.battery_voltage).includes(query) ||
               String(r.engine_temperature).includes(query);
    });

    renderTableRows(filtered);
}
