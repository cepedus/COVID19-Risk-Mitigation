from __future__ import division
import numpy as np
import pandas as pd
import glob
import os

def french_datify(s, year):
    d, m = s.split('-')
    if m == 'mars':
        m = '03'
    elif m == 'avr.':
        m = '04'
    elif m == 'mai':
        m = '05'
    elif m == 'juin':
        m = '06'
    elif m == 'juil.':
        m = '07'
    return '-'.join([year, m, d])

def deaths_INSEE(file, y):
    # Open CSV and keep only national-yearwise data
    data = pd.read_csv(file, sep=";",header=0)
    data = data[data.Zone == 'France']
    keep_cols = [c for c in data.columns if 'Total' in c or 'Date' in c]
    data = data.drop([c for c in data.columns if c not in keep_cols], axis=1)
    # Rename columns accordingly
    col_names = []
    for c in keep_cols:
        if 'Total' in c:
            col_names.append(c.split('_')[-1])
        else:
            col_names.append('date')
    data.columns = col_names
    # Keep only one year
    year = str(y)
    data['date'] = data['date'].apply(lambda s: french_datify(s, year))
    data = data.drop([c for c in data.columns if c not in ['date', year]], axis=1)
    data.columns = ['date', 'D_total']
    data = data.reset_index(drop=True)
    return data

def hospitalieres_departments(file):
    """
    Creates database for department columns
    """
    # Open CSV & create df with present dates
    data = pd.read_csv(file, sep=";",header=0)
    data['dep'] = data['dep'].apply(lambda x: str(x))
    new_df = pd.DataFrame()
    dates= data['jour'].unique()
    #Extract list of departments
    deps = list(data['dep'].unique())
    deps.pop(-1) # delete 'nan' element
    new_df['date'] = dates
    data = data[data['sexe'] == 0]
    # For relevant columns (hospitalized, dead, sent to home, in reanimation) get columns for all departments
    for d in deps:
        for c in ['hosp', 'rea', 'rad', 'dc']:
            dep_data = data[data['dep'] == d][c].to_numpy() 
            col_name = d + '_' + c
            new_df[col_name] = dep_data
    return new_df
    
def hospitalieres_summary(file):
    """
    Creates national summary database from daily hospitary data per department
    """
    # Open CSV & create df with present dates
    data = pd.read_csv(file, sep=";",header=0)
    new_df = pd.DataFrame()
    dates= data['jour'].unique()
    new_df['date'] = dates
    # Filter data: separate male & female 
    data = data[data['sexe'] != 0]
    # For relevant columns (hospitalized, dead, sent to home, in reanimation) sum for all departments in a given day
    for c in ['hosp', 'rea', 'rad', 'dc']:
        cum_data = data.groupby('jour')[c].sum().to_numpy()
        # Assign relevant summarized column to storage df
        new_df[c] = cum_data
    return new_df

def tests_old_departments(file):
    """
    Creates database for department columns
    """
    # Open CSV & create df with present dates
    data = pd.read_csv(file, sep=";",header=0)
    data['dep'] = data['dep'].apply(lambda x: str(x))
    new_df = pd.DataFrame()
    dates= data['jour'].unique()
    #Extract list of departments
    deps = list(data['dep'].unique())
    new_df['date'] = dates   
    # Filter by age group: consider cumulated data
    filtered = data[data['clage_covid'] == '0']    
    # Add columns for total tests & positive tests per departments
    for d in deps:
        col_name = d + '_' + 'oldP'
        new_df[col_name] = filtered[filtered['dep'] == d]['nb_pos'].to_numpy()
        col_name = d + '_' + 'oldT'
        new_df[col_name] = filtered[filtered['dep'] == d]['nb_test'].to_numpy()    
    return new_df


def tests_old_summary(file):
    """
    Creates national summary database from daily test data per department
    """
    # Open CSV & create df with present dates
    data = pd.read_csv(file, sep=";",header=0)
    new_df = pd.DataFrame()
    dates= data['jour'].unique()
    new_df['date'] = dates    
    # Filter by age group: consider cumulated data
    filtered = data[data['clage_covid'] == '0']    
    # Add columns for total tests & positive tests per day summed for all departments
    series = filtered.groupby('jour')['nb_pos'].sum().to_numpy()
    new_df['positive_tests_old'] = series
    series = filtered.groupby('jour')['nb_test'].sum().to_numpy()
    new_df['total_tests_old'] = series    
    return new_df

def tests_departments(file):
    """
    Creates national summary database from daily test data per department
    """
    # Open CSV & create df with present dates
    data = pd.read_csv(file, sep=",",header=0)
    data['dep'] = data['dep'].apply(lambda x: str(x))
    new_df = pd.DataFrame()
    dates= data['jour'].unique()
    #Extract list of departments
    deps = list(data['dep'].unique())
    new_df['date'] = dates
    # Filter by age group: consider cumulated data
    filtered = data[data['cl_age90'] == 0]
    # Add columns for total tests & positive tests per departments
    for d in deps:
        col_name = d + '_' + 'oldP'
        new_df[col_name] = filtered[filtered['dep'] == d]['p'].to_numpy()
        col_name = d + '_' + 'oldT'
        new_df[col_name] = filtered[filtered['dep'] == d]['t'].to_numpy() 
    
    # Open aux CSV to get popupations
    pops_file = file.replace('sp-pos-quot', 'sp-pe-tb-quot')
    deps_df = pd.read_csv(pops_file, sep=",",header=0)
    # Get population of every indexed department
    deps_df = deps_df[deps_df['cl_age90'] == 0].groupby('dep')['pop'].unique()
    #Create dict of population attributes per deparment
    deps_sizes = {}
    deps = deps_df.index.to_numpy()
    for d in deps:
        deps_sizes[d] = deps_df[d][0]
    return new_df, deps_sizes

def tests_summary(file):
    """
    Creates national summary database from daily test data per department
    """
    # Open CSV & create df with present dates
    data = pd.read_csv(file, sep=",",header=0)
    new_df = pd.DataFrame()
    dates= data['jour'].unique()
    new_df['date'] = dates
    # Filter by age group: consider cumulated data
    filtered = data[data['cl_age90'] == 0]
    # Add columns for total tests & positive tests per day summed for all departments
    series = filtered.groupby('jour')['p'].sum().to_numpy()
    new_df['positive_tests'] = series
    series = filtered.groupby('jour')['t'].sum().to_numpy()
    new_df['total_tests'] = series
    # Open aux CSV to get popupations
    pops_file = file.replace('sp-pos-quot', 'sp-pe-tb-quot')
    deps_df = pd.read_csv(pops_file, sep=",",header=0)
    # Get population of every indexed department
    deps_df = deps_df[deps_df['cl_age90'] == 0].groupby('dep')['pop'].unique()
    #Create dict of population attributes per deparment
    deps_sizes = {}
    deps = deps_df.index.to_numpy()
    for d in deps:
        deps_sizes[d] = deps_df[d][0]
    return new_df, deps_sizes

def extract_owid(file):
    """
    Extracts France data from OWID database, creates country attributes from single-valued columns
    """
    # Open, country-filter & relevant column-filer data
    data = pd.read_csv(file, sep=",",header=0)
    data = data[data['iso_code'] == 'FRA']
    cols = ['date', 'total_cases', 'total_deaths', 'stringency_index', 
            'population','gdp_per_capita',
           'cvd_death_rate', 'diabetes_prevalence', 'female_smokers',
           'male_smokers', 'hospital_beds_per_thousand']
    # Drop unnecesary columns
    data = data.drop([c for c in data.columns if c not in cols], axis=1)
    # Get single-valued columns to return as country attribute
    uniques = unique_columns(data)
    attrs = {}
    for col in uniques:
        attrs[col] = data[col].iloc[0]
    # Drop single-valued columns
    data = data.drop(uniques, axis=1)
    return data, attrs

def unique_columns(df):
    """Return name of columns with an unique value"""
    return [c for c in df.columns if len(df[c].unique()) == 1]

def single_valued_dict_csv(dic, file):
    """
    Saves single-valued dictionary to csv file 
    """
    keys = list(dic.keys())
    vals = [str(dic[k]) for k in keys]
    with open(file, 'w') as out:
        out.write(', '.join(keys) + '\n')
        out.write(', '.join(vals) + '\n')
        
def mobility_matrix(file, source='school'):
    """
    Computes mobility matrices for mobility tables (Recensement de la population 2016) based on individual weights of
    registered households. Returns also array of departmental keys per row/column
    """
    # Input check
    if source not in ['school', 'work']:
        print('Not a valid source')
        return np.zeros(1)
    # Open CSV as all strings
    data = pd.read_csv(file, sep=";",header=0, dtype=object)
    # Restrict to Metropolitan France & not-frontalière
    mask = (data.METRODOM =='M')
    if source == 'school':
        mask &= (data.DCETUE == '99999')
    elif source == 'work':
        mask &= (data.DCFLT == '99999')
    # Filter
    data = data[mask]
    # Extract departments
    data['DEP_ORIG'] = data.COMMUNE.apply(lambda x: x[:2]) # this column is restricted to Metropolitan France
    if source == 'school':
        data['DEP_DEST'] = data.DCETUF.apply(lambda x: x[:2])
    elif source == 'work':
        data['DEP_DEST'] = data.DCLT.apply(lambda x: x[:2])
    # Drop unnecesary columns: keep only origin, destination & weight
    keep_cols = ['DEP_ORIG', 'DEP_DEST', 'IPONDI']
    data = data.drop([c for c in data.columns if c not in keep_cols], axis=1)
    # Numerize weights
    data['IPONDI'] = pd.to_numeric(data['IPONDI'])
    # Department list
    deps = list(data['DEP_ORIG'].unique())
    # Create & fill mobility matrix
    mob_matrix = np.zeros((len(deps), len(deps)))
    for i in range(len(deps)):
        # Sum "Poids de l'individu" per origin department 
        orig = deps[i]
        series = data[data['DEP_ORIG'] == orig].groupby('DEP_DEST')['IPONDI'].sum()
        # Check they're in metropolitan France
        for dest in list(series.index):
            try:
                j = deps.index(dest)
            except ValueError:
                continue
            # Assign summed interactions
            mob_matrix[i, j] = series[dest]
        # Normalize per row: per origin department
        mob_matrix[i,:] /= mob_matrix[i,:].sum()
    return mob_matrix, deps

def save_matrix(fname, mat, deps=[]):
    """
    Saves mobility matrix and dep list indexes to path
    """
    np.savetxt(fname, mat, delimiter=',',newline='\n')
    if len(deps) != 0:
        meta_fname = fname.replace('.csv', '_META.csv', 1)
        with open(meta_fname, 'w') as out:
            out.write(';'.join(deps)+'\n')