# 8-Puzzle Search Algorithms - FASE 1

## Descripción

Implementación completa de algoritmos de búsqueda informados y no informados para resolver el problema del 8-puzzle usando únicamente librerías estándar de Python.

## Estructura del Proyecto

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

### Fase 1 ✅
- [x] Estructuras de datos manuales (Stack, Queue, MinHeap)
- [x] 6 algoritmos de búsqueda completos
- [x] 2 heurísticas optimizadas
- [x] Interfaz CLI con menú interactivo
- [x] Interfaz GUI básica (tkinter)
- [x] Métricas completas (tiempo, nodos, costo)
- [x] Validación de estados
- [x] API consistente entre algoritmos

### Próximas Fases
- [ ] Animación paso a paso (GUI)
- [ ] Extensión a laberintos
- [ ] Versión móvil (Pythonista/Pydroid)
- [ ] Optimizaciones de rendimiento

## Autor

Implementación completa para el Taller 1 de Buscadores en IA.
