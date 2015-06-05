# -*- coding: utf-8 -*-

import elpais,sys,os
import cPickle as pickle
from webcache import WebCache
from bs4 import BeautifulSoup
import html2text
import random,re,sys,string
import json
import datetime as datetime
from dateutil.relativedelta import *
import time


#from pandas import *
#from scipy import stats
#from pandas.core.groupby import GroupByError
from collections import defaultdict
from scipy.odr.odrpack import RealData


reload(sys)  # Reload does the trick!
sys.setdefaultencoding("utf-8")

#COsas que se cuentan
validThings = ["personas", "firmas", "trabajadores", "vecinos", "alumnos", "estudiantes", "presos", "manifestantes", "miembros", "empleados", "j\u00f3venes", "agentes", "profesores", "jornaleros", "ciudadanos", "reclusos", "polic\u00edas", "activistas", "inmigrantes", "funcionarios", "profesionales", "agricultores", "taxistas", "mujeres", "hombres", "ni\u00f1os", "universitarios", "operarios", "delegados", "mineros", "representantes", "obreros", "alcaldes", "docentes", "despedidos", "pescadores", "pasajeros", "guardias", "concejales", "asistentes", "ayuntamientos", "usuarios", "m\u00e9dicos", "residentes", "insumisos", "escolares", "grapos", "muertos", "sindicalistas", "bomberos", "comerciantes", "periodistas", "ecologistas", "parados", "menos", "desahucios", "indignados", "maestros", "conductores", "familiares", "propietarios", "objetores", "ancianos", "abogados", "afiliados", "socios", "musulmanes", "espectadores", "artistas", "magreb\u00edes", "diputados", "extrabajadores", "gitanos", "pacientes", "ganaderos", "fallecidos", "procesados", "voluntarios", "huelguistas", "padres", "empresarios", "militares", "sacerdotes", "telegramas", "contusionados", "damnificados", "acampados", "opositores", "encausados", "seguidores", "ecuatorianos", "hospitalizados", "desahuciados", "vigilantes", "auxiliares", "simpatizantes", "extranjeros", "ediles", "directivos", "madrile\u00f1os", "vendedores", "celadores", "extreme\u00f1os", "portugueses", "etarras", "camioneros", "desempleados", "colegas", "destinados", "grapo", "corredores", "congregados", "marineros", "yonkis", "int\u00e9rpretes", "cultivadores", "gaditanos", "fascistas", "arquitectos", "antidisturbios", "estibadores", "declaraciones", "arrestos", "curiosos", "surfistas", "empleadas", "valverde\u00f1os", "pensionistas", "aut\u00f3nomos", "pacifistas", "moteros", "alumnas", "cocineros", "valencianos", "curt\u00eddores", "encapuchados", "internados", "toxic\u00f3manos", "sanitarios", "jubilados", "quiosqueros", "licenciados", "armenios", "te\u00f3logos", "vascos", "ciclistas", "republicanos", "perjudicados", "drogadictos", "vizca\u00ednos", "personalidades", "candidatos", "encerrados", "colaboradores", "mariscadores", "catalanes", "cooperativistas", "agicultores", "reclusas", "clientes", "integrantes", "cirr\u00f3ticos", "imputados", "drogodependientes", "ceut\u00edes", "refugiados", "ultraderechistas", "m\u00fasicos", "labradores", "granadinos", "proveedores", "preferentistas", "parejas"]
categoryTags = {'Empleo':[1640,11,90,1853,510,1996,1291,255,1923,149,164,347,2211,268,2219,870],
            'Salud':[ 2051,911,1749,125,1803,2151,12,1167,1616],
             'Educacion':[ 234,1513,551,547,1363,346,2254,2087,1960,1501,571,1892,2408,1907],
             'Vivienda':[ 392,943,333,1689,391,991,1297],
             'Seguridad_y_Justicia':[ 207,2299,1138,158,759,2099,147,915,2467,2302,120,517,1117],
             'Medio_ambiente':[ 1754,966,213,138,209,359,1126]
        }
pathData = "../data/protests4.json"

json_data = {}
with open(pathData) as json_file:
    json_data = json.load(json_file)
    list_things =  json_data['things']
    list_tagNames =  json_data['tagNames']
    dict_articles = json_data['articles']
    dict_tagMap =  json_data['tagMap']
    print("Things:" , list_things[0])
    print("TagNames: " , list_tagNames[1])
    firstKey =dict_tagMap.keys()[0] 
    print("TagMap: ",dict_tagMap[firstKey]) #diccionario
    firstKey = dict_articles.keys()[0]
    print("Articles: ", dict_articles[firstKey]) #diccionario
'''    
p_data = pandas.io.json.json_normalize(json_data) 
print(format(p_data))
'''

#CREACION DEL EJE TEMPORAL_1
dateMin = 99999999
dateMax = 00000000
dateFormat = "%Y%m%d"

#CONTAR COSAS POR ARTÍCULO
print("REHACER EL DICCIONARIO")
articleDict = {}
for article in dict_articles.items():
    try:
        id_article = article[0]
        title = article[1][u'title']
        date = int(article[1][u'date'])
        tags = article[1][u'tags']
        categories = []
        
        if(dateMin > date ):
            dateMin = date
        if(dateMax < date ):
            dateMax = date
        categoryKeys = categoryTags.keys()
        for t in tags:
            for cat in categoryKeys:
                if t in categoryTags[cat]:
                    if cat not in categories:
                        categories.append(cat)

        dict_things_size = article[1][u'things']
        stringCosas = []
        imprimir = False
        
        s =[]
        numTotalCosas = 0
        cosas = {}
        for cosa in dict_things_size.items():
            nombreCosa = str(list_things[int(cosa[0])])
            
            if(nombreCosa in validThings):
                cantidadCosa = cosa[1]
                s.append( "    -" + nombreCosa + ": " + str(cantidadCosa))
                cosas[nombreCosa] =  cantidadCosa
                numTotalCosas += cantidadCosa
                imprimir = True
        if(imprimir):
             articleDict[id_article] = {'title': title, 'things': cosas, 'totalThings': numTotalCosas, 'date': date, 'categories': categories}
             print(title + " (" + str(date) + ")")
             for n in s:
                print(n)
        
    except:
        print 
        #print(article[0], " no things added ")
print("articleDict: ", articleDict) 
print("ACABADO DE REHACER EL DICCIONARIO") 
dataArticlesSinEpigrafe = "../data/cosasPorArticulo.json"
try:
    with(open(dataArticlesSinEpigrafe, 'w')) as outfile:
        json.dump(articleDict, outfile)
except:
    print("Error al abrir el archivo:", dataArticlesSinEpigrafe)


#CREACION DEL EJE TEMPORAL_2
print("DateMin: " + str(dateMin))
print("DateMax: " + str(dateMax))
d_startDate = datetime.datetime.strptime(str(dateMin), dateFormat) 
d_endDate = datetime.datetime.strptime(str(dateMax), dateFormat)
numTotalDays = (d_endDate - d_startDate).days+1
rd = relativedelta(d_endDate, d_startDate)
numTotalMonths = rd.months
print("numTotalDays: " + str(numTotalDays))
print("numTotalMonths: " +str(numTotalMonths))

numYears = d_endDate.year- d_startDate.year
numMonths = 475 #(numYears-1)*12 + 12-d_startDate.month+1 + 12-d_endDate.month + 1
print("Years: " + str(numYears), "NumMonths: " + str(numMonths))

dayList = list(range(0,numTotalDays))
dayListFormated = []
for day in dayList:
    realDay = d_startDate + relativedelta(days=day)
    realDayFormated = str(realDay.year)+ str(realDay.month)+ str(realDay.day)#realDay = datetime.datetime.strptime(str(realDay), dateFormat)
    realDayFormated= realDay.strftime("%Y%m%d")
    dayListFormated.append(realDayFormated)
    #print realDayFormated
    
#print dayListFormated

 
dict_numThings = {}
for day in dayListFormated:
    dict_numThings[day] = 0
   # print(day, dict_numThings[day])
    
print("numTotalDays: " + str(numTotalDays))
print ("Length: " + str(len(dayListFormated)))

print(len(dict_numThings))

def writeBorderData():
    print("Min date: ", d_startDate, dayListFormated[0], d_startDate.month)
    print("Max date: ", d_endDate, dayListFormated[len(dayListFormated)-1],  d_endDate.month)
    print("Num days: ", numTotalDays)
    print("dict_numThings: ", len(dict_numThings))
    return 

writeBorderData() 
  
  
for article in articleDict.items():
    date = article[1]['date']
    dict_numThings[str(date)] += article[1]['totalThings']
    #print("date: ", date, " Cosas", dict_numThings[str(date)] )
    
    
dataDatesAndCountThings = "../data/cosasPorFecha.json"
try:
    with(open(dataDatesAndCountThings, 'w')) as outfile:
        json.dump(dict_numThings, outfile)
except:
    print("Error al abrir el archivo:", dataDatesAndCountThings)

#MONTHS
list_index_months = list(range(1, numMonths+1))
months_data = {}
yearLoop = 1976
monthLoop = 5
for index_month in list_index_months:
    months_data[index_month]={"year": yearLoop, 'month': monthLoop, 'things': 0}
    for article in articleDict.items():
        date = article[1]['date']
        month = str(date)[4:6]
        year = str(date)[0:4]
        if month == str(monthLoop) and year == str(yearLoop):
            months_data[index_month]['things']+=article[1]['totalThings'] 
    
    monthLoop +=1
    if monthLoop % 13 == 0:
        monthLoop = 1
        yearLoop +=1
        
#print(yearLoop)
        
  
dataDatesAndCountThings = "../data/cosasPorMes.json"
try:
    with(open(dataDatesAndCountThings, 'w')) as outfile:
        json.dump(months_data, outfile)
except:
    print("Error al abrir el archivo:", dataDatesAndCountThings)
    
    
print(months_data) 
print("Length months: ", len(months_data))       
    
    


categoryKeys = categoryTags.keys()
categories_dict_perMonth = {}
for c in categoryKeys:
    print("HACIENDO CATEGORIA: " + str(c))
    yearLoop = 1976
    monthLoop = 5
    months_data_per_category = {}
    for index_month in list_index_months:
        months_data_per_category[index_month]={'year': yearLoop, 'month': monthLoop, 'things': 0 }
        for article in articleDict.items():
            date = article[1]['date']
            month = str(date)[4:6]
            year = str(date)[0:4]
            categories = article[1]['categories']
            #print(categories)
            if month == str(monthLoop) and year == str(yearLoop) and c in categories:
                months_data_per_category[index_month]['things']+= article[1]['totalThings'] 
         #Cambio mes y año
        monthLoop +=1
        if monthLoop % 13 == 0:
            monthLoop = 1
            yearLoop +=1
    categories_dict_perMonth[str(c)] =  months_data_per_category

print categories_dict_perMonth

  
dataDatesAndCountThings = "../data/cosasPorCategoriaYMes.json"
try:
    with(open(dataDatesAndCountThings, 'w')) as outfile:
        json.dump(categories_dict_perMonth, outfile)
except:
    print("Error al abrir el archivo:", dataDatesAndCountThings)

if __name__ == '__main__':
    print("------")
   