from __future__ import division
import numpy as np
import pandas as pd
import glob
import os

def summary_hospitalieres(file):
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
    for c in data.columns:
        if c not in ['dep', 'sexe', 'jour']:
            cum_data = data.groupby('jour')[c].sum().to_numpy()
            # Assign relevant summarized column to storage df
            new_df[c] = cum_data
    return new_df

def summary_tests_old(file):
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

def summary_tests(file):
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
    mat.tofile(fname, sep=';')
    if len(deps) != 0:
        meta_fname = fname.replace('.csv', '_META.csv', 1)
        with open(meta_fname, 'w') as out:
            out.write(';'.join(deps)+'\n')