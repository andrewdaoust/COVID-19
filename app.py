import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from covid import Covid

covid_data = Covid()

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='COVID-19'),
    html.Div(children='Select categories to plot.'),

    html.Div(children=[
        covid_data.states_dropdown(),
        dcc.RadioItems(
            id='plot-type',
            options=[
                {'label': 'Daily', 'value': 'daily'},
                {'label': 'Total', 'value': 'total'}
            ],
            value='daily'
        ),
        dcc.RadioItems(
            id='data-type',
            options=[
                {'label': 'Cases', 'value': 'cases'},
                {'label': 'Deaths', 'value': 'deaths'}
            ],
            value='cases'
        ),
        # html.Button('Update Chart', id='submit', n_clicks=0),
    ]),

    html.Div(id='chart'),
])


def build_data_dicts(pt, dt, groups):
    pre = ''
    if pt == 'daily':
        pre = 'new_'
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
        title = groups[0] + ' ' + title

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