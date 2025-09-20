from processor import DataProcessor

file_path = '/your_path/foo_sales_dataset.csv'
target_col = 'TOTAL_SALES'

# Load data and create a processor data frame object 
processor = DataProcessor(filepath=file_path).load()

#print(type(processor.df))

# Helps visualize a comparison between before and after leverage Z-score threshold data transformation
original_df = processor.df.copy()

# Show head of the data
print("\n🔹 First 5 rows:")
print(processor.df.head())

# Show tail of the data
print("\n🔹 Last 5 rows:")
print(processor.df.tail())

#print(f"\n🔹 Number of rows in the dataset: {processor.df.shape[0]}")
print(f"\n🔹 Number of rows and columns in the dataset: {processor.df.shape}")

print("\n🔹 Check for Data Types:")
processor.check_dtypes()

# Check for categorical columns
print("\n🔹 Check for categorical columns:")
processor.check_categorical_columns()

#print("\n🔹 Drop unused columns:")
#processor.drop_columns([])
'''
print("\n🔹 Set column ID as an Index:")
processor.set_index_column('ID')

print("\n🔹 Set column Date as an Index:")
#processor.set_index_date('ID')
processor.set_index('DATE', log_invalid=True, check_index=False)

print("\n🔹 Checking if Date is an Index:")
processor.check_index_is_datetime()

#print("\n🔹 Filtering by date range:")
#processor.filter_by_date_range("2025-03-01", "2025-06-30")

# Check missing values
print("\n🔹 Missing values check:")
processor.check_missing()

# Hnndle missing values
print("\n🔹 Handle missing values:")
processor.handle_missing_values('mean')

print("\n🔹 Check for duplicate rows in DataFrame:")
if processor.inspect_duplicates(subset=None, keep=False, return_rows=False) > 0:
    print("\n🔹 Make log file for duplicates:")
    processor.log_duplicates()
    
    print("\n🔹 Handling duplicate rows:")
    processor.handle_duplicates(method="keep_first")

print("\n🔹Basic Statistics:")
print(processor.df.describe())

print("\n🔹 Check for outliers:")
processor.check_outliers()

print("\n🔹Removing outliers from specific column according to z_score")
processor.remove_outliers_from_column('TOTAL_SALES', z_thresh=1)

#print("\n🔹 Remove outliers with IQR method:")
#processor.remove_outliers_iqr('TOTAL_SALES', iqr_multiplier=1.5)
	
print(f"\n🔹 Number of rows after outlier removal: {processor.df.shape[0]}")

# Show preprocessed data
print("\n🔹Preprocessed data (top 5 rows):")
#print(processor.get_processed_data().head())
print(processor.get_processed_data())

print("\n🔹Visualize data before and after handling outliers:")
processor.visualize_outliers_boxplot(original_df, processor.df, 'TOTAL_SALES')
processor.visualize_outliers_histogram(original_df, processor.df, 'TOTAL_SALES')

print("\n🔹Saving to file:")
processor.save(path="/your_path/data/processed_data.xlsx", format="xlsx")
'''
