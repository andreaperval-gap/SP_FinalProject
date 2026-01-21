"""Contains all functions related to preprocessing the data. """

# To run the whole preprocessing just run the last function preprocess_df()

import numpy as np
import pandas as pd
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

new_columns = [
        "age",
        "blood_pressure",
        "specific_gravity",
        "albumin",
        "sugar",
        "rbc",
        "pus_cell",
        "pus_clumps",
        "bacteria",
        "glucose",
        "urea",
        "creatinine",
        "sodium",
        "potassium",
        "hemoglobin",
        "pcv",
        "wbc",
        "rbc_count",
        "hypertension",
        "diabetes",
        "coronary_disease",
        "appetite",
        "edema",
        "anemia",
        "ckd"
    ]

categorical_columns = [
        "rbc",
        "pus_cell",
        "pus_clumps",
        "bacteria",
        "hypertension",
        "diabetes",
        "coronary_disease",
        "appetite",
        "edema",
        "anemia",
        "ckd", 
        "specific_gravity",
        "albumin",
        "sugar",
    ]

numerical_columns = [
    "age",
    "blood_pressure",
    "glucose",
    "urea",
    "creatinine",
    "sodium",
    "potassium",
    "hemoglobin",
    "pcv",
    "wbc",
    "rbc_count"
]

# categorical (numerical categories, e.g. "1.0", "1.05", "1.1")
#        "specific_gravity",
#        "albumin",
#        "sugar",


def rename_columns(df,new_columns=new_columns):
    """Renames the columns of the dataframe with the names given
    
    The column names will be matched in order. 

    Args:
        df: a dataframe
        new_columns: a list of the new column names

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

def columns_to_numeric(df, numerical_columns=numerical_columns):
    """Converts the given columns to numeric. 
    
    Args: 
        df: a dataframe
        numerical_columns: a list of the column names to be converted
    
    Returns: 
        The dataframe with the columns converted to numeric
    """

    # Convert selected columns to numeric types
    for col in numerical_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df

def cleaning_categorical_columns(df,categorical_cols=categorical_columns):
    """Cleans the formatting of the categorical columns of the dataframe
    
    Args: 
        df: a dataframe
    
    Returns: 
        The dataframe with the column values cleaned. 
    """

    # Strip leading/trailing whitespace from all string values in these columns
    df[categorical_columns] = df[categorical_columns].map(lambda x: x.strip() if isinstance(x, str) else x)

    return df

def remove_outliers(df):
    """Remove outliers from the dataset. 
    
    The method to select these outliers is visual inspection of pair plots plus
    knowledge of the expected values of the variables. The reasoning can be
    found in Scientific_Programming.ipynb in Task 2. 
    
    Args: 
        df: a dataframe
    
    Returns: 
        The dataframe without the ouliers
    """ 
    idxs = df[(df["sodium"] < 5) | (df["potassium"] > 20)].index
    no_outliers_df = df.drop(labels=idxs,inplace=False).reset_index(drop=True)
    return no_outliers_df

def normalize_df(df, numerical_columns=numerical_columns):
    """Normalizes the numerical columns in the df using 0-1 normalization.
    
    Args: 
        df: a dataframe
        numerical_columns: a list of the numeric column names
    
    Returns:
        The dataframe with its numerical columns normalized
    """

    df[numerical_columns] = (df[numerical_columns]-df[numerical_columns].min()) / \
    (df[numerical_columns].max()-df[numerical_columns].min())
    return df

def impute_numerical(df,numerical_columns=numerical_columns,method="lr"):
    """Imputes the missing values of numerical columns in the dataframe. 
    
    The method used is multiple imputation (MICE) with linear regression (lr) or 
    a random forest classifier (rf). 
    
    Args: 
        df: a dataframe
        numerical_columns: a list of the numeric column names
        method: the method to be used for imputation. Either "lr" or "rf". 
    """
    if method == "lr":
        estimator = LinearRegression()
    if method == "rf":
        estimator = RandomForestRegressor(n_estimators=100)

    # We create the imputer
    imp = IterativeImputer(estimator=estimator, verbose=2, max_iter=10)#, tol=1e-10, imputation_order='roman')
    # Apply it to the numerical columns
    ImputedData = imp.fit_transform(df[numerical_columns])
    # Convert the imputed values to a dataframe
    Imputed_data = pd.DataFrame(ImputedData)
    Imputed_data.columns = numerical_columns
    # Substitute the imputed values into the dataframe
    # Copy is not necessary, for the time being I keep it to not modify existing dfs
    imp_df = df.copy()
    imp_df[numerical_columns] = Imputed_data
    return imp_df

def preprocess_df(df, new_columns=new_columns, numerical_columns=numerical_columns):
    """Peforms data cleaning on the dataframe. 
    
    This is the entire data cleaning pipeline.

    Args: 
        df: a dataframe
        new_columns: a list of the new column names
        numerical_columns: a list of the numeric column names

    Returns: 
        The cleaned dataframe.
    """
    # Renames all the columns to clearer names
    df = rename_columns(df)
    # Replaces the missing values (default "?") with np.nan
    df = missing_to_nan(df)
    # Converts the numeric columns to numeric type (default object)
    df = columns_to_numeric(df)
    # Cleans the formatting of the categories names in categorical variables
    df = cleaning_categorical_columns(df)
    # Remove outliers
    df = remove_outliers(df)
    # Normalize numerical values 0-1
    df = normalize_df(df)
    return df
