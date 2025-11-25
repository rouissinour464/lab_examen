from flask import Flask, jsonify
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time
import random

app = Flask(__name__)

# --------------------
# Définition des métriques Prometheus
# --------------------
REQUEST_COUNT = Counter('app_requests_total', 'Nombre total de requêtes reçues', ['endpoint'])
REQUEST_LATENCY = Histogram('app_request_latency_seconds', 'Latence des requêtes en secondes', ['endpoint'])

# --------------------
# Routes de l'application
# --------------------
@app.route('/')
def index():
    start_time = time.time()
    REQUEST_COUNT.labels(endpoint='/').inc()
    
    # Simulation d’un traitement aléatoire
    simulated_latency = random.uniform(0.1, 0.5)
    time.sleep(simulated_latency)
    
    REQUEST_LATENCY.labels(endpoint='/').observe(time.time() - start_time)
    
    return jsonify(message="Hello DevOps! Welcome to Monitoring Lab."), 200


@app.route('/hello/<name>')
def hello(name):
    """Nouvelle route pour tester les requêtes avec paramètres"""
    start_time = time.time()
    REQUEST_COUNT.labels(endpoint='/hello').inc()
    
    simulated_latency = random.uniform(0.1, 0.7)
    time.sleep(simulated_latency)
    
    REQUEST_LATENCY.labels(endpoint='/hello').observe(time.time() - start_time)
    
    return jsonify(message=f"Hello {name}!"), 200


@app.route('/metrics')
def metrics():
    """Endpoint pour Prometheus"""
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}


# --------------------
# Lancement de l'application
# --------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
