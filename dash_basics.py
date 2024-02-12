""" python3 -m pip install packaging
python3 -m pip install pandas dash
pip3 install httpx==0.20 dash plotly """

import pandas as pd
import plotly.express as px
import dash
from dash import dcc
from dash import html


airline_data = pd.read_csv(
    'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv',
    encoding='ISO-8859-1',
    dtype={
        'Div1Airport': str,
        'Div1TailNum': str,
        'Div2Airport': str,
        'Div2TailNum': str
    }
)

data = airline_data.sample(n=500, random_state=42)

fig = px.pie(
    data,
    values='Flights',
    names='DistanceGroup',
    title='Distance Group Proportion by Flights'
)

fig.update_layout(
    title=dict(
        x=0.5,
        font=dict(
            size=20
        )
    )
)

""" Components of dash application:
- Title of the application
- Description of the application
- Chart conveying the proportion of distance group by month

Mapping to the respective Dash HTML tags:
- Title added using html.H1() tag
- Description added using html.P() tag
- Chart added using dcc.Graph() tag """

# create a dash application
app = dash.Dash(__name__)

app.layout = html.Div(
    children=[
        html.H1(
            'Airline On-Line Performance Dashboard',
            style={
                'textAlign': 'center',
                'color': '#503D36',
                'font-size': 50
            }
        ),
        html.P(
            'Proportion of Distance Group (250 Mile Distance Interval Group) by Flights',
            style={'textAlign': 'center', 'color': '#F57241'}
        ),
        dcc.Graph(figure=fig)
    ]
)

# run the app
if __name__ == '__main__':
    app.run_server()