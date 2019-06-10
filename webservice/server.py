#!flask/bin/python
# coding: utf-8

# Librairies:
from flask import Flask, request, jsonify, abort, Response
import cv2, numpy as np

# Reconnaissance d'image:
from classifier import getLabelsFromImage

app = Flask(__name__)

# Détermine les labels des éléments contenus dans une image:
@app.route("/labelImage", methods=['GET'])
def labelImage():
  # Si l'image n'est pas présente:
  if not request.data:
    abort(Response('Error: image absente'))

  labels = getLabels(request.data, tiny_weights = False)

  # Retourne les labels trouvés:
  return jsonify(labels)


# Détermine les labels des éléments contenus dans une image avec weight-tiny:
@app.route("/labelImage_tiny", methods=['GET'])
def labelImage_tiny():
  # Si l'image n'est pas présente:
  if not request.data:
    abort(Response('Error: image absente'))

  labels = getLabels(request.data, tiny_weights = True)

  # Retourne les labels trouvés:
  return jsonify(labels)


# Récupère les labels des éléments d'une image provenant d'une requête:
def getLabels(data, tiny_weights = False):
  # Récupère l'image envoyée:
  image = cv2.imdecode(np.fromstring(data, dtype=np.uint8), cv2.IMREAD_COLOR)

  # Enregistre l'image:
  cv2.imwrite('img.jpg', image)

  # Détermine les labels de l'image:
  labels = getLabelsFromImage('img.jpg', tiny_weights)

  return labels

if __name__ == '__main__':
  app.run(debug=True)