#!/usr/bin/env python
# coding: utf-8

# Librairies:
import pybullet, pybullet_data
from qibullet import SimulationManager
from qibullet import PepperVirtual
import cv2, random, time, numpy as np

# Scripts:
from image_recognition import getLabelFromImage
from send_image import getLabelsFromImage_darknet

# Liste des objets composant le décor:
objects = [
  { "name": "objet/table.urdf", "basePosition": [1, 1, 0], "globalScaling": 0.5 },
  { "name": "objet/diningTable.urdf", "basePosition": [-2, 0.8, -0.1], "globalScaling": 0.5 },
  { "name": "objet/diningTable.urdf", "basePosition": [4, 0.8, -0.1], "globalScaling": 0.5 }
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
  print('Initialisation')
  simulation_manager = SimulationManager()
  client = simulation_manager.launchSimulation(gui = True)
  pepper = simulation_manager.spawnPepper(client) #, spawn_ground_plane = True)
  
  # Charge les objets:
  print('Ajout des éléments du monde')
  placeObjectsInWorld(client, objects)

  # Charge les totems:
  print('Ajout des totems')
  placeRandomlyObjects(client, totems, totems_places)

  # Initialise la position du Pepper:
  init_move(pepper)

  # Attend la commande:
  # [objet, table] = ...
  [objet, table] = ['banana', 1]
  
  # Déplacement de Pepper pour récupérer l'objet demandé:
  delta_pos = moveToObject(pepper, objet)

  # Prend l'objet en face de Pepper:
  takeObject(pepper)

  # Amène l'objet à la table:
  moveToTable(pepper, table, delta_pos)

  # Dépose l'objet sur la table:
  putObjectOnTable(pepper)


  while True:
    time.sleep(10)



""" World """

# Ajoute des objets dans le monde:
def placeObjectsInWorld(client, objects):
  for objet in objects:
    pybullet.loadURDF(objet["name"], basePosition = objet["basePosition"], globalScaling = objet["globalScaling"], physicsClientId = client)

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

  
""" Déplacement """

# Déplacement de Pepper pour récupérer et placer un objet:
def init_move(pepper):
  pepper.goToPosture("Crouch", 0.6)
  time.sleep(0.5)
  pepper.goToPosture("Stand", 0.6)
  time.sleep(0.5)


# Déplace Pepper devant l'objet demandé:
def moveToObject(pepper, objet_label):
  # S'oriente vers le premier objet;
  pepper.moveTo(0, 0, 3.1415/2.0, frame=PepperVirtual.FRAME_ROBOT, speed = 10000.0)

  # Active la caméra:
  pepper.subscribeCamera(PepperVirtual.ID_CAMERA_TOP)

  i = 0
  img_label = ''
  print("A la recherche de l'objet: '%s'" % objet_label)

  # Passe devant chaque objet jusqu'à ce que les labels correspondent:
  while objet_label != img_label:

    # Si l'objet n'est pas trouvé: recommence depuis le début
    if i == 3:
      i = 0
      pepper.moveTo(0, 1.5, 0, frame=PepperVirtual.FRAME_ROBOT, speed = 10000.0)
    i += 1

    # Déplace Pepper devant l'objet suivant:
    pepper.moveTo(0, -0.5, 0, frame=PepperVirtual.FRAME_ROBOT, speed = 10000.0)
    
    # Récupère l'objet du label devant Pepper:
    img_label = getLabelFromObject(pepper)
    print(img_label)
  
  print("Trouvé !!!")
  print("  '%s' à la place %d" %  (objet_label, i))

  # Position de correction pour les déplacement:
  delta_pos = i * 0.5

  # Désactive la caméra:
  pepper.unsubscribeCamera(PepperVirtual.ID_CAMERA_TOP)

  # Aligne le bras avec l'objet:
  pepper.moveTo(0.3, -0.125, 0, frame=PepperVirtual.FRAME_ROBOT, speed = 10000.0)

  return delta_pos


# Prend l'objet en face de Pepper:
def takeObject(pepper):
  # Place le bras devant l'objet:
  pepper.setAngles('LShoulderPitch',0.5 ,1)
  pepper.setAngles('LHand',1.57,1)

  # S'approche un peu de l'objet:
  pepper.moveTo(0.2, 0, 0, frame=PepperVirtual.FRAME_ROBOT, speed = 10)
  time.sleep(0.5)

  # Ferme la main:
  pepper.setAngles('LHand',0,0.2)


# Déplace Pepper devant la bonne table:
def moveToTable(pepper, table, delta_pos):
  # Recule de la table:
  pepper.moveTo(-1, 0 , 0, frame=PepperVirtual.FRAME_ROBOT, speed = 100)

  if table == 1:
    pepper.moveTo(0, 0, 3.1415/2.0, frame=PepperVirtual.FRAME_ROBOT, speed = 10000.0)
    pepper.moveTo(2.0 + delta_pos, 0, 0, frame=PepperVirtual.FRAME_ROBOT, speed = 100)
    pepper.moveTo(0, 0, -3.1415/2.0, frame=PepperVirtual.FRAME_ROBOT, speed = 100)
  
  elif table == 2:
    pepper.moveTo(0, 0, -3.1415/2.0, frame=PepperVirtual.FRAME_ROBOT, speed = 10000.0)
    pepper.moveTo(3.8 - delta_pos, 0, 0, frame=PepperVirtual.FRAME_ROBOT, speed = 10000.0)
    pepper.moveTo(0, 0, 3.1415/2.0, frame=PepperVirtual.FRAME_ROBOT, speed = 10000.0)  
  
  pepper.moveTo(0.35, 0, 0, frame=PepperVirtual.FRAME_ROBOT, speed = 10000.0)
  
  time.sleep(1)


# Dépose l'objet sur la table:
def putObjectOnTable(pepper):
  # Ouvre la main:
  pepper.setAngles('LShoulderPitch', 0.7,1)
  pepper.setAngles('LHand', 1, 1)
  time.sleep(1)
  pepper.setAngles('LShoulderRoll', 0.3, 1)
  time.sleep(1)
  pepper.moveTo(-0.35, 0, 0, frame=PepperVirtual.FRAME_ROBOT, speed = 100.0)


""" Reconnaissance d'image """

# Détermine le label de l'objet devant Pepper:
def getLabelFromObject(pepper):
  # Se place un peu mieux pour prendre la photo:
  pepper.setAngles('HipPitch', -0.4, 1)

  # Récupère l'image capturé par Pepper:
  img = pepper.getCameraFrame()
  #cv2.imshow("bottom camera", img)

  # Détermine le label de l'objet contenu dans l'image:
  print("Recherche du label...")
  #label = getLabelFromImage(img)   # Algorithmia
  label = getLabelsFromImage_darknet(img)[0]['label']  # darknet/yolo
  #print(getLabelsFromImage_darknet(img)[0])
  #label = 'banana'

  # Repositionnement d'origine:
  pepper.setAngles('HipPitch', 0, 1)
  
  print("Objet: %s" % label)

  return label


if __name__ == "__main__":
  main()
