"""Schematic figures for the report: process route, research framework, Gantt chart, timeline."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, FancyArrowPatch, Polygon
from common import C, INK, INK2, SEQ, savefig

rng = np.random.default_rng(5)

def crystals(ax, x0, x1, y0, y1, d, n, color, exclude=None):
    xs = rng.uniform(x0, x1, n); ys = rng.uniform(y0, y1, n)
    for x, y in zip(xs, ys):
        if exclude and exclude[0] < x < exclude[1]: continue
        ax.add_patch(Circle((x, y), d, color=color, lw=0))

def process_route():
    fig, axs = plt.subplots(1, 5, figsize=(15, 3.9))
    titles = ["① 成核态前驱体\n（纳米晶<50 nm，透明）", "② 贝塞尔飞秒线聚焦改性\n（非晶化/缺陷径迹）", "③ HF/KOH 选择性刻蚀\n（相衬度放大选择比）",
              "④ 晶化长大+相环构筑\n（增韧、CTE调控、饱和晶化）", "⑤ 种子层+电镀Cu+RDL\n（全填/共形，界面粘结）"]
    for k, ax in enumerate(axs):
        ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off"); ax.set_title(titles[k], fontsize=9.5)
        ax.add_patch(Rectangle((0.5, 1), 9, 7, facecolor="#eef4fc", edgecolor=INK2, lw=1))
        if k == 0:
            crystals(ax, 0.6, 9.4, 1.1, 7.9, 0.06, 900, SEQ[3])
        elif k == 1:
            crystals(ax, 0.6, 9.4, 1.1, 7.9, 0.06, 900, SEQ[3], exclude=(4.8, 5.2))
            ax.add_patch(Rectangle((4.85, 1), 0.3, 7, color=C[1], alpha=0.8, lw=0))
            ax.add_patch(Polygon([[3.2, 10], [6.8, 10], [5.05, 8.05], [4.95, 8.05]], color=C[1], alpha=0.25, lw=0))
            ax.text(5, 9.1, "fs Bessel", ha="center", fontsize=8, color=C[1])
        elif k == 2:
            crystals(ax, 0.6, 9.4, 1.1, 7.9, 0.06, 900, SEQ[3], exclude=(3.6, 6.4))
            ax.add_patch(Polygon([[3.7, 8], [6.3, 8], [5.6, 1], [4.4, 1]], facecolor="white", edgecolor=INK2, lw=1))
            ax.text(5, 4.5, "via", ha="center", fontsize=9, color=INK2)
        elif k == 3:
            crystals(ax, 0.6, 9.4, 1.1, 7.9, 0.16, 330, SEQ[5], exclude=(3.0, 7.0))
            ax.add_patch(Polygon([[3.1, 8], [3.7, 8], [4.4, 1], [3.8, 1]], color=C[2], alpha=0.55, lw=0))
            ax.add_patch(Polygon([[6.3, 8], [6.9, 8], [6.2, 1], [5.6, 1]], color=C[2], alpha=0.55, lw=0))
            ax.add_patch(Polygon([[3.7, 8], [6.3, 8], [5.6, 1], [4.4, 1]], facecolor="white", edgecolor=INK2, lw=1))
            ax.text(2.0, 0.3, "相环(低E/高α 梯度)", fontsize=8, color=C[2])
        else:
            crystals(ax, 0.6, 9.4, 1.1, 7.9, 0.16, 330, SEQ[5], exclude=(3.0, 7.0))
            ax.add_patch(Polygon([[3.1, 8], [3.7, 8], [4.4, 1], [3.8, 1]], color=C[2], alpha=0.55, lw=0))
            ax.add_patch(Polygon([[6.3, 8], [6.9, 8], [6.2, 1], [5.6, 1]], color=C[2], alpha=0.55, lw=0))
            ax.add_patch(Polygon([[3.7, 8], [6.3, 8], [5.6, 1], [4.4, 1]], facecolor="#d9895b", edgecolor=INK2, lw=1))
            ax.add_patch(Rectangle((2.2, 8), 5.6, 0.45, color="#d9895b")); ax.add_patch(Rectangle((2.6, 0.55), 4.8, 0.45, color="#d9895b"))
            ax.text(5, 4.5, "Cu", ha="center", fontsize=9, color="white")
    fig.subplots_adjust(wspace=0.32)
    for k in range(4):
        p0 = axs[k].get_position(); p1 = axs[k + 1].get_position()
        fig.add_artist(FancyArrowPatch((p0.x1 - 0.003, 0.45), (p1.x0 + 0.003, 0.45), transform=fig.transFigure, arrowstyle="-|>", mutation_scale=18, color=INK2))
    fig.suptitle("核心工艺路线 R2：“先孔后晶（Via-first, Ceram-later）”——以纳米晶态完成激光成孔，再晶化增韧", y=1.04, fontsize=12)
    savefig(fig, "fig_process_route.png")

def box(ax, x, y, w, h, text, fc, fs=9, ec=None, tc=INK):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.12", fc=fc, ec=ec or fc, lw=1.2))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, color=tc, wrap=True)

def arrow(ax, p, q, col=INK2):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=12, color=col, lw=1.1))

def framework():
    fig, ax = plt.subplots(figsize=(14, 7.6)); ax.set_xlim(0, 14); ax.set_ylim(0, 8); ax.axis("off")
    ax.text(7, 7.7, "研究框架：3 个关键科学问题 → 5 个工作包 → 多物理仿真闭环 + 实验验证 → 成果", ha="center", fontsize=13, color=INK)
    ksp = ["KSP1 两相介质中超快激光-物质作用\n与相衬度选择性刻蚀机制",
           "KSP2 多尺度失配应力的产生、传递与\n断裂控制（晶粒—相环—通孔—面板）",
           "KSP3 多相氧化物亚太赫兹介电损耗与\n导体粗糙度损耗的结构起源"]
    for i, t in enumerate(ksp):
        box(ax, 0.2, 5.6 - i * 1.9, 3.4, 1.4, t, "#dbeefc", fs=9)
    wps = ["WP1 材料设计：可调CTE/低损耗\n透明纳米晶微晶玻璃（MAS/镁橄榄石）",
           "WP2 激光改性+选择刻蚀成孔\n（贝塞尔光束、相衬度、AR≥15）",
           "WP3 晶化动力学与相环工程\n（先孔后晶、饱和晶化、梯度相环）",
           "WP4 金属化与可靠性\n（粘结、全填/共形、TC/HAST/EM）",
           "WP5 高频与系统演示\n（D-band 互连、天线/芯粒集成）"]
    for i, t in enumerate(wps):
        box(ax, 4.6, 6.4 - i * 1.4, 3.6, 1.1, t, "#fbe3d6", fs=8.8)
    sims = ["S1 Mie/MC/热累积", "S2 FMM/CA 刻蚀", "S3 弹塑性FEM/断裂", "S4 层合板/可行域", "S5 热扩散级数/FEM",
            "S6 RVE/电磁/传输线", "S7 JMAK/面板套刻", "S8 Selsing/微裂", "S9 Weibull", "S10 Sobol 敏感性"]
    for i, t in enumerate(sims):
        box(ax, 9.2 + (i % 2) * 2.1, 6.5 - (i // 2) * 1.05, 1.95, 0.8, t, "#e3f2e6", fs=8.3)
    box(ax, 9.2, 0.25, 4.05, 0.95, "成果：Nature Electronics / Nature Communications\n+ IEDM / ECTC + 专利 + 设计规则", "#f0efec", fs=9)
    for i in range(3):
        for j in range(5):
            if (i, j) in [(0, 0), (0, 1), (1, 2), (1, 3), (2, 0), (2, 4), (0, 2), (1, 0)]:
                arrow(ax, (3.6, 6.3 - i * 1.9), (4.6, 6.95 - j * 1.4))
    arrow(ax, (8.2, 4.0), (9.2, 4.0)); arrow(ax, (9.2, 3.6), (8.2, 3.6))
    ax.text(8.7, 4.15, "预测", ha="center", fontsize=8, color=INK2); ax.text(8.7, 3.25, "标定", ha="center", fontsize=8, color=INK2)
    arrow(ax, (11.2, 2.25), (11.2, 1.25))
    savefig(fig, "fig_framework.png")

def gantt():
    tasks = [("WP1 材料设计与熔制", 0, 12, C[0]), ("WP1 介电/力学/热物性全表征", 4, 18, C[0]),
             ("WP2 激光改性参数窗口", 3, 15, C[1]), ("WP2 选择刻蚀与AR≥15成孔", 8, 22, C[1]),
             ("WP3 晶化动力学/相环构筑", 6, 20, C[2]), ("WP3 面板级套刻与翘曲", 14, 28, C[2]),
             ("WP4 金属化与粘结", 12, 26, C[3]), ("WP4 可靠性 TC/HAST/EM", 20, 34, C[3]),
             ("WP5 D-band 互连/天线", 18, 32, C[6]), ("WP5 芯粒集成演示", 26, 36, C[6]),
             ("仿真闭环（贯穿）", 0, 36, C[5])]
    fig, ax = plt.subplots(figsize=(11, 4.8))
    for i, (t, s, e, c) in enumerate(tasks):
        ax.barh(i, e - s, left=s, color=c, height=0.55)
    ms = [(12, "M1 材料定型"), (22, "M2 AR≥15 无裂纹孔"), (28, "M3 510 mm 面板验证"), (34, "M4 1000 TC 通过"), (36, "M5 系统演示/投稿")]
    for x, t in ms:
        ax.axvline(x, color=INK2, ls=":", lw=1); ax.text(x, -1.0, t, rotation=0, ha="center", fontsize=7.5, color=INK2)
    ax.set_yticks(range(len(tasks))); ax.set_yticklabels([t[0] for t in tasks], fontsize=8.5); ax.invert_yaxis()
    ax.set_xlim(0, 37); ax.set_ylim(len(tasks) - 0.4, -1.5); ax.set_xlabel("月")
    ax.set_xticks(range(0, 37, 3)); ax.grid(axis="y", visible=False)
    ax.set_title("36 个月研究进度与里程碑")
    savefig(fig, "fig_gantt.png")

def timeline():
    ev = [(2010, "GT PRC：玻璃中介层TPV\n(ECTC 2010)", 0.5), (2013, "TSMC：300 mm 超薄玻璃中介层\n(IEDM 2013)", -0.5),
          (2015, "KAIST：TGV RLGC 建模\n(ECTC 2015)", 0.5), (2020, "GT：28 GHz 玻璃 AiP\n0.095 dB/孔 (TMTT)", 0.5),
          (2021, "Corning：径向/环向\n裂纹机理 (MR/TDMR)", -0.5), (2023, "Intel 发布\n玻璃芯基板", 0.5),
          (2024, "NEG GC Core 微晶玻璃芯\nAbsolics CHIPS 资助", -1.05), (2025, "ECTC 玻璃芯专场\nNEG 515×510 面板", 1.05),
          (2026, "Microsyst. Nanoeng. TGV 机理论文\nBOE 15:1 TGV；Intel EMIB-玻璃", -0.5),
          (2027.5, "SEMCO 合资\n量产目标 2H27", 0.5), (2028.5, "TSMC CoPoS / DNP / BOE\n量产目标", -1.05), (2030, "业界预期\n规模化采用", 1.05)]
    fig, ax = plt.subplots(figsize=(14, 4.4))
    ax.axhline(0, color=INK2, lw=1.5)
    for x, t, s in ev:
        col = C[0] if x <= 2026.8 else C[1]
        ax.plot([x, x], [0, s], color=col, lw=1); ax.plot(x, 0, "o", color=col, ms=6)
        ax.text(x, s + (0.06 if s > 0 else -0.06), t, ha="center", va="bottom" if s > 0 else "top", fontsize=7.6, color=INK)
    ax.axvspan(2026.8, 2031, color="#fbf1c7", alpha=0.5, zorder=0); ax.text(2029.6, 1.75, "规划/预期（非已实现）", ha="center", fontsize=8, color=INK2)
    ax.set_ylim(-1.9, 1.9); ax.set_xlim(2009, 2031.2); ax.set_yticks([]); ax.spines["left"].set_visible(False)
    ax.set_xticks(range(2010, 2031, 2)); ax.grid(False)
    ax.set_title("TGV / 玻璃芯基板关键里程碑（基于公开报道整理）")
    savefig(fig, "fig_timeline.png")

if __name__ == "__main__":
    process_route(); framework(); gantt(); timeline()
