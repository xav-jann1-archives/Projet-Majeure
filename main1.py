#!/usr/bin/env python
# coding: utf-8

# Librairies:
import pybullet, pybullet_data
from qibullet import SimulationManager
from qibullet import PepperVirtual
import cv2, random, time, numpy as np

# Scripts:
from image_recognition import getLabelFromImage

# Liste des objets composant le décor:
objects = [
  { "name": "objet/sol.urdf", "basePosition": [0, 0, 0], "globalScaling": 0.5 },
  { "name": "objet/table.urdf", "basePosition": [1, 1, 0], "globalScaling": 0.5 },
  { "name": "objet/diningTable.urdf", "basePosition": [-2, 0.8, -0.1], "globalScaling": 0.5 },
  { "name": "objet/diningTable.urdf", "basePosition": [4, 0.8, -0.1], "globalScaling": 0.5 },
  { "name": "objet/mur.urdf", "basePosition": [-3, 4, 0], "globalScaling": 0.5 },
   { "name": "objet/roof.urdf", "basePosition": [-1, 0, 2], "globalScaling": 0.5 }
]

# Liste des totems:
totems = [
  { "name": "objet/totem_pizza.urdf", "basePosition": [0.5, 1, 0.8], "globalScaling": 0.8 },
  { "name": "objet/totem_banane.urdf",  "basePosition": [1, 1, 0.8], "globalScaling": 0.8 },
  { "name": "objet/totem_bouteille.urdf",  "basePosition": [1.5, 1, 0.8], "globalScaling": 0.8 }
  
]

# Liste des positions des totems:
totems_places = [
  [0.5, 0.8, 0.8], [1, 0.8, 0.8], [1.5, 0.8, 0.8]
]


def main():
  # qibullet:
  simulation_manager = SimulationManager()
  client = simulation_manager.launchSimulation(gui = True)
  pepper = simulation_manager.spawnPepper(client) #, spawn_ground_plane = True)
  
  # Charge les objets:
  for objet in objects:
    pybullet.loadURDF(objet["name"], basePosition = objet["basePosition"], globalScaling = objet["globalScaling"], physicsClientId = client)

  # Charge les totems:
  placeRandomlyObjects(client, totems, totems_places)
  
  # Déplacement de Pepper pour récupérer un objet:
  deplacement(pepper)

  # Active la caméra:
  pepper.subscribeCamera(PepperVirtual.ID_CAMERA_TOP) #ID_CAMERA_BOTTOM)

  while True:
    img = pepper.getCameraFrame()
    cv2.imshow("bottom camera", img)

    label = getLabelFromImage(img)
    print(label)
    time.sleep(10);

    cv2.waitKey(1)

# Place aléatoirement des objets:
def placeRandomlyObjects(client, objects, places):
  if len(objects) > len(places):
    print("Error 'placeRandomlyObjects': il y a plus de places que d'objets")
    return
  
  # Mélange les objets:
  random.shuffle(objects)
  
  # Ajoute autant d'objets que de positions:
  for i in range(len(places)):
    objet = objects[i]
    pybullet.loadURDF(objet["name"], basePosition = places[i], globalScaling = objet["globalScaling"], physicsClientId = client)
    

# Déplacement de Pepper pour récupérer et placer un objet:
def deplacement(pepper):
  pepper.goToPosture("Crouch", 0.6)
  time.sleep(0.5)
  pepper.goToPosture("Stand", 0.6)
  time.sleep(0.5)
  PriseObjet(0, pepper,1)
  PoseTable(0, pepper, 1)


# Prend un objet avec sa main gauche:
def PriseObjet(pos,pepper,table):
  pepper.moveTo(0.625 + pos, 0.3 , 3.1415/2.0, frame=PepperVirtual.FRAME_ROBOT, speed = 10000.0)
  pepper.setAngles('LShoulderPitch',0.5 ,1)
  pepper.setAngles('LHand',1.57,1)
  pepper.moveTo(0.2, 0, 0, frame=PepperVirtual.FRAME_ROBOT, speed = 10)
  time.sleep(0.5)
  pepper.setAngles('LHand',0,0.2)
  

# Repose l'objet sur la table:
def PoseTable(pos,pepper,table):
  pepper.moveTo(-1, 0 , 0, frame=PepperVirtual.FRAME_ROBOT, speed = 100)
  
  if(table == 1):
    pepper.moveTo(0, 0 , 3.1415/2.0, frame=PepperVirtual.FRAME_ROBOT, speed = 100) 
    pepper.moveTo(pos+2.7,0 , 0, frame=PepperVirtual.FRAME_ROBOT, speed = 100)
    pepper.moveTo(0, 0 , -3.1415/2.0, frame=PepperVirtual.FRAME_ROBOT, speed = 100)
    pepper.moveTo(0.25, 0 , 0, frame=PepperVirtual.FRAME_ROBOT, speed = 100)
    time.sleep(1)
    pepper.setAngles('LShoulderPitch',0.7 ,1)
    pepper.setAngles('LHand',1.57,0.1) 
  
  elif (table == 2):
    pepper.moveTo(0,0, -3.1415/2.0, frame=PepperVirtual.FRAME_ROBOT, speed = 10000.0) 
    pepper.moveTo(3.2-pos,0, 0, frame=PepperVirtual.FRAME_ROBOT, speed = 10000.0)
    pepper.moveTo(0, 0 , 3.1415/2.0, frame=PepperVirtual.FRAME_ROBOT, speed = 10000.0)  
    pepper.moveTo(0.35, 0 , 0, frame=PepperVirtual.FRAME_ROBOT, speed = 10000.0)
    pepper.setAngles('LShoulderPitch',0.7 ,1)
    pepper.setAngles('LHand',1.57,1) 


if __name__ == "__main__":
  main()
