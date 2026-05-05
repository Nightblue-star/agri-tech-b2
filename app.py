from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

parcelles = []
observations = []
utilisateurs = [
    {"email": "test@agritech.fr", "password": "password123", "nom": "Jean Cultivateur"}
]

@app.route('/')
def accueil():
    return jsonify({"message": "Bienvenue sur l'API Agri-Tech du projet d'etudes"})


@app.route('/api/parcelles', methods=['GET', 'POST'])
def gerer_parcelles():
    if request.method == 'POST':
        data = request.json or {}
        if not data.get('id') or not data.get('nom') or not data.get('culture'):
            return jsonify({"erreur": "Les champs 'id', 'nom' et 'culture' sont obligatoires"}), 400
        
        
        parcelles.append(data)
        return jsonify({"message": "Parcelle ajoutée avec succès", "parcelle": data}), 201
        
    return jsonify(parcelles)

@app.route('/api/parcelles/<int:parcelle_id>', methods=['PUT'])
def modifier_parcelle(parcelle_id):
    data = request.json or {}
    for p in parcelles:
        if p.get('id') == parcelle_id:
            p['nom'] = data.get('nom', p['nom'])
            p['culture'] = data.get('culture', p['culture'])
            return jsonify({"message": "Parcelle mise à jour", "parcelle": p}), 200
            
    return jsonify({"erreur": "Parcelle non trouvée"}), 404


@app.route('/api/observations', methods=['GET', 'POST'])
def gerer_observations():
    if request.method == 'POST':
        data = request.json or {}
        champs_requis = ['parcelle_id', 'temperature', 'humidite', 'etat']
        
        if not all(champ in data for champ in champs_requis):
            return jsonify({"erreur": "Champs manquants : parcelle_id, temperature, humidite, etat"}), 400
            
        observations.append(data)
        
        
        temp = data.get('temperature', 0)
        hum = data.get('humidite', 0)
        alerte = None
        if hum > 70 and temp > 25:
            alerte = {
                "niveau": "Alerte",
                "message": "Situation à risque détectée : Humidité élevée et température forte. Risque de maladie.",
                "parcelle_id": data['parcelle_id']
            }
            
        return jsonify({"message": "Observation enregistrée", "alerte": alerte}), 201
        
    return jsonify(observations)


@app.route('/api/dashboard', methods=['GET'])
def tableau_de_bord():
    alertes = []
    for obs in observations:
        if obs.get('humidite', 0) > 70 and obs.get('temperature', 0) > 25:
            alertes.append({
                "parcelle_id": obs['parcelle_id'],
                "temperature": obs['temperature'],
                "humidite": obs['humidite'],
                "message": "Forte humidité et température élevée. Risque de maladie."
            })
            
    return jsonify({
        "indicateurs": {
            "nombre_parcelles": len(parcelles),
            "nombre_observations": len(observations),
        },
        "parcelles": parcelles,
        "observations": observations,
        "alertes": alertes
    })
    
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json or {}
    email = data.get('email')
    password = data.get('password')

    # On cherche l'utilisateur dans notre liste
    user = next((u for u in utilisateurs if u['email'] == email and u['password'] == password), None)

    if user:
        # En production, on enverrait un "Token" (JWT), mais pour le projet, 
        # renvoyer les infos de l'utilisateur suffit pour le frontend.
        return jsonify({
            "status": "success",
            "message": "Connexion réussie",
            "user": {"nom": user['nom'], "email": user['email']}
        }), 200
    
    return jsonify({"status": "error", "erreur": "Email ou mot de passe incorrect"}), 401

if __name__ == '__main__':
    app.run(debug=True, port=5000)