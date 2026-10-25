# Exploratory tests on published aggregate tables

**Status: exploratory diagnostics only.** These calculations use rounded State/UT and MPCE-fractile point estimates from NSS Report No. 594. They do not account for HCES sampling weights, strata, PSUs, or the sampling error of the published estimates. Therefore the p-values below are not design-based evidence about changes in India's population. They describe how the published aggregate cells behave under simple statistical models.

## Methods

1. **State change tests:** One-sample t-tests of the unweighted mean of the 36 State/UT point-estimate changes against zero, separately by sector and outcome. The null is that the average displayed State/UT change is zero. Holm adjustment is applied across the four tests. This is an exchangeable-state diagnostic; it is not the national, population-weighted change.
2. **MPCE gradient:** Spearman rank correlation between the ordered 12 MPCE fractiles and each published mean, separately by year, sector, and nutrient. All 12 values are strictly increasing in every comparison (rho = 1). The two-sided exact permutation p-value is 2/12!; Holm adjustment is across the eight correlations. Because the data are summaries for deliberately ordered population groups, this p-value is only a pattern diagnostic and must not be presented as survey inference.
3. **State co-movement:** Pearson correlation between State/UT changes in calories and protein, separately by sector. P-values use the usual t approximation and Holm adjustment across the two sector tests. This measures association among displayed state changes, not a causal relationship.

## Results

### Average change across State/UT point estimates

| Sector | Outcome | Mean change across 36 State/UTs | Naive SE | t (df=35) | Raw p | Holm-adjusted p |
|---|---|---:|---:|---:|---:|---:|
| Rural | Calories, kcal/person/day | +50.25 | 19.79 | 2.54 | 0.0157 | 0.0314 |
| Rural | Protein, g/person/day | +1.57 | 0.43 | 3.68 | 0.00077 | 0.0031 |
| Urban | Calories, kcal/person/day | +36.31 | 15.98 | 2.27 | 0.0293 | 0.0314 |
| Urban | Protein, g/person/day | +1.80 | 0.61 | 2.98 | 0.00528 | 0.0158 |

The equal-weight average across states is positive for both nutrients and sectors, even though the published All-India estimate shows slight calorie declines and near-zero protein changes. This is not a contradiction: an unweighted average of state changes gives small and large states equal weight, while the national estimate reflects population weighting and the report's estimator. The t-test does not establish that national intake increased.

### MPCE gradient

For calories and protein, Spearman rho is **+1.000** for rural and urban fractiles in both 2022-23 and 2023-24. Each outcome rises strictly across the 12 ordered MPCE groups in the published tables. The group-level exact permutation p-value is 4.18 × 10⁻⁹; Holm-adjusted p across the eight comparisons is 3.34 × 10⁻⁸. Treat the perfect ordering and rho as the meaningful descriptive result. The very small p-value is not evidence of population-level statistical significance because uncertainty and the survey design are unavailable in these aggregate tables.

### Calorie–protein co-movement across states

| Sector | Pearson r between state calorie and protein changes | Raw p | Holm-adjusted p |
|---|---:|---:|---:|
| Rural | 0.934 | 8.80 × 10⁻¹⁷ | 1.76 × 10⁻¹⁶ |
| Urban | 0.622 | 5.14 × 10⁻⁵ | 5.14 × 10⁻⁵ |

States with larger calorie increases tended also to show larger protein increases in their displayed changes. This is an ecological association among state-level estimates. It does not show that households whose calories rose also had protein increases, and it does not imply one nutrient caused the other.

## Interpretation and next method gate

These tests add three exploratory observations: (a) the equal-weight state average change is positive despite small national declines/flatness; (b) both nutrient means increase monotonically across every published MPCE gradient; and (c) state calorie and protein changes are positively associated. The first and third patterns are ecological and sensitive to state weighting and influential states. The MPCE gradient is already directly visible in the table, so its p-value adds little beyond a compact monotonicity summary.

Do not report these as statistically significant changes in India's intake. To make population-level tests, first validate the microdata estimator against Report 594, resolve mixed DDM codes 092–095 and the remaining scaling/coding details, and then estimate variances using the correct survey weights, strata, and PSUs. The current provisional microdata does not meet that validation gate.

## Reproducibility

- Results: `exploratory_aggregate_test_results.csv`
- Script: `run_exploratory_aggregate_tests.py` (Python standard library only)
- Input tables: `nutrition_changes_by_state_sector.csv`, `mpce_fractile_nutrition.csv`
- Official source: MoSPI/NSO, [NSS Report No. 594: Nutritional Intake in India](https://www.mospi.gov.in/sites/default/files/publication_reports/Nutritional_Intake_in_India_L.pdf), Summary Statements 1 and 5; Tables 3.2 and 3.9.
