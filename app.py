from flask import Flask, request
from database import conectar_bd
app= Flask(__name__)

@app .route("/probar")
def probar_data():
    conec = conectar_bd()
    if conec.is_connected():
        conec.close()
    return {
        "mensaje":"Conexion ok"
    }
@app.route("/api/registrohv",methods=["POST"])
def registrohvida():
    conec = conectar_bd()
    cursor = conec.cursor(dictionary=True)
    datos = request.json 

    sql = """INSERT INTO hojas_vida(nombre,edad,ciudad,correo,fotografia,programa,ficha,jornada)Values(%s,%s,%s,%s,%s,%s,%s,%s)"""
    valor = (datos["nombre"],
              datos["edad"],
              datos["ciudad"],
              datos["correo"],
              datos.get("fotografia"),
              datos["programa"],
              datos["ficha"],
              datos["jornada"])
    cursor.execute(sql,valor)
    conec.commit()
    #manejo del id de la hoja de vida
    id_generado = cursor.lastrowid

    cursor.close()
    conec.close()

    return{"mensaje":"Hoja de vida creada","id":id_generado}

@app.route("/")
def inicio():
    return "Api hoja de vida funcionando"

@app.route("/api/hojas-vida/<int:id>")
def obtener_hojasvidaid(id):
    return{
        "mensaje":"Hoja de vida encontrada","id":id
    }

@app.route("/api/hojas-vida")
def obtener_hojasvida():
    #return{
     #   "mensaje":"Listado de hojas de vida"
    #}
    hojas_vida =[{
        "id":1,
        "nombre":"Johanna Cifuentes",
        "edad":50,
        "ciudad":"Bogota",
        "fotografia":"foto",
        "programa":"adso",
        "ficha":2323,
        "jornada":"diurna"
    },
    {
        "id":2,
        "nombre":"Leydy Diaz",
        "edad":18,
        "ciudad":"Cali",
        "fotografia":"foto",
        "programa":"Fotografia",
        "ficha":1010,
        "jornada":"Nocturna"
    }]
    return hojas_vida

if __name__== "__main__":
    app.run(debug=True)