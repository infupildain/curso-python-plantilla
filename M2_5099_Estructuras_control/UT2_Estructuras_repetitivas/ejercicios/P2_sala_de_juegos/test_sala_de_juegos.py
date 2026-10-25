"""Comprobaciones automáticas de la práctica P2 · Sala de juegos.

Cómo funcionan:
  * El programa del alumno se ejecuta entero, como si se pulsara ▶ en PyCharm.
  * `input()` se sustituye por una lista de respuestas preparadas (lo que "teclea" el test).
  * `random.randint` y `random.choice` se sustituyen para fijar el número secreto
    y la jugada del ordenador, así el resultado es siempre el mismo.
  * Se comprueba que en la salida aparecen los mensajes del enunciado.

Por defecto se prueba ./sala_de_juegos.py (el del alumno).
Con la variable de entorno USAR_SOLUCION=1 se prueba solucion/sala_de_juegos.py.
"""
import ast
import os
import random
import re
import runpy
from pathlib import Path

import pytest

AQUI = Path(__file__).parent
BASE = AQUI / "solucion" if os.environ.get("USAR_SOLUCION") == "1" else AQUI
PROGRAMA = BASE / "sala_de_juegos.py"


class EntradaAgotada(Exception):
    pass


def jugar(monkeypatch, capsys, entradas, secretos=(), ordenador=()):
    """Ejecuta el programa con esas entradas y devuelve todo lo que se ha visto en pantalla.

    El "transcript" incluye cada pregunta de input() seguida de la respuesta del test,
    igual que se vería en la consola de PyCharm.
    """
    entradas, secretos, ordenador = list(entradas), list(secretos), list(ordenador)

    def falso_input(mensaje=""):
        if not entradas:
            raise EntradaAgotada(
                "El programa ha pedido más datos de los previstos. "
                "¿Falta salir del menú, o un dato inválido gasta intento/ronda?"
            )
        respuesta = entradas.pop(0)
        print(f"{mensaje}{respuesta}")
        return respuesta

    def falso_randint(a, b):
        assert secretos, "El programa ha pedido más números aleatorios de los previstos."
        return secretos.pop(0)

    def falso_choice(seq):
        assert ordenador, "El programa ha pedido más jugadas del ordenador de las previstas."
        return ordenador.pop(0)

    monkeypatch.setattr("builtins.input", falso_input)
    monkeypatch.setattr(random, "randint", falso_randint)
    monkeypatch.setattr(random, "choice", falso_choice)

    try:
        runpy.run_path(str(PROGRAMA), run_name="__main__")
    except EntradaAgotada as e:
        salida = capsys.readouterr().out
        pytest.fail(f"{e}\n\n--- Lo que se vio en pantalla ---\n{salida}")
    return capsys.readouterr().out


def contiene(salida, *lineas):
    """Comprueba que cada línea esperada aparece en la salida (ignorando espacios de los extremos)."""
    vistas = [l.strip() for l in salida.splitlines()]
    for esperada in lineas:
        assert esperada in vistas, (
            f"No aparece la línea:\n    {esperada!r}\n\n--- Lo que se vio en pantalla ---\n{salida}"
        )


# --------------------------------------------------------------------------------------
# 1. Menú (1 punto)
# --------------------------------------------------------------------------------------

def test_menu_se_muestra(monkeypatch, capsys):
    salida = jugar(monkeypatch, capsys, ["0"])
    contiene(salida, "=== SALA DE JUEGOS ===", "1. Adivina el número",
             "2. Piedra, papel o tijera", "3. Estadísticas", "0. Salir")


@pytest.mark.parametrize("salir", ["0", "s", "salir", "SALIR", "  s  "])
def test_formas_de_salir(monkeypatch, capsys, salir):
    salida = jugar(monkeypatch, capsys, [salir])
    contiene(salida, "¡Hasta pronto! Has jugado 0 partidas.")


def test_opcion_no_valida_vuelve_al_menu(monkeypatch, capsys):
    salida = jugar(monkeypatch, capsys, ["x", "7", "0"])
    assert salida.count("Opción no válida.") == 2, salida
    assert salida.count("=== SALA DE JUEGOS ===") == 3, "El menú debe volver a mostrarse"


def test_estadisticas_sin_partidas(monkeypatch, capsys):
    salida = jugar(monkeypatch, capsys, ["3", "0"])
    contiene(salida, "Todavía no has jugado ninguna partida.")


# --------------------------------------------------------------------------------------
# 2. Adivina el número (2 puntos)
# --------------------------------------------------------------------------------------

def test_adivina_ejemplo_del_enunciado(monkeypatch, capsys):
    """Reproduce el ejemplo de ejecución del enunciado (secreto = 7, nivel fácil)."""
    salida = jugar(
        monkeypatch, capsys,
        ["1", "x", "f", "25", "doce", "12", "12", "6", "9", "7", "0"],
        secretos=[7],
    )
    contiene(
        salida,
        "Nivel no válido.",
        "He pensado un número del 1 al 50. Tienes 8 intentos.",
        "El número secreto es menor que 25.",
        "Escribe un número entero del 1 al 50.",
        "El número secreto es menor que 12.",
        "Ya habías dicho ese número.",
        "El número secreto es mayor que 6.",
        "El número secreto es menor que 9.",
        "¡Acertaste en 5 intentos!",
        "¡Hasta pronto! Has jugado 1 partidas.",
    )


@pytest.mark.parametrize(
    "nivel, maximo, intentos",
    [("f", 50, 8), ("Fácil", 50, 8), ("facil", 50, 8),
     ("n", 100, 7), (" NORMAL ", 100, 7),
     ("d", 500, 9), ("difícil", 500, 9), ("dificil", 500, 9)],
)
def test_adivina_niveles(monkeypatch, capsys, nivel, maximo, intentos):
    salida = jugar(monkeypatch, capsys, ["1", nivel, "1", "0"], secretos=[1])
    contiene(salida, f"He pensado un número del 1 al {maximo}. Tienes {intentos} intentos.",
             "¡Acertaste en 1 intentos!")


def test_adivina_limites_del_rango(monkeypatch, capsys):
    """0 y 51 no valen (ni gastan intento); 1 y 50 sí."""
    salida = jugar(monkeypatch, capsys, ["1", "f", "0", "51", "-3", "1", "50", "0"], secretos=[50])
    assert salida.count("Escribe un número entero del 1 al 50.") == 3, salida
    contiene(salida, "El número secreto es mayor que 1.", "¡Acertaste en 2 intentos!")


def test_adivina_quedarse_sin_intentos(monkeypatch, capsys):
    """Nivel normal: 7 fallos terminan la partida (for-else) y cuenta como perdida."""
    fallos = [str(n) for n in range(1, 8)]
    salida = jugar(monkeypatch, capsys, ["1", "n", *fallos, "3", "0"], secretos=[100])
    assert "Intento 8/7" not in salida, "No puede haber un octavo intento en nivel normal"
    contiene(salida, "Partidas: 1 · ganadas: 0 (0 %)", "Resultados: P")


# --------------------------------------------------------------------------------------
# 3. Piedra, papel o tijera (1,5 puntos)
# --------------------------------------------------------------------------------------

def test_ppt_ejemplo_del_enunciado(monkeypatch, capsys):
    salida = jugar(
        monkeypatch, capsys,
        ["2", "4", "3", "Piedra", "papel", "lagarto", "tijera", "papel", "0"],
        ordenador=["tijera", "papel", "piedra", "piedra"],
    )
    contiene(
        salida,
        "Escribe 3 o 5.",
        "Ordenador: tijera → ganas la ronda. Marcador: 1-0",
        "Ordenador: papel → empate. Marcador: 1-0",
        "Jugada no válida.",
        "Ordenador: piedra → gana el ordenador. Marcador: 1-1",
        "Ordenador: piedra → ganas la ronda. Marcador: 2-1",
        "¡Has ganado la partida!",
    )


def test_ppt_al_mejor_de_5_los_empates_no_suman(monkeypatch, capsys):
    salida = jugar(
        monkeypatch, capsys,
        ["2", "5", "piedra", "piedra", " PAPEL ", "papel", "papel", "0"],
        ordenador=["piedra", "tijera", "papel", "piedra", "piedra"],
    )
    contiene(salida, "Ordenador: piedra → empate. Marcador: 0-0",
             "Ordenador: papel → empate. Marcador: 1-0",
             "Ordenador: piedra → ganas la ronda. Marcador: 3-0",
             "¡Has ganado la partida!")
    assert "Ronda 6" not in salida, "La partida debe terminar al llegar a 3 victorias"


# --------------------------------------------------------------------------------------
# 4. Estadísticas (1 punto)
# --------------------------------------------------------------------------------------

def test_estadisticas_ejemplo_del_enunciado(monkeypatch, capsys):
    """5 partidas: Adivina G (6 int.), PPT G, Adivina G (7 int.), PPT P, Adivina G (5 int.)."""
    entradas = (
        ["1", "f", "1", "2", "3", "4", "5", "10"]               # 1 · adivina, 6 intentos
        + ["2", "3", "papel", "papel"]                          # 2 · ppt ganada
        + ["1", "f", "1", "2", "3", "4", "5", "6", "10"]        # 3 · adivina, 7 intentos
        + ["2", "3", "piedra", "tijera", "tijera"]              # 4 · ppt perdida
        + ["1", "f", "1", "2", "3", "4", "10"]                  # 5 · adivina, 5 intentos
        + ["3", "0"]
    )
    salida = jugar(
        monkeypatch, capsys, entradas,
        secretos=[10, 10, 10],
        ordenador=["piedra", "piedra", "piedra", "piedra", "piedra"],
    )
    contiene(
        salida,
        "=== ESTADÍSTICAS ===",
        "Partidas: 5 · ganadas: 4 (80 %)",
        "Resultados: G G G P G",
        "Adivina el número · partidas: 3 · ganadas: 3",
        "Piedra, papel o tijera · partidas: 2 · ganadas: 1",
        "Mejor partida de Adivina: la nº 5 (5 intentos)",
        "Tus jugadas: piedra 1, papel 2, tijera 2",
        "Tu jugada favorita: papel",
    )


def test_estadisticas_solo_ppt_no_muestra_mejor_adivina(monkeypatch, capsys):
    salida = jugar(monkeypatch, capsys, ["2", "3", "tijera", "tijera", "3", "0"],
                   ordenador=["papel", "papel"])
    assert "Mejor partida de Adivina" not in salida, salida
    contiene(salida, "Tu jugada favorita: tijera")


def test_estadisticas_solo_adivina_no_muestra_jugadas(monkeypatch, capsys):
    salida = jugar(monkeypatch, capsys, ["1", "f", "3", "3", "0"], secretos=[3])
    assert "Tus jugadas" not in salida and "favorita" not in salida, salida
    contiene(salida, "Mejor partida de Adivina: la nº 1 (1 intentos)")


# --------------------------------------------------------------------------------------
# 5. Requisitos de código (revisión automática del código fuente)
# --------------------------------------------------------------------------------------

@pytest.fixture(scope="module")
def arbol():
    return ast.parse(PROGRAMA.read_text(encoding="utf-8"))


def _nodos(arbol, tipo):
    return [n for n in ast.walk(arbol) if isinstance(n, tipo)]


def test_sin_def_ni_try(arbol):
    assert not _nodos(arbol, (ast.FunctionDef, ast.Lambda)), "Todavía no se usan funciones (def)"
    assert not _nodos(arbol, ast.Try), "La validación se hace sin try/except"


def test_usa_while_y_match(arbol):
    assert _nodos(arbol, ast.While), "El menú debe ser un bucle while"
    assert _nodos(arbol, ast.Match), "Las opciones se resuelven con match-case"


def test_for_con_range_y_else(arbol):
    ok = [f for f in _nodos(arbol, ast.For)
          if f.orelse and isinstance(f.iter, ast.Call) and getattr(f.iter.func, "id", "") == "range"]
    assert ok, "Debe haber al menos un for ... in range(...) con su else"


def test_tres_comprensiones(arbol):
    listas = _nodos(arbol, (ast.ListComp, ast.GeneratorExp, ast.SetComp))
    assert any(g.ifs for c in listas for g in c.generators), "Falta una comprensión con filtro (if)"
    assert any(isinstance(c.elt, ast.IfExp) for c in listas), \
        "Falta una comprensión con expresión condicional (x if ... else y)"
    assert _nodos(arbol, ast.DictComp), "Falta una comprensión de diccionario"


def test_sin_min_ni_max(arbol):
    usadas = {n.func.id for n in _nodos(arbol, ast.Call) if isinstance(n.func, ast.Name)}
    assert not usadas & {"min", "max"}, "Máximo y mínimo se calculan con el algoritmo clásico"


def test_entrega_con_modo_prueba_false():
    texto = PROGRAMA.read_text(encoding="utf-8")
    assert re.search(r"^MODO_PRUEBA\s*=\s*False", texto, re.M), "Entrega con MODO_PRUEBA = False"


# --------------------------------------------------------------------------------------
# 6. Partes A, C y D presentes (el contenido lo revisa el profesor)
# --------------------------------------------------------------------------------------

@pytest.mark.parametrize("diagrama", ["menu.png", "adivina.png"])
def test_parte_a_diagramas(diagrama):
    assert (BASE / "diagramas" / diagrama).is_file(), f"Falta diagramas/{diagrama}"


def test_parte_c_tabla_de_pruebas_rellenada():
    filas = [l for l in (BASE / "PRUEBAS.md").read_text(encoding="utf-8").splitlines()
             if re.match(r"^\|\s*\d+\s*\|", l)]
    # columna 5 = "Resultado obtenido"
    rellenas = [f for f in filas if len(f.split("|")) > 5 and f.split("|")[5].strip()]
    assert len(rellenas) >= 12, f"PRUEBAS.md: hay {len(rellenas)} casos con resultado obtenido (mínimo 12)"


def test_parte_d_reflexion_respondida():
    texto = (BASE / "REFLEXION.md").read_text(encoding="utf-8")
    respuestas = texto.split("## Tus respuestas")[-1] if "## Tus respuestas" in texto else texto
    huecos = re.findall(r"^\s*\d\.\s*$", respuestas, re.M)
    assert not huecos and len(respuestas.strip()) > 40, "Responde las tres preguntas de REFLEXION.md"
