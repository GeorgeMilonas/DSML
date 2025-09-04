import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
from scipy.stats import zscore
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
import matplotlib.pyplot as plt
import seaborn as sns


class DataProcessor:
    def __init__(self, filepath=None, dataset=None):
        self.df = None
        self.filepath = filepath

        if dataset is not None:
            self.df = pd.DataFrame(dataset)
            self.filepath = None
        elif not filepath:
            raise ValueError("Either 'filepath' or 'dataset' must be provided.")

    def load(self):
        try:
            if self.filepath.endswith(('.xlsx', '.xls')):
                self.df = pd.read_excel(self.filepath)
            elif self.filepath.endswith('.csv'):
                self.df = pd.read_csv(self.filepath)
            elif self.filepath.endswith('.json'):
                self.df = pd.read_json(self.filepath)
            else:
                raise ValueError("🔴 Unsupported file format. Supported: .csv, .xlsx, .xls, .json")
        
            print("🟢 Data loaded successfully.")
            return self
        
        except Exception as e:
            raise RuntimeError(f"🔺Your file wasn't properly loaded !! Reason: {str(e)}")

    def drop_columns(self, columns_to_drop):
        if isinstance(columns_to_drop, str):
            columns_to_drop = [columns_to_drop]
        elif not isinstance(columns_to_drop, (list, tuple, set)):
            raise TypeError("🔴 columns_to_drop must be a string or list/tuple/set of strings.")
        
        # Identify valid and invalid columns
        existing_cols = set(self.df.columns)
        to_drop = [col for col in columns_to_drop if col in existing_cols]
        not_found = [col for col in columns_to_drop if col not in existing_cols]
        
        if not to_drop:
            print("🔺 No matching columns found to drop.")
        else:
            self.df.drop(columns=to_drop, inplace=True)
            print(f"🟢 Dropped columns: {to_drop}")
        
        if not_found:
            print(f"🔺 These columns were not found in the DataFrame and were skipped: {not_found}")
        
        return self

    def set_index(self, index_column, log_invalid=False, log_path="invalid_datetime_rows.csv"):
        # 1. Check if the column exists
        if index_column not in self.df.columns:
            raise ValueError(f"Column '{index_column}' not found in the DataFrame.")
        
        # 2. Attempt to convert column to datetime
        self.df[index_column] = pd.to_datetime(self.df[index_column], errors='coerce')
        
        # 3. Identify invalid datetime rows (i.e., rows where conversion failed)
        invalid_rows = self.df[self.df[index_column].isna()]
        num_invalid = len(invalid_rows)
        
        if num_invalid > 0:
            print(f"🔺️ {num_invalid} rows in '{index_column}' could not be converted to datetime (set as NaT).")
        
            # Optional logging of invalid rows
            if log_invalid:
                invalid_rows.to_csv(log_path, index=False)
                print(f"🔸 Invalid datetime rows saved to: {log_path}")
        
        # 4. Set the datetime column as the index
        self.df.set_index(index_column, inplace=True)
        print(f"🟢 Index set to column: '{index_column}'")
        
        return self


# --- Check methods ---
    def check_dtypes(self):
        print("Data types:")
        print(self.df.dtypes)
        return self.df.dtypes
        
    def check_missing(self, verbose=True, return_all=False, return_rows=False):
        missing_counts = self.df.isnull().sum()
        total_missing = missing_counts.sum()
        
        if verbose:
            print("🔹 Missing values per column:")
            if total_missing == 0:
                print("🟢 No missing values found.")
            else:
                print(missing_counts[missing_counts > 0])
        
        if return_rows:
            missing_rows = self.df[self.df.isnull().any(axis=1)]
            print(f"\n🔴 Rows with missing values: {len(missing_rows)}")
            return missing_rows
        
        return missing_counts if return_all else missing_counts[missing_counts > 0]


    def handle_missing_values(self, strategy='mean'):
        initial_missing = self.df.isnull().sum().sum()

        if initial_missing == 0:
            print("🟢 No missing values to handle.")
            return self
        
        numerical_cols = self.df.select_dtypes(include=['int64', 'float64']).columns
        categorical_cols = self.df.select_dtypes(include=['object']).columns
        
        if strategy == 'mean':
            self.df[numerical_cols] = self.df[numerical_cols].fillna(self.df[numerical_cols].mean())
            print(f"🔸 Filled missing numeric values using mean in columns: {list(numerical_cols)}")
        
        elif strategy == 'median':
            self.df[numerical_cols] = self.df[numerical_cols].fillna(self.df[numerical_cols].median())
            print(f"🔸 Filled missing numeric values using median in columns: {list(numerical_cols)}")
        
        elif strategy == 'most_frequent':
            if categorical_cols.empty:
                print("🟢 No categorical columns found to fill.")
            else:
                try:
                    mode = self.df[categorical_cols].mode().iloc[0]
                    self.df[categorical_cols] = self.df[categorical_cols].fillna(mode)
                    print(f"🔸 Filled missing categorical values using mode in columns: {list(categorical_cols)}")
                except IndexError:
                    print("🔺 Could not compute mode — no non-null values in categorical columns.")
        
        elif strategy == 'drop':
            before_drop = len(self.df)
            self.df.dropna(inplace=True)
            after_drop = len(self.df)
            print(f"🟢 Dropped rows with missing values: {before_drop - after_drop}")
        
        else:
            raise ValueError("🔴 Invalid strategy. Choose from: 'mean', 'median', 'drop', or 'most_frequent'.")
        
        # Automatic re-check
        remaining_missing = self.df.isnull().sum().sum()
        if remaining_missing == 0:
            print("🟢 All missing values handled.")
        else:
            print(f"🔴 {remaining_missing} missing values still remain after applying strategy '{strategy}'.")
        return self

    def check_duplicates(self):
        duplicates = self.df.duplicated().sum()
        print(f"Duplicate rows: {duplicates}")
        return duplicates

    def get_duplicates(self, subset=None, keep=False):
        dups = self.df[self.df.duplicated(subset=subset, keep=keep)]
        print(f"Found {len(dups)} duplicate rows.")
        return dups

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

    def log_duplicates(self, subset=None, keep=False, log_dir="logs", filename=None, file_format="csv"):
        duplicates = self.df[self.df.duplicated(subset=subset, keep=keep)]
        num_dups = len(duplicates)

        if num_dups == 0:
            print("No duplicates found to log.")
            return None

        log_path = Path(log_dir)
        log_path.mkdir(parents=True, exist_ok=True)

        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"duplicates_log_{timestamp}.{file_format}"
        else:
            filename = f"{filename}.{file_format}" if not filename.endswith(f".{file_format}") else filename

        file_path = log_path / filename

        if file_format == "csv":
            duplicates.to_csv(file_path, index=False)
        elif file_format == "xlsx":
            duplicates.to_excel(file_path, index=False)
        else:
            raise ValueError("file_format must be 'csv' or 'xlsx'.")

        print(f"Logged {num_dups} duplicate rows to: {file_path}")
        return file_path

    def check_index_is_datetime(self):
        is_dt = pd.api.types.is_datetime64_any_dtype(self.df.index)
        print(f"Index is datetime: {is_dt}")
        return is_dt

    def check_outliers(self, z_thresh=2):
        numeric_df = self.df.select_dtypes(include='number')
        print("\n🟢 Numeric columns used for Z-score calculation:")
        print(numeric_df.columns)
    
        z_scores = numeric_df.apply(zscore)
        print("\n🟢 Sample Z-scores:")
        print(z_scores.head())
    
        outliers = (z_scores.abs() > z_thresh).sum()
        print("\n🟢 Outliers per column (Z-score > threshold):")
        print(outliers[outliers > 0])
        return outliers
    
    def remove_outliers_zscore(df, z_thresh=2):
        numeric_df = df.select_dtypes(include='number')
        z_scores = numeric_df.apply(zscore)
        mask = (z_scores.abs() < z_thresh).all(axis=1)  # Keep rows where all z-scores are below threshold
        return df[mask]
    
    def remove_outliers_from_column(self, column, z_thresh=2):
        z = zscore(self.df[column].dropna())
        mask = (abs(z) < z_thresh)
        filtered_df = self.df.loc[self.df[column].dropna().index[mask]]
        removed = self.df.shape[0] - filtered_df.shape[0]
        print(f"\n🟢 Removed {removed} outliers from '{column}' (Z-thresh = {z_thresh})")
        self.df = filtered_df  # Update the DataFrame in the object
        return self
    
    def remove_outliers_iqr(self, column):
        """
        Remove outliers from the specified column using the IQR method.
        Updates self.df and returns self.
        """
        if column not in self.df.columns:
            print(f"⚠ Column '{column}' not found in the dataset.")
            return self
        
        q1 = self.df[column].quantile(0.25)
        q3 = self.df[column].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        
        before_rows = self.df.shape[0]
        self.df = self.df[(self.df[column] >= lower_bound) & (self.df[column] <= upper_bound)]
        after_rows = self.df.shape[0]
        removed = before_rows - after_rows
        
        print(f"\n🟢 Removed {removed} outliers from '{column}' using IQR method.")
        return self

    def filter_by_date_range(self, start_date, end_date):
        if not pd.api.types.is_datetime64_any_dtype(self.df.index):
            raise ValueError("🔴Index is not datetime. Use set_index() to set a datetime column first.")

        print(f"Filtering from {start_date} to {end_date}")
        filtered_df = self.df.loc[start_date:end_date]
        print(f"Rows after filtering: {len(filtered_df)}")
        return filtered_df

# Lists all categorical columns in the DataFrame.
    def check_categorical_columns(self):
        categorical_cols = self.df.select_dtypes(include=['object', 'category']).columns
        if categorical_cols.empty:
            print("🔴 No categorical columns found.")
        else:
            print(f"🟢 Categorical columns: {list(categorical_cols)}")
        return list(categorical_cols)
        
    def get_processed_data(self):
        #Returns the processed DataFrame.    
        return self.df

    def run_all_checks(self):
        print("\nRunning data quality checks...")
        self.check_missing()
        self.check_duplicates()
        self.check_dtypes()
        self.check_index_is_datetime()
        return self
        
    def visualize_outliers_boxplot(self, original_df, cleaned_df, column):
        fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=True)
    
        sns.boxplot(y=original_df[column], ax=axes[0], color="salmon")
        axes[0].set_title(f"Before Outlier Removal: {column}")
        axes[0].set_ylabel(column)
    
        sns.boxplot(y=cleaned_df[column], ax=axes[1], color="lightgreen")
        axes[1].set_title(f"After Outlier Removal: {column}")
        axes[1].set_ylabel("")
    
        plt.tight_layout()
        plt.show()
    
    def visualize_outliers_histogram(self, original_df, cleaned_df, column):
        plt.figure(figsize=(12, 5))
    
        sns.histplot(original_df[column], kde=True, color='salmon', label='Before', stat='density')
        sns.histplot(cleaned_df[column], kde=True, color='lightgreen', label='After', stat='density')
    
        plt.title(f"Distribution of '{column}' Before and After Z-Score Cleaning")
        plt.xlabel(column)
        plt.ylabel("Density")
        plt.legend()
        plt.tight_layout()
        plt.show()
    
    
    def save(self, path, format="csv"):
            if format == "csv":
                self.df.to_csv(path)
            elif format == "xlsx":
                self.df.to_excel(path)
            else:
                raise ValueError("Unsupported format. Use 'csv' or 'xlsx'.")
            print(f"Data saved to {path}")
            return self
