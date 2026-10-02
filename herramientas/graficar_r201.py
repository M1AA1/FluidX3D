"""Graficos del caso CASO_R201 (tanque tipo R-201, exploratorio).

Uso:  python herramientas/graficar_r201.py <carpeta con r201_plano.csv y r201_fondo.csv>
Requiere numpy y matplotlib. Escribe r201_plano.png y r201_fondo.png en la misma carpeta.

Los campos son velocidades medias en el tiempo normalizadas por la velocidad de punta de pala.
El caso se basa en supuestos de geometria y operacion, no en datos de proceso del R-201.
"""
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.patches import Circle
from matplotlib.colors import LinearSegmentedColormap

# rampa secuencial de un solo tono (azul, claro = cerca de cero, oscuro = alto)
AZUL = ["#cde2fb", "#b7d3f6", "#9ec5f4", "#86b6ef", "#6da7ec", "#5598e7", "#3987e5",
        "#2a78d6", "#256abf", "#1c5cab", "#184f95", "#104281", "#0d366b"]
CMAP = LinearSegmentedColormap.from_list("azul_secuencial", AZUL)
CMAP.set_bad("#8f8e8a")  # solidos: gris neutro
TINTA, TINTA_2 = "#1f1e1c", "#5f5e5a"
NOTA = "Exploratorio: geometría y operación supuestas (H = T, D = T/3, C = T/3, 4 deflectores, palas a 45°); no son datos de proceso del R-201."

plt.rcParams.update({"font.size": 10, "text.color": TINTA, "axes.labelcolor": TINTA_2,
                     "xtick.color": TINTA_2, "ytick.color": TINTA_2, "axes.edgecolor": "#c9c8c4"})


def leer(ruta):
    datos = np.genfromtxt(ruta, delimiter=",", skip_header=1, names=True)  # la primera linea es un comentario descriptivo
    return datos


def malla(a, b, *campos):
    ua, ub = np.unique(a), np.unique(b)
    ia, ib = np.searchsorted(ua, a), np.searchsorted(ub, b)
    salida = []
    for c in campos:
        m = np.full((ub.size, ua.size), np.nan)
        m[ib, ia] = c
        salida.append(m)
    # la malla de FluidX3D es uniforme; el CSV redondea a 4 decimales y streamplot exige espaciado exacto
    return np.linspace(ua[0], ua[-1], ua.size), np.linspace(ub[0], ub[-1], ub.size), salida


def plano(carpeta):
    d = leer(carpeta / "r201_plano.csv")
    r, z, (ur, uz, sol) = malla(d["r_T"], d["z_H"], d["u_r"], d["u_z"], d["solido"])
    mag = np.hypot(ur, uz)
    solido = sol > 0.5
    mag_m = np.ma.masked_where(solido, mag)
    fig, ax = plt.subplots(figsize=(6.4, 6.6), layout="constrained")
    im = ax.pcolormesh(r, z, mag_m, cmap=CMAP, vmin=0.0, vmax=float(np.nanmax(mag_m)), shading="nearest")
    ur_s, uz_s = np.where(solido, 0.0, ur), np.where(solido, 0.0, uz)
    sl = ax.streamplot(r, z, ur_s, uz_s, density=1.4, color=TINTA, linewidth=0.7, arrowsize=0.7)
    sl.lines.set_path_effects([pe.Stroke(linewidth=2.0, foreground="white", alpha=0.7), pe.Normal()])
    ax.set_aspect("equal")
    ax.set_xlim(r.min(), r.max()); ax.set_ylim(0, 1)
    ax.set_xlabel("r / T"); ax.set_ylabel("z / H")
    ax.set_title("Velocidad media en el plano vertical por el eje\n(a medio camino entre deflectores; eje en gris)", loc="left", fontsize=11)
    cb = fig.colorbar(im, ax=ax, shrink=0.8)
    cb.set_label("|(u_r, u_z)| / u_punta"); cb.outline.set_visible(False)
    fig.get_layout_engine().set(rect=(0, 0.06, 1, 0.94))  # franja inferior para la nota
    fig.text(0.01, 0.01, NOTA, fontsize=7.5, color=TINTA_2, wrap=True)
    fig.savefig(carpeta / "r201_plano.png", dpi=160)
    plt.close(fig)


def fondo(carpeta):
    d = leer(carpeta / "r201_fondo.csv")
    x, y, (uh, sol) = malla(d["x_T"], d["y_T"], d["u_h"], d["solido"])
    uh_m = np.ma.masked_where(np.isnan(uh) | (sol > 0.5), uh)
    fig, ax = plt.subplots(figsize=(6.2, 5.6), layout="constrained")
    im = ax.pcolormesh(x, y, uh_m, cmap=CMAP, vmin=0.0, vmax=float(uh_m.max()), shading="nearest")
    borde = Circle((0, 0), 0.5, transform=ax.transData, facecolor="none", edgecolor="#8f8e8a", linewidth=1.0)
    ax.add_patch(borde)
    im.set_clip_path(borde)  # fuera del tanque no hay datos; en gris quedan solo los deflectores
    ax.set_aspect("equal"); ax.set_xlim(-0.52, 0.52); ax.set_ylim(-0.52, 0.52)
    ax.set_xlabel("x / T"); ax.set_ylabel("y / T")
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)
    ax.set_title("Velocidad horizontal media junto al fondo\n(vista en planta; deflectores en gris)", loc="left", fontsize=11)
    cb = fig.colorbar(im, ax=ax, shrink=0.8)
    cb.set_label("|u_horizontal| / u_punta"); cb.outline.set_visible(False)
    fig.get_layout_engine().set(rect=(0, 0.06, 1, 0.94))
    fig.text(0.01, 0.01, NOTA, fontsize=7.5, color=TINTA_2, wrap=True)
    fig.savefig(carpeta / "r201_fondo.png", dpi=160)
    plt.close(fig)


if __name__ == "__main__":
    carpeta = Path(sys.argv[1] if len(sys.argv) > 1 else "bin")
    plano(carpeta)
    fondo(carpeta)
    print("graficos en", carpeta)
