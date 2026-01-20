import pandas as pd
import glob
import os

def load_csv_files(directory_pattern, dataset_type='enrolment'):
    """Load and concatenate all CSV files matching the directory pattern with optimized memory."""
    files = glob.glob(directory_pattern)
    if not files:
        print(f"No files found for pattern: {directory_pattern}")
        return pd.DataFrame()
    
    # Define optimal dtypes for memory and speed
    # Note: pincode must be string to preserve leading zeros and avoid mixed-type issues
    dtype_map = {
        'state': 'category',
        'district': 'category',
        'pincode': str
    }
    
    # Specific numeric columns for each dataset
    if dataset_type == 'enrolment':
        dtype_map.update({'age_0_5': 'int32', 'age_5_17': 'int32', 'age_18_greater': 'int32'})
    elif dataset_type == 'demographic':
        dtype_map.update({'demo_age_5_17': 'int32', 'demo_age_17_': 'int32'})
    elif dataset_type == 'biometric':
        dtype_map.update({'bio_age_5_17': 'int32', 'bio_age_17_': 'int32'})
    
    df_list = []
    for file in files:
        # engine='c' is default and fast; low_memory=False avoids warnings
        df = pd.read_csv(file, dtype=dtype_map, low_memory=False)
        df_list.append(df)
    
    return pd.concat(df_list, ignore_index=True)

def load_enrollment_data(base_path='.'):
    pattern = os.path.join(base_path, 'api_data_aadhar_enrolment', '*.csv')
    return load_csv_files(pattern, 'enrolment')

def load_demographic_data(base_path='.'):
    pattern = os.path.join(base_path, 'api_data_aadhar_demographic', '*.csv')
    return load_csv_files(pattern, 'demographic')

def load_biometric_data(base_path='.'):
    pattern = os.path.join(base_path, 'api_data_aadhar_biometric', '*.csv')
    return load_csv_files(pattern, 'biometric')

def merge_all_datasets(enr_df, demo_df, bio_df):
    """Merge enrollment, demographic, and biometric datasets on key columns with optimized grouping."""
    key_cols = ['state', 'district', 'pincode']
    
    # Aggregating with numeric_only=True is CRITICAL for speed (stops string concatenation)
    enr_agg = enr_df.groupby(key_cols).sum(numeric_only=True).reset_index()
    demo_agg = demo_df.groupby(key_cols).sum(numeric_only=True).reset_index()
    bio_agg = bio_df.groupby(key_cols).sum(numeric_only=True).reset_index()
    
    # Basic merge
    merged = pd.merge(enr_agg, demo_agg, on=key_cols, how='outer', suffixes=('_enr', '_demo'))
    merged = pd.merge(merged, bio_agg, on=key_cols, how='outer', suffixes=('', '_bio'))
    
    return merged
