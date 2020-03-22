import pandas as pd

url = "https://opendata.arcgis.com/datasets/dd4580c810204019a7b8eb3e0b329dd6_0.csv"
df = pd.read_csv(url)

df['Meldedatum'] = pd.to_datetime(df["Meldedatum"])
df.sort_values(by='Meldedatum')


tables = pd.read_html("https://de.wikipedia.org/wiki/Liste_der_deutschen_Bundesl%C3%A4nder_nach_Bev%C3%B6lkerung", thousands='.')
population_states = tables[0][['Bundesland', '2018']]

population_states.loc[2, 'Bundesland'] = 'Berlin'
population_states.loc[16, 'Bundesland'] = 'Germany'

narrow_df = df[['Bundesland', 'AnzahlFall', 'AnzahlTodesfall', 'Meldedatum']]
narrow_df['Meldedatum'] = narrow_df['Meldedatum'].apply(lambda x:x.date())

narrow_df.sort_values(by='Meldedatum', inplace=True)
cumsum_dfs = []

for bundesland in list(narrow_df['Bundesland'].unique())+['Germany']:
    if bundesland == 'Germany':
        sel = narrow_df
    else:
        sel = narrow_df[narrow_df['Bundesland']==bundesland]
    sel = sel[['Meldedatum','AnzahlFall', 'AnzahlTodesfall']].groupby('Meldedatum').agg('sum')
    sel = sel.sort_values(by='Meldedatum')
    sel['cumulative_cases'] = sel['AnzahlFall'].cumsum()
    sel['cumulative_deaths'] = sel['AnzahlTodesfall'].cumsum()

    if len(sel[sel['cumulative_cases'] > 50]) > 0:
        first_case_date = sel[sel['cumulative_cases'] > 50].iloc[0].name
        sel['days_since_50_cases'] = (sel.index - first_case_date)/pd.Timedelta(days=1)
    else:
        sel['days_since_50_cases'] = None

    if len(sel[sel['cumulative_deaths'] > 0]) > 0:
        first_death_date = sel[sel['cumulative_deaths'] > 0].iloc[0].name
        sel['days_since_first_death'] = (sel.index - first_death_date)/pd.Timedelta(days=1)
    else:
        sel['days_since_first_death'] = None
    sel['Bundesland'] = bundesland

    cumsum_dfs.append(sel.reset_index())

all_cum_df = pd.concat(cumsum_dfs)

all_cum_df = all_cum_df.merge(population_states, left_on='Bundesland', right_on='Bundesland')
all_cum_df.rename({'2018': 'population'}, axis='columns', inplace=True)

all_cum_df['cumulative_deaths_normed'] = all_cum_df['cumulative_deaths']*100000/all_cum_df['population']
all_cum_df['cumulative_cases_normed'] = all_cum_df['cumulative_cases']*100000/all_cum_df['population']

german_state_abbrs = {
'Baden-Württemberg': 'BW',
'Bayern': 'BY',
'Berlin': 'BE',
'Brandenburg': 'BB',
'Bremen': 'HB',
'Hamburg': 'HH',
'Hessen': 'HE',
'Niedersachsen': 'NI',
'Mecklenburg-Vorpommern': 'MV',
'Nordrhein-Westfalen': 'NW',
'Rheinland-Pfalz': 'RP',
'Saarland': 'SL',
'Sachsen': 'SN',
'Sachsen-Anhalt': 'ST',
'Schleswig-Holstein': 'SH',
'Thüringen': 'TH',
}

all_cum_df['state'] = all_cum_df['Bundesland'].apply(lambda x:german_state_abbrs[x] if x!='Germany' else 'Germany')
all_cum_df['date'] = all_cum_df['Meldedatum'].apply(lambda x:pd.Timestamp(x))

all_cum_df.to_hdf('germany.h5', key='data')

