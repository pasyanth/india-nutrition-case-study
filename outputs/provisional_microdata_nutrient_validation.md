# Provisional HCES microdata nutrient run

Prepared 15 October 2026. This run is a diagnostic and is **not a reproduction** of NSS Report No. 594.

## What was run

- Joined the 2022-23 and 2023-24 Level 03 household records to Level 05 food records, Level 06 Section 7 records, Level 10 CSQ records, Level 02 meal counts, and Level 04 meals served.
- Applied the Report 594 Table 2.2 coefficients, including the prepared rural/urban CPI-adjusted rupee coefficients.
- Applied the 30/7 expansion to Section 6 item codes in Level 05, Section 7 records, and CSQ Section 12 records. A code-specific scaling correction for beverage code 011 was identified after this run; the current output files have not been rerun for that minor code correction.
- Applied the Report 594 meal adjustment: ordinary household nutrients multiplied by B/(A+B), then away-from-home meal nutrients X added. Household size and the FDQ multiplier were used for weighted per-capita estimates.
- Omitted food DDM aggregates 092-095 because their released rows do not preserve the component-food quantities needed to apply the distinct Report 594 factors. 45,345 rows were omitted in 2022-23 and 60,184 in 2023-24.

The processing script is `build_provisional_microdata_nutrients.py`. Household diagnostic estimates are in `provisional_microdata_nutrient_households.csv`, weighted rural/urban summaries in `provisional_microdata_nutrient_summary.csv`, and the benchmark comparison is in `provisional_microdata_nutrient_benchmark_comparison.csv`.

## Benchmark result

The current estimates are materially below the published national rural and urban estimates:

| Year | Sector | Calories difference | Protein difference | Fat difference |
|---|---|---:|---:|---:|
| 2022-23 | Rural | -9.6% | -10.4% | -22.3% |
| 2022-23 | Urban | -13.7% | -13.9% | -25.1% |
| 2023-24 | Rural | -10.0% | -10.9% | -22.7% |
| 2023-24 | Urban | -13.0% | -13.8% | -25.1% |

These gaps are too large to treat the microdata estimates as reproduced. The omitted mixed DDM groups are a known source of downward bias, particularly for fat because edible-oil code 095 is among them. The difference may also reflect other unresolved details in the published estimator; this run does not isolate the contribution of each issue. The code 011 reference-period correction also remains to be applied to the output files.

## Decision and next action

Keep the validated published aggregate datasets as the primary analysis source. Use this microdata run only to document the reproduction attempt; do not report it as an independent estimate or use it for significance tests. The next useful work is to complete the research-question analysis from the published state/sector and MPCE-fractile tables. A defensible microdata replication would require resolving the DDM composition and reconciling the remaining estimator details, then rerunning and benchmarking before any inference.

## Source

MoSPI/NSO, [NSS Report No. 594: Nutritional Intake in India (HCES 2022-23 and 2023-24)](https://www.mospi.gov.in/sites/default/files/publication_reports/Nutritional_Intake_in_India_L.pdf), especially §2.9.8 and Table 2.2.
