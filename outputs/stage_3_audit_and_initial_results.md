# HCES dataset audit and initial results

Audit run: 15 October 2026. Raw files were read without modification.

## Scope and sources

The primary source is MoSPI/NSO, *NSS Report No. 594: Nutritional Intake in India (HCES 2022-23 and 2023-24)*. Its estimates use household food-consumption data and food nutrient values; they are not direct individual dietary measurements. The local CSV `protein_intake_state_sector_2022_23_2023_24.csv` reproduces the report's State/UT x sector entries for Summary Statement 5.

Local unit-level deliveries were found for both years, each with 15 CSV levels and a layout workbook. The 2022-23 level files use abbreviated field names; the 2023-24 files use descriptive field names. They must be mapped through the layout workbooks before harmonization.

## File audit

| Year | File | Rows | Unique household keys | Audit note |
|---|---|---:|---:|---|
| 2022-23 | Level 01 (household identifiers) | 261,746 | 261,746 | No repeated base household keys |
| 2022-23 | Level 03 (household particulars) | 261,746 | 261,746 | No repeated base household keys |
| 2022-23 | Level 05 (food-item consumption) | 12,056,839 | 261,082 | Repeated household keys are expected: one row per item; 664 sampled household keys have no Level 05 row |
| 2022-23 | Level 15 (Section 1.1/A2/B2/C2) | 1,046,984 | 261,746 | Exactly four rows per household key: 11, A2, B2, C2 |
| 2023-24 | Level 01 (household identifiers) | 261,953 | 261,953 | No repeated base household keys |
| 2023-24 | Level 03 (household particulars) | 261,953 | 261,953 | No repeated base household keys |
| 2023-24 | Level 05 (food-item consumption) | 12,754,437 | 261,245 | Repeated household keys are expected: one row per item; 708 sampled household keys have no Level 05 row |
| 2023-24 | Level 15 (Section 1.1/A2/B2/C2) | 1,047,812 | 261,953 | Exactly four rows per household key: 11, A2, B2, C2 |

The household identity fields occupy the same positions in both deliveries, but their names differ. In 2022-23 they include `b1q1pt7`, `b1q1pt10`, `b1q1pt11`, and `b1q1pt12`; in 2023-24 they are `Sample_SU_No`, `Sample_Sub_Division_No`, `Second_Stage_Stratum_No`, and `Sample_Household_No`. Join only after normalizing the complete household identifier from the layout, not on state or FSU alone.

The item-level food files have 164 observed item codes in 2022-23 and 162 in 2023-24. This is a signal to verify item-code coverage and units against the schedules before comparing item quantities. Quantity is not safely additive across different foods until units and item definitions are checked.

Level 15 carries household expenditure and household size in A2, B2, and C2 rows. Those rows repeat per household, so they cannot be treated as an MPCE field directly. The sugar estimates below use FDQ household size and the FDQ multiplier from the item-level food records; MPCE has not been reconstructed.

MoSPI's *Survey Methodology & Estimation Procedure* resolves that issue for future expenditure analysis: MPCE is based on households with all three questionnaires; total monthly expenditure is `E1 + (E2/P2)*P1 + (E3/P3)*P1`, then divided by FDQ household size `P1`. The third-visit multiplier is used for MPCE estimates. Do not use just one A2/B2/C2 expenditure value as the full MPCE.

## Initial, report-based comparison

These are descriptive comparisons of MoSPI's published all-India per-capita daily estimates, in the units shown by the report. Percentage changes are calculated from the displayed rounded values. The report tables do not provide standard errors here, so these are not significance tests.

| Outcome | Sector | 2022-23 | 2023-24 | Change | Relative change |
|---|---|---:|---:|---:|---:|
| Calories (kcal/person/day) | Rural | 2,233 | 2,212 | -21 | -0.9% |
| Calories (kcal/person/day) | Urban | 2,250 | 2,240 | -10 | -0.4% |
| Protein (g/person/day) | Rural | 61.9 | 61.8 | -0.1 | -0.2% |
| Protein (g/person/day) | Urban | 63.2 | 63.4 | +0.2 | +0.3% |
| Fat (g/person/day) | Rural | 59.7 | 60.4 | +0.7 | +1.2% |
| Fat (g/person/day) | Urban | 70.5 | 69.8 | -0.7 | -1.0% |

At this aggregate level, calories and protein are nearly flat between these adjacent survey years, while fat moves slightly in opposite directions in rural and urban estimates. This is a descriptive starting point, not a long-run trend or evidence of a causal effect. The rural-urban per-capita gap also differs by nutrient: calories (urban minus rural) move from 17 to 28 kcal/day; protein from 1.3 to 1.6 g/day; fat from 10.8 to 9.4 g/day.

MoSPI's own historical tables also show a longer, report-based comparison for 2009-10, 2011-12, 2022-23 and 2023-24. Between 2009-10 and 2023-24, its displayed all-India per-capita calorie estimates rise 3.0% rural (2,147 to 2,212 kcal/day) and 5.5% urban (2,123 to 2,240). Protein rises 4.2% rural (59.3 to 61.8 g/day) and 7.8% urban (58.8 to 63.4). Fat rises more: 40.1% rural (43.1 to 60.4 g/day) and 31.7% urban (53.0 to 69.8). This suggests a stronger change in reported fat quantity than in calories, but the gap between survey rounds and design/method changes mean these are broad historical comparisons, not a tightly controlled continuous series.

## Sugar-commodity dataset and first estimates

The HCES food questionnaire identifies sugar codes 074 (free sugar from PDS), 171 (sugar-PDS at subsidized price) and 172 (sugar from other sources); each quantity is in kg for the last 30 days. Codes 173 (jaggery/gur), 174 (candy/misri) and 175 (honey) are kept as separate quantities. The sugar measure sums only 074+171+172. It excludes sugars in sweets, beverages and other foods, so it is not total dietary sugar or total added sugar.

The reproducible script `build_sugar_dataset.py` maps the correct quantity column by year (the 2022-23 abbreviated column is `b5pt1q5`; `b5pt1q7` is the source code), joins food records to FDQ household size using the household ID, includes households with no recorded sugar as zero when they have other FDQ item records, and applies the FDQ multiplier. The weighted per-person daily estimate is the weighted total sugar quantity divided by weighted household population and 30 days. The derived household files retain the household key plus FSU, stratum and related design fields for later uncertainty estimation. The dataset excludes 664 households in 2022-23 and 708 in 2023-24 with no Level 05 item rows. No food keys were unmatched, and no invalid target quantities or nonpositive sizes/weights were found.

| Year | Sector | Matched households | Weighted sugar commodities (g/person/day) | Weighted household quantity (kg/30 days) |
|---|---|---:|---:|---:|
| 2022-23 | Rural | 154,750 | 21.77 | 2.923 |
| 2022-23 | Urban | 106,332 | 23.54 | 2.723 |
| 2022-23 | All India | 261,082 | 22.27 | 2.860 |
| 2023-24 | Rural | 154,114 | 21.34 | 2.830 |
| 2023-24 | Urban | 107,131 | 22.65 | 2.534 |
| 2023-24 | All India | 261,245 | 21.73 | 2.731 |

The weighted all-India sugar-commodity estimate is 0.54 g/person/day lower in 2023-24 (about 2.4%); the rural estimate is lower by 0.43 g/day and the urban estimate by 0.88 g/day. These are point estimates only. Design-based confidence intervals and significance tests are not yet computed. The unit-level data contains a small number of extreme household quantities: 11 households in 2022-23 and 5 in 2023-24 exceed 500 g per person per day. Removing those flagged records changes the all-India point estimates only to 22.22 and 21.72 g/day respectively; they are retained in the main estimate pending record-level investigation.

Across the 36 State/UT codes, exploratory point-estimate changes vary in direction: for rural households the largest estimated decrease is Delhi (-6.22 g/person/day) and the largest increase is Andaman & Nicobar Islands (+4.61); for urban households the largest decrease is Lakshadweep (-5.88) and largest increase Chandigarh (+5.06). These are leads for survey-design uncertainty checks, not findings to present as established differences yet.

## Scope update and next analysis gates

The project now prioritizes protein as the primary nutrient and calories as the companion outcome. The sugar-commodity dataset and initial sugar results above are optional exploratory work and are excluded from the primary analysis. The follow-up `analysis_ready_dataset_notes.md` records the protein/calorie validation and files prepared from MoSPI Summary Statements 1 and 5.

1. Reproduce selected published state/sector and MPCE-fractile estimates from authorized HCES microdata, including a consistent MPCE construction.
2. Determine whether the delivered microdata and documentation support design-based uncertainty calculations for the derived nutrient outcomes (weights, strata and PSUs).
3. Only make inferential claims after the design-based uncertainty checks; otherwise present state/sector/fractile comparisons as descriptive.

The microdata input audit is now recorded in `microdata_reproduction_plan.md`. It parsed the report's full nutrient conversion table and mapped food-record coverage across both years. No microdata nutrient estimates have been labeled as reproduced yet: rupee-based conversions require matching official rural/urban food CPI adjustments, and unmatched item/subtotal codes and the meal adjustment still need reconciliation.

## Provenance

- MoSPI/NSO, *NSS Report No. 594: Nutritional Intake in India (2022-23 & 2023-24)*, especially Summary Statements 1, 5, 6-8 and report methodology: https://www.mospi.gov.in/sites/default/files/publication_reports/Nutritional_Intake_in_India_L.pdf
- MoSPI/NSO, *Survey Methodology & Estimation Procedure: HCES 2023-24*, especially Sections 3.5, 3.7 and 4: https://www.mospi.gov.in/sites/default/files/publication_reports/Survey_methodology_and_Estimation_Procedure.pdf
- Local source files: `protein_intake_state_sector_2022_23_2023_24.csv`; `Layout_HCES_2022_23_1.xlsx`; `Layout_HCES 2023-24.xlsx`; the 2022-23 and 2023-24 HCES level CSV folders.
- Item definitions and units: `HCES2022_Vol_II_1.pdf` and `HCES2023-24_Vol_II-2.pdf`; state labels from `tabulation_state_code_2.xlsx`.
