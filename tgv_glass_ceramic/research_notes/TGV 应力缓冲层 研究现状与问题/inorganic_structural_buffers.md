# Inorganic, metallic and structural (geometry-based) stress-buffer approaches for Cu-metallized TGVs and glass-core substrates

Scope: non-polymer stress relief for Cu TGVs, 2010–2026 (search date 2026-10-16).
Evidence tags used below: [EXP] = experimental result; [SIM] = FEM/MD/phase-field simulation only; [PATENT] = patent/application claim or description (not peer-reviewed data); [SECONDARY] = number seen only in news, review or aggregator text, not in the primary paper; (unverified) = could not confirm against the primary text.
Method note: WebFetch failed (DNS errors) for every domain during this session, so all findings come from search-engine extracts of abstracts, highlights, patent summaries and secondary reports. No full text was read. Treat fine-grained numbers accordingly.

---

## 1. Inorganic and metallic interlayers between glass and Cu (adhesion, barrier, stress buffer)

### Takeaway
In production-style TGVs, inorganic and metallic interlayers are thin (nm-scale) adhesion, seed and barrier layers such as Ti/Cu, Cr/Cu, TiN/Ru, ZnO and TiO2. They are chosen for adhesion, hermeticity and step coverage, not to absorb stress. The only quantitative "inorganic stress-buffer" results (μm-thick sintered TiO2/ZnO/ZrO2, 49–67% lower maximum principal stress) come from simulation only, and they show a thickness trade-off. Meanwhile, three independent experimental groups identify the Ti/Cu interface as a primary failure site under HAST and high-temperature aging.

### Cited Findings

**A. μm-thick inorganic "stress buffer layers" (Chinese 电子与封装 2025 Vol.25 No.7 TGV special issue), all [SIM]**
- The 电子与封装 2025 Vol.25 No.7 special issue "玻璃通孔技术进展与应用" contains 王展博, 张泽玺, 杨斌, 郭旭, 杨冠南, 张昱, 黄光汉, 崔成强, "应力缓冲层对玻璃基板填孔结构内应力及可靠性的调控规律研究", 电子与封装 2025, 25(7): 070103. The same issue includes reviews 070106 (TGV技术及其可靠性研究现状) and 070109 (TGV力学可靠性问题及研究进展). — [科学网 special-issue listing](https://blog.sciencenet.cn/home.php?mod=space&uid=3415146&do=blog&id=1514708); [电子与封装 site](https://ep.org.cn/CN/news/news204.shtml)
- A separate paper, reported by 中国粉体网 as 赵泉露 et al., "降低玻璃基板TGV应力的无机缓冲层方法与仿真分析" from the 中科院微电子所 陈钏 team (author/affiliation per news report), sintered an inorganic buffer layer between glass and Cu and compared ZnO, TiO2 and ZrO2 by FEM. Its reported results:
  - A pure-Cu-filled TGV glass core reached 202.36 MPa maximum stress during heating.
  - All three inorganic layers lowered stress and outperformed a conventional polyimide (PI) buffer.
  - TiO2 performed best, cutting maximum principal stress by 49.3% against pure Cu during the heating stage.
  - From 1 to 5 μm buffer thickness, heating-stage stress kept falling while cooling-stage stress rose slightly (stated to stay in a safe range), with diminishing returns at larger thickness.
  - Glass core thickness from 400 to 1200 μm changed stress very little, because buffer and Cu column scale together. [SIM][SECONDARY] — [中国粉体网](https://news.cnpowder.com.cn/85217.html)
- A researching.cn listing of a 2025 电子与封装 paper (Vol.25 Issue 7, article 70108 per the search extract) on sintered ZnO/TiO2/ZrO2 buffer layers reports a 66.58% stress reduction for a 5 μm TiO2 layer. It also reports that thicker buffers and smaller TGV diameters lower glass-core stress during heating. This matches the "~66.6%" figure in the brief. The 49.3% (news) and 66.58% (listing) numbers probably refer to different thickness or load cases of the same study (unverified). [SIM] — [researching.cn](https://www.researching.cn/articles/OJ6c1dee1b5d059512)
- A secondary review states that 王展博 et al. found a "two-sided" thickness effect: an over-thick buffer shrinks the effective Cu cross-section and instead aggravates stress concentration. [SECONDARY] (attribution unverified) — [艾邦半导体网 review "玻璃芯基板研究进展：从工艺到可靠性"](https://www.ab-sm.com/a/75667)
- No source was found for "a 1 μm buffer layer reduces max principal stress by ~40%" (see Gaps).

**B. Thin adhesion, hermetic and seed layers in practice (Ti, Cr, Ta, TaN, TiN, Ni, oxides)**
- Corning's "Hermetic metallized via with improved reliability" family (US 11152294; US 12131985; US 11201109; WO2019199677) covers the following [PATENT]:
  - A helium-hermetic adhesion layer on the via wall, 1–500 nm thick, with ~100 nm as an example.
  - Ti as the preferred material, with Cr, Ta and Ni as alternatives.
  - Hermeticity defined as He permeability <1e-5 atm·cc/s, ideally <1e-8 atm·cc/s.
  - An embodiment with a Cu coating <12 μm at each major surface.
  - In the PCT version, He hermeticity ≤1.0e-8 atm·cc/s after 1000 thermal-shock cycles. — [USPTO 11152294](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11152294); [USPTO 12131985](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12131985); [WO2019199677A3](https://patents.google.com/patent/WO2019199677A3/en)
- Corning US 11171094B2, "Hermetic fully-filled metallized through-hole vias" (filed 2019-02-05, granted 2021-11-09), covers a via whose maximum diameter is ≤30 μm and fully filled along its axis, with a helium-hermetic adhesion layer of Ti, TiN, Ta, TaN, Cr, Ni or a metal oxide. [PATENT] — [USPTO 11171094](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11171094)
- Corning's IMAPS TGV presentation describes a sputtered Ti/Cu seed with no barrier covering the glass, which is the baseline industrial stack. — [Corning IMAPS TGV](https://www.corning.com/media/worldwide/cdt/documents/IMAPs_Corning_TGV_FINAL.pdf)
- An all-ALD glass metallization stack (5 nm TiO2 bonding / 11 nm TiN barrier / 11 nm Ru adhesion / 80 nm Cu seed) achieved 97.7% step coverage and 1.18% non-uniformity in 25:1 TGVs. PVD TiN in the same study gave interface defects and poor step coverage. [EXP] — [ScienceDirect, MSSP 2025, ALD TiO2/TiN/Ru/Cu](https://www.sciencedirect.com/science/article/abs/pii/S1369800125010224)
- Forge Nano (CS MANTECH 2025) used ALD TiN (5–10 nm, as a nucleation layer) plus ALD Ru (15–20 nm) as a conformal conductive seed, and electroplated vias up to 30:1 aspect ratio. [EXP, conference] — [CS MANTECH 2025 paper](https://csmantech.org/wp-content/uploads/2025/05/12.12-Final.2025.pdf)
- A 2026 focused review in Micromachines rates ALD/CVD adhesion, barrier and seed layers as having excellent conformality for high-AR vias but low throughput, high equipment cost and integration complexity. It also notes that insufficient seed step coverage in high-AR TGVs causes voids and pinch-off. — [Park et al., Micromachines 17(6):720, 2026](https://www.mdpi.com/2072-666X/17/6/720)
- An optimized NiP electroless seed layer for TGV was published in Microelectronic Engineering (2022). Details were not retrieved. — [ScienceDirect MEE 2022](https://www.sciencedirect.com/science/article/abs/pii/S0167931722000296)

**C. Sol-gel and wet-chemical oxide adhesion layers (ZnO, TiO2)** [EXP]
- Dip-coated Ag-doped ZnO sol-gel worked as a catalytic adhesion layer on glass and in TGVs, replacing etching and sensitization:
  - It gave full seed coverage in 10:1 TGVs.
  - After electroplating to 11 μm Cu, adhesion was 4.19 N/cm after a 300 °C vacuum anneal. — [J. Electrochem. Soc. 2025, Nano-silver doped ZnO adhesion layer](https://iopscience.iop.org/article/10.1149/1945-7111/ada589)
- Low-temperature (~70 °C) SILAR/CBD ZnO on Borofloat 33 gave peel strength >6.8 N/cm for Cu up to ~3 μm. The authors attribute this to mechanical anchoring of Cu in the porous ZnO. — [J. Electrochem. Soc. 2025, ZnO adhesion promoter](https://iopscience.iop.org/article/10.1149/1945-7111/ae02c9); [SSRN preprint](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5234878)
- A solution-processed Cu–TiO2 catalytic adhesion layer reached up to 0.5 kN/m after thermal treatment. — [ResearchGate](https://www.researchgate.net/publication/295398456_Copper_Plating_on_Glass_Using_a_Solution_Processed_Copper-Titanium_Oxide_Catalytic_Adhesion_Layer)
- One search summary reported that electroless Cu on glass without an adhesive oxide shows no adhesion, and gave a ≥5 N/cm, 90°-peel benchmark for 15 μm Cu (source among results not pinned; unverified). — [Adhesive Enabling Technology for Directly Plating Copper onto Glass](https://www.researchgate.net/publication/284599101_Adhesive_Enabling_Technology_for_Directly_Plating_Copper_onto_Glass)
- An alternative to oxide layers is localized TGV sidewall roughening: ultrasonic machining gave better seed adhesion than ECDM roughening, attributed to mechanical interlocking. [EXP] — [ScienceDirect MSSP 2024](https://www.sciencedirect.com/science/article/abs/pii/S136980012400653X)
- None of the ZnO, TiO2 or ALD adhesion-layer papers above reports a stress-reduction or crack-rate result. They report adhesion and coverage only.

**D. Nano-structured and porous inorganic or metallic buffers (patent stage only)**
- An Intel application, "Porous copper liner for through glass via (TGV) glass cores" (Pietambaram et al. per search summary), describes a buffer layer whose elastic modulus is lower than the via's. Details [PATENT]:
  - One embodiment has a near-zero-porosity via and a buffer with up to ~60% porosity.
  - The buffer can be a ring around the via and can sit directly on glass, on a seed layer, or over a liner.
  - It notes that polymer liners can peel from the sidewall, and that a compressible liner consumes space that plated Cu would otherwise occupy. — [trea.com application page](https://trea.com/information/porous-copper-liner-for-through-glass-via-tgv-glass-cores/patentapplication/edc94632-2fe9-410d-b95d-12772cd3acf4)
- An Intel application, "Technologies for Nanowires in Through-Glass Vias" (publication 20260182403 per search summary), grows ZnO nanowires in glass cavities, decorated with Pd particles to nucleate the Cu seed. The nanowires are said to "act as a buffer between the copper vias and the glass core, accommodating thermal expansion". [PATENT; number and details unverified against full text] — [Justia Intel application listing](https://patents.justia.com/company/intel?list=applications&page=5)
- A related Intel application on polymer TGV buffer layers (20260182404, filed Dec 2024) is polymer-based, so outside this scope. It is listed here only for completeness (unverified). — [Justia Intel listing](https://patents.justia.com/company/intel?list=applications&page=5)
- Intel US 12087623, "Dielectric liners on through glass vias", cites the Cu/glass CTE difference as a source of via-wall delamination risk. [PATENT] — [USPTO 12087623](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12087623)
- US 10325839B2 / US 10593616, "Reduction of stress in via structure" (inventors include Toyohiro Aoki and Takashi Hisada; assignee not confirmed, possibly IBM, unverified), describes a stress buffer layer on the substrate surface with an opening aligned to the via hole, filled afterwards. A low-Young's-modulus buffer is said to reduce principal stress near the glass surface. [PATENT/SIM] — [Google Patents US10325839B2](https://patents.google.com/patent/US10325839); [USPTO 10325839](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10325839)

**E. Interface failures of metallic adhesion layers (Ti/Cu) under aging and HAST** [EXP]
- Okoro et al. (Corning), Microelectron. Reliab. 2022, Cu TGVs in HPFS fused silica:
  - Wafers stayed below 1.0e-8 atm·cc/s He leak.
  - HAST was the most damaging test, with failures after 400–1600 h from Cu oxidation and Ti–Cu interface debonding. — [ScienceDirect, "Evaluation of the helium hermeticity reliability of copper through-glass vias"](https://www.sciencedirect.com/science/article/abs/pii/S0026271422003079)
- Xiamen University (马盛林 team), 2023, glass–Ti–Cu partially-filled TGVs (X-type and "bridge-type"), tested per JEDEC HAST/TCT/HTS:
  - He leak rate and DC resistance were most sensitive to HAST.
  - Ti–Cu interface micro-defects and through cracks were the main HAST failure modes.
  - The proposed mechanism is Ti diffusion into glass and Cu diffusion into Ti, creating interface defects that become microcracks. — [CNKI JBXK202310018](http://dbase2.gslib.com.cn/KCMS/detail/detail.aspx?filename=JBXK202310018&dbcode=CJFD&dbname=CJFD2023); [腾讯新闻转载](https://news.qq.com/rain/a/20230916A017AJ00)
- G. Sun and S. Zhang (2026, Materials Science in Semiconductor Processing; Shuye Zhang is commonly affiliated with Harbin Institute of Technology, but affiliation was not confirmed in results):
  - Under high-temperature aging the glass/Ti/Cu interface coarsens, and irregular voids and microcracks form at the Cu/Ti interface.
  - These grow under thermal stress into through-thickness cracks that run mainly along via sidewalls, transgranularly, driven by shear at the glass/Ti/Cu interface.
  - Ti diffusion slows as the system approaches equilibrium; Cu grain size grows from 3.12 to 9.97 μm. — [ScienceDirect author page, Shuye Zhang](https://www.sciencedirect.com/author/56437796500/shuye-zhang)
- Chen et al. (2026), Microsystems & Nanoengineering, laser-induced-etch plus double-sided electroplated TGV-Cu aged at 250 °C for up to 1008 h:
  - Hardness fell from ~2.0–2.5 GPa to <0.5 GPa, and modulus from 110–130 GPa to 40–90 GPa, with the largest changes near the surface.
  - Grain size grew from 0.46 to 1.86 μm.
  - The glass kept stable mechanical properties until microcracks formed after 1008 h. — [Microsyst. Nanoeng. s41378-026-01160-0](https://www.nature.com/articles/s41378-026-01160-0)
- Heat-treatment study (J. Alloys Compd. 2025, via secondary report), 100–300 °C in N2 plus MD simulation on electroplated TGV substrates:
  - It reports that temperature affects SiO2–Ti–Cu interface stability.
  - Σ3/Σ9 grain boundaries reached up to 45.46%.
  - Resistivity went from 15.83 to 18.11 (units given as ×10⁻⁶ Ω·m in the report, likely mis-scaled; unverified).
  - Warpage reached a curvature radius of 979 m. [EXP+SIM][SECONDARY] — [生物通 report](https://www.ebiotrade.com/newsf/2025-6/20250616150524216.htm)

### Inferences
- Two distinct classes are often conflated under "inorganic buffer layer":
  1. Thin (1–500 nm) adhesion, hermetic and barrier layers (Ti, Cr, TiN, Ta/TaN, ALD TiO2, sol-gel ZnO) that set adhesion, He hermeticity and step coverage. They are too thin and too stiff to change the CTE-driven stress field materially.
  2. Thick (1–5 μm) sintered or ceramic layers (TiO2, ZnO, ZrO2) whose 49–67% stress reduction appears only in FEM.
- The plausible stress-relief mechanism in the thick-layer simulations is that a lower-modulus, intermediate-CTE ring reduces radial constraint during heating. That same layer then raises cooling-stage stress and takes Cu cross-section ("two-sided effect"). This implies an optimum thickness rather than "thicker is better".
- The recurring experimental weak link is the Ti/Cu interface (Corning HAST debonding; XMU HAST microcracks; Sun & Zhang aging voids and cracks). Adding more metallic interfaces, as in graded or multilayer stacks, adds more diffusion-driven failure sites unless a true barrier (TiN, TaN) separates Ti from Cu. This is inferred from the mechanisms reported, not directly tested in the sources found.
- Porous-Cu, ZnO-nanowire and other "compliant metallic" buffers are at patent stage only. No published stress, crack or reliability data were found.

### Gaps
- The "1 μm buffer layer reduces max principal stress ~40%" claim could not be found in any source (unverified). It may be in the full text of the 王展博/崔成强 paper (070103) or the 赵泉露/陈钏 paper, but neither full text was accessible.
- Full texts of the 电子与封装 2025 papers (070103 and the sintered-buffer paper) could not be read. Material properties used, boundary conditions, ΔT, and whether any experiment (sintering trial, crack inspection) was done are unknown. All their numbers are treated as simulation-only.
- No experimental study was found measuring stress (micro-Raman, nanoindentation, XRD) or crack incidence with and without an inorganic buffer (SiO2, SiNx, Al2O3, TiO2) in Cu TGVs.
- No TGV-specific data were found for TiW, Mo or Cr–Cu graded layers, or for SiNx/SiO2 liners used as stress buffers. Their use is documented in TSV practice but was not found for TGV with numbers.
- The thermal-cycling fatigue life of thin metal liners in TGVs was not quantified in any source found.

---

## 2. Structural (geometry-based) buffers: conformal/annular Cu, air gaps, partial fill, via shape, pads/RDL, edge buffers

### Takeaway
The strongest experimental structural result is Corning's: in conformal (annular) Cu TGVs (~47.5 μm via, HPFS fused silica), circumferential cracks after a 400 °C anneal are eliminated when the Cu wall is thinner than 12 μm, against a ~140 MPa FEA threshold stress. Simulation also ranks a hollow TGV with Cu pad as having the lowest crack energy release rate. Air-gap decoupling (Intel-attributed 2026 filings), porous liners and edge coatings are mostly patent or industry-report stage. The best edge-coating number (95 → 49 MPa) is second-hand.

### Cited Findings

**A. Conformal / annular vs full fill: Cu thickness thresholds**
- Okoro, Park, Allowatt, Pollard (Corning), IEEE TDMR 21(3):354–360, 2021, "Elimination of thermo-mechanically driven circumferential crack formation in copper through-glass via substrate":
  - Circumferential cracks form in glass around Cu TGVs during cooling after a 400 °C anneal (via mean outer diameter 47.5 μm, Corning HPFS fused silica).
  - No cracks formed for metallization thickness <12 μm; crack formation rose exponentially for ≥12 μm.
  - FEA puts the crack-initiation threshold stress at ~140 MPa, reached at the 12 μm thickness.
  - Cracks are driven by high tensile radial stress in the glass during cooling. [EXP+SIM] — [IEEE Xplore 9481891](https://ieeexplore.ieee.org/document/9481891/)
- The ECTC 2021 companion is Okoro, Allowatt, Pollard, "Resolving Thermo-Mechanically Induced Circumferential Crack Formation in Copper Through-Glass Vias", pp. 954–958. — [IEEE Xplore 9501526](https://ieeexplore.ieee.org/document/9501526/)
- The Corning "Hermetic metallized via" patent family restates the 12 μm threshold: Cu coating <12 μm gives no cracks, while ≥12 μm shows circumferential microcracks (FIG. 8B). [PATENT] — [USPTO 12131985](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12131985); [USPTO 11152294](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11152294)
- One numerical study (attribution among results unverified; likely Le & Choa 2024) reports that when the Cu layer reaches 15–20 μm, the Cu on opposite sidewalls merges and the growth of first principal stress slows. [SIM] — [Le & Choa, J. Mech. Sci. Technol. 2024](https://link.springer.com/article/10.1007/s12206-024-0522-1)
- Le & Choa, J. Mech. Sci. Technol. 38 (2024), computed energy release rate (ERR) for circumferential and radial cracks:
  - Cracks can be reduced or eliminated by choice of glass, annealing temperature and Cu via structure.
  - A hollow TGV with a Cu pad showed the lowest ERR.
  - Cracks can still occur during thermal cycling even though cycling ERR is smaller than annealing ERR. [SIM] — [Springer s12206-024-0522-1](https://link.springer.com/article/10.1007/s12206-024-0522-1); [SeoulTech record](https://pure.seoultech.ac.kr/en/publications/a-comprehensive-numerical-analysis-for-preventing-cracks-in-25d-g/)
- A snippet quotes a "compromise design" (via radius 21.246 μm, pitch 69.172 μm, Cu thickness 1.011 μm) giving a 14.8% reduction in maximum principal stress. The source paper could not be confirmed (unverified). [SIM] — [ResearchGate page of TGV review](https://www.researchgate.net/publication/383151568_Thermo-mechanical_reliability_of_glass_substrate_and_Through_Glass_Vias_TGV_A_comprehensive_review)
- Chinese industry practice is that fully solid Cu-filled TGVs are usually limited to via diameter <50 μm and glass thickness <100 μm to avoid anneal cracking. Larger or thicker vias move to double-sided partial-fill schemes, conformal on the sidewall and solid only at a specific location such as the X-via waist. [SECONDARY] — [矢量科学/腾讯新闻](https://news.qq.com/rain/a/20230916A017AJ00); [知乎 转载](https://zhuanlan.zhihu.com/p/1889791319913764607)
- Conformal TPV reliability in thin glass (Georgia Tech-style TPV papers; institution not confirmed in results) [EXP]:
  - Conformally plated 60 μm TPVs in 100 μm glass showed no degradation after 4000 thermal cycles.
  - 30 μm TPVs in 100 μm glass kept stable resistance after 3000 cycles (−55 to 125 °C), with initial daisy-chain resistance of 80–230 mΩ.
  - Delamination and glass cracking near TPV corners were the failure modes.
  - Simulated Cu plastic strain accumulation was ~0.005 per cycle.
  - Per-number attribution across these papers is from search summaries (unverified). — [Reliability of Cu TPVs in bare glass interposers](https://www.academia.edu/119963275/Reliability_of_Copper_Through_Package_Vias_in_Bare_Glass_Interposers); [Thermomechanical and electrochemical reliability of fine-pitch TPV](https://www.researchgate.net/publication/260192671_Thermomechanical_and_electrochemical_reliability_of_fine-pitch_through-package-copper_vias_TPV_in_thin_glass_interposers_and_packages); [IMAPS 2014, 30 μm TPVs](https://meridian.allenpress.com/ism/article-pdf/2014/1/000402/2252418/isom-wa16.pdf)

**B. Hourglass / pinched-via geometry (geometry plus superconformal plating)**
- Kanungo, Vaddi, Okoro, Pollard, Mazumder, ECTC 2025 pp. 1043–1046, "Metallization of Helium-Hermetic and Thermo-Mechanically Reliable TGV by Conformal Pinched Via (CPV) Approach":
  - Single-step metallization of high-AR TGVs using the additive NTBC and superconformal plating in an engineered (hourglass) via.
  - A He-tight adhesion layer on sidewalls near the via entry.
  - Claims high-temperature thermomechanical reliability plus liquid and He hermeticity. Detailed test data were not retrieved. [EXP, abstract-level] — [Semantic Scholar record](https://www.semanticscholar.org/paper/Metallization-of-Helium-Hermetic-and-Reliable-Glass-Kanungo-Vaddi/f7e85f42e70b8fc01bbd7048bd6b20915daf7e4c)
- The related US 11148935 (conformal pinched through-via in a glass-cap MEMS switch) reports He leak <1.0e-6 atm·cm³/s. [PATENT] — [USPTO 11148935](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11148935)
- A review states that full Cu fill causes thermomechanical problems from the Cu/glass CTE gap. It describes CPV (hourglass via plus He-tight adhesion layer near the entry) as a solution. [SECONDARY] — [A Review of Glass Substrate Technologies (MDPI, 2025)](https://www.mdpi.com/2674-0729/4/3/37)
- Defect-free metallization of TGVs with engineered (X-shaped) geometry: the vias pinch at the waist and then fill void-free in a kinetic-limited plating regime. [EXP] — [ResearchGate, "Defect-Free Metallization of TGV with Engineered Geometry"](https://www.researchgate.net/publication/362013274_Defect-Free_Metallization_of_through-Glass_Vias_TGV_with_Engineered_Geometry)
- One study of straight vs X-shaped TGVs (AR 12) under glass-core temperature rise found that X-shaped vias carried more thermal stress, attributed to the larger via angle. Stress values and source paper not confirmed (unverified). [SIM] — [A Review of Glass Substrate Technologies](https://www.mdpi.com/2674-0729/4/3/37)
- Zhao, Chen, Qin, Yu, Micromachines 13:1799 (2022): a tapered TGV (25 μm inner / 60 μm outer opening, 300 μm pitch). An FE model predicted stress evolution, and a revised process flow fixed an RDL-crack problem. This is an example of an RDL/pad-level fix rather than a via-level buffer. [SIM+EXP] — [MDPI mi13101799](https://www.mdpi.com/2072-666X/13/10/1799); [PMC9607209](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9607209/)

**C. Deliberate air gap / decoupling between Cu and glass sidewall (patent stage)**
- DE102025144620A1 (Patsnap summary) uses bottom-up Cu plating without a nucleation layer on the glass sidewall. The plating is "at least partially physically decoupled from the sidewall … so that an air gap is discernible", which the filing says reduces stress from through-hole metallization. [PATENT; AI summary] — [Patsnap DE102025144620A1](https://eureka.patsnap.com/patent/DE102025144620A1)
- US20260173267A1 (Patsnap summary) frames the gaps as separating glass from TGV conductors to alleviate CTE-mismatch stress. It includes an optional low-modulus sidewall liner and three metallization routes: subtractive etch, modified SAP, and flowable materials filling a cavity during bottom-up plating. The assignee was not shown. [PATENT; AI summary] — [Patsnap US20260173267A1](https://eureka.patsnap.com/patent/US20260173267A1)
- Chinese commentary attributes an application titled "Bottom-Up Plating of Through-Glass Vias" to Intel, published 2026-06-18. It describes a controllable air gap combined with a composite buffer layer and three process routes. A match to the DE/US numbers above is plausible but not confirmed (unverified). [SECONDARY] — [cnyes 鉅亨 post 256628](https://hao.cnyes.com/post/256628); [cnyes post 258730](https://hao.cnyes.com/post/258730)
- An Intel application "Skip layer with air gap on glass substrates" (US20240063100A1) was seen only as a citation in a patent family table. Its content is unverified. — [Google Patents US12080632B2 family](https://patents.google.com/patent/US12080632B2/en)
- The TSV analog, US 8962474 "Method for forming an air gap around a through-silicon via", places an air gap between Si and Cu TSV for the same CTE reason. [PATENT] — [USPTO 8962474](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/8962474)

**D. Electrical and hermetic penalties of annular / conformal vias**
- Measured TGV contribution to CPW insertion loss at 30 GHz is 0.48 dB (conformal), 0.34 dB (partially filled) and 0.23 dB (fully filled). More Cu fill gives lower loss. [EXP] — [IEEE EPS Glass Substrates TC overview, Nov 2025](https://eps.ieee.org/wp-content/uploads/2025/11/Glass_Substrates_Adv_Substrates_TC_UPDATED_Nov25.pdf)
- This conflicts with an EM simulation (~30 μm via, 60 μm pitch) that found conformal Cu TPV loss "almost identical" to fully filled, attributed to skin effect. Source paper not pinned (unverified).
- A tapered, conformally plated "inverted" TGV gave 0.014 dB at 10 GHz and 28 mΩ DC for a 100 μm-tall via (attribution unverified; likely Menlo Micro). [EXP] — [Menlo Micro, TGV for RF](https://menlomicro.com/images/general/2016-01-TGV_for_RF.pdf)
- Magnetically assembled wire TGVs gave ~64 mΩ per via, compared with ~40 mΩ for bottom-up plated Ni TGVs. [EXP] — [academia.edu, TGVs by magnetic assembly of microscale wires](https://www.academia.edu/123146282/Through_Glass_Vias_for_Glass_Interposers_and_MEMS_Packaging_Applications_Fabricated_Using_Magnetic_Assembly_of_Microscale_Metal_Wires)
- The 2026 Micromachines review says fully Cu-filled TGVs give the best electrical performance but suffer CTE-mismatch reliability issues. It lists polymer/dielectric plugging, plug/re-drill, conductive-paste plugging and hybrid Cu/plug structures as application-specific alternatives. — [Park et al., Micromachines 2026](https://www.mdpi.com/2072-666X/17/6/720); [PMC13303985](https://pmc.ncbi.nlm.nih.gov/articles/PMC13303985/)

**E. Edge buffers / panel-edge cracking (SeWaRe), pull-back and edge clearance**
- Tom's Hardware (2026 glass-substrate roadmap article): "Edge-coating work has cut measured edge stress from 95 MPa to 49 MPa." It also reports low-temperature dielectrics curing <180 °C developed to reduce build-up thermal stress. The article does not tie the 95 → 49 MPa figure to Absolics, name the coating, or name the method, so the Absolics attribution in the brief is unverified. [SECONDARY] — [Tom's Hardware](https://www.tomshardware.com/tech-industry/manufacturing/glass-substrate-roadmap-examined)
- Shinko Electric received an ECTC 2025 outstanding session paper award. It identified the SeWaRe root cause as CTE mismatch between the glass core and build-up resin layers, and showed that edge coating suppressed SeWaRe even after a 260 °C reflow test. No MPa figure was given in the announcement. [EXP, company report] — [Shinko news](https://www.shinko.co.jp/english/news/2026/07/b2e0e1c9fadd06989a3ba3940788615cdb6ddaf4.php)
- TrendForce reports that Shinko reinforced substrate edges with resin to disperse stress and suppress SeWaRe under thermal loading. [SECONDARY] — [TrendForce 2026-08-18](https://www.trendforce.com/news/2026/08/18/news-glass-substrate-war-heats-up-shinko-electric-advances-22-layer-product-as-samsung-reportedly-faces-ramp-up-uncertainty/)
- Georgia Tech Research Institute WO2025208144A1, "Methods & architectures of edge coated glass substrates" (published 2025-10-02): a carrier/dicing film on one side, the panel diced into substrates, then a polymer applied to cover edges at least partially. It notes that existing edge-coating methods are manual. [PATENT] — [Google Patents WO2025208144A1](https://patents.google.com/patent/WO2025208144A1/en)
- Intel US20230087838A1, "Protective coating on an edge of a glass core", exists (title seen only). — [Google Patents US20230087838A1](https://patents.google.com/patent/US20230087838A1/en)
- Le, Yoo, Choa, Micromachines 16:1256 (2025) [SIM]:
  - A top-edge crack near the RDL/glass interface is the highest risk, with the highest peeling stress and ERR. The center-edge crack has 144 MPa von Mises and 132 MPa peeling stress, lower than top-edge.
  - Risk rises with more RDL layers and thinner glass.
  - Higher-CTE glasses (D263, Gorilla, ceramic glass) suppress crack growth better than Borofloat 33 or fused silica.
  - ABF GZ-41 is best among the dielectrics studied.
  - Edge clearance ≥300 μm effectively suppresses propagation (the geometric analog of build-up pull-back). — [Micromachines 16:1256](https://doi.org/10.3390/mi16111256); [PMC12654316](https://pmc.ncbi.nlm.nih.gov/articles/PMC12654316)

### Inferences
- Thin conformal Cu (<12 μm wall) is the only geometry-based buffer with a clear, experimentally validated threshold (Corning/HPFS). It specifically suppresses cooling-stage circumferential cracks. It does not address heating-stage radial cracks, which Corning controls separately by ramp rate (Section 3).
- Hollow or annular vias move the problem to hermeticity and the via core. Corning's answer is a He-hermetic adhesion layer plus pinched/hourglass geometry (CPV). Others plug the core with polymer, dielectric or paste. The measured RF penalty of conformal vias is modest (~0.25 dB extra at 30 GHz per TGV vs full fill), but DC resistance and current-carrying penalties for power-delivery TGVs in glass cores were not quantified in any source found.
- Air-gap and decoupled-sidewall concepts remove radial constraint entirely. That also removes the mechanical anchoring that limits Cu pumping and sliding (Pan et al. list sliding and delamination as observed failure types). It likely creates moisture or contamination paths and loses hermeticity, which matters given the HAST sensitivity in Section 1. These consequences are inferred; no data were found.
- For glass-core panels, the dominant non-via cracking problem (SeWaRe) is driven by build-up/glass CTE mismatch at diced edges. Geometric levers (edge clearance ≥300 μm, pull-back) and edge coatings are the main mitigations. The 95 → 49 MPa (~48% reduction) is the only quantitative edge-coating figure found, and it is second-hand.

### Gaps
- Full text of IEEE TDMR 21(3) was not accessed. Plating method, whether the via core was left hollow or plugged, and the Cu-thickness/diameter ratio dependence (does 12 μm scale with via diameter?) are unknown.
- No experimental study comparing hollow vs filled TGV crack incidence at matched geometry was found beyond Corning's thickness sweep. No Chinese FEM paper with numbers on 空心 vs 实心 TGV was retrieved.
- No full text, assignee confirmation or data were found for the Intel air-gap / bottom-up-plating filings (DE102025144620A1, US20260173267A1, US20240063100A1). Gap width, liner material and test results are unknown.
- No primary source was found for the 95 → 49 MPa edge-coating result, or for any Absolics-specific data. SKC/Absolics, Samsung Electro-Mechanics, LG Innotek, DNP and BOE patents on via-level stress buffers were not found in searches; a dedicated KIPO/JPO search is needed.
- "Hanging-wall" Cu thickness, pad-size and thin surface RDL effects on TGV stress were not found with numbers, apart from Le & Choa's "hollow TGV with Cu pad = lowest ERR".
- Current-carrying capacity and electromigration of annular vs filled TGVs: no data found.

---

## 3. Process-side stress management that acts like a buffer (anneal ramp/dwell, Cu microstructure/additives, low-CTE fills, alternative conductors)

### Takeaway
The best-validated "buffer" is thermal-process control. Corning showed experimentally that radial cracks in fully metallized HPFS TGVs rise exponentially with heating rate and vanish at ≤6.5 °C/min, and patented ramp limits (<8.7 °C/min, narrower 1.0–6.5 °C/min) between ~200–300 °C and ~350–450 °C. Pre-anneal dwell (≥120 min at 400 °C) removes later protrusion. Additive and impurity control (BOE 2025) targets protrusion. Low-CTE electroplated Ni-Fe fills (CTE 7.27 ppm/K vs glass 7.2 ppm/K, 2025–2026) remove the mismatch at source but have no published quantitative stress or electrical penalty data. CNT–Cu and low-CTE paste fills have no TGV-specific data.

### Cited Findings

**A. Anneal heating rate (radial cracks during heating)**
- Okoro, Jayaraman, Pollard (Corning), Microelectron. Reliab. 120:114092 (May 2021), DOI 10.1016/j.microrel.2021.114092: in fully metallized Cu TGVs in HPFS fused silica annealed to 420 °C, radial crack formation increased exponentially with heating rate. Cracks were eliminated at ≤6.5 °C/min. [EXP] — [ScienceDirect S0026271421000585](https://www.sciencedirect.com/science/article/abs/pii/S0026271421000585)
- The Corning patent family "Glass or glass ceramic articles with copper-metallized through holes and processes for making the same" (US 11760682; US 12515977; CN113474311A) claims [PATENT]:
  - An average heating rate between a first temperature (200–300 °C) and a second temperature (350–450 °C) of >0 and <8.7 °C/min.
  - A narrower range of 1.0–6.5 °C/min.
  - The claimed article has no radial cracks. — [USPTO 12515977](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12515977); [USPTO 11760682](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11760682); [CN113474311A](https://patents.google.com/patent/CN113474311A/en); [Justia Corning listing](https://patents.justia.com/assignee/corning-incorporated?page=7)
- A related Corning hermetic-via filing states that controlled heating can minimize or eliminate radial cracking regardless of via pitch. [PATENT] — [WO2019199677A3](https://patents.google.com/patent/WO2019199677A3/en)
- Pan et al. (Binghamton/Corning), Microelectron. Reliab. 129:114487 (2022), in-situ RT → 400 °C with optical profilometry and 2D DIC:
  - Glass in-plane displacement near vias peaks around 250 °C, then decreases as Cu protrudes and creeps.
  - Slower ramp rates (4–50 °C/min tested) reduced glass deformation, attributed to more Cu creep relaxing CTE stress. [EXP] — [ScienceDirect S0026271422000117](https://www.sciencedirect.com/science/article/abs/pii/S0026271422000117)
- Pan et al., ECTC 2021 (DOI 10.1109/ECTC32696.2021.00263), HPFS, RT → 400 °C:
  - Average protrusion went from −0.2 to ~1.6 μm at 400 °C.
  - Cu stays constrained by glass and adhesion up to ~250 °C, and protrusion is partly irreversible after cooling.
  - The listed failure types are glass/TGV cracking, protrusion, Cu sliding and delamination. [EXP] — [IEEE Xplore 9501700](https://ieeexplore.ieee.org/document/9501700/); [ResearchGate](https://www.researchgate.net/publication/353808728_Investigation_of_Copper_and_Glass_Interaction_in_Through_Glass_Via_TGV_During_Thermal_Cycling)

**B. Anneal dwell, pre-annealing and long-time anneal (protrusion and residual stress)**
- Okoro, Maurey, Pollard, IEEE TDMR 21:129–136 (2021), 50 μm × 300 μm Cu TGVs in HPFS [EXP]:
  - At 400 °C, protrusion depends on dwell and saturates at ~240 min.
  - A later 400 °C/60 min step adds no protrusion if the prior anneal dwell was ≥120 min.
  - Downstream protrusion can be removed by a 120 min dwell at 400 °C or by 450 °C/60 min. — [IEEE Xplore 9353697](https://ieeexplore.ieee.org/document/9353697/)
- Wang et al., Microsyst. Nanoeng. 12:52 (2026, online 2026-02-06), nanoindentation and AFM on annealed TGVs [EXP + model]:
  - Moderate annealing relieves glass stress, but prolonged annealing builds residual tensile stress in glass that leads to cracking.
  - Cu protrusion rises with anneal time at a decreasing rate.
  - The paper gives a creep-rate model (RMSE 1.143 in the published version; the preprint reported "87.32% accuracy") and a linear residual stress–protrusion correlation.
  - Circumferential crack length was 6.9 μm after 216 h at 300 °C and 18.9 μm after 288 h.
  - A critical glass stress of 549 MPa is cited. The crack and stress figures come from search extracts of this paper (unverified against full text). — [Microsyst. Nanoeng. s41378-026-01162-y](https://www.nature.com/articles/s41378-026-01162-y); [PubMed 41651804](https://pubmed.ncbi.nlm.nih.gov/41651804/); [Research Square preprint](https://www.researchsquare.com/article/rs-7322629/v1)

**C. Cu microstructure and plating-additive control**
- BOE, SID Digest 56(1):1109–1112 (2025), paper 81-2, "Effect of Electroplating Additives on Copper Protrusion of Metallized TGVs" (DOI 10.1002/sdtp.18370): impurities from organic additives create vacancies, which aggregate under CTE-mismatch thermal stress and drive Cu protrusion. Reducing impurity minimizes protrusion. Numbers not retrieved. [EXP] — [Wiley SID Digest](https://sid.onlinelibrary.wiley.com/doi/abs/10.1002/sdtp.18370); [SID PDF 81-2](https://sid.org/Portals/sid/Files/SID-Digest/docs/81-2.pdf)
- The Corning CPV work uses the additive NTBC to obtain superconformal single-step fill (see Section 2B). — [Semantic Scholar](https://www.semanticscholar.org/paper/Metallization-of-Helium-Hermetic-and-Reliable-Glass-Kanungo-Vaddi/f7e85f42e70b8fc01bbd7048bd6b20915daf7e4c)
- The J. Alloys Compd. 2025 heat-treatment study (100–300 °C) is summarized in Section 1E: Σ3/Σ9 boundaries, warpage curvature radius 979 m. [SECONDARY] — [生物通](https://www.ebiotrade.com/newsf/2025-6/20250616150524216.htm)
- One domestic double-sided plating study reports that after 250 °C/30 min annealing, TGV surface Cu roughness was 388 nm and resistivity 190 mΩ·μm, with little change from annealing. [SECONDARY] — [矢量科学/腾讯新闻](https://news.qq.com/rain/a/20230916A017AJ00)

**D. Low-CTE fills and alternative conductors**
- Yang, Park, Lee, Yoon, Yoo, J. Mater. Sci. Technol. (2026 letter; DOI 10.1016/j.jmst.2025.11.043 per search extract):
  - Electrodeposited Ni-Fe alloy (tuned by the NiSO4/FeSO4 ratio and additives) reached CTE 7.27 × 10⁻⁶ K⁻¹, matching glass at 7.2 × 10⁻⁶ K⁻¹.
  - Void-free superfill was obtained, with sodium saccharin both lowering internal stress and promoting superfilling.
  - "Significantly improved CTE mismatch and thermal stability" vs Cu, but no quantitative stress, cycling or resistivity numbers in the extracts. [EXP] — [ScienceDirect S1005030225011983](https://www.sciencedirect.com/science/article/abs/pii/S1005030225011983)
- A companion IEEE paper, "Ni-Fe Alloy Filling of Through Glass Via for Thermally Reliable Advanced Packaging", reached an Invar-like low-CTE composition by adjusting the Ni²⁺/Fe²⁺ ratio. [EXP] — [IEEE Xplore 11392609](https://ieeexplore.ieee.org/abstract/document/11392609/)
- CNT–Cu composites: no TGV data found. For Si TSVs, a vertically aligned CNT–Cu nanocomposite showed resistivity ~1e-8 Ω·m and CTE similar to Si. A review notes that uniform Cu filling and CNT dispersion remain unsolved. [EXP, TSV analog] — [PubMed 27383767](https://pubmed.ncbi.nlm.nih.gov/27383767/); [PMC12471306 review](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12471306/)
- Low-CTE conductive paste: a patent for Si via filling describes Cu plus a low-CTE phase (silica, cordierite, spodumene, borosilicate glass, mullite, β-eucryptite, W, Mo) giving a composite of much lower CTE than pure metal. [PATENT, Si analog] — [USPTO 7288474](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/7288474)
- Another patent covers through-die vias with a dispersed graphitic-carbon/CNT phase for lower thermal expansion and higher conductance. [PATENT] — [USPTO 7666768](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/7666768)
- Cu–W co-electroplating to suppress TSV extrusion has been reported (Si analog; details not retrieved). — [ResearchGate 273503445](https://www.researchgate.net/publication/273503445_Extrusion_Suppression_of_TSV_Filling_Metal_by_Cu-W_Electroplating_for_Three-Dimensional_Microelectronic_Packaging)
- Glass-side CTE as a lever: the reported CTE mismatch is Cu ≈ 17 ppm/°C vs glass 3–8 ppm/°C [SECONDARY]. — [Patsnap materials overview](https://eureka.patsnap.com/materials/glass-packaging-substrate)
- One FEM result (source paper not pinned) says principal and shear stress fall by 46% as glass CTE rises from 0.57 to 9.4 ppm/°C (unverified). [SIM]

### Inferences
- Ramp-rate control works through Cu creep and stress relaxation during heating, consistent with Pan's DIC data showing glass deformation peaks near 250 °C. It is effectively a time-domain buffer and the most mature, patented, experimentally validated non-polymer mitigation. Its cost is throughput: at ≤6.5 °C/min, a 25 → 420 °C ramp takes ~60 min (simple arithmetic).
- Anneal windows have two sides. Pre-annealing (≥120 min at 400 °C) stabilizes protrusion, but prolonged high-temperature exposure (hundreds of hours at 250–300 °C) produces residual tensile stress, circumferential crack growth and Ti/Cu interface voiding (Wang 2026; Sun & Zhang 2026; Chen 2026). Process-side relief and long-term aging reliability therefore have to be co-optimized.
- Low-CTE Ni-Fe fills attack the root cause, but Invar-class Fe-Ni alloys are generally known to have electrical resistivity tens of times higher than Cu. This is general materials knowledge, not from the cited papers, which gave no resistivity. That suggests use for signal or mechanical vias rather than power-delivery TGVs in glass cores.

### Gaps
- BOE SID 2025 numerical results (protrusion heights vs additive/impurity level, anneal conditions) were not retrieved.
- The Ni-Fe TGV papers' resistivity, thermal-cycling data and crack results were not retrieved.
- No TGV-specific data were found for Cu alloying (Cu–Ag, Cu–W), nanotwinned Cu, Cu–CNT, Cu–Invar composites, Ag paste or W fills in glass with stress or crack measurements.
- No study was found that quantifies cooling-rate effects on circumferential cracks (as opposed to heating-rate effects on radial cracks).

---

## 4. Problems, trade-offs and contradictions

### Takeaway
Every non-polymer buffer trades one failure mode for another:
- Thicker inorganic layers lower heating stress but raise cooling stress and take Cu area.
- Thin Ti adhesion layers give hermeticity but become the HAST and aging failure site.
- Conformal Cu stops circumferential cracks but costs RF loss and hermeticity, and needs core plugging.
- Air gaps decouple stress but forfeit anchoring and sealing.
- Slow ramps and long dwells cost throughput, and over-annealing causes tensile cracking.
Most stress-reduction percentages are simulation-only.

### Cited Findings
- **Thickness trade-off (simulation):** for 1 → 5 μm TiO2/ZnO/ZrO2 buffers, heating-stage stress falls but cooling-stage stress rises slightly [SIM]. — [中国粉体网](https://news.cnpowder.com.cn/85217.html). Over-thick buffers reduce effective Cu area and aggravate stress concentration ("two-sided effect", 王展博 et al.) [SECONDARY]. — [艾邦](https://www.ab-sm.com/a/75667)
- **Adhesion-layer failure:** failure is at Ti–Cu interface debonding after 400–1600 h HAST (Corning). — [ScienceDirect S0026271422003079](https://www.sciencedirect.com/science/article/abs/pii/S0026271422003079). The same holds for Ti–Cu micro-defects and through cracks under HAST (XMU). — [CNKI](http://dbase2.gslib.com.cn/KCMS/detail/detail.aspx?filename=JBXK202310018&dbcode=CJFD&dbname=CJFD2023). Under aging, Cu/Ti interface voids and microcracks grow into through-thickness sidewall cracks driven by shear (Sun & Zhang 2026). — [ScienceDirect author page](https://www.sciencedirect.com/author/56437796500/shuye-zhang)
- **Step coverage:** PVD (line-of-sight) seed and barrier layers give poor step coverage in high-AR TGVs. ALD stacks fix coverage (97.7% at 25:1) at higher cost and lower throughput. — [ALD TiO2/TiN/Ru/Cu](https://www.sciencedirect.com/science/article/abs/pii/S1369800125010224); [USPTO 12628669 "Through glass via with a metal wall"](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12628669); [Park et al. 2026 review](https://www.mdpi.com/2072-666X/17/6/720)
- **Electrical penalty of conformal vias:** +0.25 dB per TGV at 30 GHz vs full fill (measured). — [IEEE EPS TC](https://eps.ieee.org/wp-content/uploads/2025/11/Glass_Substrates_Adv_Substrates_TC_UPDATED_Nov25.pdf). This is contradicted in magnitude by an EM simulation claiming near-identical loss (skin effect; source unverified).
- **Polymer liners can peel** from sidewalls, and compressible liners consume plating cross-section. This is the stated motivation for metallic porous-Cu buffers. — [Intel porous Cu liner application](https://trea.com/information/porous-copper-liner-for-through-glass-via-tgv-glass-cores/patentapplication/edc94632-2fe9-410d-b95d-12772cd3acf4)
- **Anneal-window contradiction:** moderate annealing relieves glass stress, but prolonged annealing creates residual tensile stress and cracks. — [Wang et al. 2026](https://www.nature.com/articles/s41378-026-01162-y). This sits against Corning's recommendation of longer pre-anneal dwell to stabilize protrusion. — [IEEE 9353697](https://ieeexplore.ieee.org/document/9353697/)
- **Crack type depends on step:** radial cracks form during heating (ramp-rate controlled). — [MR 114092](https://www.sciencedirect.com/science/article/abs/pii/S0026271421000585). Circumferential cracks form during cooling (Cu-thickness controlled). — [TDMR 9481891](https://ieeexplore.ieee.org/document/9481891/). A mitigation that addresses one does not necessarily address the other.
- **Thermal cycling after annealing:** cracks can still occur during thermal cycling even when the ERR is lower than during annealing [SIM]. — [Le & Choa 2024](https://link.springer.com/article/10.1007/s12206-024-0522-1)
- **Laser damage interaction:** sidewall roughness and microcracks from via formation promote seed discontinuity and crack propagation, so buffer effectiveness depends on via-formation quality. — [Park et al. 2026](https://www.mdpi.com/2072-666X/17/6/720)

### Inferences
- **Hoop vs radial trade-off.** Mechanically, a compliant inorganic layer or air gap lowers the radial and hoop stress that the Cu plug transmits to the glass. On cooling, though, the Cu shrinks away from the wall, so the radial tensile load moves onto the weakest interface (Ti/Cu, or buffer/Cu). This matches the experimental observation that interface delamination and Ti/Cu cracking dominate once glass cracking is controlled. It is inferred from the combined sources, not from a single study.
- **Validation gap.** Only Corning (HPFS fused silica) has experimental crack-incidence-vs-parameter curves: Cu thickness (12 μm) and heating rate (6.5 °C/min). These were obtained on fused silica (CTE ~0.5 ppm/K). Thresholds for borosilicate, alkali-free display glass or glass-ceramic cores (CTE 3–9 ppm/K) are not established in the sources found. Le, Yoo, Choa's simulation suggests higher-CTE glasses are more crack-tolerant.
- **Contradictory headline numbers.** The inorganic-buffer stress reduction is reported as 49.3% (news, TiO2, heating) and 66.58% (listing, 5 μm TiO2). These likely refer to different thickness or load cases. Neither has been verified against the paper, and the "1 μm → 40%" figure has no traceable source.

### Gaps
- No experimental comparison of inorganic buffers (TiO2/ZnO/ZrO2/Al2O3/SiNx) vs polymer buffers vs no buffer in real TGVs, with crack counts or measured stress, was found.
- No published data on hermeticity loss, moisture ingress or Cu pumping in air-gap TGVs.
- No data on the thermal-cycling fatigue life of thin (≤100 nm) Ti or TiN liners in TGVs beyond HAST and aging observations.
- Absolics, SKC, Samsung, LG Innotek, BOE and DNP patent disclosures on via-level non-polymer buffers were not found in the searches performed.
