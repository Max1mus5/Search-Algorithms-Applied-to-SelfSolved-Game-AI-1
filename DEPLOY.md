# 🚀 Deploy Instructions

## Backend en Render

### 1. Configuración Render
- **Root Directory**: `api-backend`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python main.py`
- **Environment**: Python 3.11

### 2. Variables de Entorno Render
```
PORT=8000
HOST=0.0.0.0
```

## Frontend en Vercel

### 1. Configuración Vercel
- **Root Directory**: `web-frontend`
- **Build Command**: `npm run build`
- **Output Directory**: `.next`
- **Install Command**: `npm install`

### 2. Variables de Entorno Vercel
```
NEXT_PUBLIC_BACKEND_URL=https://your-backend-app.onrender.com
```

## 🔗 Conexión Frontend-Backend

1. **Deploy Backend primero** en Render
2. **Copiar URL** del backend (ej: `https://puzzle-solver-api.onrender.com`)
3. **Configurar variable** `NEXT_PUBLIC_BACKEND_URL` en Vercel
4. **Deploy Frontend** en Vercel

## 📝 Comandos de Configuración

### Para Render (Backend):
```bash
cd api-backend
pip install -r requirements.txt
python main.py
```

### Para Vercel (Frontend):
```bash
cd web-frontend
npm install
npm run build
npm start
```

## 🔧 Troubleshooting

### Si Render falla:
- Verificar que Python 3.11 esté configurado
- Asegurar que `requirements.txt` no tenga dependencias con Rust
- Verificar que las rutas de importación sean correctas

### Si Vercel falla:
- Verificar que `lib/utils.js` existe
- Configurar variable `NEXT_PUBLIC_BACKEND_URL`
- Asegurar que Next.js 14 esté soportado

## 🌐 URLs de Producción

- **Backend**: https://puzzle-solver-api.onrender.com
- **Frontend**: https://puzzle-solver-web.vercel.app
- **API Docs**: https://puzzle-solver-api.onrender.com/docs
