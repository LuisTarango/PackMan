#Luis Fernando Tarango Falix   A00827678
#Hiram David Arguelles Ramirez A00826301
from random import choice
from turtle import *
from freegames import floor, vector

state = {'score': 0}        #Variable que mantiene puntaje
path = Turtle(visible=False)        #Variable que define el camino
writer = Turtle(visible=False)
aim = vector(5, 0)                  #Variable que define direccion y magnitud del movimiento del pacman
pacman = vector(-40, -80)           #Posicion inicial del packmane
ghosts = [                          #Posicion, velocidades y direcciones inicales de los fantasmas
    [vector(-180, 160), vector(10, 0)],
    [vector(-180, -160), vector(0, 10)],
    [vector(100, 160), vector(0, -10)],
    [vector(100, -160), vector(-10, 0)],
]
#Se modifico al mapa cambiando la configuaracoion de la matriz para hacerle modificacon al mapa 
#Se agrego el nombre del equipo almapa 
tiles = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0,
    0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0,
    0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0,
    0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0,
    0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0,
    0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0,
    0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0,
    0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0,
    0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0,
    0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0,
]

def square(x, y):       #Crea los cuadros para dibujar el tablero
    "Draw square using path at (x, y)."
    path.up()
    path.goto(x, y)
    path.down()
    path.begin_fill()

    for count in range(4):
        path.forward(20)
        path.left(90)

    path.end_fill()

def offset(point):
    "Return offset of point in tiles."
    x = (floor(point.x, 20) + 200) / 20
    y = (180 - floor(point.y, 20)) / 20
    index = int(x + y * 20)
    return index

def valid(point):       #Revisa que donde se quiera mover sea una posicion valida
    "Return True if point is valid in tiles."
    index = offset(point)

    if tiles[index] == 0:
        return False

    index = offset(point + 19)

    if tiles[index] == 0:
        return False

    return point.x % 20 == 0 or point.y % 20 == 0

def world():        #Dibuja el camino del tablero
    "Draw world using path."
    bgcolor('black')
    path.color('blue')

    for index in range(len(tiles)):
        tile = tiles[index]

        if tile > 0:        #Revisa que elementos de la matriz son 1s para poder dibujar el laberitno en base a ellos
            x = (index % 20) * 20 - 200
            y = 180 - (index // 20) * 20
            square(x, y)

            if tile == 1:
                path.up()
                path.goto(x + 10, y + 10)
                path.dot(2, 'white')

def move():     #Se define como se mueve el pacman y los fantasmas
    "Move pacman and all ghosts."
    writer.undo()
    writer.write(state['score'])

    clear()

    if valid(pacman + aim):     #Revisa si el pacman se puede mover en la direccion a la que esta viendo
        pacman.move(aim)

    index = offset(pacman)

    if tiles[index] == 1:       #Revisa si el pacman a obtenido un punto
        tiles[index] = 2
        state['score'] += 1
        x = (index % 20) * 20 - 200
        y = 180 - (index // 20) * 20
        square(x, y)

    up()
    goto(pacman.x + 10, pacman.y + 10)
    dot(20, 'yellow')

    for point, course in ghosts:        #Se encarha del movimiento de los fanatsmas
        if valid(point + course):       #Hara que el fantasama se mueva hasta chocar con una pared
            point.move(course)
        else:                           #Al quedarse sin camino incilizara este script para obtener uno nuevo
            
            if pacman.x > point.x and pacman.y > point.y: #En esta serie de ifs se le dan opciones a los fantasmas que prioritizan el acercarse hacia el pacmanpara hacerlo mas desafiante
                options = [
                vector(10, 0),
                vector(10, 0),
                vector(10, 0),
                vector(-10, 0),
                vector(0, 10),
                vector(0, 10),
                vector(0, 10),
                vector(0, -10),
            ]
            elif pacman.x < point.x and pacman.y > point.y:
                options = [
                vector(10, 0),
                vector(-10, 0),
                vector(-10, 0),
                vector(-10, 0),
                vector(0, 10),
                vector(0, 10),
                vector(0, 10),
                vector(0, -10),
            ]
            elif pacman.x > point.x and pacman.y < point.y:
                options = [
                vector(10, 0),
                vector(10, 0),
                vector(10, 0),
                vector(-10, 0),
                vector(0, 10),
                vector(0, -10),
                vector(0, -10),
                vector(0, -10),
            ]
            elif pacman.x < point.x and pacman.y < point.y:
                options = [
                vector(10, 0),
                vector(-10, 0),
                vector(-10, 0),
                vector(-10, 0),
                vector(0, 10),
                vector(0, -10),
                vector(0, -10),
                vector(0, -10),
            ]
            else:
                options = [         #Este else es en caso de que se encuentren en un punto en comun, dar oportunidad al jugador de no ser perseguido
                vector(10, 0),
                vector(-10, 0),
                vector(0, 10),
                vector(0, -10),
                ]

            plan = choice(options)
            course.x = plan.x
            course.y = plan.y

        up()
        goto(point.x + 10, point.y + 10)
        dot(20, 'red')

    update()

    for point, course in ghosts:
        if abs(pacman - point) < 20:
            return

    ontimer(move, 100)

def change(x, y):                   #Cambia la direccion del pacman a otra que tiene valida para el laberinto
    "Change pacman aim if valid."
    if valid(pacman + vector(x, y)):
        aim.x = x
        aim.y = y


#Set up de la ventana y colores
setup(420, 620, 370, 0)
hideturtle()
tracer(False)
writer.goto(160, 160)
writer.color('white')
writer.write(state['score'])
listen()

#Se encargan de registrar los inputs del packman
onkey(lambda: change(5, 0), 'Right')
onkey(lambda: change(-5, 0), 'Left')
onkey(lambda: change(0, 5), 'Up')
onkey(lambda: change(0, -5), 'Down')

world()
move()
done()
