from flask import Flask, render_template, request, redirect, url_for
import rule_engine

app = Flask(__name__)

# Base de datos de clientes en memoria
clientes = []

# Definir reglas con rule-engine
reglas_puntuacion = [
    (rule_engine.Rule("edad < 30"), 0),
    (rule_engine.Rule("edad >= 30 and edad <= 50"), 30),
    (rule_engine.Rule("edad > 50"), 50),
    
    (rule_engine.Rule("salud == 'saludable'"), 0),
    (rule_engine.Rule("salud == 'hipertension'"), 15),
    (rule_engine.Rule("salud == 'obesidad'"), 15),
    (rule_engine.Rule("salud == 'diabetes'"), 15),

    (rule_engine.Rule("historial_familiar"), 5),  

    (rule_engine.Rule("estilo_vida == 'fumador'"), 10),
    (rule_engine.Rule("estilo_vida == 'alcoholico'"), 10),

    (rule_engine.Rule("ocupacion == 'oficina'"), 0),
    (rule_engine.Rule("ocupacion == 'piloto'"), 10),
    (rule_engine.Rule("ocupacion == 'bombero'"), 10),

    (rule_engine.Rule("historial_seguro == 'reclamos_frecuentes'"), 10)
]


# Función para calcular el puntaje
def calcular_puntaje(cliente):
    puntaje = 100  # Iniciamos con el puntaje máximo

    for regla, penalizacion in reglas_puntuacion:
        if regla.matches(cliente):
            puntaje -= penalizacion
    
    return max(0, puntaje)  # Ajustado para evitar valores negativos

# Función para asignar categoría de riesgo
def obtener_riesgo(puntaje_riesgo): 
    if puntaje_riesgo >= 95:
        return "Bajo Riesgo"
    elif 55 <= puntaje_riesgo < 95:
        return "Moderado Riesgo"
    else:
        return "Alto Riesgo"


@app.route('/')
def index():
    return render_template('index.html', clientes=clientes)

@app.route('/agregar_cliente', methods=['GET', 'POST'])
def agregar_cliente():
    if request.method == 'POST':
        nombre = request.form['nombre']
        edad = int(request.form['edad'])
        salud = request.form['salud']
        historial_familiar = request.form['historial_familiar'].lower() == 'true'  # Convertir a booleano
        estilo_vida = request.form['estilo_vida']
        ocupacion = request.form['ocupacion']
        historial_seguro = request.form['historial_seguro']
        
        # Crear nuevo cliente y agregarlo a la base de datos
        nuevo_cliente = {
            "nombre": nombre,
            "edad": edad,
            "salud": salud,
            "historial_familiar": historial_familiar,
            "estilo_vida": estilo_vida,
            "ocupacion": ocupacion,
            "historial_seguro": historial_seguro
        }
        
        clientes.append(nuevo_cliente)
        return redirect(url_for('index'))
    
    return render_template('agregar_cliente.html')

@app.route('/evaluar_riesgo')
def evaluar_riesgo():
    resultados = []
    for cliente in clientes:
        puntaje_riesgo = calcular_puntaje(cliente)
        nivel_riesgo = obtener_riesgo(puntaje_riesgo)
        resultados.append({
            "nombre": cliente['nombre'],
            "puntaje_riesgo": puntaje_riesgo,
            "nivel_riesgo": nivel_riesgo
        })
    
    return render_template('resultados.html', resultados=resultados)

if __name__ == '__main__':
    app.run(debug=True)
