# D. RF & high-impact publications (subagent summary; snippet-based)
## Dk/Df
- NIST Jungwirth et al. APL 124:072902 (2024): fused silica JGS2 Dk 3.87+-0.03, Df<0.005, 0.32-325 GHz on-wafer CPW mTRL.
- Rodriguez-Cano, Lanagan, Perini et al. IEEE TIM 72:6003008 (2023) doi:10.1109/TIM.2023.3256463: crystalline ~1e-4, fused silica <1e-3, multicomponent glasses lossiest up to 115 GHz; tan rises ~linearly with f; NBO/impurity.
- Rodriguez-Cano et al. AIP Advances 2024: phase-separated high-B2O3 borosilicate Dk 3-3.5, Df 5.6e-4; alkali raises to 1-7e-3.
- Chudpooti, Somjit et al. Mater Res Express 8:056201 (2021) THz-TDS.
- IMAPS 2023 table: FS ~3.8/4e-4 @100 GHz; aluminoborosilicate 0.006 @10, 0.004 @35 GHz.
- Eagle XG Dk~5.1, Df 0.002@0.1 GHz -> ~0.013@70 GHz (unverified distributor).
- SCHOTT low-loss borosilicate 2024: Dk 4.0, Df 0.0021 @10 GHz.
- ABF/AGC glass/ABF: Dk 4.72; Df 0.004/0.009/0.012 @23/103/140 GHz (Penn State/GT TCPMT).
- Fraunhofer: eps uncertainty 1-2%, tan 10-25%.
## Loss data
- GT Watanabe et al. TMTT 68(12):5082 (2020) doi:10.1109/TMTT.2020.3022357: 0.095 dB/via @28 GHz (100 um glass), microstrip 0.108 dB/mm.
- IMAPS DPC 2021: line+TGV 30 GHz: quartz 0.23 dB vs EN-A1 0.48 dB.
- Jia et al. IMS 2024: die-embedded glass 140 GHz InP PA, <1.04 dB/interconnect 110-170 GHz; TCPMT 2025 20 um vias EN-A1+ABF 0.2-0.3 dB @140 GHz sim.
- D-band microstrip/SIW on ABF in glass 0.25/0.35 dB/mm; SIW glass 0.5-1 dB/mm.
- Roughness: Xiaolin Yang group RLGC TGV roughness 1.257 um -> 25 nm by controlled LIWE; LIDE fused silica micro-holes Ra 38 nm (arXiv:2510.19100).
- Huray snowball DesignCon 2010; Hammerstad.
- SI/PI: GT Lim group DAC 2023/TCAD 2025 glass interposer; Kim Micromachines 14(10):1880 (2023), 16(1):112 (2025): low-loss glass -> undamped PDN resonances; Kim TEMC 2016.
- Inductors: Kim, Pulugurtha, Sundaram, Tummala, Yun TCPMT 8(4):643 (2018); TPV 3D inductor Q>150 @1 GHz.
## High-impact
- IEDM 2013 TSMC Lai et al. 300 mm ultra-thin glass interposer + high-Q embedded helical inductor.
- ECTC 2010 Sukumaran/Tummala TPV glass interposer; ECTC 2015 KAIST RLGC TGV; ECTC 2025 special session glass core vs RDL (Intel 1:20 TGV, 6 um >15:1, RENA taper <1 deg); ECTC 2026 DNP.
- Microsyst Nanoeng 12:52 (2026) doi:10.1038/s41378-026-01162-y (TGV residual stress & protrusion); 12:46 (2026) doi:10.1038/s41378-026-01160-0 (HT aging, Potts-phase field).
- Science 375:307 (2022) Sun et al. (Qiu) 3D perovskite nanocrystals in glass; Nat Commun 15:8366 (2024) doi:10.1038/s41467-024-52628-4; LSA 2026 doi:10.1038/s41377-026-02253-1 single-pulse amorphization of crystals; LSA 2020 doi:10.1038/s41377-020-0250-y; LSA 2020 doi:10.1038/s41377-020-0298-8; LSA 2023 doi:10.1038/s41377-023-01098-2; Microsyst Nanoeng 2023 doi:10.1038/s41378-023-00511-5 (quartz MEMS fs-assisted); Sci Rep 5:10391 (2015) doi:10.1038/srep10391; Sci Rep 2017 doi:10.1038/srep44327.
- Nat Electron 7:425 (2024) Das Sharma & Mahajan doi:10.1038/s41928-024-01175-3; Nat Electron 2024 doi:10.1038/s41928-024-01126-y; Nat Rev Electr Eng doi:10.1038/s44287-026-00270-1, doi:10.1038/s44287-024-00038-5.
- No Nat Electron/Nat Commun primary paper on TGV/glass interposer as RF platform found -> opportunity.
## Open questions
sub-THz loss physics in multiphase oxides; laser-matter in two-phase solid (phase-contrast etching, roughness floor); roughness-aware conductor loss on curved walls; programmable local crystallization collar; voxel dielectric engineering (quasi-coax TGV); functional substrate; PDN damping phase; alkali migration/CAF; k of nanocrystalline phases.
- IEDM expects: wafer/panel process, via chain stats, TC/HAST, dB/via & dB/mm 110-170 GHz benchmarks. Nature Electron/Commun: mechanism w/ atomic evidence + capability glass can't deliver.
