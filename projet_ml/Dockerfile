# Utiliser une image de base avec Python préinstallé
FROM python:3.9-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers de l'application dans le conteneur
COPY . /app

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port sur lequel Flask sera disponible
EXPOSE 5000

# Commande pour lancer l'application
CMD ["python", "test.py"]
