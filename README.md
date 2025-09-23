# DSML – Data Science / Machine Learning Project

# Project Summary
A reusable Python project providing classes to simplify common data science / ML workflows: data cleaning, missing value & outlier handling, and transformation steps. Ideal for analysts or machine learning practitioners to integrate into their pipelines.


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
###  Key Class: `DataProcessor`

| Method | Description |
|--------|-------------|
| `check_dtypes()` | Inspect data types of all columns |
| `drop_columns(columns)` | Drop specified columns from the DataFrame |
| `check_categorical_columns()` | List all categorical columns |
| `set_index_date(column_name)` | Convert a column to datetime and set as index |
| `check_index_is_datetime()` | Check if index is datetime type |
| `check_missing()` | Display count of missing values |
| `handle_missing_values(strategy='drop')` | Handle missing values (`drop`, `mean`, `median`, `mode`) |
| `inspect_duplicates(subset=None)` | Check for duplicate rows |
| `handle_duplicates(action='drop')` | Drop or keep duplicate records |
| `log_duplicates(filepath)` | Save duplicate rows to a CSV log |
| `check_outliers(z_thresh=2)` | Detect outliers using Z-score method |
| `remove_outliers_zscore(z_thresh=2)` | Remove outliers with Z-score method |
| `remove_outliers_iqr(multiplier=1.5)` | Remove outliers with IQR method |
| `visualize_outliers_boxplot(before_df, after_df)` | Compare outliers using boxplots |
| `visualize_outliers_histogram(before_df, after_df)` | Compare histograms before/after cleaning |
| `run_all_checks()` | Run a full suite of data quality checks |
| `save(filepath, format='csv')` | Save cleaned DataFrame to disk |

## Project Status & Roadmap
| Feature                      | Status         |
| ---------------------------- | -------------- |
| Data cleaning                | ✅ Implemented  |
| Outlier detection            | ✅ Implemented  |
| Visualization tools          | 🔄 In Progress |
| Forecasting / Model training | 🔜 Planned     |
| Time series support          | 🔜 Planned     |


## License

This project is licensed under the [MIT License](./LICENSE) © 2025 George Milonas.
