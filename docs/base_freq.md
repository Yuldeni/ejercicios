# Refactorización del Código de Frecuencias de Bases

Se te entrega un programa que calcula la frecuencia de A, T, G y C de una secuencia FASTA, pero está escrito como **código espagueti** y sin funciones.

Tu tarea es **mejorarlo**, convirtiéndolo en un programa modular y limpio.


## ✔️ Objetivo

Refactorizar el código para:

* separar responsabilidades
* agregar funciones claras
* mejorar legibilidad
* mantener exactamente la misma funcionalidad


## 📁 Archivo a refactorizar

```
src/base_freq.py
```


## 🛠️ Lo que debes hacer

### 1) Analiza el código

Identifica rápidamente:

* dónde se mezclan validaciones, lectura, limpieza, cálculo y salida
* ausencia de funciones
* nombres poco descriptivos

Escribe un análisis breve en:

```
docs/analisis_base_freq.md
```

* O bien puedes usar el asistente PyLIA para que te haga una propuesta de como haria el rediseño de este programa.
* O bien puedes usa el Copilot Chat dentro de VS Code, y puedes usar el siguiente prompt:

```
Ayúdame a refactorizar el archivo que tengo abierto.

No escribas el código final. Solo guíame.

1. Analiza el archivo y dime:
   - qué responsabilidades están mezcladas
   - qué partes deberían ser funciones
   - qué problemas de claridad tiene

2. Proponme una lista corta de funciones en las que debería dividirlo.

3. Cuando te pida continuar:
   - guíame función por función
   - revisa mi código y dame retroalimentación

El comportamiento del programa debe seguir siendo exactamente el mismo.
``` 


### 2) Refactoriza

Crea un archivo limpio:

```
src/base_freq_clean.py
```

Incluye:

* varias funciones pequeñas (3–5)
* nombres claros
* docstrings
* validaciones separadas
* un `main()` simple y ordenado

---

### 3) Reflexión sobre Copilot

Archivo:

```
docs/reflexion_copilot_base_freq.md
```

Incluye en pocas líneas:

* sugerencias aceptadas
* sugerencias rechazadas
* qué parte fue más difícil

---

## 📤 Entrega mínima

```
src/base_freq_clean.py
docs/analisis_base_freq.md  --> si lo hiciste con el asistente PyLIA
docs/reflexion_copilot_base_freq.md
```

Tu meta: dejar el código claro, modular y fácil de mantener.
