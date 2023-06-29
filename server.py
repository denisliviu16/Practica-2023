import dash
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np


df1 = pd.read_excel('accidents.xlsx')
df2 = pd.read_excel('data.xlsx')
df3 = pd.read_excel('budget.xlsx')
df4 = pd.read_excel('internet.xlsx')
df5 = pd.read_excel('gdp.xlsx')
df6 = pd.read_excel('africa.xlsx')
df7 = pd.read_excel('facts.xlsx',header=None)
df8 = pd.read_excel('ukrainian_refugee_destinations.xlsx')


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
    title=f"Life Expectancy in Europe (2021)",
    scope="europe",
    color_continuous_scale="PiYG"
)
fig2.update_layout(
    width=800,
    height=600
)

fig6 = px.choropleth(
    data_frame=df6,
    locations="Country",
    locationmode="country names",
    color="Combined",
    title=f"List of countries by median age (2020)",
    hover_data=["Male","Female"],
    #scope="africa"
    projection='natural earth'
)
fig6.update_layout(
    width=800,
    height=600
)

fig3 = px.pie (df3,names='Member state',values='Contribution',title=f"Financing of the general EU budget by member state (2023)")


df4['Pct'] = df4['Pct'].str.rstrip('%').astype(float)

fig4 = px.choropleth(
    data_frame=df4,
    locations='Country',
    locationmode='country names',
    color='Pct',
    title=f"Internet users in 2022 as a percentage(%) of a country's population",
    hover_data=["Region","Subregion", "Internet users", "Population(2021)"],
    projection='natural earth',
    color_continuous_scale="Viridis"
)
fig4.update_layout(
    width=800,
    height=500
)

fig5 = px.line(df5, x='Country', y=df5.columns[2])
fig5.update_layout(
    title='Line graph of countries by GDP',
    xaxis_title='Country',
    yaxis_title='GDP (billion USD)',
    width=1200,
    plot_bgcolor='#f2f2f2',
    height=600
)

df8['Number'] = pd.to_numeric(df8['Number'], errors='coerce', downcast='integer')

fig8 = px.choropleth(
    data_frame=df8,
    locations="Country",
    locationmode="country names",
    color="Number",
    title=f"Ukrainian Refugee Destinations by the Numbers as of March 11, 2023",
    scope="europe",
    color_continuous_scale="YlOrRd"
)


fig8.update_layout(
    width=800,
    height=600
)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)


SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}



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
    [Input('dropdown-an', 'value')]
)
def update_line_chart(selected_an):
    filtered_data = df5[['Country', selected_an]].copy()
    filtered_data = filtered_data.dropna(subset=[selected_an])
    filtered_data[selected_an] = pd.to_numeric(filtered_data[selected_an], errors='coerce')
    
    fig = px.line(filtered_data, x='Country', y=selected_an)

    fig.update_layout(
        title='Line graph of countries by GDP (USD billion)',
        xaxis_title='Country',
        yaxis_title='GDP (USD billion)',
        width=1100,
        plot_bgcolor='#f2f2f2',
        height=600
    )
    return fig

@app.callback(
    dash.dependencies.Output('output', 'children'),
    [dash.dependencies.Input('dropdown-category', 'value')]
)
def update_output(value):
    column_values = df7[value].values.tolist()
    return html.Div([
        html.H3(column_values[0], style={'margin-top': '50px', 'margin-bottom': '50px'}),
        *[html.P(val) for val in column_values[1:]]
    ])


@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def render_page_content(pathname):
    if pathname == "/":
        return [
                html.H1('50 unbelievable facts about the world to make you seem cultured',
                        style={'textAlign':'center'}),
                
                dcc.Dropdown(
                        id='dropdown-category',
                        options=[{'label': str(df7.iloc[0][column]), 'value': column} for column in df7.columns],
                        style={'width': '300px', 'height': '40px'},
                        value=df7.columns[0],),
                html.Div(id='output')
        ]
    elif pathname == "/charts":
        return [
                html.H1('Europe charts statistics',
                        style={'textAlign':'center'}),
                
                html.Div([
                    html.Label("Select the year:", style={'display': 'inline-block'}),
                    dcc.Dropdown(
                        id='dropdown-year',
                        options=[{'label': str(year), 'value': year} for year in df1.columns[1:]],
                        style={'width': '150px', 'height': '40px'},
                        value=df1.columns[1],)
                        ]),
                dcc.Graph(id='bar-chart',
                style={'width':'1100px','height':'550px'}),
                
                    html.Div([
                    dcc.Graph(id='graph', figure=fig3, style={'float': 'left', 'margin': 'auto', 'width': '800px', 'height': '600px'})
                ]),
                html.Div([
                    dcc.Graph(id='choropleth-map1',
                            figure=fig3,
                            style={'width': '800px', 'height': '600px'}
                    )
                ]),
                
                html.Div([
                    html.Label("Select the year:", style={'display': 'inline-block'}),
                    dcc.Dropdown(
                        id='dropdown-an',
                        options=[{'label': str(year), 'value': year} for year in df5.columns[2:]],
                        style={'width': '150px', 'height': '40px'},
                        value=df5.columns[2],
                    )
                ]),
    
                html.Div([
                dcc.Graph(
                    id='line-chart',
                    figure=fig5,
                    style={'width': '1100px', 'height': '600px'}
                    )
                ])
                
                ]
    elif pathname == "/maps":
        return [
                html.H1('World & rest of world statistics maps',
                        style={'textAlign':'center'}),
                
                html.Div([
                dcc.Graph(
                    figure=fig2,
                    style={'width': '800px', 'height': '600px'}
                    )
                ]),
                
                html.Div([
                dcc.Graph(
                    figure=fig6,
                    style={'width': '800px', 'height': '600px'}
                    )
                ]),
                
                html.Div([
                dcc.Graph(
                    figure=fig4,
                    style={'width': '800px', 'height': '600px'}
                )
                ]),
                
                html.Div([
                dcc.Graph(
                    figure=fig8,
                    style={'width': '800px', 'height': '600px'}
                    )
                ])
                ]
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )



sidebar = html.Div(
    children=[
        html.Div(
            children=[
                html.H2("WorldStat", className="display-4", style={"font-size": "40px"}),
                html.Img(src="https://static.vecteezy.com/system/resources/previews/013/743/847/original/planet-earth-icon-png.png", className="float-right", style={"width": "40px", "height": "40px"}),
            ],
            style={"display": "flex", "align-items": "center"}
        ),
        html.Hr(),
        html.P("Personalized dashboards created with scraped information from the Internet", className="lead"),
        dbc.Nav(
            [
                dbc.NavLink(
                    html.Div(
                        [
                            "50 Facts",
                            html.Img(
                                src="https://png.pngtree.com/png-vector/20230120/ourmid/pngtree-did-you-know-label-vector-illustration-png-image_6561764.png",
                                height="100px",
                                width="75px",
                                style={"margin-left": "20px"}
                            ),
                        ],
                        style={"display": "flex", "align-items": "center", "width": "100px", "height": "80px"}
                    ),
                    href="/",
                    active="exact"
                ),
                dbc.NavLink(
                    html.Div(
                        [
                            "Charts",
                            html.Img(
                                src="https://cdn1.iconfinder.com/data/icons/social-messaging-ui-color/254000/71-512.png",
                                height="70px",
                                width="70px",
                                style={"margin-left": "20px"}
                            ),
                        ],
                        style={"display": "flex", "align-items": "center", "width": "100px", "height": "80px"}
                    ),
                    href="/charts",
                    active="exact"
                ),
                dbc.NavLink(
                    html.Div(
                        [
                            "Maps",
                            html.Img(
                                src="https://cdn2.iconfinder.com/data/icons/real-estate-268/512/104_Map_Location_Real_Estate-512.png",
                                height="50px",
                                width="50px",
                                style={"margin-left": "20px"}
                            ),
                        ],
                        style={"display": "flex", "align-items": "center", "width": "100px", "height": "80px"}
                    ),
                    href="/maps",
                    active="exact"
                ),    
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)



content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)


app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    content
])

if __name__=='__main__':
    app.run_server(debug=True)