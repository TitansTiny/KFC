from flask import Blueprint, jsonify, request
import mysql.connector
from AccesoDatos.Conexion import cadena_conexion

platos_bp  = Blueprint('platos_bp', __name__)


# GET all platos
@platos_bp.route('/get_platos', methods = ['GET'])
def get_platos():
    connection = mysql.connector.connect(**cadena_conexion)
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM platos")
    platos = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(platos)

# GET plato por nombre
@platos_bp.route('/get_platos/<string:nombre_Plato>', methods = ['GET'])
def get_platos_id(nombrePlato):
    connection = mysql.connector.connect(**cadena_conexion)
    cursor = connection.cursor(dictionary=True)
    search_pattern =nombrePlato + '%'
    cursor.execute("SELECT * FROM platos WHERE nombrePlato LIKE %s", (search_pattern,))
    #cursor.execute("SELECT * FROM platos WHERE nombrePlato = %s", (nombrePlato,))
    platos = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(platos)

# POST new plato
@platos_bp.route('/insert_platos', methods = ['POST'])
def insert_platos():
    data = request.get_json()
    nombre_plato = data.get('nombre_plato')
    descripcion = data.get('descripcion')
    precio = data.get('precio')
    imagen = data.get('imagen')
    id_categoria = data.get('id_categoria')

    connection = mysql.connector.connect(**cadena_conexion)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO platos (nombre_plato, descripcion, precio, imagen, id_categoria) VALUES (%s, %s, %s, %s, %s)",
                   (nombre_plato, descripcion, precio, imagen, id_categoria))
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({"message": "El plato se creó correctamente"}), 201

#PUT/Actualizar un plato

@platos_bp.route('/actualizar_platos/<int:id>', methods=['PUT'])
def update_plato(id):
    try:
        data = request.get_json()
        connection = mysql.connector.connect(**cadena_conexion)  # Utilizamos tu función para crear la conexión
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE platos SET nombre_Plato = %s, descripcion = %s, precio = %s, imagen = %s, id_categoria = %s WHERE id_plato = %s",
            (data['nombre_plato'], data['descripcion'], data['precio'], data['imagen'], data['id_categoria'], id)
        )
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({'message': 'El plato se actualizó correctamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    
# DELETE plato by id
@platos_bp.route('/delete_platos/<int:id_plato>', methods = ['DELETE'])
def delete_platos(id_plato):
    connection = mysql.connector.connect(**cadena_conexion)
    cursor = connection.cursor()
    cursor.execute("DELETE FROM platos WHERE id_plato = %s", (id_plato,))
    connection.commit()
    if cursor.rowcount == 0:
        return jsonify({"message": "No se encontró el plato con el id proporcionado"}), 404
    cursor.close()
    connection.close()
    return jsonify({"message": "El plato se eliminó correctamente"})


