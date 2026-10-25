# P2 · Sala de juegos
# Autor/a:

import random

# Constantes
MODO_PRUEBA = False   # True: muestra el número secreto y la jugada del ordenador
JUGADAS = ["piedra", "papel", "tijera"]
GANA_A = {"piedra": "tijera", "papel": "piedra", "tijera": "papel"}   # clave gana a valor

# Datos que se guardan entre partidas
historial = []         # una tupla por partida: (juego, ganada, intentos_o_rondas)
jugadas_usuario = []   # todas tus jugadas de piedra, papel o tijera

# Tu programa empieza aquí
