# Validation policy

The repository intentionally does not publish invented accuracy, precision, recall or F1 numbers. Run the reproducible training command to generate `ml-service/artifacts/metrics.json` from the labelled dataset in `ml-service/data/health_queries.csv`.

The included dataset is synthetic development data. It is not a clinical validation dataset and should not be used to infer medical performance. A research-grade evaluation should use a clinically reviewed, appropriately licensed and representative dataset, with a held-out test set and documented annotation protocol.
