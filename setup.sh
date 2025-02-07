#!/bin/bash

# Mise à jour du système et installation de la bibliothèque libGL.so.1
apt-get update
apt-get install -y libgl1-mesa-glx

# Lancer Gunicorn (assurez-vous que la commande Gunicorn correspond à votre configuration)
gunicorn --bind 0.0.0.0:8000 wsgi:app

