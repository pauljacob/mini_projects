import pandas as pd
import os

def p(df_):
    """
    Return the first 5 and last 5 rows of this DataFrame df_ as the DataFrame for display.
    
    Args:
        df_ (DataFrame): The DataFrame to be operated on.
        
    Returns:
        The concatenated head and tail of the DataFrame df_.
    """
    if df_.shape[0] > 6:
        print(df_.shape)
        return pd.concat([df_.head(), df_.tail()])
    else:
        return df_

def rcr(file_, pd_=None):
    """Read the filename from relative the relative directory '../raw_data'
    
    Args:
        file_ (str): The name of the file.
    Returns:
        The DataFrame at the relative filename path.
    """
    if pd_ == None:
        return pd.read_csv(os.path.join('..', 'raw_data', file_))
    else:
        return pd.read_csv(os.path.join('..', 'raw_data', file_), parse_dates=pd_)
    

    

    
#################################################################################################################################
#Data Wrangling Functions
#################################################################################################################################

def clean_the_DataFrame(df):
    """Clean the DataFrame df column names and values and then return the cleaned DataFrame df.
    
    Args:
        df (DataFrame): The DataFrame df to be cleaned.
    
    Returns:
        df (DataFrame): The cleaned DataFrame df.
    """
    
    #feature column name rename
    column_name_list=['age', 'workclass', 'fnlwgt', 'education', 'educational-num', 'marital-status', 'occupation', 'relationship', 'race', 'gender', 'capital-gain', 'capital-loss', 'hours-per-week', 'native-country', 'income',]
    column_name_list_renamed=['Age', 'Work class', 'Final weight', 'Education', 'Educational number', 'Marital status', 'Occupation', 'Relationship', 'Race', 'Gender', 'Capital gain', 'Capital loss', 'Hours per week', 'Native country', 'Income',]
    column_name_dictionary=dict(zip(column_name_list, column_name_list_renamed))
    df=df.rename(columns=column_name_dictionary)

    #replace target column name 'Income' values '<=50K' with '≤50K'.
    df.loc[:, 'Income']=df.loc[:, 'Income'].replace({'<=50K':'≤50K'})

    #extract feature column name 'Age group' from feature column name 'age'
    bin_list = [16, 19, 24, 29, 34, 39, 44, 49, 54, 59, 64, 69, 74, 79, 84, 89, 94, 99]
    label_list=['17-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64','65-69', '70-74', '75-79', '80-84', '85-89', '90-94', '95-99']
    df.loc[:, 'Age group'] = pd.cut(x=df.loc[:, 'Age'], bins=bin_list, labels=label_list)

    #replace feature column name 'Work class' value '?' with 'Unknown'
    df.loc[:, 'Work class']=df.loc[:, 'Work class'].replace({'?':'Unknown'})

    #replace feature column name 'Education' values with more explicit values
    feature_column_name_education_value_list=['Preschool', '1st-4th', '5th-6th', '7th-8th', '9th', '10th', '11th', '12th', 'HS-grad', 'Some-college', 'Assoc-voc', 'Assoc-acdm', 'Bachelors', 'Masters', 'Prof-school', 'Doctorate']
    feature_column_name_education_value_list_renamed=['Preschool', '1st-4th grade', '5th-6th grade', '7th-8th grade', '9th grade', '10th grade', '11th grade', '12th grade', 'High school graduate', 'Some college', 'Associates vocational', 'Associates academic', 'Bachelors', 'Masters', 'Professional school', 'Doctorate']
    feature_column_name_education_value_dictionary=dict(zip(feature_column_name_education_value_list, feature_column_name_education_value_list_renamed))
    df.loc[:, 'Education']=df.loc[:, 'Education'].replace(feature_column_name_education_value_dictionary)

    #replace feature column name 'Marital status' values with more explicit values
    feature_column_name_marital_status_value_list=['Never-married', 'Married-civ-spouse', 'Widowed', 'Divorced', 'Separated', 'Married-spouse-absent', 'Married-AF-spouse']
    feature_column_name_marital_status_value_list_renamed=['Never married', 'Married civilian spouse', 'Widowed', 'Divorced', 'Separated', 'Married spouse absent', 'Married armed forces spouse']
    feature_column_name_marital_status_value_dictionary=dict(zip(feature_column_name_marital_status_value_list, feature_column_name_marital_status_value_list_renamed))
    df.loc[:, 'Marital status']=df.loc[:, 'Marital status'].replace(feature_column_name_marital_status_value_dictionary)

    #replace feature column name 'Occupation' values with more explicit values
    feature_column_name_occupation_value_list=['Machine-op-inspct', 'Farming-fishing', 'Protective-serv', '?', 'Other-service', 'Prof-specialty', 'Craft-repair', 'Adm-clerical', 'Exec-managerial', 'Tech-support', 'Sales', 'Priv-house-serv', 'Transport-moving', 'Handlers-cleaners', 'Armed-Forces']
    feature_column_name_occupation_value_list_renamed=['Machine operator/inspector', 'Farming/fishing', 'Protective services', 'Unknown', 'Other service', 'Professional specialty', 'Craft/repair', 'Administrative/clerical', 'Executive/managerial', 'Tech support', 'Sales', 'Private house services', 'Transport/moving', 'Handlers/cleaners', 'Armed Forces']
    feature_column_name_occupation_value_dictionary=dict(zip(feature_column_name_occupation_value_list, feature_column_name_occupation_value_list_renamed))
    df.loc[:, 'Occupation']=df.loc[:, 'Occupation'].replace(feature_column_name_occupation_value_dictionary)

    #replace feature column name 'Relationship' values with more explicit values
    feature_column_name_relationship_value_list=['Own-child', 'Husband', 'Not-in-family', 'Unmarried', 'Wife', 'Other-relative']
    feature_column_name_relationship_value_list_renamed=['Own child', 'Husband', 'Not in family', 'Unmarried', 'Wife', 'Other relative']
    feature_column_name_relationship_value_dictionary=dict(zip(feature_column_name_relationship_value_list, feature_column_name_relationship_value_list_renamed))
    df.loc[:, 'Relationship']=df.loc[:, 'Relationship'].replace(feature_column_name_relationship_value_dictionary)

    #replace feature column name 'Race' values with more explicit values
    feature_column_name_race_value_list=['Black', 'White', 'Asian-Pac-Islander', 'Other', 'Amer-Indian-Eskimo']
    feature_column_name_race_value_list_renamed=['Black', 'White', 'Asian/Pacific Islander', 'Other', 'American Indian/Eskimo']
    feature_column_name_relationship_value_dictionary=dict(zip(feature_column_name_race_value_list, feature_column_name_race_value_list_renamed))
    df.loc[:, 'Race']=df.loc[:, 'Race'].replace(feature_column_name_relationship_value_dictionary)

    #replace feature column name 'Native country' values with more human interpretable values
    feature_column_name_native_country_value_list=['United-States', '?', 'Peru', 'Guatemala', 'Mexico', 'Dominican-Republic', 'Ireland', 'Germany', 'Philippines', 'Thailand', 'Haiti', 'El-Salvador', 'Puerto-Rico', 'Vietnam', 'South', 'Columbia', 'Japan', 'India', 'Cambodia', 'Poland', 'Laos', 'England', 'Cuba', 'Taiwan', 'Italy', 'Canada', 'Portugal', 'China', 'Nicaragua', 'Honduras', 'Iran', 'Scotland', 'Jamaica', 'Ecuador', 'Yugoslavia', 'Hungary', 'Hong', 'Greece', 'Trinadad&Tobago', 'Outlying-US(Guam-USVI-etc)', 'France', 'Holand-Netherlands']
    feature_column_name_native_country_value_list_renamed=['United States', 'Unknown', 'Peru', 'Guatemala', 'Mexico', 'Dominican Republic', 'Ireland', 'Germany', 'Philippines', 'Thailand', 'Haiti', 'El Salvador', 'Puerto Rico', 'Vietnam', 'South', 'Columbia', 'Japan', 'India', 'Cambodia', 'Poland', 'Laos', 'England', 'Cuba', 'Taiwan', 'Italy', 'Canada', 'Portugal', 'China', 'Nicaragua', 'Honduras', 'Iran', 'Scotland', 'Jamaica', 'Ecuador', 'Yugoslavia', 'Hungary', 'Hong', 'Greece', 'Trinadad & Tobago', 'Outlying US (Guam, USVI, etc)', 'France', 'Holand Netherlands']
    feature_column_name_native_country_value_dictionary=dict(zip(feature_column_name_native_country_value_list, feature_column_name_native_country_value_list_renamed))
    df.loc[:, 'Native country']=df.loc[:, 'Native country'].replace(feature_column_name_native_country_value_dictionary)

    return df
    

#################################################################################################################################
#Feature Engineering Functions
#################################################################################################################################


def extract_and_add_features(df):
    """Extracted and add features to the DataFrame df and then return DataFrame df.
    
    Args:
        df (DataFrmae): The DataFrame df to extract and append features from and to.
    Returns:
        df (DataFrame): The DataFrame df with added features. 
    """
    #extract target colummn name 'Income ordinal integer encoding' from target column name 'Income'
    df.loc[df.loc[:, 'Income'].isin(['≤50K']), 'Income ordinal integer encoding']=0
    df.loc[df.loc[:, 'Income'].isin(['>50K']), 'Income ordinal integer encoding']=1
    
    #extract feature colummn name 'Gender binary integer encoding' from feature column name 'Gender'
    df.loc[df.loc[:, 'Gender'].isin(['Female']), 'Gender binary integer encoding']=0
    df.loc[df.loc[:, 'Gender'].isin(['Male']), 'Gender binary integer encoding']=1
    
    #extract feature colummn name 'Marital status group' from feature column name 'Marital status'
    feature_column_name_value_list_never_married=['Never married']
    feature_column_name_value_list_is_married=['Married civilian spouse', 'Married spouse absent', 'Married armed forces spouse', 'Separated',]
    feature_column_name_value_list_was_married=[ 'Widowed', 'Divorced',]
    df.loc[df.loc[:, 'Marital status'].isin(feature_column_name_value_list_never_married), 'Marital status group']='Never married'
    df.loc[df.loc[:, 'Marital status'].isin(feature_column_name_value_list_is_married), 'Marital status group']='Is married'
    df.loc[df.loc[:, 'Marital status'].isin(feature_column_name_value_list_was_married), 'Marital status group']='Was married'

    #extract feature colummn name 'Marital status group ordinal integer encoding' from feature column name 'Marital status group'
    df.loc[df.loc[:, 'Marital status group'].isin(['Never married']), 'Marital status group ordinal integer encoding']=0
    df.loc[df.loc[:, 'Marital status group'].isin(['Is married']), 'Marital status group ordinal integer encoding']=1
    df.loc[df.loc[:, 'Marital status group'].isin(['Was married']), 'Marital status group ordinal integer encoding']=2
    
    #extract feature column name 'Capital-gain-loss difference' from feature column names 'Capital gain' and 'Capital loss'
    df.loc[:, 'Net capital gain']=df.loc[:, 'Capital gain']-df.loc[:, 'Capital loss']

    #extract feature column name 'Employment type' from feature column names 'Hours per week'
    df.loc[:, 'Employment type']='Part-time'
    df.loc[(df.loc[:, 'Hours per week']>=35) & (df.loc[:, 'Hours per week']<=40), 'Employment type']='Full-time'
    df.loc[(df.loc[:, 'Hours per week']>40), 'Employment type']='Overtime'
    
    return df

#################################################################################################################################
#Exploratory Data Analysis
#################################################################################################################################

def capital_loss_capital_gain_relationship_check(df):
    """Get the values of Capital loss and Capital gain when each is 0 and print it.
    
    Args:
        df (DataFrame): The DataFrame containing feature column names 'Capital gain' and 'Capital loss' and values.
    Returns:
        None
    """
    value_list=list(df.loc[df.loc[:, 'Capital loss']>0, 'Capital gain'].value_counts().index)
    print('When Capital loss is >0, Capital gain has values '+str(value_list))
    
    value_list=list(df.loc[df.loc[:, 'Capital gain']>0, 'Capital loss'].value_counts().index)
    print('When Capital gain is >0, Capital loss has values '+str(value_list))

