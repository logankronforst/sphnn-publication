#!/usr/bin/env python3
from pathlib import Path
import sys

import numpy as np
from scipy.io import loadmat

import matplotlib
matplotlib.use("Agg")
from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes, mark_inset


PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = PROJECT_DIR / "data" / "cascaded_tanks" / "dataBenchmark.mat"
OUT_DIR = PROJECT_DIR / "experiments" / "cascaded_tanks" / "figures"
OUT_FILE = OUT_DIR / "cascaded_tanks_dataset.png"

if not DATA_FILE.exists():
    raise FileNotFoundError(f"Missing dataset at {DATA_FILE}")

sys.path.append(str(PROJECT_DIR))
from util import colors


SMALL_SIZE = 7
MEDIUM_SIZE = 8
BIGGER_SIZE = 10

plt.rc("font", size=SMALL_SIZE)
plt.rc("axes", titlesize=BIGGER_SIZE)
plt.rc("axes", labelsize=MEDIUM_SIZE)
plt.rc("xtick", labelsize=SMALL_SIZE)
plt.rc("ytick", labelsize=SMALL_SIZE)
plt.rc("legend", fontsize=MEDIUM_SIZE)
plt.rc("figure", titlesize=BIGGER_SIZE)

colors.set_custom_cycle()

PLOT_DPI = 200

data = loadmat(DATA_FILE)
ys_train = np.expand_dims(np.stack(data["yEst"], axis=0), axis=0)
us_train = np.expand_dims(np.stack(data["uEst"], axis=0), axis=0)
ys_vali = np.expand_dims(np.stack(data["yVal"], axis=0), axis=0)
us_vali = np.expand_dims(np.stack(data["uVal"], axis=0), axis=0)
ts = 4.0 * np.arange(ys_train.shape[1])

plot_kwargs = {"lw": 1}
y_kwargs = {
    "color": colors.theme_colors["lightblue"],
    "label": "Sensor output $y$",
} | plot_kwargs
u_kwargs = {
    "color": colors.theme_colors["black"],
    "label": "Pump speed $u$",
    "ls": "--",
} | plot_kwargs
axis_kwargs = {
    "xlabel": "$t / s$",
    "xlim": [ts.min(), ts.max()],
    "ylim": [0, 10.5],
}

fig, axes = plt.subplots(
    1,
    2,
    figsize=(6, 2),
    dpi=PLOT_DPI,
    sharey="row",
    gridspec_kw={"wspace": 0.1},
)

y_line, = axes[0].plot(ts, ys_train[0, :, 0].T, **y_kwargs)
u_line, = axes[0].plot(ts, us_train[0, :, 0].T, **u_kwargs)
axes[0].set(
    title="Training trajectory",
    ylabel="$u, y / V$",
    **axis_kwargs,
)
axes[1].plot(ts, ys_vali[0, :, 0].T, **y_kwargs)
axes[1].plot(ts, us_vali[0, :, 0].T, **u_kwargs)
axes[1].set(title="Test trajectory", **axis_kwargs)

axins = zoomed_inset_axes(
    axes[0],
    zoom=4,
    loc="upper center",
    bbox_to_anchor=(0.6, 0.95),
    bbox_transform=axes[0].transAxes,
)
axins.plot(ts, ys_train[0, :, 0].T, **y_kwargs)
axins.set(xlim=[3450, 3750], ylim=[9.3, 10.1], xticks=[], yticks=[])
mark_inset(axes[0], axins, loc1=2, loc2=4, fc="none", ec="0.5", lw=1.5)

fig.patch.set_alpha(0.0)
plt.legend(
    handles=[u_line, y_line],
    loc="upper center",
    bbox_to_anchor=(0.5, -0.08),
    bbox_transform=fig.transFigure,
    fancybox=True,
    shadow=False,
    ncol=2,
)

OUT_DIR.mkdir(parents=True, exist_ok=True)
fig.savefig(OUT_FILE, dpi=PLOT_DPI, bbox_inches="tight", transparent=True)
print(f"Saved dataset figure to {OUT_FILE}")
