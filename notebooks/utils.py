import pandas as pd
import re

def read_file(filepath): 
    data = pd.read_excel(filepath)
    return data

def clean_text(data):

    if isinstance(data, str):
        clean = re.sub(r'\([^)]*\)', '', data)
        clean = re.sub("\D","",clean)
        
        return clean

    else:
        return data

def read_and_clean_data(filepath):

    # Load the excel file
    dataset = read_file(filepath)

    # Get categorical variable
    tot_cols = dataset.columns
    num_cols = dataset._get_numeric_data().columns
    cat_cols = list(set(tot_cols)-set(num_cols))

    # Drop columns
    drop_cols = ['NDB_No', 'Shrt_Desc']
    dataset = dataset.drop(drop_cols, axis=1)

    # Remove text in GmWt_Desc2 and GmWt_Desc1
    try:
        try:
            dataset[cat_cols[0]] = dataset[cat_cols[0]].apply(clean_text)
            dataset[cat_cols[1]] = dataset[cat_cols[1]].apply(clean_text)
        except:
            dataset[cat_cols[1]] = dataset[cat_cols[1]].apply(clean_text)
            dataset[cat_cols[2]] = dataset[cat_cols[2]].apply(clean_text)
    except:
        dataset[cat_cols[0]] = dataset[cat_cols[0]].apply(clean_text)
        dataset[cat_cols[2]] = dataset[cat_cols[2]].apply(clean_text)

    # Fill missing data with median
    get_median = dataset.median()
    dataset = dataset.fillna(get_median)

    return dataset

def split_X_y(dataset):

    # Getting the labels
    labels = ['Calcium_(mg)', 'Iron_(mg)','Zinc_(mg)', 
    'Vit_A_IU', 'Vit_D_IU', 'Folate_Tot_(µg)']

    # List of names of the columns that we will drop for the input data
    drop_cols = ['Vit_D_µg', 'Vit_A_RAE'] + labels

    # Get the data for labels
    y = dataset[labels].values

    # Get the data for inputs
    X = dataset.drop(drop_cols, axis=1).values

    return X, y