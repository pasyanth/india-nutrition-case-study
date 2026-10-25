# HCES microdata reproduction: next-stage audit

Prepared 15 October 2026 from the local HCES unit-level deliveries and MoSPI/NSO *NSS Report No. 594: Nutritional Intake in India*.

## Decision

The unit-level data contain food quantity/value records for a household-level reproduction attempt. The official CPI input is assembled and rupee-based factors are adjusted to the two survey periods. A provisional calculation has been run, but it does not reproduce the report closely enough to be used as an analysis estimate. Four broad food DDM codes do not map uniquely to distinct factors in Table 2.2, and other estimator details remain to be reconciled.

## Completed in this stage

- `audit_microdata_nutrient_inputs.py` extracts all 176 entries of Report 594 Table 2.2 and scans the food records for observed codes, quantity availability, and value availability.
- `nutrient_conversion_table_report594.csv` is the extracted factor table (176 rows; 158 distinct item codes because some rupee-based factors have separate rural/urban rows).
- `microdata_nutrient_input_audit.csv` is the corrected coverage audit. It uses Level 10 CSQ quantity/value fields `b12pt1q5`/`b12pt1q6` for 2022-23 and the corresponding descriptive fields for 2023-24.
- The official 2012-base CPI Group 1 food-and-beverages series is assembled for Aug 2022-Dec 2024 in `cpi_food_beverages_official_extracted.csv`. All 24 required survey-period months are final; Dec 2024 is provisional. CPI averages and the resulting rural/urban adjustments to rupee-based Table 2.2 coefficients are in `cpi_period_averages_and_deflators.csv` and `cpi_adjusted_rupee_conversion_factors.csv`. See `cpi_food_beverages_validation.md` for provenance and validation.
- `nutrient_code_crosswalk.csv` classifies every observed unmatched code. Coarse-grain source subcodes map to Report 594 factors 001, 070 or 002; subtotal codes and non-food CSQ items are explicitly excluded to prevent double counting or adding non-food consumption. Four food DDM aggregates (092–095) remain unresolved because each combines food types with different conversion factors and the available item field does not identify a unique Table 2.2 factor.
- The Level 05 CSV schemas were checked directly: both survey years provide one `Item_Code` field (2022-23: `b5pt1q2`), quantity, value, source and household identifiers, but no finer food-type field for codes 092–095. The downloaded files therefore do not retain the sub-item split needed to assign their distinct Table 2.2 factors. This closes the local-file search for that detail; it is not a request for you to obtain another dataset.

| File group | 2022-23 rows | 2023-24 rows | Conversion-table match |
|---|---:|---:|---:|
| FDQ, Level 05 (Sections 5 and 6; mixed reference periods) | 12,056,839 | 12,754,437 | 132 / 164 and 132 / 162 observed codes |
| FDQ, Section 7 (7-day items) | 1,637,576 | 1,757,264 | 19 / 21 observed codes |
| CSQ, Section 12 (7-day items) | 762,523 | 829,310 | 7 / 20 observed codes |

The crosswalk resolves the coarse-grain subcodes and identifies subtotals/non-food rows. The remaining issue is codes 092–095: they represent milk-product, fresh-fruit, dry-fruit and edible-oil aggregates whose component foods have distinct nutrient factors. Do not assign one factor to these mixed groups without item-level composition.

## Required estimator logic

1. Normalize the household key across all questionnaire levels and join FDQ/CSQ quantities, household particulars, meal counts and multipliers.
2. Apply Report 594 Table 2.2 factors. Level 05 combines 30-day Section 5 items with 7-day Section 6 items; scale Section 6 item codes by 30/7. Also scale 7-day Section 7 and CSQ Section 12 records by 30/7. Exclude the report-specified meal codes and CSQ items from the ordinary food sum.
3. For rupee-denominated Table 2.2 factors, use the prepared rural/urban period-specific coefficients. The report bases them on December 2024 prices and instructs adjustment with average CPI for Aug 2022-Jul 2023 and Aug 2023-Jul 2024; the calculation and source values are recorded separately.
4. Reconstruct the meals-served/consumed adjustment described in Report 594 §2.9.8 using Level 04 meals served to non-household members and Level 02 meals consumed at home/away. Then calculate household nutrient totals and per-capita daily estimates using FDQ household size and the correct survey multiplier.
5. Compare reconstructed rural, urban and all-India estimates to Summary Statement 1 / 5. Investigate deviations before treating microdata outputs as replicated. Only after that, reproduce MPCE fractiles and uncertainty estimates using the survey design variables.

## Open checks before a comparison is valid

- CPI input and adjustment stage is complete. Use the final rural/urban Group 1 food-and-beverages values for the two 12-month survey periods and the December 2024 provisional reference; do not substitute general CPI or CFPI. The downloaded candidate CSV mismatched all 24 survey-month rows, so it is not used.
- The released Level 05 files do not contain sub-item information behind food DDM codes 092–095. Keep published-aggregate analyses primary. Any microdata reproduction should first omit these four codes transparently, then compare against the report and label the result incomplete; a separate sensitivity analysis can bound their effect only if defensible lower/upper nutrient factors are available.
- Map away-meal source categories and at-home meal counts consistently across both survey years; verify Level 02 and Level 04 joins and the annual multiplier definitions.
- Account for sampled households with no Level 05 rows. Current file audit finds 664 such households in 2022-23 and 708 in 2023-24; determine from MoSPI's prescribed missing-item treatment whether they are valid zero-consumption cases or require another file/adjustment.
- Confirm design variables and MPCE fractile formation against the published methodology before computing standard errors or tests.

- The first provisional computation incorrectly treated all Level 05 records as 30-day. It is superseded and must not be used. The rerun applies the questionnaire's 7-day reference period to Section 6 item codes before making any benchmark comparison.

## Current limit

The provisional microdata run is documented in `provisional_microdata_nutrient_validation.md`. It falls 9.6–13.7% below published calorie estimates, 10.4–13.9% below published protein, and 22.3–25.1% below published fat across year-sector combinations. It omits DDM codes 092–095 and requires a code 011 period-scaling correction; it is not a reproduced estimator. The validated published tables remain the valid primary analysis dataset for descriptive findings. Do not use the provisional household-level estimates for substantive conclusions or significance tests.

## Sources

- MoSPI/NSO, [NSS Report No. 594: Nutritional Intake in India (HCES 2022-23 and 2023-24)](https://www.mospi.gov.in/sites/default/files/publication_reports/Nutritional_Intake_in_India_L.pdf), especially Table 2.2 and §2.9.8.
- MoSPI, [CPI API User Manual](https://cpi.mospi.gov.in/PDFile/Api%20User%20Manual%20-%20CPI.pdf). The API manual describes authenticated access for larger queries; this audit does not create an account or token.
- Reserve Bank of India, [Database on Indian Economy, Table 165: Consumer Price Index - Monthly](https://dbie.rbi.org.in/DBIE/dbie.rbi?site=statistics), consulted to assess public CPI coverage.
