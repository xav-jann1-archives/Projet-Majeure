#!/usr/bin/env python
# coding: utf-8

# Scripts:
from image_recognition import getLabelFromFilename



def main():
  filename = './img.jpg'
  label = getLabelFromFilename(filename)
  print(label)

if __name__ == "__main__":
  main()
