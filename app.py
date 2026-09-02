from flask import Flask, request
from database import conectar_bd

app = Flask(__name__)


@app.route("/probar")
def probar_data():
    connect = conectar_bd()

    if connect.is_connected():
        connect.close()

    return {
        "mensaje": "CONNECTED TO DATABASE"
    }


@app.route("/api/registrohv", methods=["POST"])
def registrohvida():
    conec = conectar_bd()
    cursor = conec.cursor()
    datos = request.json

    
    sql_consulta = "SELECT id FROM hojas_vida WHERE correo = %s"
    cursor.execute(sql_consulta, (datos["correo"],))
    usuario_existente = cursor.fetchone()

    if usuario_existente:

        id_existente = usuario_existente[0]

        cursor.close()
        conec.close()

        return {
            "mensaje": "El usuario ya está registrado con este correo",
            "id": id_existente
        }

    
    sql = """INSERT INTO hojas_vida
    (nombre, edad, ciudad, correo, fotografia, programa, ficha, jornada)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""

    valor = (
        datos["nombre"],
        datos["edad"],
        datos["ciudad"],
        datos["correo"],
        datos.get("fotografia"),
        datos["programa"],
        datos["ficha"],
        datos["jornada"]
    )

    cursor.execute(sql, valor)
    conec.commit()

    
    id_generado = cursor.lastrowid

    cursor.close()
    conec.close()

    return {
        "mensaje": "Hoja de vida creada",
        "id": id_generado
    }


@app.route("/api/hojasvida", methods=["GET"])
def listar_hojasvida():
    conec = conectar_bd()
    cursor = conec.cursor()

    sql = "SELECT * FROM hojas_vida"
    cursor.execute(sql)

    datos = cursor.fetchall()

    columnas = [columna[0] for columna in cursor.description]

    resultado = []

    for fila in datos:
        hoja_vida = dict(zip(columnas, fila))
        resultado.append(hoja_vida)

    cursor.close()
    conec.close()

    return {
        "hojas_vida": resultado
    }


if __name__ == "__main__":
    app.run(debug=True)
