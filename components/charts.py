import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from utils.helpers import PERFORMANCE_COLORS, PERFORMANCE_LABELS

# ── Global dark style ─────────────────────────────────────────
_dark = {
    "figure.facecolor":  "#0D001F",
    "axes.facecolor":    "#0D001F",
    "axes.edgecolor":    "#1E0A3A",
    "axes.labelcolor":   "#64748B",
    "xtick.color":       "#475569",
    "ytick.color":       "#475569",
    "text.color":        "#E2E8F0",
    "grid.color":        "#1E0A3A",
    "grid.alpha":        0.6,
    "font.family":       "sans-serif",
}
plt.rcParams.update(_dark)

_GRAD = ["#7C3AED", "#8B5CF6", "#4F8CFF", "#22D3EE"]


def _fig(w=6, h=3.8):
    fig, ax = plt.subplots(figsize=(w, h))
    fig.patch.set_facecolor("#0D001F")
    ax.set_facecolor("#0D001F")
    return fig, ax


def confidence_bar_chart(classes, probabilities):
    labels = [PERFORMANCE_LABELS[c] for c in classes]
    colors = [PERFORMANCE_COLORS[c] for c in classes]
    fig, ax = _fig(5.5, 3)
    bars = ax.barh(labels, probabilities, color=colors, height=0.45, edgecolor="none")
    ax.set_xlim(0, 1)
    ax.set_title("Prediction Confidence", color="#C4B5FD", fontsize=12, pad=10, fontweight="bold")
    ax.spines[:].set_visible(False)
    ax.xaxis.grid(True, color="#1E0A3A", linewidth=0.8)
    ax.set_axisbelow(True)
    for bar, val in zip(bars, probabilities):
        ax.text(val + 0.01, bar.get_y() + bar.get_height() / 2,
                f"{val:.0%}", va="center", fontsize=11, color="#E2E8F0", fontweight="600")
    fig.tight_layout(pad=1.5)
    return fig


def performance_distribution_chart(df: pd.DataFrame):
    mapping = {1: "Low", 2: "Good", 3: "Excellent", 4: "Outstanding"}
    colors  = [PERFORMANCE_COLORS[k] for k in [1,2,3,4]]
    counts  = df["PerformanceRating"].map(mapping).value_counts()
    counts  = counts.reindex(["Low", "Good", "Excellent", "Outstanding"])
    fig, ax = _fig(6.5, 4)
    bars = ax.bar(counts.index, counts.values, color=colors, width=0.5,
                  edgecolor="none", zorder=2)
    ax.set_ylabel("Employees", color="#64748B", fontsize=11)
    ax.spines[:].set_visible(False)
    ax.yaxis.grid(True, color="#1E0A3A", linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    for bar, val in zip(bars, counts.values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 2,
                str(val), ha="center", fontsize=12, fontweight="bold", color="#E2E8F0")
    fig.tight_layout(pad=1.5)
    return fig


def feature_importance_chart(model, feature_columns):
    imp = pd.Series(model.feature_importances_, index=feature_columns).sort_values()
    fig, ax = _fig(6.5, 4.5)
    colors = plt.cm.cool([x / max(imp) for x in imp])
    ax.barh(imp.index, imp.values, color=colors, height=0.55, edgecolor="none", zorder=2)
    ax.set_xlabel("Importance Score", color="#64748B", fontsize=11)
    ax.spines[:].set_visible(False)
    ax.xaxis.grid(True, color="#1E0A3A", linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    fig.tight_layout(pad=1.5)
    return fig


def correlation_heatmap(df: pd.DataFrame):
    numeric = df.select_dtypes("number")
    fig, ax = _fig(7.5, 5.5)
    sns.heatmap(
        numeric.corr(), annot=True, fmt=".2f",
        cmap=sns.color_palette("rocket_r", as_cmap=True),
        ax=ax, linewidths=0.5, linecolor="#1A063A",
        annot_kws={"size": 9, "color": "#E2E8F0"},
        cbar_kws={"shrink": 0.8},
    )
    ax.tick_params(colors="#94A3B8", labelsize=9)
    fig.tight_layout(pad=1.5)
    return fig


def department_avg_chart(df: pd.DataFrame):
    dept_avg = df.groupby("Department")["PerformanceRating"].mean().sort_values()
    fig, ax  = _fig(6.5, 4)
    colors   = plt.cm.plasma([x / 4 for x in dept_avg.values])
    bars     = ax.barh(dept_avg.index, dept_avg.values, color=colors, height=0.45, edgecolor="none", zorder=2)
    ax.set_xlim(0, 4.3)
    ax.set_xlabel("Avg Rating", color="#64748B", fontsize=11)
    ax.spines[:].set_visible(False)
    ax.xaxis.grid(True, color="#1E0A3A", linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    for i, val in enumerate(dept_avg.values):
        ax.text(val + 0.06, i, f"{val:.2f}", va="center", fontsize=11,
                color="#E2E8F0", fontweight="600")
    fig.tight_layout(pad=1.5)
    return fig


def salary_vs_performance(df: pd.DataFrame):
    colors = [PERFORMANCE_COLORS[r] for r in df["PerformanceRating"]]
    fig, ax = _fig(6.5, 4)
    ax.scatter(df["MonthlyIncome"], df["PerformanceRating"],
               c=colors, alpha=0.55, s=28, edgecolors="none", zorder=2)
    ax.set_xlabel("Monthly Income (Rs.)", color="#64748B", fontsize=11)
    ax.set_ylabel("Performance Rating", color="#64748B", fontsize=11)
    ax.spines[:].set_visible(False)
    ax.grid(True, color="#1E0A3A", linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    fig.tight_layout(pad=1.5)
    return fig
