import pandas as pd
import numpy as np
import dash_core_components as dcc


class Covid(object):
    def __init__(self):
        _us = pd.read_csv('us.csv', index_col='date', parse_dates=True)
        self._state = pd.read_csv('us-states.csv', index_col=['state', 'date'], parse_dates=True)
        self._county = pd.read_csv('us-counties.csv', index_col=['state', 'county', 'date'], parse_dates=True)

        self.data = {'US': _us}

        self.daily_7day_14day('US')
        self.build_states()
        self.build_counties()

    def _daily_values(self, key, new_col, old_col):
        shifted_col = old_col + '_shifted'
        self.data[key][shifted_col] = self.data[key][old_col].shift(1, fill_value=0)

        self.data[key][new_col] = self.data[key][old_col] - self.data[key][shifted_col]

    def _7_14day(self, key, old_col):
        new_removed = old_col.replace('new_', '')
        seven_col = 'seven_day_' + new_removed
        fourteen_col = 'fourteen_day_' + new_removed

        for i in range(1, 14):
            self.data[key][f'{new_removed}_shift{i}'] = self.data[key][old_col].shift(i, fill_value=0)

        seven = [old_col] + [f'{new_removed}_shift{n}' for n in range(1, 7)]
        fourteen = [old_col] + [f'{new_removed}_shift{n}' for n in range(1, 13)]

        self.data[key][seven_col] = self.data[key][seven].mean(axis=1)
        self.data[key][fourteen_col] = self.data[key][fourteen].mean(axis=1)

    def daily_7day_14day(self, key):
        self._daily_values(key, 'new_cases', 'cases')
        self._daily_values(key, 'new_deaths', 'deaths')

        self._7_14day(key, 'new_cases')
        self._7_14day(key, 'new_deaths')

    def build_states(self):
        state_list = ['Alabama', 'Alaska', 'Arizona', 
                      'Arkansas', 'California', 'Colorado', 'Connecticut', 
                      'Delaware', 'District of Columbia', 'Florida', 'Georgia', 
                      'Guam', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 
                      'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 
                      'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 
                      'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 
                      'New Jersey', 'New Mexico', 'New York', 'North Carolina', 
                      'North Dakota', 'Northern Mariana Islands', 'Ohio', 'Oklahoma', 
                      'Oregon', 'Pennsylvania', 'Puerto Rico', 'Rhode Island', 
                      'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 
                      'Vermont', 'Virgin Islands', 'Virginia', 'Washington', 
                      'West Virginia', 'Wisconsin', 'Wyoming']
                      # 'American Samoa'

        for s in state_list:
            self.data[s] = self._state.loc[s].copy()
            self.daily_7day_14day(s)

    def build_counties(self):
        counties_list = [
            ('Essex', 'Massachusetts'),
            ('Hillsborough', 'New Hampshire'),
            ('Virginia Beach city', 'Virginia'),
            ('Rockingham', 'New Hampshire')
            # ('Rensselaer', 'New York')
        ]

        for c in counties_list:
            key = f'{c[0]}-{c[1]}'
            self.data[key] = self._county.loc[c[1], c[0]].copy()
            self.daily_7day_14day(key)

    def dropdown(self):
        return dcc.Dropdown(
            id='dropdown',
            options=[
                {'label': 'United States', 'value': 'US'},
                {'label': 'Alabama', 'value': 'Alabama'},
                {'label': 'Alaska', 'value': 'Alaska'},
                #{'label': 'American Samoa', 'value': 'American Samoa'},
                {'label': 'Arizona', 'value': 'Arizona'},
                {'label': 'Arkansas', 'value': 'Arkansas'},
                {'label': 'California', 'value': 'California'},
                {'label': 'Colorado', 'value': 'Colorado'},
                {'label': 'Connecticut', 'value': 'Connecticut'},
                {'label': 'Delaware', 'value': 'Delaware'},
                {'label': 'District of Columbia', 'value': 'District of Columbia'},
                {'label': 'Florida', 'value': 'Florida'},
                {'label': 'Georgia', 'value': 'Georgia'},
                {'label': 'Guam', 'value': 'Guam'},
                {'label': 'Hawaii', 'value': 'Hawaii'},
                {'label': 'Idaho', 'value': 'Idaho'},
                {'label': 'Illinois', 'value': 'Illinois'},
                {'label': 'Indiana', 'value': 'Indiana'},
                {'label': 'Iowa', 'value': 'Iowa'},
                {'label': 'Kansas', 'value': 'Kansas'},
                {'label': 'Kentucky', 'value': 'Kentucky'},
                {'label': 'Louisiana', 'value': 'Louisiana'},
                {'label': 'Maine', 'value': 'Maine'},
                {'label': 'Maryland', 'value': 'Maryland'},
                {'label': 'Massachusetts', 'value': 'Massachusetts'},
                {'label': 'Michigan', 'value': 'Michigan'},
                {'label': 'Minnesota', 'value': 'Minnesota'},
                {'label': 'Mississippi', 'value': 'Mississippi'},
                {'label': 'Missouri', 'value': 'Missouri'},
                {'label': 'Montana', 'value': 'Montana'},
                {'label': 'Nebraska', 'value': 'Nebraska'},
                {'label': 'Nevada', 'value': 'Nevada'},
                {'label': 'New Hampshire', 'value': 'New Hampshire'},
                {'label': 'New Jersey', 'value': 'New Jersey'},
                {'label': 'New Mexico', 'value': 'New Mexico'},
                {'label': 'New York', 'value': 'New York'},
                {'label': 'North Carolina', 'value': 'North Carolina'},
                {'label': 'North Dakota', 'value': 'North Dakota'},
                {'label': 'Northern Mariana Islands', 'value': 'Northern Mariana Islands'},
                {'label': 'Ohio', 'value': 'Ohio'},
                {'label': 'Oklahoma', 'value': 'Oklahoma'},
                {'label': 'Oregon', 'value': 'Oregon'},
                {'label': 'Pennsylvania', 'value': 'Pennsylvania'},
                {'label': 'Puerto Rico', 'value': 'Puerto Rico'},
                {'label': 'Rhode Island', 'value': 'Rhode Island'},
                {'label': 'South Carolina', 'value': 'South Carolina'},
                {'label': 'South Dakota', 'value': 'South Dakota'},
                {'label': 'Tennessee', 'value': 'Tennessee'},
                {'label': 'Texas', 'value': 'Texas'},
                {'label': 'Utah', 'value': 'Utah'},
                {'label': 'Vermont', 'value': 'Vermont'},
                {'label': 'Virgin Islands', 'value': 'Virgin Islands'},
                {'label': 'Virginia', 'value': 'Virginia'},
                {'label': 'Washington', 'value': 'Washington'},
                {'label': 'West Virginia', 'value': 'West Virginia'},
                {'label': 'Wisconsin', 'value': 'Wisconsin'},
                {'label': 'Wyoming', 'value': 'Wyoming'},
                {'label': 'Hillsborough County, NH', 'value': 'Hillsborough-New Hampshire'},
                {'label': 'Essex County, MA', 'value': 'Essex-Massachusetts'},
                {'label': 'Virginia Beach, Virginia', 'value': 'Virginia Beach city-Virginia'},
                {'label': 'Rockingham Country, NH', 'value': 'Rockingham-New Hampshire'}
            ],
            value=['New Hampshire'],
            clearable=False,
            multi=True,
        )
