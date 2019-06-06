#!/usr/bin/env python
# coding: utf-8

import os, subprocess

darknet_dir = '/home/tp/Bureau/darknet'
working_dir = os.getcwd()

#argv = ['./darknet', 'detect', 'cfg/yolov3.cfg', 'yolov3.weights', 'data/dog.jpg']
#argv = ['./darknet', 'detect', 'cfg/yolov3.cfg', 'yolov3.weights', '/home/tp/Bureau/Projet-Majeure/webservice/img.2.jpg']


def getLabelsFromImage(filename):
  # Correction du chemin:
  if filename[0] != '/':
    filename = working_dir + '/' + filename

  argv = ['./darknet', 'detect', 'cfg/yolov3.cfg', 'yolov3.weights', filename]

  # Exécute le programme de reconnaissance:
  result = subprocess.check_output(argv, cwd=darknet_dir)
  #result = subprocess.call(argv, stdout=subprocess.PIPE, cwd=darknet_dir)  # Python 3
  print(result)

  # Conversion: 'bytes' -> 'str'
  #result = result.stdout.decode('utf-8')  # Python 3

  # Décompose en ligne la réponse:
  lines = result.split('\n')

  # Récupère les labels et les probabilités trouvées:
  labels = list()
  for i in range(1, len(lines) - 1):
    [label, prob] = lines[i].split(': ')  # !: prob = '99%'
    labels.append({ 'label': label, 'prob': int(prob[:-1])})

  return labels


if __name__ == '__main__':
  labels = getLabelsFromImage('img.2.jpg')
  print(labels)