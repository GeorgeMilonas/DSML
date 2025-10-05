# DataProcessor

This document provides a detailed API reference for the `DataProcessor` class used in the DSML project.

## Methods


---

## 1. `__init__(self, filepath=None, dataset=None)`

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
