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
import sys
import config
from App import controller
from DISClib.ADT import stack
from DISClib.DataStructures import listiterator as it
import timeit
assert config
"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""
# ___________________________________________________
#  Variables
# ___________________________________________________
file1 = '201801-1-citibike-tripdata.csv'
file2 = '201801-2-citibike-tripdata.csv'
file3 = '201801-3-citibike-tripdata.csv'
file4 = '201801-4-citibike-tripdata.csv'
copia= "201801-1-citibike-tripdata copy.csv"
#Archivos que se van a cargar
totalFiles = [file1]
# ___________________________________________________
#  Menu principal
# ___________________________________________________
def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información de rutas citybike")
    print("3- Cantidad de clusters de Viajes")
    print("4- Ruta turística Circular")
    print("5- Estaciones críticas ")
    print("6- Ruta turística por resistencia ")
    print("7- Recomendador de Rutas  ")
    print("8- Ruta de interés turístico  ")
    print("9- Identificación de Estaciones para Publicidad ")
    print("10- Identificación de Bicicletas para Mantenimiento ")
    print("0- Salir")
    print("*******************************************")
def optionTwo():
    print("\nCargando información de rutas citybike ....")
    controller.loadFiles(analyzer, totalFiles)
    numTrips = controller.totalTrips(analyzer)
    numedges = controller.totalConnections(analyzer)
    numvertex = controller.totalStations(analyzer)
    print('Numero de viajes: ' + str(numTrips))
    print('Numero de vertices: ' + str(numvertex))
    print('Numero de arcos: ' + str(numedges))
def optionThree():
    try:
        print('El número de componentes conectados es: ' +
              str(controller.connectedComponents(analyzer)))
        if id1.isdigit() and id2.isdigit():
            connected = controller.verticesSCC(analyzer, id1, id2)
            if connected:
                print("Las estaciones con codigo "+id1+" y "+id2+" pertenecen al mismo cluster")
            elif connected is None:
                print("No se puede hacer la busqueda, intente con estaciones diferentes")
            else:
                print("Las estaciones con codigo "+id1+" y "+id2+" no pertenecen al mismo cluster")
        else:
            print("Los ID tienen que ser un numero natural, intente con entradas diferentes")
    except:
        print("Hubo un error en la busqueda")
def optionFour():
    pass
def optionFive():
    try:
        mayIn,mayOut,less = controller.getCriticStation(analyzer)
        first,second,third = mayIn
        print("Las 3 estaciones Top de llegada son: \n")
        num,stat = first
        print("1. "+stat+ " con "+str(num)+" llegadas")
        num2,stat2 = second
        print("2. "+stat2+ " con "+str(num2)+" llegadas")
        num3,stat3 = third
        print("3. "+stat3+ " con "+str(num3)+" llegadas\n")
        first2,second2,third2 = mayOut
        print("Las 3 estaciones Top de salida son: \n")
        num4,stat4 = first2
        print("1. "+stat4+ " con "+str(num4)+" salidas")
        num5,stat5 = second2
        print("2. "+stat5+ " con "+str(num5)+" salidas")
        num6,stat6 = third2
        print("3. "+stat6+ " con "+str(num6)+" salidas\n")
        print("Las 3 estaciones menos visitadas son: ")
        first3,second3,third3 = less
        num7,stat7 = first3
        print("1. "+stat7+ " con "+str(num7)+" visitas")
        num8,stat8 = second3
        print("2. "+stat8+ " con "+str(num8)+" visitas")
        num9,stat9 = third3
        print("3. "+stat9+ " con "+str(num9)+" visitas\n")
    except:
        print("Hubo un error en la busqueda")
def optionSix():
    try:
        if id.isdigit() and (int(res)>0) and res.isdigit():
            rutas=controller.rutas(analyzer,id,int(res))
            routeIterator = it.newIterator(rutas)
            if rutas["first"] == None:
                print("No se puede hacer la busqueda, intente con estaciones diferentes")
            else:
                print("Rutas que puede hacer desde la estación de salida: ")
                i=1
                while it.hasNext(routeIterator):
                    routeDict = it.next(routeIterator)
                    print(str(i)+". :")
                    print("\tNombre de la estación de inicio: "+str(routeDict["startName"]))
                    print("\tNombre de la estación de final: "+str(routeDict["endName"]))
                    print("\tTiempo por segmentos:")
                    segIterator = it.newIterator(routeDict["Seg"])
                    while it.hasNext(segIterator):
                        seg,timeSeg = it.next(segIterator)
                        print("\t"+seg+": "+str(timeSeg)+" segundos.")
                    print("Duración estimada de la ruta: "+str(routeDict["time"])+"\n")
                    i +=1
        else:
            print("Las entradas tienen que ser un numero natural, intente con entradas diferentes")
    except:
            print("Hubo un error en la busqueda")
def optionSeven():
    try:
        if (cat.isdigit()) and (int(cat)>0) and (int(cat)<8):
            inStat,outStat,strRoute = controller.getRecommendedRoute(analyzer,int(cat))
            numIn,statIn = inStat
            numOut,statOut = outStat
            print("La estacion donde las personas del rango de edad más llegan es la "+ statIn+ " con "+str(numIn)+ " llegadas.")
            print("La estacion donde las personas del rango de edad más salen es la "+ statOut+ " con "+str(numOut)+ " salidas.")
            if "-" in strRoute:
                print("La ruta más corta para llegar de " +statOut+" a "+statIn+" es "+strRoute+"\n")
            else:
                print(strRoute)
        else:
            print("La categoria ingresada debe ser un numero natural entre 1 y 7")
    except:
        print("Hubo un error en la busqueda")

def optionEight():
    try:
        if (id.isdigit()) and (int(id)>0):
            routeBike=controller.bike(analyzer,date,id)
            if routeBike == (None, None, None):
                print("No se puede hacer la busqueda, intente con datos diferentes")
            else:
                use,parked,stations=routeBike
                routeIterator = it.newIterator(stations)
                print("El tiempo total de uso de la bicicleta fue :"+str(use))
                print("El tiempo total estacionada de la bicicleta fue :"+str(parked))
                print("Lista de todas las estaciones por las que ha pasado: ")
                while it.hasNext(routeIterator):
                    route = it.next(routeIterator)
                    print("\t"+str(route))
        else:
            print("Las entradas tienen que ser un numero natural, intente con entradas diferentes")
    except:
        print("Hubo un error en la busqueda")
def optionNine():
    try:
        if (cat.isdigit()) and (int(cat)>0) and (int(cat)<8):
            catLst,size = controller.getPublicityRoute(analyzer,int(cat))
            routeIterator = it.newIterator(catLst)
            ite = 1
            if size > 2:
                print("Las rutas que son las más adecuadas para publicidad dentro del rango de edad ingresado son:\n")
            else:
                print("La ruta que es la más adecuada para publicidad dentro del rango de edad ingresado es:\n")
            while it.hasNext(routeIterator) and (ite<size):
                routeTup = it.next(routeIterator)
                num,route = routeTup
                if num == 0:
                    print("No hay viajes registrados que cumplan con los requisitos en ese grupo de edad")
                else:
                    print("La ruta "+route+" con "+str(num)+" veces realizada.")
                ite +=1
            total = it.next(routeIterator)
            print("\nHubo "+str(total)+" viajes hechos por personas del rango de edad ingresado que tienen suscripción de 3 días")   
        else:
            print("La categoria ingresada debe ser un numero natural entre 1 y 7")
    except:
        print("Hubo un error en la busqueda")
def categorias():
    print("Escoja la categoria de edad a la cual pertenece:\n")
    print("1-(0-10)")
    print("2-(11-20)")
    print("3-(21-30)")
    print("4-(31-40)")
    print("5-(41-50)")
    print("6-(51-60)")
    print("7-(60+)\n")
    cat = input("Ingrese el numero de su categoria:")
    return cat

def archivosCargados():
    if analyzer is None:
        return False
    else:
        return True
"""
Menu principal
"""
analyzer = None
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')
    if int(inputs[0]) == 1:
        print("\nInicializando....")
        # cont es el controlador que se usará de acá en adelante
        analyzer = controller.init()
        print("\nAnalizador iniciado con exito")
    elif int(inputs[0]) == 2:
        if archivosCargados():
            executiontime = timeit.timeit(optionTwo, number=1)
            print("Tiempo de ejecución: " + str(executiontime))
        else:
            print("Se necesita tener el analizador inicializado antes de ejecutar esta opción")
    elif int(inputs[0]) == 3:
        if archivosCargados():
            id1 = input('Ingrese el ID de la primera estacion: ' )
            id2 = input('Ingrese el ID de la segunda estacion: ' )
            executiontime = timeit.timeit(optionThree, number=1)
            print("Tiempo de ejecución: " + str(executiontime))
        else:
            print("Se necesita tener el analizador inicializado antes de ejecutar esta opción")
    elif int(inputs[0]) == 4:
        executiontime = timeit.timeit(optionFour, number=1)
        print("Tiempo de ejecución: " + str(executiontime))
    elif int(inputs[0]) == 5:
        if archivosCargados():
            executiontime = timeit.timeit(optionFive, number=1)
            print("Tiempo de ejecución: " + str(executiontime))
        else:
            print("Se necesita tener el analizador inicializado antes de ejecutar esta opción")
    elif int(inputs[0]) == 6:
        if archivosCargados():
            res=input("Ingrese el tiempo máximo de resistencia: ")
            id=input("Ingrese el id de la estación inicial: ")
            executiontime = timeit.timeit(optionSix, number=1)
            print("Tiempo de ejecución: " + str(executiontime))
        else:
            print("Se necesita tener el analizador inicializado antes de ejecutar esta opción")
    elif int(inputs[0]) == 7:
        if archivosCargados():
            cat = categorias()
            executiontime = timeit.timeit(optionSeven, number=1)
            print("Tiempo de ejecución: " + str(executiontime))
        else:
            print("Se necesita tener el analizador inicializado antes de ejecutar esta opción")
    elif int(inputs[0]) == 8:
        if archivosCargados():
            id=input("Ingrese el id de la bicicleta: ")
            date=input("Ingrese la fecha, en el formato (DD-MM-AA), que desea consular: ")
            executiontime = timeit.timeit(optionEight, number=1)
            print("Tiempo de ejecución: " + str(executiontime))
        else:
            print("Se necesita tener el analizador inicializado antes de ejecutar esta opción")
    elif int(inputs[0]) == 9:
        if archivosCargados():
            cat = categorias()
            executiontime = timeit.timeit(optionNine, number=1)
            print("Tiempo de ejecución: " + str(executiontime))
        else:
            print("Se necesita tener el analizador inicializado antes de ejecutar esta opción")
    else:
        sys.exit(0)
sys.exit(0)