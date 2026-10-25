# UT2 · Estructuras repetitivas — resumen para la P2

**Módulo 5099 · Estructuras de control en Python**

> Este apunte está en Markdown para probar la conversión automática a HTML para Moodle.
> El material completo de la unidad está en los PDF de esta carpeta.

## `while`: repetir mientras se cumpla una condición

```python
while True:
    opcion = input("Opción: ").strip().lower()
    if opcion in ("0", "s", "salir"):
        break          # sale del bucle
    print("Opción no válida.")
```

## Bucle de validación

Se repite la pregunta **hasta que el dato sea válido**. Se comprueba el texto **antes** de convertir:

```python
while True:
    texto = input("Número: ").strip()
    if texto.isdecimal() and 1 <= int(texto) <= 50:
        break
    print("Escribe un número entero del 1 al 50.")
```

## `for` con `range` y `else`

El `else` del `for` solo se ejecuta si el bucle termina **sin `break`**:

```python
for intento in range(1, max_intentos + 1):
    if numero == secreto:
        break
else:
    print("Sin intentos.")
```

## Comprensiones

| Tipo | Ejemplo |
| --- | --- |
| Con filtro | `[p for p in historial if p[1]]` |
| Con expresión condicional | `["G" if p[1] else "P" for p in historial]` |
| De diccionario | `{j: jugadas.count(j) for j in JUGADAS}` |

## Máximo y mínimo "a mano"

Se inicializa con el **primer elemento** y se compara con `<` o `>` estricto
(así, en caso de empate, se queda el primero):

```python
mejor = valores[0]
for v in valores:
    if v < mejor:
        mejor = v
```
