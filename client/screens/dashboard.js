import { safe, formatDate } from '../lib/utils.js';

export function renderDashboard(app, state, actions) {
    const tpl = document.getElementById('dashboard-template');
    const clone = tpl.content.cloneNode(true);

    // Elementos estáticos
    clone.getElementById('display-user-id').textContent = safe(state.userId, '-');

    const logoutBtn = clone.getElementById('logout-btn');
    logoutBtn.addEventListener('click', actions.logout);

    const retryBtn = clone.getElementById('retry-btn');
    if (retryBtn) retryBtn.addEventListener('click', actions.fetchSubscription);

    // Estados
    const loadingState = clone.getElementById('loading-state');
    const errorState = clone.getElementById('error-state');
    const dataState = clone.getElementById('data-state');

    if (state.loading) {
        loadingState.classList.remove('hidden');
        errorState.classList.add('hidden');
        dataState.classList.add('hidden');
    } else if (state.error) {
        loadingState.classList.add('hidden');
        errorState.classList.remove('hidden');
        dataState.classList.add('hidden');
        clone.getElementById('error-message').textContent = state.error;
    } else if (state.data) {
        loadingState.classList.add('hidden');
        errorState.classList.add('hidden');
        dataState.classList.remove('hidden');

        // Rellenar datos con valores por defecto si faltan
        clone.getElementById('plan-value').textContent = safe(state.data.plan, '-');

        const status = safe(state.data.status, 'unknown');
        const statusBadge = clone.getElementById('status-badge');
        statusBadge.textContent = String(status).replace('_', ' ');
        statusBadge.className = `badge badge-${status} capitalize`;
        if (!['active', 'past_due'].includes(status)) {
            statusBadge.classList.add('badge-default');
        }

        clone.getElementById('billing-date').textContent = formatDate(state.data.next_billing_at);

        if (state.data && state.data.trial_ends_at) {
            const trialSection = clone.getElementById('trial-section');
            trialSection.classList.remove('hidden');
            clone.getElementById('trial-date').textContent = formatDate(state.data.trial_ends_at, true);
        } else {
            const trialSection = clone.getElementById('trial-section');
            if (trialSection) trialSection.classList.add('hidden');
        }
    }

    app.appendChild(clone);
}
