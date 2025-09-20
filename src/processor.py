import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, date, time
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
            raise ValueError("🔴 Either 'filepath' or 'dataset' must be provided.")

    def load(self):
        try:
            if self.filepath.endswith((".xlsx", ".xls")):
                self.df = pd.read_excel(self.filepath)
            elif self.filepath.endswith(".csv"):
                self.df = pd.read_csv(self.filepath)
            elif self.filepath.endswith(".json"):
                self.df = pd.read_json(self.filepath)
            else:
                raise ValueError(
                    "🔴 Unsupported file format. Supported: .csv, .xlsx, .xls, .json"
                )

            print("🟢 Data loaded successfully.")
            return self

        except Exception as e:
            raise RuntimeError(
                f"🔺Your file wasn't properly loaded !! Reason: {str(e)}"
            )

    def check_dtypes(self):
        print("Data types:")
        print(self.df.dtypes)
        return self.df.dtypes

#    def check_categorical_columns(self):
#        categorical_cols = self.df.select_dtypes(include=["object", "category"]).columns
#        if categorical_cols.empty:
#            print("🔴 No categorical columns found.")
#        else:
#            print(f"🟢 Categorical columns: {list(categorical_cols)}")
#        return list(categorical_cols)

    def check_categorical_columns(self):
        categorical_cols = self.df.select_dtypes(include=["object", "category"]).columns
        if categorical_cols.empty:
            print("🔴 No categorical columns found.")
        else:
            print(f"🟢 Categorical columns and unique value counts:")
            for col in categorical_cols:
                unique_count = self.df[col].nunique(dropna=True)
                print(f" - {col}: {unique_count} unique value(s)")
        return list(categorical_cols)

    def drop_columns(self, columns_to_drop):
        if isinstance(columns_to_drop, str):
            columns_to_drop = [columns_to_drop]
        elif not isinstance(columns_to_drop, (list, tuple, set)):
            raise TypeError(
                "🔴 columns_to_drop must be a string or list/tuple/set of strings."
            )
        existing_cols = set(self.df.columns)
        to_drop = [col for col in columns_to_drop if col in existing_cols]
        not_found = [col for col in columns_to_drop if col not in existing_cols]
        if not to_drop:
            print("🔺 No matching columns found to drop.")
        else:
            self.df.drop(columns=to_drop, inplace=True)
            print(f"🟢 Dropped columns: {to_drop}")
        if not_found:
            print(
                f"🔺 These columns were not found in the DataFrame and were skipped: {not_found}"
            )
        return self
    
    def set_index_column(self, column_name):
        if column_name not in self.df.columns:
            raise ValueError(f"🔴 Column '{column_name}' not found in the DataFrame.")
        
        if self.df.index.name == column_name:
            print(f"🔹 Column '{column_name}' is already the index.")
            return self

        self.df.set_index(column_name, inplace=True)
        print(f"🟢 Column '{column_name}' set as index.")
        return self

    def set_index_date(
        self,
        index_column,
        log_invalid=False,
        log_path="invalid_datetime_rows.csv",
        check_index=True,
        force_plain_date=False,
    ):

        # 0. If already index, skip re-indexing
        if self.df.index.name == index_column:
            print(f"🔺 Column '{index_column}' is already set as index.")
            if check_index:
                self.check_index_is_datetime()
            return self

        # 1. Check if column exists
        if index_column not in self.df.columns:
            raise ValueError(f"🔴 Column '{index_column}' not found in the DataFrame.")

        # 2. Convert to datetime if not already
        if not pd.api.types.is_datetime64_any_dtype(self.df[index_column]):
            self.df[index_column] = pd.to_datetime(
                self.df[index_column], errors="coerce"
            )
            print(f"🟢 Column '{index_column}' converted to datetime.")

        # 3. Check for all NaT values
        if self.df[index_column].isna().all():
            print(f"🔴 All values in '{index_column}' are NaT. Cannot set as index.")
            return self

        # 4. Log invalid datetime values
        invalid_rows = self.df[self.df[index_column].isna()]
        num_invalid = len(invalid_rows)
        if num_invalid > 0:
            print(
                f"🔺 {num_invalid} rows in '{index_column}' could not be converted to datetime (set as NaT)."
            )
            if log_invalid:
                invalid_rows.to_csv(log_path, index=False)
                print(f"🔸 Invalid datetime rows saved to: {log_path}")

        # 5. Format date vs datetime
        non_na_values = self.df[index_column].dropna()
        sample_value = non_na_values.iloc[0]

        if isinstance(sample_value, date) and not isinstance(sample_value, datetime):
            print(f"🟢 Column '{index_column}' is already in date format (YYYY-MM-DD).")
        else:
            if force_plain_date:
                print(
                    f"🟢 force_plain_date=True — converting '{index_column}' to plain date."
                )
                self.df[index_column] = self.df[index_column].dt.date
            else:
                if hasattr(sample_value, "time") and sample_value.time() == time(0, 0):
                    print(
                        f"🟢 Column '{index_column}' appears to be date-only — converting to plain date."
                    )
                    self.df[index_column] = self.df[index_column].dt.date
                else:
                    print(
                        f"🟢 Column '{index_column}' contains time — normalizing to 00:00:00."
                    )
                    self.df[index_column] = self.df[index_column].dt.normalize()

        # 6. Warn about duplicate index values
        if self.df[index_column].duplicated().any():
            print(
                f"🔴 Warning: '{index_column}' contains duplicate values — consider handling them before indexing."
            )

        # 7. Set the index
        if index_column not in self.df.columns:
            print(f"🔴 Column '{index_column}' no longer exists. Cannot set as index.")
            return self

        self.df.set_index(index_column, inplace=True)
        print(f"🟢 Index set to column: '{index_column}'")

        # 8. Check if index is datetime or date
        if check_index:
            self.check_index_is_datetime()

        return self

    def check_index_is_datetime(self):
        if self.df.index.empty:
            print("🔴 Index is empty — cannot determine index type.")
            return False

        first_index_value = self.df.index[0]

        if isinstance(first_index_value, pd.Timestamp):
            print("🟢 Index is of type pandas Timestamp (datetime64).")
            return True
        elif isinstance(first_index_value, datetime):
            print("🟢 Index is of type datetime.datetime.")
            return True
        elif isinstance(first_index_value, date):
            print("🟢 Index is of type datetime.date.")
            return True
        else:
            print(
                f"🔴 Index is not datetime or date. Detected type: {type(first_index_value)}"
            )
            return False

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

    def handle_missing_values(self, strategy="mean"):
        initial_missing = self.df.isnull().sum().sum()

        if initial_missing == 0:
            print("🟢 No missing values to handle.")
            return self

        numerical_cols = self.df.select_dtypes(include=["int64", "float64"]).columns
        categorical_cols = self.df.select_dtypes(include=["object"]).columns

        if strategy == "mean":
            self.df[numerical_cols] = self.df[numerical_cols].fillna(
                self.df[numerical_cols].mean()
            )
            print(
                f"🔸 Filled missing numeric values using mean in columns: {list(numerical_cols)}"
            )

        elif strategy == "median":
            self.df[numerical_cols] = self.df[numerical_cols].fillna(
                self.df[numerical_cols].median()
            )
            print(
                f"🔸 Filled missing numeric values using median in columns: {list(numerical_cols)}"
            )

        elif strategy == "most_frequent":
            if categorical_cols.empty:
                print("🟢 No categorical columns found to fill.")
            else:
                try:
                    mode = self.df[categorical_cols].mode().iloc[0]
                    self.df[categorical_cols] = self.df[categorical_cols].fillna(mode)
                    print(
                        f"🔸 Filled missing categorical values using mode in columns: {list(categorical_cols)}"
                    )
                except IndexError:
                    print(
                        "🔺 Could not compute mode — no non-null values in categorical columns."
                    )

        elif strategy == "drop":
            before_drop = len(self.df)
            self.df.dropna(inplace=True)
            after_drop = len(self.df)
            print(f"🟢 Dropped rows with missing values: {before_drop - after_drop}")

        else:
            raise ValueError(
                "🔴 Invalid strategy. Choose from: 'mean', 'median', 'drop', or 'most_frequent'."
            )

        # Automatic re-check
        remaining_missing = self.df.isnull().sum().sum()
        if remaining_missing == 0:
            print("🟢 All missing values handled.")
        else:
            print(
                f"🔴 {remaining_missing} missing values still remain after applying strategy '{strategy}'."
            )
        return self

    def inspect_duplicates(self, subset=None, keep=False, return_rows=False):
        dups = self.df[self.df.duplicated(subset=subset, keep=keep)]
        num_dups = len(dups)

        if num_dups > 0:
            print(f"🔴 Found {num_dups} duplicate row(s).")
        else:
            print("🟢 No duplicate rows found.")

        if return_rows:
            return num_dups, dups
        else:
            return num_dups

    def handle_duplicates(self, method="keep_first"):
        duplicates = self.df.duplicated()
        num_duplicates = duplicates.sum()

        if num_duplicates == 0:
            print("🟢 No duplicate rows to handle.")
            return self

        print(
            f"🔴 Found {num_duplicates} duplicate row(s). Applying method: '{method}'"
        )

        if method == "keep_first":
            self.df.drop_duplicates(keep="first", inplace=True)
            print("🔸 Kept first occurrence of duplicates.")
        elif method == "keep_last":
            self.df.drop_duplicates(keep="last", inplace=True)
            print("🔸 Kept last occurrence of duplicates.")
        elif method == "drop_all":
            self.df = self.df[~duplicates]
            print("🔸 Dropped all duplicate rows.")
        elif method == "flag":
            self.df["is_duplicate"] = duplicates
            print("🔸 Flagged duplicate rows in 'is_duplicate' column.")
        else:
            raise ValueError(f"🔴 Unknown duplicate handling method: '{method}'")
        return self

    def log_duplicates(
        self, subset=None, keep=False, log_dir="logs", filename=None, file_format="csv"
    ):
        duplicates = self.df[self.df.duplicated(subset=subset, keep=keep)]
        num_dups = len(duplicates)

        if num_dups == 0:
            print("🟢 No duplicates found to log.")
            return None

        log_path = Path(log_dir)
        log_path.mkdir(parents=True, exist_ok=True)

        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"🔴 duplicates_log_{timestamp}.{file_format}"
        else:
            filename = (
                f"{filename}.{file_format}"
                if not filename.endswith(f".{file_format}")
                else filename
            )

        file_path = log_path / filename

        if file_format == "csv":
            duplicates.to_csv(file_path, index=False)
        elif file_format == "xlsx":
            duplicates.to_excel(file_path, index=False)
        else:
            raise ValueError("🔴 File_format must be 'csv' or 'xlsx'.")

        print(f"🔴 Logged {num_dups} duplicate rows to: {file_path}")
        return file_path

    def check_outliers(self, z_thresh=2):
        numeric_df = self.df.select_dtypes(include="number")
        print("\n🟢 Numeric columns used for Z-score calculation:")
        print(numeric_df.columns)

        z_scores = numeric_df.apply(zscore)
        print("\n🟢 Sample Z-scores:")
        print(z_scores.head())

        outliers = (z_scores.abs() > z_thresh).sum()
        print("\n🟢 Outliers per column (Z-score > threshold):")
        print(outliers[outliers > 0])
        return outliers

    def remove_outliers_zscore(self, z_thresh=2):
        numeric_df = self.df.select_dtypes(include="number")
        z_scores = numeric_df.apply(zscore)
        mask = (z_scores.abs() < z_thresh).all(axis=1)
        self.df = self.df[mask]
        print(f"🟢 Removed outliers using Z-score threshold = {z_thresh}")
        return self

    def remove_outliers_from_column(self, column, z_thresh=2):
        z = zscore(self.df[column].dropna())
        mask = abs(z) < z_thresh

        filtered_df = self.df.loc[self.df[column].dropna().index[mask]]
        removed = self.df.shape[0] - filtered_df.shape[0]

        if removed > 0:
            print(
                f"\n🔴 Removed {removed} outlier(s) from '{column}' (Z-thresh = {z_thresh})"
            )
        else:
            print(f"\n🟢 No outliers found in '{column}' (Z-thresh = {z_thresh})")

        self.df = filtered_df  # Update the internal DataFrame
        return self

    def remove_outliers_iqr(self, column, iqr_multiplier=1.5):
        if column not in self.df.columns:
            print(f"🔴 Column '{column}' not found in the dataset.")
            return self

        q1 = self.df[column].quantile(0.25)
        q3 = self.df[column].quantile(0.75)
        iqr = q3 - q1

        lower_bound = q1 - iqr_multiplier * iqr
        upper_bound = q3 + iqr_multiplier * iqr

        before_rows = self.df.shape[0]
        self.df = self.df[
            (self.df[column] >= lower_bound) & (self.df[column] <= upper_bound)
        ]
        after_rows = self.df.shape[0]
        removed = before_rows - after_rows

        if removed > 0:
            print(
                f"\n🔴 Removed {removed} outlier(s) from '{column}' using IQR (multiplier={iqr_multiplier})"
            )
        else:
            print(
                f"\n🟢 No outliers found in '{column}' using IQR (multiplier={iqr_multiplier})"
            )
        return self

    def get_processed_data(self):
        # Returns the processed DataFrame.
        return self.df

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

        sns.histplot(
            original_df[column],
            kde=True,
            color="salmon",
            label="Before",
            stat="density",
        )
        sns.histplot(
            cleaned_df[column],
            kde=True,
            color="lightgreen",
            label="After",
            stat="density",
        )

        plt.title(f"Distribution of '{column}' Before and After Z-Score Cleaning")
        plt.xlabel(column)
        plt.ylabel("Density")
        plt.legend()
        plt.tight_layout()
        plt.show()

    def run_all_checks(self):
        print("\n🔹 Running data quality checks...")
        self.check_missing()
        self.inspect_duplicates()
        self.check_dtypes()
        self.check_index_is_datetime()
        return self

    def save(self, path, format="csv"):
        if format == "csv":
            self.df.to_csv(path)
        elif format == "xlsx":
            self.df.to_excel(path)
        else:
            raise ValueError("🔴 Unsupported format. Use 'csv' or 'xlsx'.")
        print(f"🟢 Data saved to {path}")
        return self
