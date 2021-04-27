# Projet Oracle Sportif Web

### Technologies utilisées

- Framework Python : **Flask**
- Base de données : **SQL Server (Azure)**
- Hébergement/Déploiement : **Azure**

### Running de l'application Web en local

- Télécharger le projet en local, puis se placer à la racine du projet
- Création d'un "virtual environment"
```
python3 -m venv venv
# Si python3 non reconnu, essayer avec 'python'
```
- On rentre dans l'environnement virtuel
```
#  Sur Unix et MacOS
source venv/bin/activate

# Sur Windows
venv\Scripts\activate.bat
```
- Mise à jour pip
```
pip install --upgrade pip
```
- Installation des dépendances (dans le virtual env)
```
pip install -r requirements.txt
```
- Variables globales
```
#  Sur Unix et MacOS
export FLASK_APP=projectapp.py
export FLASK_ENV=development

# Sur Windows
set FLASK_APP=projectapp.py
set FLASK_ENV=development
```
- Running du projet
```
flask run
```
NB : kill le serveur + sortir de l'environnement virtuel 
```
$ 'CTRL C'

$ deactivate
```
