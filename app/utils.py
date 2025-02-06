import os
from threading import Lock

from deepface import DeepFace
from werkzeug.utils import secure_filename
from langdetect import detect
import pyttsx3
import threading


engine = pyttsx3.init()
lock: Lock = threading.Lock()  # Verrou pour empêcher plusieurs threads d'appeler runAndWait()

# Comparaison des images avec vérifications des chemins

def compare_image(image_file, image_model):
    try:
        # Construire le chemin complet de l'image modèle
        model_image_path = os.path.join('uploads', image_model)

        # Vérifier si le fichier image modèle existe
        if not os.path.exists(model_image_path):
            raise FileNotFoundError(f"Le fichier modèle '{model_image_path}' est introuvable.")

        # Vérifier si le fichier image fourni existe
        if not os.path.exists(image_file):
            raise FileNotFoundError(f"Le fichier temporaire '{image_file}' est introuvable.")

        # Effectuer la comparaison avec DeepFace
        result = DeepFace.verify(image_file, model_image_path, enforce_detection=False)

        if result.get("verified", False):
            print(f"Les deux images correspondent avec une distance de {result['distance']:.4f}.")
        else:
            print(f"Les deux images ne correspondent pas. Distance : {result['distance']:.4f}.")

        return result

    except FileNotFoundError as fnf_error:
        print(f"Erreur de fichier : {fnf_error}")
        return {"error": str(fnf_error)}

    except Exception as e:
        print(f"Une erreur s'est produite : {e}")
        return {"error": str(e)}

# authentification
def save_temp_image(image_file, temp_folder='temp_images'):
    """
    Sauvegarde temporairement l'image dans un dossier et retourne son chemin.
    """
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)

    filename = secure_filename(image_file.filename)
    file_path = os.path.join(temp_folder, filename)
    image_file.save(file_path)

    return file_path

# fin authentification
def save_uploaded_file(upload_folder, file):
    """
    Sauvegarde un fichier téléchargé et renvoie son nom de fichier sécurisé.
    """
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    filename = secure_filename(file.filename)
    file_path = os.path.join(upload_folder, filename)
    file.save(file_path)

    return filename

def summarize_text_simple(text, ratio):
    """
    Résume un texte donné en fonction du ratio.
    """
    # Diviser le texte en phrases, en prenant soin de ne pas laisser de 'vide' à la fin
    sentences = [sentence.strip() for sentence in text.split('.') if sentence.strip()]

    # Calculer le nombre de phrases à conserver en fonction du ratio
    num_sentences = int(len(sentences) * ratio)

    # Si le ratio est trop petit, on garde au moins 1 phrase
    num_sentences = max(1, num_sentences)

    # Retourner les phrases les plus importantes (ici, les premières phrases)
    summary = '. '.join(sentences[:num_sentences])

    # Ajouter un point à la fin si nécessaire
    if summary and not summary.endswith('.'):
        summary += '.'

    return summary

def detect_language(text):
    """
    Détecte la langue du texte.
    :param text: Texte dont la langue doit être détectée.
    :return: Code de la langue détectée (ex : 'en', 'fr').
    """
    try:
        return detect(text)
    except Exception as e:
        print(f"Erreur lors de la détection de la langue : {e}")
        return 'en'  # Langue par défaut

# text to speech


# Variables globales
is_paused = False
is_speaking = False  # Pour suivre l'état de la parole
lock = threading.Lock()  # Verrou pour éviter des conflits lors de l'exécution du moteur

def run_speech(text):
    """
    Fonction pour exécuter la synthèse vocale dans un thread.
    """
    global is_paused
    with lock:
        is_paused = False
        engine.say(text)
        engine.runAndWait()

def text_to_speech(text):
    """
    Fonction pour convertir le texte en parole.
    """
    global speech_thread, is_paused

    if is_paused:
        return "Lecture en pause. Reprenez avant de rejouer un texte."

    if speech_thread and speech_thread.is_alive():
        return "Une lecture est déjà en cours."

    speech_thread = threading.Thread(target=run_speech, args=(text,))
    speech_thread.start()
    return "Lecture démarrée."

def pause_speech():
    """
    Met en pause la synthèse vocale en arrêtant temporairement le moteur.
    """
    global is_paused
    if not is_paused:
        engine.stop()
        is_paused = True
        return "Lecture en pause."
    return "La lecture est déjà en pause."

def resume_speech():
    """
    Reprend la synthèse vocale après une pause.
    """
    global is_paused, speech_thread

    if is_paused:
        is_paused = False
        speech_thread = threading.Thread(target=run_speech, args=("Reprise de la lecture.",))
        speech_thread.start()
        return "Lecture reprise."
    return "Aucune lecture en pause."

def stop_speech():
    """
    Arrête complètement la lecture.
    """
    global is_paused
    engine.stop()
    is_paused = False
    return "Lecture arrêtée."
