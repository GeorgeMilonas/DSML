import pandas as pd                             # For DataFrame manipulation
from pathlib import Path                        # For creating directories and handling file paths
from datetime import datetime                   # For timestamps in log filenames
from scipy.stats import zscore                  # For outlier detection (Z-score)
from sklearn.preprocessing import MinMaxScaler  # For normalizing numeric data


class DataProcessor:
    def __init__(self, filepath):
        self.filepath = filepath
        self.df = None

    def load(self):
        self.df = pd.read_excel(self.filepath)
        print("Data loaded successfully.")
        return self

    def drop_columns(self, columns_to_drop):
        self.df.drop(columns=columns_to_drop, inplace=True)
        print(f"Dropped columns: {columns_to_drop}")
        return self

    def set_index(self, index_column):
        self.df[index_column] = pd.to_datetime(self.df[index_column], errors='coerce')
        self.df.set_index(index_column, inplace=True)
        print(f"Index set to column: {index_column}")
        return self

####
## Check Methods
# 1. Check for Missing Values
    def check_missing(self):
        missing = self.df.isnull().sum()
        print("Missing values per column:")
        print(missing[missing > 0])
        return missing
        
# 2. Check for Duplicates
    def check_duplicates(self):
        duplicates = self.df.duplicated().sum()
        print(f"Duplicate rows: {duplicates}")
        return duplicates
  
# 2b. How to get Duplicates       
    def get_duplicates(self, subset=None, keep=False):
        """
        Return all duplicate rows in the DataFrame.
	    
        Parameters:
            subset (list or str, optional): Columns to check for duplicates.
            keep (bool or str): 'first', 'last', or False (default is False to return all).
	    
        Returns:
            pd.DataFrame: DataFrame containing duplicate rows.
        """
        dups = self.df[self.df.duplicated(subset=subset, keep=keep)]
        print(f"Found {len(dups)} duplicate rows.")
        return dups
    
# 2c. How to Handle Duplicates    
    def handle_duplicates(self, method="keep_first"):
        duplicates = self.df.duplicated()
        num_duplicates = duplicates.sum()
        print(f"Found {num_duplicates} duplicate rows.")
	    
        if num_duplicates == 0:
            return self
	    
        if method == "keep_first":
            self.df.drop_duplicates(keep='first', inplace=True)
            print("Kept first occurrence of duplicates.")
        elif method == "keep_last":
            self.df.drop_duplicates(keep='last', inplace=True)
            print("Kept last occurrence of duplicates.")
        elif method == "drop_all":
            self.df = self.df[~duplicates]
            print("Dropped all duplicate rows.")
        elif method == "flag":
            self.df['is_duplicate'] = duplicates
            print("Flagged duplicate rows in 'is_duplicate' column.")
        else:
            raise ValueError(f"Unknown duplicate handling method: {method}")
	    
        return self
        
# 2d. Make a log file
    def log_duplicates(self, subset=None, keep=False, log_dir="logs", filename=None, file_format="csv"):
        """
        Logs duplicate rows to a file.
	    
        Parameters:
            subset (list or str, optional): Columns to check for duplicates.
            keep (bool or str): 'first', 'last', or False (default is False to return all duplicates).
            log_dir (str): Directory to save the log file.
            filename (str, optional): Custom filename. If None, it will auto-generate one.
            file_format (str): 'csv' or 'xlsx'.
        """
        duplicates = self.df[self.df.duplicated(subset=subset, keep=keep)]
        num_dups = len(duplicates)
	    
        if num_dups == 0:
            print("No duplicates found to log.")
            return None
	    
        # Ensure log directory exists
        log_path = Path(log_dir)
        log_path.mkdir(parents=True, exist_ok=True)
	    
        # Generate filename if not provided
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"duplicates_log_{timestamp}.{file_format}"
        else:
            filename = f"{filename}.{file_format}" if not filename.endswith(f".{file_format}") else filename
	    
        # Full file path
        file_path = log_path / filename
	    
        # Save file
        if file_format == "csv":
            duplicates.to_csv(file_path, index=False)
        elif file_format == "xlsx":
            duplicates.to_excel(file_path, index=False)
        else:
            raise ValueError("file_format must be 'csv' or 'xlsx'.")
	    
        print(f"Logged {num_dups} duplicate rows to: {file_path}")
        return file_path
        
# 3. Check Data Types
    def check_dtypes(self):
        print("Data types:")
        print(self.df.dtypes)
        return self.df.dtypes

# 4. Check Date Index
# Make sure the index is a valid datetime index:
    def check_index_is_datetime(self):
        is_dt = pd.api.types.is_datetime64_any_dtype(self.df.index)
        print(f"Index is datetime: {is_dt}")
        return is_dt

# 5. Check for Outliers (Basic Example)
    def check_outliers(self, z_thresh=3):
        numeric_df = self.df.select_dtypes(include='number')
        z_scores = numeric_df.apply(zscore)
        outliers = (z_scores.abs() > z_thresh).sum()
        print("Outliers per column (Z-score > 3):")
        print(outliers[outliers > 0])
        return outliers
        
## 6. A Method to Run All Checks
    def run_all_checks(self):
        print("\nRunning data quality checks...")
        self.check_missing()
        self.check_duplicates()
        self.check_dtypes()
        self.check_index_is_datetime()  
        
# &. A method to Normalizze Columns
    def normalize_columns(self, columns=None):
        """
        Normalize specified columns (min-max scaling).
        If columns is None, normalize all numeric columns.
        """	    
        cols = columns or self.df.select_dtypes(include='number').columns
        scaler = MinMaxScaler()
        self.df[cols] = scaler.fit_transform(self.df[cols])
        print(f"Normalized columns: {list(cols)}")
        return self

# 7. A method to Filter by Date
    def filter_by_date_range(self, start_date, end_date):
        """
        Filter the DataFrame by a date range on the index (assumes datetime index).
        """
        if not pd.api.types.is_datetime64_any_dtype(self.df.index):
            raise ValueError("Index is not datetime. Use set_index() to set a datetime column first.")
        
        print(f"Filtering from {start_date} to {end_date}")
        print(f"Data index range: {self.df.index.min()} to {self.df.index.max()}")

        filtered_df = self.df.loc[start_date:end_date]
        print(f"Rows after filtering: {len(filtered_df)}")
        return filtered_df
'''
        # Checkpoint Sanity Test
        print(f"Filtered data from {start_date} to {end_date}. Rows: {len(filtered_df)}")
        return filtered_df
'''
