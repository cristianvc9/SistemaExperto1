from flask import Flask, render_template, request, redirect, url_for
import rule_engine

app = Flask(__name__)

# Base de datos en memoria (simulación)
clientes = []

# Reglas de evaluación de riesgo
reglas_aprobado = [
    rule_engine.Rule("(historialCrediticio > 750) and (historialPrestamo == 'sinRetraso')"),
    rule_engine.Rule("(ingresosMensuales > 3) and (deudaIngreso < 30)"),
    rule_engine.Rule("(tipoEmpleo == 'contratoFijoMayor5') and (ingresosMensuales > 3)"),
    rule_engine.Rule("(ingresosMensuales > 3) and ((tipoEmpleo == 'autonomo') or (tipoEmpleo == 'independiente'))"),
    rule_engine.Rule("(garantias == 'avalAltoValor')")
]
reglas_aprobado_condicional = [
    rule_engine.Rule("(historialCrediticio > 600 and historialCrediticio <= 750) and (historialPrestamo == 'retrasoOcasional')"),
    rule_engine.Rule("(deudaIngreso >= 30 and deudaIngreso <= 50)"),
    rule_engine.Rule("(garantias == 'avalMedioValor') and (montoPrestamo < 50000) and (tasaInteres > 10)"),
    rule_engine.Rule("((tipoEmpleo == 'autonomo') or (tipoEmpleo == 'independiente')) and (garantias == 'avalBajoValor')")
]
reglas_rechazado = [
    rule_engine.Rule("(historialCrediticio > 1 and historialCrediticio <= 600) and (historialPrestamo == 'retrasoFrecuente') and (garantias != 'avalAltoValor')"),
    rule_engine.Rule("(ingresosMensuales < 1.5) and (deudaIngreso >= 50 and deudaIngreso <= 80) and (garantias != 'avalAltoValor')"),
    rule_engine.Rule("(ingresosMensuales < 1.5) and (deudaIngreso >= 50 and deudaIngreso <= 80) and (garantias == 'avalAltoValor')"),
]


def evaluar_cliente(cliente):
    datos_cliente = {
        "historialCrediticio": int(cliente["historialCrediticio"]),
        "historialPrestamo": cliente["historialPrestamo"],
        "ingresosMensuales": float(cliente["ingresosMensuales"]),
        "deudaIngreso": float(cliente["deudaIngreso"]),
        "tipoEmpleo": cliente["tipoEmpleo"],
        "garantias": cliente["garantias"]
    }

    # Verificar en qué grupo de reglas cae el cliente
    if any(regla.matches(datos_cliente) for regla in reglas_aprobado):
        return "Aprobado"
    elif any(regla.matches(datos_cliente) for regla in reglas_aprobado_condicional):
        return "Aprobado Condicional"
    else:
        return "Rechazado"


@app.route("/")
def index():
    return render_template("index.html", clientes=clientes)

@app.route("/agregar_cliente", methods=["GET", "POST"])
def agregar_cliente():
    if request.method == "POST":
        cliente = {
            "nombre": request.form["nombre"],
            "historialCrediticio": request.form["historialCrediticio"],
            "historialPrestamo": request.form["historialPrestamo"],
            "ingresosMensuales": request.form["ingresosMensuales"],
            "deudaIngreso": request.form["deudaIngreso"],
            "tipoEmpleo": request.form["tipoEmpleo"],
            "garantias": request.form["garantias"]
        }
        clientes.append(cliente)
        return redirect(url_for("index"))
    
    return render_template("agregar_cliente.html")

@app.route("/resultados")
def resultados():
    clientes_evaluados = [{"nombre": c["nombre"], "evaluacion": evaluar_cliente(c)} for c in clientes]
    return render_template("resultados.html", clientes=clientes_evaluados)

if __name__ == "__main__":
    app.run(debug=True)
