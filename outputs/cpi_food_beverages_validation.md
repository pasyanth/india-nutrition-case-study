# MoSPI food-and-beverages CPI: validation and rupee-factor adjustment

Prepared 15 October 2026. The source file in Downloads was inspected but left unchanged.

## Outcome

The uploaded CSV has the correct variables for this task (month, rural, urban, combined), but its 24 values for the required survey months (August 2022–July 2024) do not match MoSPI's official Group 1, “Food and beverages,” indices. Its December 2024 values (203.9 rural, 209.4 urban, 205.9 combined) do match the official provisional figures. Use `cpi_food_beverages_official_extracted.csv` as the project series.

That file contains the continuous 29-month series August 2022–December 2024, the release status for each observation, and the source PDF or official source URL. All 24 months used in the two survey-period averages are final. December 2024 is provisional, as MoSPI labels it.

## Survey-period CPI averages

| Survey period | Months | Rural average | Urban average | Combined average |
|---|---:|---:|---:|---:|
| August 2022–July 2023 | 12 | 177.091667 | 183.141667 | 179.316667 |
| August 2023–July 2024 | 12 | 190.308333 | 197.175000 | 192.841667 |

The December 2024 reference indices are 203.9 rural and 209.4 urban (provisional). The project report states that Table 2.2's rupee-to-nutrient factors are based on December 2024 prices and should be adjusted using average CPI during each survey period. For this calculation, the period-specific rupee factor is the December 2024 factor multiplied by `December 2024 sector CPI / 12-month survey-period average sector CPI`. This raises the per-rupee nutrient factor for earlier, lower-price periods.

| Survey period | Rural adjustment ratio | Urban adjustment ratio |
|---|---:|---:|
| August 2022–July 2023 | 1.151381111 | 1.143377167 |
| August 2023–July 2024 | 1.071419188 | 1.062000761 |

The factor values inherit the one-decimal rounding of MoSPI's published monthly index. Ratios are therefore precise calculations from rounded CPI observations, not higher-precision CPI estimates.

## Files prepared

- `cpi_food_beverages_official_extracted.csv`: official monthly values, status, and per-month source.
- `cpi_period_averages_and_deflators.csv`: the two 12-month averages, December 2024 reference indices, and calculated ratios.
- `cpi_adjusted_rupee_conversion_factors.csv`: 36 rural/urban rupee-based conversion rows adjusted for both periods (72 rows total). Quantity-based factors remain unchanged.
- `build_cpi_index_from_pdfs.py` and `build_cpi_adjusted_rupee_factors.py`: reproducible extraction and adjustment scripts. Source releases are retained in `cpi_sources/`.

## Remaining work before household-level nutrient estimates

The CPI input stage is complete. The adjustment table can now feed the household estimator, but it does not itself reproduce nutrient intake. Next, reconcile the food-item codes and subtotal rows against the HCES schedules, then implement the report's quantity/value, recall-period, meal-adjustment, household-size, and multiplier rules. Validate the resulting rural/urban estimates against NSS Report 594 before interpreting any microdata results.

## Sources

- MoSPI/NSO, [NSS Report No. 594: Nutritional Intake in India](https://www.mospi.gov.in/sites/default/files/publication_reports/Nutritional_Intake_in_India_L.pdf), Chapter 2, CPI adjustment instruction following Table 2.2.
- MoSPI, [September 2022 CPI release (October 2022 final/provisional table)](https://mospi.gov.in/sites/default/files/press_release/CPI%20Press%20Release%20October%202022.pdf).
- MoSPI, [January 2023 final CPI release](https://mospi.gov.in/sites/default/files/press_release/CPI_PR_13mar23.pdf), [June 2023 final CPI release](https://mospi.gov.in/sites/default/files/press_release/CPI_PR_14aug23.pdf), [November 2023 final CPI release](https://mospi.gov.in/sites/default/files/press_release/CPI_PR_12Jan24.pdf), [January 2024 final CPI release](https://mospi.gov.in/sites/default/files/press_release/CPI_PR_12Mar24.pdf), and [May 2024 final CPI release](https://mospi.gov.in/sites/default/files/press_release/CPI_PR_12july24.pdf).
- MoSPI, [December 2024 CPI release](https://cpi.mospi.gov.in/PDFile/Press/PR%20December%202024.pdf), which publishes December 2024 provisionally.
