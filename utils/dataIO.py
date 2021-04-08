# For csv file r/w manipulation
# This code is written by Steven HH Chen.

# Python internal module import

# Python external module import
import pandas as pd
from loguru import logger

# User module import

# Read dataset
@logger.catch
def read_csv_to_pandas_df(filename, colname):
    return pd.read_csv(filename, low_memory=False, names=colname)


