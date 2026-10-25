# Protein and calorie patterns across MPCE fractiles

Prepared 15 October 2026 from MoSPI/NSO *NSS Report No. 594: Nutritional Intake in India (HCES 2022-23 and 2023-24)*, Table 3.2 (calories) and Table 3.9 (protein).

## Dataset

- `mpce_fractile_nutrition.csv`: 52 rows, one per MPCE population fractile × rural/urban × year; includes per-capita and per-consumer-unit values for protein and calories.
- `mpce_fractile_nutrition_changes.csv`: 26 paired year-to-year comparisons.
- Rebuild with `build_mpce_fractile_dataset.py` using the local official report PDF and Python `pypdf`.

The 12 MPCE groups are 0-5%, 5-10%, 10-20%, …, 90-95%, 95-100%; “All-India” is included as an aggregate row. These are population fractiles formed separately for rural and urban sectors, ranked by MPCE. They are not absolute income bands and do not track the same households between survey years.

## Extraction and consistency checks

The builder parsed all 13 fractile/aggregate rows in both tables for both sectors and both years (52 rows). Protein and calorie All-India cells match the previously validated state/sector dataset for all four year-sector combinations. In both years and sectors, the extracted per-capita calorie and protein estimates are non-decreasing across the published MPCE fractiles, consistent with the report's description.

## Initial findings

| Sector and MPCE fractile | Calories 2022-23 → 2023-24 (kcal/person/day) | Protein 2022-23 → 2023-24 (g/person/day) |
|---|---:|---:|
| Rural, bottom 5% | 1,607 → 1,688 (+81) | 42.4 → 44.3 (+1.9) |
| Rural, top 5% | 3,116 → 2,941 (-175) | 88.5 → 85.8 (-2.7) |
| Urban, bottom 5% | 1,623 → 1,696 (+73) | 44.5 → 46.2 (+1.7) |
| Urban, top 5% | 3,478 → 3,092 (-386) | 94.5 → 85.8 (-8.7) |

The top-to-bottom protein gap narrowed in the published point estimates: rural 46.1 to 41.5 g/person/day (-4.6), urban 50.0 to 39.6 (-10.4). The calorie gap narrowed too: rural 1,509 to 1,253 kcal/day (-256), urban 1,855 to 1,396 (-459). This combines improvement in the lowest MPCE fractile with lower published intake in the highest fractile. The all-India averages alone conceal that contrasting movement across the distribution.

The broad pattern is a strong positive association between MPCE rank and reported protein/calorie intake in each survey year, alongside partial compression of the top-bottom differences from 2022-23 to 2023-24. These are descriptive published estimates. They do not show that changing expenditure caused a change in nutrient intake, or that the same households moved between intake levels. The two survey years are repeated cross-sections.

## Limits and next step

These are aggregate fractile tables from the report; they do not provide household-level observations, covariates, standard errors for each fractile estimate, or sufficient data here for design-based tests of the gap changes. The report's calorie-distribution tables by MPCE group use consumer-unit calorie thresholds; those are a separate outcome and should not be conflated with the average per-capita calorie estimates in Table 3.2.

The next step is to see whether the authorized HCES unit-level data can reproduce the protein/calorie estimates and the MPCE groups. If so, construct design-consistent uncertainty estimates before testing whether the observed gaps changed beyond sampling variation. Until then, present the fractile results as descriptive evidence.

## Source

MoSPI/NSO, [NSS Report No. 594: Nutritional Intake in India (2022-23 & 2023-24)](https://www.mospi.gov.in/sites/default/files/publication_reports/Nutritional_Intake_in_India_L.pdf), Tables 3.2 and 3.9. The report derives nutrient estimates from household food consumption and nutrient content values; these are not direct individual dietary recalls.
