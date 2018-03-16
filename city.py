import mcpi.minecraft as minecraft
import time
from datetime import datetime
import RPi.GPIO as GPIO

mc = minecraft.Minecraft.create()
mc.setting('world_immutable',True)

GPIO.setmode(GPIO.BCM)
#SENSOR HUMEDAD
GPIO.setup(4,GPIO.IN)
#SENSOR LUZ
GPIO.setup(17,GPIO.IN)
#SENSOR TEMPERATURA
GPIO.setup(18,GPIO.IN)
#LEDS DE ALARMAS
GPIO.setup(27,GPIO.OUT)
GPIO.setup(22,GPIO.OUT)



PISOS = 2
ALARMA=[]
LEDS = [22, 27]
LUZ = False
PANEL = False


for i in range(0,PISOS):
	ALARMA.append(False)
	
#Free the space in minecraft world
def freeBlock():
	#15 x 20       x 5        75 x 100
	mc.setBlocks(-50,1,-60,50,50,60,0)
	mc.setBlocks(-50,-10,-60,50,0,60,44)
#Initialize the light in minecraft world
def luzDeDia(light):
	if light:
		mc.setBlocks(-50,50,-60,50,50,60,0)
	else:
		mc.setBlocks(-50,50,-60,50,50,60,1)
#Build the streets
def streets():
	mc.setBlocks(0,1,-35,4,1,40,16)
	mc.setBlocks(35,1,-35,39,1,40,16)

	mc.setBlocks(-30,1,-35,-34,1,40,16)
	mc.setBlocks(-50,1,20,50,1,24,16)
	mc.setBlocks(-50,1,-10,50,1,-14,16)
#Builds the construction
def building(plantas):
	#Central cimientos
	mc.setBlocks(5,1,-9,34,1,19,13)
	mc.setBlocks(6,2,-8,33,2,18,13)
	#Creacion edificio
	level(plantas)
	puerta(False)
	for i in range(0,PISOS):
		crearLuz(i)
	escaleras(plantas)
	ventanas(plantas)
#Build each floor
def level(pisos):
	for i in range(0,pisos):
		mc.setBlocks(7,2+(6*i),-7,32,8+(6*i),17,1)
		mc.setBlocks(8,3+(6*i),-6,31,7+(6*i),16,0)
#Create the building door 
def puerta(persona):

	if persona:
		mc.setBlocks(17,3,17,15,5,17,0)
	else:
		mc.setBlocks(17,3,17,15,5,17,102)
#Build the windows
def ventanas(pisos):
	for i in range(0,pisos):
		mc.setBlocks(10,4+(6*i),17,11,5+(6*i),17,102)

		mc.setBlocks(21,4+(6*i),17,22,5+(6*i),17,102)

		mc.setBlocks(7,4+(6*i),-4,7,5+(6*i),1,102)
		mc.setBlocks(7,4+(6*i),5,7,5+(6*i),9,102)
		mc.setBlocks(7,4+(6*i),12,7,5+(6*i),15,102)


		mc.setBlocks(32,4+(6*i),-4,32,5+(6*i),1,102)
		mc.setBlocks(32,4+(6*i),5,32,5+(6*i),9,102)
		mc.setBlocks(32,4+(6*i),12,32,5+(6*i),15,102)

		mc.setBlocks(10,4+(6*i),-7,11,5+(6*i),-7,102)

		mc.setBlocks(21,4+(6*i),-7,22,5+(6*i),-7,102)

#Create the stairs
def escaleras(pisos):

	for i in range(0,pisos):
		mc.setBlocks(26,3+(6*i),13,27,3+(6*i),13,53,2)
		mc.setBlocks(26,4+(6*i),14,27,4+(6*i),14,53,2)
		mc.setBlocks(26,3+(6*i),14,27,3+(6*i),14,5,2)
		mc.setBlocks(26,5+(6*i),15,27,4+(6*i),15,53,2)
		mc.setBlocks(26,3+(6*i),15,27,4+(6*i),15,5,2)
		mc.setBlocks(26,3+(6*i),16,27,5+(6*i),16,5,2)
		mc.setBlocks(28,5+(6*i),16,29,4+(6*i),16,5,2)
		mc.setBlocks(28,6+(6*i),15,29,6+(6*i),15,53,3)
		mc.setBlocks(28,7+(6*i),14,29,7+(6*i),14,53,3)

		mc.setBlocks(28,8+(6*i),13,29,8+(6*i),13,53,3)
		mc.setBlocks(28,8+(6*i),14,29,8+(6*i),16,0)


#Change the light
def crearLuz(piso):
	mc.setBlocks(9,7+(6*piso),-5,27,7+(6*piso),15,51)
	LUZ = True
	
def noLuz(piso):
	mc.setBlocks(9,7+(6*piso),-5,27,7+(6*piso),15,0)
	LUZ = False

#Create the park
def park():
	mc.setBlocks(-1,1,-9,-29,1,19,2)
	mc.setBlocks(-1,1,-15,-29,1,-35,2)
	mc.setBlocks(-35,1,-9,-50,1,19,2)
	mc.setBlocks(-35,1,-15,-50,1,-35,2)
	mc.setBlocks(-35,1,25,-50,1,40,2)
	mc.setBlocks(5,1,-15,34,1,-35,2)
	mc.setBlocks(40,1,-15,50,1,-35,2)
	mc.setBlocks(40,1,-9,50,1,19,2)
	mc.setBlocks(40,1,25,50,1,40,2)
	trees()
#Create a park with dry grass
def parkDry():
	mc.setBlocks(-1,1,-9,-29,1,19,24)
	mc.setBlocks(-1,1,-15,-29,1,-35,24)
	mc.setBlocks(-35,1,-9,-50,1,19,24)
	mc.setBlocks(-35,1,-15,-50,1,-35,24)
	mc.setBlocks(-35,1,25,-50,1,40,24)
	mc.setBlocks(5,1,-15,34,1,-35,24)
	mc.setBlocks(40,1,-15,50,1,-35,24)
	mc.setBlocks(40,1,-9,50,1,19,24)
	mc.setBlocks(40,1,25,50,1,40,24)
	trees()
#Create the park trees
def trees():
	tree(-5,-5)
	tree(-5,5)
	tree(-5,15)

#Each tree
def tree(x,z):
	mc.setBlocks(x,2,z,x,5,z,17)
	mc.setBlocks(x-1,6,z-1,x+1,6,z+1,18)
	mc.setBlocks(x-2,7,z-2,x+2,7,z+2,18)
	mc.setBlocks(x-2,8,z-2,x+2,8,z+2,18)
	mc.setBlocks(x-1,9,z-1,x+1,9,z+1,18)

#Snow in the park
def snowPark():
	mc.setBlocks(-1,2,-9,-29,2,19,78)
	mc.setBlocks(-1,2,-15,-29,2,-35,78)
	mc.setBlocks(-35,2,-9,-50,2,19,78)
	mc.setBlocks(-35,2,-15,-50,2,-35,78)
	mc.setBlocks(-35,2,25,-50,2,40,78)
	mc.setBlocks(5,2,-15,34,2,-35,78)
	mc.setBlocks(40,2,-15,50,2,-35,78)
	mc.setBlocks(40,2,-9,50,2,19,78)
	mc.setBlocks(40,2,25,50,2,40,78)
	trees()
#No more snow
def noSnowPark():
	mc.setBlocks(-1,2,-9,-29,2,19,0)
	mc.setBlocks(-1,2,-15,-29,2,-35,0)
	mc.setBlocks(-35,2,-9,-50,2,19,0)
	mc.setBlocks(-35,2,-15,-50,2,-35,0)
	mc.setBlocks(-35,2,25,-50,2,40,0)
	mc.setBlocks(5,2,-15,34,2,-35,0)
	mc.setBlocks(40,2,-15,50,2,-35,0)
	mc.setBlocks(40,2,-9,50,2,19,0)
	mc.setBlocks(40,2,25,50,2,40,0)
	trees()

#Builds a under construction train station
def trainStation():
	mc.setBlocks(5,1,25,34,1,40,5)
	mc.setBlocks(24,1,25,28,1,27,0)
	mc.setBlocks(26,0,25,30,-1,27,0)
	mc.setBlocks(28,-2,25,32,-3,27,0)
	mc.setBlocks(30,-4,25,34,-5,27,0)
	mc.setBlocks(32,-6,25,36,-7,27,0)
	mc.setBlocks(32,-8,25,36,-9,27,0)
	mc.setBlocks(26,-4,28,36,-9,35,0)
	mc.setBlocks(26,-7,28,36,-9,35,35,5)
	mc.setBlocks(28,-8,29,36,-9,33,0)
	mc.setBlocks(34,-8,28,35,-9,29,0)
#Defines the "train"
def train(person):
	if person:
		mc.player.setTilePos(18,2,-18)
#Builds the control panel
def controlPanel (position):
	mc.setBlocks(10,2,28,20,6,40,22)
	mc.setBlocks(11,2,29,19,5,39,0)
	mc.setBlocks(10,2,30,10,5,32,0)
	mc.setBlocks(11,2,28,20,5,28,102)
	mc.setBlocks(11,5,29,19,5,39,51)
	for i in range(0,PISOS):
		if ALARMA[i]:
			mc.setBlock(19,3,30+(2*i),41)
		else:
			mc.setBlock(19,3,30+(2*i),42)
#Shows a welcome control panel message
def msgControlPanel(position, pan):
	if position.x >= 5 and position.x <=23 and position.y >=2 and position.z >= 25 and position.z <= 42 and pan == False:
		mc.postToChat("Welcome to the building control panel")
		pan = True
	if mc.getBlock(position.x,position.y-1,position.z) != 5:
		pan = False
	
	return pan 		
#Shows the instructions for the panel control
def msgAlarmCubes(position,pan):
	if position.x >= 12 and position.x <=18 and position.y >=2 and position.z >= 30 and position.z <= 38 and pan == False:
		mc.postToChat("Hit a cube with the sword to modify the building alarm")
		pan = True
	if mc.getBlock(position.x,position.y-1,position.z) != 5:
		pan = False
	return pan 		

#Reads the hits 
def hitBlock():
	hits = mc.events.pollBlockHits()
	for i in hits:
		for j in range(0,PISOS):
			if i.pos.x == 19 and i.pos.y == 3 and i.pos.z == 30+(2*j):
				mc.postToChat("The alarm in the floor " + str(j) + " is ")
				if ALARMA[j]:
					mc.setBlock(19,3,30+(2*j),42)
					mc.postToChat("Off")
					ALARMA[j] = False
				else:
					ALARMA[j] = True
					mc.setBlock(19,3,30+(2*j),41)
					mc.postToChat("On")
				

if __name__ == '__main__':
	CUBOS = False
	position = mc.player.getTilePos()
	freeBlock()
	#Simulate the GPIO sensors
	lightCent = True
	tempCent = True
	humidityCent = False

	streets()
	park()
	building(PISOS)
	trainStation()
	controlPanel(True)
	while True: 
		position = mc.player.getTilePos()
		puerta(position.z < 21 and position.z > 13)
		train(position.x >28 and position.x < 36 and position.y <= -8 and position.z >29 and position.z < 33)
		#if humidityCent:
		if GPIO.input(4):
			park()
		else:
			parkDry()

		#if tempCent:
		if GPIO.input(18):
			noSnowPark()
		else:
			snowPark()

		if GPIO.input(17):
		#if lightCent:
			luzDeDia(True)
			for i in range (0, PISOS):
				noLuz(i)
		else:
			luzDeDia(False)
			for i in range(0,PISOS):
				crearLuz(i)

		hitBlock()
		PANEL = msgControlPanel(position, PANEL)
		CUBOS = msgAlarmCubes(position, CUBOS)
		#Alarm
		for a in range(0,PISOS):
			if ALARMA[a]:
				if position.x >= 8 and position.x <=31  and position.y >=3+(6*a) and position.y <= 7+(6*a) and position.z >= -6 and position.z <=16:
					#mc.postToChat("Hay una persona en el piso: "+str(a))
					GPIO.output(LEDS[a],GPIO.HIGH)

				else:
					#mc.postToChat("No hay una persona en el piso "+str(a))
					GPIO.output(LEDS[a],GPIO.LOW)
		time.sleep(1)

			
						

