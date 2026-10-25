# Research question synthesis: India nutrition trends

**Project title:** “Analyze trends in calorie, sugar, or protein intake using public datasets and statistical tools.”

**Evidence base:** MoSPI/NSO NSS Report No. 594, HCES 2022-23 and 2023-24, using validated published state/sector and MPCE-fractile tables. These are household-consumption-derived nutrient estimates, not direct measurements of each person's intake. Changes below are descriptive because the published aggregate tables do not provide the uncertainty estimates needed for significance testing.

## Answers to the core questions

| Research question | What the available data says | Answerability |
|---|---|---|
| 1. How did calories and protein change? | National rural calories fell from 2,233 to 2,212 kcal/person/day (-0.9%); urban fell from 2,250 to 2,240 (-0.4%). Protein was almost unchanged: rural 61.9 to 61.8 g/person/day (-0.2%); urban 63.2 to 63.4 (+0.3%). | Answered descriptively for the two rounds. Not a long-run trend. Sugar is not part of this primary analysis. |
| 2. How do patterns differ by residence, state, and expenditure group? | The state/sector panel shows heterogeneous changes. Published MPCE fractiles show higher average calories and protein at higher MPCE ranks in both rounds and sectors. | Answered descriptively. No design-based uncertainty or significance claims. |
| 3. Is higher expenditure associated with better dietary composition? | Protein and calorie means rise across MPCE fractiles, but these tables do not supply enough detail to test whether protein density or broader dietary quality improves, plateaus, or changes nonlinearly with expenditure. | Partly answered: higher MPCE rank coincides with higher nutrient quantities. Composition and nonlinear association require validated household-level data and an appropriate model. |
| 4. Do calories and protein move proportionally? | At national means, both declined slightly in rural areas; in urban areas calories declined slightly while protein rose slightly. The ratio of aggregate means rose modestly in both sectors. | Descriptive comparison only. The ratio is not the mean household/person protein density. |
| 5. Are rural–urban gaps changing? | Urban-minus-rural calorie gap widened from 17 to 28 kcal/day; protein gap widened from 1.3 to 1.6 g/day; fat gap narrowed from 10.8 to 9.4 g/day. | Direction of displayed point estimates answered; whether gaps changed beyond sampling variation is unknown. |
| 6. Did food-group composition change? | The current primary analysis uses nutrient summary tables, not a harmonized food-group composition panel. Separate sugar-commodity files do not measure total dietary or added sugar. | Not answered yet. Requires a carefully harmonized food-group expenditure/quantity analysis; sugar remains optional and secondary. |
| 7. Do states form distinct dietary-pattern groups? | There are 36 State/UT observations per sector and only two rounds, with a narrow nutrient set. | Exploratory clustering is possible but not strong or stable enough for a core claim. Defer unless richer comparable state indicators are assembled. |
| 8. Do averages hide differences? | Yes, descriptively: across MPCE groups the bottom 5% increased while the top 5% decreased between rounds. Rural calorie gap between top and bottom 5% narrowed 1,509 to 1,253 kcal/day; urban narrowed 1,855 to 1,396. Protein gaps narrowed 46.1 to 41.5 g/day rural and 50.0 to 39.6 urban. | Answered descriptively for published fractiles. These are re-ranked groups, not the same households followed over time. |
| 9. Are there unusual state/group patterns? | Sikkim has the largest displayed calorie increases (+509 rural, +423 urban); Karnataka rural has the largest decrease (-125), and West Bengal urban the largest (-85). | These are flags for checking, not verified outliers or statistically reliable rankings. Validate source context and uncertainty before interpreting. |
| 10. Which groups are at risk of inadequate intake? | Aggregate average grams per person cannot establish individual adequacy, and the current tables do not provide the person-level distributions and requirement variables needed. | Not answerable with this evidence. Do not classify people as adequate/inadequate from these averages. |

## Main interpretation

For the two latest HCES rounds, national average protein and calorie estimates were nearly stable, while the published MPCE-fractile tables show a contrasting movement: the bottom 5% had higher estimates and the top 5% lower estimates in 2023-24 than in 2022-23. This is a potentially interesting distributional pattern, but it is not a causal result, a same-household change, or a statistically tested convergence. The strongest safe story is that national means conceal different patterns across expenditure groups and nutrients.

## What remains before a defensible final case study

The descriptive analysis and core question answers are complete using published official aggregates. There is no data-acquisition blocker for this version. To add inferential statistics, the remaining work is a separate validation track:

1. Confirm the exact unit-level HCES coding, weights, strata/PSUs, and nutrient-conversion rules against the official documentation.
2. Reproduce selected published estimates with unit-level data; the current reconstruction misses several benchmarks and is diagnostic only.
3. Resolve the mixed DDM item codes and sampling-design implementation before reporting standard errors, confidence intervals, p-values, or household-level nonlinear models.
4. If time permits, add food-group composition as a secondary analysis. Do not treat the sugar-commodity series as total sugar intake.

The first two items are a bounded validation task, not a prerequisite to presenting the descriptive results above. Exact microdata reconciliation could take substantially longer because the current item-level data have unresolved composition/coding issues. The immediate analysis questions can be presented now; inferential claims must wait for validated design-aware estimates.

## Recommended final study scope

- **Primary outcome:** protein (g/person/day).
- **Companion outcome:** calories (kcal/person/day); use fat only as contextual evidence when clearly labeled.
- **Main comparisons:** national rural/urban, state/sector descriptive changes, and MPCE-fractile patterns.
- **Analysis status:** validated published aggregate descriptions; no inferential tests or causal claims.
- **Exclude from core claims:** sugar as total intake, individual adequacy, long-run trends, causal effects of expenditure, significance of state rankings, and microdata-reconstruction estimates.

## Source

MoSPI/NSO, [NSS Report No. 594: Nutritional Intake in India (HCES 2022-23 and 2023-24)](https://www.mospi.gov.in/sites/default/files/publication_reports/Nutritional_Intake_in_India_L.pdf), Summary Statements 1 and 5, Tables 3.2 and 3.9.
