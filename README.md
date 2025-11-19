# Prueba Técnica — Motor de Facturación y Suscripciones (SaaS)

## Descripción
Sistema de automatización para una empresa SaaS ficticia que gestiona el ciclo de vida de facturación y suscripciones.  
Incluye recordatorios de prueba, renovaciones, reintentos de pago fallido (dunning) y un portal de cliente para consultar el estado de la suscripción.  
La solución integra **n8n** como orquestador, una **base de datos real en supabase**, un **microservicio en FastApi** y un **frontend en JS vainilla**.

---

## Desarrollador

| Nombre         | Albieri Alaña                                                                                 |
|----------------|-----------------------------------------------------------------------------------------------|
| Rol            | Desarrollador Full Stack                                                                     |
| Contacto       | [Albieri Alaña - LinkedIn](https://www.linkedin.com/in/albieri-maximiliano-ala%C3%B1a-reyes/) |

## Arquitectura
- **n8n (Orquestador)**: Flujos CRON diarios, enrutamiento dinámico y sub-workflows reutilizables.
- **Base de Datos (Supabase/Postgres)**: tablas `subscriptions` y `automation_logs`.
- **Microservicio Backend (Python/FastAPI)**: API REST con lógica de negocio y conexion a la base de datos.
- **Frontend JS Vainilla**: Portal simple pero funcional y seguro para clientes.
- **Error Trigger Global**: Captura y registro centralizado de fallos.

---

### 1.1 Diseño de la Base de Datos

Tabla `subscriptions`:

- `user_id` (string, PK)  
- `email` (string)  
- `plan_type` (string: 'basic', 'pro')  
- `status` (enum: 'trial', 'active', 'past_due', 'canceled')  
- `trial_ends_at` (timestamp)  
- `next_billing_at` (timestamp)  
- `last_payment_attempt` (timestamp, opcional)

Tabla `automation_logs`:

- `id` (string, PK)  
- `action` (string)  
- `error_message` (string)  
- `created_at` (timestamp)  

---

Para poblar la base de datos deje un archivo json con datos ficticios, pueden cambiarlos a su gusto y un scrip solo de ejecutarlo llamado load_subscriptions en entorno windows

## Arquitectura del Microservicio (Resumen)

## Visión general
Microservicio construido con FastAPI siguiendo una arquitectura por capas:
- API (endpoints) → Services (lógica de negocio) → Domain (modelos Pydantic) → Settings (acceso a datos/Supabase, autentificacion).

## Estructura principal
- `app/main.py` — Configuración de la app, middleware (CORS) y montaje de routers.
- `app/api/v1/endpoints/` — Rutas/Controllers:
  - `subscription_status.py`
  - `billing_actions.py`
- `app/services/` — Lógica de negocio:
  - `billing_service.py`
  - `subscription_service.py`
- `app/domain/` — Modelos Pydantic y schemas:
  - `domain.py` (modelos de dominio)
  - `schemas.py` (request/response)
- `app/settings/` — Configuración e infra:
  - `config.py` (settings)
  - `database.py` (cliente Supabase con `httpx`)

## Flujo de una petición (rápido)
1. Cliente → HTTP request a `/api/v1/...`.
2. FastAPI rutea al endpoint en `app/api/v1/endpoints`.
3. Endpoint valida/decodifica payload con Pydantic y obtiene dependencias (`Depends()`).
4. Endpoint llama al servicio correspondiente en `app/services`.
5. Servicio orquesta lógica y llama a la capa infra (`SupabaseClient`) para obtener datos.
6. Datos JSON devueltos por la infra son mapeados a modelos `SubscriptionDomain`.
7. Servicio devuelve modelos de dominio; el endpoint convierte a `response_model` y FastAPI responde en JSON.

## Reglas de negocio clave (billing)
- Si `status == 'trial'` y `trial_ends_at` es en 3 días → `send_trial_reminder`.
- Si `status == 'trial'` y `trial_ends_at` es hoy → `process_trial_conversion`.
- Si `status == 'active'` y `next_billing_at` es hoy → `process_renewal_payment`.
- Si `status == 'past_due'` → `send_dunning_email`.

## Consideraciones prácticas
- Secrets: no hardcodear en `config.py`; usar variables de entorno, por temas de rapidez en este proyecto estan expuestas temporalmente.
- Timezones: hoy se compara por fecha (YYYY-MM-DD). Si se llegara a necesitar un cambio por hora/timezone, usar parsing timezone-aware (p. ej. `dateutil` / `pendulum`) y normalizar a UTC.
- Errores: atrapar parseos de fecha y errores de red en la capa servicio/infra para evitar 500s inesperados.

## Comandos rápidos
```bash
# Desde la carpeta del microservicio
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
Endpoints:
- **POST /calculate-billing-actions**  
  Decide acciones de facturación según estado y fechas.
- **GET /subscription-status/:user_id**  
  Devuelve estado de suscripción para el portal.
- **GET /health**  
  Devuelve el estado del microservicio.

---

## Flujos en n8n
- **Flujo Principal (CRON diario)**  
  1. Leer suscripciones activas/trial.  
  2. Enviar lista al microservicio.  
  3. Recibir acciones → `SplitInBatches` + `Switch`.  
  4. Ejecutar sub-workflows de notificación y actualización BD.

- **Sub-Workflow Notificación**  
  - Input: `user_id`, `email`, `template_name`.  
  - Nodo Code JS: gestor de plantillas.  
  - Output: email/SMS real.  
  - Manejo de errores: registro en `automation_logs`.

- **Gestión de Estado**  
  - Ejemplo: `process_renewal_payment` → notificación + update BD.  
  - Transaccionalidad simulada: si falla update, se registra error.

---

## Frontend JS Vainilla
Portal simple para clientes:
- Login simulado con `user_id` en `localStorage`.
- Dashboard: `fetch` a `GET /subscription-status/:user_id` con Bearer Token.
- Muestra plan, estado y próxima facturación.
- Manejo de estados: “Cargando…”, éxito o error.

Ejemplo:
```html
<input id="userIdInput" placeholder="Ingresa tu User ID" />
<button onclick="login()">Login</button>
<div id="status"></div>
<script>
  const API_URL = "http://localhost:8000/subscription-status/";
  const TOKEN = "";
  async function login() {
    const userId = document.getElementById("userIdInput").value;
    localStorage.setItem("user_id", userId);
    const res = await fetch(API_URL + userId, { headers: { Authorization: TOKEN }});
    const data = await res.json();
    document.getElementById("status").innerText =
      `Plan: ${data.plan}, Estado: ${data.status}, Próxima Facturación: ${data.next_billing_at}`;
  }
</script>
### Instalar el ambiente local (Conda)

Recreemos el entorno de desarrollo

```powershell
# Crea el entorno desde environment.txt (usa el nombre que esté en el archivo)
conda env create -f environment.txt

# Activa el entorno (reemplaza <env_name> por el nombre del entorno creado)
conda activate <env_name>
```

Si prefieres crear un entorno nuevo e instalar dependencias manualmente:

```powershell
conda create -n fastApi python=3.10 -y
conda activate fastApi
pip install -r billing_microservice/requirements.txt 
```


---

### Levantar el frontend (Live Server)

Para levantar el cliente desde Visual Studio Code puedes usar la extensión **Live Server**.

> Nota: el cliente incluye un token hardcodeado para agilizar las pruebas (no recomendado en producción).

### Ejecutar n8n con Docker

1. Asegúrate de tener Docker instalado.
2. Crea un volumen para persistir los datos de n8n:

```powershell
docker volume create n8n_data
```

3. Ejecuta n8n en un contenedor (puerto por defecto 5678):

```powershell
docker run -it --rm --name n8n -p 5678:5678 -v n8n_data:/home/node/.n8n docker.n8n.io/n8nio/n8n
```

4. Importa los flujos (`.json`) desde la UI: `Workflows → Import`.

5. Configura las credenciales en `Credentials` (Gmail / Supabase / etc.) y ajusta los nodos de email para usar `{{$json["email"]}}` o las variables correspondientes.

Documentación oficial de n8n: https://github.com/n8n-io/n8n

---

## Fin

Con esto solo queda pendiente ejecutar el proyecto en tu IDE de preferencia. Si tienes dudas, contáctame — será un gusto ayudar! 🔥🔥