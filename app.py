import numpy as np
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
df = pd.read_csv('./googleplaystore.csv')

# Convert installs to integer
df['Installs'] = df['Installs'].apply(lambda x: x.replace('+', '') if '+' in str(x) else x)
df['Installs'] = df['Installs'].apply(lambda x: x.replace(',', '') if ',' in str(x) else x)
pd.to_numeric(df.Installs, errors='coerce')

number_of_apps_in_category = df['Category'].value_counts().sort_values(ascending=True)

# print('Number of apps : ', len(df))
# print('Average app rating = ', np.mean(df['Rating']))

groups = df.groupby('Category').filter(lambda x: len(x) >= 170).reset_index()
# print('Average rating = ', np.nanmean(list(groups.Rating)))
c = ['hsl('+str(h)+',50%'+',50%)' for h in np.linspace(0, 720, len(set(groups.Category)))]

# Web app layout
app.layout = html.Div(children=[
    html.H4(
        children='Google Play Store Apps',
        style={
            'textAlign': 'center'
        }
    ),
    html.Div(
        children='Web scraped data of 10k Play Store apps for analysing the Android market.',
        style={
            'textAlign': 'center'
        }
    ),
    dcc.Graph(
        id='data_table',
        figure={
            'data': [
                go.Table(
                    header=dict(
                        values=list(df.columns),
                        line=dict(color='#7D7F80'),
                        fill=dict(color='#a1c3d1'),
                        align=['left'] * 5
                    ),
                    cells=dict(
                        values=[df.App, df.Category, df.Rating, df.Reviews, df.Size, df.Installs, df.Type, df.Price, df.Content_Rating],
                        line=dict(color='#7D7F80'),
                        fill=dict(color='#EDFAFF'),
                        align=['left'] * 5
                    ),
                )
            ]
        }
    ),
    html.Li(
        children='Number of apps : ' + str(len(df)),
        style={
            'textAlign': 'center'
        }
    ),
    dcc.Markdown(
        children='---'
    ),
    html.H5(
        children='Which category has the highest share of (active) apps in the market ?',
        style={
            'textAlign': 'center'
        }
    ),
    dcc.Graph(
        id='data_pie',
        figure={
            'data': [
                go.Pie(
                    labels=number_of_apps_in_category.index,
                    values=number_of_apps_in_category.values,
                    hoverinfo='label+value'
                )
            ]
        }
    ),
    html.Li(
        children='Family and Game apps have the highest market prevelance.',
        style={
            'textAlign': 'center'
        }
    ),
    dcc.Markdown(
        children='---'
    ),
    html.H5(
        children='Apps rating',
        style={
            'textAlign': 'center'
        }
    ),
    dcc.Graph(
        id='data_bar',
        figure={
            'data': [
                go.Histogram(
                    x=df.Rating,
                    xbins={'start': 1, 'size': 0.1, 'end': 5}
                )
            ]
        }
    ),
    html.Li(
        children='Average app rating = ' + str(np.mean(df['Rating'])),
        style={
            'textAlign': 'center'
        }
    ),
    dcc.Markdown(
        children='---'
    ),
    html.H5(
        children='Best performing categories',
        style={
            'textAlign': 'center'
        }
    ),
    dcc.Graph(
        id='data_category_rating',
        figure={
            'data': [{
                'y': df.loc[df.Category == category]['Rating'],
                'type': 'violin',
                'name': category,
                'showlegend': True,
                } for i, category in enumerate(list(set(groups.Category)))
            ],
            'layout': [{
                'title': 'App ratings across major categories',
                'xaxis': {'tickangle': -40},
                'yaxis': {'title': 'Rating'},
                'plot_bgcolor': 'rgb(250,250,250)',
                'shapes': [{
                    'type': 'line',
                    'x0': -.5,
                    'y0': np.nanmean(list(groups.Rating)),
                    'x1': 19,
                    'y1': np.nanmean(list(groups.Rating)),
                    'line': {'dash': 'dashdot'}
                }]
            }]
        }
    ),
    html.Li(
        children='Health and Fitness and Books and Reference produce the highest quality apps with 50% apps having a rating greater than 4.5.',
        style={
            'textAlign': 'left'
        }
    ),
    html.Li(
        children='50%% of apps in the Dating category have a rating lesser than the average rating.',
        style={
            'textAlign': 'left'
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
