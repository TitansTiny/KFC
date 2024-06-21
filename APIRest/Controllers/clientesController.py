from flask import Blueprint, jsonify, request
import mysql.connector 
from AccesoDatos.Conexion import cadena_conexion

clientes_bp = Blueprint('clientes_bp', __name__)

#GET clientes 
@clientes_bp.route('/get_clientes', methods = ['GET']) 
def get_clientes():
    connection = mysql.connector.connect(**cadena_conexion)
    cursor = connection.cursor(dictionary=True)
    cursor.execute("select * from clientes")
    clientes = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(clientes)

#GET clientes por nombre
@clientes_bp.route('/get_clientes/<string:nombreCliente>', methods = ['GET'])
def get_platos_id(nombreCliente):
    connection = mysql.connector.connect(**cadena_conexion)
    cursor = connection.cursor(dictionary=True)
    search_pattern = nombreCliente + '%'
    cursor.execute("SELECT * FROM clientes WHERE nombreCliente LIKE %s", (search_pattern,))
    #cursor.execute("SELECT * FROM clientes WHERE nombreCliente = %s", (nombreCliente,))
    clientes = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(clientes)

#PUT/Actualizar un pedido
@clientes_bp.route('/actualizar_clientes/<int:idCliente>', methods=['PUT'])
def update_cliente(idCliente):
    try:
        data = request.get_json()
        connection = mysql.connector.connect(**cadena_conexion)  # Utilizamos tu función para crear la conexión
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE clientes SET nombreCliente = %s, telefonoCliente = %s, emailCliente = %s, direccionCliente = %s WHERE idCliente = %s",
            (data['nombreCliente'], data['telefonoCliente'], data['emailCliente'], data['direccionCliente'], idCliente)
        )
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({'message': 'El cliente se actualizó correctamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
#Insert/POST clientes
@clientes_bp.route('/insert_clientes', methods = ['POST'])
def insert_platos():
    data = request.get_json()
    nombreCliente = data.get('nombreCliente')
    telefonoCliente = data.get('telefonoCliente')
    emailCliente = data.get('emailCliente')
    direccionCliente = data.get('direccionCliente')
    connection = mysql.connector.connect(**cadena_conexion)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO clientes (nombreCliente, telefonoCliente, emailCliente, direccionCliente) VALUES (%s, %s, %s, %s)",
                   (nombreCliente, telefonoCliente, emailCliente, direccionCliente))
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({"message": "El cliente se creó correctamente"}), 201

#Delete clientes

@clientes_bp.route('/delete_clientes/<int:idClientes>', methods = ['DELETE'])
def delete_platos(idCliente):
    connection = mysql.connector.connect(**cadena_conexion)
    cursor = connection.cursor()
    cursor.execute("DELETE FROM platos WHERE idPlato = %s", (idCliente,))
    connection.commit()
    if cursor.rowcount == 0:
        return jsonify({"message": "No se encontró el cliente con el id proporcionado"}), 404
    cursor.close()
    connection.close()
    return jsonify({"message": "El cliente se eliminó correctamente"})
