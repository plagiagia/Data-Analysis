# Imports
import pandas as pd
import dash
import dash_html_components as html
import dash_table
import dash_core_components as dcc
import plotly.express as px
from dash.dependencies import Input, Output

# Load data
data = pd.read_csv('./restaurants_df.csv')

# Make the app
app = dash.Dash(external_stylesheets=['./assets/style.css'])
default_table = data.sample(10).to_dict('records')

# Build the layout
app.layout = html.Div([
    # Header with paragraph
    html.Div([
        html.H1("Berlin Restaurant Dashboard", className='header-title'),
        html.P("This dashboard shows information about different restaurants in the city", className='header-paragraph')
    ], className='header'),

    # Filters
    html.Div([
        # Category filter
        dcc.Dropdown(id='category-selector',
                     options=[{"label": cat, 'value': cat} for cat in sorted(data['category_title'].unique())],
                     multi=True,
                     value=['German'])
    ], className='filters'),

    # Table
    html.Div([
        dash_table.DataTable(id='table',
                             columns=[{'name': i, 'id': i} for i in data.columns],
                             data=default_table
                             )], className='div-table'),

    # Graph div
    html.Div([
        # MAP
        html.Div([dcc.Graph(id='map-graph', config={"displayModeBar": False}, )], className='card'),
        html.Div([dcc.Graph(id='pie-graph', config={"displayModeBar": False}),
                  dcc.Graph(id='bar-graph', config={"displayModeBar": False})], className='card-double'),
    ], className='graphDiv')

])


@app.callback([Output('map-graph', 'figure'),
               Output('table', 'data'),
               Output('table', 'columns'),
               Output('pie-graph', 'figure'),
               Output('bar-graph', 'figure')],
              [Input('category-selector', 'value')])
def update_page(category):
    if len(category) == 1:
        f_data = data.loc[data['category_title'] == category[0], :]
    else:
        f_data = data.query("category_title in @category")
    fig = px.scatter_mapbox(f_data,
                            lat='restaurant_coordinates_latitude',
                            lon='restaurant_coordinates_longitude',
                            size='restaurant_review_count',
                            color='restaurant_rating',
                            zoom=10,
                            hover_name='restaurant_name',
                            mapbox_style='stamen-terrain',
                            title=f'{", ".join(category)} Restaurants in Berlin')

    columns = [{"name": i, "id": x} for (x, i) in
               zip(['restaurant_name', 'category_title', 'restaurant_rating', 'restaurant_price',
                    'restaurant_review_count',
                    'restaurant_rating', 'restaurant_location_address1', 'restaurant_phone'],
                   ['Name', 'Category', 'Rating', 'Price', 'Reviews', 'Rating', 'Address', 'Phone'])
               ]
    # Pie
    pie = px.pie(f_data, values='restaurant_review_count', names='category_title')
    # Bar
    bar = px.bar(f_data, y='restaurant_name', x='restaurant_rating', text='restaurant_rating')
    bar.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    bar.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')

    return fig, f_data.to_dict('records'), columns, pie, bar


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
