#[== Indéfini ==]
#! /usr/bin/python
# -*- coding:utf-8 -*-

import socket
import sys
import os
from Crypto.Cipher import AES
from Crypto import Random

# Initialisation variables

continuer = 'True'
host = 'localhost'
port = 4444
message_envoyer = ''
message_recus = ''

# Configuration AES

key = 'palsm453lkejru34'
block_size = 16
mode = AES.MODE_CFB
iv = Random.new().read(block_size)
cipher = AES.new(key, mode, iv)

# Fonction upload
  
def upload():
  cmd = os.popen('ls', 'r') # On liste les fichiers dispo sur notre machine
  print (cmd.read()) # On les affiches
  nom = raw_input('nom du fichier: ') # On entre le nom du fichier à uploader avec l'extension
  fichier = open(nom, 'r') # On ouvre le fichier en lecture
  nom = cipher.encrypt(nom) # On crypte le nom du fichier en aes
  c.send(nom) # On envois le nom du fichier au serveur pour qu'il puisse créer le fichier
  data = fichier.read() # On récupère toutes les données du fichier
  data = cipher.encrypt(data) # On crypte les données du fichier en aes
  c.send(data) # On envois les données crypter en aes au serveur pour qu'il puisse recréer le fichier
  message_recus = c.recv(1024) # On récupère le message qui vas nous dire si tous sais bien passer
  messages_recus = cipher.decrypt(message_recus) # on décrypte se message
  if(messages_recus == 'ok'): # Si le message vaut ok c'est que le fichier à bien été uploader par le serveur
    print ("Fichier uploader avec succès")
  else:
    print ("Erreur lors de l'upload du fichier")
   
# Fonction download
   
def download():
  data = c.recv(1024) # On récupère la liste des fichier sur le serveur
  data = cipher.decrypt(data) # On décrypte la liste de fichier
  print (data) # On affiche la liste des fichier présent dans le répertoire
  nom = raw_input('Nom du fichier: ') # On entre le nom du fichier que l'on veut télécharger avec l'extension
  fichier = open(nom, 'w') # On ouvre un fichier en écriture avec le même nom et extension
  nom = cipher.encrypt(nom) # On crypte le nom du fichier
  c.send(nom) # On envois le nom du fichier au serveur pour qu'il sachent sur qu'elle fichier travailler
  data = c.recv(10000) # On récupère les données du fichier que le serveur vient de nous envoyer
  data = cipher.decrypt(data) # On décrypte les données
  fichier.write(data) # On écrit les données pour recréer le fichier
  fichier.close() # On ferme le fichier on a fini de l'écrire
  message_recus = c.recv(1024) # On récupère le message qui vas nous dire si tout sais bien passer
  message_recus = cipher.decrypt(message_recus) # On décrypte le message
  if(message_recus == 'ok'): # Si le message vaut ok c'est que le fichier a été télécharger
    print("fichier télécharger avec succès\n")
  else:
    print("Erreur lors du téléchargement du fichier")

# Liaison tcp/ip

c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connection au serveur

try:
  c.connect((host, port))
except(socket.error):
  print ("Hote injoignable")
  sys.exit()

# échange client serveur

while(continuer == 'True'):
  message_recus = c.recv(1024)
  message_recus = cipher.decrypt(message_recus)
  print(message_recus)
  message_envoyer = input('message: ')
  if(message_envoyer == 'close'):
    message_envoyer = cipher.encrypt(message_envoyer)
    c.send(message_envoyer)
    print ("bye")
    sys.exit()
  elif(message_envoyer == 'upload'): # Si message_envoyer vaut upload
    message_envoyer = cipher.encrypt(message_envoyer) # On encrypte message_envoyer
    c.send(message_envoyer) # On l'envois au serveur pour le mettre au courant que l'on vas uploader un fichier
    upload() # On appel la fonction upload
  elif(message_envoyer == 'download'): # Si message_envoyer vaut download
    message_envoyer = cipher.encrypt(message_envoyer) # On encrypte message_envoyer
    c.send(message_envoyer) # On l'envois au serveur pour le mettre au courant que l'on vas télécharger un fichier
    download() # On appel la fonction download
  else:
    message_envoyer = cipher.encrypt(message_envoyer)
    c.send(message_envoyer)
  
c.close()