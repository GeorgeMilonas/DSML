# DS/ML – Data Science / Machine Learning Project
A Python toolkit designed to streamline common data science and machine learning workflows by providing reusable classes for data cleaning, missing value handling, outlier detection, and transformations.

# Project Summary
A reusable Python project providing classes to simplify common data science / ML workflows: data cleaning, missing value – outlier handling, and transformation steps. Ideal for analysts or machine learning practitioners to integrate into their pipelines.


## Contents

- [Installation](#installation)  
- [Quick Start](#quick-start)  
- [Folder Structure](#folder-structure)  
- [Work Flow](#workflow)  
- [Key Classes](#key-classes)  
- [Project Status & Roadmap](#project-status--roadmap)  
- [Contributing](#contributing)  
- [License](#license)


## Installation

```bash
git clone https://github.com/GeorgeMilonas/DSML.git
cd DSML
pip install -r requirements.txt
```

## Quick Start

```python
from processor import DataProcessor

file_path = '/your_path/data/foo_sales_dataset.csv'
target_col = 'your_target_column'

# Load data and create a processor data frame object 
processor = DataProcessor(filepath=file_path).load()

processor.check_missing()
processor.handle_missing_values('mean')
processor.save(path="/your_path/data/processed_data.xlsx", format="xlsx")
```

## Folder Structure
```plaintext
DSML/
├── src/              # reusable modules and classes
├── data/             # datasets or download scripts
├── models/           # saved models
├── tests/            # unit tests
├── requirements.txt
├── README.md
└── LICENSE
```


## Workflow

1. Data Processing – Clean, transform, and prepare data for analysis.

2. Visualization – Explore data using visual tools to identify trends and patterns.

3. Model Selection / Forecasting – Choose appropriate models and generate forecasts based on the data.


## Key Classes
### Key Class: `DataProcessor` – Methods Overview

| No. | Method | Description |
|-----|--------|-------------|
| 1. | `__init__(filepath=None, dataset=None)` | Initialize the class with a file path or dataset |
| 2. | `load()` | Load data from CSV, Excel, or JSON files |
| 3. | `check_dtypes()` | Print and return data types of each column |
| 4. | `check_categorical_columns()` | List categorical columns and count unique values |
| 5. | `drop_columns(columns_to_drop)` | Drop specified columns from the DataFrame |
| 6. | `set_index_column(column_name)` | Set any column as the DataFrame index |
| 7. | `set_index_date(...)` | Convert a column to datetime and set as index (with options) |
| 8. | `check_index_is_datetime()` | Validate if index is a datetime/date type |
| 9. | `check_missing(...)` | Analyze and print missing data; return rows if needed |
| 10. | `handle_missing_values(strategy)` | Handle missing values using strategy (`mean`, `median`, etc.) |
| 11. | `inspect_duplicates(...)` | Detect duplicate rows with optional subset & output |
| 12. | `handle_duplicates(method)` | Drop, keep, or flag duplicate rows |
| 13. | `log_duplicates(...)` | Save duplicate rows to a log file (`csv` or `xlsx`) |
| 14. | `inspect_duplicate_columns()` | Checks for duplicate column names in the DataFrame |
| 15. | `handle_duplicate_columns()` | Removes duplicate columns from the DataFrame |
| 16. | `check_outliers(z_thresh)` | Identify numeric outliers using Z-score |
| 17. | `remove_outliers_zscore(z_thresh)` | Remove rows with outliers across all numeric columns |
| 18. | `remove_outliers_from_column(column, z_thresh)` | Remove outliers from a specific column (Z-score) |
| 19. | `remove_outliers_iqr(column, multiplier)` | Remove outliers from a column using IQR |
| 20. | `get_processed_data()` | Return the current version of the processed DataFrame |
| 21. | `visualize_outliers_boxplot(original_df, cleaned_df, column)` | Compare outliers before and after using boxplots |
| 22. | `visualize_outliers_histogram(original_df, cleaned_df, column)` | Compare distribution before/after with histograms |
| 23. | `run_all_checks()` | Run major data quality checks in one step |
| 24. | `save(path, format='csv')` | Save the final DataFrame as a CSV or Excel file |


## Project Status & Roadmap
| Classes                      | Status         |
| ---------------------------- | -------------- |
| Data Processor               |  Implemented  |
| Visualization tools          |  In Progress |
| Forecasting / Model training |  In Progress   |
| Time series support          |  In Progress   |


## License(https://img.shields.io/badge/license-MIT-green)

This project is licensed under the [MIT License](./LICENSE) © 2025 George Milonas.
