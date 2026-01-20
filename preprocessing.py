"""Contains all functions related to preprocessing the data. """

import numpy as np
import pandas as pd

def rename_columns(df,new_columns):
    """Renames the columns of the dataframe with the names given
    
    The column names will be matched in order. 

    Args:
        df: a dataframe
        new_column: a list of the new column names.  

    Returns: 
        The dataframe with the new column names. 
    """ 

    dict_names = {}
    col_names =df.columns  # passing current column names as a list
    if len(col_names) != len(new_columns):
        raise ValueError("Lists lenght missmatch") # sanity check to ensure we have added all the new columns names
    
    # create mapping dictionary
    dict_names = dict(zip(col_names, new_columns))
    #apply renaming
    renamed_df = df.rename(columns=dict_names)
    #return dictionary to visualize mapping
    return renamed_df


def missing_to_nan(df):
    """Converts the missing values ("?") to np.nan. 
    
    Args: 
        df: a dataframe
    
    Returns: 
        The dataframe with the converted missing values.
    """
    cleaned_df = df.replace("?", np.nan)
    return cleaned_df

def columns_to_numeric(df, numeric_cols):
    """Converts the given columns to numeric. 
    
    Args: 
        df: a dataframe
        numeric_cols: a list of the column names to be converted
    
    Returns: 
        The dataframe with the columns converted to numeric
    """

    # Convert selected columns to numeric types
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df