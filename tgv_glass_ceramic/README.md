# 微晶玻璃基板 TGV 三维封装：可行性研究方案与多物理场仿真

**主交付物**：`微晶玻璃TGV三维封装可行性研究方案与仿真报告.docx`（约 46 页，35 幅图（多为多子图），19 张表，65 条参考文献）

## 目录结构
| 路径 | 内容 |
|---|---|
| `sim/` | 10 个仿真模块（S1–S10）及求解器：`fem_axi.py` 自编轴对称 Q4-Bbar 弹塑性 FEM；`fem_skfem.py` scikit-fem P2 求解器；`analytic_mech.py` 解析解 |
| `results/` | 各模块数值结果（JSON）与运行日志；`summary.json` 为关键数值与 19 组交叉验证汇总 |
| `figures/` | 报告全部插图（PNG，200 dpi） |
| `research/` | 文献调研笔记（工艺与产业 / 可靠性与矛盾 / 微晶玻璃 / 射频与高影响力论文） |
| `research_notes/`、`reports/` | 应力缓冲层专题调研笔记与报告（Markdown + Word） |
| `sim/buffer_recheck/` | 缓冲策略全局指标复算脚本（相环变体、峰值定位、共形 Cu 壁厚） |
| `report/` | 报告源文件（`part1–5.md`）与 Word 生成脚本 `md2docx.js`（docx-js） |

## 复现
```bash
pip install numpy scipy matplotlib scikit-fem scikit-fmm miepython scikit-rf SALib
cd sim
python3 s1_laser.py; python3 s2_etch.py; python3 s2b_etch3d.py; python3 s3_thermomech.py
python3 s3b_fracture.py; python3 s3c_fracture_check.py; python3 s4_warpage.py; python3 s5_thermal.py
python3 s6_electrical.py; python3 s7_ceramming.py; python3 s8_microstructure.py; python3 s10_sobol.py
python3 summary.py; python3 make_schematics.py
cd .. && cat report/part{1,2,3,4,5}.md > report/report.md && node report/md2docx.js report/report.md 报告.docx
```
在 4 核 / 16 GB 机器上全部运行约 40 分钟（S3 弹塑性历程与 S3b/S3c 断裂 FEM 最耗时）。

## 说明
仿真采用文献代表性材料参数与明确声明的假设（见报告附录 A 与 7.3 节），用于可行性筛选与机理分析，不替代实验。文献信息基于公开检索，部分条目标注“未核实”，投稿前需逐条核对原文。
