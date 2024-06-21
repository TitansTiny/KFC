from flask import Blueprint, jsonify, request
import mysql.connector 
from AccesoDatos.Conexion import cadena_conexion

pedidos_bp = Blueprint('pedidos_bp', __name__)

#GET pedidos 
@pedidos_bp.route('/get_pedidos', methods = ['GET']) 
def get_pedidos():
    connection = mysql.connector.connect(**cadena_conexion)
    cursor = connection.cursor(dictionary=True)
    cursor.execute("select * from pedidos")
    pedidos = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(pedidos)

#GET pedidos por id
@pedidos_bp.route('/get_pedidos/<int:idPedido>', methods = ['GET'])
def get_pedidos_id(idPedido):
    connection = mysql.connector.connect(**cadena_conexion)
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM pedidos WHERE idPedido = %s", (idPedido,))
    platos = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(idPedido)

#PUT/Actualizar un pedido
@pedidos_bp.route('/actualizar_pedidos/<int:idPedido>', methods=['PUT'])
def update_pedido(idPedido):
    try:
        data = request.get_json()
        connection = mysql.connector.connect(**cadena_conexion)  # Utilizamos tu función para crear la conexión
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE pedidos SET idCliente = %s, fechaPedido = %s, total = %s WHERE idPedido = %s",
            (data['idCliente'], data['fechaPedido'], data['total'], idPedido)
        )
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({'message': 'El pedido se actualizó correctamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
#Insert/POST pedidos
@pedidos_bp.route('/insert_pedidos', methods=['POST'])
def insert_pedidos():
    data = request.get_json()
    idCliente = data.get('idCliente')
    fechaPedido = data.get('fechaPedido')
    total = data.get('total')
    connection = mysql.connector.connect(**cadena_conexion)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO pedidos (idCliente, fechaPedido, total) VALUES (%s, %s, %s)",
                   (idCliente, fechaPedido, total))
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({"message": "El Pedido se creó correctamente"}), 201



#Delete pedidos

@pedidos_bp.route('/delete_pedidos/<int:idPedido>', methods=['DELETE'])
def delete_pedidos(idPedido):
    connection = mysql.connector.connect(**cadena_conexion)
    cursor = connection.cursor()
    cursor.execute("DELETE FROM pedidos WHERE idPedido = %s", (idPedido,))
    connection.commit()
    if cursor.rowcount == 0:
        return jsonify({"message": "No se encontró el Pedido con el id proporcionado"}), 404
    cursor.close()
    connection.close()
    return jsonify({"message": "El Pedido se eliminó correctamente"})