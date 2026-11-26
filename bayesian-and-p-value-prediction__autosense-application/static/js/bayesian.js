/* Bayesian Network Vis.js Graph Controller for AutoSense Nexus */

let networkInstance = null;

document.addEventListener('DOMContentLoaded', () => {
    initBayesianGraph();
});

async function initBayesianGraph() {
    const container = document.getElementById('bayesian-network-graph');
    const loadingEl = document.getElementById('graph-loading');
    if (!container) return;

    try {
        const response = await fetch('/api/bayesian-network');
        const data = await response.json();

        if (loadingEl) loadingEl.classList.add('hidden');
        if (!data.success) return;

        // Build Vis.js Nodes & Edges
        const nodesArray = data.graph.nodes.map(n => {
            let colorObj = { background: '#1e293b', border: '#334155' };
            if (n.type === 'fault') {
                colorObj = { background: '#ef4444', border: '#f87171' };
            } else if (n.type === 'sensor') {
                colorObj = { background: '#06b6d4', border: '#38bdf8' };
            } else if (n.type === 'symptom') {
                colorObj = { background: '#f59e0b', border: '#fbbf24' };
            }

            return {
                id: n.id,
                label: n.label,
                color: colorObj,
                font: { color: '#ffffff', face: 'JetBrains Mono', size: 12 },
                shape: n.type === 'fault' ? 'diamond' : 'box',
                margin: 10,
                shadow: true,
                states: n.states
            };
        });

        const edgesArray = data.graph.edges.map(e => ({
            from: e.from,
            to: e.to,
            arrows: 'to',
            color: { color: '#475569', highlight: '#06b6d4' },
            width: 1.5
        }));

        const visData = {
            nodes: new vis.DataSet(nodesArray),
            edges: new vis.DataSet(edgesArray)
        };

        const options = {
            nodes: {
                borderWidth: 2,
                shadow: true
            },
            edges: {
                smooth: { type: 'cubicBezier', forceDirection: 'vertical' }
            },
            physics: {
                solver: 'forceAtlas2Based',
                forceAtlas2Based: {
                    gravitationalConstant: -50,
                    centralGravity: 0.01,
                    springLength: 100,
                    springConstant: 0.08
                },
                maxVelocity: 50,
                minVelocity: 0.1,
                stabilization: { iterations: 150 }
            },
            interaction: {
                hover: true,
                zoomView: true,
                dragView: true
            }
        };

        networkInstance = new vis.Network(container, visData, options);

        // Click Event listener for node selection
        networkInstance.on('selectNode', (params) => {
            if (params.nodes.length > 0) {
                const nodeId = params.nodes[0];
                inspectNode(nodeId, nodesArray.find(n => n.id === nodeId));
            }
        });

    } catch (err) {
        console.error('Failed to load Bayesian network graph:', err);
        if (loadingEl) loadingEl.innerText = 'Failed to load graph data.';
    }
}

async function inspectNode(nodeId, nodeObj) {
    const emptyEl = document.getElementById('node-inspector-empty');
    const contentEl = document.getElementById('node-inspector-content');

    if (!emptyEl || !contentEl) return;

    emptyEl.classList.add('hidden');
    contentEl.classList.remove('hidden');

    document.getElementById('insp-node-name').innerText = nodeObj.label;
    document.getElementById('insp-node-type').innerText = `Node Key: ${nodeObj.id} | Type: ${nodeObj.shape === 'diamond' ? 'Target Fault' : 'Evidence Variable'}`;

    // Render states
    const statesEl = document.getElementById('insp-node-states');
    statesEl.innerHTML = '';
    (nodeObj.states || []).forEach(st => {
        const badge = document.createElement('span');
        badge.className = 'px-2 py-0.5 rounded bg-slate-800 border border-slate-700 text-cyan-400 font-mono text-[11px]';
        badge.innerText = st;
        statesEl.appendChild(badge);
    });

    // Fetch Tabular CPT
    const cptContainer = document.getElementById('insp-cpt-container');
    cptContainer.innerHTML = '<div class="p-3 text-slate-400">Loading CPT table...</div>';

    try {
        const response = await fetch(`/api/bayesian-cpd/${nodeId}`);
        const data = await response.json();

        if (!data.success) {
            cptContainer.innerHTML = '<div class="p-3 text-slate-400">No CPT available for this node.</div>';
            return;
        }

        renderCPDTable(cptContainer, data.cpd);
    } catch (err) {
        cptContainer.innerHTML = '<div class="p-3 text-rose-400">Failed to load CPT.</div>';
    }
}

function renderCPDTable(container, cpd) {
    const states = cpd.state_names[cpd.variable] || [];
    const values = cpd.values || [];

    let html = '<table class="w-full text-left font-mono text-[11px] border-collapse">';
    html += '<thead><tr class="bg-slate-900 border-b border-slate-800 text-cyan-400"><th class="p-2">State</th><th class="p-2 text-right">Probability</th></tr></thead>';
    html += '<tbody class="divide-y divide-slate-800">';

    states.forEach((st, idx) => {
        let probVal = values[idx];
        if (Array.isArray(probVal)) {
            probVal = probVal[0]; // First slice for visualization
        }
        const pct = (parseFloat(probVal) * 100).toFixed(1);
        html += `<tr>
            <td class="p-2 text-slate-200">${st}</td>
            <td class="p-2 text-right text-emerald-400 font-bold">${pct}%</td>
        </tr>`;
    });

    html += '</tbody></table>';
    container.innerHTML = html;
}
