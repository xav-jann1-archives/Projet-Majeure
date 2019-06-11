# PROJET MAJEURE

Simulation d'un robot Pepper pour **reconnaître, récupérer et placer des objets** à l'endroit demandé par un utilisateur à partir d'une *Interface Homme Robot*.


## AUTEURS :
- Estelle Briand
- Xavier Jannin
- Paul Martinez
- Jean-Baptiste Porret
 

## YOUTUBE :
 - [Vidéo]()
 
## GITHUB :
 - [Projet-Majeure](https://github.com/xav-jann1/Projet-Majeure)
 
## SOURCES :
 - [Sujet](https://github.com/cpe-majeure-robotique/S8-Simulated-Pepper-Project/wiki)
 - [Documentation NAOqi APIs](http://doc.aldebaran.com/2-5/naoqi/index.html)
 - [Algorithmia](https://algorithmia.com/)
 - [Darknet/yolo](https://pjreddie.com/darknet/yolo/)
 - [Flask](http://flask.pocoo.org/)
 - Exécution d'une commande du terminal depuis un programme Python : [Stack Overflow: Running shell command and capturing the output](https://stackoverflow.com/questions/4760215/running-shell-command-and-capturing-the-output)
 - [Turbosquid](https://www.turbosquid.com/)


## Projet initial commun :
- **Done :**
	- Génération du monde avec des tables
	- Placement aléatoire de trois objets sur une table
	- IHM sur un navigateur web, pour récupérer la commande de l'utilisateur
	- Déplacement de Pepper pour se placer devant les objets et la table demandé par l'utilisateur
 	- Mouvement de Pepper pour récupérer des objets grâce à sa main et son bras
 	- Prend en photo un seul objet, et le reconnaît grâce au webservice *Algorithmia*

- **TODO :**
 	- Prendre une image des trois objets en même temps, pour exécuter la reconnaissance une seule fois

- **Bugs :**
 	- Plus il y a des déplacements, plus la saisie d'un objet est incertain

 
## BONUS :

- **Numéro 4 :** Create a beautiful world, with an enhanced scenario, and an enhanced HRI

	- **Done :**
		- Création et recherche des models 3D pour notre environnement grâce à Blender 
		- Intégration de murs, toit et un paysage ainsi que tous le mobiliers liés au thème "plage" après avoir créer des fichiers `.urdf`
		- Utlisation de Bootstrap et d'un CSS pour l'IHR
		- Les images et les models utilisés dans l'IHR sont tous libre de droits, généralement pris sur des banques d'images gratuites
		- Le scénario se déroule dans un restaurant au bord de mer. Le client commande son plat (pizza), sa boisson (vin) ou son dessert (banane) sur la tablette et indique sa table. Le robot peut alors aller chercher la commande sur le comptoir pour l'apporter à la bonne table.

	- **TODO :**
		- Amelioration de la performance du programme lors de l'ajout complet de la scène

	- **Bugs :**
		- L'ajout d'éléments ralentit le système et diminue le framerate, ce qui rend la simulation moins précise et génère plus souvent des erreurs sur le placement du Pepper pour saisir l'objet


- **Numéro 5 :** Replace Algoritmia by your own webservice server
	- **Done :**
		- Webservice, fonctionnant sous *Flask*, pour déterminer les objets présent sur une image
		- La reconnaissance est réalisé grâce à *Darknet/YOLO*.
		- Renvoie un JSON avec une liste des objets reconnus, ainsi que la probabilité de certitude de la reconnaissance
		- Possibilité d'exécuter deux modèles de reconnaissance différents: `yolov3-tiny.weights` est beaucoup plus rapide (5s < 40s), mais moins efficace que `yolov3.weights`

	- **TODO :**
		- Localiser les objets sur l'image, et renvoyer leur position dans la réponse

	- **Bugs :**
		- Pas vraiment un bug, mais le temps d'exécution pour la reconnaissance dure au moins 40 secondes !!!


---
## ABORESCENCE DES FICHIERS
- README.md : Ce fichier

- [Rendu_Codes] :
	- main.py : programme lançant la simulation *qibullet*
	- [application]
		- app.py
		- dialog.top
		- [html]
			- index.html
			- ...
	- [webservice]:
		- classifier.py
		- server.py
	- [objets]: modèles 3D
		- [objet]
		- objet.urdf
		- ...	

- [Présentation] : 
	- presentation.pptx

---
##  PROCEDURE D'INSTALLATION

### Téléchargement de l'archive :

L'ensemble des programmes utilisés pour ce projet se trouve sur GitHub:
`$ git clone https://github.com/xav-jann1/Projet-Majeure`


### Installation de la tablette :

Déplacer le dossier `application` de l'archive dans le dossier `/home/tp/softbankRobotics/naoqi-tablet-simulator/apps`.

*Note: `naoqi-tablet-simulator` est considéré comme déjà installé dans le dossier `/home/tp/softbankRobotics`*

### Installation du serveur :

Pour permettre le bon fonctionnement du serveur, **Flask** et **Darknet/YOLO** doivent être installé sur le système:

**Flask**: `$ pip install Flask`

Reconnaissance d'image avec **Darknet/YOLO** :
- Télécharger sur le bureau (`~/Bureau`) l'archive : `$ git clone https://github.com/pjreddie/darknet`

- Entrer dans le dossier et compiler le programme de reconnaissance:
	- `$ cd darknet`
	- `$ make`

- Télécharger les modèles déjà entraînés :
	- `yolov3.weights` : `$ wget https://pjreddie.com/media/files/yolov3.weights`
	- `yolov3-tiny.weights` : `$ wget https://pjreddie.com/media/files/yolov3-tiny.weights`

*Notes :*
- les fichiers `yolov3.weights` et `yolov3-tiny.weights` doivent se trouver dans le dossier `darknet`
- le dossier `darknet` peut se trouver n'importe où dans le système, il suffit d'adapter le chemin de la variable `darknet_dir` dans le fichier `webservice/classifier.py`
- la reconnaissance est d'abord réalisée avec le modèle plus petit `yolov3-tiny.weights` (~5 secondes de temps de calcul). Puis, s'il n'y a aucun résultat, la reconnaissance est exécutée avec le modèle classique `yolov3.weights` (~40 secondes)

---
## PROCEDURE DE MISE EN ROUTE

### Mise en route de la Web tablette :

Ouvrir au total 4 terminaux: (*avec `terminator`*)
- Pour lancer `$ naoqi-bin`
- Pour lancer la simulation tablette : `cd softbankRobotics/naoqi-tablet-simulator`
- Pour lancer l'application web : `cd softbankRobotics/naoqi-tablet-simulator/apps/repertoireapplication` puis `python app.py`
- Pour lancer choregraphe: `$ choregraphe_launcher`

**Ordre de lancement :**
	1 -`$ naoqi-bin`
	2 - Ouvrir une fenêtre web à l'adresse `file:///home/tp/softbankRobotics/naoqi-tablet-simulator/web/page.html`
	3 - Lancer `$ ./launcher.sh` (dans `softbankRobotics/naoqi-tablet-simulator`)
	4 - Rafraîchir la page
	5 - Lancer l'application `$ python app.py`


### Mise en route du serveur :
*(pour utiliser darknet/YOLO pour la reconnaissance d'objet)*

Lancer le programme python `webservice/server.py`:
`$ python webservice/server.py`


### Mise en route de l'application :

Si *Algorithmia* doit être utilisé pour la reconnaissance, vérifier que `useAlgorithmia = True` dans le fichier `main.py`.

Si *darknet/YOLO* doit être utilisé pour la reconnnaissance, c'est-à-dire le serveur fonctionne, vérifier que `useAlgorithmia = False` dans le fichier `main.py`.

Quand tout est en fonctionnement, lancer le programme python `main.py`:
`$ python main.py`

