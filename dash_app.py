from flask import Flask, request
import joblib
import json

from jupyter_dash import JupyterDash as Dash
from dash import html, dcc, dash_table, Input, Output, dependencies, State
import dash_bootstrap_components as dbc

import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# create new flask app here
#app = Flask(__name__)


########## SETTING UP THE APPS ##########

flask_app = Flask(__name__)
external_stylesheets = [dbc.themes.BOOTSTRAP]
dash_app = Dash(__name__, external_stylesheets=external_stylesheets, server=flask_app) 
#,requests_pathname_prefix='/dash/') ####

########## HELPER FUNCTIONS ##########

jobs_forecast = pd.read_csv('data/jobs_forecast.csv')
dates = jobs_forecast.date
mytotaldates = {i:datetime.datetime.strptime(x, "%Y-%m-%d").date() for i,x in enumerate(dates)}
a = (list(mytotaldates.keys()))

def create_sliders(X):
    """
    creates sliders for use in user input (continous data) 
    for generating a prediction w/ layoff classification model
    """
    
    slider_items = []
    for column in X:
        label = html.H5(column)
        
        lower_bound = X[column].min()
        upper_bound = X[column].max()
        value = X[column].median()

        slider = dcc.Slider(
            min=lower_bound,
            max=upper_bound,
            value=value, # set median as default
            marks=None,
            tooltip={"always_visible": True},
            id=column # set id based on column name
        )

        item = dbc.ListGroupItem(children=[
            label,
            slider
        ])
        slider_items.append(item)
    return dbc.ListGroup(slider_items)

def layoff_prediction(industry, stage, country, funds_raised): # any other features
    """
    Given the above features, predict whether the company will have
    multiple rounds of layoffs
    """
    with open("model.pkl", "rb") as f:
        model = joblib.load(f)
        
    X = [[industry, stage, country, funds_raised]]
    predictions = model.predict(X)
    # model.predict takes a list of records and returns a list of predictions
    # but we are only making a single prediction
    prediction = int(predictions[0])
    return {"predicted_class": prediction}

def check_prediction(selected_row_data):
    """
    Return an Alert component with information about the model's prediction
    vs. the true class value
    """
    data_copy = selected_row_data.copy()
    actual_class = data_copy.pop("class")
    # remove " (cm)" from labels
    data_cleaned = {k.split(" (cm)")[0].replace(" ", "_"):v for k, v in data_copy.items()} # DONT NEED THIS
    result = layoff_prediction(**data_cleaned)
    predicted_class = result["predicted_class"]
    correct_prediction = predicted_class == actual_class
    if correct_prediction:
        color = "success"
    else:
        color = "danger"
    return dbc.Alert(f"Predicted class: {predicted_class}", color=color)

######### LAYOUT / COMPONENTS #########

jobs_forecast = pd.read_csv('data/jobs_forecast.csv')
jobs_forecast.date = pd.to_datetime(jobs_forecast.date)

#graphs
# Create figure with secondary y-axis
fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.add_trace(
    go.Scatter(x=sector['Date'], y=sector['Market Cap'], name="Market Cap", mode='lines'),
    secondary_y=False,
)
fig.add_trace(
    go.Scatter(x=sector['Date'], y=sector['Earnings'], name="Earnings", mode='lines'),
    secondary_y=True,
)
fig.update_layout(
    title_text="Tech Sector Market Cap & Earnings <br><sup>Source: Simple Wall Street</sup>"
)
fig.update_xaxes(title_text="Date")
fig.update_yaxes(title_text="<b>Market Cap</b>", secondary_y=False)
fig.update_yaxes(title_text="<b>Earnings</b>", secondary_y=True)

fig2 = px.bar(total_layoffs_by_month, x="month", y="total_laid_off", 
              title='Total Layoffs, Globally <br><sup>Source: layoffs.fyi</sup>', 
              color_discrete_sequence=["red"])

fig3 = px.line(census_data_seas_sectors[(census_data_seas_sectors['time']>='2020') & 
                                       (census_data_seas_sectors['sector']=='Information')], 
               x="time", y="cell_value",
               title='Business Formations, Information Sector, 2020 and later \
                       <br><sup>Source: U.S. Census Bureau</sup>', 
               color='sector', 
               color_discrete_sequence=['magenta'])

tech_stocks = pd.read_csv('data/IXN_ETF.csv')
fig4 = px.line(tech_stocks, x='date', y='close_px', 
               title='Global Tech iShares ETF (IXN), Closing Price \
                       <br><sup>Source: Yahoo Finance</sup>')

# prediction_layout = html.Div(children=[
#     create_sliders(X),
#     dbc.Alert("Prediction will go here", color="info", id="prediction-output")
# ]) 

markdown = dcc.Markdown("""
## 

Given the massive recent layoffs in the tech sector, I thought it would
be helpful to take a deeper look at the state of the tech market to get a 
sense of what is really going on behind the scenes -- and to see
whether there is hope for any of us out there who are looking for a job.

This dashboard is split into three sections - the first will give a general 
sense of economic conditions in the sector and more generally, the second
will take a closer look at recent layoffs and predict whether companies
will experience multiple rounds or just a one off, and the third will 
focus on job postings.

""")

past_data_layout = html.Div(children=[
    html.Div(markdown),
    html.Div(
        [dcc.Graph(figure=fig, style={"height":"520px"}), 
         dcc.Graph(figure=fig4, style={"height":"520px"}),
         dcc.Graph(figure=fig2, style={"height":"520px"}), 
         dcc.Graph(figure=fig3, style={"height":"520px"})
        ])
])

layoffs_layout = html.Div(children=[
    
    html.Div(
        [dcc.Graph(figure=fig5, style={"height":"520px"}),
         dcc.Graph(figure=fig6, style={"height":"520px"}),
         dcc.Graph(figure=fig7, style={"height":"520px"}),
         dcc.Graph(figure=fig8, style={"height":"520px"}),
         dcc.Graph(figure=fig9, style={"height":"520px"}),
        ])
])



## DROPDOWN ##
job_forecast_layout = html.Div(children=[
    html.Img(src='assets/job_forecast.png'),
    html.P("Select a date: "),
    html.Div([dcc.Dropdown(className = 'date_input', id='Datedropdown', 
                 options=[{'label': str(v), 'value': v} for v in mytotaldates.values()],
                 value=a[-1]
            ),
        html.Div(id='OutputContainer'), 
        
        #Calculate and Reset Buttons
        html.Div(
            [
                html.Button('Reset', id='btn_reset', n_clicks=0, 
                className= "btn_reset"),
                html.Button('Calculate', id='btn_calculate', n_clicks=0, 
                            className = "btn_calculate"),
            ],
         className="date_input", id="job-buttons"                         
         ),
            html.Div(id='OutputContainer2')

    ]) 
])


tabs = dbc.Tabs(children=[
        #tab1,
        dbc.Tab(past_data_layout, label="Economic Conditions"),
        dbc.Tab(layoffs_layout, label="Layoffs Dashboard"),
        dbc.Tab(job_forecast_layout, label="Job Postings")
    ])

####

dash_app.layout = dbc.Container(children=[
    html.H1("State of the Tech Labor Market"),
    tabs
])

########## CALLBACKS ##########

@dash_app.callback(Output('OutputContainer', 'children'), 
                   [Input('Datedropdown', 'value')]) # or Dateslider
def rangerselection(val):
    val = jobs_forecast.date[val]
    #return f'Selected Date: {str(value)}'
    return f"Predicted job postings, relative to Jan 2020: \
            {float(jobs_forecast.prediction[jobs_forecast.date==val])}"

@dash_app.callback(
    Output('OutputContainer', 'children'),
    [Input('btn_calculate', 'n_clicks')],
    [State('OutputContainer', 'value')],
)

def job_pred(n_clicks, value):
    if(n_clicks):
        return print(str(value)) #float(jobs_forecast.prediction[jobs_forecast.date==val])
    else:
        return('Error')

def render_information(rows, selected_rows):
    if selected_rows:
        # selection is set to "single" so there will be exactly 1 selected row
        selected_row_data = rows[selected_rows[0]]      
        return html.Div(dbc.Row(children=[
            dbc.Col(create_image_card(selected_row_data)),
            dbc.Col(children=[
                create_list_group(selected_row_data),
                html.Hr(),
                check_prediction(selected_row_data)
            ])
        ]))

########## ROUTES ##########

@flask_app.route('/predict', methods=['POST'])
def predict():
    request_json = request.get_json()
    result = iris_prediction(**request_json) ## need to fix
    return json.dumps(result)

## NEED TO ADD RESET