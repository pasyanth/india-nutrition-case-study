# India Nutrition Trends Case Study

This repository contains the code, analysis outputs, figures, and assignment documents for the India nutrition trends project. The primary analysis uses protein as its main outcome and calories as supporting context, drawing on MoSPI/NSO HCES estimates for 2022-23 and 2023-24.

## Main deliverables

- `outputs/final_case_study.md` — complete report, including the four protein analyses and figures, with references at the end.
- `outputs/India_Nutrition_Protein_Case_Study.docx` — formatted Word version for submission.
- `outputs/presentation_and_defense_guide.md` — presentation script, five-slide outline, and likely questions.
- `outputs/analysis_ready_nutrition_state_sector.csv` — published State/UT and sector nutrient estimates.
- `outputs/mpce_fractile_nutrition.csv` — published nutrient estimates by MPCE fractile.
- `outputs/exploratory_aggregate_test_results.csv` — exploratory tests on published aggregate cells.

## Repository contents

- Root-level Python scripts audit HCES source files and build analysis-ready datasets.
- `outputs/` contains derived tables, analysis notes, the final report, scripts, and figures.
- PDF reports, layouts, codebooks, and CPI source releases used in the analysis are included as source references.
- Three large household-level derived CSVs are stored as `.csv.gz` files in `outputs/derived_household_data/` to reduce repository size. The corresponding uncompressed CSV paths are ignored by Git.

## HCES unit-level data

The two local unit-level source folders are intentionally excluded from Git: they occupy about 6.9 GB and may be subject to the terms of the official data access. Obtain or retain the files through authorized MoSPI/NSO channels and place them in these project-root folders:

- `CSV_data_HH_Cons_exp_22_23/`
- `HCES_Data_2023-24_Csv/`

Keep the official file names and layouts so the scripts can locate the expected levels. The included survey reports, methodology documents, and layout workbooks describe the source variables and estimation rules.

## Setup

Use Python 3.12 or a compatible version, then install the dependencies:

```powershell
python -m pip install -r requirements.txt
```

Run commands from the repository root. For example:

```powershell
python build_analysis_ready_datasets.py
python build_mpce_fractile_dataset.py
python build_sugar_dataset.py
python outputs/run_exploratory_aggregate_tests.py
python outputs/plot_published_aggregate_findings.py
python outputs/plot_protein_four_analyses.py
python outputs/build_assignment_docx.py
```

The dataset builders that process unit-level HCES records require the locally held source folders above. The analysis tests and plotting scripts use the included published aggregate CSVs. Rebuilding the Word document uses the figures in `outputs/figures/`.

## Interpretation notes

- The primary published HCES estimates are household-consumption-derived nutrient estimates, not individual dietary recalls.
- Published aggregate comparisons are descriptive. The exploratory p-values do not account for survey weights, strata, PSUs, or uncertainty in each published estimate.
- The provisional unit-level nutrient reconstruction is diagnostic only. It does not reproduce several published benchmarks closely enough for inferential claims.
- The selected sugar-commodity dataset does not measure total dietary or added sugar.
- No causal claims or individual adequacy conclusions are supported by these materials.

## Main source

MoSPI/NSO, *NSS Report No. 594: Nutritional Intake in India (HCES 2022-23 and 2023-24)*, [official report PDF](https://www.mospi.gov.in/sites/default/files/publication_reports/Nutritional_Intake_in_India_L.pdf).

Survey unit-level files remain subject to their original source terms; this repository does not grant redistribution rights.
