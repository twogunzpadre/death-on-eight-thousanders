#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import numpy as np
import datetime

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px


# Load the data using pandas
df = pd.read_csv('https://github.com/twogunzpadre/death-on-eight-thousanders/blob/main/deaths_on_eight-thousanders.csv')
df.replace("?", np.nan, inplace=True)

missing_data = df.isnull()
missing_data.head(5)

val_cause = df["Cause of death"].value_counts()
max_val_cause = val_cause.idxmax()

df["Cause of death"].replace(np.nan, max_val_cause, inplace=True)
rows_with_nan = df[df.isnull().any(axis=1)]
df['Nationality'] = df['Nationality'].replace('NaN', 'Unknown')
for column in missing_data.columns.values.tolist():
    print(column)
    print(missing_data[column].value_counts())
    print("")
df['Date'] = pd.to_datetime(df['Date'])
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month
df[['Name', 'Nationality', 'Cause of death', 'Mountain']] = df[
    ['Name', 'Nationality', 'Cause of death', 'Mountain']].astype("str")
# Initialize the Dash app
app = Dash(__name__)
server = app.server

# Set the title of the dashboard
# app.title = "Automobile Statistics Dashboard"

# ---------------------------------------------------------------------------------
# -----------------------------------
# Create the layout of the app
app.layout = html.Div([
    # TASK 2.1 Add title to the dashboard
    html.H1("Yearly Statistics for deaths on Eight Thousanders.",
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 24}),
    html.Div([
        html.Label("Select a country"),
        dcc.Dropdown(
            id='country-drop',
            options=[{'label': country, 'value': country} for country in df['Nationality'].unique()],
            value=df['Nationality'].iloc[0],
            placeholder='Select a report type',
            style={'textAlign': 'center', 'width': '80%', 'padding': '3px', 'font-size': '20px'}
        ),
        html.Div([
            html.H4(children='DataFrame Preview'),
            dcc.Graph(
                id='dataframe-table',
                figure={
                    'data': [{
                        'type': 'table',
                        'header': {
                            'values': df.columns
                        },
                        'cells': {
                            'values': df.values.T
                        }
                    }]
                }
            )
        ])
    ]),

    html.Div(id='output-container', className='chart-grid', style={'display': 'flex'}),
    html.Div(id='display-graph', className='', style = {'display': 'flex'})

])


# TASK 2.4: Creating Callbacks
# Define the callback function to update the input container based on the selected statistics
@app.callback(
    Output(component_id='output-container', component_property='children'),
    Input(component_id='country-drop', component_property='value'))
def update_output(selected_country):
    dfcountry = df[df['Nationality'] == selected_country]
    dfcountry = dfcountry['Year'].value_counts().to_frame().reset_index()
    dfcountry.columns = ['Year', 'Counts']
    dfcountry = dfcountry.sort_values(by="Year")
    R_chart1 = dcc.Graph(
        figure=px.line(dfcountry, x=dfcountry['Year'], y=dfcountry['Counts'],
                       title="Counts of deaths on eight thousanders by Year for " + selected_country))
    return html.Div(className='chart-item', children=[html.Div(children=R_chart1)], style={'display': 'flex'})


# Run the Dash app
if __name__ == '__main__':
    app.run_server(port = 8051)
