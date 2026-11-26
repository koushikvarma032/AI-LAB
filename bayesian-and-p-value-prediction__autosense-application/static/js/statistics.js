/* Statistical Lab JavaScript Controller for AutoSense Nexus */

document.addEventListener('DOMContentLoaded', () => {
    const selectEl = document.getElementById('fault-filter-select');
    if (selectEl) {
        selectEl.addEventListener('change', async (e) => {
            const targetFault = e.target.value;
            
            try {
                const response = await fetch('/api/statistical-analysis', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ target_fault: targetFault })
                });

                const data = await response.json();
                if (!data.success) return;

                renderStatsTable(data.results);
            } catch (err) {
                console.error('Error fetching statistical analysis:', err);
            }
        });
    }
});

function renderStatsTable(results) {
    const tbody = document.getElementById('stats-table-body');
    const badge = document.getElementById('test-count-badge');
    if (!tbody) return;

    if (badge) badge.innerText = `Showing ${results.length} Variable Tests`;
    tbody.innerHTML = '';

    results.forEach(r => {
        const tr = document.createElement('tr');
        tr.className = 'hover:bg-slate-800/40 transition-colors';

        tr.innerHTML = `
            <td class="p-3 font-semibold text-slate-200">${r.variable_label}</td>
            <td class="p-3 text-slate-400">${r.target_fault.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}</td>
            <td class="p-3 text-slate-300">${r.test_type}</td>
            <td class="p-3 text-right font-bold text-slate-200">${r.statistic}</td>
            <td class="p-3 text-right font-bold ${r.is_significant ? 'text-emerald-400' : 'text-slate-400'}">
                ${r.p_value_formatted}
            </td>
            <td class="p-3 text-center">
                ${r.is_significant 
                    ? '<span class="px-2.5 py-1 rounded-full bg-emerald-500/20 text-emerald-400 border border-emerald-500/40 font-bold text-[10px]">SIGNIFICANT (p < 0.05)</span>'
                    : '<span class="px-2.5 py-1 rounded-full bg-slate-800 text-slate-400 border border-slate-700 font-bold text-[10px]">NOT SIGNIFICANT</span>'}
            </td>
        `;
        tbody.appendChild(tr);
    });
}
