import os
import skillsnetwork
import asyncio
import pandas as pd
import plotly.express as px
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output


### Lab 6: SpaceX Dashboard
async def async_download(url, filename):
    await skillsnetwork.download(url, filename)

def get_pie_chart(entered_site):
    if entered_site == 'All Sites':
        grouped_data = spacex_df.groupby('Launch Site')['class'].mean()
        names = spacex_df.groupby('Launch Site')['Launch Site'].first()
        title = 'Total Successful Launches by Site'
    else:
        filtered_data = spacex_df[spacex_df['Launch Site'] == str(entered_site)]
        grouped_data = filtered_data['class'].value_counts(normalize=True)
        names = spacex_df['class'].unique()
        title = f'Total Successful and Unsuccessful Launches for Site {entered_site}'
    fig = px.pie(
        values=grouped_data,
        names=names,
        title=title
    )
    fig.update_layout(title=dict(text=title, x=0.475))
    return fig

def get_scatter_chart(entered_site, payload_mass):
    if entered_site == 'All Sites':
        data = spacex_df[spacex_df['Payload Mass (kg)'].between(payload_mass[0], payload_mass[1])]
        title = 'Correlation Between Payload and Successful Launches for All Sites'
    else:
        filtered_data = spacex_df[spacex_df['Launch Site'] == str(entered_site)]
        data = filtered_data[filtered_data['Payload Mass (kg)'].between(payload_mass[0], payload_mass[1])]
        title = f'Correlation Between Payload and Successful Launches for Site {entered_site}'
    fig = px.scatter(
        data,
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version Category',
        hover_data=['Launch Site'],
        title=title
    )
    fig.update_layout(
        title=dict(text=title, x=0.475),
        yaxis_title='Launch Result'
    )
    return fig


os.chdir(r'C:\Users\42073\Desktop\Python_data_science\C5')
url_dataset = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv'
filename_dataset = 'spacex_dash.csv'
url_skeleton = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_3/spacex_dash_app.py'
filename_skeleton = 'spacex_dash_app.py'

""" asyncio.run(async_download(url_dataset, filename_dataset))
asyncio.run(async_download(url_skeleton, filename_skeleton)) """

spacex_df = pd.read_csv('spacex_dash.csv')
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()


app = dash.Dash(__name__)

app.layout = html.Div(
    children=(
        [
            html.H1(
                'SpaceX Launch Records Dashboard',
                style={
                    'textAlign': 'center',
                    'color': '#503D36',
                    'font-size': 40
                }
            ),

            ## Task 1: Add a dropdown list to enable Launch Site selection
            # The default select value is for ALL sites
            dcc.Dropdown(
                id='site-dropdown',
                options=[
                    {'label': 'All Sites', 'value': 'All Sites'},
                    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                ],
                placeholder='Select a Launch Site',
                value='All Sites',
                searchable=True
            ),
            html.Br(),

            ## Task 2a: Add a pie chart to show the total successful launches count for all sites
            # If a specific launch site was selected, show the Success vs. Failed counts for the site
            html.Div(dcc.Graph(id='success-pie-chart')),
            html.Br(),

            html.P('Payload Range [kg]:'),

            ## Task 3: Add a slider to select payload range
            dcc.RangeSlider(
                id='payload-slider',
                min=0,
                max=10000,
                step=1000,
                marks={i: str(i) for i in range(0, 10001, 1000)},
                value=[min_payload, max_payload]
            ),

            ## Task 4a: Add a scatter chart to show the correlation between payload and launch success
            html.Div(dcc.Graph(id='success-payload-scatter-chart'))
        ]
    )
)

## Task 2b: Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(
        component_id='success-pie-chart',
        component_property='figure'
    ),
    Input(
        component_id='site-dropdown',
        component_property='value'
    )
)
def update_pie_chart(entered_site):
    fig = get_pie_chart(entered_site)
    return fig

## Task 4b: Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(
        component_id='success-payload-scatter-chart',
        component_property='figure'
    ),
    [
        Input(
        component_id='site-dropdown',
        component_property='value'
        ),
        Input(
        component_id='payload-slider',
        component_property='value'
        )
    ]
)
def update_scatter_chart(entered_site, payload_mass):
    fig = get_scatter_chart(entered_site, payload_mass)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)