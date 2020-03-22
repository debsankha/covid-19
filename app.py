import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

all_cum_df = pd.read_hdf('germany.h5', key='data')


federal_states_sorted = sorted(list(set(all_cum_df['state'])-{'Germany'})) + ['Germany']

germany_time_start = datetime.strptime('2020-02-16', "%Y-%m-%d")
today = datetime.today()



def gen_data_and_layout_death(normed=True):
    normed_suffix_string="/100,000 inhabitants" if normed==True else ""
    data = []
    for state in federal_states_sorted:
        sel = all_cum_df[all_cum_df['state']==state]
        x = sel['date']
        if normed == True:
            y = sel['cumulative_deaths_normed']
        else:
            y = sel['cumulative_deaths']
        data.append({'x': x, 'y': y, 'name': state})
    layout = {
            'title': 'Cumulative number of deaths',
            'showlegend': True,
            'yaxis': {'type': 'log', 'title': 'Deaths'+normed_suffix_string},
            'xaxis': {'title': 'Date', 'range': [germany_time_start, today]},
            }
    return data, layout

def gen_data_and_layout_death_shifted(normed=True):
    normed_suffix_string="/100,000 inhabitants" if normed==True else ""
    data = []
    for state in federal_states_sorted:
        sel = all_cum_df[all_cum_df['state']==state]
        x = sel['days_since_first_death']
        if normed == True:
            y = sel['cumulative_deaths_normed']
        else:
            y = sel['cumulative_deaths']

        data.append({'x': x, 'y': y, 'name': state})
    layout = {
            'title': 'Cumulative number of deaths',
            'showlegend': True,
            'yaxis': {'type': 'log', 'title': 'Deaths'+normed_suffix_string},
            'xaxis': {'title': 'number of days since first death', 'rangemode': 'nonnegative'},
            }
    return data, layout

def gen_data_and_layout_case(normed=True):
    normed_suffix_string="/100,000 inhabitants" if normed==True else ""
    data = []
    for state in federal_states_sorted:
        sel = all_cum_df[all_cum_df['state']==state]
        x = sel['date']
        if normed == True:
            y = sel['cumulative_cases_normed']
        else:
            y = sel['cumulative_cases']
        data.append({'x': x, 'y': y, 'name': state})
    layout = {
            'title': 'Cumulative number of cases',
            'showlegend': True,
            'yaxis': {'type': 'log', 'title': 'Cases'+normed_suffix_string},
            'xaxis': {'title': 'Date', 'range': [germany_time_start, today]},
            }
    return data, layout

def gen_data_and_layout_case_shifted(normed=True):
    normed_suffix_string="/100,000 inhabitants" if normed==True else ""
    data = []
    for state in federal_states_sorted:
        sel = all_cum_df[all_cum_df['state']==state]
        x = sel['days_since_50_cases']
        if normed == True:
            y = sel['cumulative_cases_normed']
        else:
            y = sel['cumulative_cases']
        data.append({'x': x, 'y': y, 'name': state})
    layout = {
            'title': 'Cumulative number of cases',
            'showlegend': True,
            'yaxis': {'type': 'log', 'title': 'Cases'+normed_suffix_string},
            'xaxis': {'title': 'number of days since 50 cases', 'rangemode': 'nonnegative'},
            }
    return data, layout

data_death, layout_death = gen_data_and_layout_death()
data_death_shifted, layout_death_shifted = gen_data_and_layout_death_shifted()
data_case, layout_case = gen_data_and_layout_case()
data_case_shifted, layout_case_shifted = gen_data_and_layout_case_shifted()


app.layout = html.Div(
    [
    html.H1(children='Some COVID-19 Charts'),
    html.Div(children=[
        "Based on: ", 
        html.A('Federal state-level data', 
                href='https://npgeo-corona-npgeo-de.hub.arcgis.com/datasets/dd4580c810204019a7b8eb3e0b329dd6_0/data'
                ),
        " from germany, updated daily. ",
        html.A('Source code on GitHub', href="https://github.com/debsankha/covid-19/"),
        ]
        ),
    dcc.Checklist(
            id="checklist",
            options=[
                {"label": "Normalize by 100,000 inhabitants", "value": "norm"},
            ],
            value=["norm"],
        ),
    html.Div(
    [
    dcc.Graph(
        id='case',
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
        id='death',
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

@app.callback(
    [
     Output("death", "figure"),
     Output("death_shifted_x", "figure"),
     Output("case", "figure"),
     Output("case_shifted_x", "figure"),
    ],
    [Input("checklist", "value")],
)
def toggle_normalization(is_normed):
    if is_normed==['norm']:
        tonorm = True
    else:
        tonorm = False
    data_death, layout_death = gen_data_and_layout_death(normed=tonorm)
    data_death_shifted, layout_death_shifted = gen_data_and_layout_death_shifted(normed=tonorm)
    data_case, layout_case = gen_data_and_layout_case(normed=tonorm)
    data_case_shifted, layout_case_shifted = gen_data_and_layout_case_shifted(normed=tonorm)


    return [
            {"data": data_death, "layout": layout_death},
            {"data": data_death_shifted, "layout": layout_death_shifted},
            {"data": data_case, "layout": layout_case},
            {"data": data_case_shifted, "layout": layout_case_shifted},
            ]


if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port=8080)
