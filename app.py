import dash
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

all_cum_df = pd.read_hdf('germany.h5', key='data')


federal_states_sorted = sorted(list(set(all_cum_df['state'])-{'Germany'})) + ['Germany']

def gen_data_and_layout_death():
    data = []
    for state in federal_states_sorted:
        sel = all_cum_df[all_cum_df['state']==state]
        x = sel['Meldedatum']
        y = sel['cumulative_deaths_normed']
        data.append({'x': x, 'y': y, 'name': state})
    layout = {
#            'title': 'foo',
            'showlegend': True,
            'yaxis': {'type': 'log', 'title': 'Deaths/100,000 inhabitants'},
            'xaxis': {'title': 'Date'},
            }
    return data, layout

def gen_data_and_layout_death_shifted():
    data = []
    for state in federal_states_sorted:
        sel = all_cum_df[all_cum_df['state']==state]
        x = sel['days_since_first_death']
        y = sel['cumulative_deaths_normed']
        data.append({'x': x, 'y': y, 'name': state})
    layout = {
 #           'title': 'foo',
            'showlegend': True,
            'yaxis': {'type': 'log', 'title': 'Deaths/100,000 inhabitants'},
            'xaxis': {'title': 'Date since first death', 'rangemode': 'nonnegative'},
            }
    return data, layout

def gen_data_and_layout_case():
    data = []
    for state in federal_states_sorted:
        sel = all_cum_df[all_cum_df['state']==state]
        x = sel['Meldedatum']
        y = sel['cumulative_cases_normed']
        data.append({'x': x, 'y': y, 'name': state})
    layout = {
    #        'title': 'foo',
            'showlegend': True,
            'yaxis': {'type': 'log', 'title': 'Cases/100,000 inhabitants'},
            'xaxis': {'title': 'Date'},

            }
    return data, layout

def gen_data_and_layout_case_shifted():
    data = []
    for state in federal_states_sorted:
        sel = all_cum_df[all_cum_df['state']==state]
        x = sel['days_since_50_cases']
        y = sel['cumulative_deaths_normed']
        data.append({'x': x, 'y': y, 'name': state})
    layout = {
     #       'title': 'foo',
            'showlegend': True,
            'yaxis': {'type': 'log', 'title': 'Cases/100,000 inhabitants'},
            'xaxis': {'title': 'Date since 50 cases', 'rangemode': 'nonnegative'},
            }
    return data, layout

data_death, layout_death = gen_data_and_layout_death()
data_death_shifted, layout_death_shifted = gen_data_and_layout_death_shifted()
data_case, layout_case = gen_data_and_layout_case()
data_case_shifted, layout_case_shifted = gen_data_and_layout_case_shifted()




app.layout = html.Div(
    [
    html.H1(children='Some COVID-19 Charts'),
    html.Div(children='''
        Federal state-level data from germany
    '''),

    html.Div(
    [
    dcc.Graph(
        id='cases',
        figure={
            'data': data_case,
            'layout': layout_case,
            }
    )], style={'width': '49%', 'display': 'inline-block'}),
    html.Div([
    dcc.Graph(
        id='case_shifted_x',
        figure={
            'data': data_case_shifted,
            'layout': layout_case_shifted,
            }
    )
    ], style={'width': '49%', 'display': 'inline-block'}),



    html.Div(
    [
    dcc.Graph(
        id='deaths',
        figure={
            'data': data_death,
            'layout': layout_death,
            }
    )], style={'width': '49%', 'display': 'inline-block'}),
    html.Div([
    dcc.Graph(
        id='death_shifted_x',
        figure={
            'data': data_death_shifted,
            'layout': layout_death_shifted,
            }
    )
    ], style={'width': '49%', 'display': 'inline-block'}),

    ])



if __name__ == '__main__':
    app.run_server(debug=True, port=9898)
