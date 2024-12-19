import pandas as pd
from flask import Flask, jsonify, request
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Counter, make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware

# Charger les données
file_path = './donnees_brutes/covid_data.csv'
try:
    data = pd.read_csv(file_path, sep=';')
except FileNotFoundError:
    print(f"Fichier non trouvé : {file_path}. Chargement d'un DataFrame vide.")
    data = pd.DataFrame(columns=['reg', 'date_de_passage', 'sursaud_cl_age_corona', 'nbre_pass_corona', 'nbre_pass_tot'])

# Sélection des colonnes pertinentes
selected_columns = ['reg', 'date_de_passage', 'sursaud_cl_age_corona', 'nbre_pass_corona', 'nbre_pass_tot']
data = data[selected_columns]

# Transformation des données
data['date_de_passage'] = pd.to_datetime(data['date_de_passage'], errors='coerce')
data = data.dropna()
data['reg'] = data['reg'].astype(int)
data['sursaud_cl_age_corona'] = data['sursaud_cl_age_corona'].astype(int)
data['nbre_pass_corona'] = data['nbre_pass_corona'].astype(int)
data['nbre_pass_tot'] = data['nbre_pass_tot'].astype(int)

# Création de l'API Flask
app = Flask(__name__)

# Ajouter l'endpoint /metrics manuellement
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})

# Initialisation des métriques avec Prometheus
metrics = PrometheusMetrics(app)
metrics.info('app_info', 'Application info', version='1.0.0')

# Compteurs Prometheus
data_request_counter = Counter('data_requests_total', 'Nombre total de requêtes sur /api/data', ['reg'])
summary_request_counter = Counter('summary_requests_total', 'Nombre total de requêtes sur /api/summary')

@app.route('/api/data', methods=['GET'])
def get_data():
    reg = request.args.get('reg', type=int)
    start_date = request.args.get('start_date', type=str)
    end_date = request.args.get('end_date', type=str)

    if reg:
        data_request_counter.labels(reg=reg).inc()

    filtered_data = data
    if reg:
        filtered_data = filtered_data[filtered_data['reg'] == reg]
    if start_date:
        filtered_data = filtered_data[filtered_data['date_de_passage'] >= start_date]
    if end_date:
        filtered_data = filtered_data[filtered_data['date_de_passage'] <= end_date]

    if filtered_data.empty:
        return jsonify({"error": "Aucune donnée trouvée pour les paramètres fournis."}), 404

    result = filtered_data.to_dict(orient='records')
    return jsonify(result)

@app.route('/api/summary', methods=['GET'])
def get_summary():
    summary_request_counter.inc()
    summary = data.groupby('reg').agg({
        'nbre_pass_corona': 'sum',
        'nbre_pass_tot': 'sum'
    }).reset_index()
    summary = summary.rename(columns={
        'nbre_pass_corona': 'total_pass_corona',
        'nbre_pass_tot': 'total_passages'
    })
    result = summary.to_dict(orient='records')
    return jsonify(result)

@app.route('/api/prometheus', methods=['GET'])
def get_prometheus_data():
    """
    Endpoint pour Grafana : renvoie les données au format compatible
    """
    prometheus_data = []
    for _, row in data.iterrows():
        prometheus_data.append({
            "timestamp": row['date_de_passage'].isoformat(),  # ISO 8601 format
            "region": row['reg'],
            "corona_cases": row['nbre_pass_corona'],
            "total_cases": row['nbre_pass_tot'],
            "age_category": row['sursaud_cl_age_corona']
        })
    return jsonify(prometheus_data)

if __name__ == '__main__':
    print("Aperçu des données chargées :")
    print(data.head())
    app.run(debug=True, host='0.0.0.0', port=5000)