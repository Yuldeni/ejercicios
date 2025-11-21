# 🧪 Práctica 10 — Debug & Fix: Filtrado de Genes por Expresión

Este ejercicio consiste en **corregir un programa con varios errores sencillos**, algunos **marcados explícitamente** con comentarios como:

```python
# <-- ERROR
```

y otros **sin marcar**, que deberás identificar revisando la lógica del programa.

Tu tarea es entregar una **versión corregida y funcional** del script sin modificar el diseño general.


## 🎯 Objetivo

* Detectar errores sintácticos, lógicos y de validación.
* Corregir el flujo del programa para que funcione correctamente.
* Practicar debugging con pandas.
* Usar GitHub Copilot como apoyo, no como reemplazo del análisis personal.


## 🛠️ Actividades

### 1. Revisa el archivo buggy

En el código encontrarás:

* Algunos errores **marcados** con:

  ```python
  # <-- ERROR
  ```
* Varios errores **no marcados**, relacionados con:

  * importaciones de librerias
  * mal llamado a funciones, etc.

Tu trabajo es encontrarlos y corregirlos.


### 2. Corrige los errores detectados

El programa debe terminar haciendo lo siguiente:

1. Leer un archivo TSV con columnas:

   ```
   gene    expression
   ```
2. Convertir la columna `expression` a valores numéricos.
3. Recibir un threshold numérico desde la línea de comandos.
4. Filtrar los genes con expresión **mayor o igual** al threshold.
5. Imprimir los genes filtrados en orden alfabético.


### 3. Usa Copilot de forma crítica

Puedes pedir sugerencias, pero debes **evaluarlas**:

Crea el archivo:

```
docs/copilot_decisiones_expression.md
```

Incluye:

* sugerencias aceptadas
* sugerencias rechazadas
* por qué te parecieron correctas o incorrectas

---

### 4. Prueba tu programa

Ejecuta:

```bash
python src/gene-expression.py data/condA.tsv -t 10
```

Verifica que:

* no haya errores,
* solo aparezcan genes con expresión ≥ threshold,
* estén ordenados alfabéticamente.

Prueba también con diferentes thresholds.
