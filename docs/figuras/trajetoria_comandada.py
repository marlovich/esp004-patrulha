"""Trajetória comandada pelo PatrolNode sob um modelo cinemático ideal.

Reproduz a lógica discreta do nó (controle a 10 Hz, integração do último
comando) e integra o modelo de uniciclo, supondo que a base executa os
comandos de /cmd_vel sem erro. Não depende do ROS 2.

Uso:  python3 trajetoria_comandada.py
Gera: trajetoria_comandada.png (na mesma pasta do script)
"""
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Parâmetros do PatrolNode
VEL_LINEAR = 0.3     # m/s
VEL_ANGULAR = 0.785  # rad/s
DIST_LADO = 2.0      # m
N_LADOS = 4
T = 0.1              # período de controle (s)

AZUL, CINZA, TINTA, TINTA_2, FUNDO = "#2a78d6", "#8a8984", "#0b0b0b", "#52514e", "#fcfcfb"


def simular():
    """Devolve os pontos (x, y) da trajetória e a orientação final (rad)."""
    n_lado = math.ceil(DIST_LADO / (VEL_LINEAR * T) - 1e-9)       # períodos avançando
    n_giro = math.ceil((math.pi / 2) / (VEL_ANGULAR * T) - 1e-9)  # períodos girando
    x = y = theta = 0.0
    pontos = [(x, y)]
    for _ in range(N_LADOS):
        for _ in range(n_lado):
            x += VEL_LINEAR * T * math.cos(theta)
            y += VEL_LINEAR * T * math.sin(theta)
            pontos.append((x, y))
        theta += n_giro * VEL_ANGULAR * T
    return pontos, theta, n_lado, n_giro


def main():
    pontos, theta, n_lado, n_giro = simular()
    xs, ys = zip(*pontos)
    erro = math.hypot(xs[-1], ys[-1])
    giro = math.degrees(n_giro * VEL_ANGULAR * T)

    print(f"Períodos por lado: {n_lado}  ->  {n_lado * VEL_LINEAR * T:.2f} m")
    print(f"Períodos por giro: {n_giro}  ->  {giro:.2f} graus")
    print(f"Erro de fechamento: {erro:.3f} m")
    print(f"Erro de orientação final: {math.degrees(theta) - 360:.2f} graus")

    fig, ax = plt.subplots(figsize=(7.2, 6.0), dpi=160)
    fig.patch.set_facecolor(FUNDO)
    ax.set_facecolor(FUNDO)

    q = DIST_LADO
    ax.plot([0, q, q, 0, 0], [0, 0, q, q, 0], color=CINZA, lw=1.2, ls=(0, (4, 3)),
            label="Quadrado ideal (2 m)", zorder=1)
    ax.plot(xs, ys, color=AZUL, lw=2, solid_capstyle="round",
            label="Trajetória comandada", zorder=2)

    ax.plot(0, 0, "o", ms=8, color=TINTA, mec=FUNDO, mew=2, zorder=4)
    ax.plot(xs[-1], ys[-1], "o", ms=8, color=AZUL, mec=FUNDO, mew=2, zorder=4)
    ax.annotate("Partida", (0, 0), xytext=(-10, 10), textcoords="offset points",
                ha="right", color=TINTA, fontsize=10)
    ax.annotate(f"Chegada\nerro de fechamento: {erro:.2f} m".replace(".", ","), (xs[-1], ys[-1]),
                xytext=(12, -6), textcoords="offset points", va="top",
                color=TINTA, fontsize=10)
    ax.annotate(f"{giro:.1f}° por giro".replace(".", ","), (q + 0.01, 0), xytext=(12, 14),
                textcoords="offset points", color=TINTA_2, fontsize=10)

    ax.set_aspect("equal")
    ax.set_xlim(-0.75, 3.1)
    ax.set_ylim(-0.75, 2.5)
    ax.set_xlabel("x (m)", color=TINTA_2)
    ax.set_ylabel("y (m)", color=TINTA_2)
    ax.set_title("Trajetória comandada e quadrado ideal", loc="left",
                 color=TINTA, fontsize=12, fontweight="bold", pad=12)
    ax.grid(True, color="#e4e3df", lw=0.8)
    ax.set_axisbelow(True)
    ax.tick_params(colors=TINTA_2, length=0)
    for lado in ax.spines.values():
        lado.set_visible(False)
    ax.legend(loc="upper right", frameon=False, fontsize=9, labelcolor=TINTA_2)

    saida = Path(__file__).with_name("trajetoria_comandada.png")
    fig.savefig(saida, facecolor=FUNDO, bbox_inches="tight")
    print(f"Figura salva em {saida}")


if __name__ == "__main__":
    main()
