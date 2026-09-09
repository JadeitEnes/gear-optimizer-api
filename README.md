⚙️ GEAR OPTIMIZER
**Hardware Performance Analyzer & System Optimizer**

Gear Optimizer is a full-stack web application designed for PC enthusiasts to analyze hardware configurations. It calculates performance efficiency across multiple workloads, providing deep insights into system capabilities.

## 🎨 Design Philosophy
The project features an **Authentic Retro-Terminal** interface. By combining classic computing aesthetics with a modern glassmorphism approach, Gear Optimizer offers a unique, distraction-free user experience. 

- **Retro Aesthetic:** Monospaced typography and high-contrast green color palette inspired by 80s hardware terminals.
- **Monogram Texture:** A custom-layered background pattern that adds depth and professional branding.
- **Dynamic Overlays:** Transparent analysis panels that provide a seamless transition from configuration to results.

## 🚀 Technical Stack
- **Backend:** FastAPI (Python) - High-performance asynchronous processing.
- **Frontend:** Pure JavaScript (Vanilla JS), HTML5, and CSS3 - Lightweight and highly responsive.
- **Database:** PostgreSQL - Robust and scalable data management for hardware components.
- **Containerization:** Fully Dockerized environment for seamless deployment.

## 🛠️ Key Features & Fixes
- **Unified Frontend:** Completely custom-built UI architecture.
- **Optimized Logic:** Fixed synchronization issues between frontend inputs and backend analysis services.
- **Usage Purpose Profiles:** Specialized analysis for Gaming, Video Editing, and Software Development.
- **Responsive Layout:** Fully compatible with mobile and desktop displays.

## 📦 Getting Started

### Docker (PostgreSQL included)
```bash
docker-compose up --build
```

### Local (SQLite, no database server needed)
```bash
pip install -r requirements-dev.txt
export DATABASE_URL="sqlite:///./gear_optimizer.db"
uvicorn app.main:app --reload
```

The catalog is seeded on startup, so no migration step is required.

| Endpoint | Purpose |
| --- | --- |
| `/ui` | Web interface |
| `/docs` | Interactive API docs |
| `/health` | Liveness probe for deployment platforms |

## ✅ Tests
```bash
pytest
```
Tests run against an in-memory SQLite database with fixed hardware fixtures, so no
external service is required and the production database is never touched.

## ⚙️ Configuration
| Variable | Default | Notes |
| --- | --- | --- |
| `DATABASE_URL` | *(required)* | PostgreSQL or SQLite connection string |
| `ALLOWED_ORIGINS` | `http://localhost:8000` | Comma-separated CORS origins. Only needed if the frontend is served from a different domain than the API |
| `SECRET_KEY` | `default_secret` | Override in production |
| `DEBUG` | `false` | |