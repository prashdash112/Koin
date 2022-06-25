########################### Importing Libraries #############################################
import numpy as np 
import pandas as pd
from dash import dcc,html,Dash,Input,Output
import plotly.express as px
import warnings
warnings.filterwarnings("ignore")
from api_to_df import extractor,api_df
#from api_to_df import open_df,high_df,low_df,close_df,volume_df,mkt_cap_df
###########################################################################################

# Defining app name 
app = Dash(__name__)

colors = {
    'background': '#231F20',
    'text': '#ADD8E6'
}
############### Defining elements for dropdowns ####################################################

ticker_list = ["ETH", "XRP", "BTC", "LTC", "LRC", "DOT", "MANA", "EGLD", "SHIB", "SOL", "TFUEL", "ICP", "SAND", "MATIC"]
type_list = ["open", "high", "low", "close", "volume", "mkt_cap"]
currency_list  = ["USD"]
############################################################################################################
markdown_text = '''

Koin: A crypto webapp for newbies.

'''

def generate_table(dataframe, max_rows=15):
    '''

    generate_table function is used to parse pandas dataframes into html tables.
    
    '''
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

# Div is used to create divisions in an html block
# children is a subbranch of an Division tree
app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[ 
    # H1 is header 1 i.e Heading of the webapp
    html.H1(
        children='KOIN',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    
    # style is used to style a particular dash/html component
    #dcc.markdown is used to add markdown/text info to the frontend
    html.Div(children =[dcc.Markdown(children=markdown_text,
        style={
        'textAlign': 'center',
        'color': colors['text'] }
         )
         ]
         ),
    
    #Inside children branch, a dcc dropdown component is created to add filters
    html.Div(children =[html.Label('Ticker symbol'),
            dcc.Dropdown(id='ticker_dropdown',
                options=[{'label': x, 'value': x} for x in ticker_list] ,style={'color':'#000000'})
            ], 
            style={'color': colors['text'],'padding': 10, 'flex': 1} 
            ),

    html.Div(children =[html.Label('Data type'),
             dcc.Dropdown(id='type_dropdown',
                          options=[{'label': x, 'value': x} for x in type_list],
                          style={'color':'#000000'})
             ], 
             style={'color': colors['text'],'padding': 10, 'flex': 1} 
             ),

    html.Div(children = [html.Label('Currency'),
             dcc.Dropdown(id='currency_dropdown',
                 options=[{'label': x, 'value': x} for x in currency_list], style={'color':'#000000'})
             ], 
             style={'color': colors['text'],'padding': 10, 'flex': 1}
             ),

    #html.H2(children='Crypto price',style={'color':colors['text']}),
    
    #Adding generate_table function to html division
    html.Div([html.Div(id = 'table',style={'width': '10%', 'display': 'inline-block','color':colors['text']})
            , html.Div([dcc.Graph(id='graph',figure={})], style={'width': '90%', 'display': 'inline-block'}) ], style={'display': 'flex'}),
    #dcc.graph is used to parse plotly graphs to html
    #dcc.Graph(
    #    id='graph',
    #    figure={}
    #)
]
)

@app.callback(
    Output('table','children'),
    Output('graph','figure'),
    [Input('ticker_dropdown', 'value'),
    Input('currency_dropdown', 'value'),
    Input('type_dropdown', 'value')],
    prevent_initial_call = True,
    prevent_initial_callbacks = True
) 

def update_figure(tck,curr,type) :
    #df = type_value[select_type]
    final_df  = api_df(extractor(tck,curr))
    op_df = final_df[['date',type]]
    table = generate_table(op_df)
    fig = px.line(op_df, x  = 'date', y =op_df.columns[1] )
                 

    # Updating the layout of the figure 
    fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text'],
    transition_duration=500
    )
    return table,fig



if __name__ =="__main__":
    app.run_server(debug=False)


# As of now, the idea is to use the api_df & extrctor function inside update graph func to update the graphs 
# 1) the api_df&Extractor will run, produces the desiered ops like open_df, etc 
# 2) We'll import that info in the main file(app.py) & utilize it inside the graph update func to produce the final graph op.
