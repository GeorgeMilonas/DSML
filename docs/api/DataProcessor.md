# DataProcessor

This document provides a detailed API reference for the `DataProcessor` class used in the DSML project.

## Table of Contents

1. [__init__](#1-__init__)
2. [load](#2-load)
3. [check_dtypes](#3-check_dtypes)
4. [check_categorical_columns](#4-check_categorical_columns)
5. [drop_columns](#5-drop_columns)
6. [set_index_column](#6-set_index_column)
7. [set_index_date](#7-set_index_date)
8. [check_index_is_datetime](#8-check_index_is_datetime)
9. [check_missing](#9-check_missing)
10. [handle_missing_values](#10-handle_missing_values)
11. [inspect_duplicates](#11-inspect_duplicates)
12. [handle_duplicates](#12-handle_duplicates)
13. [log_duplicates](#13-log_duplicates)
14. [inspect_duplicate_columns](#14-inspect_duplicate_columns)
15. [handle_duplicate_columns](#15-handle_duplicate_columns)
16. [check_outliers](#16-check_outliers)
17. [remove_outliers_zscore](#17-remove_outliers_zscore)
18. [remove_outliers_from_column](#18-remove_outliers_from_column)
19. [remove_outliers_iqr](#19-remove_outliers_iqr)
20. [get_processed_data](#20-get_processed_data)
21. [visualize_outliers_boxplot](#21-visualize_outliers_boxplot)
22. [visualize_outliers_histogram](#22-visualize_outliers_histogram)
23. [run_all_checks](#23-run_all_checks)
24. [save](#24-save)


## Methods


### Initialization & Loading
---

## 1. `__init__(self, filepath=None, dataset=None)`<a name="1-__init__"></a>

**Description:**  
Initializes a `DataProcessor` instance. Either a file path or a dataset must be provided.

**Args:**
- `filepath` (`str`, optional): Path to the data file (`.csv`, `.xlsx`, `.xls`, or `.json`).
- `dataset` (`pd.DataFrame`, optional): A dataset provided directly as a DataFrame or convertible structure.

**Raises:**
- `ValueError`: If neither `filepath` nor `dataset` is provided.

**Example:**
```python
processor = DataProcessor(filepath="data/data.csv")
# or
processor = DataProcessor(dataset=my_dataframe)
```

## 2. `load(self)`<a name="2-load"></a>

**Description:** 
Loads the dataset from the specified file path. Supports `.csv`, `.xlsx`, `.xls`, and `.json` formats.

**Returns:**
- `DataProcessor`: The updated instance.
- `pd.DataFrame`, optional: Returned only if `return_rows=True`.

**Raises:**
- `RuntimeError`: If the file cannot be loaded due to format or internal read errors.

**Example:**
```python
processor = DataProcessor(filepath="/your_path/data/your_data.csv").load()
```


### Basic Data Inspection
---

## 3. `check_dtypes(self)`<a name="3-check_dtypes"></a>

**Description:** 
Prints and returns the data types of each column in the dataset.

**Returns:**
- `pd.Series`: Series containing data types of each column.

**Example:**
```python
dtypes = processor.check_dtypes()
```

## 4. `check_categorical_columns(self)`<a name="4-check_categorical_columns"></a>

**Description:** 
Identifies and prints categorical columns (object or category dtype) and their unique value counts.

**Returns:**
- `list`: List of categorical column names.

**Example:**
```python
categoricals = processor.check_categorical_columns()
```


### Index & Column Management
---

## 5. `drop_columns(self, columns_to_drop)`<a name="5-drop_columns"></a>

**Description:** 
Drops one or more specified columns from the dataset if they exist.

**Args:**
- `columns_to_drop` (`str` or `list`/`tuple`/`set` of `str`): The name(s) of the column(s) to be dropped.

**Returns:**
- `DataProcessor`: The current instance, allowing for method chaining.

**Raises:**
- `TypeError`: If the input is not a string or list/tuple/set of strings.

**Example:**
```python
processor.drop_columns("unnecessary_column")
processor.drop_columns(["col1", "col2"])
```

## 6. `set_index_column(self, column_name)`<a name="6-set_index_column"></a>

**Description:** 
Sets the specified column as the index of the DataFrame.

**Args:**
- `column_name` (`str`): The name of the column to set as index.

**Returns:**
- `DataProcessor`: The current instance, allowing for method chaining.

**Raises:**
- `ValueError`: If the column does not exist in the dataset.

**Example:**
```python
processor.set_index_column("ID")
```

## 7. `set_index_date(self)`<a name="7-set_index_date"></a>

`**Signature:**`
```python
def set_index_date(
    self,
    index_column,
    log_invalid=False,
    log_path="invalid_datetime_rows.csv",
    check_index=True,
    force_plain_date=False,
)
```

**Description:**
Sets a DataFrame column as the datetime index, handling conversion, validation, and optional logging.

**Args:**
- `index_column` (`str`): Name of the column to set as index.
- `log_invalid` (`bool`, optional): Whether to log rows with invalid datetime values. Defaults to False.
- `log_path` (`str`, optional): File path to save invalid datetime rows if logging is enabled. Defaults to "invalid_datetime_rows.csv".
- `check_index` (`bool`, optional): Whether to validate the index after setting it. Defaults to True.
- `force_plain_date` (`bool`, optional)`: Whether to force conversion to plain date (YYYY-MM-DD) instead of datetime. Defaults to False.

**Returns:**
- `DataProcessor`: The `DataProcessor` instance with the datetime index set.

**Raises:**
- `ValueError`: If the specified column does not exist in the DataFrame.

**Example:**
```python
processor.set_index('DATE', log_invalid=True, check_index=False)
```

## 8. `check_index_is_datetime(self)`<a name="8-check_index_is_datetime"></a>

**Description:**
Checks if the DataFrame index is of a datetime-related type.

**Returns:**
- `bool`: True if the index is datetime, date, or pandas Timestamp; False otherwise.

**Example:**
```python
processor.check_index_is_datetime()
```


### Missing Data Handling
---

## 9. `check_missing(self)`<a name="9-check_missing"></a>

`**Signature:**`
```python
def check_missing(
    self,
    verbose=True,
    return_all=False,
    return_rows=False
)
```

**Description:**
Analyzes and reports missing values in the DataFrame.

**Args:**
- `verbose` (`bool`, optional): Whether to print detailed missing info. Defaults to True.
- `return_all` (`bool`, optional): Reserved for future use. Currently has no effect.
- `return_rows` (`bool`, optional): Whether to return rows with missing values.

**Returns:**
- `Optional[pd.DataFrame]` (`pd.DataFrame`, optional): DataFrame containing rows with missing values, if `return_rows` is True.

**Example:**
```python
processor.check_missing(return_rows=True)
```

## 10. `handle_missing_values(self)`<a name="10-handle_missing_values"></a>

`**Signature:**`
```python
def handle_missing_values(self,
    strategy="mean",
    force_int_cols=None
)
```

**Description:**
Handles missing values in the DataFrame using the specified strategy.

**Args:**
- `strategy` (`str`, optional): Strategy to fill or drop missing values. Choices are `"mean"`, `"median"`, `"most_frequent"`, `"drop"`. Defaults to `"mean"`.
- `force_int_cols` (`list[str]`, optional): List of columns that should be converted back to integers after imputation.

**Returns:**
- `DataProcessor`: The modified instance with missing values handled.

**Raises:**
- `ValueError`: If an invalid strategy is provided.

**Example:**
```python
processor.handle_missing_values(strategy='mean', force_int_cols=['your_column'])
```


### Duplicate Handling
---

## 11. `inspect_duplicates(self)`<a name="11-inspect_duplicates"></a>

`**Signature:**`
```python
def inspect_duplicates(
    self,
    subset=None,
    keep=False,
    return_rows=False
)
```

**Description:**
Inspects the DataFrame for duplicate rows.

**Args:**
- `subset` (`list[str]`, optional): Columns to consider for duplicate detection. If None, all columns are used.
- `keep` (`bool` or `str`, optional): Whether to keep the first/last duplicate or mark all. Defaults to False.
- `return_rows` (`bool`, optional): Whether to return the duplicate rows.

**Returns:**
- `int`: Number of duplicate rows found.
- `DataProcessor`: The updated instance.
- `pd.DataFrame`, optional: Returned only if `return_rows=True`.
  
**Example:**
```python
processor.inspect_duplicates(subset=None, keep=False, return_rows=False)
```

## 12. `handle_duplicates(self, method="keep_first")`<a name="12-handle_duplicates"></a>

**Description:**
Handles duplicate rows in the DataFrame using the specified method.

**Args:**
- `method` (`str`, optional): Strategy for handling duplicates. Options are `"keep_first"`, `"keep_last"`, `"drop_all"`, `"flag"`. Defaults to `"keep_first"`.

**Returns:**
- `DataProcessor`: The modified instance with duplicates handled.

**Raises:**
- `ValueError`: If an unknown method is provided.

**Example:**
```python
processor.handle_duplicates(method="keep_first")
```

## 13. `log_duplicates(self)`<a name="13-log_duplicates"></a>

`**Signature:**`
```python
def log_duplicates(
    self,
    subset=None,
    keep=False,
    log_dir="logs",
    filename=None,
    file_format="csv"
)
```
**Description:**
Logs duplicate rows to a file.

**Args:**
- `subset` (`list[str]`, optional): Columns to consider for duplicates. Defaults to all.
- `keep` (`bool` or `str`, optional): Duplicate retention policy for identification. Defaults to False.
- `log_dir` (`str`, optional): Directory where log file will be saved. Defaults to "logs".
- `filename` (`str`, optional): Filename to use. If None, a timestamped file will be created.
- `file_format` (`str`, optional): Output format - `"csv"` or `"xlsx"`. Defaults to `"csv"`.

**Returns:**
- `Optional[Path]`: Path to the saved log file, or None if no duplicates were found.

**Raises:**
- `ValueError`: If `file_format` is not "csv" or "xlsx".

**Example:**
```python
processor.log_duplicates()
```

## 14. `inspect_duplicate_columns(self)`<a name="14-inspect_duplicate_columns"></a>

**Description:**
Checks for duplicate column names in the DataFrame.

**Returns:**
- `list[str]`: List of duplicate column names.

**Example:**
```python
processor.inspect_duplicate_columns()
```

## 15. `handle_duplicate_columns(self, keep="first")`<a name="15-handle_duplicate_columns"></a>

**Description:**
Removes duplicate columns from the DataFrame.

**Args:**
- `keep` (`str`, optional): Which duplicate to keep - "first" or "last". Defaults to "first".

**Returns:**
- `DataProcessor`: The modified instance with duplicate columns removed.

**Raises:**
- `ValueError`: If `keep` is not "first" or "last".

**Example:**
```python
processor.handle_duplicate_columns()
```


### Outlier Detection & Removal
---

## 16. `check_outliers(self)`<a name="16-check_outliers"></a>

`**Signature:**`
```python
def check_outliers(
    self,
    z_thresh=2,
    return_rows=False,
    log_path=None
)
```

**Description:**
Detects outliers in numerical columns using Z-score method.

**Args:**
- `z_thresh` (`float`, optional): Z-score threshold to identify outliers. Defaults to 2.
- `return_rows` (`bool`, optional): If True, return full rows containing outliers. Defaults to False.
- `log_path` (`str` or `Path`, optional): File path to save outlier rows as CSV. Optional.

**Returns:**
- `pd.DataFrame` or `pd.Series`: DataFrame of outlier rows (if `return_rows` is True), or Series with outlier counts per column.
- `DataProcessor`: The updated instance.
- `pd.DataFrame`, optional: Returned only if `return_rows=True`.

**Example:**
```python
processor.check_outliers()  # Simple output
outliers = processor.check_outliers(z_thresh=2, return_rows=True, log_path='/your_path/data/your_data.csv') # Enhanced
```

## 17. `remove_outliers_zscore(self, z_thresh=2)`<a name="17-remove_outliers_zscore"></a>

**Description:**
Removes rows that contain outliers in any numeric column based on Z-score.

**Args:**
- `z_thresh` (`float`, optional): Z-score threshold to define outliers. Defaults to 2.

**Returns:**
- `DataProcessor`: The modified instance with outliers removed.

**Example:**
```python
processor.remove_outliers_zscore()
```

## 18. `remove_outliers_from_column(self, column, z_thresh=2)`<a name="18-remove_outliers_from_column"></a>

**Description:**
Removes outliers from a specific column using Z-score method.

**Args:**
- `column` (`str`): Column name to check for outliers.
- `z_thresh` (`float`, optional): Z-score threshold. Defaults to 2.

**Returns:**
- `DataProcessor`: The modified instance with outliers removed from the specified column.

**Example:**
```python
processor.remove_outliers_from_column('your_column', z_thresh=2)
```

## 19. `remove_outliers_iqr(self)`<a name="19-remove_outliers_iqr"></a>

`**Signature:**`
```python
def remove_outliers_iqr(
    self,
    column,
    iqr_multiplier=1.5,
    return_rows=False,
    log_path=None
)
```

**Description:**
Removes rows containing outliers from a specified column using the IQR method.

**Args:**
- `column` (`str`): Column to process.
- `iqr_multiplier` (`float`, optional): Multiplier to define outlier range. Defaults to 1.5.
- `return_rows` (`bool`, optional): Whether to return the removed outlier rows. Defaults to False.
- `log_path` (`str` or `Path`, optional): Path to save removed outliers as CSV. Optional.

**Returns:**
- `DataProcessor` or `pd.DataFrame`: Modified instance, or removed outliers DataFrame if `return_rows` is True.
- `DataProcessor`: The updated instance.
- `pd.DataFrame`, optional: Returned only if `return_rows=True`.

**Example:**
```python
processor.remove_outliers_iqr(
    column='your_column',
    iqr_multiplier=1,
    return_rows=True,
    log_path="logs/iqr_outliers.csv"
)
```


### Visualization
---

## 20. `get_processed_data(self)`<a name="20-get_processed_data"></a>

**Description:**
Returns the processed DataFrame.

**Returns:**
- `pd.DataFrame`: The internal DataFrame after processing.

**Example:**
```python
print(processor.get_processed_data())
```

### Visualization
---
## 21. `visualize_outliers_boxplot(self, original_df, cleaned_df, column)`<a name="21-visualize_outliers_boxplot"></a>
    
**Description:**
Displays side-by-side boxplots before and after outlier removal.

**Args:**
- `original_df` (`pd.DataFrame`): DataFrame before outlier removal.
- `cleaned_df` (`pd.DataFrame`): DataFrame after outlier removal.
- `column` (`str`): Column to visualize.

**Example:**
```python
processor.visualize_outliers_boxplot(original_df, processor.df, 'your_column')
```

**Example Output:**
**Foo Sales Data**
![Boxplot before and after outlier removal `foo_data`](/docs/images/Figure_1_foo_Before_after.png)

**Example Output:**
**Real Sales Data**
![Boxplot before and after outlier removal `real data`](/docs/images/Figure_3_real_Before_after.png)

---

## 22. `visualize_outliers_histogram(self)`<a name="22-visualize_outliers_histogram"></a>

`**Signature:**`
```python
def visualize_outliers_histogram(
    self,
    original_df,
    cleaned_df,
    column
)
```

**Description:**
Displays histograms before and after outlier removal using KDE plots.

**Args:**
- `original_df` (`pd.DataFrame`): DataFrame before outlier removal.
- `cleaned_df` (`pd.DataFrame`): DataFrame after outlier removal.
- `column` (`str`): Column to visualize.

**Example:**
```python
processor.visualize_outliers_histogram(original_df, processor.df, 'your_column')
```

**Example Output:**
**Foo Sales Data**
![Histogram before and after outlier removal `foo_data`](/docs/images/Figure_2_foo_Before_after.png)

**Example Output:**
**Real Sales Data**
![Histogram before and after outlier removal `real data`](/docs/images/Figure_4_real_Before_after.png)

---

### Automation & Export
---
## 23. `run_all_checks(self)`<a name="23-run_all_checks"></a>

**Description:**
Runs a set of basic data quality checks on the DataFrame.

**Returns:**
- `DataProcessor`: The instance after running all checks.

**Example:**
```python
processor.run_all_checks()
```

## 24. `save(self, path, format="csv")`<a name="24-save"></a>

**Description:**
Saves the DataFrame to disk.

**Args:**
- `path` (`str` or `Path`): File path where the data should be saved.
- `format` (`str`, optional): Output format: 'csv' or 'xlsx'. Defaults to 'csv'.

**Returns:**
- `DataProcessor`: The instance after saving the data.

**Raises:**
- `ValueError`: If the format is not supported.

**Example:**
```python
processor.save(path="/your-path/data/processed_data.xlsx", format="xlsx")
```

---
