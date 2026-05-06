/* 
   ==========================================================================
    LOGIQUE DU SITE
    Nous avons regroupé ici tout ce qui concerne l'interactivité pour que 
    le projet soit plus facile à lire et à modifier plus tard.
   ========================================================================== 
*/

document.addEventListener('DOMContentLoaded', () => {
    console.log("Dashboard prêt.");
    // On lance le rendu des stats une fois que tout le reste est chargé
    initDashboardChart();
});

function initDashboardChart() {
    const chartEl = document.getElementById('chart');
    const labelsEl = document.getElementById('chart-labels');
    
    if (!chartEl) return;

    // Nous avons mis des données en dur pour l'instant pour tester le rendu visuel
    const days = ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim'];
    const rain = [3, 0, 8, 12, 6, 2, 7]; 
    const temp = [16, 19, 21, 14, 13, 17, 18]; 
    
    // On récupère les valeurs max pour que nos barres restent toujours dans le cadre du graphique
    const maxRain = Math.max(...rain);
    const maxTemp = Math.max(...temp);

    let chartHTML = '';
    days.forEach((day, i) => {
        // Nous générons le HTML ici directement pour éviter de manipuler le DOM à chaque fois
        // On fait un produit en croix simple pour que la barre la plus haute fasse 140px
        chartHTML += `
            <div class="bar-group" style="flex: 1; display: flex; align-items: flex-end; justify-content: center; gap: 4px;" title="${day}: ${rain[i]}mm, ${temp[i]}°C">
                <div class="bar rain" style="height:${(rain[i] / maxRain) * 140}px; background: linear-gradient(to top, #3b82f6, #60a5fa); width: 10px; border-radius: 5px;" title="${rain[i]}mm"></div>
                <div class="bar temp" style="height:${(temp[i] / maxTemp) * 140}px; background: linear-gradient(to top, #f59e0b, #fbbf24); width: 10px; border-radius: 5px;" title="${temp[i]}°C"></div>
            </div>
        `;
    });

    chartEl.innerHTML = chartHTML;
    
    if (labelsEl) {
        // On génère tous les labels d'un coup avec map et join pour avoir un code plus court
        labelsEl.innerHTML = days.map(d => `<span style="flex:1; text-align:center; font-size:11px; font-weight: 700; color:#94a3b8;">${d}</span>`).join('');
    }
}

// Nous avons mis tous les filtres ici pour que l'utilisateur puisse trier ses données rapidement
// Ça nous permet de cacher des lignes sans avoir à recharger toute la page.
function filterAlerts(level, btn) {
    document.querySelectorAll('.filter-tab').forEach(t => t.classList.remove('active'));
    btn.classList.add('active');
    document.querySelectorAll('.alert-card').forEach(card => {
        if (level === 'all' || card.dataset.level === level) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

function openModal() { document.getElementById('modalOverlay').classList.add('open'); }
function closeModal() { document.getElementById('modalOverlay').classList.remove('open'); }
function closeModalOutside(e) { if (e.target === document.getElementById('modalOverlay')) closeModal(); }

function filterParcelles() {
    const search = document.getElementById('searchInput').value.toLowerCase();
    const culture = document.getElementById('cultureFilter').value;
    const risk = document.getElementById('riskFilter').value;
    document.querySelectorAll('.parcelle-card').forEach(card => {
        const text = card.textContent.toLowerCase();
        const matchSearch = !search || text.includes(search);
        const matchCulture = !culture || (card.dataset.culture || '').includes(culture);
        const matchRisk = !risk || card.dataset.risk === risk;
        // On vérifie les 3 conditions en même temps. Si tout est vrai, on affiche la carte.
        // L'opérateur ternaire (condition ? vrai : faux) nous évite un gros bloc if/else.
        card.style.display = (matchSearch && matchCulture && matchRisk) ? 'block' : 'none';
    });
}

let mapScale = 1;
function zoom(factor) {
    const svg = document.getElementById('mapSvg');
    if (!svg) return;
    mapScale *= factor;
    // On borne le zoom entre 0.5 et 3 pour éviter que l'utilisateur ne perde la carte du regard
    mapScale = Math.max(0.5, Math.min(3, mapScale));
    svg.style.transform = `scale(${mapScale})`;
    svg.style.transformOrigin = 'center';
}
function selectParcelleMap(id) {
    const poly = document.getElementById(id);
    if (!poly) return;
    document.querySelectorAll('.parcelle-poly').forEach(p => {
        p.style.fillOpacity = (p.id === id) ? '0.9' : '0.5';
        p.style.strokeWidth = (p.id === id) ? '3' : '1';
    });
    const tt = document.getElementById('tooltip');
    if (tt) {
        document.getElementById('tt-title').textContent = poly.dataset.name;
        document.getElementById('tt-culture').textContent = poly.dataset.culture;
        document.getElementById('tt-ha').textContent = poly.dataset.ha + ' ha';
        tt.style.display = 'block';
    }
}
