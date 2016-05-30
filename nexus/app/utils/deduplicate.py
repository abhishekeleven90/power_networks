#to remove duplicates for pandas DataFrame
#currently using it to remove from file - 'google_cities'


import pandas as pd


def deduplicate(df, columns):
    return df.drop_duplicates(columns)

if __name__ == "__main__":
    df = pd.read_csv('./locdata/google_cities.csv')
    df_new = deduplicate(df, ['SID', 'city'])
    df_new.to_csv('google_cities_nodups.csv')
