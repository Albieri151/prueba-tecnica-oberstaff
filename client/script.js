// Módulo principal - Orquesta pantallas y llamadas API
import { renderLogin } from './screens/login.js';
import { renderDashboard } from './screens/dashboard.js';
import { safe, formatDate } from './lib/utils.js';

// Configuración
const API_URL = 'http://localhost:8000/api/v1/subscription-status';
const API_TOKEN = 'prueba-tecnica-oberstaff-seguridad';

// Elemento raíz
const app = document.getElementById('app');

// Estado de la aplicación
let state = {
    userId: localStorage.getItem('subscription_user_id'),
    loading: false,
    error: null,
    data: null
};

// Inicialización
function init() {
    render();
    if (state.userId) fetchSubscription();
}

// Renderiza la vista correcta
function render() {
    app.innerHTML = '';

    if (!state.userId) {
        renderLogin(app, (userId) => login(userId));
    } else {
        renderDashboard(app, state, { logout, fetchSubscription });
    }
}

// Acciones
function login(userId) {
    state.userId = userId;
    localStorage.setItem('subscription_user_id', userId);
    render();
    fetchSubscription();
}

function logout() {
    state.userId = null;
    state.data = null;
    state.error = null;
    localStorage.removeItem('subscription_user_id');
    render();
}

async function fetchSubscription() {
    state.loading = true;
    state.error = null;
    render();

    try {
        const response = await fetch(`${API_URL}/${state.userId}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${API_TOKEN}`
            }
        });

        if (!response.ok) {
            throw new Error(`Error: ${response.status} ${response.statusText}`);
        }

        const data = await response.json();
        state.data = data;
    } catch (err) {
        state.error = err.message;
    } finally {
        state.loading = false;
        render();
    }
}

// Export utilidad local por compatibilidad con módulos que la requieran
export { safe, formatDate };

// Iniciar app
document.addEventListener('DOMContentLoaded', init);
