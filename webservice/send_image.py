#!/usr/bin/env python
# coding: utf-8

import cv2
import httplib
#import http.client as httplib  # Python 3

# Connection au serveur:
conn = httplib.HTTPConnection('127.0.0.1:5000', timeout=50)

# Envoie d'une requête pour récupérer les labels d'une image:
def getLabelsFromImage(img):
  # Si img est le chemin de l'image:
  if type(img) is str:
    # Charge l'image:
    img = cv2.imread(img)

  # Encode l'image pour l'envoyer:
  imencoded = cv2.imencode('.jpg', img)[1]

  # Requête:
  headers = {"Content-type": "test/plain"}
  try:
    conn.request("GET", "/labelImage", imencoded.tostring(), headers)
    response = conn.getresponse()
  except conn.timeout as e:
    print("timeout")

  return response.read()

if __name__ == '__main__':
  # Charge l'image:
  img = cv2.imread('img_banane.jpg')

  # Récupère les labels de l'image:
  labels = getLabelsFromImage(img)
  print(labels)