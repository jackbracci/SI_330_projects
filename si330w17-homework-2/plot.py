#!/usr/bin/env python

import plotly.plotly as py
import pandas as pd

df_countries = pd.read_csv('nodes.csv', encoding='latin1')
df_countries.head()

df_migration_paths = pd.read_csv('edges.csv')
df_migration_paths.head()

countries = [ dict(
        type = 'scattergeo',
        lon = df_countries['longitude'],
        lat = df_countries['latitude'],
        hoverinfo = 'text',
        text = df_countries['country'],
        mode = 'markers',
        marker = dict(
            size=2,
            color='rgb(255, 0, 0)',
            line = dict(
                width=3,
                color='rgba(68, 68, 68, 0)'
            )
        ))]

migration_paths = []
for i in range( len( df_migration_paths ) ):
    migration_paths.append(
        dict(
            type = 'scattergeo',
            lon = [ df_migration_paths['start_long'][i], df_migration_paths['end_long'][i] ],
            lat = [ df_migration_paths['start_lat'][i], df_migration_paths['end_lat'][i] ],
            hoverinfo = 'none',
            mode = 'lines+markers',
            line = dict(
                width = float(df_migration_paths['count'][i])/float(df_migration_paths['count'].max())* 10,
                color = 'rgb(231, 123, 118)',
            ),
            opacity = 1,
        )
    )

layout = dict(
        title = 'Worldwide migration paths<br>(Hover for country names)',
        showlegend = False,
        geo = dict(
            projection=dict( type='orthographic' ),
            showland = True,
            showcountries = True,
            showocean = True,
            landcolor = 'rgb(233, 213, 172)',
            countrycolor = 'rgb(204, 204, 204)',
            oceancolor = 'rgb(210, 230, 250)',
        ),
    )

fig = dict( data=migration_paths + countries, layout=layout )
py.iplot( fig, filename='d3-migration-paths' )
