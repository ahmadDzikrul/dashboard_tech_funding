from dash import dcc,html, Dash, dash_table
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(name='Technology Companies Funding Dashboard', external_stylesheets=external_stylesheets)
app.title = 'Technology Companies Funding Dashboard'

df = df = pd.read_csv("tech_fundings.csv")
df_new = df[df["Funding Amount (USD)"] != "Unknown"]
df_new = df_new.reset_index().iloc[:,2:]
df_new["Vertical"] = df_new["Vertical"].astype("category")
region_fix = []
for i in df_new["Region"]:
    if i == "Unkown":
        region_fix.append("Unknown")
    else:
        region_fix.append(i)
df_new["Region"] = region_fix
df_new["Region"] = df_new["Region"].astype("category")
funding_stage_fix = []
for i in df_new["Funding Stage"]:
    if i == "Unkown":
        funding_stage_fix.append("Unknown")
    else:
        funding_stage_fix.append(i)
df_new["Funding Stage"] = funding_stage_fix
df_new["Funding Stage"] = df_new["Funding Stage"].astype("category")
df_new["Funding Date Category"] = df_new["Funding Date"].astype("category")
df_new["Funding Amount (USD)"] = df_new["Funding Amount (USD)"].astype("float")
df_new["Funding Date"] = pd.to_datetime(df_new["Funding Date"],format = "%b-%y")

list_date_category= list(df_new["Funding Date Category"].unique())

def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns], style={"font-size":"1.2vw",'padding-right': '1px'})
        ),
        html.Tbody([
            html.Tr([
                html.Td([round(dataframe.iloc[i][col],2)],style={"font-size":"0.9vw",'padding-right': '1px'}) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])


# create dropdown option
dropdown_option_plot4 = [{"label":"All Country","value":"All Country"}]
unique_country = df_new['Region'].unique()
for i in unique_country:
    if str(i) != "nan":
        dropdown_option_plot4.append({"label":str(i),"value":str(i)})

dropdown_category = [
    {"label":"Funding Amount VS Region","value":"Funding Amount VS Region"},
    {"label":"Funding Amount VS Vertical (Industry)","value":"Funding Amount VS Vertical"},
    {"label":"Funding Amount VS Funding Stage","value":"Funding Amount VS Funding Stage"}
]


statistic_table = html.Div()

app.layout = html.Div(children=[
    html.Br(),
    html.H1(children="TECHNOLOGY COMPANIES FUNDING DURING 2020-2021",style={'textAlign': 'center', 'color':"#FFFFFF"}),

    html.Div([
        dcc.Tabs([
            dcc.Tab(label='Table', children=[
                html.Div([
                    html.H4(children='Technology Company Funding Data Table'),
                    dash_table.DataTable(
                        df_new.to_dict("records"),
                        [{"name": i, "id": i} for i in df_new.columns],
                        filter_action="native",
                        filter_options={"placeholder_text": "Filter column..."},sort_action="native",
                        sort_mode='multi',
                        page_size=10,
                        style_as_list_view=True,
                        style_data={
                            'color': 'black',
                            'backgroundColor': 'white'
                        },
                        style_cell_conditional=[
                                {
                                    'textAlign': 'left'
                                }
                            ],
                        style_data_conditional=[
                            {
                                'if': {'row_index': 'even'},
                                'backgroundColor': '#79bded',                                
                            }
                        ],
                        style_header={
                            'backgroundColor': '#2570dd',
                            'color': 'white',
                            'fontWeight': 'bold'
                        }
                    )
                    ], style={'padding': '10px 10px 10px 10px'})
            ]),
            dcc.Tab(label='Visualization', children=[
                html.Div([
                        dbc.Card([
                            dbc.CardHeader('Select Category'),
                            dbc.CardBody([
                                dcc.Dropdown(
                                    id="dropdown_category",
                                    options=dropdown_category,
                                    value="Funding Amount VS Region"
                                ),
                            ]),
                        ], style={'padding': '10px 10px 10px 10px'}),
                        dcc.RadioItems(
                                        ['Top 10', 'Bottom 10', 'All'],
                                        'Top 10',
                                        id='category_radio_filter',
                                        labelStyle={'display': 'inline-block', 'marginTop': '5px','padding': '10px 10px 10px 10px'}
                                    ),
                        dcc.Graph(
                            id='plot_category'
                        ),

                        html.Div([
                            dbc.Card([
                                dbc.CardHeader('Select Country'),
                                dbc.CardBody([
                                    dcc.Dropdown(
                                        id="plot4_dropdown",
                                        options=dropdown_option_plot4,
                                        value="All Country"
                                    ),
                                ]),
                            ]),
                            html.Br(),
                            html.Br(),
                            dcc.Graph(
                                id='plot4'
                            ),
                            html.Div(dcc.RangeSlider(
                                    min =0,
                                    max = len(df_new["Funding Date Category"].unique())-1,
                                    step=1,
                                    id='slider_fig4',
                                    value=[0,len(df_new["Funding Date Category"].unique())-1],
                                    marks={i: {"label":str(df_new['Funding Date Category'].unique()[i]),"style": {"transform": "rotate(45deg)", "white-space": "nowrap"}} for i in range(len(df_new['Funding Date Category'].unique()))}
                                ),style={'width': '90%', 'display': 'inline-block','padding': '0px 20px 20px 50px'})
                        ],style={'width': '50%', 'display': 'inline-block','padding': '10px 10px 0px 10px'}
                        ),
                        
                        html.Div([
                            html.Div([
                                html.H4(children='Descriptive Statistics'),
                                statistic_table
                                ], style={'padding': '0px 0px 5px 5px'}),
                            html.Div([
                                dcc.Graph(
                                    id= 'plot5'
                                )
                                ], style={'padding': '0px 0px 5px 5px'})
                        ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'}
                        )
                ])
            ])
        ])
    ]),
    html.Div([
        html.P(['Copyright 2022'], style={'textAlign':'center', 'color':'#ffffff','padding': '0px 0px 0px 0px'}),
        html.P(['Ahmad Dzikrul Fikri'], style={'textAlign':'center', 'color':'#ffffff','padding': '0px 0px 0px 0px'})
        
    ],style={'backgroundColor':'#1e1c1c','padding': '30px 0px 10px 0px'})
], style = {'backgroundColor': 'black','color': '#63a7e5'})

@app.callback(
    Output(component_id='plot4', component_property='figure'), # graph component for output
    Output(statistic_table, component_property='children'), # table component for output
    Input(component_id='plot4_dropdown', component_property='value'), # component from dropdown
    Input(component_id='slider_fig4', component_property='value') # component from dropdown
)
def update_graph4(value_dropdown_plot4,slider):
    if value_dropdown_plot4 == "All Country":
        df_new_plot4 = df_new
    else:
        df_new_plot4 = df_new[df_new["Region"] == value_dropdown_plot4]

    list_date_category_unique= list(df_new_plot4["Funding Date Category"].unique())

    value_awal = list_date_category[slider[0]]
    value_akhir = list_date_category[slider[1]]

    list_nomor = []
    for i in range(len(list_date_category)):
        if list_date_category[i] in list_date_category_unique:
            list_nomor.append(i)

    nomor_awal = slider[0]
    while nomor_awal not in list_nomor:
        nomor_awal+=1

    nomor_akhir = slider[1]
    while nomor_akhir not in list_nomor:
        nomor_akhir -=1

    value_awal = list_date_category[nomor_awal]
    value_akhir = list_date_category[nomor_akhir]

    value_akhir_graph = list_date_category_unique[-1]
    value_awal_graph = list_date_category_unique[0]

    list_date_category_graph4 = list(df_new_plot4["Funding Date Category"])
    index_awal = list_date_category_graph4.index(value_awal)

    index_akhir = 0
    if value_akhir == value_akhir_graph:
        index_akhir = len(df_new_plot4)
    else:
        index_akhir = list_date_category_graph4.index(value_akhir)
        while list_date_category_graph4[index_akhir] == value_akhir:
            index_akhir +=1
    df_new_plot4 = df_new_plot4.iloc[index_awal:index_akhir]
    cek = df_new_plot4
    print(cek)
    fundXfunding_date = pd.crosstab(index=df_new_plot4["Funding Date"],
            columns='Amount',
            colnames=' ',
                values = df_new["Funding Amount (USD)"],
            aggfunc = "sum").sort_values(by="Funding Date")

    fig4 = px.line(fundXfunding_date.reset_index(),
    x="Funding Date",
    y="Amount",
    title=value_dropdown_plot4+' Sum of Funding During the Time',
    template = 'plotly_dark',
    markers=True)
    fig4.update_traces(marker_color='#63a7e5',line=dict(color='firebrick', width=4))
    # print(df_new_plot4)
    df_table_fig4 = df_new_plot4.describe().rename(columns = {"index":""}).T
    return fig4, generate_table(df_table_fig4)


country_lama = 'All Country'
@app.callback(
    Output(component_id='plot5', component_property='figure'), # graph component for output
    Input(component_id='plot4_dropdown', component_property='value'), # component from dropdown
    Input(component_id='plot4', component_property='hoverData') # component from hover
)
def update_graph_hover(value_dropdown_plot4, hoverData):
    global country_lama
    if value_dropdown_plot4 == "All Country":
        df_new_plot5 = df_new
    else:
        df_new_plot5 = df_new[df_new["Region"] == value_dropdown_plot4]

    if str(hoverData).lower() != "none" and country_lama == value_dropdown_plot4:
        df_new_plot5 = df_new_plot5[df_new_plot5["Funding Date"] == hoverData['points'][0]["x"]]
        tanggal = str(hoverData['points'][0]["x"])
    else:
        tanggal = "Jan-20 - Sep-21"
    country_lama = value_dropdown_plot4
    fundXvertical_plot5 = pd.crosstab(index=df_new_plot5["Vertical"],
            columns='Amount',
            colnames=' ',
            values = df_new_plot5["Funding Amount (USD)"],
            aggfunc = "sum").sort_values(by="Amount", ascending = False).head(10)

    fig=px.bar(
        fundXvertical_plot5.reset_index(),
        x = "Vertical",
        y = "Amount",
        labels={
                "Vertical": "Vertical (Industry)"
                },
        title='Industry Categories Rank in '+value_dropdown_plot4+' ('+tanggal+')',
        template = 'plotly_dark')
    fig.update_traces(marker_color='#63a7e5', textposition='outside')
    fig.update_layout(font=dict(
        size=11
    ))
    return fig

@app.callback(
    Output(component_id='plot_category', component_property='figure'), # graph component for output
    Input(component_id='dropdown_category', component_property='value'), # component from dropdown
    Input(component_id='category_radio_filter', component_property='value') # component from radiobutton
)
def update_graph_category(value_dropdown_category,radio_value):
    if value_dropdown_category == "Funding Amount VS Region":
        fundXregion = pd.crosstab(index=df_new["Region"],
                columns='Amount',
                colnames=' ',
                    values = df_new["Funding Amount (USD)"],
                aggfunc = "sum").sort_values(by="Amount", ascending = False)

        if radio_value == "Top 10":
            fundXregion = fundXregion.head(10)
        elif radio_value == "Bottom 10":
            fundXregion = fundXregion.tail(10)

        fig=px.bar(
            fundXregion.reset_index(),
            x = "Region",
            y = "Amount",
            labels={
                     "Region": "Country"
                 },
            title='Ranking of Countries Based on Amount of Funding in Technology Companies',
            template = 'plotly_dark')
    elif value_dropdown_category == "Funding Amount VS Vertical":
        fundXvertical = pd.crosstab(index=df_new["Vertical"],
                columns='Amount',
                colnames=' ',
                    values = df_new["Funding Amount (USD)"],
                aggfunc = "sum").sort_values(by="Amount", ascending = False)

        if radio_value == "Top 10":
            fundXvertical = fundXvertical.head(10)
        elif radio_value == "Bottom 10":
            fundXvertical = fundXvertical.tail(10)

        fig=px.bar(
            fundXvertical.reset_index(),
            x = "Vertical",
            y = "Amount",
            labels={
                     "Vertical": "Vertical (Industry)"
                 },
            title='Ranking of Industry Categories Based on Amount of Funding in Technology Companies',
            template = 'plotly_dark')
    else:
        fundXfunding_stage = pd.crosstab(index=df_new["Funding Stage"],
                columns='Amount',
                colnames=' ',
                    values = df_new["Funding Amount (USD)"],
                aggfunc = "sum").sort_values(by="Amount", ascending = False)

        if radio_value == "Top 10":
            fundXfunding_stage = fundXfunding_stage.head(10)
        elif radio_value == "Bottom 10":
            fundXfunding_stage = fundXfunding_stage.tail(10)

        fig=px.bar(
            fundXfunding_stage.reset_index(),
            x = "Funding Stage",
            y = "Amount",
            title='Ranking of Funding Stages Based on Amount of Funding in Technology Companies',
            template = 'plotly_dark')
    fig.update_traces(marker_color='#63a7e5', textposition='outside')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)