# DSML – Data Science / Machine Learning Project

# Project Summary
A reusable Python project providing classes to simplify common data science / ML workflows: data cleaning, missing value & outlier handling, and transformation steps. Ideal for analysts or machine learning practitioners to integrate into their pipelines.


## Contents

- [Installation](#installation)  
- [Quick Start](#quick-start)  
- [Folder Structure](#folder-structure)  
- [Core Modules / Key Classes](#core-modules--key-classes)  
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


##  Key Class: DataProcessor

This class wraps common data cleaning and preprocessing tasks into convenient methods.

Method	Description
check_dtypes()	Inspect data types of all columns
drop_columns(columns)	Drop specified columns from the DataFrame
check_categorical_columns()	List all categorical columns
set_index_date(column_name)	Convert a column to datetime and set as index
check_index_is_datetime()	Check if index is datetime type
check_missing()	Display count of missing values
handle_missing_values(strategy='drop')	Handle missing values (drop, mean, median, mode)
inspect_duplicates(subset=None)	Check for duplicate rows
handle_duplicates(action='drop')	Drop or keep duplicate records
log_duplicates(filepath)	Save duplicate rows to a CSV log
check_outliers(z_thresh=2)	Detect outliers using Z-score method
remove_outliers_zscore(z_thresh=2)	Remove outliers with Z-score method
remove_outliers_iqr(multiplier=1.5)	Remove outliers with IQR method
visualize_outliers_boxplot(before_df, after_df)	Compare outliers using boxplots
visualize_outliers_histogram(before_df, after_df)	Compare histograms before/after cleaning
run_all_checks()	Run a full suite of data quality checks
save(filepath, format='csv')	Save cleaned DataFrame to disk

**Purpose:**
Logs duplicate rows to a CSV file for review.

**Arguments:**

* `filepath` *(str)* — File path to save the log.

**Why Use It:**
Enables manual inspection before deletion or further processing.

---

### 11. `check_outliers(z_thresh=2)`

**Purpose:**
Detects outliers in numeric columns using the Z-score method.

**Arguments:**

* `z_thresh` *(float)* — Z-score threshold (default = 2).

**Why Use It:**
Quick way to find extreme values in normally distributed data.

---

### 12. `remove_outliers_zscore(z_thresh=2)`

**Purpose:**
Removes rows with outlier values in any numeric column using Z-score.

**Arguments:**

* `z_thresh` *(float)* — Z-score threshold for removal.

**Why Use It:**
Cleans the entire dataset from outliers across all numeric features.

---

### 13. `remove_outliers_iqr(multiplier=1.5)`

**Purpose:**
Removes outliers using the IQR method.

**Arguments:**

* `multiplier` *(float)* — Multiplier to scale IQR bounds (default = 1.5).

**Why Use It:**
Better suited for skewed or non-normal distributions (e.g., income, age).

---

### 14. `visualize_outliers_boxplot(before_df, after_df)`

**Purpose:**
Compares data distributions before and after cleaning using boxplots.

**Arguments:**

* `before_df` *(DataFrame)* — Data before outlier removal.
* `after_df` *(DataFrame)* — Data after outlier removal.

**Why Use It:**
Visual validation of how much data was affected or removed.

---

### 15. `visualize_outliers_histogram(before_df, after_df)`

**Purpose:**
Shows histograms comparing data before and after cleaning.

**Arguments:**

* `before_df` *(DataFrame)* — Data before outlier removal.
* `after_df` *(DataFrame)* — Data after outlier removal.

**Why Use It:**
Helps detect changes in distribution caused by data cleaning.

---

### 16. `run_all_checks()`

**Purpose:**
Runs all major data quality checks in a single method.

**Arguments:**
*None*

**Why Use It:**
Perfect for early-stage EDA to get a quick overview of dataset quality.

---

### 17. `save(filepath, format='csv')`

**Purpose:**
Saves the cleaned DataFrame to disk.

**Arguments:**

* `filepath` *(str)* — Path to save the file.
* `format` *(str)* — `'csv'` or `'xlsx'` (default = `'csv'`)

**Why Use It:**
Persists results for sharing, reporting, or downstream analysis.

---


## License

This project is licensed under the [MIT License](./LICENSE) © 2025 George Milonas.
