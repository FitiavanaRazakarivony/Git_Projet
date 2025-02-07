    import os
    from dotenv import load_dotenv
    import mysql.connector

    # Charger les variables d'environnement à partir du fichier .env
    if not load_dotenv():
        print("⚠️ Attention : Le fichier .env est introuvable ou non chargé !")

    class Config:
        """
        Configuration générale de l'application.
        """
        # Configuration de la base de données
        MYSQLHOST = os.getenv("MYSQLHOST", "localhost")
        MYSQLUSER = os.getenv("MYSQLUSER", "root")
        MYSQLPASSWORD = os.getenv("MYSQLPASSWORD", "")
        MYSQLDATABASE = os.getenv("MYSQLDATABASE", "facial_auth")

        SQLALCHEMY_DATABASE_URI = os.getenv(
            'DATABASE_URL',
            f"mysql+mysqlconnector://{MYSQLUSER}:{MYSQLPASSWORD}@{MYSQLHOST}/{MYSQLDATABASE}"
        )
        SQLALCHEMY_TRACK_MODIFICATIONS = False

        # Configuration du dossier de téléchargement
        UPLOAD_FOLDER = 'uploads'

        # Clés secrètes
        SECRET_KEY = os.getenv('SECRET_KEY', 'votre_clé_secrète')
        JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'votre_clé_jwt_secrète')

    # Vérifier si toutes les variables sont bien chargées
    if not all([Config.MYSQLHOST, Config.MYSQLUSER, Config.MYSQLDATABASE]):
        raise ValueError("⚠️ Erreur : Vérifie tes variables d'environnement !")

    try:
        # Connexion à MySQL
        db = mysql.connector.connect(
            host=Config.MYSQLHOST,
            user=Config.MYSQLUSER,
            password=Config.MYSQLPASSWORD,
            database=Config.MYSQLDATABASE
        )

        # Vérifier la connexion
        if db.is_connected():
            print("✅ Connexion réussie à MySQL")

        # Exécuter une requête
        cursor = db.cursor()
        cursor.execute("SHOW TABLES")

        print("📋 Tables dans la base de données :")
        for table in cursor.fetchall():
            print(table[0])

    except mysql.connector.Error as e:
        print(f"❌ Erreur MySQL : {e}")

    finally:
        if 'db' in locals() and db.is_connected():
            cursor.close()
            db.close()
            print("🔌 Connexion fermée")


