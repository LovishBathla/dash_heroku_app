import dash
import dash_html_components as html
import dash_core_components as dcc
import time
from load import load_data
from dash.dependencies import Input, Output
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import dash_table
import plotly

import pandas as pd
import numpy as np
import io 
import flask as flask

app = dash.Dash(__name__)

# Function to generate table
def generate_table(dataframe, max_rows=10):
    '''Given dataframe, return template generated using Dash components
    '''
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


# Function to create Pivot table
def generate_pv(frame, variable):
    pv = pd.pivot_table(
    frame, 
    index = variable,
    values = ['P04'],   # sexo
    columns = 'A02',    # A02 tuvo un trabajo en la ultima semana
    aggfunc = len,
    fill_value=0)
    pv[variable] = pv.index
    pv['Total'] = pv.apply(lambda x: x.iloc[0] + x.iloc[1], axis=1)
    pv['Activo'] = (round(pv.iloc[:,0] / pv['Total'],2)*100).astype(str) + '%'
    pv['Inactivo']= (round(pv.iloc[:,1] / pv['Total'],2)*100).astype(str) + '%'
    #pv.drop('5 años - 9 años', inplace=True)
    
    return pv.iloc[:,2:]

# List of variables for second dropdown
drop_dict = {'RECB01':'Ocupación principal',
             'RECB02':'Sector económico de ocupacion principal' ,
             'ED01':'Idioma principal en casa',
             'AÑOESTU':'Nivel o curso más alto aprobado',
             'A06' : '¿Qué hizo para conseguir trabajo en el último mes?',
             'A09': 'Razón por la qué no buscó trabajo el último mes', 
             'A15':'Categoría o posición que tenía en su última ocupación',
             'A16': 'Número de personas que trabajan en su establecimiento de trabajo',
             'A18': 'Razón principal por la que dejó su última ocupación',
             'B22': 'Tipo de contrato de trabajo en su ocupacion principal',
             'D01': '¿Desea mejorar su ocupación o cambiar o adicionar otra ocupación?',
             'D02': 'Razón principal por la que desea cambiar o adicionar su empleo actual',
             'E01GC': 'País de orígen de ingresos del exterior',
             'EDAD_QUIN': 'Edad',
             'PEAD':  'Actividad económica (desagregada)',
             'PEAA': 'Actividad económica (agrupada)',
             'trimestre': 'Trimestre',
             'E01GC' : 'País de orígen de remesas ',
             'P02' : 'Relacion de parentesco con el jefe de hogar',
             'P06': 'Estado Civil',
             'ED02': '¿Sabe leer y escribir?',
             'ED03': '¿Asiste o asistió a una institución de enseñanza formal?',
             'ED05': 'Tipo de institución de enseñanza actual',
             'ED06': 'Sector de la institución o programa de enseñanza',
             'ED07': 'Razon por la que no asiste una institucion de enseñanza',
             'A01': '¿La persona responde por sí misma ?',
             # 'A02': '¿Ha realizado algun trabajo la semana pasada?',
             'A03': '¿Tiene algun trabajo aunque no lo haya realizado la anterior semana?',
             'A04': '¿Hizo algo para conseguir trabajo en la semana pasada?',
             'A05': '¿Hizo algo para conseguir trabajo en el mes pasado?',
             'A11': 'Razón por la que no habría podido aceptar una oferta de trabajo',
             'A12': '¿Ha trabajado anteriormente?',
             'RECA13' : 'Ocupación en anterior trabajo',
             'RECA14':'Sector económico de anterior trabajo',
             'B05': 'Razón por la que no trabajó las horas habituales',
             'B10':'¿Aporta a una caja de jubilación?',
             'B11': 'Categoría o posición en su actual ocupación',
             'D03': '¿Buscó algun trabajo adicional la semana pasada?',
             'D04': '¿Estuvo disponible para trabajar más horas la semana pasada?',
             'B23': '¿Tuvo un trabajo secundario en la semana pasada?',
             
            }

colors = {
    'background': '#0C99F4',
    'plots': 'rgba(217, 217, 217, 0.3)',
    'text': '#7FDBFF'
}


array=[a for a in range(2010,2017)]
app.layout = html.Div([
    

    #Page Header
    html.H1("Encuesta Continua de Empleo Paraguay", style={'margin-left':40,
                                                           'margin-right':40,
                                                           'font-family': 'Helvetica',
                                                           "margin-top": 25, 
                                                           "margin-bottom": 5,
                                                          'backgroundColor':colors['background']},),
    

        html.A("Descargar Datos Transformados", href="/download_excel/",
          style={'text-align': 'right', 'margin-left':10} , className= "eleven columns"),



        html.Div([ 
        html.Div([
         
        # Dropdown año
            html.Div([
                html.Div('Seleccione el Año (Opcional)',
                         style={'font-style': 'bold', 
                                'font-weight': 'bold', 
                                'font-family': 'Helvetica',
                                'fontSize': 18},
                         className='four columns'),
                html.Div(dcc.Dropdown(id="drop-1",
                        options=([{'label': year, 'value': year } for year in array]),
                        value= None,
                        className='eight columns',  style={'margin-left':10,'margin-right':10,
                                                          "margin-bottom": 15}))
                    ]),
      
        
        # Dropdown variable
            html.Div([
                html.Div('Seleccione la Variable', 
                         style={'font-style': 'bold', 
                                'font-weight': 'bold', 
                                'font-family': 'Helvetica',
                                'fontSize': 18}, 
                         className='four columns'),
                html.Div(dcc.Dropdown(id="drop-2",
                        options = ([{'label': label, 'value': var} for var,label in drop_dict.items()]),
                        value= 'EDAD_QUIN',
                        className='eight columns',  style={'margin-left':10,'margin-right':10,
                                                          "margin-bottom": 15}))
                    ]),
             
            
        ], className='six columns'),

       
        ],   className='twleve columns'),

    dcc.Loading(
                    
                    children=[
    # Closes dropdown grid

        # Graphs grid
    html.Div([

        # Graficos izquierdos 
        html.Div([
            # Graph1
            dcc.Graph(id='funnel-graph-1', style={'height':'500px'},
                      config={'toImageButtonOptions': {'width': 1500, 'height': 1000}}),
            
            # Graph2
            dcc.Graph(id='funnel-graph-2', style={'height': '700px'},
                      config={'toImageButtonOptions': {'width': 1500, 'height': 1000}})
            
            
        ], className='six columns'),
       

        # Graficos derechos 
        html.Div([

            # Graph3
            dcc.Graph(id='funnel-graph-3', style={'height': '700px'},
                      config={'toImageButtonOptions': {'width': 1500, 'height': 1000}}),
            
            # summary table
            html.Table(id='variable-table-1',style={'height': '500px',
                                                   'margin-left':50,
                                                    'margin-right':10}),
            
            # style={},

        ], className='six columns')
       
    ] , style={'backgroundColor':colors['plots']}, className = 'twelve columns'),
   
    # Third grid
    html.Div([
        
          # Graph 5
        html.Div([
            dcc.Graph(id='funnel-graph-4', style={'height': '600px'},
                      config={'toImageButtonOptions': {'width': 1500, 'height': 1000}}) ,
        ], className='twelve columns'),
       # html.Div([
       #     dcc.Graph(id='funnel-graph-5', style={'height': '600px'}) ,
       # ], className='six columns'),

    ], className = 'twelve columns'),
        ],type='cube'),
    ],
)



'''
@app.callback(Output("loading-2", "children"),
              
              [Input("drop-2", "value"),
               ])
def input_triggers_nested(value):
    global df
    df=load_data()
'''
    

# 1. Function to update first graph
@app.callback(
    dash.dependencies.Output('funnel-graph-1', 'figure'),
    [dash.dependencies.Input('drop-1', 'value')])

def update_graph_1(year):
    df=load_data()
    if year == None:
        frame = df.copy()
    else:
        frame = df[df['year'].isin([year])]
    
    variable = 'EDAD_QUIN'   
    
    frame_men = frame[frame['P04']==1]
    frame_women = frame[frame['P04']==6]
    
    pv = generate_pv(frame, variable)
    pv1 = generate_pv(frame_men,variable)
    pv2 = generate_pv(frame_women,variable)
    
    for i in [pv,pv1, pv2]:
        if '5 años - 9 años' in i.index:
            i.drop(['5 años - 9 años'],inplace=True)
    
    trace1 = go.Scatter(x=pv.index, y=pv['Activo'],
                        name='Total Poblacion Activa',
                        marker=dict(color= 'rgba(50, 171, 96, 0.7)'))
    trace2 = go.Scatter(x=pv1.index, y=pv1['Activo'], 
                        name='Poblacion Masculina Activa',
                        marker=dict(color='rgba(55, 128, 191, 0.7)'))
    trace3 = go.Scatter(x=pv2.index, y=pv2['Activo'], 
                        name='Poblacion Femenina Activa',
                        marker=dict(color='rgba(219, 64, 82, 0.7)'))   
    
    if year == None:
        title = 'Todos los Años'
    else:
        title = year
        
    return {
            
        'data': [trace1, trace2, trace3],
        'layout':
        go.Layout(
            plot_bgcolor=colors['plots'],
            paper_bgcolor= colors['plots'],
            title={"text":'Poblacion Activa por Edad -  {}'.format(title),
                   "font": {"family": 'Helvetica',
                            "size": 24,
                            },
                  },
            ), 
    }
# 2. Function to update second graph PIE chart
@app.callback(
    dash.dependencies.Output('funnel-graph-2', 'figure'),
    [dash.dependencies.Input('drop-2', 'value'),
    dash.dependencies.Input('drop-1', 'value')] )

def update_graph_2(var, year):
    df=load_data()
    if year == None:
        frame = df
        
    else:
        frame = df[df['year']==year]
    


    #frame[var].fillna(0,inplace=True)
    pv = frame.groupby([var]).size()
    #pv = (100. * pv/ pv.sum()).round(1)
   
    # Title
    if year!= None:
        title =  drop_dict[var] +' - Distribución - {}'.format(year)
    else:
        title = drop_dict[var] + ' - Distribución - Todos los Años'
        
    return {
        "data": [go.Pie(labels=pv.index.tolist(), values=pv.tolist(),
                        opacity=0.7)],
        "layout": go.Layout(
                            plot_bgcolor=colors['plots'],
                            paper_bgcolor= colors['plots'],
                            title={"text": title,
                                   "font": {"family": 'Helvetica',
                                    "size": 22,
                            },
                  },
                            margin={"l": 200, "r": 200, },
                            legend={"x": 1, "y": 0.7})}


# 3. Function to make table of trimestres
@app.callback(
    dash.dependencies.Output('variable-table-1', 'children'),
    [dash.dependencies.Input('drop-2', 'value'),
    dash.dependencies.Input('drop-1', 'value')] )

def update_table_1 (var, year):
    df=load_data()
    if year == None:
        frame = df[df[var].notnull()]
    else:
        frame = df[(df['year']==year) & (df[var].notnull())]
    
    
    # Title
    if year!= None:
        title =  drop_dict[var] +' - {}'.format(year)
    else:
        title = drop_dict[var] + ' - Todos los Años'
    
    
        
    pv = frame.groupby([var,'trimestre'])[['trimestre']].count()
    pv = pv.unstack(level=1)
    pv = (100. * pv/ pv.sum()).round(1).astype(str) + '%'
    pv.insert(loc=0, column= title, value=pv.index)
    
    return generate_table(pv, max_rows=50)


# 4. Function to update third graph
@app.callback(
        dash.dependencies.Output('funnel-graph-3', 'figure'),
        [dash.dependencies.Input('drop-2', 'value'),
        dash.dependencies.Input('drop-1', 'value')])

def update_graph_3(var, year):
    df=load_data()
    if year == None:
        frame = df.copy()
    else:
        frame = df[df['year'].isin([year])]
    
    pv = frame.groupby([var,'P04'])[['P04']].count()
    pv = pv.unstack(level=1)
    pv = (100. * pv/ pv.sum()).round(1).astype(str) + '%'


    trace1 = go.Bar(y=pv.index, x=pv[('P04',1)], 
                    name='Poblacion Masculina', 
                    orientation='h',                
                    marker=dict(color='rgba(55, 128, 191, 0.7)') )
                    
    trace2 = go.Bar(y=pv.index, x=pv[('P04',6)], 
                    name='Poblacion Femenina', 
                    orientation='h',
                    marker=dict(color='rgba(219, 64, 82, 0.7)'))
    #trace3 = go.Bar(x=pv2.index, y=pv2['Activo'], name='Poblacion Femenina',orientation='v')   
    
    if year == None:
        title= drop_dict[var] + (' - Por Género - Todos los Años')
    else:
        title= drop_dict[var] + (' - Por Género - {} '.format(year) )
    
        
    return {
        'data': [trace1, trace2],
        'layout':
        go.Layout(
            plot_bgcolor=colors['plots'],
            paper_bgcolor= colors['plots'],
            yaxis=dict(autorange="reversed",showticklabels=True, automargin=True), 
            title={"text": title,
                   "font": {"family": 'Helvetica',
                            "size": 22,
                            },
                  }, 
        )
    }   
  
    

#5. Function for fourth graph
@app.callback(
    dash.dependencies.Output('funnel-graph-4', 'figure'),
        [dash.dependencies.Input('drop-2', 'value'),
        dash.dependencies.Input('drop-1', 'value')
        ])


def update_graph_4(var,year):
    df=load_data()
    if year == None:
        frame = df.copy()

    else:
        frame = df[df['year'].isin([year])]
    
    
    pv = frame.groupby([var,'year'])[['E01T']].mean()
    pv = pv.unstack(level=1)
    pv = pv['E01T']
    traces = []
    for i in pv.index.unique():
        #df_plot = df[df[var] == i]

        traces.append(go.Bar(
            x=pv.columns.tolist(),
            y=pv.loc[i,:].tolist(),
            #text= pv.index,
            opacity=0.7,

            name=str(i)
        ))


   
    # Title
    if year == None:
        title= drop_dict[var] + (' - Ingreso Mensual Promedio ₲ - Todos los Años')
    else:
        title= drop_dict[var] + (' - Ingreso Mensual Promedio ₲ - {} '.format(year) )
        
    # Radio

    
    
    return {
        'data': traces,
        'layout':
        go.Layout( 
            plot_bgcolor=colors['plots'],
            paper_bgcolor= colors['plots'],
            title={"text": title,
                   "font": {"family": 'Helvetica',
                            "size": 24,
                            },
                  },
            barmode= 'group')
    }

    
# 6. Function for fifth graph
#@app.callback(
#    dash.dependencies.Output('funnel-graph-5', 'figure'),
#    [dash.dependencies.Input('drop-1', 'value')])

def update_graph_5(year):
    df=load_data()
    
    if year == None:
        frame = df.copy()
    else:
        frame = df[df['year'].isin([year])]
    traces = []
    for i in frame.P04.unique():
        
        df_by_gender = frame[frame['P04'] == i]
        
        traces.append(go.Scatter(
            x=df_by_gender['HORABH'],
            y=df_by_gender['E01T'],
            text=df_by_gender['P04'],
            mode='markers',
            opacity=0.7,
            marker={
                'size': 15,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=str(i)
        ))

    return {
        'data': traces,
        'layout': go.Layout(
            plot_bgcolor=colors['plots'],
            paper_bgcolor= colors['plots'],
            xaxis={'type': 'log', 'title': 'Horas Trabajadas Habituales'},
            yaxis={'title': 'Salario Mes Pasado'},
            margin={'l': 50, 'b': 100, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest'),
        
    }



# DOWNLOAD CSV


@app.server.route('/download_excel/')
def download_csv():
    #Convert DF
    str_io = io.StringIO()
    df.to_csv(str_io)
    mem = io.BytesIO()
    mem.write(str_io.getvalue().encode('utf-8'))
    mem.seek(0)
    return flask.send_file(mem,
                       mimetype='text/csv',
                       attachment_filename='encuesta_limpia.csv',
                       as_attachment=True)

if __name__ == "__main__":
    app.run_server(debug=True)
