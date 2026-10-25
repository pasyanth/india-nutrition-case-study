# India nutrition trends: published aggregate analysis

## Project objective

Assess how published household-consumption-based estimates of protein and calories changed across HCES 2022-23 and 2023-24, and whether national averages conceal different rural/urban, state, or MPCE-fractile patterns. Protein is the primary outcome; calories are the companion outcome. Sugar-commodity quantities remain optional exploratory material and are not part of the primary findings.

## Data and interpretation

The primary analysis uses the validated State/UT-by-sector entries in NSS Report No. 594 Summary Statements 1 and 5 and its MPCE-fractile tables. These are published aggregate estimates derived from household food consumption and nutrient conversion factors, not direct individual dietary measurements. Changes are descriptive comparisons of two adjacent cross-sectional survey rounds; the same households are not followed over time.

The local state/sector dataset has 148 observations (37 State/UT and All-India labels × two sectors × two years). The MPCE dataset has 52 observations (13 published groups including All-India × two sectors × two years). Reported values are rounded. Calculated differences and percentages use those displayed values. The tables do not supply the uncertainty needed here to test these changes, so no p-values or claims of statistical significance are reported.

## Findings

### National protein and calorie estimates are nearly stable

| Sector | Calories, 2022-23 → 2023-24 | Protein, 2022-23 → 2023-24 |
|---|---:|---:|
| Rural | 2,233 → 2,212 kcal/person/day (-21; -0.9%) | 61.9 → 61.8 g/person/day (-0.1; -0.2%) |
| Urban | 2,250 → 2,240 kcal/person/day (-10; -0.4%) | 63.2 → 63.4 g/person/day (+0.2; +0.3%) |

At the national level, protein is essentially unchanged, while calories edge down slightly. This is a short, two-round comparison, not evidence of a long-run trend.

The ratio of national mean protein to national mean calories rose from 27.72 to 27.94 g per 1,000 kcal in rural India and from 28.09 to 28.30 in urban India. This is a ratio of rounded aggregate means. It is not the average household or person-level protein density and does not establish a meaningful dietary-composition shift.

### Rural–urban gaps vary by nutrient

The urban-minus-rural calorie gap widened from 17 to 28 kcal/person/day. The protein gap widened from 1.3 to 1.6 g/person/day. The fat gap narrowed from 10.8 to 9.4 g/person/day as published fat estimates moved in opposite directions: rural fat rose from 59.7 to 60.4 g/person/day, while urban fat fell from 70.5 to 69.8.

The direction is not uniform across nutrients. The point estimates do not establish whether any gap changed beyond sampling variation.

### State-level changes are heterogeneous

Among the 36 State/UT entries (excluding All-India), calorie estimates fell in 15 rural and 15 urban comparisons. Protein estimates fell in 10 rural and 10 urban comparisons. Both calorie and protein fell in 10 rural comparisons and 9 urban comparisons. The largest displayed calorie increase was in Sikkim in both sectors (+509 rural; +423 urban kcal/day), while the largest decrease was Karnataka rural (-125) and West Bengal urban (-85). These extremes warrant source-table/context checks and uncertainty estimates before interpretation; they are not established outliers or statistically verified changes.

### Published MPCE fractiles show a steeper gradient and contrasting movements

In both survey years and sectors, published average per-capita protein and calories rise across MPCE population fractiles. The bottom and top 5% comparisons show different directions between rounds:

| Sector / fractile | Calories, 2022-23 → 2023-24 | Protein, 2022-23 → 2023-24 |
|---|---:|---:|
| Rural, bottom 5% | 1,607 → 1,688 (+81 kcal/day) | 42.4 → 44.3 (+1.9 g/day) |
| Rural, top 5% | 3,116 → 2,941 (-175 kcal/day) | 88.5 → 85.8 (-2.7 g/day) |
| Urban, bottom 5% | 1,623 → 1,696 (+73 kcal/day) | 44.5 → 46.2 (+1.7 g/day) |
| Urban, top 5% | 3,478 → 3,092 (-386 kcal/day) | 94.5 → 85.8 (-8.7 g/day) |

The top-to-bottom protein gap narrowed from 46.1 to 41.5 g/day in rural areas and from 50.0 to 39.6 g/day in urban areas. The calorie gap narrowed from 1,509 to 1,253 kcal/day rural and from 1,855 to 1,396 urban. This pattern combines higher estimates for the bottom 5% with lower estimates for the top 5%; it is not evidence that the same households changed their diets, because the fractiles are separately ranked in each round.

## What these data cannot establish

- They do not directly measure each individual's intake or food absorption, and they do not establish nutritional adequacy for individuals.
- Two adjacent rounds cannot support a strong long-run trend or a causal explanation for dietary changes.
- Published rounded point estimates without corresponding uncertainty do not support significance tests for the displayed changes or state rankings.
- The aggregate MPCE tables do not permit household-level nonlinear modeling, within-group inequality metrics, or design-consistent confidence intervals.
- The provisional unit-level reconstruction is not a substitute: it misses several published benchmarks and still has unresolved DDM composition and coding details. Its numbers are diagnostic only.

## Analysis decision

Use the validated published aggregate tables for the case-study findings above. Keep all changes explicitly descriptive. Do not make claims of statistical significance, adequacy, causation, or individual intake. Treat the microdata reproduction as an unresolved validation track, not as the source of the main estimates. Sugar is not required to answer this protein-and-calorie-centered analysis; the separate sugar-commodity dataset measures only selected sugar commodities, not total dietary or added sugar.

## Figures

![National protein and calorie estimates by survey round](figures/national-protein-calories.png)

![Published changes in bottom and top MPCE fractiles](figures/mpce-bottom-top-nutrients.png)

![State and sector changes in calorie and protein estimates](figures/state-calorie-protein-changes.png)

## Reproducible source files

- `analysis_ready_nutrition_state_sector.csv`
- `nutrition_changes_by_state_sector.csv`
- `mpce_fractile_nutrition.csv`
- `mpce_fractile_nutrition_changes.csv`
- `analysis_ready_dataset_notes.md`
- `mpce_fractile_analysis_notes.md`

## Source

MoSPI/NSO, [NSS Report No. 594: Nutritional Intake in India (HCES 2022-23 and 2023-24)](https://www.mospi.gov.in/sites/default/files/publication_reports/Nutritional_Intake_in_India_L.pdf), particularly Summary Statements 1 and 5 and Tables 3.2 and 3.9.
