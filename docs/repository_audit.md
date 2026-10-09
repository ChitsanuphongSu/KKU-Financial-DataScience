# Repository Audit

## Locations

- Master read-only reference: local master project, intentionally not published
- New repository: this repository root

## Selective inclusions

- Core cleaning, analysis-data, EDA, sensitivity, and correlation scripts.
- Approved aggregate tables and aggregate-only public figures under `outputs/figures/public/`.
- Reader notebook and public-facing documentation generated in this repository.

## Exclusions

- Raw survey CSV, all respondent-level workbooks/datasets, private investigation tables, raw-observation visuals, the approved final presentation (private instructor distribution only), output ZIP, preview renders, internal phase history, and runtime build artifacts.
- Presentation-production script excluded because it depends on a bundled local presentation runtime and is not required to understand or reproduce the public analysis walkthrough.

## Dependency and path review

Copied Python scripts use `Path(__file__).resolve().parents[1]` and contain no machine-specific paths. They expect private input workbooks at repository root, so full execution is intentionally limited by the privacy policy.

## Reproducibility status

The public notebook uses only aggregate tables and aggregate-only release figures. No scientific analysis was changed to create the public visual layer. Full source-pipeline execution is not performed because the private raw/processed data are intentionally absent.

## Git safety

Git is initialized only in this new repository. No remote is configured and nothing is pushed.

## Master integrity

Important master hashes were recorded before copy and compared after packaging. Result: PASS.
