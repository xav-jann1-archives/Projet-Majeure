#!/usr/bin/env python
# coding: utf-8

import cv2, random
import time
import pybullet
import pybullet_data
from qibullet import SimulationManager
from qibullet import PepperVirtual

# Scripts:
from image_recognition import getLabelFromImage


objects = [
	{ "name": "objet/table.urdf", "basePosition": [1, 1, 0], "globalScaling": 0.5 },
	{ "name": "objet/diningTable.urdf", "basePosition": [-2, 1, 0], "globalScaling": 0.5 },
]

# Liste des totems:
totems = [
  { "name": "objet/totem.urdf", "basePosition": [0.5, 1, 0.8], "globalScaling": 0.8 },
	{ "name": "objet/totem_banane.urdf",  "basePosition": [1, 1, 0.8], "globalScaling": 0.8 },
  { "name": "objet/totem_bouteille.urdf",  "basePosition": [1.5, 1, 0.8], "globalScaling": 0.8 }
  
]

# Liste des positions des totems:
totems_places = [
  [0.5, 1, 0.8], [1, 1, 0.8], [1.5, 1, 0.8]
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
  
  # Déplacement de Pepper:
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
    



def deplacement(pepper):
  pepper.goToPosture("Crouch", 0.6)
  time.sleep(2)
  pepper.goToPosture("Stand", 0.6)
  time.sleep(2)
  #pepper.goToPosture("StandZero", 0.6)
  #time.sleep(2)

  # Move to the specified [x, y, theta] coordinates in the robot frame, 
  # synchronous call
  pepper.moveTo(0.5, 0.0, 3.1415/2.0, frame=PepperVirtual.FRAME_ROBOT, speed = 10000.0)
  #time.sleep(5)
  #pepper.moveTo(0.4, 0.0, 0.0, frame=PepperVirtual.FRAME_ROBOT, speed = 10000.0)


if __name__ == "__main__":
  main()
