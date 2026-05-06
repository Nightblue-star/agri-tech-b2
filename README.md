# 🌾 AgriTech - Plateforme de Pilotage Agricole Moderne

Bienvenue sur **AgriTech**, une solution numérique de pointe conçue pour transformer la gestion quotidienne des exploitations agricoles. Ce projet a été développé avec une vision claire : offrir aux exploitants un véritable "Centre de Commande" professionnel, esthétique et performant.

## 🎯 Objectif du projet ?

Le secteur agricole fait face à des défis croissants (climat, maladies, optimisation des ressources). Ce projet a été créé pour :
- **Centraliser les données** : Regrouper en un seul lieu la météo, l'état des parcelles et les observations terrain.
- **Aider à la décision** : Transformer des données brutes (température, humidité) en indicateurs exploitables (risques de maladies, conseils d'intervention).
- **Professionnaliser l'interface** : Sortir des outils austères pour proposer une expérience utilisateur (UX) haut de gamme, digne des meilleurs outils SaaS modernes.

## 🚀 Ce qui a été réalisé

Le projet se compose d'un écosystème complet, allant du tableau de bord global à la gestion fine des parcelles.

### 1. Tableau de Bord (Dashboard)
- **Indicateurs Clés (KPIs)** : Vue immédiate sur la surface exploitée, le nombre de parcelles actives et les alertes critiques.
- **Visualisation de données** : Graphiques interactifs (pluviométrie et température) générés dynamiquement en JavaScript.
- **Santé des cultures** : Liste priorisée des parcelles avec jauges de santé et statuts en temps réel.

### 2. Gestion des Parcelles
- **Inventaire complet** : Organisation des terres par type de culture (Blé, Maïs, Colza, etc.).
- **Filtrage intelligent** : Système de recherche et de tri par risque ou par culture pour une navigation fluide.
- **Ajout dynamique** : Interface modale pour l'enregistrement de nouvelles parcelles.

### 3. Observations & Alertes
- **Saisie de données** : Formulaire dédié pour enregistrer les conditions relevées sur le terrain.
- **Moteur de risques** : Système capable d'identifier des situations critiques (ex: risque de Mildiou ou stress hydrique) basé sur les seuils d'humidité et de température.

### 4. Météo & Agronomie
- **Prévisions locales** : Tableau prévisionnel à 7 jours.
- **Indicateurs agronomiques** : Suivi de l'évapotranspiration (ETP) et conseils personnalisés pour optimiser les travaux dans les champs.

### 5. Cartographie Interactive
- **Visualisation SVG** : Une carte interactive permettant de visualiser la disposition géographique des terres et d'accéder aux détails de chaque parcelle d'un simple clic.

## 🛠️ Stack Technique

Le projet repose sur des technologies robustes et légères, privilégiant la performance et la clarté du code :

- **Frontend** : 
  - **HTML5 & Vanilla CSS3** : Design system sur mesure (variables CSS, flexbox/grid, animations `fade-up`).
  - **Vanilla JS** : Toute l'interactivité (chartes, filtres, modales) sans dépendances lourdes.
  - **Typographie** : Utilisation des polices *Plus Jakarta Sans* et *Inter* pour un rendu premium.
- **Backend** : 
  - **Python (Flask)** : Serveur API prêt à gérer la persistance des données et les calculs agronomiques complexes.
- **Aesthetics** : Design moderne utilisant le glassmorphism, des dégradés subtils et une iconographie soignée.

## 📂 Structure du Projet

```text
├── index.html          # Tableau de bord principal
├── parcelles.html      # Gestion des terres
├── observations.html   # Saisie des données terrain
├── alertes.html        # Monitoring des risques
├── meteo.html          # Prévisions et indicateurs
├── carte.html          # Visualisation géographique
├── app.py              # Serveur Backend (API)
├── css/
│   └── style.css       # Design System et composants
└── js/
    └── main.js         # Logique interactive
```

## 🏁 Guide de démarrage

### Pour lancer l'interface (Frontend)
Il suffit d'ouvrir le fichier `index.html` dans n'importe quel navigateur moderne. 
Pour une expérience optimale (gestion des chemins relatifs), vous pouvez lancer un serveur local :
```bash
# Avec Python
python -m http.server 8000
```
Puis accédez à `http://localhost:8000`.

### Pour lancer l'API (Backend)
Le serveur est basé sur Flask. Pour le démarrer :
1. Assurez-vous d'avoir Python installé.
2. Installez Flask si nécessaire : `pip install flask flask-cors`
3. Lancez le serveur : `python app.py`

Le serveur sera accessible sur `http://localhost:5000`.

---
*Développé avec passion pour une agriculture connectée et performante.*
