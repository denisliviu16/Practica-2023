import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

df1 = pd.read_excel('accidents.xlsx')
df2 = pd.read_excel('data.xlsx')
df3 = pd.read_excel('budget.xlsx')
df4 = pd.read_excel('internet.xlsx')

fig1 = px.bar(df1, x='Country', y=df1.columns[1])
fig1.update_layout(
    xaxis_title="Country from the EU",
    yaxis_title="Rate per million population",
    title=f"Road deaths per million inhabitants - Year {df1.columns[1]}"
)
fig1.update_layout(
    width = 800,
    height = 600
)
fig2 = px.choropleth(
    data_frame=df2,
    locations="Country",
    locationmode="country names",
    color="Life Expectancy",
    scope="europe"
)
fig2.update_layout(
    width=800,
    height=600
)

fig3 = px.pie (df3,names='Member state',values='Contribution')


app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.Label("Select the year:", style={'display': 'inline-block'}),
        dcc.Dropdown(
            id='dropdown-year',
            options=[{'label': str(year), 'value': year} for year in df1.columns[1:]],
            style={'width': '150px', 'height': '40px'},
            value=df1.columns[1],
        )
    ]),
    
    dcc.Graph(id='bar-chart',
              style={'width':'1200px','height':'550px'}),
    
    html.Div([
        html.Title('Financing of the general EU budget by member state (2023)', style={'text-align': 'left'}),
        dcc.Graph(id='graph', figure=fig3, style={'float': 'left', 'margin': 'auto', 'width': '800px', 'height': '600px'})
    ]),
    
    html.Div([
        dcc.Graph(id='choropleth-map1',
                  figure=fig3,
                  style={'width': '800px', 'height': '600px'}
        )
    ]),
    
    html.Div([
        dcc.Graph(
                  figure=fig2,
                  style={'width': '800px', 'height': '600px'}
        )
    ]),
    
    html.Div([
        html.Label("Select the region:", style={'display': 'inline-block'}),
        dcc.Dropdown(
            id='dropdown-region',
            options=[{'label': region, 'value': region} for region in df4['Region'].unique()],
            style={'width': '150px', 'height': '40px'},
            value=df4['Region'].unique()[0],
        )
    ]),
    
    html.Div([
    dcc.Graph(
        id='line-chart',
        style={'width': '1200px', 'height': '800px'}
        )
    ],
    style={'margin-bottom': '50px'})
])




@app.callback(
    Output('bar-chart', 'figure'),
    [Input('dropdown-year', 'value')]
)
def update_graph(selected_year):
    fig = px.bar(df1, x='Country', y=selected_year)
    fig.update_layout(
        xaxis_title="Country from the EU",
        yaxis_title="Rate per million population",
        title=f"Road deaths per million inhabitants - Year {selected_year}"
    )
    return fig

@app.callback(
    Output('line-chart', 'figure'),
    [Input('dropdown-region', 'value')]
)
def update_line_chart(selected_region):
    filtered_data = df4[df4['Region'] == selected_region]
    
    sorted_data = filtered_data.sort_values(by='Country', ascending=True)
    sorted_data.loc[:, 'Pct'] = sorted_data['Pct'].str.rstrip('%').astype(float)
    sorted_data = sorted_data.sort_values(by='Pct', ascending=True)
    sorted_data.loc[:, 'Pct'] = sorted_data['Pct'].astype(str) + '%'
    
    fig = px.line(sorted_data, x='Country', y='Pct',hover_data=["Subregion", "Internet users", "Population(2021)"])
    
    fig.update_layout(
        title='Line graph of countries by number of Internet users',
        xaxis_title='Country',
        yaxis_title='Percentage of Internet users',
        width=1200,
        plot_bgcolor='#f2f2f2',
        height=600
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
