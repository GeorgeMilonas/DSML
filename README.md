# DS/ML – Data Science / Machine Learning Project
![License](https://img.shields.io/badge/license-MIT-green)
![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)

A Python toolkit designed to streamline common data science and machine learning workflows by providing reusable classes for data cleaning, missing value handling, outlier detection, and transformations.

# Project Summary
A reusable Python project providing classes to simplify common DS / ML workflows: data cleaning, missing value and outlier handling, and transformation steps. Ideal for analysts or machine learning practitioners to integrate into their pipelines.


## Documentation

Full API and method reference are available in the [`docs/`](docs/index.md) folder.


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
You can find the sample dataset [here](./data/foo_sales_dataset.csv).

### Sample Output

```plaintext
🟢 Data loaded successfully.

🔹 First 5 rows:
ID        DATE        DAY  MANAGER  ESALES   CARDS    CASH  TOTAL_SALES  RECEIPT
0   1  2025-01-01  Wednesday      Bob  166.57  304.67  334.48       805.72       34
1   2  2025-01-01  Wednesday  Charlie  614.18  156.63  239.96      1010.77       33
2   3  2025-01-01  Wednesday    Alice  143.21  419.47  263.33       826.01       51
3   4  2025-01-02   Thursday      Bob  988.67  669.25  433.05      2090.97       32
4   5  2025-01-03     Friday      Bob  263.15  615.05  439.86      1318.06       83

🔹 Number of rows and columns in the dataset: (654, 9)

🔹 Check for Data Types:
ID               int64
DATE            object
DAY             object
MANAGER         object
ESALES         float64
CARDS          float64
CASH           float64
TOTAL_SALES    float64
RECEIPT          int64
dtype: object

🔹 Categorical columns and unique value counts:
 - DATE: 221 unique value(s)
 - DAY: 7 unique value(s)
 - MANAGER: 3 unique value(s)
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

3. Model Selection & Forecasting – Select appropriate models and generate predictions or forecasts based on the data.


## Key Classes

### 01. `DataProcessor`
<details>
<summary>Expand here: Method List</summary>

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
</details>

### 02. `DataEDA`
<details>
<summary>Expand here: Method List</summary>
 
| No. | Method | Description |
|-----|--------|-------------|
| 1. | `plot_categorical_counts(...)` | Shows bar charts of counts for categorical or date columns |
| 2. | `_apply_weekday_ordering()` | Detects if a column contains weekdays and orders them Monday → Sunday |
| 3. | `plot_categorical_heatmap()` | Shows a heatmap of counts or proportions between two categorical columns |
| 4. | `plot_target_distribution(target)` | Plots a bar chart of counts for the target variable, with special ordering for weekdays |
| 5. | `summary_by_target(target)` | Shows summary statistics grouped by the target variable |
| 6. | `run_target_analysis(...)` | Runs a full analysis on the target variable, including plots and summary stats. Can bin numeric targets |
| 7. | `group_and_describe(...)` | Groups data by one or more columns and returns summary statistics |
| 8. | `plot_grouped_summary(...)` | Plots aggregated numeric data (mean, boxplots, violin plots, etc.) grouped by categories |
| 9. | `bin_numeric_column(...)` | Converts a numeric column into categorical bins |
| 10. | `plot_missing_data()` | Shows a bar plot of missing value counts for each column |
| 11. | `run_all()` | Runs a complete EDA, including summaries, missing data, distributions, correlations, and optional target analysis |
</details>


## Project Status & Roadmap
| Classes                      | Status         |
| ---------------------------- | -------------- |
| Data Processor               |  Implemented  |
| Visualization tools          |  In Progress |
| Forecasting / Model training |  In Progress   |
| Time series support          |  In Progress   |


## Contributing

Contributions are welcome! Please feel free to open issues or submit pull requests to improve the project.

---

Thank you for your support!


## License

This project is licensed under the [MIT License](./LICENSE) © 2025 George Milonas.
