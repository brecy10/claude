# TSV/TPV stress-buffer liners as analogs for TGV: transferable concepts, buffer-layer modeling methods, and electrical/RF/thermal/reliability penalties

> Scope note. Most evidence below comes from **Si TSVs** (tagged **[TSV/Si]**). Transfer to glass needs care. Glass (borosilicate or alkali-free, E ≈ 70–75 GPa, CTE ≈ 0.5–3.5 ppm/K for fused silica to boro-aluminosilicate, k ≈ 1 W/m·K) is brittle and has no MOSFET mobility "keep-out zone". It has no MOS depletion capacitance, and it is a far poorer heat spreader than Si (k ≈ 150 W/m·K). Glass-side evidence is tagged **[TGV/glass]**.
>
> Tool limits. In this session the full-text fetch tools failed: DNS errors from WebFetch, and the proxy returned 403 for IEEE, ScienceDirect, ResearchGate, arXiv and university hosts. Quoted numbers therefore come from search-engine abstracts and snippets of the cited pages, not from reading the full texts. Numbers marked "(unverified)" could not be confirmed against a retrievable source. Rows labeled **"own calc"** are back-of-envelope results I computed with closed-form models (scripts in scratchpad). They use typical handbook or datasheet properties that I did not verify in this session: Cu E = 120 GPa, ν = 0.34, α = 17 ppm/K; Si 130 GPa, 0.28, 2.6 ppm/K; boro glass 73 GPa, 0.22, 3.2 ppm/K; fused silica 72 GPa, 0.17, 0.55 ppm/K; SiO2 liner 70 GPa, 0.5 ppm/K; BCB 2.9 GPa, 0.34, 42 ppm/K; standard PI 3.0 GPa, 40 ppm/K; low-CTE PI 8.5 GPa, 3 ppm/K; parylene-C 2.8 GPa, 0.40, 35 ppm/K. They are trend indicators, not literature data.

## Q1. Which TSV polymer, low-k, air-gap and annular/coaxial buffer concepts work, by how much, and which transfer to glass?

### Takeaway
In Si TSVs, soft liners (BCB, VDP-polyimide, parylene, SU-8, PPC) and air gaps consistently lower the stress in the substrate and the interfacial energy release rate (ERR). Reported gains include about 29% lower von Mises stress for a 500 nm BCB liner versus SiO2, roughly 22% smaller KOZ for coaxial-annular TSVs, and about 80 MPa residual stress with air-gap liners. The cost is a less constrained Cu plug, which shows larger axial expansion and protrusion. In glass the relative benefit of a compliant liner is smaller than in Si, because glass (about 70 GPa) is already more compliant than Si (130–169 GPa). The TSV-specific motivation (transistor mobility and KOZ) also does not exist in glass; there the metrics that matter are glass hoop tension, interface ERR and RDL-edge stress.

### Cited Findings

**Polymer liners (BCB, PI, parylene, SU-8, PPC): stress [TSV/Si]**
- The Young's modulus of BCB is much lower than that of Cu, Si and SiO2, so a BCB liner absorbs CTE-mismatch stress. Thicker liners lower the stress at the TSV edge, most strongly for BCB, and BCB lowers the maximum interfacial-crack ERR relative to SiO2. These are full-chip FEA/semi-analytical results (GT/UT Austin full-chip group). — [Jung et al., TSV stress-aware full-chip mechanical reliability (GT)](https://gtcad.gatech.edu/www/papers/06238396.pdf); [Full-chip TSV interfacial crack analysis (GT)](https://gtcad.gatech.edu/www/papers/06105386.pdf)
- "A 500-nm-thick BCB liner can reduce the von Mises stress by 29% compared with SiO2 liner", which met the yield criterion for all circuits tested. The baseline uses a 5 µm TSV with a 125 nm liner, and KOZ = 1.205 µm (TSV_A) and 2.44 µm (TSV_B) from the TSV edge at the 45 nm node. — [UT Austin/GT, J47 full-chip TSV reliability](https://www.cerc.utexas.edu/utda/publications/J47.pdf); [same group, C114](https://www.cerc.utexas.edu/utda/publications/C114.pdf)
- A SiO2 liner acting as a buffer reduces σrr at the TSV edge by only about 35 MPa, which is small next to BCB. (The snippet came from the same full-chip search cluster; exact paper attribution unverified.) — [J47](https://www.cerc.utexas.edu/utda/publications/J47.pdf)
- An analytical TSV thermal-stress model with FEM validation (Xidian Univ., Chinese Physics B 2015) found that the liner absorbs CTE-mismatch stress and that stress decreases as the liner gets thicker. It concluded that BCB is a better liner material than SiO2 and that the Cu diffusion barrier has negligible effect on stress. — [CPB 24(5) 056601, 2015](https://iopscience.iop.org/article/10.1088/1674-1056/24/5/056601)
- Tohoku Univ. (Murugesan, Fukushima, Koyanagi et al.) developed a CVD/vapor-deposition-polymerized (VDP) polyimide liner. Micro-Raman and micro-XRD showed it "tremendously reduces" thermo-mechanical stress in the nearby Si compared with PECVD SiO2, which they attribute to the soft PI absorbing Cu expansion. Raman was measured before and after thermal cycling (IEDM 2014, DOI 10.1109/IEDM.2014.7047054). The liner was reported stable at 350 °C (SSDM 2013). Exact stress values are not in the snippets (unverified). — [IEDM 2014 "Highly beneficial organic liner…"](https://www.researchgate.net/publication/273003298_Highly_Beneficial_Organic_Liner_with_Extremely_Low_Thermal_Stress_for_Fine_Cu-TSV_in_3D-Integration); [Low-temperature high-step-coverage PI liner by VDP](https://www.researchgate.net/publication/301383064_Low-Temperature_and_High-Step-Coverage_Polyimide_TSV_Liner_Formation_by_Vapor_Deposition_Polymerization); [VDP PI for via-last](https://www.researchgate.net/publication/312633908_Characterization_of_Vapor_Deposited_Polyimides_and_Process_Integration_with_the_Polymeric_Liner_for_Via-LastBackside-Via_Cu-TSV_Formation); [On-wafer thermomechanical characterization of VDP PI vs PECVD SiO2](https://www.researchgate.net/publication/342805207_On-wafer_thermomechanical_characterization_of_a_thin_film_polyimide_formed_by_vapor_deposition_polymerization_for_through-silicon_via_applications_Comparison_to_plasma-enhanced_chemical_vapor_depositi)
- The same Tohoku group has a paper titled "Replacing the PECVD-SiO2 … with organic liner: merits and demerits", which signals known trade-offs. Its content was not retrieved. — [ResearchGate 266203177](https://www.researchgate.net/publication/266203177_Replacing_the_PECVD-SiO_2_in_the_Through-Silicon_Via_of_High-Density_3D_LSIs_with_Highly_Scalable_Low_Cost_Organic_Liner_Merits_and_Demerits)
- An FE study of BCB-lined TSVs (Microelectronics Reliability 2013) concluded that BCB liners "reduce the thermal induced stresses in substrates, but increase the axial thermal expansion of copper plugs". This is the clearest statement of the stress-versus-protrusion trade-off. — [Reliability of TSVs with BCB liners, Microelectron. Reliab. 2013](https://www.sciencedirect.com/science/article/abs/pii/S0026271413000036)
- A Raman spectroscopy study combined with FE at elevated temperature looked at high-aspect-ratio BCB-lined TSVs. Void-free BCB was achieved with a vacuum-assisted filling method, and wafer curvature was used alongside Raman. — [Near-surface stresses around TSVs at elevated temperature, Raman + simulation](https://www.researchgate.net/publication/272376144_Study_of_Near-Surface_Stresses_in_Silicon_Around_Through-Silicon_Vias_at_Elevated_Temperatures_by_Raman_Spectroscopy_and_Simulations)
- A spin-on poly(propylene carbonate) polymer insulation in annular trenches (5 µm wide × 50 µm deep) used a wettability-enhanced solvent fill. It gave resistance below 100 mΩ and a capacitance density of 2.45 nF/cm², about one tenth of SiO2-insulated TSVs. Low-modulus polymer is cited as absorbing Cu expansion. The search summary attributed this to imec, but I believe it is the Tsinghua (Z. Wang) group (affiliation unverified). — [Microelectron. Eng. 2012, HAR low-capacitance TSVs with polymer insulation](https://www.sciencedirect.com/science/article/abs/pii/S0167931712005734)
- "A low-modulus liner can act as a buffer between the via conductor and the substrate." — [Innovative PI liner deposition for HAR TSVs, Microelectron. Eng. 2015](https://www.sciencedirect.com/science/article/abs/pii/S0167931715300551)
- About a 5 µm BCB interlayer visibly relaxes the thermal stress around Cu TSVs, especially at the Cu/Si interface. This is from vendor-related (EVG) material and the source identity is unverified. — [3D InCites](https://www.3dincites.com/?p=8078); [EVG lithography for 3DIC pdf](https://www.circuitnet.com/news/uploads/2/Lithography_for_3DIC_HVM_EVGroup_1.pdf)
- Fill or underfill polymer comparison in an 8-layer TSV stack: von Mises stress was highest with ABF, then BCB, lowest with NUF, and **the CTE of the filler dominated Cu-via stress**. — [SeoulTech, 8-layer stacked TSV reliability](https://pure.seoultech.ac.kr/en/publications/study-of-thermo-mechanical-reliability-of-tsv-for-8-layer-stacked/)
- Georgia Tech (Bakir group; Thadesar dissertation 2015) built polymer-clad TSVs and polymer-embedded vias (PEVs, Cu vias in SU-8 wells in low-resistivity Si). A thick polymer liner, unlike thin SiO2, "helps reduce TSV stress and electrical loss". — [Thadesar dissertation 2015](https://www.bakirlab.gatech.edu/sites/default/files/%5BThesis%5D/THADESAR-DISSERTATION-2015.pdf); [Polymer-enhanced TSVs, inductors, antennas (Bakir lab)](https://bakirlab.ece.gatech.edu/papers/Fabrication%20and%20characterization%20of%20polymer-enhanced%20TSVs,%20inductors%20and%20antennas%20for%20mixed-signal%20silicon%20interposer%20platforms.pdf)
- A review in *Engineering* (IMECAS 2023) notes that polymers such as SU-8 used in place of the dielectric reduce substrate stress and parasitic capacitance together. — [Engineering 2023, low-stress TSV array](https://www.engineering.org.cn/engi/CN/10.1016/j.eng.2023.11.023)

**Low-k inorganic and oxide liner effects on Cu pumping [TSV/Si]**
- imec found that the effect of liner elastic modulus on *residual* Cu pumping is low and matches FEM trends. A **low-k dielectric liner decreased residual Cu pumping and TSV stress** compared with O3-TEOS and ALD SiO2 liners. — [Impact of oxide liner properties on TSV Cu pumping and TSV stress](https://www.researchgate.net/publication/273146056_Impact_of_oxide_liner_properties_on_TSV_Cu_pumping_and_TSV_stress)
- A patent on liner densification argues the opposite direction for stiffness: a denser, stiffer liner changes less in the radial direction during anneal, "leading to more TSV metal protrusion … in the axial direction". Radial compliance therefore relieves the hydrostatic constraint that drives axial plastic extrusion. — [US 10163655 Through substrate via liner densification](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10163655)
- A 2024 FEM study of TSV annealing found that Cu sidewall expansion is restrained by slight Si protrusion near the sidewall. Cu shows reversible thermal expansion plus irreversible plastic deformation. — [Microsyst. Nanoeng. 2024, sidewall Cu grain condition](https://www.nature.com/articles/s41378-024-00830-1)

**Air-gap TSVs [TSV/Si]**
- Tsinghua (Huang, Chen, Wu, Z. Wang, 2013) made air-gap TSVs with a sacrificial polymer and vacuum-assisted solvent refilling for the thin sidewall cladding. Accumulation capacitance was **48 fF** and leakage **1.22 pA at 20 V**. The index page is weak and the full text was not retrieved. — [index entry](https://manuscript.isc.ac/Inventory/49/7085.htm)
- The *Engineering* 2023 review cites Huang et al.: an air gap replacing SiO2 gives the metal room to deform radially and lowers stress to about **80 MPa**. — [Engineering 2023](https://www.engineering.org.cn/engi/CN/10.1016/j.eng.2023.11.023)
- A*STAR IME formed embedded air gaps in Si around via-middle TSVs by a high-temperature anneal in a de-oxidizing ambient. Thermo-mechanical simulation showed stress isolation from CMOS without enlarging the KOZ. The KOZ numbers were not in the snippets. — [A*STAR OAR pdf](https://oar.a-star.edu.sg/storage/v/vdqy8np1eo/a-novel-method-for-air-gap-formation-around-via-middle-vm-tsvs-for-effective-reduction-in-keep-out-zones-koz.pdf)
- Patent claims (not independently verified): a ~17 nm air gap protects a 5 µm TSV up to 400 °C and allows transistors <1 µm from the TSV. — [US 9425127](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9425127); [US 8962474](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/8962474)
- Stress-relief structures reduce KOZ to ≤1 µm against a "typical" 20 µm (patent claim). — [US 9214374](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9214374)
- A BIT silicon–air–silicon TSV reached a capacitance density of 0.137 nF/cm². — [BIT pure](https://pure.bit.edu.cn/zh/publications/a-novel-silicon-air-silicon-through-silicon-via-structure-realize/)
- IMECAS (Jiao Binbin team) reported a hollow "rugby-ball" TSV with stress-release space, giving residual stress of **31.02 MPa**. This is from a press release, not a journal paper. — [IMECAS news 2024](https://ime.cas.cn/kygz/kydt/202404/t20240426_7133192.html)

**Annular, coaxial and ATI TSVs [TSV/Si]**
- Coaxial-annular TSVs reduce KOZ by **1.6 µm (22.2%)** relative to coaxial TSVs while keeping coaxial signal integrity, which beats cylindrical and annular designs. The work used an analytical thermal-stress model with FEM and studied Cu plasticity, TSV material, size and inner plating ratio (Wang et al., IEEE TED 61(8):2928–2934, 2014). — [IEEE TED 2014](https://ieeexplore.ieee.org/document/6845357/)
- Experimentally, a nested coaxial-TSV array needs transistor spacing of about **4 µm (analog)** and **2 µm (digital)** (Adamshick 2018). — [IET Micro & Nano Letters 2018](https://digital-library.theiet.org/doi/10.1049/mnl.2018.5280)
- An annular-trench-isolated (ATI) TSV used 2 µm parylene-HT in 10 µm ATI TSVs and showed lower simulated Si stress than regular or annular TSVs. — [Microelectron. Reliab. 2016, ATI-TSV](https://www.sciencedirect.com/science/article/abs/pii/S0026271416300853)
- **Scaling caveat:** simulation shows that replacing SiO2 with parylene, or using annular TSVs, *loses stress-reduction effectiveness as TSVs scale down*, which motivated the ATI design. — [IEEE 7159725, ECTC 2015](https://ieeexplore.ieee.org/abstract/document/7159725/)
- Parylene-HT is room-temperature conformal and pinhole-free, and is stable to about 350 °C. — [Parylene-HT liner bottom-up Cu TSV](https://www.researchgate.net/publication/282177249_Fabrication_and_electrical_characterization_of_Parylene-HT_liner_bottom-up_copper_filled_through_silicon_via_TSV)
- A patent model reports that large voids at the TSV bottom reduce maximum stress 5× (attribution to a specific patent in the result set is unverified). — [US 10886195](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10886195)

**KOZ and mobility context [TSV/Si; not applicable to glass]**
- KOZ area for p-MOSFETs grows roughly with D² of the TSV. One secondary caption states TSV stress cannot change mobility by more than about 10% (unverified) (Ryu et al., IEEE TDMR 2012, DOI 10.1109/TDMR.2012.2194784). — [figure caption](https://www.researchgate.net/figure/Effect-of-TSV-diameter-on-Keep-out-Zone_fig9_228854224)
- Large KOZs can cost up to 4× chip area and 2× wirelength in stress-driven placement studies. — [academia.edu, stress-driven 3D-IC placement](https://www.academia.edu/26843228/Stress_driven_3D_IC_placement_with_TSV_keep_out_zone_and_regularity_study)

**Glass analogs of buffer concepts [TGV/glass]**
- Georgia Tech built polymer-laminated glass with tailored CTE and found it **reduces TPV thermomechanical stress**. The recommendation is to pair **higher-CTE glass with lower-CTE polymer**. TPVs were plated both conformal (annular) and fully filled. — [Reliability of fine-pitch through-vias in glass (J Mater Sci: Mater Electron 2018)](https://link.springer.com/article/10.1007/s10854-018-9384-6); [academia copy](https://www.academia.edu/90067663/Reliability_of_fine_pitch_through_vias_in_glass_interposers_and_packages_for_high_bandwidth_computing_and_communications)
- In TGV structures, using polymer "structure B" lowered stress at both the TGV and RDL edges, because the polymer's E and CTE are smaller than Cu's and it acts as a buffer. Polymer "structure A" *raised* stress at the TGV edge while lowering it at the RDL edge. Increasing polymer thickness lowered edge stresses (Zhao, Chen, Qin, Yu, Micromachines 13:1799, 2022). — [Micromachines 2022](https://www.mdpi.com/2072-666X/13/10/1799); [PMC copy](https://pmc.ncbi.nlm.nih.gov/articles/PMC9607209/)
- A glass-substrate review states that polymer buffer layers significantly reduce TGV stress, and that FE showed a ">75% reduction in ERR compared to solid vias". The structure behind that number was not retrieved. — [MDPI review of glass substrate technologies](https://www.mdpi.com/2674-0729/4/3/37)
- A patent describes TGV dielectric liners as "a buffer or a compliant layer" relieving CTE-mismatch stress. — [US 12087623 Dielectric liners on through glass vias](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12087623)
- A low-temperature-cured Cu paste fill of 30 µm and 100 µm TGVs in 130 µm and 300 µm glass panels is pursued "for lower stress" than electroplated Cu. — [GT thesis, panel glass packaging](https://repository.gatech.edu/server/api/core/bitstreams/fdc8e606-3f53-4562-8b17-1c147de9c767/content)

### Inferences
- **Own calc: 3-layer elastic Lamé model, generalized plane strain, 50 µm hole, ΔT = ±250 K.** Glass-wall radial and hoop stress magnitude, |σ| at r = b, by substrate and liner:
  - **Si, no liner:** 360 MPa. SiO2 0.5 µm: 342 (−5%). BCB at 1/2/5/10 µm: 240/189/129/100 (−33/−48/−64/−72%).
  - **Borosilicate glass, CTE 3.2, no liner:** 228 MPa. SiO2 0.5 µm: 218 (−4%). BCB at 1/2/5/10 µm: 177/149/112/91 (−23/−35/−51/−60%). Parylene-C at 1/2/5/10 µm: 189/166/131/109. Low-CTE PI (8.5 GPa, 3 ppm/K) at 10 µm: 37 MPa (−84%).
  - **Fused silica, no liner:** 278 MPa. BCB 5 µm: 127 MPa.
  - **Why glass benefits less:** a compliant liner gives a smaller *relative* reduction in glass than in Si, because glass is already about half as stiff.
  - **Fixed-hole confound:** about half of the "thick-liner" benefit comes from the smaller Cu core when the hole diameter is fixed.
  - **Liner CTE matters:** a high-CTE polymer (35–42 ppm/K, more than Cu's 17) adds its own mismatch, so a low-CTE PI outperforms BCB at large thickness. This agrees with the SeoulTech result that filler CTE dominates.
  - **Elastic upper bound:** these are upper bounds. Cu plasticity caps the absolute values, but the ratios show the trend.
- **Sign and failure mode in glass (own calc plus standard Lamé physics).** On heating, glass hoop stress at the wall is tensile, which drives radial cracks in glass, for example during Cu anneal. On cooling, interfacial radial stress is tensile, which drives Cu/glass delamination. A buffer liner reduces both. Glass has no plastic relief, so hoop tension on heating matters more for TGV than for TSV.
- **What does not transfer:**
  - KOZ in the MOSFET-mobility sense, and Raman-based Si stress metrics, have no direct equivalent in glass. The glass analogs are hoop-stress (radial crack) margins, ERR at the Cu/liner/glass interfaces, surface ring cracks, and RDL-edge stress.
  - Air gaps formed by de-oxidizing anneal in Si (A*STAR) and silicon-air-silicon schemes do not transfer directly. A glass analog would be a sacrificial-polymer or annular etched gap, or a hollow/conformal Cu TGV, which Georgia Tech already uses.
- **What does transfer:** compliant polymer liners (BCB, VDP-PI, parylene-HT), annular/coaxial geometry, and "soft fill inside conformal Cu". Glass favors **low-CTE, moderate-modulus** polymers (low-CTE PI) over high-CTE BCB or parylene, because a high-CTE liner on a low-CTE glass creates a second mismatch interface.
- **Scaling caveat (from ECTC 2015) applies to fine-pitch TGV (≤10–20 µm):** liners thin enough to fit stop helping much.

### Gaps
- Full-text numbers were not retrieved for: Tohoku PI-liner Raman values; the Tsinghua BCB-liner Raman stress; A*STAR air-gap KOZ; and GT full-chip BCB-thickness ERR percentages.
- No KOZ-percentage comparison of BCB versus SiO2 was found.
- No specific polymer-liner TSV stress papers were found from imec (beyond the oxide/low-k pumping work), Fraunhofer IZM, KAIST or IME Singapore. The polymer annular-fill attribution (imec versus Tsinghua) is unresolved.
- No experimental Raman, photoelasticity or birefringence measurement of a polymer-lined TGV was found in this search. Other researchers may cover TGV-specific literature.

## Q2. How should a via with a buffer layer be modeled (analytical, fracture, constitutive, numerical), and what design rules exist?

### Takeaway
Standard practice has four layers:
1. Closed-form 2D or generalized-plane-strain Lamé (concentric-cylinder) solutions for far-field trends.
2. 3D FEA of the near-surface free-edge region, where interfacial stresses are singular and drive delamination and protrusion.
3. Fracture mechanics: a steady-state ERR as an upper bound plus crack-length-dependent ERR from FEA.
4. Elastic-plastic or creep Cu with temperature- and time-dependent (viscoelastic) polymer.

Published results agree on these scalings: ERR ∝ D·(ΔαΔT)², cooling is the worse case for delamination, and a soft liner reduces substrate stress but can raise the axial expansion of Cu and change the crack-length dependence of the ERR. No universal closed-form "optimal liner thickness" rule was found.

### Cited Findings
**Analytical (Lamé, concentric cylinders)**
- In the UT Austin model (Ryu, Lu, Zhang, Im, Ho, Huang), near-surface 3D stresses differ qualitatively from the 2D Lamé solution, and the free surface creates the interfacial shear and normal stresses that drive delamination. The steady-state ERR is an analytical *upper bound* for interfacial delamination, checked by FEA, and is **linearly proportional to via diameter**, which sets an upper bound on D (IEEE TDMR 2011, DOI 10.1109/TDMR.2010.2068572). Using W instead of Cu lowers the driving force. — [Impact of near-surface thermal stresses on interfacial reliability of TSVs](https://www.researchgate.net/publication/224169323_Impact_of_Near-Surface_Thermal_Stresses_on_Interfacial_Reliability_of_Through-Silicon_Vias_for_3-D_Interconnects); [academia copy](https://www.academia.edu/1790780/Impact_of_Near_Surface_Thermal_Stresses_on_Interfacial_Reliability_of_Through_Silicon_Vias_for_3_D_Interconnects)
- The ERR approaches steady state once the crack is several via diameters long; one write-up says about 2–3 D. — [UT Austin repository](https://repositories.lib.utexas.edu/server/api/core/bitstreams/7407b0a3-c02a-4156-9017-6263411eeb42/content); [AIP Conf. Proc. 2011](https://sites.utexas.edu/ruihuang/files/2021/03/AIP2011.pdf)
- **BCB liner (UT Austin ECTC 2010):** "a soft polymer liner can reduce the thermal stress in the silicon matrix, but it may affect the driving force for delamination in two ways, depending on crack length." The detailed direction (short versus long crack) was not retrieved (unverified). — [ECTC 2010, Thermal stress induced delamination of TSVs](https://sites.utexas.edu/ruihuang/wp-content/uploads/sites/6034/2021/03/ECTC2010.pdf)
- The Xidian analytical model (CPB 2015) includes liner and barrier layers in a multi-layer concentric model validated by FEM. — [CPB 2015](https://iopscience.iop.org/article/10.1088/1674-1056/24/5/056601)
- An analytical estimate exists for stress around doubly periodic TSV arrays (title only), relevant to pitch effects. — [ResearchGate 256815510](https://www.researchgate.net/publication/256815510_Analytical_estimates_of_stress_around_a_doubly_periodic_arrangement_of_through-silicon_vias)
- The coaxial-annular TSV work combined an analytical thermal-stress model with FEM, including Cu plasticity. — [IEEE TED 2014](https://ieeexplore.ieee.org/document/6845357/)
- Ryu et al. modeled a plasticity mechanism for Cu extrusion in TSVs (title only). — [ResearchGate 260704927](https://www.researchgate.net/publication/260704927_Plasticity_mechanism_for_copper_extrusion_in_through-silicon_vias_for_three-dimensional_interconnects)

**Fracture and ERR in glass [TGV/glass]**
- Coupled FEM and ERR model of Cu-filled TGVs (Microelectronic Engineering 2025):
  - **ERR ∝ via diameter (linear) and ∝ ΔT² (quadratic)**.
  - ERR peaks at a crack length of **about D/4**.
  - **Fused silica gives the highest stress and ERR**, while a "ceramic glass" (glass-ceramic) is more reliable.
  - [Effect of thermally-induced cracks on TGVs, Microelectron. Eng. 2025](https://www.sciencedirect.com/science/article/abs/pii/S0167931725001303)
- The ERR from **cooling exceeds that from heating**, so cooling is more likely to cause TGV–Cu delamination and cracking. For ringed (annular) TGVs, the ERR is expressed in terms of the mismatch strain Δα·ΔT and the inner/outer diameter ratio φ. — [Micromachines 2022](https://www.mdpi.com/2072-666X/13/10/1799); [Semantic Scholar pdf](https://pdfs.semanticscholar.org/ed57/eaec1ba767db3ed61677321486c90bd9334e.pdf)
- Georgia Tech: the ERR for Cu delamination from glass along the TPV sidewall increases linearly with TPV diameter, because crack-area growth is proportional to D. — [Springer 2018](https://link.springer.com/article/10.1007/s10854-018-9384-6)
- A 2024 numerical crack-prevention study for 2.5D glass interposers found that TGV cracks can be reduced or eliminated by choosing the glass, the annealing temperature and the Cu via structure. — [J. Mech. Sci. Tech. 2024](https://link.springer.com/article/10.1007/s12206-024-0522-1)
- A study of the time and temperature dependence of residual stress and protrusion in TGVs (2026) shows that the time-dependent (creep/relaxation) behavior of TGV Cu is under active study. Details were not retrieved. — [Microsyst. Nanoeng. 2026](https://www.nature.com/articles/s41378-026-01162-y)

**Submodeling, edge singularity, cohesive zones, viscoelasticity**
- TGV interposer layout stress has been studied with **submodeling** plus a factorial design. — [Micromachines 14:1506 (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC10456845/)
- A pitch of at least 2× via diameter minimized neighbor stress interaction in one TGV simulation (attribution within the search set unverified). — [MDPI 2674-0729/4/3/37](https://www.mdpi.com/2674-0729/4/3/37)
- The free-edge interface singularity is where high stress concentrates. A compliant (nanostructured) interlayer can **eliminate the free-edge singularity** (thin-film study, not TSV). — [Eng. Fract. Mech., singularity disappearance](https://www.sciencedirect.com/science/article/abs/pii/S0013794407004456)
- Cohesive-zone practice: a bilinear traction-separation law reduces numerical singularity artifacts. Rate-dependent CZMs separate a viscoelastic liner's bulk deformation from true interface separation (HTPB liner, non-TSV). — [arXiv 2209.09387](https://arxiv.org/pdf/2209.09387); [Polymer Testing 2025, rate-dependent CZM](https://www.sciencedirect.com/science/article/pii/S0142941825001126)
- The standard route to polymer viscoelasticity is Prony series with time-temperature shift factors from master curves. Each Prony term adds FE state variables, so short series are preferred. — [NASA TM-2000-210123](https://ntrs.nasa.gov/api/citations/20000052499/downloads/20000052499.pdf)
- In glass TPVs, the CTE mismatch among Cu, glass and polymer causes Cu plastic deformation during thermal cycling, which leads to fatigue. This needs an elastic-plastic Cu model with fatigue-life (Coffin–Manson-type) post-processing. Plastic strain rises as glass gets thinner. — [Springer 2018](https://link.springer.com/article/10.1007/s10854-018-9384-6); [Reliability of Cu TPVs in bare glass](https://www.academia.edu/119963275/Reliability_of_Copper_Through_Package_Vias_in_Bare_Glass_Interposers)

### Inferences
- **Recommended modeling stack for a TGV buffer liner.** This is synthesized from the sources above and is not a published standard.
  1. **Screening:** a 3-layer generalized-plane-strain Lamé solution (Cu / liner / glass). In each layer u_r = A·r + B/r. Take B = 0 in Cu and the free-expansion far field in glass. Impose u_r and σ_rr continuity at r = a and r = b, with ε_z = α_glass·ΔT in all layers. This gives the wall hoop and radial stress and the Cu pressure within seconds (see Q1 own calc). Add the periodic (pitch) correction or superposition for arrays.
  2. **Near-surface 3D axisymmetric FEA:** mesh to the singular corner where Cu, liner, glass and RDL meet. Extract interfacial σ_n and τ at the free edge, the Cu protrusion, and the glass surface hoop stress. Use the Ryu-type steady-state ERR as the upper bound, and the FEA crack-length sweep (expect a peak near D/4 per the 2025 TGV study) via J-integral or VCCT.
  3. **Constitutive models:** Cu as elastic-plastic with temperature-dependent yield and kinematic hardening, plus creep or relaxation above about 150–200 °C. The polymer as linear viscoelastic (Prony + WLF/Arrhenius shift) with a modulus drop through Tg. A purely elastic polymer model overpredicts liner stiffness above Tg and misses relaxation during anneal dwell.
  4. **Interfaces:** cohesive zones (bilinear TSL with mode mixity) at Cu/liner and liner/glass, with toughness from four-point bend or stud-pull data. Glass radial and ring cracks via XFEM or a Weibull flaw-population check, because glass fails from flaws rather than by yield.
  5. **Submodeling** from interposer or package scale (warpage, CTE of build-up) down to the via cell.
- **Trend rule (synthesis):** a softer and thicker liner gives (i) lower substrate hoop and radial stress, (ii) lower Cu hydrostatic stress and therefore *lower residual* plastic pumping (consistent with imec's low-k result and the densified-liner patent), but (iii) *larger reversible axial Cu expansion and protrusion* at temperature and higher shear on the Cu/liner interface near the free surface (consistent with the BCB Microelectronics Reliability 2013 statement). The two are not contradictory: residual (plastic) pumping and reversible thermal protrusion are different quantities, and both must be reported.
- **Own calc: thin-interlayer shear-lag transfer length.** L* = √(E_Cu·a·t / (2·G_liner)), with a 50 µm hole:
  - SiO2 0.5 µm: about 5 µm.
  - BCB, PI or parylene at 1–10 µm: about 36–95 µm.
  - Low-CTE PI at 1–10 µm: about 21–53 µm.
  - **Consequence:** in typical 100–500 µm-thick glass, a polymer liner makes L* comparable to the via half-length. The Cu is then nearly decoupled axially, and elastic end displacement grows from about 18 nm (SiO2) to about 130–340 nm (polymer) for ΔT = 250 K, from ε_mis·L* ≈ 3.45×10⁻³·L*. This quantifies the protrusion penalty and suggests a modulus/thickness window, for example a liner with G ≥ about 3 GPa and t of about 2–5 µm (own estimate, not validated).
- **Closed-form design rules found (scalings only):** ERR_ss ∝ E·(Δα·ΔT)²·D. ERR increases with D, quadratically with ΔT, and peaks at a crack about D/4 for TGV. KOZ (Si) area ∝ D². The cooling case controls delamination; the heating case controls glass hoop-tension radial cracks (own inference from Lamé signs). No published closed-form optimum liner t or E was found.

### Gaps
- No TSV or TGV paper was found that combines a viscoelastic BCB or PI liner (Prony, Tg) with Cu plasticity and a cohesive-zone free edge. This combination appears to be open.
- The exact Ryu steady-state ERR expression and its BCB-liner variant (and which crack-length regime gets worse) could not be retrieved.
- No experimentally validated optimum liner thickness or modulus was found for glass.
- Glass fracture toughness and Weibull data for TGV sidewalls (laser-modified plus etched) were not covered here.

## Q3. What electrical, RF, thermal and current-carrying penalties or benefits do buffer liners impose?

### Takeaway
In Si, low-k, polymer and air-gap liners are an electrical *benefit*. They cut TSV capacitance by about 27.6% (k ≈ 2.8) and reach about one tenth of SiO2's capacitance density (PPC). Polymer-clad and polymer-embedded vias show up to 80% lower insertion loss at 50 GHz versus state-of-the-art TSVs, because they shield the field from lossy Si.

In glass the substrate is already a low-loss insulator, so a polymer liner gives only modest capacitance reduction (about 10–45% in my coax estimate). Its effect on loss depends on whether the polymer's Df is below or above the glass's Df: BCB (about 0.001–0.009 at mmWave) and parylene-N (<0.0006) help, while PI and SU-8 (0.015–0.055) hurt.

The bigger penalties in glass are less Cu cross-section for a fixed drilled hole (R_dc and axial R_th rise 1.18× at 2 µm and 1.56× at 5 µm per side in a 50 µm hole), impedance shift, and the very low thermal conductivity of polymers (parylene-C 0.10–0.18 W/m·K).

### Cited Findings
**Capacitance and leakage [TSV/Si]**
- A low-k liner (effective k about 2.8) cut TSV capacitance by **about 27.6%** compared with PETEOS oxide. — [TSV with low-κ liner: parasitic capacitance and leakage](https://www.researchgate.net/publication/258672942_Through_Silicon_Via_Fabrication_with_Low-k_Dielectric_Liner_and_Its_Implications_on_Parasitic_Capacitance_and_Leakage_Current)
- BCB-liner TSVs (IEEE TCPMT 2014, Z. Wang et al.): TSV capacitance is modeled as the dielectric capacitance in series with Si depletion capacitance, with a minimum of **28.4 fF**. C-V and I-V were measured from room temperature to 125 °C, and high-temperature stress did not degrade BCB insulation. — [IEEE TCPMT 2014 pdf](https://ieeexplore.ieee.org/iel7/5503870/6979775/06945811.pdf); [ResearchGate](https://www.researchgate.net/publication/273394670_Thermal_and_Electrical_Properties_of_BCB-Liner_Through-Silicon_Vias)
- A high-aspect-ratio PI-liner TSV gave depletion capacitance of **33 fF**, leakage of **2.2 pA at 20 V**, and **0.164 pF/TSV** in arrays (paper attribution likely but unverified). VDP-PI gives lower inter-via capacitance than an SACVD TEOS liner. — [Micromachines 13:1147, 2022](https://www.mdpi.com/2072-666X/13/7/1147); [VDP PI liner](https://www.researchgate.net/publication/301383064_Low-Temperature_and_High-Step-Coverage_Polyimide_TSV_Liner_Formation_by_Vapor_Deposition_Polymerization)
- Tohoku also reported improved C-V and I-V after post-heat-treatment of a co-polymerized organic liner for high-frequency TSVs (title only). — [ResearchGate 283104115](https://www.researchgate.net/publication/283104115_Improved_C-V_I-V_characteristics_for_co-polymerized_organic_liner_in_the_Through-Silicon-Via_for_high_frequency_applications_by_post_heat_treatment)
- Other low-capacitance results: PPC polymer gives 2.45 nF/cm², about one tenth of SiO2 ([Microelectron. Eng. 2012](https://www.sciencedirect.com/science/article/abs/pii/S0167931712005734)); the air-gap TSV gives 48 fF and 1.22 pA at 20 V ([index](https://manuscript.isc.ac/Inventory/49/7085.htm)); the Si–air–Si TSV gives 0.137 nF/cm² ([BIT](https://pure.bit.edu.cn/zh/publications/a-novel-silicon-air-silicon-through-silicon-via-structure-realize/)).
- A patent notes that the large capacitance of a thin isolation layer contributes to TSV signal loss, with example insertion loss of about 0.76 and 0.81 dB at 10 GHz for two conductor designs. — [US 11545416](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11545416)

**RF and mmWave**
- Georgia Tech polymer-embedded vias (SU-8 wells) were characterized to 30 GHz (TCPMT 2016). Georgia Tech reports **up to 80% reduction in TSV insertion loss at 50 GHz** compared with state-of-the-art TSVs (attribution to a specific page within the Georgia Tech site set is unverified). Thicker Si raises TSV capacitance and RF loss. — [Thadesar dissertation](https://www.bakirlab.gatech.edu/sites/default/files/%5BThesis%5D/THADESAR-DISSERTATION-2015.pdf); [GT news](https://hg.gatech.edu/node/280901)
- A silicon-core coaxial TSV (120 µm deep, 40 µm core, 20 µm dielectric gap) showed **about 0.053 dB at 10 GHz**. A cooled variant showed about 0.14 dB at 40 GHz against about 0.2 dB for a typical coaxial-TSV interposer. — [Si-core coaxial TSV](https://www.researchgate.net/publication/316469071_Silicon-core_Coaxial_Through_Silicon_Via_for_Low-loss_RF_Si-interposer?_tp=eyJjb250ZXh0Ijp7InBhZ2UiOiJzY2llbnRpZmljQ29udHJpYnV0aW9ucyIsInByZXZpb3VzUGFnZSI6bnVsbCwic3ViUGFnZSI6bnVsbH19)
- Fabricated coaxial vias avoided a resonance near 20 GHz that the non-coaxial via showed (review). — [Vertical interconnect with coaxial structure](https://www.researchgate.net/publication/384780128_Vertical_Interconnect_Technology_in_Silicon_Package_and_Printed_Circuit_Board_PCB_with_Coaxial_Structure)
- Coaxial ring TSVs have lower insertion loss than cylindrical TSVs (transmission-line analysis). — [Energy Reports 2022](https://www.sciencedirect.com/science/article/pii/S2352484722014652)
- **[TGV/glass] Coaxial TGVs with BCB isolation (Sadhana 2024, simulation):** thicker polymer lowers the polymer capacitance, improves shielding, and lowers insertion-loss magnitude. MWCNT fill beats Cu. — [Sadhana 2024 (ias.ac.in)](https://www.ias.ac.in/public/Volumes/sadh/049/00/0044.pdf)
- **[TGV/glass]** Georgia Tech thin-glass mmWave package: about **0.021 dB per through-package via** and less than 1 dB for the whole chain. — [Tentzeris TMTT 2020](https://tentzeris.ece.gatech.edu/tmtt20_atom.pdf)
- A patent for a coaxial through-hole uses a shield wall with a low-permittivity plug of BCB or perfluoroalkyl polymers. — [US 12672559](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12672559)
- Shielded TSVs with air-gap isolation have been characterized for RF/mmWave (title only). — [ResearchGate 377681524](https://www.researchgate.net/publication/377681524_Electrical_Characterization_of_Shielded_TSVs_With_Airgap_Isolation_for_RFmmWave_Applications)

**Liner dielectric data (mmWave and sub-THz)**
- **BCB:** Dk about 2.65. tanδ about 0.001–0.009 over 11–65 GHz ([BCB as mmW substrate](https://www.researchgate.net/publication/225360912_Benzocyclobutene_as_Substrate_Material_for_Planar_Millimeter-Wave_Structures_Dielectric_Characterization_and_Application)). 0.0008–0.002 from 1 MHz to 10 GHz, with permittivity stable to 1.5 THz ([Radioengineering 2011](https://www.radioeng.cz/fulltexts/2011/11_04_785_789.pdf)). ε about 2.45 and loss 7–9×10⁻³ at 1 THz ([Microelectron. Eng. 2008](https://www.sciencedirect.com/science/article/abs/pii/S0167931708003298)).
- **SU-8:** εr about 3.2. tanδ 0.015 at 1 GHz, 0.027 at 200 GHz, 0.055 at 1 THz, strongly dependent on cure ([SU-8 mmW/THz](https://www.researchgate.net/publication/273392849_Permittivity_and_Loss_Characterization_of_SU-8_Films_for_mmW_and_Terahertz_Applications)). About 0.04 at 40 GHz ([US 10361487](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10361487)).
- **Parylene-N:** εr 2.35–2.4, tanδ below 0.0006 to 60 GHz, CTE higher than BCB. — [IEEE TAdvP 2009 (Purdue)](https://engineering.purdue.edu/~yep/Papers/IEEE%20Trans%20Advanced%20Packaging_2009.pdf)
- A survey of low-loss polymers (parylene, PI, SU-8 and others) covers 100 GHz–2 THz; values were not retrieved. — [J Infrared Millim THz Waves 2019](https://link.springer.com/article/10.1007/s10762-019-00584-2)

**Thermal**
- **Parylene-C:** k ≈ **0.10 W/m·K** as deposited, about 0.18 after annealing (TDTR). It is the lowest-k among dense low-k materials and is proposed as a thermal *insulator*. — [arXiv 2603.03737](https://arxiv.org/abs/2603.03737)
- **Polyimide:** about 0.52 W/m·K, from a low-quality datasheet. — [Polyimide properties sheet](https://www.Topline.tv/drawings/pdf/materials/Polyimide_Properties.pdf)
- **BCB:** filled BCB composites reach 0.15–0.5 W/m·K (patent). The unfilled BCB value, often quoted as 0.29 W/m·K, was not verified (unverified). — [US 5232970](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/5232970)
- A TSV compact thermal-model table lists SiO2 at 1.38 W/m·K and Cu at 372 W/m·K. The same table's epoxy value (0.03 W/m·K) looks anomalously low next to typical epoxy (about 0.2) and should be treated as suspect. — [Sadhana compact TSV thermal model](https://www.ias.ac.in/article/fulltext/sadh/046/0035)
- Interfacial thermal resistance and geometry can add excess TSV thermal resistance and create hotspots (review). — [Microelectron. Eng. 2025 thermal-management review](https://www.sciencedirect.com/science/article/abs/pii/S0167931725000140)
- One paper argues SiO2 has better thermal conductivity than alternative dielectric liners, then recommends Al2O3, which is internally inconsistent. — [Materials Today: Proc.](https://www.sciencedirect.com/science/article/abs/pii/S2214785320351828)

### Inferences
- **Own calc: coax-like series-capacitor model.** Cu radius 25−t µm in a 25 µm-radius hole, glass εr 5.5 and tanδ 0.004 out to a 100 µm ground radius (glass values assumed typical, unverified):

  | Liner | t (µm) | C/C₀ | Z/Z₀ | Effective tanδ (vs 0.0040 for bare glass) |
  |---|---|---|---|---|
  | BCB | 2 | 0.89 | 1.09 | 0.0038 |
  | BCB | 5 | 0.75 | 1.25 | 0.0035 |
  | BCB | 10 | 0.57 | 1.55 | 0.0031 |
  | Parylene-N | 5 | 0.73 | — | 0.0031 |
  | PI (tanδ 0.008 assumed) | 5 | 0.79 | — | 0.0048 |
  | SU-8 (0.03) | 5 | 0.78 | — | 0.0096 (2.4×) |
  | SU-8 (0.03) | 10 | 0.61 | — | 0.0141 (3.5×) |

  - **Glass versus Si:** in glass, the liner's capacitance benefit is modest and its loss effect depends on the material. In Si, the large benefit comes from isolating the field from conductive Si and the MOS depletion capacitance, and neither exists in glass.
  - **Design implication:** at mmWave or sub-THz, use BCB, parylene-N/HT or low-Df PI, and avoid SU-8. Re-tune via impedance, since Z rises 9–55% with liner thickness at a fixed hole.
- **Own calc: Cu-area penalty at a fixed 50 µm hole.**
  - Liner t = 0.5/1/2/5/10 µm leaves Cu area at 0.96/0.92/0.85/0.64/0.36 of the bare value.
  - **R_dc and axial thermal resistance of a thermal via** rise by ×1.04/1.09/1.18/1.56/2.78.
  - **Current capacity at a fixed electromigration current density** drops in the same ratio.
  - **Skin-effect regime:** at mmWave, Cu skin depth is about 0.4 µm at 28 GHz and about 0.2 µm at 100 GHz (standard physics), so conductor loss scales with perimeter rather than area. The RF conductor-loss penalty is therefore roughly proportional to the radius ratio, about ×1.09 at t = 2 µm.
  - **Cross-check:** consistent with the Sadhana coaxial-TGV finding that thicker polymer lowers loss through capacitance, though conductor loss rises.
- **Own calc: radial thermal resistance per unit length.**
  - **Reference:** a glass shell from r = 25 to 100 µm (k = 1) gives 0.22 K·m/W.
  - **BCB (k = 0.29 assumed):** about 0.05/0.12/0.28 K·m/W at 2/5/10 µm, i.e. 0.2–1.3× the glass shell.
  - **Parylene-C (k = 0.10):** 0.13/0.36/0.81 K·m/W, i.e. 0.6–3.7× the glass shell.
  - **Conclusion:** in glass (k ≈ 1) a thin liner of 2 µm or less adds little lateral thermal resistance compared with the glass itself. Thick, low-k parylene does matter for lateral spreading into glass. For *vertical* thermal vias, the dominant penalty is the reduced Cu area, not the liner's k. In Si (k ≈ 150), by contrast, a polymer liner dominates lateral thermal resistance, so TSV thermal-penalty conclusions overstate the problem for glass.
- **Electromigration:** no liner-specific EM data were found. A compliant liner gives lower hydrostatic stress in the Cu, which is likely neutral to slightly beneficial for stress-migration voiding (unverified). The EM penalty is mainly current density from the reduced Cu area.

### Gaps
- No paper was found with S-parameters measured on *identical* TGVs with and without a polymer liner at mmWave or sub-THz. The Sadhana coaxial-TGV results are simulation-only.
- No measured thermal resistance of polymer-lined thermal TGVs or TSVs was found.
- The unfilled-BCB thermal conductivity, the parylene-HT Df at mmWave, and the low-CTE PI Df at mmWave were not verified.
- No electromigration or current-carrying data were found for liner or annular TSVs or TGVs.

## Q4. What reliability test evidence exists for liner/buffer vias, and what moisture, CAF and hermeticity risks do polymers add?

### Takeaway
Reliability evidence for polymer-lined TSVs is limited to small sample sets. BCB TSVs kept pA-level leakage at 40 V after 40 thermal shocks (−65/+150 °C), and their C-V and I-V even improved after thermal cycling. The Tohoku PI liner was characterized by Raman before and after cycling. No HAST, THB or long HTS data for polymer-lined through-vias were found.

Glass TPVs, without a dedicated polymer liner but sometimes in polymer-laminated glass, pass 1000–4000 cycles of −55/125 °C. Their failure modes are Cu/glass delamination and glass cracking near via corners.

Polymer liners add moisture uptake (PI equilibrium about 2.5–2.7%, parylene-N cracking under HAST), ionic-migration and CAF-like paths, and loss of hermeticity. These are significant for glass, whose selling points include hermeticity and low moisture uptake.

### Cited Findings
- **BCB-lined TSVs:** single-TSV leakage is at pA level at 40 V and did not change significantly after **40 thermal shocks between −65 °C and +150 °C**. — [Microelectron. Reliab. 2013](https://www.sciencedirect.com/science/article/abs/pii/S0026271413000036)
- **BCB-lined TSVs (TCPMT 2014):** after thermal cycling between −65 °C and 150 °C, C-V and I-V properties *improved* (cycle count not retrieved). Electrical behavior was stable up to 125 °C. — [IEEE TCPMT 2014](https://ieeexplore.ieee.org/iel7/5503870/6979775/06945811.pdf)
- **Tohoku VDP-PI liner:** micro-Raman stress was measured before and after thermal cycling, along with an XPS thermal-stability check. The liner was stable at 350 °C. — [IEDM 2014](https://www.researchgate.net/publication/273003298_Highly_Beneficial_Organic_Liner_with_Extremely_Low_Thermal_Stress_for_Fine_Cu-TSV_in_3D-Integration); [VDP PI](https://www.researchgate.net/publication/301383064_Low-Temperature_and_High-Step-Coverage_Polyimide_TSV_Liner_Formation_by_Vapor_Deposition_Polymerization)
- **Parylene-HT:** stable to about 350 °C and pinhole-free. — [ResearchGate 282177249](https://www.researchgate.net/publication/282177249_Fabrication_and_electrical_characterization_of_Parylene-HT_liner_bottom-up_copper_filled_through_silicon_via_TSV)
- **[TGV/glass] Georgia Tech TPVs:**
  - 30 µm TPVs in bare glass: most via chains passed **1000 cycles of −55/125 °C**, and Cu plastic strain increases as the glass gets thinner.
  - 30 µm TPVs in 100 µm glass: stable resistance after **3000 cycles**. The failure modes found were **delamination and glass cracking near via corners**.
  - 60 µm TPVs in 100 µm glass: no visible degradation after **4000 cycles**.
  - The work used FE models of TPVs with several glass and polymer-liner combinations, plus fatigue-life prediction.
  - [Reliability of Cu TPVs in bare glass](https://www.academia.edu/119963275/Reliability_of_Copper_Through_Package_Vias_in_Bare_Glass_Interposers); [30 µm TPV IMAPS 2014](https://meridian.allenpress.com/ism/article-pdf/2014/1/000402/2252418/isom-wa16.pdf); [Springer 2018](https://link.springer.com/article/10.1007/s10854-018-9384-6)
- **[TGV/glass]** Demir et al. (ECTC 2013) covered both thermomechanical and **electrochemical** reliability of fine-pitch TPVs in thin glass. The ECM and CAF-like results were not retrieved. — [ResearchGate 260192671](https://www.researchgate.net/publication/260192671_Thermomechanical_and_electrochemical_reliability_of_fine-pitch_through-package-copper_vias_TPV_in_thin_glass_interposers_and_packages)
- **Moisture and HAST in polymer dielectrics (RDL context):**
  - Parylene-N showed **cracking at several interfaces after high moisture uptake in HAST at 135 °C / 85% RH / 96 h**.
  - For conductor spacing below 2 µm, moisture uptake should be **under about 0.1%** with essentially no ionic content, because moisture enables ionic migration under bias.
  - [Polymers 15:3895 (2023), polymer dielectrics for RDL review](https://www.mdpi.com/2073-4360/15/19/3895)
- **Polyimide films:** equilibrium water uptake of **about 2.5–2.7%**, and electrical insulation drops significantly with humidity. — [Polymers (PMC10892007)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10892007/)
- **Parylene-C:** water-vapor transmission of about 8 g/m²/day, much higher than PI or LCP. — [bioRxiv 2026, LCP moisture barrier](https://www.biorxiv.org/content/10.64898/2026.02.24.707821v1.full)
- **BCB over parylene-C:** blocks parylene defects, makes the permeation path tortuous, and improves the barrier (OFET encapsulation, not vias). — [Beilstein J. Nanotechnol.](https://www.beilstein-journals.org/bjnano/articles/8/155)
- **Fraunhofer:** Cu–Si CTE mismatch, including Cu separation from TSV sidewalls, is a TSV reliability concern. — [Fraunhofer publica](https://publica.fraunhofer.de/bitstreams/a431b70f-22e9-4060-8d88-732a095558cc/download)

### Inferences
- **Weak evidence base for TGV qualification.** The evidence for polymer-lined vias is far below what a TGV interposer qualification needs (for example JEDEC-style TC of 1000 cycles or more, HAST/uHAST, HTS of 1000 h or more, and preconditioning with reflow). Demonstrated data are 40 thermal shocks and an unspecified number of TC cycles on Si test vehicles. The reliability of a polymer liner in glass must be treated as **unproven**.
- **Glass-specific risks a polymer liner introduces** (inference):
  1. Moisture ingress along the polymer annulus, which breaks glass's intrinsic hermeticity. This matters for RF/MEMS/photonics packages that choose glass for hermeticity.
  2. An ionic-migration and CAF-like path along the liner between adjacent TGVs at fine pitch under bias plus humidity. Na/K-containing glasses can add mobile ions, while alkali-free glass reduces this.
  3. Polymer outgassing and Tg or degradation limits during Cu anneal (300–400 °C) and reflow (260 °C). VDP-PI and parylene-HT survive about 350 °C; parylene-C is likely limited to lower temperatures (unverified).
  4. Adhesion of polymer to glass and of Cu to polymer under humidity. This sets the cohesive-zone toughness in Q2 and is not measured in the sources found.
- **Mitigation concepts transferable from the sources:** use a thin inorganic barrier cap (for example SiNx or ALD Al2O3) over or under the polymer to restore the moisture barrier (inferred from the bilayer-barrier result). Prefer low-uptake BCB over PI where moisture matters. Keep the polymer recessed from the glass surface or cap it at the RDL to avoid an exposed annulus.

### Gaps
- No HAST, uHAST, THB, HTS or electromigration data for polymer-, air-gap- or annular-lined TSVs or TGVs were found.
- No CAF or ECM data specific to TGVs were retrieved; the Demir ECTC 2013 results would fill part of this.
- No hermeticity (He leak) data for polymer-lined TGVs were found.
- Cycle counts for the TCPMT 2014 BCB TSV and the Tohoku PI TC tests were not retrieved.
