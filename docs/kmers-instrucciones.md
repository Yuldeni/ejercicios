# Práctica 2: Contador de k-mers (Nivel Intermedio)

Archivo principal: `src/kmer_counter.py`

## Objetivos
- Trabajar con cadenas y slicing en Python.
- Validar entradas biológicas (secuencias de ADN).
- Usar `argparse` con argumentos posicionales y opcionales.
- Uso de diccionarios.
- Reflexionar sobre el uso de Copilot y comparación con tu propio código.

## Tareas
1. Usar PyLIA para analizar el problema "contador de k-mers" y guardar el resultado en `docs/analisis_kmers.md`. La ideas es "Lee una secuencia desde la línea de comandos y cuenta la frecuencia de cada k-mer." No generes código en este paso.
2. Revisar y/o completar `src/kmer_counter.py`:
   - Validar que la secuencia solo contenga A, T, C, G.
   - Leer la secuencia desde un argumento posicional.
   - Leer k desde `-k/--kmer_size`.
   - Contar todos los k-mers contiguos de longitud k.
   - Imprimir los resultados en formato `kmer<TAB>conteo`.
3. Ejecutar el script con diferentes valores de k y documentar los resultados en `docs/examples/kmer_examples.txt`.
4. Escribir una breve reflexión en `docs/reflexion_kmers.md` sobre:
   - Qué sugerencias de Copilot aceptaste.
   - Qué sugerencias rechazaste y por qué.

## Evaluación sugerida
- Funcionamiento correcto del programa.
- Validación adecuada.
- Claridad del código y comentarios.
- Reflexión honesta sobre el uso de IA.
