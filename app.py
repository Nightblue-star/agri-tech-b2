import sqlite3
import os
from flask import Flask, render_template, request, jsonify, g
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ─── Base de données SQLite ─────────────────────────────────────────────────────

DATABASE = os.path.join(os.path.dirname(__file__), 'agritech.db')

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    """Crée les tables et insère les données si la BDD n'existe pas encore."""
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    cur = db.cursor()

    cur.executescript("""
        CREATE TABLE IF NOT EXISTS utilisateur (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            mot_de_passe TEXT NOT NULL,
            role TEXT DEFAULT 'agriculteur'
        );

        CREATE TABLE IF NOT EXISTS parcelles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            localisation TEXT,
            surface_ha REAL DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS cultures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            date_semis TEXT,
            parcelle_id INTEGER,
            FOREIGN KEY (parcelle_id) REFERENCES parcelles(id)
        );

        CREATE TABLE IF NOT EXISTS meteo (
            id_meteo INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            temperature REAL,
            humidite REAL,
            pluie_mm REAL DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS observations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            etat TEXT,
            parcelle_id INTEGER,
            commentaire TEXT,
            FOREIGN KEY (parcelle_id) REFERENCES parcelles(id)
        );

        CREATE TABLE IF NOT EXISTS alertes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            type TEXT,
            parcelle_id INTEGER,
            niveau INTEGER DEFAULT 1,
            FOREIGN KEY (parcelle_id) REFERENCES parcelles(id)
        );
    """)

    # Insérer les données initiales seulement si les tables sont vides
    if cur.execute("SELECT COUNT(*) FROM utilisateur").fetchone()[0] == 0:
        cur.executemany("INSERT INTO utilisateur (nom, email, mot_de_passe, role) VALUES (?,?,?,?)", [
            ('Admin', 'admin@ferme.com', 'admin123', 'admin'),
            ('Jean Agro', 'jean@ferme.com', 'agro456', 'agriculteur'),
            ('Clyfton', 'test@agritech.fr', 'password123', 'agriculteur'),
        ])

    if cur.execute("SELECT COUNT(*) FROM parcelles").fetchone()[0] == 0:
        cur.executemany("INSERT INTO parcelles (nom, localisation, surface_ha) VALUES (?,?,?)", [
            ('Parcelle 1', 'Zone A', 2.45),
            ('Parcelle 2', 'Zone B', 4.49),
            ('Parcelle 3', 'Zone C', 2.15),
            ('Parcelle 4', 'Zone D', 2.49),
            ('Parcelle 5', 'Zone E', 3.2),
            ('Parcelle 6', 'Zone A', 4.06),
            ('Parcelle 7', 'Zone B', 2.45),
            ('Parcelle 8', 'Zone C', 3.88),
            ('Parcelle 9', 'Zone D', 4.07),
            ('Parcelle 10', 'Zone E', 2.37),
        ])

    if cur.execute("SELECT COUNT(*) FROM cultures").fetchone()[0] == 0:
        cur.executemany("INSERT INTO cultures (type, date_semis, parcelle_id) VALUES (?,?,?)", [
            ('Orge', '2026-03-15', 1), ('Tournesol', '2026-03-20', 2),
            ('Blé', '2026-03-19', 3),  ('Maïs', '2026-03-21', 4),
            ('Blé', '2026-03-16', 5),  ('Tournesol', '2026-03-03', 6),
            ('Orge', '2026-03-19', 7), ('Tournesol', '2026-03-11', 8),
            ('Colza', '2026-03-12', 9),('Colza', '2026-03-17', 10),
        ])

    if cur.execute("SELECT COUNT(*) FROM meteo").fetchone()[0] == 0:
        meteo_data = [
            ('2026-03-01',17,47,0),('2026-03-02',14,74,5),('2026-03-03',29,39,30),
            ('2026-03-04',17,38,5),('2026-03-05',18,39,10),('2026-03-06',9,94,0),
            ('2026-03-07',16,44,20),('2026-03-08',17,51,0),('2026-03-09',22,94,0),
            ('2026-03-10',20,91,30),('2026-03-11',17,60,0),('2026-03-12',20,95,5),
            ('2026-03-13',12,30,10),('2026-03-14',14,76,5),('2026-03-15',9,63,0),
            ('2026-03-16',25,60,20),('2026-03-17',9,33,0),('2026-03-18',17,69,30),
            ('2026-03-19',16,86,30),('2026-03-20',25,44,0),('2026-03-21',15,74,10),
            ('2026-03-22',17,83,10),('2026-03-23',10,56,0),('2026-03-24',22,72,0),
            ('2026-03-25',6,70,0),('2026-03-26',21,49,30),('2026-03-27',25,37,5),
            ('2026-03-28',7,41,5),('2026-03-29',22,59,10),('2026-03-30',22,90,20),
            ('2026-03-31',27,69,0),('2026-04-01',7,38,0),('2026-04-02',6,77,0),
            ('2026-04-03',23,35,10),('2026-04-04',20,88,5),('2026-04-05',17,45,30),
            ('2026-04-06',20,80,0),('2026-04-07',21,42,30),('2026-04-08',18,51,5),
            ('2026-04-09',17,85,20),('2026-04-10',20,72,10),('2026-04-11',24,47,10),
            ('2026-04-12',20,93,0),('2026-04-13',17,69,30),('2026-04-14',15,73,20),
            ('2026-04-15',10,71,0),('2026-04-16',13,71,5),('2026-04-17',30,44,0),
            ('2026-04-18',17,81,20),('2026-04-19',17,83,10),('2026-04-20',21,93,5),
            ('2026-04-21',13,85,10),('2026-04-22',5,50,0),('2026-04-23',6,89,5),
            ('2026-04-24',13,92,20),('2026-04-25',14,91,30),('2026-04-26',19,42,0),
            ('2026-04-27',15,65,0),('2026-04-28',27,89,0),('2026-04-29',23,56,20),
        ]
        cur.executemany("INSERT INTO meteo (date, temperature, humidite, pluie_mm) VALUES (?,?,?,?)", meteo_data)

    if cur.execute("SELECT COUNT(*) FROM observations").fetchone()[0] == 0:
        obs_data = [
            ('2026-03-02','OK',2,'Sol sec'),('2026-03-15','Risque maladie',3,'Sol sec'),
            ('2026-04-17','OK',8,'Sol sec'),('2026-03-02','Stress hydrique',8,'Sol sec'),
            ('2026-03-30','Stress hydrique',9,'Sol sec'),('2026-03-11','OK',3,'Humidité élevée'),
            ('2026-03-09','Maladie détectée',2,'Humidité élevée'),('2026-04-28','OK',10,'Humidité élevée'),
            ('2026-03-08','Stress hydrique',9,'Feuilles jaunies'),('2026-03-20','Stress hydrique',8,'Humidité élevée'),
            ('2026-04-19','Risque maladie',4,'Sol sec'),('2026-03-02','Stress hydrique',8,'Feuilles jaunies'),
            ('2026-03-02','Maladie détectée',5,'Feuilles jaunies'),('2026-03-01','OK',7,'Humidité élevée'),
            ('2026-03-17','Stress hydrique',2,'Humidité élevée'),('2026-04-06','Maladie détectée',7,'Feuilles jaunies'),
            ('2026-03-23','Risque maladie',9,'Sol sec'),('2026-03-28','OK',4,'Humidité élevée'),
            ('2026-03-05','Stress hydrique',5,'Rien à signaler'),('2026-03-16','Risque maladie',8,'Rien à signaler'),
            ('2026-03-22','OK',2,'Humidité élevée'),('2026-04-20','OK',3,'Feuilles jaunies'),
            ('2026-03-05','Maladie détectée',10,'Rien à signaler'),('2026-04-13','OK',10,'Rien à signaler'),
            ('2026-04-21','OK',7,'Sol sec'),('2026-04-18','Maladie détectée',10,'Humidité élevée'),
            ('2026-03-04','OK',10,'Rien à signaler'),('2026-04-18','OK',7,'Feuilles jaunies'),
            ('2026-03-09','Risque maladie',6,'Sol sec'),('2026-04-19','Maladie détectée',9,'Humidité élevée'),
        ]
        cur.executemany("INSERT INTO observations (date, etat, parcelle_id, commentaire) VALUES (?,?,?,?)", obs_data)

    if cur.execute("SELECT COUNT(*) FROM alertes").fetchone()[0] == 0:
        alertes_data = [
            ('2026-04-11','Stress hydrique',3,2),('2026-03-04','Stress hydrique',8,1),
            ('2026-03-29','Stress hydrique',4,1),('2026-04-07','Stress hydrique',10,2),
            ('2026-03-05','Risque maladie',4,2),('2026-04-12','Stress hydrique',1,2),
            ('2026-03-23','Stress hydrique',2,3),('2026-03-29','Stress hydrique',1,2),
            ('2026-03-25','Risque maladie',4,1),('2026-04-14','Stress hydrique',4,3),
            ('2026-03-10','Risque maladie',5,2),('2026-04-10','Risque maladie',7,1),
            ('2026-04-19','Stress hydrique',9,2),('2026-04-02','Stress hydrique',9,3),
            ('2026-04-28','Stress hydrique',7,2),('2026-04-12','Stress hydrique',10,2),
            ('2026-03-14','Risque maladie',5,2),('2026-03-21','Stress hydrique',9,3),
            ('2026-03-25','Risque maladie',3,1),('2026-04-14','Risque maladie',7,3),
            ('2026-04-13','Risque maladie',1,1),('2026-03-10','Risque maladie',2,2),
            ('2026-03-03','Risque maladie',10,1),('2026-03-27','Risque maladie',7,1),
            ('2026-03-12','Risque maladie',3,3),('2026-04-17','Stress hydrique',3,2),
            ('2026-04-23','Stress hydrique',8,2),('2026-04-15','Stress hydrique',6,2),
            ('2026-04-09','Risque maladie',7,3),('2026-04-21','Risque maladie',3,3),
        ]
        cur.executemany("INSERT INTO alertes (date, type, parcelle_id, niveau) VALUES (?,?,?,?)", alertes_data)

    db.commit()
    db.close()

# ─── Routes pages HTML ──────────────────────────────────────────────────────────

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/')
def connexion():
    return render_template('connexion.html')

@app.route('/parcelles')
def page_parcelles():
    return render_template('parcelles.html')

@app.route('/observations')
def page_observations():
    return render_template('observations.html')

@app.route('/carte')
def page_carte():
    return render_template('carte.html')

@app.route('/meteo')
def page_meteo():
    return render_template('meteo.html')

@app.route('/alertes')
def page_alertes():
    return render_template('alertes.html')

# ─── API Parcelles ──────────────────────────────────────────────────────────────

@app.route('/api/parcelles', methods=['GET', 'POST'])
def api_parcelles():
    db = get_db()
    if request.method == 'POST':
        data = request.json or {}
        nom = data.get('nom', '').strip()
        localisation = data.get('localisation', '').strip()
        surface = data.get('surface_ha', 0)
        culture = data.get('culture', '').strip()
        if not nom:
            return jsonify({"erreur": "Le champ 'nom' est obligatoire"}), 400
        cur = db.execute(
            "INSERT INTO parcelles (nom, localisation, surface_ha) VALUES (?,?,?)",
            (nom, localisation, surface)
        )
        parcelle_id = cur.lastrowid
        # Si une culture est précisée, on l'ajoute dans la table cultures
        if culture:
            import datetime
            db.execute(
                "INSERT INTO cultures (type, date_semis, parcelle_id) VALUES (?,?,?)",
                (culture, datetime.date.today().isoformat(), parcelle_id)
            )
        db.commit()
        return jsonify({"message": "Parcelle ajoutée", "id": parcelle_id}), 201

    rows = db.execute("""
        SELECT p.id, p.nom, p.localisation, p.surface_ha, c.type as culture
        FROM parcelles p
        LEFT JOIN cultures c ON c.parcelle_id = p.id
        GROUP BY p.id
        ORDER BY p.id
    """).fetchall()
    return jsonify([dict(r) for r in rows])

@app.route('/api/parcelles/<int:pid>', methods=['PUT', 'DELETE'])
def api_parcelle_detail(pid):
    db = get_db()
    if request.method == 'DELETE':
        db.execute("DELETE FROM parcelles WHERE id=?", (pid,))
        db.commit()
        return jsonify({"message": "Parcelle supprimée"})
    data = request.json or {}
    db.execute(
        "UPDATE parcelles SET nom=?, localisation=?, surface_ha=? WHERE id=?",
        (data.get('nom'), data.get('localisation'), data.get('surface_ha'), pid)
    )
    db.commit()
    return jsonify({"message": "Parcelle mise à jour"})

# ─── API Observations ───────────────────────────────────────────────────────────

@app.route('/api/observations', methods=['GET', 'POST'])
def api_observations():
    db = get_db()
    if request.method == 'POST':
        data = request.json or {}
        parcelle_id = data.get('parcelle_id')
        etat = data.get('etat', '').strip()
        commentaire = data.get('commentaire', '').strip()
        date = data.get('date', '')
        if not parcelle_id or not etat:
            return jsonify({"erreur": "Champs 'parcelle_id' et 'etat' obligatoires"}), 400
        import datetime
        if not date:
            date = datetime.date.today().isoformat()
        db.execute(
            "INSERT INTO observations (date, etat, parcelle_id, commentaire) VALUES (?,?,?,?)",
            (date, etat, parcelle_id, commentaire)
        )
        db.commit()
        return jsonify({"message": "Observation enregistrée"}), 201

    rows = db.execute("""
        SELECT o.id, o.date, o.etat, o.commentaire, o.parcelle_id, p.nom as parcelle_nom
        FROM observations o
        LEFT JOIN parcelles p ON p.id = o.parcelle_id
        ORDER BY o.date DESC
        LIMIT 50
    """).fetchall()
    return jsonify([dict(r) for r in rows])

@app.route('/api/observations/<int:oid>', methods=['DELETE'])
def api_observation_delete(oid):
    db = get_db()
    db.execute("DELETE FROM observations WHERE id=?", (oid,))
    db.commit()
    return jsonify({"message": "Observation supprimée"})

# ─── API Alertes ────────────────────────────────────────────────────────────────

@app.route('/api/alertes', methods=['GET'])
def api_alertes():
    db = get_db()
    niveau = request.args.get('niveau')
    query = """
        SELECT a.id, a.date, a.type, a.niveau, a.parcelle_id, p.nom as parcelle_nom
        FROM alertes a
        LEFT JOIN parcelles p ON p.id = a.parcelle_id
    """
    params = []
    if niveau:
        query += " WHERE a.niveau = ?"
        params.append(int(niveau))
    query += " ORDER BY a.date DESC LIMIT 50"
    rows = db.execute(query, params).fetchall()
    return jsonify([dict(r) for r in rows])

# ─── API Météo ──────────────────────────────────────────────────────────────────

@app.route('/api/meteo', methods=['GET'])
def api_meteo():
    db = get_db()
    rows = db.execute(
        "SELECT * FROM meteo ORDER BY date DESC LIMIT 7"
    ).fetchall()
    return jsonify([dict(r) for r in rows])

# ─── API Dashboard ──────────────────────────────────────────────────────────────

@app.route('/api/dashboard', methods=['GET'])
def api_dashboard():
    db = get_db()
    nb_parcelles = db.execute("SELECT COUNT(*) FROM parcelles").fetchone()[0]
    nb_observations = db.execute("SELECT COUNT(*) FROM observations").fetchone()[0]
    nb_alertes = db.execute("SELECT COUNT(*) FROM alertes WHERE niveau >= 2").fetchone()[0]
    surface_totale = db.execute("SELECT ROUND(SUM(surface_ha),2) FROM parcelles").fetchone()[0] or 0
    meteo = db.execute("SELECT * FROM meteo ORDER BY date DESC LIMIT 1").fetchone()
    alertes = db.execute("""
        SELECT a.date, a.type, a.niveau, p.nom as parcelle_nom
        FROM alertes a LEFT JOIN parcelles p ON p.id = a.parcelle_id
        WHERE a.niveau >= 2 ORDER BY a.date DESC LIMIT 5
    """).fetchall()
    return jsonify({
        "indicateurs": {
            "nombre_parcelles": nb_parcelles,
            "nombre_observations": nb_observations,
            "nombre_alertes": nb_alertes,
            "surface_totale": surface_totale,
        },
        "meteo_actuelle": dict(meteo) if meteo else {},
        "alertes_recentes": [dict(r) for r in alertes]
    })

# ─── API Login ──────────────────────────────────────────────────────────────────

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json or {}
    email = data.get('email', '').strip()
    password = data.get('password', '').strip()
    db = get_db()
    user = db.execute(
        "SELECT * FROM utilisateur WHERE email=? AND mot_de_passe=?",
        (email, password)
    ).fetchone()
    if user:
        return jsonify({
            "status": "success",
            "message": "Connexion réussie",
            "user": {"nom": user['nom'], "email": user['email'], "role": user['role']}
        }), 200
    return jsonify({"status": "error", "erreur": "Email ou mot de passe incorrect"}), 401

# ─── Démarrage ──────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)