import matplotlib.pyplot as plt
import random

"""
Se tiene el siguiente escenario:
•	En cada evento, los pilotos realizan la “clasificación” o “qualy” que es una sesión en donde 
los autos están en su máximo performance y en donde los pilotos pueden llevar los autos al límite. 
En estas sesiones la última vuelta es la que importa. 
•	Se debe tomar el tiempo de cada piloto en la última vuelta en 5 eventos en específico 
(Mónaco, Silverstone, SPA, Zandvoort y Abu Dhabi).
•	Se debe graficar la clasificación de los pilotos en los cinco Grandes Premios anteriormente 
mencionados y así poder determinar tanto a nivel de equipo como a nivel de piloto quien es el mejor.

"""
#-----------------------------------------------------------------------------------------------------
"""
Consideraciones:
•	Debe utilizar la función random.seed() y recibir como parámetro un código numérico para 
inicializarla. Por ejemplo: 135711.
•	Debe utilizar orientación a objetos para representar pilotos y equipos.
•	Debe utilizar matplotlib para la generación del gráfico, estando permitido también utilizar 
la librería pandas para la preparación de los datos.
"""
semilla = 135711
aleatorio = random.seed(semilla)
listaParticipantes = [] #Lista que contendrá todos los objetos "Participantes"

# Definir clase que contenga a los pilotos:
class Participantes:

    def __init__(self, equipo, nombre, edad) -> None:
        self.equipo = equipo
        self.nombre = nombre
        self.edad = edad
        self.tiempoVuelta = {} # Dict. para agregar para cada participante la pista y el tiempo de compleción

    # Sólo para mostrar mejor los datos
    def __str__(self):
        return f"Equipo: {self.equipo}, nombre: {self.nombre}, edad: {self.edad}"

    def pistas(self, nombrePista, tiempo):
        self.tiempoVuelta[nombrePista] = tiempo  

    # Sólo para mostrar pistas y tiempo de compleción por piloto
    def imprime_tiempo_vuelta(self):
        return f"Piloto: {self.nombre}\nEstadisticas: {self.tiempoVuelta}"


# csv que contiene la información sobre los equipos, con cada uno de sus pilotos y su edad
def leer_equipos():
    equipos = open("equipos.csv", "r", encoding='utf-8-sig')
    listaEquipos = []
    for fila in equipos:
        fila = fila.rstrip()
        listaEquipos.append(fila.split(","))
    return listaEquipos

# csv que contiene la información sobre el evento y cuánto es el tiempo aproximado en que un competidor
# puede dar una vuelta
def leer_tracks(): 
    pistas = open("tracks.csv", "r", encoding='utf-8-sig')
    listaPistas = []
    for fila in pistas:
        fila = fila.rstrip()
        listaPistas.append(fila.split(","))
    return listaPistas
    
# Itera sobre el archivo de pilotos para crear los objetos Participante
def genera_participantes():
    listaEquipos = leer_equipos()
    for fila in listaEquipos:
        if fila[0] == "nombre_equipo": #Para saltarse el encabezado
            continue
        listaParticipantes.append(Participantes(fila[0],fila[1],fila[2]))
        listaParticipantes.append(Participantes(fila[0],fila[3],fila[4]))
    return listaParticipantes

# Simular las vueltas de cada piloto según el "qualy", usando random 
# entre el tiempo récord y el estimado del track.csv
def simular_vueltas():
    listaPistas = leer_tracks()
    for fila in listaPistas:
        if fila[0] == "Round": #Para saltarse la primera fila
            continue
        generar_csv(fila[2], int(fila[-1]), float(fila[6]), float(fila[7]))
    return listaPistas

# Se debe generar un csv que tenga los resultados obtenidos de la simulación (Piloto; Equipo; L1~L{qualy})
# El nombre del archivo debe estar compuesto de la palabra "resultado_" y el nombre corto de la pista
def generar_csv(nombre_pista, qualy_laps, t_record, t_estimado):
    nombreArchivo = f"resultado_{nombre_pista}.csv"
    archivo = open(nombreArchivo, "w")
    encabezado = ["piloto", "equipo"]
    encabezado.extend(["L"+str(i) for i in range(1, qualy_laps+1)])
    archivo.write(",".join(encabezado)+"\n")
    linea = []
    for i in listaParticipantes:
        linea.append(i.nombre)
        linea.append(i.equipo)
        for _ in range(qualy_laps):
            linea.append(str(round(random.uniform(t_record, t_estimado),2)))
        archivo.write(",".join(linea)+"\n")
        linea.clear()
    archivo.close()

# Función para abrir los archivos csv generados y almacenar la información necesaria en cada piloto
# para luego generar el gráfico (nombre piloto, pista, tiempo última vuelta)
def leer_simulacion():
    listaPistas = leer_tracks()
    nombrePistas = [] #Contendrá sólo el nombre del archivo a abrir
    for i in listaPistas:
        if i[2] == "Short_Name": #Para saltar el encabezado
            continue
        nombrePistas.append(i[2])
    for j in nombrePistas:
        nombreArchivo = f"resultado_{j}.csv"
        archivo = open(nombreArchivo, "r")
        for numero, fila in enumerate(archivo):
            fila = fila.rstrip().split(",")
            if fila[0] == "piloto": #Saltar encabezado
                continue
            listaParticipantes[numero-1].pistas(j,float(fila[-1])) # Para llenar el diccionario del objeto

# Una vez generado los archivos estos deben ser leídos para poder generar el gráfico 
# con el tiempo de la última vuelta
def generar_grafico():
    ax = plt.subplot()
    # Itera sobre cada objeto, y asigna los valores para el gráfico
    for i in listaParticipantes:
        ax.plot(i.tiempoVuelta.keys(),i.tiempoVuelta.values(), label = i.nombre)
    ax.set_xlabel('Pista')
    ax.set_ylabel('Tiempo')
    ax.legend()
    plt.show()

# Esta función sólo ejecuta las funciones necesarias para hacer funcionar el código
def principal():
    genera_participantes()
    simular_vueltas()
    leer_simulacion()
    generar_grafico()

principal()
