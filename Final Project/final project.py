import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
from sodapy import Socrata

client = Socrata('health.data.ny.gov',
                 'FIP0B5tQL0HpZfWNU7W77Rgj6')


def get_all(name):
    return [row['n'] if 'n' in row else 'n/a' for row in client.get("22g3-z7e7", select=f'distinct {name} as n')]


hospital_service_areas = get_all('hospital_service_area')
types_of_admission = get_all('type_of_admission')
ccs_procedure_descriptions = get_all('ccs_procedure_description')
apr_severity_of_illnesses = get_all('apr_severity_of_illness')
apr_medical_surgicals = get_all('apr_medical_surgical')
ccs_diagnosis_descriptions = get_all('ccs_diagnosis_description')
payment_typologies = get_all('payment_typology_1')

app = dash.Dash()


app.layout = html.Div([
    html.Div([
        html.Div([
            html.H3('New York State Hospitals'),
            html.Div('The data used for this visualization is from the New York State Department of Health. It contains the discharge level details on patient characteristics, diagnoses, treatments, services, and charges for 2017 Hospital Inpatient discharges in New York State. This web app is designed to display information directly from DOH API. It shows the top hospital and the procedure costs in New York City, and allows a user to choose region, types of admissions, diagnosis categories, etc. It  shows a high-cost trending procedure and providers by total cost and average cost per procedure. The table at the end of the page shows the highest cost claims(outliers) in each selection.'),
            html.Div([
                html.H4('Hospital service area'),
                dcc.Dropdown(
                    id='hospital_service_area',
                    multi=True,
                    options=[{'label': name, 'value': name} for name in hospital_service_areas],
                    value=[]
                ),
            ])  
            ,
            html.Div([
                html.H4('Type of admission'),
                dcc.Dropdown(
                    id='type_of_admission',
                    multi=True,
                    options=[{'label': name, 'value': name} for name in types_of_admission],
                    value=[]
                ),
            ]),
            html.Div([
                html.H4('Procedure description'),
                dcc.Dropdown(
                    id='ccs_procedure_description',
                    multi=True,
                    options=[{'label': name, 'value': name} for name in ccs_procedure_descriptions],
                    value=[]
                ),
            ]),
            html.Div([
                html.H4('Severity of illness'),
                dcc.Dropdown(
                    id='apr_severity_of_illness',
                    multi=True,
                    options=[{'label': name, 'value': name} for name in apr_severity_of_illnesses],
                    value=[]
                ),
            ]),
            html.Div([
                html.H4('Medical surgical'),
                dcc.Dropdown(
                    id='apr_medical_surgical',
                    options=[{'label': name, 'value': name} for name in apr_medical_surgicals],
                    value='all'
                )
            ]),
            html.Div([
                html.H4('Diagnosis description'),
                dcc.Dropdown(
                    id='ccs_diagnosis_description',
                    multi=True,
                    options=[{'label': name, 'value': name} for name in ccs_diagnosis_descriptions],
                    value=[]
                )
            ]),
            html.Div([
                html.H4('Payment typology'),
                dcc.Dropdown(
                    id='payment_typology_1',
                    multi=True,
                    options=[{'label': name, 'value': name} for name in payment_typologies],
                    value=[]
                )
            ]),
        ], style={'width': '350px', 'flex': '1', 'padding': '15px','background': '#dddddd'}),
        html.Div([
            dcc.Graph(id='sum_hospital_cost'),
            dcc.Graph(id='sum_procedure_cost'),
            dcc.Graph(id='avg_hospital_cost'),
            dcc.Graph(id='avg_procedure_cost'),
            dcc.Graph(id='max_claims'),
        ], style={'flex': '2', 'padding': '15px','width': '600px'})
    ], style={'display': 'flex'})
], style={'font-family': 'Arial'})


@app.callback(
    Output('sum_hospital_cost', 'figure'),
    [
        Input('hospital_service_area', 'value'),
        Input('type_of_admission', 'value'),
        Input('ccs_procedure_description', 'value'),
        Input('apr_severity_of_illness', 'value'),
        Input('apr_medical_surgical', 'value'),
        Input('ccs_diagnosis_description', 'value'),
        Input('payment_typology_1', 'value'),
    ]
)
def handle(hospital_service_area,
           type_of_admission,
           ccs_procedure_description,
           apr_severity_of_illness,
           apr_medical_surgical,
           ccs_diagnosis_description,
           payment_typology_1):

    results = client.get("22g3-z7e7",
                         select='facility_name,sum(total_costs) as sum_total_costs',
                         where=get_filter(hospital_service_area,
                                          type_of_admission,
                                          ccs_procedure_description,
                                          apr_severity_of_illness,
                                          apr_medical_surgical,
                                          ccs_diagnosis_description,
                                          payment_typology_1),
                         group='facility_name',
                         limit=10,
                         order='sum_total_costs desc')
    if len(results) == 0:
        trace = go.Bar(x=[], y=[])
    else:
        df = pd.DataFrame.from_records(results)
        df['sum_total_costs'] = df['sum_total_costs'].astype(pd.np.float64)

        trace = go.Bar(
            x=pd.Series(map(lambda x: x.replace(' ', '<br>'), df['facility_name'])),
            y=df['sum_total_costs'],
        )

    return {
        'data': [trace],
        'layout': go.Layout(
            title='Top 10 Hospital total cost',
            xaxis=dict(
                title='Facility name',
                tickfont=dict(size=10)
            ),
            yaxis={'title': 'Total cost'},
        )
    }


@app.callback(
    Output('sum_procedure_cost', 'figure'),
    [
        Input('hospital_service_area', 'value'),
        Input('type_of_admission', 'value'),
        Input('ccs_procedure_description', 'value'),
        Input('apr_severity_of_illness', 'value'),
        Input('apr_medical_surgical', 'value'),
        Input('ccs_diagnosis_description', 'value'),
        Input('payment_typology_1', 'value'),
    ]
)
def handle(hospital_service_area,
           type_of_admission,
           ccs_procedure_description,
           apr_severity_of_illness,
           apr_medical_surgical,
           ccs_diagnosis_description,
           payment_typology_1):

    results = client.get("22g3-z7e7",
                         select='ccs_procedure_description,sum(total_costs) as sum_total_costs',
                         where=get_filter(hospital_service_area,
                                          type_of_admission,
                                          ccs_procedure_description,
                                          apr_severity_of_illness,
                                          apr_medical_surgical,
                                          ccs_diagnosis_description,
                                          payment_typology_1) + ' and ccs_procedure_description != "NO PROC"',
                         group='ccs_procedure_description',
                         limit=10,
                         order='sum_total_costs desc')
    if len(results) == 0:
        trace = go.Bar(x=[], y=[])
    else:
        df = pd.DataFrame.from_records(results)
        df['sum_total_costs'] = df['sum_total_costs'].astype(pd.np.float64)

        trace = go.Scatter(
            x=pd.Series(map(lambda x: x.replace(' ', '<br>'), df['ccs_procedure_description'])),
            y=df['sum_total_costs'],
            mode='lines+markers',
            line={'color': 'rgb(128, 0, 128)'}
        )

    return {
        'data': [trace],
        'layout': go.Layout(
            title='Top 10 Procedure total cost',
            xaxis=dict(
                title='Procedure',
                tickfont=dict(size=10)
            ),
            yaxis={'title': 'Total cost'}
        )
    }


@app.callback(
    Output('avg_hospital_cost', 'figure'),
    [
        Input('hospital_service_area', 'value'),
        Input('type_of_admission', 'value'),
        Input('ccs_procedure_description', 'value'),
        Input('apr_severity_of_illness', 'value'),
        Input('apr_medical_surgical', 'value'),
        Input('ccs_diagnosis_description', 'value'),
        Input('payment_typology_1', 'value'),
    ]
)
def handle(hospital_service_area,
           type_of_admission,
           ccs_procedure_description,
           apr_severity_of_illness,
           apr_medical_surgical,
           ccs_diagnosis_description,
           payment_typology_1):

    results = client.get("22g3-z7e7",
                         select='facility_name,avg(total_costs) as avg_total_costs',
                         where=get_filter(hospital_service_area,
                                          type_of_admission,
                                          ccs_procedure_description,
                                          apr_severity_of_illness,
                                          apr_medical_surgical,
                                          ccs_diagnosis_description,
                                          payment_typology_1),  # + ' and total_costs < 200000',
                         group='facility_name',
                         limit=10,
                         order='avg_total_costs desc')
    if len(results) == 0:
        trace = go.Bar(x=[], y=[])
    else:
        df = pd.DataFrame.from_records(results)
        df['avg_total_costs'] = df['avg_total_costs'].astype(pd.np.float64)

        trace = go.Bar(
            x=pd.Series(map(lambda x: x.replace(' ', '<br>'), df['facility_name'])),
            y=df['avg_total_costs'],
        )

    return {
        'data': [trace],
        'layout': go.Layout(
            title='Top 10 hospital average visit cost',
            xaxis=dict(
                title='Facility name',
                tickfont=dict(size=10)
            ),
            yaxis={'title': 'Average cost'}
        )
    }


@app.callback(
    Output('avg_procedure_cost', 'figure'),
    [
        Input('hospital_service_area', 'value'),
        Input('type_of_admission', 'value'),
        Input('ccs_procedure_description', 'value'),
        Input('apr_severity_of_illness', 'value'),
        Input('apr_medical_surgical', 'value'),
        Input('ccs_diagnosis_description', 'value'),
        Input('payment_typology_1', 'value'),
    ]
)
def handle(hospital_service_area,
           type_of_admission,
           ccs_procedure_description,
           apr_severity_of_illness,
           apr_medical_surgical,
           ccs_diagnosis_description,
           payment_typology_1):

    results = client.get("22g3-z7e7",
                         select='ccs_procedure_description,avg(total_costs) as avg_total_costs',
                         where=get_filter(hospital_service_area,
                                          type_of_admission,
                                          ccs_procedure_description,
                                          apr_severity_of_illness,
                                          apr_medical_surgical,
                                          ccs_diagnosis_description,
                                          payment_typology_1) + ' and ccs_procedure_description != "NO PROC"',
                         group='ccs_procedure_description',
                         limit=10,
                         order='avg_total_costs desc')
    if len(results) == 0:
        trace = go.Bar(x=[], y=[])
    else:
        df = pd.DataFrame.from_records(results)
        df['avg_total_costs'] = df['avg_total_costs'].astype(pd.np.float64)

        trace = go.Scatter(
            x=pd.Series(map(lambda x: x.replace(' ', '<br>'), df['ccs_procedure_description'])),
            y=df['avg_total_costs'],
            mode='lines+markers',
            line={'color': 'rgb(128, 0, 128)'}
        )

    return {
        'data': [trace],
        'layout': go.Layout(
            title='Top 10 procedure average cost',
            xaxis=dict(
                title='Procedure',
                tickfont=dict(size=10)
            ),
            yaxis={'title': 'Average cost'}
        )
    }


@app.callback(
    Output('max_claims', 'figure'),
    [
        Input('hospital_service_area', 'value'),
        Input('type_of_admission', 'value'),
        Input('ccs_procedure_description', 'value'),
        Input('apr_severity_of_illness', 'value'),
        Input('apr_medical_surgical', 'value'),
        Input('ccs_diagnosis_description', 'value'),
        Input('payment_typology_1', 'value'),
    ]
)
def handle(hospital_service_area,
           type_of_admission,
           ccs_procedure_description,
           apr_severity_of_illness,
           apr_medical_surgical,
           ccs_diagnosis_description,
           payment_typology_1):

    select = ', '.join((
        'hospital_service_area',
        'facility_name',
        'length_of_stay',
        'payment_typology_1',
        'type_of_admission',
        'ccs_diagnosis_description',
        'ccs_procedure_description',
        'apr_medical_surgical',
        'total_costs'
    ))

    results = client.get("22g3-z7e7",
                         select=select,
                         where=get_filter(hospital_service_area,
                                          type_of_admission,
                                          ccs_procedure_description,
                                          apr_severity_of_illness,
                                          apr_medical_surgical,
                                          ccs_diagnosis_description,
                                          payment_typology_1),
                         limit=10,
                         order='total_costs desc')
    if len(results) == 0:
        return html.Table()
    else:
        df = pd.DataFrame.from_records(results)
        table = go.Table(
            header=dict(
                values=[name.replace('_', ' ') for name in df.columns[1:]],
                font=dict(size=10),
                line=dict(color='rgb(50, 50, 50)'),
                align='left',
                fill=dict(color='#d562be'),
            ),
            cells=dict(
                values=[df[k].tolist() for k in df.columns[1:]],
                line=dict(color='rgb(50, 50, 50)'),
                align='left',
                fill=dict(color='#f5f5fa')
            )
        )
        return {
            'data': [table],
            'layout': go.Layout()
        }


def get_statement(name, value):
    if value in (None, 'all', []):
        return None
    if type(value) == list:
        return '(' + ' or '.join(f'{name}="{x}"' for x in value) + ')'
    else:
        return f'{name}="{value}"'


def get_filter(hospital_service_area,
               type_of_admission,
               ccs_procedure_description,
               apr_severity_of_illness,
               apr_medical_surgical,
               ccs_diagnosis_description,
               payment_typology_1):
    variables = {
        'hospital_service_area': hospital_service_area,
        'type_of_admission': type_of_admission,
        'ccs_procedure_description': ccs_procedure_description,
        'apr_severity_of_illness': apr_severity_of_illness,
        'apr_medical_surgical': apr_medical_surgical,
        'ccs_diagnosis_description': ccs_diagnosis_description,
        'payment_typology_1': payment_typology_1
    }
    statements = (get_statement(name, value) for name, value in variables.items())
    where = [x for x in statements if x is not None]
    where.append('total_costs is not null')
    where.append('total_costs > 0')
    return ' and '.join(where)


if __name__ == "__main__":
    app.run_server(debug=True)
