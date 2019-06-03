#!/usr/bin/env python
# coding: utf-8

import cv2
import Algorithmia
from Algorithmia.acl import ReadAcl, AclType

# API Key:
apiKey = "simkOxovpKv0vV4YIAcMcrwpjq+1"

# Chemin du fichier:
imageInput = "data://jbporret/nlp_directory/img.jpg"


# Create the Algorithmia client:
client = Algorithmia.client(apiKey)

# Set your Data URI:
nlp_directory = client.dir("data://jbporret/nlp_directory")
# Create your data collection if it does not exist
if nlp_directory.exists() is False:
    nlp_directory.create()

# Create the acl object and check if it's the .my_algos default setting:
acl = nlp_directory.get_permissions()  # Acl object
acl.read_acl == AclType.my_algos  # True

# Update permissions to private:
nlp_directory.update_permissions(ReadAcl.private)
nlp_directory.get_permissions().read_acl == AclType.private # True


# Détermine le label d'une image:
# @param img {~cv2.img}: image de la caméra du Pepper
# @return label {string}
def getLabelFromImage(img):
	# Sauvegarde l'image:	
	cv2.imwrite('img.jpg', img)

	# Upload local file
	client.file(imageInput).putFile('./img.jpg')

	input = {
	  "image": imageInput,
	  "output": "data://.algo/deeplearning/ObjectDetectionCOCO/temp/imgOut.jpg",
	  "min_score": 0.1,
	  "model": "ssd_mobilenet_v1"
	}

	# Create the algorithm object using the Summarizer algorithm
	# Pass in input required by algorithm
	algo = client.algo('deeplearning/ObjectDetectionCOCO/0.2.1')
	
	# Récupère les labels de l'image:
	result = algo.pipe(input).result
	print(result)	
	result = result['boxes']
	
	# Si un label est trouvé:
	if len(result) > 0:
		return result[0]['label']

	return 'null'

