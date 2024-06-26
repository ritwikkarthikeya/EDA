# Import required libraries
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go

# Read the dataframe
spacex_df = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv')

# Create a dash application
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True

# Build dash app layout
# Build dash app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard', style={'textAlign': 'center'}),
    html.Div([
        html.H2('Select Year:', style={'margin-right': '2em'}),
        dcc.Dropdown(
            id='site-dropdown',
            options=[
                {'label': 'All Sites', 'value': 'ALL'},
                {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
            ],
            value='ALL',
            placeholder='Select a Launch Site here',
            searchable=True
        )
    ]),
    html.Div([
        html.Div([], id='success-pie-chart')
    ]),
    html.Div([
        dcc.Graph(id='success-payload-scatter-chart')
    ]),
    dcc.RangeSlider(
        id='payload-slider',
        min=0, max=10000, step=1000,
        marks={0: '0', 100: '100', 15600: '15600'},
        value=[0, 15600]
    ),            
])


# Function decorator to specify function input and output
@app.callback(
    Output(component_id='success-pie-chart', component_property='children'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
   filtered_df = spacex_df
   if entered_site == 'ALL':
    success_count1 = spacex_df[(spacex_df['class'] == 1) & (spacex_df['Launch Site'] == 'CCAFS LC-40')]['class'].count()
    success_count2 = spacex_df[(spacex_df['class'] == 1) & (spacex_df['Launch Site'] == 'VAFB SLC-4E')]['class'].count()
    success_count3 = spacex_df[(spacex_df['class'] == 1) & (spacex_df['Launch Site'] == 'KSC LC-39A')]['class'].count()
    success_count4 = spacex_df[(spacex_df['class'] == 1) & (spacex_df['Launch Site'] == 'CCAFS SLC-40')]['class'].count()
    labels = ['s1', 's2', 's3', 's4']
    values = [success_count1, success_count2, success_count3, success_count4]

    fig = px.pie(
        values=values,
        names=labels,
        title='Success/Failure Counts for All Sites'
    )
    return dcc.Graph(figure=fig)

   else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        success_count = filtered_df[filtered_df['class'] == 1]['class'].count()
        failure_count = filtered_df[filtered_df['class'] == 0]['class'].count()
        labels = ['Success', 'Failure']
        values = [success_count, failure_count]

        fig = px.pie(
            values=values,
            names=labels,
            title='Success/Failure Counts for {}'.format(entered_site)
        )
        return dcc.Graph(figure=fig)
   
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
   [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")])
              

def get_scaterr(selected, payload_range):
    print("Selected site:", selected) 
    if selected == 'ALL':
        filtered_df = spacex_df
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected]

    filtered_df = filtered_df[(filtered_df['Payload Mass (kg)'] >= payload_range[0]) & (filtered_df['Payload Mass (kg)'] <= payload_range[1])]
    fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category',title=f'Scatter Plot of Payload Mass vs. Launch Outcome for {selected}',
                     labels={'Payload Mass (kg)': 'Payload Mass (kg)', 'class': 'Launch Outcome'})
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
