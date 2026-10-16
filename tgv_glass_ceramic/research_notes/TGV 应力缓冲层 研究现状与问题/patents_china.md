# TGV / 玻璃芯基板应力缓冲层：专利格局、中国研究与产业现状（2015–2026）

> Method note: direct page fetching (WebFetch/curl) was blocked in this session: DNS failures, and the egress proxy returned 403 for asm.confex.com, m.researching.cn, patents.google.com, patents.justia.com and hao.cnyes.com. Every finding below therefore comes from search-engine result text (titles, snippets, search-tool summaries) of the cited URLs. I could not open primary full texts or patent claims, so claim scope, thicknesses and numbers should be checked against the originals before they go into a final report. Items with a single secondary source are marked "(unverified)".

## Q1. Patents (2015–2026) from major players on buffer / stress-relief layers or structures around TGVs or at glass/build-up interfaces

### Takeaway
Intel has by far the densest public filing activity on TGV-level stress buffers. Its 2023–2026 applications cover compliant/porous liners, polyelectrolyte or sol-gel sidewall buffers, double and multilayer liners, CTE-intermediate metal "thermal expansion layers", bottom-up plating that leaves a controlled sidewall air gap, and glass-core edge-stress and edge-protection structures. Other players' patents mostly address (a) Cu-fill/anneal process control (Corning: heating-rate profiles to suppress radial and circumferential cracks; hermetic fully-filled vias), (b) planar stress-relief layers between the glass and the build-up/plating (Toppan: compressive dry-coated insulator; a "through electrode substrate" family, probably DNP: inorganic stress-relaxation layer; BOE: dielectric "flexible stress buffer" layer), or (c) adhesion/dielectric liners (Yield Engineering Systems). I found no CN patent from 沃格/通格微, 三叠纪, 云天, 中科院微电子所, 厦门大学 or 华中科技大学 that explicitly claims a TGV buffer layer. BOE's CN122008643A was the only Chinese buffer-type filing I could identify.

### Cited Findings

**Intel (US/DE applications; glass-core TGV buffers)**
- **US 2025/0183182 A1, "Microelectronic assemblies with through-glass via stress alleviation in glass cores" (Intel).** The figures show cationic and anionic polyelectrolytes deposited on TGV-opening sidewalls to form a buffer layer, and polymer-filled TGVs. The stated benefit is "reduced susceptibility to fracture" of glass cores. The family also covers polymer nanoemulsion and sol-gel buffer routes. — [Google Patents US20250183182A1](https://patents.google.com/patent/US20250183182A1/en); a Patsnap summary characterizes it as a buffer layer between the conductive material and the glass core, "with CTE smaller than the conductive material" (AI summary, unverified) — [Patsnap DE102025140880A1 / related](https://eureka.patsnap.com/patent/DE102025140880A1)
- **DE102025140880A1 (Intel, per Patsnap).** A partial lining on the sidewalls of TGVs in glass cores "acts as a buffer layer, reducing stress by separating the glass from conductive filler materials." — [Patsnap DE102025140880A1](https://eureka.patsnap.com/patent/DE102025140880A1)
- **US 2025/0105132, "Porous Copper Liner for Through Glass Via (TGV) Glass Cores" (Intel), filed 2023-09-26.** Inventors: Pratyush Mishra, Pratyasha Mohapatra, Srinivas V. Pietambaram. The buffer is a ring around the via whose elastic modulus is lower than the via's. It is meant to accommodate CTE-mismatch stresses that can crack the glass during annealing. — [Trea: Porous copper liner for TGV glass cores](https://trea.com/information/porous-copper-liner-for-through-glass-via-tgv-glass-cores/patentapplication/edc94632-2fe9-410d-b95d-12772cd3acf4) (publication number from search summary; unverified)
- **US 2025/0132239, "Porous liners for through-glass vias" (Intel), filed 2024-12-30.** A porous material between the conductive fill and the hole sidewall. — [Justia, inventor Bai Nie listing](https://patents.justia.com/inventor/bai-nie)
- **Other Intel TGV-liner filings seen only in Justia listings; numbers not obtained (unverified):**
  - A carbon-containing via liner between the glass and the fill, filed Dec 2022.
  - A "buffer layer between the conductive material and the glass core, wherein a CTE of the buffer layer is smaller than a CTE of the conductive material", filed Nov 2023.
  - A liner made of a beta-titanium-alloy layer, a polymer-hydrogel layer plus an MXene seed, organic + metal layers, or an organic layer between two metal layers.

  — [Justia, inventor Bai Nie listing](https://patents.justia.com/inventor/bai-nie)
- **"Bottom-up plating of through-glass vias" (Intel).** Application US18/985,261, filed 2024-12-18, published 2026-06-18. The publication number conflicts between sources: Patsnap gives US20260173267A1 and Justia/艾邦 give US 2026/0173908 A1. The sidewall has no full seed layer, so Cu grows from the via bottom and leaves a controlled air gap at the sidewall as a stress buffer. An optional composite low-modulus liner provides "secondary stress relief". The application describes three manufacturing routes: subtractive etch, mSAP and flowable cavity fill. It contains no measured data. — [Patsnap US20260173267A1](https://eureka.patsnap.com/patent/US20260173267A1); [艾邦半导体网](https://www.ab-sm.com/a/75754)
- **US 2026/0165174 A1, "Coefficient of thermal expansion matching in semiconductor package substrate through glass vias" (Intel), published 2026-06-11.** A second "thermal expansion layer" inside the TGV mitigates the glass–Cu thermo-mechanical mismatch. The layer can be Ti, Pt, W, FeNi36 (Invar) or their alloys. The article cites Cu CTE ≈16.5 ppm/°C against 3–10 ppm/°C for packaging glass. Single secondary source (unverified). — [鉅亨 cnyes 文章](https://hao.cnyes.com/post/256887)
- **A related Intel filing tunes the fill itself:** a "multi-layer fill material… to approximate a desired or target CTE with respect to the glass core". Number not obtained. — [Search result citing Intel filings / Justia](https://patents.justia.com/company/intel?list=applications&page=5)
- **Intel double-liner application.** It alleviates "stresses in through-glass vias by providing double liner materials". It is in a July 2026 publication cluster that also contains 20260198337 (heterogeneous TGVs) and 20260198335 (double-sided bottom-up plating with a peelable core). The search summary named 20260198346 (double liner) and 20260173934 (multilayer organic/inorganic liner), but neither number could be confirmed (unverified). — [Justia Intel assignee listing](https://patents.justia.com/assignee/intel-corporation?page=29)
- **US 2025/0112175, edge stress reduction in glass cores (Intel).** Filed 2023-09-29, published 2025-04-03. Inventors include Brandon C. Marin, Whitney Bryks and Yosef Kornbluth. The abstract gives three examples: the glass core embedded in a panel of organic material, sidewall angle >90°, and a pattern of material on the sidewalls. — [Justia inventor listings](https://patents.justia.com/inventor/whitney-bryks)
- **Other Intel glass-core edge/crack filings:**
  - US 2025/0022786, "Methods and apparatus for edge protected glass cores". — [Justia 20250022786](https://patents.justia.com/patent/20250022786)
  - US 2025/0201732, "Microelectronic assemblies with crack-healing materials for glass cores". — [Justia 20250201732](https://patents.justia.com/patent/20250201732)

**Corning (hermetic / fully-filled Cu TGV; anneal profile)**
- **Hermetic via families.** WO2019199677 / US 11,152,294, "Hermetic metallized via with improved reliability", and US 11,171,094 B2, "Hermetic fully-filled metallized through-hole vias", cover glass or glass-ceramic substrates with vias hermetically sealed by a metal connector. Copper–glass CTE mismatch causes radial and circumferential cracks during high-temperature processing. On cooling, Cu contracts faster and pulls on the glass, which drives circumferential cracks. — [WO2019199677A3](https://patents.google.com/patent/WO2019199677A3/en); [US11152294 PDF](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11152294); [US11171094 PDF](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11171094)
- **Anneal heating-rate family.** CN113474311A/B, US 11,760,682 and US 12,515,977, "Glass or glass ceramic articles with copper-metallized through holes and processes for making the same". The patents show radial cracking at constant heating rates of 26.0, 13.0 and 8.7 °C/min. They claim that a low average heating rate above a "first temperature", where crack risk becomes significant, allows stress relaxation, lowers hoop stress and reduces or eliminates radial cracks. Circumferential stress rises roughly linearly with temperature, and cracks between adjacent Cu-filled holes can link up. Exact ramp values and temperatures were not obtained. — [CN113474311B](https://patents.google.com/patent/CN113474311B/zh); [US11760682 PDF](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11760682); [US11152294 PDF](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11152294)
- **WO2020061437A1 / US 12,200,875 B2, "Copper metallization for through-glass vias on thin glass".** Claim details not obtained. — [WO2020061437A1](https://patents.google.com/patent/WO2020061437A1/en)
- **Partially-filled (conformal) Corning approach.** A review describes hour-glass-shaped vias with a helium-tight adhesion layer on the sidewalls near the via entry. — [MDPI review "A Review of Glass Substrate Technologies"](https://www.mdpi.com/2674-0729/4/3/37); [Corning IMAPS TGV slides](https://www.corning.com/media/worldwide/cdt/documents/IMAPs_Corning_TGV_FINAL.pdf)

**Toppan, DNP(?), SKC, YES, IBM/Adeia**
- **US 11,516,911 B2, "Glass circuit board and stress relief layer" (Toppan Printing).** Inventor Masahiko Kijima; application US17/101,677; published as US20210076491A1. The stress-relief layer is an insulator formed by a dry coating method and puts the glass in compressive residual stress at room temperature. It sits under the seed and electroplated Cu, on both surfaces of the glass, which has through-holes. It reduces cracking, fracture and warpage caused by Cu plating expansion and shrinkage during manufacture and thermal cycling. — [Google Patents US11516911B2](https://patents.google.com/patent/US11516911); [EPO family record EP3806140A4](https://data.epo.org/gpi/EP3806140A4)
- **US 11,195,768 and US 12,394,680, "Through electrode substrate, manufacturing method thereof and mounting substrate".** An inorganic, insulating stress relaxation layer (37) sits between the glass substrate and the organic insulation layer (36) of the wiring layer. It may also sit between the insulation layers of the first and second wiring layers. The organic layer pulls on the glass while the inorganic layer compresses it, which prevents warpage. The assignee could not be confirmed from the results; the title style suggests Dai Nippon Printing (unverified). — [US11195768 PDF](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11195768); [US12394680 PDF](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12394680)
- **SKC / Absolics.**
  - US 10,903,157 (SKC, granted 2021-01-26): a glass core with a core via and an insulating layer around the conductive pattern.
  - US 11,437,308 (packaging glass substrate): specifies a stress difference value P ≤1.5 MPa between via and non-via regions.
  - A related SKC filing gives a via-line stress difference ratio Kv ≤6.

  No explicit buffer layer was found in SKC filings. — [US10903157B2](https://patents.google.com/patent/US10903157B2/en); [Justia US11437308](https://patents.justia.com/patent/11437308); [US20210398891A1](https://patents.google.com/patent/US20210398891A1/en)
- **US 12,087,623 B1, "Dielectric liners on through glass vias" (Yield Engineering Systems).** Application US18/422,346; inventors Ramakanth Alapati, M Ziaul Karim and Christopher Lane. A low-viscosity curable polymer is coated on the TGV inner wall and cured into a dielectric liner with tensile strength >~8 MPa and dielectric loss <~0.002. Cu is then deposited on the liner to improve Cu–glass adhesion. — [Justia 12087623](https://patents.justia.com/patent/12087623); [Google Patents US12087623](https://patents.google.com/patent/US12087623)
- **US 10,325,839 B2 / US 10,593,616 B2, "Reduction of stress in via structure" (original assignee IBM, current Adeia).** A stress-buffer layer on the substrate around the via hole. The conductive body intrudes into it, and the wiring layer is separated from the substrate surface. The substrate is generic, not specifically glass. — [Google Patents US10325839B2](https://patents.google.com/patent/US10325839)

**Samsung Electro-Mechanics, LG Innotek, AGC, SCHOTT, NEG, TSMC, Unimicron, Applied Materials**
- Searches surfaced no SEMCO, LG Innotek, AGC, SCHOTT, NEG, TSMC, Unimicron or Applied Materials patent that explicitly claims a TGV or glass/build-up buffer layer. — [search context: SEMCO news](https://www.trendforce.com/news/2026/08/18/news-glass-substrate-war-heats-up-shinko-electric-advances-22-layer-product-as-samsung-reportedly-faces-ramp-up-uncertainty/); [Justia LG Innotek assignee page](https://patents.justia.com/assignee/lg-innotek-co-ltd)
- **US 2024/0351945, "Glass ceramic substrate with through-glass via"**, surfaced in the LG Innotek search, but its assignee was not confirmed. — [Justia 20240351945](https://patents.justia.com/patent/20240351945)
- **US 9,892,971, "Crack prevent and stop for thin glass substrates" (assignee not shown).** A protective fill layer dissipates crack energy, combined with trenches and rows of vias that divert cracks. — [US9892971 PDF](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9892971)

**Chinese (CN) patents**
- **CN122008643A, 一种玻璃基载板及其制备方法.** Applicants: 北京京东方传感技术有限公司, 京东方科技集团 and 北京京东方技术开发有限公司; published 2026-05-12. A dielectric layer between the glass and the insulating build-up layer acts as a 柔性的应力缓冲结构 (flexible stress-buffer structure). It is said to passivate the CTE jump between glass and insulating layer, reduce warpage and fracture risk from thermal stress, optimise interface morphology and raise peel strength. — [新浪财经 2026-05-14](https://finance.sina.com.cn/stock/aigc/zl/2026-05-14/doc-inhxvpqq8741383.shtml)
- **CN122825848A, 一种基板及其制作方法 (京东方科技集团), filed 2026-07.** The TGV is filled with a 3D conductive mesh structure, with conductive filler in its pores. The report does not mention a buffer or stress layer, but the design is a composite-fill alternative to solid Cu. — [搜狐](https://www.sohu.com/a/1081721135_114984)
- **CN102820262A, 一种玻璃通孔的制作及互连的方法 (older; assignee not shown).** Stacked glass wafers are bonded with polymer (PI, SU-8, BCB), then an adhesion layer is formed on the hole wall before metallisation and fill. — [Google Patents CN102820262A](https://patents.google.com/patent/CN102820262A/zh)
- **通格微 (沃格光电 subsidiary).** VP 魏炳义 publicly lists insufficient Cu adhesion, microcrack propagation and fill voids as the main metallisation problems. He says they are addressed via "材料改性、工艺参数优化、设备自主开发" with "数十项发明专利". No specific CN number or buffer claim was found. — [通格微新闻](https://www.tgvtech.cn/newsdetail408.aspx); [沃格光电新闻](https://www.wgtechjx.com/news/212.html)
- 三叠纪 (东莞): no buffer-layer patent was found. The company reports panel-level 50 µm vias at 20:1 AR with 100% plated-through fill, and wafer-level 10 µm at 50:1. — [36氪](https://www.36kr.com/p/2873312313643401); [未来半导体](http://www.fsemi.tech/cms/xinwenkuaixun/3611.html)

### Inferences
- The Intel portfolio sorts into five stress-mitigation strategies:
  1. Compliant or low-modulus liners: polymer, polyelectrolyte LbL, sol-gel, porous Cu, hydrogel.
  2. CTE-intermediate metal liners or fills: Ti/Pt/W/Invar, multilayer Invar-type fill.
  3. Decoupling by a sidewall air gap from bottom-up plating.
  4. Double or multilayer organic/inorganic liners.
  5. Glass-core edge engineering: organic panel embedding, bevelled sidewalls, edge protection, crack-healing materials.

  This breadth from 2023 to 2026 implies Intel has not converged publicly on one solution.
- Two families of "buffer" should be kept apart in the report. (a) Radial buffers between the via metal and the glass sidewall address via-level radial and circumferential cracks, Cu pumping and inter-via cracks. (b) Planar stress-relief layers between the glass surface and the build-up or plating layers (Toppan, the DNP-like family, BOE CN122008643A) address warpage and SeWaRe-type edge/interface cracks.
- Corning's approach is process-side rather than a buffer layer: anneal-ramp control and hermetic full fill. A slow ramp lets Cu creep and relax instead of loading the glass.
- Patent text found for these families shows no quantitative stress-reduction data. Quantitative claims come from the academic literature (Q2).

### Gaps
- Claims, buffer thickness ranges and moduli for the Intel applications (US20250183182, US20250105132, US20250132239, the bottom-up plating application, US20260165174, the double-liner application) could not be read; only abstracts and summaries were available.
- The publication number conflict for the Intel bottom-up plating application (US20260173267A1 vs US20260173908A1) is unresolved.
- The assignee of US11195768/US12394680 (presumed DNP) is unconfirmed.
- I found no patents from SEMCO, LG Innotek, AGC, SCHOTT, NEG, TSMC, Unimicron or Applied Materials that explicitly claim TGV buffer layers. This may be a search limitation (Korean/Japanese-language filings, KIPRIS/J-PlatPat not searched) rather than true absence.
- I found no CN buffer-layer patents from 沃格/通格微, 三叠纪, 云天半导体, 中科院微电子所, 厦门大学 or 华中科技大学. CNIPA and SooPAT could not be queried directly.

## Q2. Chinese university, institute and company research on TGV stress buffers: materials, structures, numbers, simulation vs experiment, problems

### Takeaway
The main quantitative Chinese results are in the 电子与封装 2025 Vol.25 No.7 TGV special issue.
- **070108 (赵全禄 et al.; IMECAS 陈钏 team per trade press):** sintered inorganic buffers (ZnO/TiO₂/ZrO₂). FEA gives a 66.58% glass-core stress reduction for 5 µm TiO₂; trade press reports 49.3% lower max principal stress vs pure Cu and better than a PI buffer.
- **070103 (王展博 et al., 广东工业大学):** an organic-polymer buffer. FEA gives ~40% lower glass max principal stress with a 1 µm layer, with supporting experiments.

The rest of Chinese work is mostly reviews (BJUT 秦飞 / XMU 于大全; 070106; 070109) and reliability tests of glass–Ti–Cu stacks (XMU 马盛林). Those tests identify Ti–Cu interface microcracking under HAST as the dominant failure, not glass cracking. Most buffer results are simulation-only, with limited experimental validation.

### Cited Findings

**电子与封装 2025, 25(7) "玻璃通孔技术进展与应用" special issue (identified papers)**
- **070108, 赵全禄 et al., "降低玻璃基板TGV应力的无机缓冲层方法与仿真分析" (Method and simulation analysis of an inorganic buffer layer for reducing TGV stress in glass substrates).**
  - Method: an inorganic buffer layer is sintered between the TGV glass and the Cu, and ZnO, TiO₂ and ZrO₂ are simulated by FEA.
  - Parameters varied: buffer thickness, glass core thickness and TGV diameter.
  - Result: compared with pure-Cu TGVs, glass-core stress during lamination-stage heating is reduced, with a 66.58% reduction for sintered 5 µm TiO₂.
  - Trends: thicker buffers and smaller TGV diameters lower stress.

  — [researching.cn 70108](https://www.researching.cn/articles/OJ6c1dee1b5d059512); [m.researching.cn 70108](https://m.researching.cn/articles/OJ6c1dee1b5d059512)
- **Trade-press report on the same inorganic-buffer work (attributed to 中国科学院微电子研究所 陈钏团队).**
  - Materials ZnO/TiO₂/ZrO₂ were chosen for compatibility with electroless plating; evaluation was by FEA.
  - Under lamination heating from 25 to 190 °C, the pure-Cu glass core reaches a maximum stress of 202.36 MPa.
  - TiO₂ was best, reducing max principal stress by 49.3% vs pure Cu, and "明显优于常规PI缓冲层" (clearly better than a conventional PI buffer).
  - From 1 to 5 µm buffer thickness, heating-stage stress fell steadily while cooling-stage stress rose slightly but stayed "within the safe range".
  - Core thickness (400–1200 µm) had little effect.
  - Simulation only; no experimental validation was reported.

  — [中国粉体网 2025](https://news.cnpowder.com.cn/85217.html)
- **Conflict:** the 70108 abstract gives 66.58% (5 µm TiO₂, "glass core stress") while the trade press gives 49.3% (TiO₂, "max principal stress"). They probably refer to different metrics or thicknesses; not reconciled. — [researching.cn 70108](https://www.researching.cn/articles/OJ6c1dee1b5d059512); [中国粉体网](https://news.cnpowder.com.cn/85217.html)
- **070103, 王展博 et al., "应力缓冲层对玻璃基板填孔结构内应力及可靠性的调控规律研究" (广东工业大学 per search summary).** The work uses FEA plus experiments on an organic polymer layer at the glass–Cu interface as a stress buffer. Simulation shows that a 1 µm buffer layer reduces the glass's maximum principal stress by ~40%, and experiments support improved thermal-stress reliability. This is the "1 µm → 40%" paper the brief refers to; it is 070103, not 070108 or 070109. The first author "王展博" and the affiliation 广东工业大学 come from search summaries (unverified). — [m.researching.cn 70103](https://m.researching.cn/articles/OJb7b8695062740314); [electronics & packaging site](https://ep.org.cn/CN/news/news204.shtml)
- **070106, 马丙戌, 王浩中, 钟祥祥, 向峻杉, 刘沛江, 周斌, 杨晓锋, "玻璃通孔技术及其可靠性研究现状" (review).** The brief's "马秉旭" appears to be 马丙戌. The author list comes from a search-result citation; I could not open the page (unverified). — [科学网 special-issue post](https://blog.sciencenet.cn/home.php?do=blog&id=1514708&mod=space&uid=3415146); [电子与封装 site](https://ep.org.cn/CN/news/news204.shtml)
- **070109, 马小菡, 董瑞鹏, 万欣, 贾冯睿, 龙旭, "玻璃通孔技术的力学可靠性问题及研究进展" (review).** The brief's "马晓晗" appears to be 马小菡. An excerpt says glass–metal CTE difference introduces significant thermal stress, leading to stress concentration at the hole wall, microcrack propagation and interface delamination. — [m.researching.cn 70109](https://m.researching.cn/articles/OJc82833288907322d); [mirror excerpt](https://www.xinzhorui.cn/hangye/158.html)
- **Other papers in the same issue:**
  - 070107: 孙鹏, 钟毅, 于大全, "玻璃通孔化学镀金属化研究进展".
  - 070101: 喻甜 et al., RF integration.
  - 070104: 刘晓贤 et al., IPD.

  — [科学网 special-issue post](https://blog.sciencenet.cn/home.php?do=blog&id=1514708&mod=space&uid=3415146)

**Other Chinese groups**
- **北京工业大学 (秦飞) with 厦门大学 / 云天 (于大全, 钟毅): 赵瑾, 李威, 钟毅, 于大全, 秦飞, "玻璃通孔三维互连技术中的应力问题", 机械工程学报 2022, 58(2): 246–258.** The review covers thermal-stress models for Cu fill, fully vs partially filled states and local stress concentration. It concludes that "孔内填充聚合物可缓解残余应力及热应力，具有较高的抗热应力可靠性" (polymer filling inside the via relieves residual and thermal stress and gives high thermal-stress reliability). — [机械工程学报](https://qikan.cmes.org/jxgcxb/CN/10.3901/JME.2022.02.246)
- **厦门大学 (马盛林 group): double-sided electroplated, partially filled TGV in a glass–Ti–Cu system.**
  - Tested to JEDEC: HAST, temperature cycling (−40 to 125 °C, 100 cycles) and HTS.
  - No Cu protrusion or interface cracking was reported after testing.
  - The main HAST failure mode is growth and through-propagation of Ti–Cu interface microcracks, attributed to Cu diffusing into Ti and Ti into glass, which forms micro-voids. This is also the main cause of the rising leak rate.

  — [腾讯新闻 (矢量科学 repost)](https://news.qq.com/rain/a/20230916A017AJ00); [CNKI JBXK202310018](http://dbase2.gslib.com.cn/KCMS/detail/detail.aspx?filename=JBXK202310018&dbcode=CJFD&dbname=CJFD2023)
- **厦门大学 / 云天 (陈力, 杨晓锋, 于大全), "玻璃通孔技术研究进展", 电子与封装 2021, 21(4): 040101.** Cu conductive-paste fill can tune CTE and reduce mismatch failures. The review notes that high-density TGV, metal fill and fine RDL "尚未成熟" (are not yet mature). — [电子与封装 2021](https://ep.org.cn/CN/10.16257/j.cnki.1681-1070.2021.0401)
- **广东工业大学 (陈新, 陈云 team; context, not a buffer).** Asymmetric bidirectional pulse plating achieved defect-free full-Cu fill of a 75 µm, AR 5.5 TGV in 180 min. — [艾邦半导体网](https://www.ab-sm.com/a/71569)
- **Heat-treatment study (group not identified).** Treatment temperature (100–300 °C) affects SiO₂–Ti–Cu interface stability, Cu-pillar grain orientation and the warpage of electroplated TGV substrates. — [生物通 2025-06](https://www.ebiotrade.com/newsf/2025-6/20250616150524216.htm)
- **"高性能封装玻璃基板TGV技术的研究现状、挑战与未来展望", 电子与封装 2026 (review).** Summarises microcrack control for brittle glass and thermal-stress-mismatch solutions, and notes the trend toward large-panel packaging. Authors were not obtained. — [电子与封装 2026.0139](https://ep.org.cn/CN/10.16257/j.cnki.1681-1070.2026.0139)

**International reference points (for context in synthesis)**
- **Ahmed, Okoro, Pollard, Jiang (2020, Multidiscipline Modeling in Materials and Structures).** Energy-release-rate analysis vs via design and thermal-strain mismatch; a stress buffer layer "significantly reduced" substrate cracking. — [Emerald MMMS-05-2020-0125](https://emerald.com/insight/content/doi/10.1108/MMMS-05-2020-0125/full/html)
- **Review: a thin compliant polymer liner cuts the ERR for radial cracking by >75% in FEA.** — [MDPI "A Review of Glass Substrate Technologies"](https://www.mdpi.com/2674-0729/4/3/37); [洁芯 review summary](https://jesinesz-semicon.com/nd.jsp?id=51)
- **Cu TGV in fused silica.** Circumferential cracks on cooling after a 400 °C anneal depend exponentially on Cu thickness, with no cracks below ~12 µm. This supports conformal or partially filled designs. — [UOS publication](https://pure.uos.ac.kr/en/publications/elimination-of-thermo-mechanically-driven-circumferential-crack-f/)
- **Le, Yoo, Choa (SeoulTech), Micromachines 2025, 16(11): 1256.** Top-edge cracks near the glass/RDL interface carry the highest risk, and an edge clearance ≥300 µm suppresses crack propagation. — [PMC12654316](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12654316/)
- **Low-quality AI summary: thin dielectric buffers (SiO₂, SiNx, SOG) give a 30–50% interfacial stress reduction (unverified).** — [Patsnap materials page](https://eureka.patsnap.com/materials/glass-core-substrate)

### Inferences
- Chinese buffer-layer research has two clear branches. IMECAS works on inorganic sintered oxides compatible with electroless Cu; TiO₂ is best, and the oxides are claimed to outperform PI. 广东工业大学 works on thin organic polymer layers (~1 µm gives ~40%).
- Both report max principal stress or stress in the glass from FEA. Only 070103 claims experimental support, and no paper found reports long-term reliability statistics (TC cycles to failure, HAST) for a buffered TGV.
- **Problems identified:**
  1. Thickness trade-off: the inorganic buffer lowers heating stress but raises cooling stress with thickness. Thicker buffers also shrink the Cu cross-section, raising resistance and possibly concentrating stress — a "double-edged" effect noted in a review summary (unverified attribution).
  2. Interface adhesion and diffusion: Ti–Cu microcracking under HAST in XMU tests means any added layer adds another interface that must survive humidity and bias.
  3. Process compatibility: sintering an oxide on a glass sidewall, and conformality in high-AR vias.
  4. The lack of experimental validation in most studies.
- XMU's experimental results suggest that partial or conformal fill is itself a stress-relief strategy used in Chinese practice. Industrial failure on such samples appears to shift from glass cracking to interface degradation.

### Gaps
- I could not find specific buffer-layer papers from 哈尔滨工业大学 (TGV residual stress, protrusion, thermal shock), 华中科技大学, 上海交通大学, 中科院上海微系统所, 电子科技大学, 北京大学, 大连理工 or 中电科58所/55所. Searches returned only reviews; CNKI/万方 could not be queried directly.
- Full author lists, affiliations, DOIs and figures for 070108 and 070103 are missing. The affiliation of 070108 to IMECAS 陈钏 rests on a trade-press article, and the affiliation of 070103 to 广东工业大学 on a search summary.
- The 70108 discrepancy (66.58% vs 49.3%) is unresolved without the full text.
- No experimental TC/HAST cycles-to-failure data were found for buffered vs unbuffered TGVs in Chinese literature.

## Q3. Industry status signals: who uses buffer or stress-relief layers in production, and what remains unsolved

### Takeaway
Public evidence of production use is thin and indirect.
- An ISTFA 2026 paper (Oct 2026) reports that a stress buffer layer with tuned modulus and thickness suppressed inter-via cracks in glass-core substrates, validated by TC and HAST. Its authors and company could not be identified.
- Shinko has publicly adopted resin edge coating/protection; one example quoted 95 → 49 MPa edge stress.
- Intel claims "No SeWaRe" but has not disclosed its methods.
- BOE says it has achieved "低应力" metallisation and dicing and has filed a dielectric stress-buffer patent.
- DNP relies on conformal (sidewall-adhered) TGVs.

Mass production by any player is still expected 2026–2028, glass microcracking (SeWaRe) and Cu–glass CTE mismatch remain the main unsolved problems, and no company publicly confirms a TGV-level buffer liner in high-volume production.

### Cited Findings
- **ISTFA 2026, "Comprehensive Failure Analysis and Mitigation of Glass Core Substrate Defects for Advanced AI Server Packaging" (scheduled Oct 8, 2026).**
  - Three defect modes: (1) microcracks during TGV processing, studied after laser modification and etch with holotomography; (2) cracks between vias after metallisation; (3) backside cracks after build-up.
  - Thermo-mechanical modelling showed stress concentration between vias.
  - "a stress buffer layer with tuned elastic modulus and thickness" was introduced to suppress cracking and validated with temperature cycling and HAST.
  - Authors, affiliation and buffer material were not available.

  — [ISTFA 2026 program, Paper 66092](https://asm.confex.com/asm/istfa26/webprogram/Paper66092.html)
- **Shinko Electric.**
  - Showed a 22-layer glass-core substrate (11 Cu layers per side) at Advanced Packaging Summit 2026 (July). It reinforced the substrate edges with resin or edge-protection material to disperse stress and suppress SeWaRe under thermal load. — [TrendForce 2026-08-18](https://www.trendforce.com/news/2026/08/18/news-glass-substrate-war-heats-up-shinko-electric-advances-22-layer-product-as-samsung-reportedly-faces-ramp-up-uncertainty/)
  - An earlier Shinko study found that, with a 300 µm resin layer, glass edge stress of ~95 MPa fell to ~49 MPa with an edge coating. — [TrendForce Insights](https://insights.trendforce.com/p/glass-substrate-development)
- **Intel at NEPCON Japan (Jan 22, 2026).**
  - Thick-core glass substrate with EMIB: 78×77 mm, 10-2-10 stack, two EMIB bridges, 45 µm bump pitch.
  - Claims "No SeWaRe" (no micro-cracks, including through dicing); methods not disclosed.

  — [TrendForce 2026-01-26](https://www.trendforce.com/news/2026/01/26/news-intel-reportedly-presents-first-thick-core-glass-substrate-with-emib-targeting-ai-data-centers/); [TrendForce Insights](https://insights.trendforce.com/p/glass-substrate-development)
- **Mass-production timing.** TrendForce expects Intel, TSMC, SEMCO, Rapidus and SK Absolics to reach glass-substrate mass production between 2027 and 2028. Another TrendForce item says Absolics targets 2026. — [TrendForce Insights](https://insights.trendforce.com/p/glass-substrate-development); [TrendForce 2026-05-08 on SKC](https://www.trendforce.com/news/2026/05/08/news-skc-said-to-speed-glass-substrate-mass-production-by-year-end-advances-new-non-embedding-tech-for-u-s-client/)
- **Absolics.**
  - Samples were sent to Taiwan for package-level reliability (PLR) certification, with mass production by late 2026 if it passes; other reports say 2027. — [TrendForce 2026-05-08](https://www.trendforce.com/news/2026/05/08/news-skc-said-to-speed-glass-substrate-mass-production-by-year-end-advances-new-non-embedding-tech-for-u-s-client/); [AtlasPCB](https://www.atlaspcb.com/news/news-skc-absolics-290-million-glass-substrate-semiconductor-packaging-2026/)
  - Early runs reportedly broke "hundreds of panels every couple of days", with edge chipping and cracks from drilling and dicing (secondary, citing MIT Technology Review). — [IRZ](https://irz.fr/en/articles/verre-remplace-pas-encore-organique-en/)
  - No public source describes an Absolics edge coating or buffer layer (searched).
- **SEMCO.** Ramp-up uncertainty; timeline reportedly 2H27 for glass-core material and 2028 for finished substrates. — [TrendForce 2026-08-18](https://www.trendforce.com/news/2026/08/18/news-glass-substrate-war-heats-up-shinko-electric-advances-22-layer-product-as-samsung-reportedly-faces-ramp-up-uncertainty/); [TrendForce 2026-02-03](https://www.trendforce.com/news/2026/02/03/news-samsung-reportedly-shifts-glass-substrate-project-to-business-unit-eyes-2027-ramp-up/)
- **LG Innotek.** Uses in-house AI to tackle glass-substrate microcracks and targets production around 2028. No disclosed buffer approach. — [DigiTimes 2026-09-09](https://www.digitimes.com/news/a20260909VL214/lg-innotek-glass-substrate-inspection-production-2028.html)
- **DNP.**
  - Conformal-type TGVs with metal layers adhered to the via sidewalls and AR >9:1; a proprietary method claims improved glass–metal adhesion. — [eeNews Europe](https://www.eenewseurope.com/en/dnp-improves-chip-packages-with-glass-cored-substrate/); [IEEE EPS TC deck](https://eps.ieee.org/wp-content/uploads/2025/11/Glass_Substrates_Adv_Substrates_TC_UPDATED_Nov25.pdf)
  - ECTC 2026 paper: "Development of Long-Term Reliability for Glass Core Substrates with Build-Up Layers". — [DNP ECTC 2026](https://www.global.dnp/en/news/detail/2026/05/050/)
  - Kuki pilot line; samples early 2026; mass production FY2028. — [TrendForce 2025-12-22](https://www.trendforce.com/news/2025/12/22/news-dnp-accelerates-tgv-glass-substrate-push-with-late-2025-pilot-line-early-2026-sample-shipments/)
- **BOE (京东方).**
  - Reports having run its full glass-core carrier process: high-AR TGV drilling, deep-hole Cu fill, 低应力金属布线 (low-stress metal wiring), high-layer lamination and 低应力切割 (low-stress dicing).
  - 24-layer glass carriers have been produced and sampled.

  — [新浪新闻](https://k.sina.cn/article_5952915720_162d24908067050a02.html); [网易](https://www.163.com/dy/article/L3QDV66M0556CQW3.html)
- **AGC (IEEE EPS TC).** Attributes "SeWaRe" horizontal cracking from diced glass edges to glass vs build-up CTE mismatch. Balancing core and build-up CTE may mitigate edge stress but can compromise warpage control (IMAPS). — [IEEE EPS TC deck](https://eps.ieee.org/wp-content/uploads/2025/11/Glass_Substrates_Adv_Substrates_TC_UPDATED_Nov25.pdf); [IMAPSource](https://imapsource.org/article/147120.pdf)
- **Inspection signal.** Spirox launched a TGV crack inspection system for internal microcracks after metallisation and ABF build-up: a full-panel scan of 510×515 mm in <20 min. — [I-Connect007](https://iconnect007.com/article/151619/spirox-launches-highspeed-tgv-crack-inspection-system-to-support-highvolume-glass-substrate-inspection/151616/aep)
- **MRS 2026 Spring.** Cu-filled TGVs frequently show Cu pull-out and substrate cracking at elevated temperature because of the Cu–glass CTE mismatch. — [MRS 2026 abstract](https://www.mrs.org/meetings-events/annual-meetings/archive/meeting/presentations/view/2026-mrs-spring-meeting/2026-mrs-spring-meeting-4434070)
- **Reliability data points from reviews.** A TGV pitch ≥2× diameter minimises neighbour interaction; a 4× design survived 3000 thermal cycles with stable DC resistance, with failures as delamination and glass cracks. Glass cracking near TGV–RDL appeared after 300 thermal-shock cycles in another study. — [MDPI review](https://www.mdpi.com/2674-0729/4/3/37)
- **IEEE EPS TC.** Glass core "has yet to be commercialized and requires further development". — [IEEE EPS TC deck](https://eps.ieee.org/wp-content/uploads/2025/11/Glass_Substrates_Adv_Substrates_TC_UPDATED_Nov25.pdf)

### Inferences
- In production-oriented disclosures, "buffer" so far most often means edge protection (Shinko resin edge coat; Intel edge-protected-core patents) and process-side mitigation: conformal or partial fill (DNP, XMU), anneal-ramp control (Corning), low-stress dicing (BOE, Intel). A via-level buffer liner is rarer.
- The ISTFA 2026 abstract is the only found industrial report that a via-level stress buffer (modulus and thickness tuned) fixed inter-via cracking and passed TC and HAST.
- **What remains unsolved:**
  - SeWaRe/edge cracks at the glass/build-up interface during cooling and dicing.
  - Inter-via cracking at tight pitch.
  - Cu pull-out/protrusion at high temperature.
  - Interface delamination/adhesion (Ti–Cu, Cu–glass) under HAST.
  - Inspection of internal microcracks at panel scale.
  - Trade-offs that buffers introduce: extra process steps, reduced Cu cross-section and higher resistance, possible RF loss from polymer liners, and warpage control when build-up CTE is tuned.

### Gaps
- Authors, company and buffer material of the ISTFA 2026 paper are unknown. The program page could not be opened (egress blocked) and searches did not surface them.
- No TSMC glass-core reliability data, and no confirmation of TSMC buffer-layer use, were found.
- No public confirmation that Absolics, SEMCO or LG Innotek use TGV buffer liners or edge coatings in production.
- No quantitative production yield or reliability statistics (TC cycles, HAST hours) comparing buffered and unbuffered glass cores from any manufacturer.
