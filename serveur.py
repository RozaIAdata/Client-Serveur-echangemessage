
#! /usr/bin/python3
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
  nom = conn.recv(1024) # On récupère le nom du fichier que le client veut uploader
  nom = cipher.decrypt(nom) # On décrypte le nom
  fichier = open(nom, 'w') # On ouvre un fichier en écriture qui a le même nom et extension
  data = conn.recv(1024) # On récupère les données du fichier client
  data = cipher.decrypt(data) # On décrypte les données
  fichier.write(data) # On écrit notre fichier avec les données reçues par le client
  fichier.close() # On ferme notre fichier
  message_envoyer = 'ok' # On envois un message ok qui avertis le client que tout sais bien passer
  message_envoyer = cipher.encrypt(message_envoyer) # On crypte le message
  conn.send(message_envoyer) # On envois le message

# Fonction download
  
def download():
  cmd = os.popen('ls', 'r') # On ouvre la commande ls pour lister les fichier dans le répertoire courant du serveur
  data = cmd.read() # On récupère la liste des fichiers
  data = cipher.encrypt(data) # On crypte la liste
  conn.send(data) # On l'envois au client
  nom = conn.recv(1024) # On récupère le nom du fichier que le client veut télécharger
  nom = cipher.decrypt(nom) # On décrypte le nom du fichier
  fichier = open(nom, 'r') # On ouvre un fichier un lecture
  data = fichier.read() # On récupère les données de ce fichier
  data = cipher.encrypt(data) # On les cryptes
  conn.send(data) # Et on les envois au client pour qu'il puisse reconstruire le fichier
  fichier.close() # On ferme le fichier on a fini les traitements
  message_envoyer = 'ok' # On envois le message ok pour dire que tout sais bien passer de notre coter
  message_envoyer = cipher.encrypt(message_envoyer) # On crypte le message
  conn.send(message_envoyer) # On l'envois

# Liaison tcp/ip

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Liaison adresse/port

try:
  s.bind((host, port))
except(socket.error):
  print("port déja utiliser")
  sys.exit()

# Serveur en écoute

s.listen(5)
print("Serveur en attente de client \n")
conn, addr = s.accept()
print("Client connecter \n")

# Boucle échange client serveur

while(continuer == 'True'):
  message_envoyer = "Serveur 1.0"
  message_envoyer = cipher.encrypt(message_envoyer)
  conn.send(message_envoyer)
  message_recus = conn.recv(1024)
  message_recus = cipher.decrypt(message_recus)
  if(message_recus == 'close'):
    print("bye")
    sys.exit()
  elif(message_recus == 'upload'): # Si message_recu vaut upload
    upload() # On appel la fonction upload
  elif(message_recus == 'download'): # si message_recu vaut download
    download() # On appel la fonction download
  else:
    print(message_recus)
  
conn.close()
s.close()
