# Presentation and defense guide

## 60–90 second presentation script

Our project asks whether recent changes in India's diet look nutritionally better, and whether national averages hide important differences. We focused on protein as the main nutrient and calories as a companion measure, using MoSPI's HCES 2022-23 and 2023-24 published estimates. These are nutrients calculated from household food consumption, not individual dietary recalls.

At the all-India level, estimates were nearly stable: rural protein moved from 61.9 to 61.8 grams per person per day, while urban protein moved from 63.2 to 63.4. Calories declined slightly in both sectors. But the expenditure-group tables tell a more varied story. Between rounds, estimates rose for the bottom 5% of MPCE fractiles and fell for the top 5%, narrowing the displayed top-to-bottom gaps. Across states, calorie and protein changes also tended to move together.

We ran exploratory tests on the published state and MPCE summaries. They describe patterns among these aggregate groups; they are not survey-design-adjusted tests of population change. The provisional household-level reconstruction does not yet reproduce the official estimates closely enough for that kind of inference. Our conclusion is therefore descriptive: national averages were stable, while published estimates differed across expenditure groups. We cannot infer individual adequacy, causation, or statistical significance from the current analysis.

## Five-slide outline

1. **Question and study design** — Research question; protein primary, calories companion; two HCES rounds; household-derived nutrient estimates.
2. **Data and boundaries** — NSS Report No. 594; state/sector and MPCE fractile tables; repeated cross-sections; no design-based uncertainty available in the published tables.
3. **National and rural–urban results** — Protein/calorie point changes; show `figures/national-protein-calories.png`; emphasize near-stability.
4. **What national averages conceal** — Bottom vs top MPCE changes; show `figures/mpce-bottom-top-nutrients.png`; explain independently ranked fractiles.
5. **Exploratory results and conclusion** — State variation and co-movement; show `figures/state-calorie-protein-changes.png`; distinguish exploratory tests from population inference; next step is microdata validation.

## Likely questions and accurate answers

**Why did you choose protein as the main nutrient?**

The project began with a protein dataset already prepared and the official HCES report provides comparable protein and calorie estimates by sector, State/UT, and MPCE group for both rounds. Protein is the primary outcome; calories help interpret whether the changes move together.

**Can you say protein intake increased in India?**

No. The published all-India estimate was nearly flat: slightly lower rural and slightly higher urban. An equal-weight average of state changes is positive, but it is not the population-weighted national estimate.

**Why do the exploratory tests show low p-values?**

They test patterns across published aggregate groups under simple assumptions. They do not incorporate HCES sampling weights, strata, clusters, or uncertainty in each published estimate. So we report them as diagnostics, not evidence of statistically significant population change.

**Does the MPCE gradient mean more spending causes better nutrition?**

No. It is an association between expenditure-ranked groups and average nutrient estimates. These aggregate comparisons cannot isolate causation or other differences between households.

**Did the bottom 5% improve over time?**

The published bottom-fractile point estimates were higher in 2023-24 than 2022-23. The groups were ranked separately in each round, so this does not mean the same households improved. We also lack uncertainty estimates to determine if the difference exceeds sampling variation.

**Is the sugar estimate total sugar intake?**

No. It covers selected sugar commodity codes only; sugar in sweets, beverages, and other foods is not included. It is secondary exploratory material, not a total sugar measure.

**Why not use the household microdata for significance tests now?**

The current reconstruction falls roughly 10–14% below the report's calorie and protein benchmarks, omits mixed food codes, and has a remaining scaling correction. Statistical tests on those estimates could give misleading results. We need to resolve and validate the estimator, then account for the survey design.

**What would be required for stronger conclusions?**

Reproduce selected official estimates from the unit-level files, validate item coding and nutrient conversion, identify the correct weights, strata, and PSUs, and then calculate design-aware standard errors and confidence intervals. Individual adequacy would require appropriate individual-level intake and requirement data as well.

## Claims safe to make

- The published national protein and calorie estimates were nearly stable between HCES 2022-23 and 2023-24.
- The published estimates rise across MPCE fractiles within both years and sectors.
- Bottom- and top-fractile point estimates moved in opposite directions between rounds.
- State-level point changes vary, and calorie and protein changes are positively associated across states.
- The exploratory tests summarize patterns in aggregate point estimates and are not survey-design-adjusted population inference.

## Claims to avoid

- “Protein intake significantly increased in India.”
- “Higher expenditure caused better nutrition.”
- “The same low-income households improved between survey rounds.”
- “The sugar dataset measures total sugar or added sugar intake.”
- “The population is protein adequate/inadequate based on the national average.”
- Any causal or significance claim based on the provisional microdata reconstruction.
