# 缓冲层削减 TGV 应力，却常只是转移热点

TGV（玻璃通孔）应力缓冲层的研究现状可以概括为**概念已经铺满，证据仍停在仿真**。聚合物（HD4100 PI、BCB、Parylene、ABF）和烧结无机层（TiO₂/ZnO/ZrO₂）在 FEA 中能把玻璃应力降低 40–69%。但拿到实验阈值的只有结构与工艺手段：Corning 证明，共形 Cu 壁厚 <12 µm 可消除降温环向裂纹，升温速率 ≤6.5 °C/min 可消除升温径向裂纹。以聚合物缓冲层为单一变量的受控实验，只有 Georgia Tech 2017 年的薄玻璃 via-first 工作和一篇细节不详的国内论文；与缓冲层直接相关的 HAST、He 气密、毫米波 S 参数和电迁移数据几乎空白。代价同样明确。在固定孔径下，5 µm 衬层使 50 µm 孔的 Cu 截面只剩 64%，电阻增加 56%；多数聚合物扛不住 400–420 °C 的 Cu 退火，还会破坏玻璃的气密性；而玻璃开裂一旦被压住，失效就转移到 Ti/Cu 等界面。产业侧，Intel 2023–2026 年的申请几乎覆盖了所有"通孔侧"缓冲思路，但公开的量产措施只有 Shinko 的树脂边缘涂层；只有 ISTFA 2026 的一篇报告称"调节模量与厚度的缓冲层"通过了 TC/HAST。国内研究集中在《电子与封装》2025 年 TGV 专刊，以仿真为主。本报告用项目前期的弹塑性 FEM 代码复算发现，文献和本项目常用的"近壁应力"指标会把缓冲收益夸大一倍以上：原相环设计的近壁环向应力降低 68%，全局最大环向应力却只降低 30%，峰值被推到了相环外缘。对"微晶玻璃 + 梯度相环"方案的直接启示是：真正起作用的杠杆是**低模量和足够宽度（约 D/4）**，CTE 应在基体值附近适度上调，而不是越高越好。宽 12.5 µm、内侧模量 20 GPa、CTE 与基体相同的相环，可使两种微晶玻璃的全局环向应力都降低 57%，且不占用 Cu 截面。前提是保住界面粘结，并避开聚合物浸渗带来的热预算与气密陷阱。

## 材料型缓冲层：40–69% 的降幅几乎全部来自仿真

先说明证据口径。本报告所依据的文献信息多来自摘要、专利摘要、会议节目单和行业报道，调研中未能逐篇读取全文；标注"未核实"的条目只作线索。下表给出各类缓冲路线的全景，后文逐类展开。

| 缓冲路线 | 代表工作 | 报道的最大收益 | 证据等级 | 主要代价 |
|---|---|---|---|---|
| 聚合物侧壁衬层/表面层压 | HD4100 10 µm；1 µm 有机层；GT ZIF/RXP-4/ABF | TGV/RDL 边缘 −51%/−69%；最大主应力 −40% | 仿真为主；GT 2013–2017 薄玻璃实验 | 占 Cu 截面；Tg 约 320–350 °C；吸湿；破坏气密 |
| 厚无机烧结层 | 5 µm TiO₂（ZnO/ZrO₂ 对比） | 玻璃芯应力 −66.58% | 仅仿真 | 降温应力上升；占截面；侧壁烧结难 |
| 薄粘附/阻挡层 | Ti ≈100 nm；ALD TiO₂/TiN/Ru | 不改变应力场，只管附着与气密 | 实验 | HAST 中 Ti/Cu 界面最先失效 |
| 共形/中空 Cu | Corning 壁厚 <12 µm | 环向裂纹归零 | 实验阈值 | 30 GHz 插损 0.48 dB（全填 0.23 dB）；需堵芯 |
| 侧壁气隙/解耦 | Intel 2026 申请 | 无数据 | 专利 | 失去锚固与气密 |
| 边缘涂层 | Shinko 300 µm 树脂 | 边缘应力 95→49 MPa | 公司报告 | 只针对 SeWaRe |
| 升温速率控制 | Corning ≤6.5 °C/min | 径向裂纹归零 | 实验 + 专利 | 产能；阈值仅在熔融石英上建立 |
| 低 CTE 填充 | 电镀 Ni-Fe，CTE 7.27 ppm/K | 未报数值 | 填充实验 | 电阻率未报 |

### 聚合物：三类用法，一个硬实验

TGV 中的聚合物缓冲可分三类。第一类是玻璃表面层压。Georgia Tech PRC 2010–2019 年的玻璃中介层项目，先用硅烷处理玻璃，再双面真空层压 ZEON ZIF、Rogers RXP-4、ABF GX92P/GY11 或环氧底漆，然后激光成孔和镀 Cu ([GT dissertation](https://repository.gatech.edu/server/api/core/bitstreams/1c691386-1e2b-48b2-bed0-fc610a84f90c/content))。第二类是侧壁衬层，包括 HD4100 PI、PI-2610/2611 类前驱体、BCB 和 Parylene HT/AF4，几乎都停留在仿真或专利阶段 ([US 12087623](https://patents.justia.com/patent/12087623))。第三类是"via-in-via"：先用聚合物填满通孔，再在聚合物中重钻小孔并金属化，剩余的聚合物环充当"应力释放屏障" ([US9275934](https://patents.google.com/patent/US9275934))。GT 的玻璃面板嵌入工作也采用了这一结构，并称它"可抵消 TGV 缺陷、提高电镀可靠性" ([JMEP 2019](https://imapsjmep.org/article/40194-design-and-demonstration-of-glass-panel-embedding-for-3d-system-packages-for-heterogeneous-integration-applications.pdf))。

仿真给出的数字很大。Zhao 等用 10 µm HD4100（模量 3.5 GPa、伸长率 45%、Tg 320 °C）作缓冲层，TGV 边缘和 RDL 边缘应力分别降低 **51.15% 和 69.1%** ([Micromachines 2022](https://www.mdpi.com/2072-666X/13/10/1799); [HD4100](https://www.hdmicrosystems.com/products/hd4100))。但同一篇论文中，另一种聚合物结构（"structure A"）降低了 RDL 边缘应力，却**升高了 TGV 边缘应力** ([PMC9607209](https://pmc.ncbi.nlm.nih.gov/articles/PMC9607209/))。这说明缓冲层可能只是把热点从一处搬到另一处。《电子与封装》2025 年 070103 号论文用约 **1 µm 有机层使玻璃最大主应力降低约 40%**，并称实验显示热应力可靠性更好，但实验条件未能获取 ([researching.cn 70103](https://m.researching.cn/articles/OJb7b8695062740314))。GT 团队的综述引用 FEA 结果称，薄的柔性聚合物衬层可使能量释放率（ERR）比实心孔低 **>75%**，但其一手来源未能识别 ([Chips 2025](https://www.mdpi.com/2674-0729/4/3/37))。Ahmed 等和 Sharma 等的断裂力学仿真也都认为缓冲层"显著降低开裂" ([Emerald MMMS](https://emerald.com/insight/content/doi/10.1108/MMMS-05-2020-0125/full/html); [Microelectron. Eng. 2026](https://www.sciencedirect.com/science/article/abs/pii/S0167931725001303))。

硬实验只有一项。Demir 等（GT，IEEE TDMR 2017）在 100 µm 聚合物层压玻璃上做 via-first TPV，经 −55/125 °C 循环无失效。SEM 显示，**裸玻璃 via-first 对照组中出现的分层和裂纹被消除**，作者把原因归于应力降低和附着增强 ([FIU Discovery](https://discovery.fiu.edu/display/pub135653))。更早的 ECTC 2013 工作比较了多种玻璃/衬层组合，CF-XX/ZIF 的剪应力和轴向拉应力最低，多数样品通过 1000 次循环，失效源于电镀缺陷 ([ResearchGate](https://www.researchgate.net/publication/260192671_Thermomechanical_and_electrochemical_reliability_of_fine-pitch_through-package-copper_vias_TPV_in_thin_glass_interposers_and_packages))。via-first 工艺（5 µm 聚合物，100 µm 玻璃上 10–20 µm 孔、40 µm 节距）通过了 1000 次 TC 和 96 h HAST ([TCPMT 2017](https://www.researchgate.net/publication/313466210_Via-First_Process_to_Enable_Copper_Metallization_of_Glass_Interposers_With_High-Aspect-Ratio_Fine-Pitch_Through-Package-Vias))。这些都是 ≤100 µm 薄玻璃、10–30 µm 小孔。今天 AI 用玻璃芯是 300–700 µm 厚板、50–100 µm 孔，聚合物缓冲在这类结构上的表现只能靠仿真外推。

工艺限制同样具体。层压前聚合物必须部分预固化，形成"帐篷孔"，否则会流进孔内 ([TCPMT 2017](https://www.researchgate.net/publication/313466210_Via-First_Process_to_Enable_Copper_Metallization_of_Glass_Interposers_With_High-Aspect-Ratio_Fine-Pitch_Through-Package-Vias))。固化残留会让孔开不全 ([GT paper](https://smtnet.com/library/files/upload/high-pitch-vias.pdf))。固化收缩会造成嵌入芯片漂移 ([IMAPS 2018](https://meridian.allenpress.com/ism/article/2018/1/000331/9472/Design-and-demonstration-of-Glass-Panel-Embedding))。Parylene 的共形性只在 TSV 上得到验证：1 µm Parylene-HT 在 AR 10 时台阶覆盖率 >80% ([ResearchGate](https://www.researchgate.net/publication/304421563_Copper_filled_TSV_formation_with_Parylene-HT_insulator_for_low-temperature_compatible_3D_integration))。TGV 内的厚度均匀性没有任何数据，Parylene AF4 用于 TGV 的说法目前只来自供应商宣传 ([COAT-X](https://coat-x.com/en/parylene-af4-the-dielectric-polymer-redefining-through-glass-via-technology/))。另有一则流传的 MRS 2026 摘要称 Parylene 涂覆可把断裂概率降低约 73%，但在会议节目单中无法定位，本报告不予采信 ([MRS 2026 program](https://www.mrs.org/docs/default-source/meetings-events/spring-meetings/2026/2026-mrs-spring-meeting-program.pdf?sfvrsn=9299efcf_1))。

### 无机与金属层：厚层只在仿真里有效，薄层是失效起点

"无机缓冲层"其实包含两类性质完全不同的东西。第一类是 µm 级烧结氧化物。《电子与封装》070108 号论文在玻璃与 Cu 之间烧结 ZnO、TiO₂ 或 ZrO₂ 并做 FEA，结果是 **5 µm TiO₂ 使玻璃芯应力降低 66.58%**；缓冲层越厚、孔径越小，应力越低 ([researching.cn 70108](https://www.researching.cn/articles/OJ6c1dee1b5d059512))。行业报道对同一工作的描述略有不同：在 25→190 °C 层压升温中，纯 Cu 玻璃芯最大应力为 202.36 MPa，TiO₂ 使最大主应力降低 49.3%，"明显优于常规 PI 缓冲层"；厚度从 1 µm 增至 5 µm 时，升温段应力持续下降，降温段应力略升；芯板厚度在 400–1200 µm 范围内影响很小 ([中国粉体网](https://news.cnpowder.com.cn/85217.html))。66.58% 与 49.3% 很可能对应不同厚度或指标，全文不可得，无法核对。这项工作没有实验验证。

第二类是 nm 级粘附、阻挡和种子层，它们才是产线现实。Corning 的气密通孔专利在孔壁上设 1–500 nm（例 ≈100 nm）的 Ti 粘附层，He 漏率 <1×10⁻⁸ atm·cc/s，且在 1000 次热冲击后保持 ([US 11152294](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11152294); [WO2019199677A3](https://patents.google.com/patent/WO2019199677A3/en))。全 ALD 叠层（5 nm TiO₂ / 11 nm TiN / 11 nm Ru / 80 nm Cu）在 25:1 TGV 中实现 97.7% 台阶覆盖率，PVD TiN 则覆盖不良 ([MSSP 2025](https://www.sciencedirect.com/science/article/abs/pii/S1369800125010224))。湿法路线也有进展。Ag 掺杂 ZnO 溶胶–凝胶层在 10:1 TGV 中实现全覆盖，300 °C 退火后附着力为 4.19 N/cm ([JECS 2025](https://iopscience.iop.org/article/10.1149/1945-7111/ada589))。低温 SILAR ZnO 依靠多孔层的机械锚固，剥离强度 >6.8 N/cm ([JECS 2025](https://iopscience.iop.org/article/10.1149/1945-7111/ae02c9))。超声加工粗化侧壁比 ECDM 粗化更利于种子层附着 ([MSSP 2024](https://www.sciencedirect.com/science/article/abs/pii/S136980012400653X))。这些论文只报告附着与覆盖，没有一篇报告应力或开裂收益：几十纳米的硬质层改变不了 CTE 失配应力场。

问题在于，薄金属层恰恰成了失效起点。Corning 在熔融石英 Cu TGV 上发现，HAST 是破坏性最强的测试，400–1600 h 后因 Cu 氧化和 **Ti–Cu 界面脱粘**而失效 ([MR 2022](https://www.sciencedirect.com/science/article/abs/pii/S0026271422003079))。厦门大学的部分填充 TGV 在 HAST 中同样以 Ti–Cu 界面微裂纹贯穿为主要失效模式，机理是 Ti 向玻璃扩散、Cu 向 Ti 扩散形成微孔洞 ([CNKI](http://dbase2.gslib.com.cn/KCMS/detail/detail.aspx?filename=JBXK202310018&dbcode=CJFD&dbname=CJFD2023))。高温老化研究也观察到 Cu/Ti 界面空洞长成沿侧壁的贯穿裂纹 ([Sun & Zhang 2026](https://www.sciencedirect.com/author/56437796500/shuye-zhang))。250 °C 老化 1008 h 后，TGV-Cu 模量从 110–130 GPa 降到 40–90 GPa，玻璃出现微裂纹 ([Microsyst. Nanoeng. 2026](https://www.nature.com/articles/s41378-026-01160-0))。更"柔"的金属缓冲，如多孔 Cu 衬层（孔隙率最高约 60%）和 ZnO 纳米线，都还只是 Intel 的专利申请，没有公开数据 ([Intel porous Cu liner](https://trea.com/information/porous-copper-liner-for-through-glass-via-tgv-glass-cores/patentapplication/edc94632-2fe9-410d-b95d-12772cd3acf4); [Justia](https://patents.justia.com/company/intel?list=applications&page=5))。

## 结构与工艺手段反而握有最硬的实验阈值

### 共形 Cu、沙漏孔与部分填充

整个领域最清楚的实验阈值来自 Corning。在 HPFS 熔融石英上，平均外径 47.5 µm 的 Cu TGV 经 400 °C 退火、降温时出现环向裂纹。**Cu 层厚度 <12 µm 时不开裂，≥12 µm 时开裂概率指数上升**；FEA 给出的起裂阈值约 140 MPa，驱动力是降温时玻璃中的径向拉应力 ([IEEE TDMR 2021](https://ieeexplore.ieee.org/document/9481891/); [ECTC 2021](https://ieeexplore.ieee.org/document/9501526/))。这一阈值已写入其专利 ([US 12131985](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12131985))。GT 的共形 TPV 数据与之呼应：100 µm 玻璃中，60 µm 孔经 4000 次循环无退化，30 µm 孔经 3000 次循环（−55/125 °C）电阻稳定，失效模式是孔角附近的分层和玻璃开裂 ([academia.edu](https://www.academia.edu/119963275/Reliability_of_Copper_Through_Package_Vias_in_Bare_Glass_Interposers); [IMAPS 2014](https://meridian.allenpress.com/ism/article-pdf/2014/1/000402/2252418/isom-wa16.pdf))。Le & Choa 的 ERR 仿真认为"带 Cu 焊盘的中空 TGV"开裂驱动力最低，但也指出，即使热循环的 ERR 低于退火，循环中仍可能开裂 ([JMST 2024](https://link.springer.com/article/10.1007/s12206-024-0522-1))。

中空孔把问题转移到了气密性和孔芯。Corning 的解法是沙漏形"共形夹断孔"（CPV）：用添加剂 NTBC 超共形电镀一步金属化，并在孔口附近设 He 密封粘附层 ([ECTC 2025](https://www.semanticscholar.org/paper/Metallization-of-Helium-Hermetic-and-Reliable-Glass-Kanungo-Vaddi/f7e85f42e70b8fc01bbd7048bd6b20915daf7e4c))。相关 MEMS 专利报告的 He 漏率 <1×10⁻⁶ atm·cm³/s ([US 11148935](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11148935))。国内业界的经验做法是：实心全填一般限于孔径 <50 µm、玻璃厚 <100 µm；更大、更厚的孔改用双面部分填充，侧壁共形、仅在 X 形孔腰部实心 ([腾讯新闻转载](https://news.qq.com/rain/a/20230916A017AJ00))。

### 气隙与边缘：专利热、数据冷

Intel 2026 年公开的"自底向上电镀"申请，在侧壁不设完整种子层，让 Cu 从孔底长起，与侧壁之间留下可辨的气隙作为应力缓冲，可选低模量衬层作"二次缓释"。申请中描述了减成刻蚀、mSAP 和可流动材料填腔三条路线，没有实测数据；公开号在不同来源中分别为 US20260173267A1 和 US 2026/0173908 A1，尚未统一 ([Patsnap](https://eureka.patsnap.com/patent/US20260173267A1); [Patsnap DE](https://eureka.patsnap.com/patent/DE102025144620A1); [艾邦](https://www.ab-sm.com/a/75754))。TSV 领域早有类似专利 ([US 8962474](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/8962474))。

面板级的另一大问题是切割边缘的 SeWaRe 侧壁裂纹，根源是玻璃芯与积层树脂的 CTE 失配。Shinko 因证明边缘涂层在 260 °C 回流后仍能抑制 SeWaRe，获得 ECTC 2025 杰出论文奖 ([Shinko](https://www.shinko.co.jp/english/news/2026/07/b2e0e1c9fadd06989a3ba3940788615cdb6ddaf4.php))。据 TrendForce，Shinko 在 300 µm 树脂层条件下用边缘涂层把边缘应力从约 **95 MPa 降至约 49 MPa** ([TrendForce Insights](https://insights.trendforce.com/p/glass-substrate-development))。Le 等的仿真则给出几何解：边缘留白 ≥300 µm 可有效抑制裂纹扩展；高 CTE 玻璃（含陶瓷玻璃）比 Borofloat 33 和熔融石英更抗裂 ([Micromachines 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12654316/))。另有一类"平面型"缓冲层，处理的是翘曲与界面开裂而非通孔开裂：Toppan 用干法涂覆绝缘层使玻璃在室温处于压应力状态 ([US 11516911](https://patents.google.com/patent/US11516911))；一组疑似 DNP 的专利在玻璃与有机绝缘层之间设无机应力松弛层 ([US 11195768](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11195768))；京东方 CN122008643A 用介电层作"柔性应力缓冲结构" ([新浪财经](https://finance.sina.com.cn/stock/aigc/zl/2026-05-14/doc-inhxvpqq8741383.shtml))。

### 工艺型缓冲：用时间换应力

升温速率控制是验证最充分的非聚合物手段。Corning 发现，全金属化 HPFS TGV 退火至 420 °C 时，径向裂纹随升温速率指数增加，**≤6.5 °C/min 时完全消除** ([MR 2021](https://www.sciencedirect.com/science/article/abs/pii/S0026271421000585))。据专利摘要，其专利族要求在 200–300 °C 至 350–450 °C 区间平均升温速率 <8.7 °C/min，优选 1.0–6.5 °C/min；专利标题明确覆盖"玻璃或微晶玻璃制品" ([US 12515977](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12515977); [CN113474311A](https://patents.google.com/patent/CN113474311A/en))。原位 DIC 揭示了机理：玻璃面内位移在约 250 °C 达到峰值，随后因 Cu 凸出和蠕变而回落，慢速升温让 Cu 有时间蠕变松弛 ([MR 2022](https://www.sciencedirect.com/science/article/abs/pii/S0026271422000117))；Cu 在约 250 °C 以下受玻璃和附着约束，400 °C 时平均凸出约 1.6 µm ([ECTC 2021](https://ieeexplore.ieee.org/document/9501700/))。代价是产能：按 6.5 °C/min 计，从 25 °C 升到 420 °C 约需 1 h。

保温与老化存在两面性。50 µm × 300 µm TGV 在 400 °C 下的凸出约 240 min 饱和；先行退火保温 ≥120 min 后，后续工序不再增加凸出 ([TDMR 2021](https://ieeexplore.ieee.org/document/9353697/))。但哈工大 2026 年的研究表明，适度退火可释放玻璃应力，长时间退火却会在玻璃中积累残余拉应力并引发开裂；300 °C 下 216 h 与 288 h 的环向裂纹长度分别为 6.9 µm 和 18.9 µm（据检索摘录，未与全文核对） ([Microsyst. Nanoeng. 2026](https://www.nature.com/articles/s41378-026-01162-y))。京东方认为，有机添加剂杂质形成空位，空位在热失配应力下聚集，驱动 Cu 凸出 ([SID Digest 2025](https://sid.onlinelibrary.wiley.com/doi/abs/10.1002/sdtp.18370))。从源头消除失配的路线也已出现：电镀 Ni-Fe 合金 CTE 达 7.27 ppm/K，与 7.2 ppm/K 的玻璃匹配，糖精钠同时降低内应力并促进超填充；但摘要未给出应力、循环或电阻率数据 ([JMST 2026](https://www.sciencedirect.com/science/article/abs/pii/S1005030225011983); [IEEE](https://ieeexplore.ieee.org/abstract/document/11392609/))。CNT–Cu 只有 TSV 数据 ([PubMed](https://pubmed.ncbi.nlm.nih.gov/27383767/))。

这一节的核心结论是：两类裂纹需要两根不同的杠杆。升温径向裂纹由 Cu 受约束膨胀引起，靠升温速率控制；降温环向裂纹由 Cu 收缩拉拽孔壁引起，靠 Cu 壁厚控制 ([MR 2021](https://www.sciencedirect.com/science/article/abs/pii/S0026271421000585); [TDMR 2021](https://ieeexplore.ieee.org/document/9481891/))。两个阈值都只在熔融石英（CTE ≈0.5 ppm/K）上建立，硼硅玻璃、无碱玻璃和微晶玻璃上的阈值仍是空白。

## TSV 经验可以迁移，但玻璃从软衬层中获益更少、指标更易失真

### 哪些 TSV 结论能搬到玻璃上

Si TSV 积累了更系统的缓冲层数据。在 full-chip 分析中，500 nm BCB 衬层比 SiO₂ 衬层降低约 **29%** 的 von Mises 应力 ([UT Austin/GT J47](https://www.cerc.utexas.edu/utda/publications/J47.pdf))，解析模型也认为 BCB 优于 SiO₂ ([CPB 2015](https://iopscience.iop.org/article/10.1088/1674-1056/24/5/056601))。东北大学（Tohoku）的气相聚合 PI 衬层经显微 Raman 证实"极大降低"了邻近 Si 的应力，可耐 350 °C ([IEDM 2014](https://www.researchgate.net/publication/273003298_Highly_Beneficial_Organic_Liner_with_Extremely_Low_Thermal_Stress_for_Fine_Cu-TSV_in_3D-Integration))，但同组也专门撰文讨论有机衬层的"利与弊" ([ResearchGate](https://www.researchgate.net/publication/266203177_Replacing_the_PECVD-SiO_2_in_the_Through-Silicon_Via_of_High-Density_3D_LSIs_with_Highly_Scalable_Low_Cost_Organic_Liner_Merits_and_Demerits))。最重要的一条权衡是：BCB 衬层"降低衬底热应力，但**增大 Cu 柱轴向热膨胀**" ([MR 2013](https://www.sciencedirect.com/science/article/abs/pii/S0026271413000036))。不过，imec 发现低 k 衬层反而降低了残余 Cu pumping ([ResearchGate](https://www.researchgate.net/publication/273146056_Impact_of_oxide_liner_properties_on_TSV_Cu_pumping_and_TSV_stress))，一项专利也认为更硬的致密化衬层会导致更多轴向凸出 ([US 10163655](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10163655))。两者并不矛盾：可逆热膨胀与不可逆塑性 pumping 是两个量，必须分别报告。

结构方面，气隙 TSV 的应力降至约 80 MPa ([Engineering 2023](https://www.engineering.org.cn/engi/CN/10.1016/j.eng.2023.11.023))；中科院微电子所的中空"橄榄球"TSV 残余应力为 31.02 MPa，但出自新闻稿 ([IMECAS](https://ime.cas.cn/kygz/kydt/202404/t20240426_7133192.html))；同轴环形 TSV 比同轴 TSV 的 KOZ 缩小 1.6 µm（22.2%） ([IEEE TED 2014](https://ieeexplore.ieee.org/document/6845357/))。两条警示同样重要。其一，随着 TSV 缩小，Parylene 替代 SiO₂ 或采用环形结构的降应力效果会消失 ([ECTC 2015](https://ieeexplore.ieee.org/abstract/document/7159725/))。其二，在 8 层堆叠 TSV 中，**填充物的 CTE 主导了 Cu 孔应力** ([SeoulTech](https://pure.seoultech.ac.kr/en/publications/study-of-thermo-mechanical-reliability-of-tsv-for-8-layer-stacked/))。GT 在玻璃上的对应结论是：高 CTE 玻璃应配低 CTE 聚合物 ([J Mater Sci 2018](https://link.springer.com/article/10.1007/s10854-018-9384-6))。

能迁移到玻璃的是柔性衬层、环形/同轴几何、"共形 Cu 内填软芯"三类思路。不能迁移的是 KOZ：它以 MOSFET 迁移率为判据，而玻璃中对应的判据是环向拉应力裕度、界面 ERR 和 RDL 边缘应力。调研组用三层 Lamé 闭式模型估算（非文献数据）：50 µm 孔、ΔT = 250 K 时，2 µm BCB 使 Si 孔壁应力降低约 48%，在硼硅玻璃中只降低约 35%，因为玻璃（约 70 GPa）本来就比 Si 柔。固定孔径时，厚衬层约一半的收益来自 Cu 芯变小。低 CTE PI 在 10 µm 厚度下明显优于高 CTE 的 BCB/Parylene。项目 FEM 中 2 µm 聚合物衬层的近壁降幅为 32%，与这一估算相符。

### 建模方法：四层工具链与一个被忽视的口径问题

文献中的建模实践可归纳为四层。第一层是广义平面应变 Lamé 同心圆柱解，用于快速筛选。第二层是近表面三维 FEA：自由表面产生驱动分层的界面剪应力和正应力，稳态 ERR 是分层的解析上界，且与孔径成正比 ([Ryu, TDMR 2011](https://www.researchgate.net/publication/224169323_Impact_of_Near-Surface_Thermal_Stresses_on_Interfacial_Reliability_of_Through-Silicon_Vias_for_3-D_Interconnects))。第三层是断裂力学：TGV 的 ERR 与孔径成线性、与 ΔT 成平方关系，**在裂纹长度约 D/4 处达到峰值**；熔融石英的 ERR 最高，"陶瓷玻璃"更可靠 ([Microelectron. Eng. 2026](https://www.sciencedirect.com/science/article/abs/pii/S0167931725001303))。降温 ERR 高于升温 ERR，因此降温更易引发分层 ([Micromachines 2022](https://www.mdpi.com/2072-666X/13/10/1799))。第四层是本构与界面模型：弹塑性/蠕变 Cu、带 Prony 级数与时温移位的粘弹性聚合物 ([NASA TM](https://ntrs.nasa.gov/api/citations/20000052499/downloads/20000052499.pdf))、双线性内聚力界面 ([arXiv](https://arxiv.org/pdf/2209.09387))，以及 Coffin–Manson 疲劳后处理 ([J Mater Sci 2018](https://link.springer.com/article/10.1007/s10854-018-9384-6))；从封装级到单孔可用子模型衔接 ([Micromachines 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10456845/))。UT Austin 早就指出，软衬层对分层驱动力的影响"取决于裂纹长度，有两种方向" ([ECTC 2010](https://sites.utexas.edu/ruihuang/wp-content/uploads/sites/6034/2021/03/ECTC2010.pdf))。迄今没有一项工作把粘弹性衬层、Cu 塑性和自由边内聚力界面放进同一个模型。

被忽视的是口径问题。各研究的百分比分别基于 TGV 边缘 von Mises 应力、玻璃最大主应力、ERR 或近壁环向应力，载荷有稳态降温，也有层压升温，彼此不可比。本报告用项目前期的自编轴对称弹塑性 FEM（d = 50 µm、板厚 300 µm、节距 150 µm、GC-F 微晶玻璃基板，25→400→25 °C）复算了几种策略，比较"近壁中面环向应力"（前期报告采用的指标）与全局峰值：

| 方案（GC-F 基板） | 近壁中面 σθ（MPa） | 全局最大 σθ（MPa，位置） | 全局最大主应力（MPa） | 退火后界面残余 σr 最大值（MPa） |
|---|---|---|---|---|
| 实心 Cu 基准 | 316 | 336（孔口表面） | 353 | 94 |
| 2 µm 聚合物衬层（3 GPa、40 ppm/K） | 215（−32%） | 308（−8%） | 341（−3%） | 65（−31%） |
| 8 µm 共形 Cu | 46（−85%） | 154（−54%） | 234（−34%） | 197（孔口自由边；中面仅 49） |
| 原相环（内侧 50 GPa、9 ppm/K、宽 5 µm） | 100（−68%） | 236（−30%，相环外缘中面） | 283（−20%） | 82（−13%） |

结论很明确：**近壁指标把聚合物衬层的收益放大了约 4 倍，把相环的收益放大了约 2 倍**，峰值被推到孔口自由边或相环外缘。共形 Cu 的"残余径向应力翻倍"出现在孔口奇异角点，数值依赖网格。中面的残余径向应力则随 Cu 壁厚单调上升：4、8、12 µm 时分别为 18、49、75 MPa。这一趋势与 Corning"壁厚越大越易出现环向裂纹"的实验一致 ([TDMR 2021](https://ieeexplore.ieee.org/document/9481891/))。由此也可看出，前期报告把共形 Cu 的近壁环向应力（46 MPa）与 Corning 的径向起裂阈值（140 MPa）直接对比，属于指标错配。今后应同时报告全局最大主应力及其位置、沿潜在裂纹路径的 K/ERR，以及自由边界面 ERR，并且升温、降温两个阶段都要报告。

## 每降一分应力，都要付出 Cu 截面、热预算与气密的代价

在钻孔直径固定时，任何侧壁衬层都会吞噬 Cu 截面。下表按均匀环形衬层计算（R ∝ 1/(D−2t)²），这一账目对小孔尤其残酷：

| 孔径 D（µm） | 衬层厚 t（µm） | 剩余 Cu 面积 | 直流电阻变化 |
|---|---|---|---|
| 50 | 1 | 92% | +8.5% |
| 50 | 5 | 64% | +56% |
| 20 | 1 | 81% | +23% |
| 20 | 2 | 64% | +56% |
| 10 | 2 | 36% | +178% |

同样比例也适用于热通孔的轴向热阻，以及固定电流密度下的载流能力。毫米波下趋肤深度只有约 0.2–0.4 µm，导体损耗按周长而非面积缩放，RF 导体损耗的增幅相应小于直流电阻的增幅。共形结构的射频代价已有实测：30 GHz 下单个 TGV 对 CPW 插损的贡献，共形为 0.48 dB，部分填充 0.34 dB，全填 0.23 dB ([IEEE EPS TC](https://eps.ieee.org/wp-content/uploads/2025/11/Glass_Substrates_Adv_Substrates_TC_UPDATED_Nov25.pdf))。衬层材料的 Df 决定它是帮忙还是添乱。BCB 的 Df 为 0.0008 ([Cyclotene 4000](https://kayakuam.com/wp-content/uploads/2024/05/888_00008_DuPont_Cyclotene_4000_Series_DS3000.pdf))，在 11–65 GHz 的 tanδ 为 0.001–0.009 ([ResearchGate](https://www.researchgate.net/publication/225360912_Benzocyclobutene_as_Substrate_Material_for_Planar_Millimeter-Wave_Structures_Dielectric_Characterization_and_Application))；Parylene-N 到 60 GHz 的 tanδ 低于 0.0006 ([Purdue](https://engineering.purdue.edu/~yep/Papers/IEEE%20Trans%20Advanced%20Packaging_2009.pdf))；SU-8 在 1 GHz 时已达 0.015，200 GHz 时 0.027 ([ResearchGate](https://www.researchgate.net/publication/273392849_Permittivity_and_Loss_Characterization_of_SU-8_Films_for_mmW_and_Terahertz_Applications))。GT 的玻璃毫米波封装中，Df = 0.02 的阻焊层使仿真线损耗增加约 50% ([TMTT 2020](https://tentzeris.ece.gatech.edu/tmtt20_atom.pdf))。在 Si 中，低 k 或聚合物衬层是电学收益：电容降低 27.6% ([ResearchGate](https://www.researchgate.net/publication/258672942_Through_Silicon_Via_Fabrication_with_Low-k_Dielectric_Liner_and_Its_Implications_on_Parasitic_Capacitance_and_Leakage_Current))，聚合物嵌入通孔在 50 GHz 的插损最多降低 80% ([GT news](https://hg.gatech.edu/node/280901))。但这些收益来自把电场与导电 Si 隔开，玻璃本身已是低损耗绝缘体，这部分收益基本不存在。调研组的同轴估算（非文献数据）显示，2 µm BCB 在玻璃中只使通孔电容降低约 11%，阻抗升高约 9%，需在阻抗设计中补偿。

热与热预算是聚合物路线的硬约束。Parylene-C 的热导率仅约 0.10 W/m·K，退火后约 0.18 ([arXiv 2026](https://arxiv.org/abs/2603.03737))。不过玻璃本身 k ≈ 1，≤2 µm 的薄衬层对横向热阻影响有限，热通孔的主要损失仍是 Cu 截面。更致命的是耐温。Parylene AF4 连续使用温度 350 °C、短时 450 °C ([Fraunhofer ENAS](https://www.enas.fraunhofer.de/content/dam/enas/Dokumente/English/Downloads/factsheets/ParylenDeposition_EN_FactSheet_FraunhoferENAS.pdf))，Parylene HT 与之相当 ([SCS](https://www.unmannedsystemstechnology.com/wp-content/uploads/2021/07/SCS-Aerospace-Defense-Coatings.pdf))；HD4100 的 Tg 为 320 °C；BCB 的 Tg >350 °C，CTE 为 42 ppm/K ([Cyclotene 4000](https://kayakuam.com/wp-content/uploads/2024/05/888_00008_DuPont_Cyclotene_4000_Series_DS3000.pdf))。而 Corning 的无裂纹退火要升到约 420 °C ([MR 2021](https://www.sciencedirect.com/science/article/abs/pii/S0026271421000585))。这意味着带聚合物缓冲的 TGV 必须把 Cu 退火压到 ≤300–350 °C，代价可能是更高的残余应力和后续凸出。Parylene 膜本身在退火中也会从约 −20 MPa 压应力转为最高约 +53 MPa 拉应力 ([academia.edu](https://www.academia.edu/20627875/Stress_in_thermally_annealed_parylene_films))。

湿气与气密是玻璃特有的代价，因为气密性和低吸湿正是玻璃的卖点。PI 薄膜平衡吸水率约 2.5–2.7%，绝缘性随湿度显著下降 ([PMC](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10892007/))；BCB 在 30–84% RH 下吸水仅 0.058–0.14 wt% ([UCSB](https://wiki.nanofab.ucsb.edu/w/images/7/72/BCB-cyclotene-3000-revA.pdf))。Parylene-N 在 135 °C/85% RH/96 h HAST 后多个界面开裂；对 <2 µm 的导体间距，吸水率应低于约 0.1% ([Polymers 2023](https://www.mdpi.com/2073-4360/15/19/3895))。Parylene-C 的水汽透过率约 8 g/m²/day ([bioRxiv](https://www.biorxiv.org/content/10.64898/2026.02.24.707821v1.full))。由此推断，聚合物环和气隙都会在相邻 TGV 之间打开湿气、离子迁移和类 CAF 通道，并破坏 Corning 依靠 Ti 粘附层获得的 He 气密 ([US 11152294](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11152294))；这一点目前尚无直接测量。Intel 申请多孔 Cu 衬层的动机之一，正是聚合物衬层会从侧壁剥离，且可压缩衬层占用电镀空间 ([Intel porous Cu liner](https://trea.com/information/porous-copper-liner-for-through-glass-via-tgv-glass-cores/patentapplication/edc94632-2fe9-410d-b95d-12772cd3acf4))。成本方面，ALD 被评为共形性优但产能低、设备贵 ([Park 2026](https://www.mdpi.com/2072-666X/17/6/720))；Parylene CVD、层压重钻、BCB 填充在面板级的成本与节拍，均无公开数字。

## 可靠性证据止步于千次温循，HAST、气密与电迁移仍是空白

把证据按强度排序，最上层是带对照组的实验，目前只有 GT Demir 2017（聚合物层压对比裸玻璃，前者消除了分层和裂纹） ([FIU](https://discovery.fiu.edu/display/pub135653))，以及《电子与封装》070103 的"实验表明热应力可靠性更好"，后者条件不明 ([researching.cn](https://m.researching.cn/articles/OJb7b8695062740314))。第二层是没有缓冲层对照、但工艺接近的通过性数据：GT 共形 TPV 3000–4000 次循环 ([academia.edu](https://www.academia.edu/119963275/Reliability_of_Copper_Through_Package_Vias_in_Bare_Glass_Interposers))；via-first 结构 1000 次 TC 加 96 h HAST ([TCPMT 2017](https://www.researchgate.net/publication/313466210_Via-First_Process_to_Enable_Copper_Metallization_of_Glass_Interposers_With_High-Aspect-Ratio_Fine-Pitch_Through-Package-Vias))；厦门大学部分填充 TGV 在 −40/125 °C 100 次循环后无凸出、无界面开裂 ([腾讯新闻转载](https://news.qq.com/rain/a/20230916A017AJ00))。第三层是 TSV 类比：BCB 衬层 TSV 在 40 次 −65/150 °C 热冲击后漏电仍为 pA 级 ([MR 2013](https://www.sciencedirect.com/science/article/abs/pii/S0026271413000036))。产业侧只有两条信号：Shinko 边缘涂层在 260 °C 回流后抑制 SeWaRe ([Shinko](https://www.shinko.co.jp/english/news/2026/07/b2e0e1c9fadd06989a3ba3940788615cdb6ddaf4.php))；ISTFA 2026 一篇论文称"调节弹性模量与厚度的应力缓冲层"抑制了金属化后孔间裂纹，并经 TC 与 HAST 验证，但作者、单位和材料均未公开 ([ISTFA 2026](https://asm.confex.com/asm/istfa26/webprogram/Paper66092.html))。综述还给出两条设计相关数据：TGV 节距 ≥2 倍孔径可把相邻孔相互作用降到最小，按 4 倍节距设计的样品经 3000 次循环电阻稳定；另一研究在 300 次热冲击后于 TGV–RDL 处出现玻璃开裂 ([Chips 2025](https://www.mdpi.com/2674-0729/4/3/37))。

缺口比证据更多。缓冲 TGV 的 HAST/uHAST、THB、≥1000 h HTS、电迁移、He 漏率、多次 260 °C 回流、Weibull 断裂统计，在检索中全部为零。更值得注意的是失效迁移现象：Corning 和厦门大学的数据都显示，玻璃开裂一旦被控制，失效就转到 Ti/Cu 界面，而且在湿热条件下最先暴露 ([MR 2022](https://www.sciencedirect.com/science/article/abs/pii/S0026271422003079); [CNKI](http://dbase2.gslib.com.cn/KCMS/detail/detail.aspx?filename=JBXK202310018&dbcode=CJFD&dbname=CJFD2023))。因此，缓冲层的鉴定不能只数裂纹，必须把界面在 HAST 中的完整性列为同等级判据。设备厂商白皮书也提醒，Cu 填充后的热循环会在玻璃芯中产生延迟到后段才扩展的应力裂纹 ([Onto Innovation](https://ontoinnovation.com/wp-content/uploads/2025/08/Intelligent-Innovation-The-Long-Climb-Formatted.pdf))。

## Intel 专利铺满通孔侧，量产披露却只见边缘涂层

Intel 是 TGV 缓冲专利最密集的申请人，2023–2026 年的申请覆盖五种策略。第一是柔性或低模量衬层：聚电解质层层自组装、溶胶–凝胶、纳米乳液缓冲层，以及聚合物填孔 ([US20250183182A1](https://patents.google.com/patent/US20250183182A1/en))；多孔 Cu 衬层，要求缓冲环模量低于通孔 ([trea](https://trea.com/information/porous-copper-liner-for-through-glass-via-tgv-glass-cores/patentapplication/edc94632-2fe9-410d-b95d-12772cd3acf4))；多孔衬层，以及含碳、β-Ti 合金、水凝胶加 MXene 种子等衬层 ([Justia Bai Nie](https://patents.justia.com/inventor/bai-nie))；还有 Kamgaing 署名的"聚合物 TGV 缓冲层"，2026-06-25 公开 ([Justia](https://patents.justia.com/company/intel?page=9))。第二是 CTE 中间层：孔内设 Ti/Pt/W/FeNi36"热膨胀层"（单一二手来源，未核实） ([鉅亨](https://hao.cnyes.com/post/256887))，以及"CTE 小于导体的缓冲层"和以目标 CTE 设计的多层填充 ([Justia](https://patents.justia.com/company/intel?list=applications&page=5))。第三是自底向上电镀形成的侧壁气隙。第四是双层或多层有机/无机衬层 ([Patsnap CN122249077A](https://eureka.patsnap.com/patent/CN122249077A); [Patsnap DE102025140880A1](https://eureka.patsnap.com/patent/DE102025140880A1))。第五是玻璃芯边缘工程：有机面板包埋、侧壁倾角 >90°、边缘保护和裂纹自愈材料 ([Justia](https://patents.justia.com/inventor/whitney-bryks); [US 2025/0201732](https://patents.justia.com/patent/20250201732))。路线如此分散，说明 Intel 在公开层面尚未收敛到单一方案。

其他玩家的专利多在通孔之外。Corning 主攻退火曲线和气密全填。Toppan、疑似 DNP 的专利族和京东方做的是平面应力层。Yield Engineering Systems 的介电衬层专利要求抗拉强度 >约 8 MPa、介电损耗 <约 0.002，用于增强 Cu–玻璃附着 ([US 12087623](https://patents.justia.com/patent/12087623))。SKC 的专利只规定通孔区与非通孔区的应力差 P ≤1.5 MPa，没有缓冲层 ([US 11437308](https://patents.justia.com/patent/11437308))。原 IBM（现 Adeia）的专利在衬底表面设带开口的低模量缓冲层，不限于玻璃 ([US10325839](https://patents.google.com/patent/US10325839))。Georgia Tech Research 申请了面板切割后自动化边缘涂覆 ([WO2025208144A1](https://patents.google.com/patent/WO2025208144A1/en))。一件标题为"带 TGV 的微晶玻璃基板"的申请受让人未能确认 ([Justia 20240351945](https://patents.justia.com/patent/20240351945))。三星电机、LG Innotek、AGC、SCHOTT、NEG、台积电、欣兴和应用材料均未检出明确的 TGV 缓冲层专利，但检索未覆盖 KIPRIS、J-PlatPat 和 CNIPA，不能据此断定不存在。

量产侧，没有任何公司公开确认在大批量中使用通孔级缓冲衬层。Intel 在 NEPCON 2026 展示 78×77 mm、10-2-10 叠层的厚芯玻璃基板并宣称"No SeWaRe"，方法未披露 ([TrendForce](https://www.trendforce.com/news/2026/01/26/news-intel-reportedly-presents-first-thick-core-glass-substrate-with-emib-targeting-ai-data-centers/))。Shinko 的 22 层产品用树脂加固边缘 ([TrendForce](https://www.trendforce.com/news/2026/08/18/news-glass-substrate-war-heats-up-shinko-electric-advances-22-layer-product-as-samsung-reportedly-faces-ramp-up-uncertainty/))。Absolics 样品在台湾做封装级可靠性认证，早期曾"每隔几天碎数百片面板" ([TrendForce](https://www.trendforce.com/news/2026/05/08/news-skc-said-to-speed-glass-substrate-mass-production-by-year-end-advances-new-non-embedding-tech-for-u-s-client/); [IRZ](https://irz.fr/en/articles/verre-remplace-pas-encore-organique-en/))。DNP 采用孔壁粘附的共形 TGV（AR >9），计划 2028 财年量产 ([eeNews](https://www.eenewseurope.com/en/dnp-improves-chip-packages-with-glass-cored-substrate/); [TrendForce](https://www.trendforce.com/news/2025/12/22/news-dnp-accelerates-tgv-glass-substrate-push-with-late-2025-pilot-line-early-2026-sample-shipments/))。LG Innotek 用 AI 检测微裂纹，目标 2028 年 ([DigiTimes](https://www.digitimes.com/news/a20260909VL214/lg-innotek-glass-substrate-inspection-production-2028.html))。检测设备已跟上：Spirox 的系统可在 20 min 内扫描 510×515 mm 面板的内部微裂纹 ([I-Connect007](https://iconnect007.com/article/151619/spirox-launches-highspeed-tgv-crack-inspection-system-to-support-highvolume-glass-substrate-inspection/151616/aep))。IEEE EPS 技术委员会的判断是，玻璃芯"尚未商业化，需要进一步开发" ([IEEE EPS TC](https://eps.ieee.org/wp-content/uploads/2025/11/Glass_Substrates_Adv_Substrates_TC_UPDATED_Nov25.pdf))。在产业语境里，"缓冲"目前主要指边缘保护和工艺侧措施，而不是通孔衬层。

## 国内研究集中在一期专刊：两条材料路线，均缺受控实验

国内的定量结果几乎都出自《电子与封装》2025 年第 25 卷第 7 期"玻璃通孔技术进展与应用"专刊 ([科学网](https://blog.sciencenet.cn/home.php?mod=space&uid=3415146&do=blog&id=1514708))。有机路线是 070103 号论文，作者王展博、张泽玺、杨斌、郭旭、杨冠南、张昱、黄光汉、崔成强，据检索摘要为广东工业大学团队。该文用 FEA 加实验研究玻璃与 Cu 间的有机缓冲层，1 µm 时玻璃最大主应力降低约 40% ([researching.cn](https://m.researching.cn/articles/OJb7b8695062740314))。无机路线是 070108 号论文，作者赵全禄等，据行业报道为中科院微电子所陈钏团队。该文以化学镀相容性为由选择 ZnO/TiO₂/ZrO₂，结论是 TiO₂ 最优、优于 PI，且仅有仿真 ([researching.cn](https://www.researching.cn/articles/OJ6c1dee1b5d059512); [中国粉体网](https://news.cnpowder.com.cn/85217.html))。同期两篇综述，070106（马丙戌等）和 070109（马小菡等），后者把孔壁应力集中、微裂纹扩展与界面分层列为 TGV 力学可靠性的核心问题 ([researching.cn 70109](https://m.researching.cn/articles/OJc82833288907322d))。一些二手材料把作者名写作"马秉旭""马晓晗""赵泉露"，应以期刊目录为准。

专刊之外的国内工作，以机理研究和工艺开发为主，较少直接研究缓冲层。北京工业大学秦飞与厦门大学于大全团队的综述认为，"孔内填充聚合物可缓解残余应力及热应力" ([机械工程学报 2022](https://qikan.cmes.org/jxgcxb/CN/10.3901/JME.2022.02.246))。厦门大学马盛林团队给出了 HAST 中 Ti–Cu 界面失效的实验证据 ([CNKI](http://dbase2.gslib.com.cn/KCMS/detail/detail.aspx?filename=JBXK202310018&dbcode=CJFD&dbname=CJFD2023))。厦门大学/云天的综述提出，Cu 导电浆料填充可调节 CTE ([电子与封装 2021](https://ep.org.cn/CN/10.16257/j.cnki.1681-1070.2021.0401))。2026 年发表在 *Microsystems & Nanoengineering* 上的两篇工作，把残余应力–凸出关系和长期老化机理推进到了 Nature 合作期刊级别 ([s41378-026-01162-y](https://www.nature.com/articles/s41378-026-01162-y); [s41378-026-01160-0](https://www.nature.com/articles/s41378-026-01160-0))。广工陈新/陈云团队用非对称双向脉冲电镀，180 min 内无缺陷全填 75 µm、AR 5.5 的孔 ([艾邦](https://www.ab-sm.com/a/71569))。

企业侧信息更少。京东方有三项相关成果：电镀添加剂与凸出机理研究 ([SID Digest 2025](https://sid.onlinelibrary.wiley.com/doi/abs/10.1002/sdtp.18370))，介电"柔性应力缓冲结构"专利 ([新浪财经](https://finance.sina.com.cn/stock/aigc/zl/2026-05-14/doc-inhxvpqq8741383.shtml))，以及以三维导电网格加填料替代实心 Cu 的新申请 ([搜狐](https://www.sohu.com/a/1081721135_114984))；并称已打通"低应力金属布线"和"低应力切割"，送样 24 层载板 ([新浪](https://k.sina.cn/article_5952915720_162d24908067050a02.html))。通格微把附着力不足、微裂纹扩展和填充空洞列为金属化难点，称已有"数十项发明专利"，但未见具体的缓冲层专利 ([通格微](https://www.tgvtech.cn/newsdetail408.aspx))。检索中未发现华中科技大学、上海交通大学、中科院上海微系统所、电子科技大学等单位的缓冲层专题论文（CNKI/万方未能直接检索）。总体看，国内形成了"中科院微电子所无机烧结 vs 广工薄有机层"两条材料路线，但都以 FEA 为主，没有一篇给出缓冲与无缓冲 TGV 的 TC/HAST 失效周期对比；而产业实践更多走部分填充路线。

## 九组矛盾表明，缓冲收益取决于量什么、在哪里量

| 矛盾 | 证据 A | 证据 B | 判断 |
|---|---|---|---|
| 软聚合物与硬无机层谁更好 | 5 µm TiO₂ −66.58%，"优于 PI" ([70108](https://www.researching.cn/articles/OJ6c1dee1b5d059512)) | 1 µm 有机层 −40% ([70103](https://m.researching.cn/articles/OJb7b8695062740314))；柔性衬层 ERR −75% ([Chips](https://www.mdpi.com/2674-0729/4/3/37)) | 载荷（层压升温 vs 退火）、厚度、指标均不同，不可比 |
| 缓冲层降低还是升高 TGV 边缘应力 | HD4100 使 TGV 边缘 −51% | 同文 structure A 使 TGV 边缘升高 ([PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC9607209/)) | 热点转移；本报告复算证实近壁指标会夸大收益 |
| 衬层/相环 CTE 应高还是低 | 低 CTE、中等刚度的 GZ-41 最好 ([Le 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12654316/))；填充物 CTE 主导应力 ([SeoulTech](https://pure.seoultech.ac.kr/en/publications/study-of-thermo-mechanical-reliability-of-tsv-for-8-layer-stacked/)) | 前期相环设计图：α_c 越高，近壁 σθ 越低 | 高 CTE 主要把应力推向外缘，全局峰值存在适中最优 |
| 共形 Cu 的径向风险 | 壁厚 <12 µm 时环向裂纹归零 ([TDMR](https://ieeexplore.ieee.org/document/9481891/)) | FEM 中 8 µm 共形 Cu 的残余 σr 翻倍 | 翻倍出现在奇异角点；中面趋势与 Corning 一致 |
| 软衬层与 Cu 凸出 | BCB 衬层增大轴向膨胀 ([MR 2013](https://www.sciencedirect.com/science/article/abs/pii/S0026271413000036)) | 低 k 衬层降低残余 pumping ([imec](https://www.researchgate.net/publication/273146056_Impact_of_oxide_liner_properties_on_TSV_Cu_pumping_and_TSV_stress)) | 可逆膨胀与塑性 pumping 是两个量，需分别报告 |
| 退火保温长短 | ≥120 min 预退火稳定凸出 ([TDMR](https://ieeexplore.ieee.org/document/9353697/)) | 长时退火积累残余拉应力并开裂 ([Wang 2026](https://www.nature.com/articles/s41378-026-01162-y)) | 存在保温窗口；两者时间尺度（h vs 百 h）不同 |
| Cu 填充率的作用 | Cu 含量几乎不改变 ERR ([Le 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12654316/)) | 应力随填充率上升 ([Zhao 2022](https://www.mdpi.com/2072-666X/13/10/1799)) | 边缘裂纹 ERR 与孔内应力是两个指标 |
| 聚合物对附着的影响 | 化学镀 Cu 在聚合物上附着更好 ([TCPMT 2017](https://www.researchgate.net/publication/313466210_Via-First_Process_to_Enable_Copper_Metallization_of_Glass_Interposers_With_High-Aspect-Ratio_Fine-Pitch_Through-Package-Vias)) | 聚合物衬层会从侧壁剥离 ([Intel](https://trea.com/information/porous-copper-liner-for-through-glass-via-tgv-glass-cores/patentapplication/edc94632-2fe9-410d-b95d-12772cd3acf4)) | Cu/聚合物界面与聚合物/玻璃界面各有其弱点 |
| 缓冲层厚度 | 1→5 µm 时升温应力持续下降 | 降温应力上升，Cu 截面减少 ([中国粉体网](https://news.cnpowder.com.cn/85217.html)) | 存在最优厚度，而非越厚越好 |

这些矛盾指向同一个根源：领域内没有统一的度量口径，也没有在相同几何下对比多种缓冲方案的受控实验。由此可以列出十个研究空白。第一，没有一项实验在同一 TGV 几何中并列比较聚合物、无机、共形和无缓冲四种方案，并给出裂纹统计。第二，没有对衬层 TGV 做过显微 Raman、同步辐射或光弹的应力实测。第三，缓冲 TGV 的 HAST、THB、He 漏率和电迁移数据为零。第四，没有在相同 TGV 上对比有无衬层的毫米波 S 参数。第五，12 µm 和 6.5 °C/min 两个阈值只在熔融石英上建立。第六，降温速率对环向裂纹的影响无人研究。第七，没有同时包含粘弹性衬层、Cu 塑性和自由边内聚力界面的模型。第八，衬层在面板级的厚度均匀性、成本与节拍不明。第九，各类 SeWaRe 方案缺少一手的定量对比。第十，微晶玻璃 TGV 的任何缓冲层数据都是空白。

## 对微晶玻璃相环的启示：靠低模量和宽度，而非一味高 CTE

### 文献支持基板选择，但要求重新定义相环的设计目标

文献对"微晶玻璃本身就是缓冲"的判断是有利的。Le & Choa 的仿真中，陶瓷玻璃的 ERR 总体低于 2 J/m² ([JMST 2024](https://link.springer.com/article/10.1007/s12206-024-0522-1))；高 CTE 玻璃（含陶瓷玻璃）比熔融石英和 Borofloat 33 更能抑制裂纹扩展 ([Micromachines 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12654316/))；Sharma 等也认为熔融石英最差、陶瓷玻璃更可靠 ([Microelectron. Eng. 2026](https://www.sciencedirect.com/science/article/abs/pii/S0167931725001303))。由此看，微晶玻璃方案的第一杠杆是高 K_IC 和可调 CTE，相环只是第二杠杆。问题在于第二杠杆的设计目标。本报告在 GC-F（E 105 GPa、α 7.5 ppm/K）和 GC-C（E 110 GPa、α 3.5 ppm/K）两种基板上复算了相环变体。模型与前期一致：d = 50 µm，相环模量和 CTE 从内侧值线性过渡到基体值，界面完全粘结，Cu 为弹塑性、不含蠕变。

| 相环（内侧 E / α / 宽度） | GC-F 全局最大 σθ | GC-F 全局最大主应力 | GC-F 残余界面 σr | GC-C 全局最大 σθ | GC-C 全局最大主应力 |
|---|---|---|---|---|---|
| 无相环 | 336 | 353 | 94 | 476 | 514 |
| 50 GPa / 9 ppm/K / 5 µm（原设计） | 236（−30%） | 283（−20%） | 82 | 354（−26%） | 394（−23%） |
| 50 GPa / 与基体同 CTE / 5 µm | 230（−31%） | 293（−17%） | 81 | 330（−31%） | 427（−17%） |
| 50 GPa / 4 ppm/K / 5 µm | 252（−25%） | 317（−10%） | 79 | — | — |
| 20 GPa / 13 ppm/K / 5 µm | 244（−27%） | 244（−31%） | 78 | — | — |
| 20 GPa / 与基体同 CTE / 5 µm | 222（−34%） | 222（−37%） | 72 | — | — |
| 50 GPa / 9 ppm/K / 12.5 µm | 179（−47%） | 259（−27%） | 69 | — | — |
| 20 GPa / 与基体同 CTE / 12.5 µm | **143（−57%）** | **178（−50%）** | **47（−50%）** | **206（−57%）** | 269（−48%） |
| 20 GPa / 9 ppm/K / 12.5 µm | — | — | — | 236（−50%） | **243（−53%）** |
| 20 GPa / 13 ppm/K / 12.5 µm | — | — | — | 262（−45%） | 262（−49%） |

（单位 MPa；括号内为相对同基板无相环的变化。）

这张表改写了前期"低模量 + 高 CTE"的反直觉规律。第一，**模量和宽度是主杠杆**：把内侧模量从 50 GPa 降到 20 GPa、宽度从 5 µm 增到 12.5 µm，两种基板的全局环向应力都降低 57%，GC-F 的残余界面径向应力也减半。第二，**CTE 存在适中最优**。高 CTE 相环自身受热膨胀，会把环向拉应力推到相环外缘，近壁数值看起来接近零，全局峰值却没有下降：GC-F 上，α 13 的相环比与基体同 CTE 的相环更差。低 CTE 同样不利，α 4 的相环让峰值回到孔口。只有在低 CTE 的 GC-C 上，适度上调到 9 ppm/K 能改善孔口表面的最大主应力，再升到 13 ppm/K 则两项指标都变差。因此，相环的 CTE 目标应定为"从基体值适度上调、平滑过渡"，方案名称也宜由"低模量高 CTE"改为"低模量、宽梯度、CTE 适配"。第三，**宽度应按孔径缩放**。12.5 µm 恰好是 D/4，与文献给出的 ERR 峰值裂纹长度（约 D/4）一致 ([Microelectron. Eng. 2026](https://www.sciencedirect.com/science/article/abs/pii/S0167931725001303))；相环需要覆盖裂纹最危险的扩展区间，而不是只覆盖近壁几微米。这些结果的局限也要说明：模型不含蠕变、相环孔隙和缺陷，孔口角点的数值依赖网格。趋势可信，绝对值需要实测标定。

### 相环外缘是新的薄弱面，界面粘结不能牺牲

峰值外移意味着相环外缘，即激光改性区与本体的过渡带，成为新的最大应力位置。这里恰恰是晶化体积变化、晶–玻失配和激光残余损伤最集中的地方。前期微结构仿真显示，镁橄榄石型晶粒界面的径向拉应力可达 +409 MPa，所以外缘的缺陷群体决定了相环的成败。因此需要三项配套措施：梯度要平滑；用全息断层扫描、声扫等手段专门检查外缘微裂纹（ISTFA 2026 的失效分析即采用全息断层扫描 ([ISTFA 2026](https://asm.confex.com/asm/istfa26/webprogram/Paper66092.html))）；Weibull 统计要按外缘位置取样。

几何可实现性也需核对。前期激光热累积仿真给出的相环半径 5–19 µm 是从激光轴算起的；对 50 µm 孔（半径 25 µm），这一区域会在刻蚀中被全部去除。要在孔壁外形成 12.5 µm 宽的相环，需要环形扫描，或在刻蚀后从孔壁向外处理。子路线 (b)"选择性浸出残余玻璃相形成多孔骨架"天然从孔壁开始，宽度可由浸出时间控制，与这一需求更吻合。阵列方面，150 µm 节距下两个 12.5 µm 相环之间仍有 75 µm 本体；若节距收紧到 2D（100 µm），只剩 25 µm，需复核孔间裂纹，ISTFA 2026 报告的正是这一失效模式。

界面粘结不能为降应力而牺牲。前期断裂力学仿真表明，Cu 芯与孔壁完全粘结时的应力强度因子只有脱粘时的 67%，即脱粘使开裂驱动力增大约 1.5 倍。这一结论直接否定了气隙和易剥离聚合物衬层用于本方案。按 GC-F 估算，一个约 0.1 µm 的气隙就足以在 400 °C 完全解除 Cu 对孔壁的径向推力，但同时会失去粘结对裂纹的屏蔽和气密性。多孔相环的优势在于提供机械锚固，这与多孔 ZnO 锚固获得 >6.8 N/cm 剥离强度的机理相同 ([JECS 2025](https://iopscience.iop.org/article/10.1149/1945-7111/ae02c9))。但 Ti/Cu 界面在 HAST 中最先失效 ([MR 2022](https://www.sciencedirect.com/science/article/abs/pii/S0026271422003079))，所以多孔相环上的金属化宜采用带 TiN 阻挡的叠层，或 ALD TiO₂/TiN/Ru/Cu 叠层 ([MSSP 2025](https://www.sciencedirect.com/science/article/abs/pii/S1369800125010224))，避免 Ti 与 Cu 直接接触。

### 子路线 (c) 的聚合物浸渗要重新权衡

在多孔骨架中浸渗 PI 或 Parylene，会同时撞上三道墙。第一是热预算：Parylene HT/AF4 连续使用上限 350 °C，HD4100 的 Tg 为 320 °C，而方案的验证工况是 400 °C 退火 ([Fraunhofer ENAS](https://www.enas.fraunhofer.de/content/dam/enas/Dokumente/English/Downloads/factsheets/ParylenDeposition_EN_FactSheet_FraunhoferENAS.pdf); [HD4100](https://www.hdmicrosystems.com/products/hd4100))。第二是湿气：PI 吸水率 2.5–2.7%，会在孔间打开类 CAF 通道 ([PMC](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10892007/))。第三是 CTE：聚合物 35–42 ppm/K 会把相环 CTE 推得过高，而复算表明过高的 CTE 没有收益。更稳妥的做法是用 ALD 氧化物封孔，或做无机致密化，让骨架保持"低模量、CTE 适配"。如果坚持用聚合物，就把 Cu 退火压到 ≤350 °C，并用 300 °C 工况重做断裂判据。射频方面，相环相当于一层同轴介质壳：多孔相环降低局部 Dk，会使阻抗上移，需纳入 50 Ω 节距/孔径设计；相环的 Df 不得高于基体，否则会抵消微晶玻璃的低损耗优势（参照 SU-8 级材料的损耗 ([ResearchGate](https://www.researchgate.net/publication/273392849_Permittivity_and_Loss_Characterization_of_SU-8_Films_for_mmW_and_Terahertz_Applications))）。与任何侧壁衬层相比，相环最大的结构优势是**不占 Cu 截面**：直流电阻和热通孔热阻都不受影响。

### 实验设计、对照组与知识产权

文献的最大空白，恰好是本方案能填补的：在相同几何下并列比较多种缓冲方案的受控实验。实验设计需要补强四处。第一，把升温速率（≤6.5 °C/min 与快速升温）和预退火保温列为显式因子，以区分相环收益与工艺收益，并在微晶玻璃上重新建立这两个阈值 ([MR 2021](https://www.sciencedirect.com/science/article/abs/pii/S0026271421000585))。第二，所有组统一报告全局最大主应力及其位置、沿裂纹路径的 K/ERR，以及升温、降温两阶段数据，并用显微 Raman 或同步辐射横跨相环外缘测量应变。第三，可靠性矩阵中 HAST 与 He 漏率要与裂纹率同等加权。第四，增设电镀 Ni-Fe 填充对照组：其 CTE 7.27 ppm/K 与 GC-F 的 7.5 ppm/K 几乎匹配，可作为信号孔的"源头消失配"基准 ([JMST 2026](https://www.sciencedirect.com/science/article/abs/pii/S1005030225011983))。

知识产权需要提前排查。Intel 的申请中有"导体与玻璃芯之间、CTE 小于导体的缓冲层"和"模量低于通孔的环形缓冲" ([Justia](https://patents.justia.com/company/intel?list=applications&page=5); [trea](https://trea.com/information/porous-copper-liner-for-through-glass-via-tgv-glass-cores/patentapplication/edc94632-2fe9-410d-b95d-12772cd3acf4))。一个 CTE 为 7.5–9 ppm/K（小于 Cu 的 17）、模量 20–50 GPa 的相环，在字面上可能落入这些权利要求。Corning 的升温速率专利族明确覆盖"微晶玻璃制品" ([US 12515977](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12515977))，本方案的退火工艺若采用类似曲线，存在实施风险。建议把权利要求锚定在"基体内原位、激光或浸出形成的晶相分数梯度"这一特征上，不使用"缓冲层"表述；同时补检 KIPRIS、J-PlatPat 和 CNIPA。

## 结论

这次调研最重要的新认识是：TGV 应力缓冲的瓶颈不在概念，而在**口径与对照**。多数 40–70% 的降幅只是在近壁某一点上测得的。复算表明，同一缓冲方案在全局峰值上的收益往往只有近壁数字的一半甚至四分之一，热点被推到孔口自由边、相环外缘或 RDL 边缘。与此同时，玻璃开裂一旦被压住，失效就迁移到 Ti/Cu 等界面，并在 HAST 中最先暴露。所以，下一代缓冲层研究的胜负手不是再提出一种新材料，而是同时证明三件事：全局峰值和 ERR 下降，界面在湿热中保持完整，气密性不被破坏。目前没有任何公开工作同时做到这三点。

对本项目而言，相环的价值主张需要从"反直觉的高 CTE"改写为"基体原生、不占 Cu 截面、保住粘结与气密的宽梯度柔性区"。它的成败取决于两件事：一是相环外缘过渡带的缺陷群体，二是宽度能否做到约 D/4，而不是近壁应力能压到多低。最值得优先做的实验是在小试片上制作 2–3 种宽度的相环，用 Raman 或同步辐射横跨外缘测应变，再在不同升温速率下统计 400 °C 退火后的裂纹率。这个实验能同时检验本报告复算的结论，并在微晶玻璃上建立第一组缓冲阈值，是文献中尚不存在的数据。
