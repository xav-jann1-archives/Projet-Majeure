import qi
import argparse
import time


#""" Communication Tablette """#

class return_object():
  """
  A simple class to react to face detection events.
  """

  def __init__(self, session):
      """
      Initialisation of qi framework and event detection.
      """
      self.memory = session.service("ALMemory")
      # Connect the event callback.
      self.subscriber = self.memory.subscriber("fincommande")
      self.subscriber.signal.connect(self.mycallback)
      # Variables utiles
      self.table = None
      self.object = None
      self.wait = True	

#Callback for event fincommande.
  def mycallback(self, value):
      print("callback")
      self.object=self.memory.getData("objet")
      self.table=self.memory.getData("table")	
      self.wait = False

  # Lance une boucle le temps que l'utilisateur termine de passer sa commande:
  def run(self):
      while self.wait:
        time.sleep(1)
          

      

def wait_command():
  # Creation de la session connecter au robot pepper par naoqi
  session = qi.Session()
  parser = argparse.ArgumentParser()
  parser.add_argument("--ip", type=str, default="127.0.0.1",
                help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
  parser.add_argument("--port", type=int, default=9559,
                help="Naoqi port number")

  args = parser.parse_args()

  try:
    session.connect("tcp://" + args.ip + ":" + str(args.port))

  except RuntimeError:
    print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n")

  # Creation de l'objet de classe "return_objet"
  commande = return_object(session)
  commande.run()
  return(commande.object, int(commande.table))   

if __name__ == "__main__":
    [objet, table] = tablette()
    print(objet,table)