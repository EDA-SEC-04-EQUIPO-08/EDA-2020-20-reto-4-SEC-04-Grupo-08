"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * Contribución de:
 *
 * Dario Correal
 *
 """

import config as cf
from App import model
import csv

"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""

# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________

def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # analyzer es utilizado para interactuar con el modelo
    analyzer = model.newAnalyzer()
    return analyzer

# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________

def loadTrips(analyzer, tripsfile):
    """
    Carga los datos de los archivos CSV en el modelo
    """
    tripsfile = cf.data_dir + tripsfile
    input_file = csv.DictReader(open(tripsfile, encoding="utf-8"),
                                delimiter=",")
    for trip in input_file:
        model.addTrip(analyzer, trip)
    return analyzer

def loadFiles(analyzer,totalFiles):
    """
    Carga todos los archivos
    """
    for filename in totalFiles:
        if filename.endswith('.csv'):
            print('Cargando archivo: ' + filename)
            loadTrips(analyzer, filename)
    print("Cargando información extra...")
    model.findPopulars(analyzer)
    model.findPopularsAdd(analyzer)
    return analyzer

# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________

def connectedComponents(analyzer):
    """
    Numero de componentes fuertemente conectados
    """
    return model.connectedComponents(analyzer)

def verticesSCC(analyzer, station1, station2):
    """
    """
    present1 = stationInGraph(analyzer, station1)
    present2 = stationInGraph(analyzer, station2)
    ans = None
    if present1 and present2:
        ans = model.sameCC(analyzer, station1, station2)
    return ans

def getCriticStation(analyzer):
    """
    Retorna las tres estaciones mas populares 
    en llegadas, salidas y las poco visitadas
    """
    mayIn = model.getRankMay(analyzer,"in")
    mayOut=model.getRankMay(analyzer,"out")
    less=model.getRankMen(analyzer,"LessPopular")
    return (mayIn,mayOut,less)

def getRecommendedRoute(analyzer,cat):
    """
    Retorna las estaciones más donde la
    categoria indicada inicia mas viajes,
    donde más los termina y la ruta entre
    ellos 
    """
    inStat,outStat,route = model.getRecommendedRoute(analyzer,cat)
    if route is not None:
        strRoute = model.convertQueueToStr(route)
    else:
        strRoute = "No hay una ruta entre las dos estaciones" 
    return (inStat,outStat,strRoute)

def getPublicityRoute(analyzer,cat):
    """
    Retorna las estaciones donde la es
    indicado poner pubilicad para un 
    gurpo de edad
    """
    lst = model.getPublicityRoute(analyzer,cat)
    size = model.lstSize(lst)
    return (lst,size)

def rutas(analyzer,id,res):
    return model.rutas(analyzer,id,res)

def getStationName(analyzer,stationId):
    """
    Obtiene el nombre de una estacion a partir de su Id
    """
    name = model.getStationName(analyzer,stationId)
    return name

def totalStations(analyzer):
    """
    Retorna el total de estaciones (vertices) del grafo
    """
    return model.totalStations(analyzer)

def totalConnections(analyzer):
    """
    Retorna el total arcos del grafo
    """
    return model.totalConnections(analyzer)

def totalTrips(analyzer):
    """
    Retorna el total viajes
    """
    return model.totalTrips(analyzer)

def stationInGraph(analyzer, stationId):
    """
    Revisa que la estacion se encuentre en el grafo
    """
    present = model.stationInGraph(analyzer, stationId)
    if not present:
        print("La estacion "+stationId+" no se encuentra registrada")
    return present

def bike(analyzer, date, id):
    """
    Retorna el tiempo total de uso y estacionamiento de una bicicleta
    y la lista de las estaciones por las que ha pasado
    """
    return model.bike(analyzer,date,id)

def getShortestCoordinate (analyzer,startLat, startLon, endLat, endLon):
    """
    Devuelve la ruta entre una coordenada origen y una final
    """
    estacionOrigen=model.getCloserStation (analyzer, startLat, startLon)
    estacionDestino=model.getCloserStation (analyzer, endLat, endLon)
    ruta,tiempo=model.getShortestCoordinate(analyzer,estacionOrigen, estacionDestino)
    return (estacionOrigen,estacionDestino,ruta,tiempo)
 
def getCircularRoute(analyzer, stationId, minTime, maxTime):
    """
    Devuelve las rutas circulares encontradas en el tiempo disponible
    """
    rutas=[]
    ruta=model.getCircularRoute(analyzer, stationId)
    for i in ruta:
        if i["total"]>minTime and i["total"]<maxTime and len(i["lista"])>1:
            rutas.append(i["lista"])
        
    return rutas
