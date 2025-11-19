export function renderLogin(app, onLogin) {
    const tpl = document.getElementById('login-template');
    const clone = tpl.content.cloneNode(true);
    const form = clone.getElementById('login-form');

    form.addEventListener('submit', (e) => {
        e.preventDefault();
        const input = form.querySelector('#user-id');
        const userId = input.value.trim();

        if (userId) {
            onLogin(userId);
        }
    });

    app.appendChild(clone);
}
