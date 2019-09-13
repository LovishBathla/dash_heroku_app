# DASH APP - ECE PARAGUAY

# Autor: Michael A. Tondu

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import dash_table
import plotly
import os
import pandas as pd
import numpy as np
import io 
import flask as flask
import pymysql
import psycopg2
##################################################
# Data Manipulation
##################################################

# Loading and cleaning data
#df = pd.read_csv('D:\dash-ece-app-master\ECE_copy.csv')
#df = pd.read_csv('ECE_copy.csv')

host="ec2-174-129-227-80.compute-1.amazonaws.com"
db="d6kqslcuso8lr"
us="bnwycizeyrtlgn"
pwd="8d207872efa476ea7e3f9ae0bc23045fe114ae3ac4b67956b7e3d754a5632d3e"
#db = psycopg2.connect(host=host,database=db, user=us, password=pwd , port=5432)
db = psycopg2.connect(host=host,database=db, user=us, password=pwd)
'''
DATABASE_URL = os.environ['DATABASE_URL']

db = psycopg2.connect(DATABASE_URL, sslmode='require')
'''
query = "SELECT * FROM data;"

df = pd.read_sql(query, db)

# Estandarizando el tipo de los datos
for i in df.columns:
    df[i] = pd.to_numeric(df[i], errors='coerce')
# Removiendo NR ("1.000000e+10") de variables de salario   
for i in df.columns:
    df[i].replace(9999999999, np.nan, inplace=True)
# Trimestre y año categoricos
df['trimestre'] = df['trimestre'].astype(str)
#df['year'] = df['year'].astype('category')

    
    
    
    
    
# MAPPING VALUES:

 #1 ED01
di = {1:'Guaraní',2:'Guaraní y castellano', 3:'Castellano', 4:'Otro idioma', 5:'No habla'}   
df['ED01'] = df['ED01'].map(di) 

 #2 Sector Economico RECB02
di2 = {1: 'Agricultura, ganadería, caza, silvicultura y pesca',2:'Explotación de minas y canteras',
       3:'Industrias manufactureras', 4:'Electricidad, gas y agua', 
       5:'Construcciones' , 6:'Comercio al por mayor y menor, restaurantes y hoteles',
       7:'Transporte, almacenamiento y comunicaciones',
       8:'Establecimientos financieros, seguros y bienes inmuebles',
       9:'Servicios comunales, sociales y personales'}
df['RECB02'] = df['RECB02'].map(di2) 

 #3 P04
#di3 = {1:'Hombre',6:'Mujer'}   
#df['P04'] = df['P04'].map(di3)

#4 AÑOESTU (ED04)
di4 = {1: 'Sin instrucción',
 2: 'Jardín o Preescolar',
 3: 'Educ. Especial',
 4: 'EEB 1ª al 6ª (Primaria)',
 5: 'EEB 7º al 9º',
 6: 'Secundario Ciclo Básico',
 7: 'Bachiller Humanístico / Científico',
 8: 'Bachiller Técnico / Comercial',
 9: 'Bachillerato a distancia',
 10: 'Educación Media Científica',
 11: 'Educación Media Técnica',
 12: 'Educ. Básica Bilingüe de Jóvenes y Adultos',
 13: 'Educ. Media a Distancia para Jóvenes y Adultos',
 14: 'Educ. Básica Alternativa de Jóvenes y Adultos',
 15: 'Educ. Media Alternativa de Jóvenes y Adultos',
 16: 'Formación Profesional no Bachillerato de la Media',
 17: 'Programa de Alfabetización',
 18: 'Grado especial / Programas Especiales',
 19: 'Técnica Superior',
 20: 'Formación Docente',
 21: 'Profesionalización Docente',
 22: 'Formación Militar/Policial',
 23: 'Universitario'}
df['AÑOESTU'] = df['AÑOESTU'].map(di4)

#5 Ocupacion RECB01
di5 = {1: 'Sector Publico', 
 2: 'Profesionales científicos e intelectuales',
 3: 'Técnicos y profesionales de nivel medio',
 4: 'Empleados de oficina',
 5: 'Servicios y vendedores de comercios y mercados',
 6: 'Agricultores y trabajadores Agropecuarios y Pesqueros',
 7: 'Oficiales, operarios y artesanos de artes mecánicas y de otros oficios',
 8: 'Operadores de instalaciones y máquinas y montadores',
 9: 'Trabajadores no calificados',
 10: 'Fuerzas armadas',
 99: 'NR'}

df['RECB01'] = df['RECB01'].map(di5) 

#6 Que hizo para conseguir trabajo en el ultimo mes? A06
di6= {1.0: 'Consultó a algún empleador o patrón',
 2.0: 'Consultó en alguna agencia',
 3.0: 'Consultó con amigos o parientes',
 4.0: 'Contestó / publicó avisos en los periódicos',
 5.0: 'Solicitó préstamo para trabajar por su cuenta ',
 6.0: 'Otras gestiones para trabajar por su cuenta',
 7.0: 'Internet',
 8.0: 'Otras gestiones '}
df['A06'] = df['A06'].map(di6)

#7 Cual es la razón principal por la qué no buscó trabajo en la semana pasada o en las 3 semanas anteriores a la semana pasada?
# A09
di7={1: 'No quiere trabajar más',
 2: 'No cree poder encontrar trabajo',
 3: 'Se cansó de buscar',
 4: 'No sabe donde consultar',
 5: 'Es demasiado joven',
 6: 'Se dedica exclusivamente a las labores del hogar',
 7: 'Es estudiante',
 8: 'Inclemencia del tiempo',
 9: 'Buscó y ahora está esperando noticias',
 10: 'Comenzará nuevo trabajo en el próximo mes',
 11: 'Estuvo enfermo',
 12: 'Es anciano o discapacitado',
 13: 'Es rentista',
 14: 'Es jubilado',
 15: 'Es pensionado',
 16: 'Motivos familiares',
 17: 'Otra razón '}
df['A09'] = df['A09'].map(di7)

#8 Categoría o posición que tenía en su última ocupación? A15
di8={1.0: 'Empleado / obrero público',
 2.0: 'Empleado / obrero privado',
 3.0: 'Empleador o patrón',
 4.0: 'Trabajador por cuenta propia',
 5.0: 'Trabajador familiar no remunerado',
 6.0: 'Empleado doméstico'}
df['A15'] = df['A15'].map(di8)

#9 Aproximadamente, cuántas personas trabajan en el establecimiento o negocio donde trabajaba en su última ocupación ? A16
di9={1.0: 'Solo',
 2.0: '2 a 5 personas',
 3.0: '6 a 10 personas',
 4.0: '11 a 20 personas',
 5.0: '21 a 50 personas',
 6.0: '51 a 100 personas',
 7.0: '101 a 500 personas',
 8.0: 'Más de 500 personas',
 9.0: 'Empleado doméstico',
 10.0: 'No sabe'}
df['A16'] = df['A16'].map(di9)

#10 Edades quinquenales
di10 = {1.0: '0 años - 04 años',
 2.0: '05 años - 09 años',
 3.0: '10 años - 14 años',
 4.0: '15 años - 19 años',
 5.0: '20 años - 24 años',
 6.0: '25 años - 29 años',
 7.0: '30 años - 34 años',
 8.0: '35 años - 39 años',
 9.0: '40 años - 44 años',
 10.0: '45 años - 49 años',
 11.0: '50 años - 54 años',
 12.0: '55 años - 59 años',
 13.0: '60 años y más'}
df['EDAD_QUIN'] = df['EDAD_QUIN'].map(di10)

#11 Actividad económica (DESAGREGADA) PEAD
di11={1.0: 'Ocupados (Sin Subocupación Visible + Invisible)',
 2.0: 'Desocupados de 2ª ó más veces',
 3.0: 'Inactivos (Excluyendo Desempleo Oculto)',
 4.0: 'Subocup. Visible',
 5.0: 'Subocup. Invisible',
 6.0: 'Desempleo Oculto',
 7.0: 'Desocupados de 1ª vez'}

df['PEAD'] = df['PEAD'].map(di11)

#12 Actividad económica (AGRUPADA) PEAA
di12={1.0: 'Ocupados',
 2.0: 'Desocupados',
 3.0: 'Inactivos'}

df['PEAA'] = df['PEAA'].map(di12)

#13 Cuál es la razón principal por la que dejó su última ocupación ? A18
di13 = {1: 'Ganaba poco',
 2: 'No tenía ingreso',
 3: 'Fue despedido',
 4: 'Cerró el establecimiento',
 5: 'Terminó su contrato',
 6: 'Período de prueba',
 7: 'Es estudiante',
 8: 'Se jubiló',
 9: 'Ambiente inadecuado',
 10: 'Poco estable',
 11: 'Trabajo temporal',
 12: 'Labores del hogar',
 13: 'Falta de pedido',
 14: 'Motivo familiar',
 15: 'Anciano o discapacitado',
 16: 'Enfermedad',
 17: 'Otra razón'}
df['A18'] = df['A18'].map(di13)

#14 Bajo que tipo de contrato trabaja en esta ocupacion? B22
di14 = {1.0: 'Contrato indefinido (nombrado)',
 2.0: 'Contrato definido (temporal)',
 3.0: 'Sin contrato (acuerdo verbal)',
 4.0: 'Período de prueba'}
df['B22'] = df['B22'].map(di14)

#15 Desea mejorar su/sus ocupación/nes o cambiar o adicionar otra ocupación ?D01
di15 = {1.0: 'Sí, mejorar su ocupación',
 2.0: 'Sí, cambiar la o las ocupaciones',
 3.0: 'Sí, adicionar otra ocupación',
 4.0: 'No desea cambiar'}
df['D01'] = df['D01'].map(di15)

#16 Cuál es la razón principal por al que desea mejorar o cambiar o adicionar su empleo actual ? D02
di16 = {1.0: 'Gana poco',
 2.0: 'El trabajo es pesado',
 3.0: 'Desea trabajar menos horas sin ganar menos',
 4.0: 'Desea trabajar menos horas aunque gane menos',
 5.0: 'Desea trabajar más horas y ganar más',
 6.0: 'No aprovecha sus estudios y experiencias',
 7.0: 'Ambiente de trabajo inadecuado',
 8.0: 'Conflictos laborales',
 9.0: 'Poco estable',
 10.0: 'Motivo familiar, personal',
 11.0: 'Otra razón'}

df['D02'] = df['D02'].map(di16)

#17 País de orígen de remesas E01GC
di17 = {1.0: 'Argentina',
 2.0: 'Brasil',
 3.0: 'EE.UU.',
 4.0: 'España',
 9.0: 'Otro'}

df['E01GC'] = df['E01GC'].map(di17)
###########
#18 Relacion de parentesco con el jefe de hogar
di18 = {1: 'Jefe/a',
 2: 'Esposo/a /compañero/a',
 3: 'Hijo/a',
 4: 'Hijastro/a',
 5: 'Nieto/a',
 6: 'Yerno/Nuera',
 7: 'Padre/Madre',
 8: 'Suegro/a',
 9: 'Otro pariente',
 10: 'No pariente',
 11: 'Personal doméstico o su familia'}
df['P02'] = df['P02'].map(di18)

#19 sexo
di19 = {1.0: 'Varón',
 6.0: 'Mujer'}
#df['P04'] = df['P04'].map(di19)

#20 Estado Civil
di20 = {1.0: 'Casado/a',
 2.0: 'Unido/a',
 3.0: 'Separado/a',
 4.0: 'Viudo/a',
 5.0: 'Soltero/a',
 6.0: 'Divorciado/a',
 9.0: 'NR'}
df['P06'] = df['P06'].map(di20)

#21 Sabe leer y escribir?
di21 = {1.0: 'Sí',
 6.0: 'No'}
df['ED02'] = df['ED02'].map(di21)

#22 Asiste o asistió alguna vez a una institución de enseñanza formal ?
di22 = {1.0: 'Sí',
 6.0: 'No'}
df['ED03'] = df['ED03'].map(di22)

#23 Asiste  actualmente a una institución de enseñanza ?
di23 = {1: 'Sí, Educ. Inicial',
 2: 'Sí, Educ. Escolar Básica',
 3: 'Sí, Educación Media Científica',
 4: 'Sí, Educación Media Técnica',
 5: 'Sí, Bachillerato a Distancia',
 6: 'Sí, Educ. Básica Bilingüe de Jóvenes y Adultos',
 7: 'Sí, Educación Media a Distancia para Jóvenes y Adultos',
 8: 'Sí, Educación Media Alternativa de Jóvenes y Adultos',
 9: 'Sí, Formación Profesional no Bachillerato de la Media',
 10: 'Sí, Programas de Alfebeticación',
 11: 'Sí, Educ. Especial',
 12: 'Sí, Grado Especial / Programas especiales',
 13: 'Sí, Técnica Superior',
 14: 'Sí, Formación Docente',
 15: 'Sí, Profesionalización Docente',
 16: 'Sí, Formación Militar / Policial',
 17: 'Sí, Superior Universitario',
 18: 'Sí, Post Superior no Universitario',
 19: 'Sí, Post Superior Universitario',
 20: 'No asiste '}
df['ED05'] = df['ED05'].map(di23)

#24 La institución o programa donde asiste es del sector
di24 = {1.0: 'Pública ',
 2.0: 'Privada ',
 3.0: 'Privada Subvencionada ',
 9.0: 'NR'}
df['ED06'] = df['ED06'].map(di24)

#25 Por qué no asiste o dejó de asistir a una institucion de enseñanza?
di25 = {1.0: 'Sin recursos en el hogar',
 2.0: 'Necesidad de trabajar',
 3.0: 'Muy costosos los materiales y matriculas',
 4.0: 'No tiene edad adecuada ',
 5.0: 'Considera que terminó los estudios',
 6.0: 'No existe institución cercana',
 7.0: 'Institución cercana muy mala',
 8.0: 'El centro educativo cerró',
 9.0: 'El docente no asiste con regularidad ',
 10.0: 'Institución no ofrece escolaridad completa',
 11.0: 'Requiere educación especial',
 13.0: 'Por enfermedad',
 14.0: 'Realiza labores en el hogar',
 15.0: 'Motivos familiares',
 16.0: 'No quiere estudiar',
 17.0: 'Asiste a enseñanza vocacional',
 18.0: 'Servicio militar',
 19.0: 'Otra razón'}
df['ED07'] = df['ED07'].map(di25)

#26 La persona responde por sí misma ?
di26 = {1.0: 'Sí',
 6.0: 'No'}
df['A01'] = df['A01'].map(di26)

#27 Ha realizado algun trabajo la semana pasada?  ##### (Utilizamos esta variable para calcular poblacion activa)
#df['A02'] = df['A02'].map(di26)

#28 Tiene algun trabajo aunque no lo haya realizado la anterior semana?
df['A03'] = df['A03'].map(di26)

#29 Hizo algo para conseguir trabajo en la semana pasada ?
df['A04'] = df['A04'].map(di26)

#30  Hizo algo para conseguir trabajo en el mes pasado ?
df['A05'] = df['A05'].map(di26)

#31 Razón por la que no habría podido aceptar una oferta de trabajo?
di31= {1.0: 'No quiere trabajar más',
 2.0: 'Es demasiado joven',
 3.0: 'Se dedica exclusivamente a las labores del hogar',
 4.0: 'Es estudiante',
 5.0: 'Estuvo enfermo',
 6.0: 'Es anciano o discapacitado',
 7.0: 'Es rentista',
 8.0: 'Es jubilado',
 9.0: 'Es pensionado',
 10.0: 'Motivos familiares',
 11.0: 'Otra razón ',
 99.0: 'NR'}
df['A11'] = df['A11'].map(di31)

#31 Ha trabajado anteriormente ?
df['A12'] = df['A12'].map(di26)

#32 Ocupación en anterior trabajo
df['RECA13'] = df['RECA13'].map(di5)
df['RECC01'] = df['RECC01'].map(di5)

#33 Sector económico de anterior trabajo
df['RECA14'] = df['RECA14'].map(di2) 
df['RECC02'] = df['RECC02'].map(di2)

#34 Razón por la que no trabajó el número habitual de horas en la semana pasada?
di34 = {1.0: 'Disminución de  trabajo',
 2.0: 'Falta de materiales',
 3.0: 'Reparaciones en la planta, máquina, vehículo',
 4.0: 'Empleo nuevo que empezó dentro de la semana',
 5.0: 'Empleo que terminó dentro de la semana',
 6.0: 'Inclemencia del tiempo',
 7.0: 'Gestiones particulares, viajes, (independientes)',
 8.0: 'Vacaciones, permiso, huelga (asalariados)',
 9.0: 'Enfermedad',
 10.0: 'Demasiado ocupado en tareas del hogar, estudio, etc.',
 11.0: 'Trabaja a tiempo completo sólo en período de mayor actividad',
 12.0: 'Día feriado, fiesta',
 13.0: 'Cualquier otra razón',
 99.0: 'NR'}
df['B05'] = df['B05'].map(di34)

#35 Aporta a una caja de jubilación por este trabajo ?
df['B10'] = df['B10'].map(di26)

#36 Categoría o posición en su actual ocupación ?
df['B11'] = df['B11'].map(di8)

#37 Durante la semana pasada, buscó algún otro trabajo para cambiar o adicionar al que ya tiene ?
df['D03'] = df['D03'].map(di26)

#38 Durente la semana pasada, estuvo disponible para trabajar más horas ?
df['D04'] = df['D04'].map(di26)

#39 Tuvo trabajo secundario en la semana pasada?
df['B23'] = df['B23'].map(di26)



  
    
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


    



external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = dash.Dash(__name__,external_stylesheets =external_stylesheets )
'''
app.css.append_css({
    "external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css",
    
})
'''
server = app.server 


colors = {
    'background': '#0C99F4',
    'plots': 'rgba(217, 217, 217, 0.3)',
    'text': '#7FDBFF'
}


#FFFFFF

##################################################
# Dashboard Layout / View
##################################################


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
         
    # Dropdown Grid

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
                        options=([{'label': year, 'value': year } for year in df['year'].unique()]),
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

        # Empty
        html.Div( className='six columns'), 
    ],   className='twleve columns'),      # Closes dropdown grid

    
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
    
])    # Final Structure parenthesis
    
    

##################################################
# Callbacks
##################################################



# 1. Function to update first graph
@app.callback(
    dash.dependencies.Output('funnel-graph-1', 'figure'),
    [dash.dependencies.Input('drop-1', 'value')])

def update_graph_1(year):
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

if __name__ == '__main__':
    app.run_server(debug=True)
