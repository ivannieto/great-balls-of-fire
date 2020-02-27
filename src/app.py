"""
This data visualization makes use of Fireballs NASA data open API, describing
all bolid impact events in Earth, registered by US goverment since 1988.

<https://ssd-api.jpl.nasa.gov/doc/fireball.html>

Field 	  Description
__________________________________________________________________________
date........date/time of peak brightness (GMT)
lat.........latitude at peak brightness (degrees)
lon.........longitude at peak brightness (degrees)
lat-dir.....latitude direction (“N” or “S”)
lon-dir.....latitude direction (“E” or “W”)
alt.........altitude above the geoid at peak brightness (km)
vel.........velocity at peak brightness (km/s)
energy......approximate total radiated energy (joules)
impact-e....approximate total impact energy (kt)
vx..........pre-entry estimated velocity (Earth centered X component, km/s)
vy..........pre-entry est. velocity (Earth centered Y component, km/s)
vz..........pre-entry est. velocity (Earth centered Z component, km/s)

"""

import os

import color_scale
import dash

import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import plotly.graph_objs as go

from dash.dependencies import Input, Output
from process_df import process_df


mapbox_access_token = 'pk.eyJ1IjoiaXZhbm5pZXRvIiwiYSI6ImNqNTU0dHFrejBkZmoycW9hZTc5NW42OHEifQ._bi-c17fco0GQVetmZq0Hw'

app = dash.Dash(name=__name__)
app.config.supress_callback_exceptions = True

server = app.server
server.secret_key = os.environ.get('secret_key', 'secret')

# Color scale for heatmap (green-to-red)
color_scale = color_scale.GREEN_RED

# Load styles
css_url = 'https://codepen.io/IvanNieto/pen/bRPJyb.css'
css_bootstrap_url = 'https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.6/css/bootstrap.min.css'
app.css.append_css({
    "external_url": [css_bootstrap_url, css_url],
})

# Read CSV file
if(os.path.isfile('src/data/filtered_data.csv')):
    df = pd.read_csv('src/data/filtered_data.csv')
else:
    df = pd.read_csv('src/data/fireballs.csv')
    df = process_df(df)
    df.to_csv('src/data/filtered_data.csv', index=False)


dfmax = df.groupby('year', as_index=False)[
    'alt', 'vel', 'impact-e', 'energy'].max()

dfmean = df.groupby('year', as_index=False)[
    'alt', 'vel', 'impact-e', 'energy'].mean()

dfmedian = df.groupby('year', as_index=False)[
    'alt', 'vel', 'impact-e', 'energy'].median()

# Get all valuable column headers
to_skip = ['lat', 'lat-dir', 'lon', 'lon-dir', 'year', 'date']
main_columns = [x for x in df.columns if x not in to_skip]

# Filter impact-e values < 10kt
df['impact-e'] = np.clip(df['impact-e'].values, 10, df['impact-e'].max())

# Layout generation
app.layout = html.Div([
    # LANDING
    html.Div(
        className='section',
        children=[
            html.H1('GREAT BALLS OF FIRE', className='landing-text')
        ]
    ),
    html.Div(
        className='content',
        children=[
            # SLIDER ROW
            html.Div(
                className='col',
                children=[
                  html.Div(
                      id='slider',
                      children=[
                          dcc.Slider(
                              id='date-slider',
                              min=min(df['year']),
                              max=max(df['year']),
                              marks={str(date): str(date)
                                     for date in df['year'].unique()},
                              value=2015,
                          ),
                      ], style={
                          'background': '#191a1a',
                          'margin-bottom': '50px'
                      }
                  )
                ], style={
                    'background': '#191a1a',
                }),
            # GRAPHS ROW
            html.Div(
                id='graphs',
                className='row',
                children=[
                    html.Div(
                        className='col-4',
                        children=[
                          dcc.Graph(
                              id='freq-graph',
                          ),
                        ]),
                    html.Div(
                        className='col-4',
                        children=[
                            dcc.Graph(
                                id='another-graph',
                            ),
                        ]),
                    html.Div(
                        className='col-4',
                        children=[
                            dcc.Graph(
                                id='plot-graph',
                            ),
                        ])
                ], style={
                    'padding-bottom': 100
                }
            ),
            # INFO ROW
            html.Div(
                id='group-x',
                className='row',
                children=[
                    html.Div(
                        className='col-6',
                        children=[
                          html.Div(
                              className='row',
                              children=[
                                  html.Div(
                                      className='col-3',
                                      children=[
                                          html.H1(
                                              id='this-year',
                                              style={
                                                  'fontSize': 60,
                                                  'color': '#FFF'
                                              }
                                          ),
                                      ]
                                  ),
                                  html.Div(
                                      className='col-3',
                                      children=[
                                          html.H3(
                                              'Max radiated impact energy',
                                              id='this-year-1st',
                                              style={
                                                  'fontSize': 12,
                                                  'color': '#FFF'
                                              }
                                          ),
                                          html.H1(
                                              id='max-energy',
                                              style={
                                                  'fontSize': 30,
                                                  'color': '#FFF'
                                              }
                                          )
                                      ]),
                                  html.Div(
                                      className='col-3',
                                      children=[
                                          html.H3(
                                              'Max velocity at peak brightness',
                                              id='this-year-2nd',
                                              style={
                                                  'fontSize': 12,
                                                  'color': '#FFF'
                                              }
                                          ),
                                          html.H1(
                                              id='max-velocity',
                                              style={
                                                  'fontSize': 30,
                                                  'color': '#FFF'
                                              }
                                          )
                                      ]),
                                  html.Div(
                                      className='col-3',
                                      children=[
                                          html.H3(
                                              'Max impact energy',
                                              id='this-year-3rd',
                                              style={
                                                  'fontSize': 12,
                                                  'color': '#FFF'
                                              }
                                          ),
                                          html.H1(
                                              id='max-impact-e',
                                              style={
                                                  'fontSize': 30,
                                                  'color': '#FFF'
                                              }
                                          )
                                      ])
                              ]),

                        ]),
                    html.Div(
                        className='col-3',
                        children=[
                            dcc.Dropdown(
                                id='xaxis-dd',
                                className='col',
                                options=[{'label': i, 'value': i}
                                         for i in main_columns],
                                value='energy',
                            ),
                            html.Div(
                                className='col radius-group',
                                children=[
                                    dcc.RadioItems(
                                        id='xaxis-type',
                                        options=[
                                          {'label': i, 'value': i} for i in ['Linear', 'Log']
                                        ],
                                        value='log',
                                        labelStyle={
                                            'color': '#FFF'
                                        }
                                    ),
                                ])
                        ]),
                    html.Div(
                        className='col-3',
                        children=[
                            dcc.Dropdown(
                                id='yaxis-dd',
                                className='col',
                                options=[{'label': i, 'value': i}
                                         for i in main_columns],
                                value='vel',
                            ),
                            html.Div(
                                className='col radius-group',
                                children=[
                                    dcc.RadioItems(
                                        id='yaxis-type',
                                        options=[
                                          {'label': i, 'value': i} for i in ['Linear', 'Log']
                                        ],
                                        value='log',
                                        labelStyle={
                                            'color': '#FFF'
                                        }
                                    ),
                                ])
                        ]),
                ]
            ),
            # MAP ROW
            html.Div(
                className='row',
                children=[
                    # Main graph holding the map
                    dcc.Graph(
                        id='map-graph',
                        animate=True,
                        style={
                          'width': '100%',
                          'height': 800,
                        }
                    ),
                ]),
            # ABOUT ROW
            html.Div(
                className='row',
                children=[
                  html.Div(
                    className='col',
                    children=[
                      html.P(
                        'Data extracted from:'
                      ),
                      html.A(
                          'NASA Fireballs open API',
                          href='https://ssd-api.jpl.nasa.gov/doc/fireball.html'
                      )                    
                    ]
                  ),
                  html.Div(
                    className='col',
                    children=[
                      html.P(
                        'Code avaliable at:'
                      ),
                      html.A(
                          'BitBucket',
                          href='https://bitbucket.org/inieto/great-balls-of-fire/'
                      )                    
                    ]
                  ),
                  html.Div(
                    className='col',
                    children=[
                      html.P(
                        'Made with:'
                      ),
                      html.A(
                          'Dash / Plot.ly',
                          href='https://plot.ly/dash/'
                      )                    
                    ]
                  ),
                  html.Div(
                    className='col',
                    children=[
                      html.P(
                        'Developer:'
                      ),
                      html.A(
                          'Ivan Nieto',
                          href='https://twitter.com/IvanNietoS'
                      )                    
                    ]
                  )                                                          
                ]
            )
        ],
        style={
            'padding': 40
        }
    )
]
)


@app.callback(
    Output('this-year', 'children'),
    [Input('date-slider', 'value')]
)
def update_text(year_value):
    """
    Callbacks for year text col
    """
    return str(year_value)


@app.callback(
    Output('max-energy', 'children'),
    [Input('date-slider', 'value')]
)
def update_text(year_value):
    """
    Callback for energy digit col
    """    # data from current selected year
    dff = df[df['year'] == year_value]
    return '{} joules'.format(str(dff['energy'].max()))


@app.callback(
    Output('max-velocity', 'children'),
    [Input('date-slider', 'value')]
)
def update_text(year_value):
    """
    Callbacks for velocity digit col
    """
    # data from current selected year
    dff = df[df['year'] == year_value]
    if(np.isnan(dff['vel'].max())):
        return 'N/A'
    return '{} km/h'.format(dff['vel'].max())


@app.callback(
    Output('max-impact-e', 'children'),
    [Input('date-slider', 'value')]
)
def update_text(year_value):
    """
    Callback for impact-e text col
    """
    # data from current selected year
    dff = df[df['year'] == year_value]
    return '{} kt'.format(str(dff['impact-e'].max()))


@app.callback(
    Output('freq-graph', 'figure'),
    [Input('date-slider', 'value')]
)
def update_graph(year_value):
    """
    Top Left graph callback
    """

    data = go.Data([
        go.Scatter(
            name='Max impact-e',
            # events qty
            x=np.arange(1988, year_value),
            # year
            y=dfmax['impact-e'],
            mode='lines',
            marker={
                'symbol': 'circle',
                'size': 5,
                'color': '#eb1054'
            },
            hoverlabel={
                'bgcolor': '#FFF',
            },
        ),
        go.Scatter(
            name='Mean impact-e',
            # events qty
            x=np.arange(1988, year_value + 1),
            # year
            y=dfmean['impact-e'],
            mode='lines',
            marker={
                'symbol': 'circle',
                'size': 5,
                'color': '#C2FF0A'
            },
            hoverlabel={
                'bgcolor': '#FFF',
            },
        ),
        go.Scatter(
            name='Median impact-e',
            # events qty
            x=np.arange(1988, year_value + 1),
            # year
            y=dfmedian['impact-e'],
            mode='lines',
            marker={
                'symbol': 'circle',
                'size': 5,
                'color': '#52e5ec'
            },
            hoverlabel={
                'bgcolor': '#FFF',
            },
        ),
    ])
    layout = go.Layout(
        xaxis={
            'autorange': True,
            'color': '#FFF',
            'title': 'year',
        },
        yaxis={
            'autorange': True,
            'color': '#FFF',
            'title': 'approximate total impact energy (kt)',
        },
        margin={
            'l': 40,
            'b': 40,
            't': 10,
            'r': 0
        },
        hovermode='closest',
        paper_bgcolor='#191a1a',
        plot_bgcolor='#191a1a',
    )

    return go.Figure(
        data=data,  # 54b4e4
        layout=layout
    )


@app.callback(
    Output('another-graph', 'figure'),
    [Input('date-slider', 'value')]
)
def update_mid(year_value):
    """
    Top Mid graph callback
    """

    traces = []
    marker_color = ''

    for year in df['year'].unique():
        if year < 2003:
            continue
        dff = df[df['year'] == year]
        if(year == year_value):
            marker_color = '#C2FF0A'
        elif year_value >= 2003:
            marker_color = '#FF0A47'
        else:
            marker_color = '#333333'
        trace = go.Box(
            name=year,
            y=dff['vel'],
            jitter=0.5,
            whiskerwidth=0.2,
            fillcolor=marker_color,
            marker=dict(
                size=2,
            ),
            line=dict(color=marker_color, width=1),
        )
        traces.append(trace)

    data = go.Data(traces,
                   style={
                       'color': '#000'})

    layout = go.Layout(
        yaxis=dict(
            title='year',
            autorange=True,
            zeroline=True,
            gridwidth=1,
            zerolinecolor='rgb(255, 255, 255)',
            zerolinewidth=2,
        ),
        hoverlabel={
            'bgcolor': '#FFF',
            'font': {
                'color': 'black'
            },
        },
        margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
        hovermode='closest',
        paper_bgcolor='#191a1a',
        plot_bgcolor='#191a1a',
    )

    return go.Figure(
        data=data,
        layout=layout
    )


@app.callback(
    Output('plot-graph', 'figure'),
    [Input('date-slider', 'value'),
     Input('xaxis-dd', 'value'),
     Input('xaxis-type', 'value'),
     Input('yaxis-dd', 'value'),
     Input('yaxis-type', 'value')]
)
def update_plot(year_value, xaxis_value, xaxis_type, yaxis_value, yaxis_type):
    """
    Top Right graph callback
    """

    dff = df[df['year'] == year_value]
    data = go.Data([
        go.Scatter(
            x=dff[xaxis_value],
            y=dff[yaxis_value],
            text=dff['legend'],
            mode='markers',
            marker={
                'symbol': 'circle',
                'size': dff['impact-e'],
                'color': '#C2FF0A'
            },
            hoverlabel={
                'bgcolor': '#FFF',
                'font': {
                    'color': 'black'
                },
            },
        )
    ],
        style={
        'color': '#FFF'})

    layout = go.Layout(
        autosize=True,
        xaxis={
            'color': '#FFF',
            'autorange': True,
            'title': xaxis_value,
            'type': 'Linear' if xaxis_type == 'Linear' else 'log',
            'showspikes': True
        },
        yaxis={
            'color': '#FFF',
            'autorange': True,
            'title': yaxis_value,
            'type': 'Linear' if yaxis_type == 'Linear' else 'log'
        },
        margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
        hovermode='closest',
        paper_bgcolor='#191a1a',
        plot_bgcolor='#191a1a',
    )

    return go.Figure(
        data=data,
        layout=layout
    )


@app.callback(
    Output('map-graph', 'figure'),
    [Input('date-slider', 'value')]
)
def update_map(year_value):
    """
    Map graph callback
    """

    # Update dataframe with the passed value
    dff = df[df['year'] == year_value]

    # Paint mapbox into the data
    data = go.Data([
        go.Scattermapbox(
            lat=dff['lat'],
            lon=dff['lon'],
            mode='markers',
            marker=go.Marker(
                # size=dff['vel']
                size=dff['impact-e'],
                colorscale=color_scale,
                cmin=dff['impact-e'].min(),
                color=dff['impact-e'],
                cmax=dff['impact-e'].max(),
                colorbar=dict(
                    title='Impact'
                ),
                opacity=0.5
            ),
            text=dff['legend'],
            hoverlabel={
                'bordercolor': 'transparent',
                'font': {
                    'color': '#FFF'
                }
            }
        )
    ],
        style={
        'height': 800
    }
    )

    # Layout and mapbox properties
    layout = go.Layout(
        autosize=True,
        hovermode='closest',
        mapbox=dict(
            accesstoken=mapbox_access_token,
            bearing=0,
            pitch=0,
            zoom=1.8,
            style='dark'
        ),
        paper_bgcolor='#191a1a',
        plot_bgcolor='#191a1a',
    )

    return go.Figure(
        data=data,
        layout=layout
    )


# Run dash server
if __name__ == '__main__':
    app.run_server(debug=True)
