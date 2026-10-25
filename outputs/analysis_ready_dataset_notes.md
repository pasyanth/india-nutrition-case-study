# Protein and calorie dataset: validation and first analysis

Prepared 15 October 2026 from the local MoSPI/NSO *NSS Report No. 594: Nutritional Intake in India (HCES 2022-23 and 2023-24)*. The study's main nutrient is protein; calorie intake is the companion outcome. Sugar is excluded from the main analysis.

## Files prepared

- `analysis_ready_nutrition_state_sector.csv`: long panel with one row per State/UT or All-India × rural/urban × survey year (148 rows). Includes published per-capita and per-consumer-unit protein and calorie estimates and a protein-to-calorie ratio.
- `calorie_intake_state_sector_2022_23_2023_24.csv`: calorie estimates transcribed from Summary Statement 1.
- `nutrition_changes_by_state_sector.csv`: paired 2022-23 to 2023-24 descriptive changes for each State/UT or All-India and sector (74 rows).

`protein_to_calorie_ratio_g_per_1000_kcal` is the ratio of the published per-capita protein mean to the published per-capita calorie mean. It is not an average of household- or person-level protein density and must not be interpreted as one.

## Validation

The reproducible builder `build_analysis_ready_datasets.py` extracts Summary Statements 1 and 5 from the local official PDF. All 148 state/sector/year per-capita protein cells in the existing protein CSV match the PDF table. The extracted calorie panel contains 148 expected rows, including the four All-India estimates. The All-India values match the report's displayed figures: calories 2,233 rural / 2,250 urban in 2022-23 and 2,212 / 2,240 in 2023-24; protein 61.9 / 63.2 g in 2022-23 and 61.8 / 63.4 g in 2023-24.

## Descriptive readout

| Sector | Calories, 2022-23 → 2023-24 | Protein, 2022-23 → 2023-24 | Protein/calorie ratio, g per 1,000 kcal |
|---|---:|---:|---:|
| Rural, All-India | 2,233 → 2,212 (-21; -0.9%) | 61.9 → 61.8 (-0.1; -0.2%) | 27.72 → 27.94 |
| Urban, All-India | 2,250 → 2,240 (-10; -0.4%) | 63.2 → 63.4 (+0.2; +0.3%) | 28.09 → 28.30 |

Across the 36 State/UTs (excluding the All-India row), calorie estimates fell in 15 rural and 15 urban comparisons. Protein estimates fell in 10 rural and 10 urban comparisons. Both fell in 10 rural and 9 urban comparisons. Point-estimate changes varied considerably: rural calorie change ranged from -125 kcal/day in Karnataka to +509 in Sikkim; urban ranged from -85 in West Bengal to +423 in Sikkim. These are leads for follow-up, not statistically established differences.

The national point estimates suggest that protein was nearly stable while calories edged down between the two rounds. The ratio of the national means rose slightly, but the ratio uses rounded aggregate estimates and does not demonstrate that individual diets became more protein-dense. State-level extrema should be interpreted cautiously for the same reason.

## Scope and limitations

- This is an analysis-ready **published aggregate** dataset, not a household-level or individual-level dataset. MoSPI estimates are derived from household food consumption and nutrient values; they do not directly measure each person's dietary intake.
- The current panel has only two adjacent survey years. It supports state/sector description and change comparisons, not a robust long-run trend or causal explanation.
- The report presents rounded point estimates. The changes and rankings above are not significance-tested. Do not describe them as statistically significant.
- Consumer-unit estimates are kept alongside per-capita estimates as published. Use per-capita values for the primary comparisons unless the research question explicitly calls for consumer-unit weighting.
- Do not infer protein adequacy from average grams alone; this would require a defensible requirement benchmark and population-level distribution, neither of which is supplied by this aggregate panel.

## Next analysis stage

The published MPCE-fractile protein/calorie dataset is now prepared and described in `mpce_fractile_analysis_notes.md`. The next gate is to reproduce key results from authorized HCES microdata and determine whether the public unit-level files support comparable MPCE groups and design-based uncertainty (weights, strata and PSUs). Only after that should we make inferential claims. Sugar remains outside the primary analysis.

## Source

MoSPI/NSO, [NSS Report No. 594: Nutritional Intake in India (2022-23 & 2023-24)](https://www.mospi.gov.in/sites/default/files/publication_reports/Nutritional_Intake_in_India_L.pdf), Summary Statements 1 and 5. Methodological note: nutrient estimates are based on household food consumption and nutrient content values; they are not direct individual-intake measurements.
