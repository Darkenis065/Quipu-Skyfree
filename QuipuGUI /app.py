from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def menu():
    return render_template('menu.html')

@app.route('/analisis')
def analisis():
    return render_template('index.html')  # tu interfaz principal

@app.route('/calcular_hubble', methods=['POST'])
def calcular_hubble():
    data = request.json
    redshift = float(data.get('redshift', 0))
    # Constante de Hubble (valor aproximado en km/s/Mpc)
    H0 = 70.0
    # Velocidad de recesión aproximada v = H0 * d → v ≈ c * z para bajas z
    c = 3e5  # velocidad de la luz en km/s
    velocidad = c * redshift
    # Distancia estimada en Mpc (simplificada)
    distancia = velocidad / H0
    resultado = {
        "redshift": redshift,
        "velocidad": round(velocidad, 2),
        "distancia": round(distancia, 2),
        "H0": H0
    }
    return jsonify(resultado)

if __name__ == '__main__':
    app.run(debug=True)

