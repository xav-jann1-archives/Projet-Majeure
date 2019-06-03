#!/usr/bin/env python
# coding: utf-8
import sys

# Scripts:
from image_recognition import getLabelFromFilename


def main():
  filename = './img.jpg'

  # Si un chemin est donnée en paramètre:
  if len(sys.argv) >= 2: filename = sys.argv[1]

  label = getLabelFromFilename(filename)
  print(label)

if __name__ == "__main__":
  main()
