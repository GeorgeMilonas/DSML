# Data Science / Machine Learning

For this Python project, the goal is to implement classes that can be
called from the main function to simplify the process of DS/ML tasks.


# Folder Structure
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


##  Class DataProcessor - Methods Overview

Below is a list of all available methods in the `DataProcessor` class, along with their purpose, arguments, and typical use cases.

## Table of Contents

1. [check\_dtypes()](#1-check_dtypes)
2. [drop\_columns()](#2-drop_columnscolumns)
3. [check\_categorical\_columns()](#3-check_categorical_columns)
4. [set\_index\_date()](#4-set_index_datecolumn_name)
5. [check\_index\_is\_datetime()](#5-check_index_is_datetime)
6. [check\_missing()](#6-check_missing)
7. [handle\_missing\_values()](#7-handle_missing_valuesstrategydrop)
8. [inspect\_duplicates()](#8-inspect_duplicatessubsetnone)
9. [handle\_duplicates()](#9-handle_duplicatesactiondrop)
10. [log\_duplicates()](#10-log_duplicatesfilepathduplicates_logcsv)
11. [check\_outliers()](#11-check_outliersz_thresh2)
12. [remove\_outliers\_zscore()](#12-remove_outliers_zscorez_thresh2)
13. [remove\_outliers\_iqr()](#13-remove_outliers_iqrmultiplier15)
14. [visualize\_outliers\_boxplot()](#14-visualize_outliers_boxplotbefore_df-after_df)
15. [visualize\_outliers\_histogram()](#15-visualize_outliers_histogrambefore_df-after_df)
16. [run\_all\_checks()](#16-run_all_checks)
17. [save()](#17-savefilepath-formatcsv)

---

### 1. `check_dtypes()`

**Purpose:**
Inspects and prints the data types of each column in the DataFrame.

**Arguments:**
*None*

**Why Use It:**
Helps ensure data types are correct before processing — essential for filtering, encoding, and modeling tasks.

---

### 2. `drop_columns(columns)`

**Purpose:**
Removes specified columns from the DataFrame.

**Arguments:**

* `columns` *(str, list, set, or tuple)* — Column(s) to drop.

**Why Use It:**
Cleans up irrelevant or redundant data. Prevents errors by safely handling non-existent columns with helpful messages.

---

### 3. `check_categorical_columns()`

**Purpose:**
Identifies columns containing categorical data.

**Arguments:**
*None*

**Why Use It:**
Useful before encoding or grouping operations, especially in preparation for machine learning models.

---

### 4. `set_index_date(column_name)`

**Purpose:**
Converts a column to datetime format and sets it as the DataFrame index.

**Arguments:**

* `column_name` *(str)* — The column to convert and set as the index.

**Why Use It:**
Essential for time series analysis and working with date-based features.

---

### 5. `check_index_is_datetime()`

**Purpose:**
Validates that the DataFrame index is of datetime type.

**Arguments:**
*None*

**Why Use It:**
Ensures compatibility with pandas time-based operations (e.g. resampling, date filtering).

---

### 6. `check_missing()`

**Purpose:**
Identifies missing values in the DataFrame.

**Arguments:**
*None*

**Why Use It:**
Gives a quick overview of the extent and location of missing data.

---

### 7. `handle_missing_values(strategy='drop')`

**Purpose:**
Handles missing values using a specified strategy.

**Arguments:**

* `strategy` *(str)* — Options: `'drop'`, `'mean'`, `'median'`, `'mode'`.

**Why Use It:**
Simplifies and standardizes missing value handling.

---

### 8. `inspect_duplicates(subset=None)`

**Purpose:**
Checks for duplicate rows based on all or selected columns.

**Arguments:**

* `subset` *(list or str, optional)* — Column(s) to check for duplicates.

**Why Use It:**
Helps detect redundant or duplicate records in your data.

---

### 9. `handle_duplicates(action='drop')`

**Purpose:**
Removes or flags duplicate rows.

**Arguments:**

* `action` *(str)* — `'drop'` or `'keep'`.

**Why Use It:**
Ensures a clean dataset without repeated entries.

---

### 10. `log_duplicates(filepath='duplicates_log.csv')`

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
