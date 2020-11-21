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
import config
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.ADT import orderedmap as om
from DISClib.ADT import queue as qu
from DISClib.DataStructures import edge as e
from DISClib.DataStructures import mapentry as me
from DISClib.DataStructures import listiterator as it
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
assert config

"""
En este archivo definimos los TADs que vamos a usar y las operaciones
de creacion y consulta sobre las estructuras de datos.
"""

# -----------------------------------------------------
#                       API
# -----------------------------------------------------
def newAnalyzer():
    """ Inicializa el analizador
   trips: Grafo para representar las rutas entre estaciones
   components: Almacena la informacion de los componentes conectados
   paths: Estructura que almancena los caminos de costo minimo desde un
           vertice determinado a todos los otros vértices del grafo
    """
    try:
        analyzer = {
                    'trips': None,
                    'components': None,
                    "stations":None,
                    "popularity":None,
                    "publicity":None,
                    "NumTrips": 0
                    }

        analyzer['trips'] = gr.newGraph(datastructure='ADJ_LIST',
                                  directed=True,
                                  size=1500,
                                  comparefunction=compareStations)
        analyzer["stations"] = m.newMap(1000,  
                                   maptype='CHAINING', 
                                   loadfactor=5, 
                                   comparefunction=compareNameInEntry)
        analyzer['popularity'] ={
                                    "in": {"1mayor":(0,""),"2mayor":(0,""),"3mayor":(0,"")},
                                    "out" : {"1mayor":(0,""),"2mayor":(0,""),"3mayor":(0,"")},
                                    "LessPopular" : {"1menor":(float("inf"),""),"2menor":(float("inf"),""),"3menor":(float("inf"),"")},
                                    "ByAges" : lt.newList("ARRAY_LIST", compare)
                                    }
        analyzer["publicity"] = {
                                    "ByAges" : lt.newList("ARRAY_LIST", compare),
                                    "BestPublicity":lt.newList("ARRAY_LIST", compare)
                                    }
        popularity = analyzer['popularity']
        publicity = analyzer["publicity"]
        createAges(popularity["ByAges"])
        createAgesMap(publicity["ByAges"])
        createPopAges(publicity["BestPublicity"])
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')

def createAges(lstAges):
    """
    Se crea una lista donde cada posicion 
    va a representar un rango de edad
    """
    for i in range (0,7):
        age_entry = {"in":(0,""), "out":(0,""),"route":None}
        lt.addLast(lstAges,age_entry)
    return lstAges

def createAgesMap(lstAges):
    """
    Se crea una lista donde cada posicion 
    va a representar un rango de edad
    y crea un mapa para almacenar las rutas
    """
    for i in range (0,7):
        age_entry = m.newMap(1000,  
                            maptype='CHAINING', 
                            loadfactor=5, 
                            comparefunction=compareNameInEntry)
        lt.addLast(lstAges,age_entry)
    return lstAges

def createPopAges(lstAges):
    """
    Se crea una lista donde cada posicion 
    va a representar un rango de edad
    """
    for i in range (0,7):
        age_entry = lt.newList("SINGLE_LINKED", compare)
        lt.addLast(age_entry,(0,""))
        lt.addLast(lstAges,age_entry)
    return lstAges

# Funciones para agregar informacion al grafo

def addTrip(analyzer, trip):
    """
    """
    origin = trip['start station id']
    destination = trip['end station id']
    duration = int(trip['tripduration'])
    age = 2018 - int(trip["birth year"])
    subType =trip["usertype"]
    addStation(analyzer, origin)
    addStation(analyzer, destination)
    addConnection(analyzer, origin, destination, duration)
    addSatationInfo(analyzer, origin, destination, age, subType)
    analyzer["NumTrips"] += 1

def addStation(analyzer, stationid):
    """
    Adiciona una estación como un vertice del grafo y como
    nueva llave al mapa
    """
    if not gr.containsVertex(analyzer ["trips"], stationid):
            gr.insertVertex(analyzer ["trips"], stationid)
            entry = newStation(stationid)
            m.put(analyzer["stations"],stationid,entry)
    return analyzer

def addConnection(analyzer, origin, destination, duration):
    """
    Adiciona un arco entre dos estaciones
    """
    edge = gr.getEdge(analyzer ["trips"], origin, destination)
    if edge is None:
        gr.addEdge(analyzer["trips"], origin, destination, duration)
    else:
        weight = e.weight(edge)
        prom = (duration + weight)/2
        edge['weight'] = prom
    return analyzer

def newStation(stationId):
    """
    Crea una entrada para la estacion en el mapa
    """
    entry = {"in":0,"out":0,"Ages" : lt.newList("ARRAY_LIST", compare)}
    for i in range(0,7):
        secondEntry = {"in":0, "out":0}
        lt.addLast(entry["Ages"],secondEntry)
    return entry

def addSatationInfo(analyzer, origin, destination, age, subType):
    age = str(age)
    if len(age) == 1:
        age = "0"+age
    category = int(age[0])+1
    if (age[1]=="0") and (category != 1):
        category -=1
    if category > 6:
        category = 7
    entryO = m.get(analyzer["stations"], origin)
    entryD = m.get(analyzer["stations"], destination)
    originInfo = me.getValue(entryO)
    desInfo = me.getValue(entryD)
    changeStationInfo(origin, "out",category, originInfo, analyzer)
    changeStationInfo(destination, "in",category, desInfo, analyzer)
    if subType == "Customer":
        popAdvisor(origin,destination,category, analyzer)
    return analyzer

def changeStationInfo(station, inOrOut, category, stationInfo, analyzer):
    """
    Agrega viajes a una estacion dependiendo de
    el rango de edad, si es origen o no
    """
    stationInfo[inOrOut] = stationInfo[inOrOut] + 1
    lstAges = stationInfo["Ages"]
    infoCat = lt.getElement(lstAges,category)
    newNum = infoCat[inOrOut] + 1
    infoCat[inOrOut] = newNum
    return analyzer

def popAdvisor(origin,destination,category, analyzer):
    """
    Añade la estacion a el mapa de populares,
    y en caso de cumplir con los requisitos mira 
    su popularidad como estacion publicitaria
    """
    route = origin + "-" + destination
    mapCategory = lt.getElement(analyzer["publicity"]["ByAges"],category)
    existsRoute = m.contains(mapCategory, route)
    if existsRoute:
        entry = m.get(mapCategory, route)
        routeTimes = me.getValue(entry) + 1
        me.setValue(entry,routeTimes)
    else:
        routeTimes = 1
        m.put(mapCategory, route, routeTimes)
    return analyzer
    
def findPopulars(analyzer):
    lstVert = gr.vertices(analyzer["trips"])
    vertIterator = it.newIterator(lstVert)
    while it.hasNext(vertIterator):
        vert = it.next(vertIterator)
        popular(vert,analyzer)
        popularByAges(vert,analyzer)
    updateShortestRoutes(analyzer)
    return analyzer

def popular(vert,analyzer):
    """
    Compara los vertices para buscar los más
    populares, y los menos populares
    """
    vertMapEntry = m.get(analyzer["stations"],vert)
    vertDict = me.getValue(vertMapEntry)
    NumIn = vertDict["in"]
    NumOut = vertDict["out"]
    total = NumIn + NumOut
    compareWithMax(analyzer['popularity']["in"],NumIn,vert)
    compareWithMax(analyzer['popularity']["out"],NumOut,vert)
    compareWithMin(analyzer['popularity']["LessPopular"],total,vert)
    return analyzer

def popularByAges(vert,analyzer):
    """
    Compara los vertices para buscar los más
    populares segun su categoria en edad
    """
    vertMapEntry = m.get(analyzer["stations"],vert)
    vertLst = me.getValue(vertMapEntry)["Ages"]
    mayLst = analyzer['popularity']["ByAges"]
    for i in range(0,7):
        pos = i+1
        mayDict = lt.getElement(mayLst,pos)
        vertDict = lt.getElement(vertLst,pos)
        satTupIn= (vertDict["in"],vert)
        satTupOut= (vertDict["out"],vert)
        if satTupIn>mayDict["in"]:
            mayDict["in"] = satTupIn
        if satTupOut>mayDict["out"]:
            mayDict["out"] = satTupOut
    return analyzer

def compareWithMax(dict,num,vert):
    statTup= (num,vert)
    if statTup > dict["1mayor"]:
        x = 1
        if statTup > dict["2mayor"]:
            x = 2
            if statTup > dict["3mayor"]:
                x = 3
        key1 = str(x)+"mayor"
        value1 = dict[key1]
        for i in range(0,x):
            key2 = str(x-(i))+"mayor"
            value2 = dict[key2]
            dict[key2] = value1
            value1 = value2
        dict[str(x)+"mayor"] = statTup
    return dict

def compareWithMin(dict,num,vert):
    statTup= (num,vert)
    if statTup < dict["1menor"]:
        x = 1
        if statTup < dict["2menor"]:
            x = 2
            if statTup < dict["3menor"]:
                x = 3
        key1 = str(x)+"menor"
        value1 = dict[key1]
        for i in range(0,x):
            key2 = str(x-(i))+"menor"
            value2 = dict[key2]
            dict[key2] = value1
            value1 = value2
        dict[str(x)+"menor"] = statTup
    return dict

def updateShortestRoutes(analyzer):
    """
    Busca las rutas mas contras entre
    las estaciones más visitadas po un 
    rango de edad
    """
    mayLst = analyzer['popularity']["ByAges"]
    for pos in range(1,8):
        mayDict = lt.getElement(mayLst,pos)
        numIn,inStat = mayDict["in"]
        numOut,outStat = mayDict["out"]
        if (numIn and numOut) != 0:
            queue  = getShortestRoute(analyzer["trips"], outStat, inStat)
            mayDict["route"] = queue
    return analyzer

def findPopularsAdd(analyzer): 
    """
    Compara los vertices para buscar los más
    populares segun su categoria en edad 
    que cumplen los requerimientos para
    tener publicidad
    """
    mayLst = analyzer["publicity"]["BestPublicity"]
    catLst = analyzer["publicity"]["ByAges"]
    for pos in range(1,8):
        total = 0
        mayCatLst = lt.getElement(mayLst,pos)
        mayTup = lt.firstElement(mayCatLst)
        routesMap = lt.getElement(catLst,pos)
        routesLst = m.keySet(routesMap)
        routeIterator = it.newIterator(routesLst)
        while it.hasNext(routeIterator):
            vert = it.next(routeIterator)
            routeEntry = m.get(routesMap,vert)
            timesRoute = me.getValue(routeEntry)
            total += timesRoute
            routeTuple = (timesRoute,vert)
            if mayTup < routeTuple:
                size = lt.size(mayCatLst)
                if size > 1:
                    for i in range(0,size-1):
                        lt.deleteElement(mayCatLst,1)
                lt.changeInfo(mayCatLst,1,routeTuple)
        lt.addLast(mayCatLst,total)
    return analyzer
    
# ==============================
# Funciones de consulta
# ==============================

def connectedComponents(analyzer):
    """
    Calcula los componentes conectados del grafo
    Se utiliza el algoritmo de Kosaraju
    """
    analyzer['components'] = scc.KosarajuSCC(analyzer['trips'])
    return scc.connectedComponents(analyzer['components'])

def sameCC(analyzer, station1, station2):
    """
    """
    sccDict = analyzer['components']
    return scc.stronglyConnected(sccDict, station1, station2)

def getRankMay(analyzer,key1):
    """
    Retorna las tres estaciones mas populares 
    en llegadas, salidas y las poco visitadas
    """
    third = analyzer['popularity'][key1]["1mayor"]
    second = analyzer['popularity'][key1]["2mayor"]
    first = analyzer['popularity'][key1]["3mayor"]
    return (first,second,third)

def getRankMen(analyzer,key1):
    """
    Retorna las tres estaciones mas populares 
    en llegadas, salidas y las poco visitadas
    """
    third = analyzer['popularity'][key1]["1menor"]
    second = analyzer['popularity'][key1]["2menor"]
    first = analyzer['popularity'][key1]["3menor"]
    return (first,second,third)

def getShortestRoute(analyzer, station1, station2):
    """
    Busca la ruta más corta con algoritmo
    dijsktra as djk
    """
    search = djk.Dijkstra(analyzer,station1)
    queuePath = djk.pathTo(search, station2)
    return queuePath

def getRecommendedRoute(analyzer,cat):
    """
    Retorna las estaciones donde la
    categoria indicada inicia mas viajes,
    donde más los termina y la ruta entre
    ellos 
    """
    mayLst = analyzer['popularity']["ByAges"]
    catDict = lt.getElement(mayLst,cat)
    inStat = catDict["in"]
    outStat = catDict["out"]
    route = catDict["route"]
    return (inStat,outStat,route)

def getPublicityRoute(analyzer,cat):
    """
    Retorna las estaciones donde la es
    indicado poner pubilicad para un 
    gurpo de edad
    """
    mayLst = analyzer["publicity"]["BestPublicity"]
    catLst = lt.getElement(mayLst,cat)
    return catLst

def totalStations(analyzer):
    """
    Retorna el total de estaciones (vertices) del grafo
    """
    return gr.numVertices(analyzer['trips'])

def totalConnections(analyzer):
    """
    Retorna el total arcos del grafo
    """
    return gr.numEdges(analyzer['trips'])

def totalTrips(analyzer):
    """
    Retorna el total viajes
    """
    return analyzer['NumTrips']

def stationInGraph(analyzer, stationId):
    """
    Revisa que la estacion se encuentre en el grafo
    """
    graph = analyzer["trips"]
    return gr.containsVertex(graph, stationId)

def lstSize(lst):
    """
    Retorna el tamaño de una lista
    """
    return lt.size(lst)

# ==============================
# Funciones Helper
# ==============================

def convertQueueToStr(queue):
    """
    Toma la cola con la ruta más corta
    y la convierte a un string
    """
    size = qu.size(queue)
    strRoute = ""
    for i in range(0,size):
        stat = qu.dequeue(queue)
        strRoute = strRoute + str(stat['vertexA'])+ " - "
    strRoute = strRoute + stat['vertexB']
    return strRoute

# ==============================
# Funciones de Comparacion
# ==============================

def compareStations(satationId, keyvalueStat):
    """
    Compara dos estaciones
    """
    Statcode = keyvalueStat['key']
    if (satationId == Statcode):
        return 0
    elif (satationId > Statcode):
        return 1
    else:
        return -1

def compare(item1, item2):
    """
    Compara dos elementos
    """
    if (item1 == item2):
        return 0
    elif (item1 > item2):
        return 1
    else:
        return -1

def compareNameInEntry(keyname, entry):
    """
    Compara un nombre con una llave de una entrada
    """
    pc_entry = me.getKey(entry)
    if (keyname == pc_entry):
        return 0
    elif (keyname > pc_entry):
        return 1
    else:
        return -1
