#!flask/bin/python
# coding: utf-8

# Librairies:
from flask import Flask, request, jsonify, abort, Response
import cv2, numpy as np

# Reconnaissance d'image:
#from classifier import getLabelsFromImage

app = Flask(__name__)

@app.route("/labelImage", methods=['GET'])

# Détermine les labels des éléments contenus dans une image:
def labelImage():
  # Si l'image n'est pas présente:
  if not request.data:
    abort(Response('Error: image absente'))

  # Récupère l'image envoyée:
  data = request.data
  image = cv2.imdecode(np.fromstring(data, dtype=np.uint8), cv2.IMREAD_COLOR)

  # Enregistre l'image:
  cv2.imwrite('img.jpg', image)

  # Détermine les labels de l'image:
  #labels = getLabelsFromImage('img.jpg')
  labels = [{'a': 2, 'b': 3}, {'c':4}]

  # Retourne les labels trouvés:
  return jsonify(labels)


if __name__ == '__main__':
  app.run(debug=True)