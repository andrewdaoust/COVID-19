import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output  #, State

from covid import Covid

covid_data = Covid()

app = dash.Dash(__name__)
app.title = 'COVID-19 Tracker'

server = app.server

app.layout = html.Div(children=[
    html.H1(children='COVID-19'),
    html.Div(children='Select categories to plot.'),

    covid_data.dropdown(),
    html.Div(children=[
        html.H4(children='Plot type'),
        dcc.RadioItems(
            id='plot-type',
            options=[
                {'label': 'Daily', 'value': 'daily'},
                {'label': 'Total', 'value': 'total'},
                {'label': '7-Day Average', 'value': '7 day average'},
                {'label': '14-Day Average', 'value': '14 day average'}
            ],
            value='daily'
        ),
    ], style={'width': '15%', 'display': 'inline-block'}),

    html.Div(children=[
        html.H4(children='Data type'),
        dcc.RadioItems(
            id='data-type',
            options=[
                {'label': 'Cases', 'value': 'cases'},
                {'label': 'Deaths', 'value': 'deaths'}
            ],
            value='cases'
        ),
    ], style={'width': '10%', 'display': 'inline-block'}),

    html.Div(id='chart'),

    html.Footer(children=[
        "Data from the ",
        dcc.Link(children="New York Times", 
            href="https://github.com/nytimes/covid-19-data",
            refresh=True
        ),
        ".  Visualization by Andrew D'Aoust."
    ]),
])


def build_data_dicts(pt, dt, groups):
    pre = ''
    if pt == 'daily':
        pre = 'new_'
    elif pt == '7 day average':
        pre = 'seven_day_'
    elif pt == '14 day average':
        pre = 'fourteen_day_'
    data = []
    for group in groups:
        d = {
            'x': covid_data.data[group].index,
            'y': covid_data.data[group][f'{pre}{dt}'],
            'type': 'bar',
            'name': group
        }

        data.append(d)

    return data


@app.callback(
    Output('chart', 'children'),
    [Input('plot-type', 'value'), Input('data-type', 'value'), Input('dropdown', 'value')]
    # [Input('submit', 'n_clicks')], 
    # state=[State('plot-type', 'value'), State('data-type', 'value'), State('dropdown', 'value')]
)
def add_chart(plot_type, data_type, groups):
    data = build_data_dicts(plot_type, data_type, groups)

    title = f'{plot_type.title()} {data_type.title()}'
    if len(groups) == 1:
        title = groups[0].replace('-', ', ').replace(' city', '') + ' - ' + title

    return dcc.Graph(
        id='graph',
        figure={
            'data': data,
            'layout': {
                'title': title
            }
        }
    )


if __name__ == '__main__':
    app.run_server(debug=True)
