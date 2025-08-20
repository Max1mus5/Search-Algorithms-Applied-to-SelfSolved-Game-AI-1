# 🧩 8-Puzzle Search Algorithms

## Descripción

Implementación completa de algoritmos de búsqueda informados y no informados para resolver el problema del 8-puzzle. El proyecto incluye:
- **6 algoritmos de búsqueda** implementados desde cero
- **Interfaz CLI** para línea de comandos  
- **Interfaz GUI** con tkinter
- **Interfaz Web moderna** con Next.js y FastAPI

## Estructura Básica

```
├── Abstractions.py           # Clases Node, Problem y utilidades comunes
├── Strucure.py               # Stack, Queue, MinHeap implementados a mano
├── Heuristics.py             # Heurísticas Manhattan y Misplaced Tiles
├── Problems/
│   └── N-8-Problem.py        # Definición del problema 8-puzzle
├── Search-algoritms/
│   └── BFS - DFS - Uniform Cost - Greedy - A - IDA.py  # Algoritmos de búsqueda
├── main.py                   # Interfaz de línea de comandos
├── main_UI.py                # Interfaz gráfica (tkinter)
└── requirements.txt          # Documentación de dependencias
```

## Arquitectura del Sistema

```mermaid
graph TD
    User["👤 Usuario"]
    StartScript["🚀 start-web.sh"]
    
    subgraph CoreSystem["🧠 Sistema Central - Python"]
        SearchAlgorithms["🔍 Algoritmos de Búsqueda"]
        N8Problem["🧩 Problema N-8"]
        
        subgraph Foundations["⚙️ Fundamentos"]
            Abstractions["📦 Abstracciones"]
            Heuristics["🎯 Heurísticas"]
            Structure["🏗️ Estructuras"]
        end
        
        subgraph EntryPoints["🚪 Puntos de Entrada"]
            MainScript["💻 CLI Principal"]
            MainUI["🖥️ GUI Principal"]
        end
    end
    
    subgraph Backend["🐍 Backend API"]
        BackendMain["🔧 Servidor FastAPI"]
        BackendReq["📋 Dependencias"]
    end
    
    subgraph Frontend["🌐 Frontend Web"]
        ParseUtils["🔄 Utilidades"]
        
        subgraph AppEntry["📱 Aplicación"]
            CustomApp["⚛️ App Principal"]
            IndexPage["🏠 Página Inicio"]
        end
        
        subgraph Config["⚙️ Configuración"]
            NextConfig["⚙️ Next.js"]
            PackageJSON["📦 NPM"]
            TailwindConfig["🎨 Tailwind"]
            GlobalStyles["💄 Estilos"]
        end
        
        subgraph Components["🧩 Componentes"]
            BoardComponent["🎲 Tablero"]
            
            subgraph UIKit["🎨 Kit UI"]
                Button["🔘 Botón"]
                Card["🃏 Tarjeta"]
                Select["📝 Selector"]
                Slider["🎚️ Deslizador"]
                Textarea["📄 Área de Texto"]
            end
        end
    end
    
    %% Relaciones principales
    Backend -->|"invoca lógica"| CoreSystem
    Backend -->|"envía resultados"| Frontend
    Frontend -->|"solicitudes HTTP"| Backend
    StartScript -->|"inicia"| Backend
    StartScript -->|"inicia"| Frontend
    User -->|"interactúa"| Frontend
    
    %% Relaciones internas
    SearchAlgorithms -->|"usa"| Abstractions
    SearchAlgorithms -->|"usa"| Heuristics
    SearchAlgorithms -->|"usa"| Structure
    N8Problem -->|"implementa"| Abstractions



## Algoritmos Implementados

### No Informados
- **BFS** (Breadth-First Search): Búsqueda en anchura
- **DFS** (Depth-First Search): Búsqueda en profundidad con límite
- **UCS** (Uniform Cost Search): Búsqueda de costo uniforme

### Informados
- **Greedy**: Búsqueda voraz (Best-First)
- **A\*** (A-Star): Búsqueda óptima con heurística
- **IDA\*** (Iterative Deepening A-Star): A* con profundización iterativa

## Heurísticas

1. **Manhattan Distance**: Suma de distancias Manhattan por ficha
2. **Misplaced Tiles**: Número de fichas fuera de lugar

## Uso

### Interfaz de Línea de Comandos

```bash
# Ejecutar menú interactivo
python main.py

# Ejecutar prueba rápida de todos los algoritmos
python main.py --test
```

### Interfaz Gráfica

```bash
# Requiere tkinter instalado
python main_UI.py
```

### Instalación de tkinter (si es necesario)

```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# CentOS/RHEL
sudo yum install tkinter

# Arch Linux
sudo pacman -S tk
```

## Estados de Prueba

- **Fácil**: `(1,2,3,4,5,6,7,0,8)` - 1 movimiento
- **Medio**: `(1,2,3,4,5,6,0,7,8)` - 2-4 movimientos  
- **Difícil**: `(7,2,4,5,0,6,8,3,1)` - Múltiples movimientos

## Métricas Reportadas

- ✅ **Éxito**: Si encontró solución
- 📏 **Profundidad**: Número de pasos en la solución
- 💰 **Costo**: Costo total de la solución
- 🔍 **Nodos Expandidos**: Número de nodos explorados
- ⏱️ **Tiempo**: Tiempo de ejecución en segundos
- 🗺️ **Acciones**: Secuencia de movimientos

## Ejemplo de Uso

```python
from Problems.N_8_Problem import EightPuzzle
from Heuristics import HEURISTICS, GOAL

# Crear problema
problem = EightPuzzle((1,2,3,4,5,6,7,0,8))

# Importar algoritmo
from Search_algoritms.BFS___DFS___Uniform_Cost___Greedy___A___IDA import astar

# Resolver con A*
h_func = lambda s: HEURISTICS["manhattan"](s, GOAL)
result = astar(problem, h_func)

print(f"Solución encontrada: {result['success']}")
print(f"Profundidad: {result['depth']}")
print(f"Tiempo: {result['time']:.6f}s")
```

## Requisitos

- Python 3.8+
- Solo librerías estándar (sin pip install requerido)
- tkinter (opcional, para GUI)

## Validación

Todos los algoritmos han sido probados con:
- ✅ Estados válidos y resolubles
- ✅ Validación de entrada
- ✅ Manejo de errores
- ✅ Métricas consistentes
- ✅ Límites de profundidad/tiempo

## Características Implementadas

### CLI y GUI (Python Nativo)
- [x] Estructuras de datos manuales (Stack, Queue, MinHeap)
- [x] 6 algoritmos de búsqueda completos
- [x] 2 heurísticas optimizadas
- [x] Interfaz CLI con menú interactivo
- [x] Interfaz GUI básica (tkinter)
- [x] Métricas completas (tiempo, nodos, costo)
- [x] Validación de estados
- [x] API consistente entre algoritmos

### Interfaz Web Moderna
- [x] FastAPI backend con endpoints REST
- [x] Next.js frontend con Tailwind CSS
- [x] Interfaz web moderna y responsive  
- [x] Animación paso a paso de soluciones
- [x] Estados predefinidos y métricas detalladas
- [x] Playback controls (play/pause/reset/speed)
- [x] Validación de solvabilidad
- [x] Integración completa frontend-backend

## Instalación y Uso

### Interfaz Web (Recomendado)

#### Inicio Rápido
```bash
# Ejecutar interfaz web completa (backend + frontend)
./start-web.sh
```

#### Instalación Manual

**Backend (FastAPI):**
```bash
cd api-backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

**Frontend (Next.js):**
```bash
cd web-frontend
npm install
npm run dev
```

#### URLs de Acceso
- 🌐 **Frontend**: http://localhost:3000
- 🔗 **Backend API**: http://localhost:8000  
- 📚 **API Documentation**: http://localhost:8000/docs

### Desarrollo Futuro
- [ ] Extensión a laberintos N×N
- [ ] Versión móvil (React Native)
- [ ] Optimizaciones de rendimiento
- [ ] Comparación de algoritmos en tiempo real

## Estructura del Proyecto

```
8-Puzzle-Solver/
├── 🐍 Backend Python
│   ├── Abstractions.py           # Clases base y abstracciones
│   ├── Strucure.py               # Estructuras de datos manuales
│   ├── Heuristics.py             # Funciones heurísticas
│   ├── Problems/N-8-Problem.py   # Definición del problema 8-puzzle
│   ├── Search-algoritms/...      # 6 algoritmos de búsqueda
│   ├── main.py                   # Interfaz CLI
│   ├── main_UI.py                # Interfaz GUI (tkinter)
│   └── api-backend/              # Servidor web FastAPI
│       ├── main.py               # API REST
│       └── requirements.txt
│
└── 🌐 Frontend Web
    └── web-frontend/             # Next.js + Tailwind CSS
        ├── pages/index.js        # Página principal
        ├── components/           # Componentes React
        ├── utils/                # Utilidades JavaScript
        └── styles/               # Estilos CSS
```

## Autor

Implementación completa para el Taller 1 de Buscadores en IA.
- ✅ **Algoritmos de Búsqueda**: 6 implementaciones completas
- ✅ **Interfaces**: CLI, GUI y Web moderna
- ✅ **Arquitectura**: Modular y escalable
