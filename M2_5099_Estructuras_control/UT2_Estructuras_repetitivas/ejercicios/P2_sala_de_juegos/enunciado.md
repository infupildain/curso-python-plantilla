# Práctica P2 · Sala de juegos

**Módulo 5099 · Estructuras de control en Python — UT2 · Estructuras repetitivas**
*Desarrollo de aplicaciones en Python*

**Hito 1 · Práctica formativa** (no cuenta para la nota final, pero se corrige y se comenta en clase). Individual.

Vas a programar una **sala de juegos de consola**: un menú que se repite hasta que el usuario decide salir, con dos juegos (*Adivina el número* y *Piedra, papel o tijera*) y una opción de **estadísticas** que resume todas las partidas jugadas.

Esta práctica **cierra la UT2** y reúne todo lo visto hasta ahora: condicionales, `match-case` y validación (UT1), y `while`, `for`, `for-else`, listas, comprensiones y algoritmos clásicos (UT2).

> **Todavía sin funciones.** Todo el programa va en un solo archivo (`sala_de_juegos.py`) y sin `def`. Cuando veamos las **funciones** refactorizaremos esta misma práctica, así que guárdala bien.

**Qué se practica:** diagramas de flujo con bucles, menú en bucle con `match-case`, bucles de validación, `for` con `range` y `else`, contadores y acumuladores, listas, comprensiones de listas y de diccionarios, máximo y mínimo con posición.

### Qué hay que entregar (todo en tu repositorio de GitHub)

| Parte | Archivo |
| --- | --- |
| **A · Diagramas de flujo** (hazlos **antes de programar**: el diagrama es tu plan) | `diagramas/menu.png` y `diagramas/adivina.png` |
| **B · Código** del programa completo | `sala_de_juegos.py` |
| **C · Pruebas**: la tabla de casos de prueba rellenada | `PRUEBAS.md` |
| **D · Hacia las funciones**: reflexión breve sobre tu código | `REFLEXION.md` |

**Para entregar:** abre el proyecto en PyCharm, haz *commit* de tus cambios y *push* a GitHub
(*Git → Commit…* marcando **Commit and Push**). Puedes hacer todos los *push* que quieras hasta la fecha límite:
se corrige el último. En la pestaña **Actions** de GitHub verás si pasan las comprobaciones automáticas.

## 0. Punto de partida

El archivo `sala_de_juegos.py` ya trae estas líneas. No las borres: tu programa empieza debajo.

```python
import random

# Constantes
MODO_PRUEBA = False   # True: muestra el número secreto y la jugada del ordenador
JUGADAS = ["piedra", "papel", "tijera"]
GANA_A = {"piedra": "tijera", "papel": "piedra", "tijera": "papel"}   # clave gana a valor

# Datos que se guardan entre partidas
historial = []         # una tupla por partida: (juego, ganada, intentos_o_rondas)
jugadas_usuario = []   # todas tus jugadas de piedra, papel o tijera
```

- `import random` carga el módulo de números aleatorios (los módulos se verán más adelante). Solo necesitas dos cosas:
  - `random.randint(1, 100)` devuelve un entero al azar entre 1 y 100, **ambos incluidos**.
  - `random.choice(JUGADAS)` devuelve un elemento al azar de la lista.
- `MODO_PRUEBA`: ponlo a `True` mientras pruebas, para saber el número secreto y la jugada del ordenador. **Entrega con `False`.**
- `GANA_A["piedra"]` vale `"tijera"`: la piedra gana a la tijera.
- Cada partida terminada se guarda en `historial` como una tupla de tres elementos:
  - `("adivina", True, 5)`: Adivina el número, ganada, en 5 intentos.
  - `("ppt", False, 4)`: Piedra, papel o tijera, perdida, en 4 rondas.

## 1. El menú

```
=== SALA DE JUEGOS ===
1. Adivina el número
2. Piedra, papel o tijera
3. Estadísticas
0. Salir
Opción:
```

- El menú **se repite** después de cada opción hasta que el usuario sale (bucle `while`).
- Lee la opción con `.strip().lower()` y resuélvela con `match-case`, tratándola **como texto**.
- Para salir valen `0`, `s` o `salir`. Al salir se muestra `¡Hasta pronto! Has jugado N partidas.`
- Cualquier otra opción muestra `Opción no válida.` y el menú vuelve a aparecer.

## 2. Opción 1 · Adivina el número

**Nivel.** Pide el nivel hasta que sea válido (acepta la letra o la palabra, con o sin tilde):

| Nivel | Se escribe | Número secreto | Intentos |
| --- | --- | --- | --- |
| Fácil | `f`, `fácil`, `facil` | del 1 al 50 | 8 |
| Normal | `n`, `normal` | del 1 al 100 | 7 |
| Difícil | `d`, `difícil`, `dificil` | del 1 al 500 | 9 |

**Partida.**

- El ordenador elige el número secreto con `random.randint`.
- Usa un **`for` con `range`** para los intentos y su **`else`** para el caso de quedarse sin intentos.
- Cada intento se pide **hasta que sea válido**: un entero dentro del rango del nivel y que **no se haya dicho antes** en esta partida. Un dato no válido o repetido muestra un aviso y **no gasta intento**.
- Si aciertas: `¡Acertaste en N intentos!` Si no, la pista: `El número secreto es mayor que 25.` o `… menor que …` (elige la palabra con una **expresión condicional**).
- Al terminar, guarda la partida en `historial`. Si se pierde, los intentos guardados son los del nivel.

**Ejemplo de ejecución:**
```
Opción: 1
Nivel (f = fácil, n = normal, d = difícil): x
Nivel no válido.
Nivel (f = fácil, n = normal, d = difícil): f
He pensado un número del 1 al 50. Tienes 8 intentos.
Intento 1/8: 25
El número secreto es menor que 25.
Intento 2/8: doce
Escribe un número entero del 1 al 50.
Intento 2/8: 12
El número secreto es menor que 12.
Intento 3/8: 12
Ya habías dicho ese número.
Intento 3/8: 6
El número secreto es mayor que 6.
Intento 4/8: 9
El número secreto es menor que 9.
Intento 5/8: 7
¡Acertaste en 5 intentos!
```

## 3. Opción 2 · Piedra, papel o tijera

- Pregunta si se juega **al mejor de 3 o de 5** (repite hasta que la respuesta sea `3` o `5`). Al mejor de 3 gana quien llega antes a 2 victorias; al mejor de 5, a 3.
- Cada ronda: el ordenador elige con `random.choice(JUGADAS)` y tú escribes tu jugada (repite hasta que sea `piedra`, `papel` o `tijera`, sin importar mayúsculas ni espacios).
- Guarda cada jugada tuya válida en `jugadas_usuario`.
- Decide quién gana la ronda usando el diccionario `GANA_A`. **Los empates no suman**, así que la partida puede durar más rondas que el número elegido.
- Tras cada ronda muestra la jugada del ordenador, el resultado y el marcador.
- Al terminar, muestra el resultado de la partida y guárdala en `historial` con el número de rondas jugadas.

**Ejemplo de ejecución:**
```
Opción: 2
¿Al mejor de cuántas rondas? (3 o 5): 4
Escribe 3 o 5.
¿Al mejor de cuántas rondas? (3 o 5): 3
Ronda 1 · piedra, papel o tijera: Piedra
Ordenador: tijera → ganas la ronda. Marcador: 1-0
Ronda 2 · piedra, papel o tijera: papel
Ordenador: papel → empate. Marcador: 1-0
Ronda 3 · piedra, papel o tijera: lagarto
Jugada no válida.
Ronda 3 · piedra, papel o tijera: tijera
Ordenador: piedra → gana el ordenador. Marcador: 1-1
Ronda 4 · piedra, papel o tijera: papel
Ordenador: piedra → ganas la ronda. Marcador: 2-1
¡Has ganado la partida!
```

## 4. Opción 3 · Estadísticas

Si todavía no hay partidas, muestra `Todavía no has jugado ninguna partida.` Si las hay, muestra:

1. Partidas jugadas, partidas ganadas y porcentaje de victorias.
2. La línea de resultados en orden: `G` por cada partida ganada y `P` por cada perdida.
3. Para cada juego, cuántas partidas se han jugado y cuántas se han ganado.
4. **Mejor partida de Adivina**: la partida ganada con menos intentos y su número de partida (posición en el historial, empezando en 1). Si hay empate, la primera. Si no se ha ganado ninguna, no se muestra la línea.
5. **Tus jugadas**: cuántas veces has sacado cada una, y tu jugada **favorita** (si hay empate, la que aparece antes en `JUGADAS`). Si no has jugado a piedra, papel o tijera, no se muestran estas líneas.

**Obligatorio:** al menos **tres comprensiones**: una con **filtro** (`if`), una con **expresión condicional** y una **comprensión de diccionario**. La mejor partida y la jugada favorita se calculan **con el algoritmo de máximo y mínimo** de los algoritmos clásicos (sin `min()` ni `max()`).

**Ejemplo de ejecución:**
```
Opción: 3

=== ESTADÍSTICAS ===
Partidas: 5 · ganadas: 4 (80 %)
Resultados: G G G P G
Adivina el número · partidas: 3 · ganadas: 3
Piedra, papel o tijera · partidas: 2 · ganadas: 1
Mejor partida de Adivina: la nº 5 (5 intentos)
Tus jugadas: piedra 1, papel 2, tijera 2
Tu jugada favorita: papel
```

## 5. Requisitos de código

- **Sin `def` y sin `try/except`**: la validación se hace comprobando el texto antes de convertir (`isdecimal()`, `in`…).
- El programa **no puede romperse ni quedarse colgado** con ninguna entrada del usuario.
- Menú con `while` + `match-case`; al menos un `for` con `range` y `else`; al menos un bucle de validación.
- Al menos **tres comprensiones** (ver apartado 4) y al menos una **expresión condicional**.
- Usa `break` y `continue` cuando eviten anidar más de lo necesario.
- Nombres de variables descriptivos y en minúsculas, constantes en MAYÚSCULAS, sangrado de 4 espacios y comentarios breves donde ayuden.

## 6. Rúbrica (formativa)

| Criterio | Puntos |
| --- | --- |
| Diagramas de flujo: bucles bien representados (vuelta atrás y salida), una entrada y una salida, coinciden con el código | 2 |
| Menú en bucle con `match-case`, salida con varias alternativas y opción no válida | 1 |
| Validación de **todas** las entradas con bucles: ninguna entrada rompe el programa ni gasta intentos | 1,5 |
| Adivina el número: niveles, pistas, números repetidos y `for-else` correctos | 2 |
| Piedra, papel o tijera: al mejor de 3 o 5, empates y marcador correctos | 1,5 |
| Estadísticas con las tres comprensiones y los algoritmos de máximo y mínimo | 1 |
| Tabla de pruebas, Parte D y estilo del código | 1 |
| **Total** | **10** |

## 7. Si terminas antes (optativo, no puntúa)

- **Caliente o frío:** si el número dicho está a 5 o menos del secreto, añade `¡Caliente!` a la pista.
- **Piedra, papel, tijera, lagarto, Spock:** amplía `JUGADAS` y cambia `GANA_A` para que cada clave tenga como valor **la lista** de jugadas a las que gana. ¿Qué otras líneas tienes que tocar?
- **Racha:** en las estadísticas, muestra la racha más larga de partidas ganadas seguidas.
- **Opción 4 · Cajero:** un cajero con saldo inicial de 100 € y un submenú en bucle para consultar, ingresar y retirar (sin quedar en negativo).

---
# Parte A · Diagramas de flujo

**Antes de escribir código**, dibuja en [draw.io](https://app.diagrams.net) **dos diagramas**:

1. El **menú principal**: el bucle que repite el menú, la lectura de la opción, una rama por cada caso del `match` y la salida del bucle.
2. El **detalle de Adivina el número**: elección del nivel (con su bucle de validación), el bucle de intentos, la validación de cada intento y las dos formas de terminar (acertar o quedarse sin intentos).

Recuerda que cada bucle se dibuja como una **decisión con una flecha que vuelve atrás**. Para el `for` de los intentos, dibuja el contador (`intento = 1`, la condición `intento <= max_intentos` e `intento += 1`).

Expórtalos como imagen (*Archivo → Exportar como → PNG*) y guárdalos en la carpeta `diagramas/` con los nombres `menu.png` y `adivina.png`.

---
# Parte B · Código

Escribe el programa completo en `sala_de_juegos.py`, debajo de las líneas de partida. Ejecútalo en PyCharm (botón ▶) y juega para probar cada opción.

---
# Parte C · Pruebas

Ejecuta el programa con **al menos 12 casos** (como mínimo uno por opción, uno por cada error de validación y los casos límite: números 1 y máximo del nivel, número repetido, quedarse sin intentos, empate, al mejor de 5…). Pon `MODO_PRUEBA = True` para saber el número secreto y la jugada del ordenador. Completa la tabla de `PRUEBAS.md` con lo que muestra tu programa.

---
# Parte D · Hacia las funciones

Responde en `REFLEXION.md` a las tres preguntas que encontrarás allí.

---
## Comprobaciones automáticas

Cada vez que haces *push*, GitHub Actions ejecuta `test_sala_de_juegos.py`, que **juega por ti**:
escribe en el menú, fija el número secreto y la jugada del ordenador, y comprueba que tu programa
muestra los mensajes del enunciado. También revisa los requisitos de código (sin `def`, `match-case`,
`for-else`, comprensiones…) y que estén los archivos de las partes A, C y D.

- Puedes lanzarlas tú en PyCharm: clic derecho en `test_sala_de_juegos.py` → **Run 'pytest in test_sala…'**.
- Una comprobación en verde **no es la nota**: los diagramas, la tabla de pruebas, la reflexión y el estilo los revisa el profesor.
- Los mensajes deben coincidir **exactamente** con los de los ejemplos (tildes, signos ¡ ! y espacios incluidos).

## Antes de entregar

1. Comprueba que `diagramas/menu.png` y `diagramas/adivina.png` se ven en GitHub.
2. Pon `MODO_PRUEBA = False`, ejecuta el programa y juega al menos una partida de cada juego.
3. Completa `PRUEBAS.md` y `REFLEXION.md`.
4. *Commit and Push* y revisa la pestaña **Actions**.
