<h1 align="center">Minicore de Comisiones</h1>

<p align="center">
  Aplicación web para registrar ventas y calcular las comisiones de los vendedores dentro de un rango de fechas.
</p>


<p align="center">
  <img src="https://img.shields.io/badge/STATUS-EN%20DESARROLLO-green" alt="Estado: en desarrollo">
  <img src="https://img.shields.io/badge/Django-REST%20Framework-092E20?logo=django&logoColor=white" alt="Django REST Framework">
  <img src="https://img.shields.io/badge/React-Vite-61DAFB?logo=react&logoColor=black" alt="React con Vite">
  <img src="https://img.shields.io/badge/DB-PostgreSQL-4169E1?logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/Deploy-Render%20%2B%20Netlify-46E3B7" alt="Render y Netlify">
</p>


Deploy: https://wonderful-puffpuff-6f8513.netlify.app/


> El plan gratuito de Render duerme el servicio tras un tiempo sin uso: la primera petición puede tardar entre 30 y 60 segundos.


[![Ver video en YouTube](https://img.youtube.com/vi/_SlsjfD5IUs/0.jpg)](https://youtu.be/_SlsjfD5IUs)

## Índice

* [Descripción del proyecto](#descripción-del-proyecto)
* [Estado del proyecto](#estado-del-proyecto)
* [Funcionalidades](#funcionalidades)
* [Reglas de comisión](#reglas-de-comisión)
* [Instalación y ejecución](#instalación-y-ejecución)
* [Despliegue](#despliegue)
* [API](#api)
* [Tecnologías utilizadas](#tecnologías-utilizadas)

## Descripción del proyecto

**Minicore de Comisiones** es una aplicación web full stack que permite registrar las ventas de cada vendedor y consultar cuánto les corresponde de comisión en un rango de fechas.

El backend expone una API REST con Django REST Framework. El frontend, hecho con React, consume esa API y ofrece una pantalla para registrar ventas (con un combo box de vendedores) y otra para consultar las comisiones por rango de fechas. Las reglas de comisión están definidas directamente en el código.

## Estado del proyecto

En desarrollo. Desplegado con el backend y la base de datos en Render y el frontend en Netlify.

## Funcionalidades

- `Registro de ventas`: se elige el vendedor en un combo box y se ingresa la cantidad. La fecha se asigna automáticamente (`auto_now_add`).
- `Listado de vendedores`: la API entrega los vendedores para llenar el combo box.
- `Cálculo de comisiones`: dado un rango `desde` / `hasta`, agrupa las ventas por vendedor y calcula total vendido, porcentaje aplicado y comisión.
- `Panel de administración`: los modelos están registrados en el admin de Django para crear vendedores y ventas.
- `Validaciones`: fechas con formato inválido, rango invertido y cantidades no positivas devuelven errores claros.

## Reglas de comisión

Se aplica un único porcentaje según el total vendido por el vendedor en el rango:

| Total vendido | Porcentaje |
|---|---|
| > 10 000 | 10% |
| > 5 000 | 7% |
| > 1 000 | 5% |
| < 1 000 | 2% |

Las reglas están en `commissions/services.py` (`COMMISSION_TIERS`).

## Instalación y ejecución

### Requisitos previos

- Python 3.10 o superior
- Node.js 18 o superior
- `pip` y `npm`

### 1. Backend (Django)

```bash
# Crear y activar un entorno virtual
python -m venv .venv
source .venv/bin/activate        # En Windows: .venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Crear la base de datos
python manage.py makemigrations
python manage.py migrate

# Crear un superusuario para el admin
python manage.py createsuperuser

# Iniciar el servidor
python manage.py runserver
```

El backend queda disponible en `http://localhost:8000/`. En local usa SQLite (`db.sqlite3`).

### 2. Frontend (React + Vite)

En otra terminal:

```bash
cd frontend
npm install
npm run dev
```

El frontend queda disponible en `http://localhost:5173/`. Rutas:

- `/ventas`: registrar una venta
- `/comisiones`: consultar comisiones por rango de fechas


## Despliegue

### Backend en Render

- **Build command:**
  ```
  pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
  ```
- **Start command:**
  ```
  gunicorn config.wsgi:application
  ```
- Crear una base PostgreSQL en Render (misma región) y pegar su *Internal Database URL* en `DATABASE_URL`.

### Frontend en Netlify

- **Build command:** `npm run build`
- **Publish directory:** `dist`
- Archivo `public/_redirects` para que funcionen las rutas de React Router:
  ```
  /*    /index.html   200
  ```


## API

Prefijo base: `/api/`

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/api/vendedores/` | Listar vendedores |
| POST | `/api/ventas/` | Crear una venta. Body: `{"Vendedor": 1, "cantidad": 250.5}` |
| GET | `/api/comisiones/?desdeYYYY-MM-DD&hastaYYYY-MM-DD` | Comisiones por vendedor en el rango |

Ejemplo de respuesta de comisiones:

```json
{
  "desde": "2026-10-01",
  "hasta": "2026-10-31",
  "resultados": [
    {
      "vendedor_id": 1,
      "vendedor": "Ana",
      "num_ventas": 12,
      "total_ventas": "6350.50",
      "porcentaje": "7.00",
      "comision": "444.54"
    }
  ]
}
```

## Tecnologías utilizadas

**Backend**

- [Python](https://www.python.org/)
- [Django](https://www.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [django-cors-headers](https://github.com/adamchainz/django-cors-headers)
- [WhiteNoise](https://whitenoise.readthedocs.io/)
- [Gunicorn](https://gunicorn.org/)
- [PostgreSQL](https://www.postgresql.org/) (producción) y SQLite (local)

**Frontend**

- [React](https://react.dev/)
- [Vite](https://vitejs.dev/)
- [React Router](https://reactrouter.com/)
- CSS con variables personalizadas

**Despliegue**

- [Render](https://render.com/) (API y base de datos)
- [Netlify](https://www.netlify.com/) (frontend)
