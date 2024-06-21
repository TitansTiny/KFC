from flask import Blueprint, jsonify, request
import mysql.connector 
from AccesoDatos.Conexion import cadena_conexion

detalles_pedidos_bp = Blueprint('detalles_pedidos_bp', __name__)

#GET detalles pedidos 
@detalles_pedidos_bp.route('/get_detalles_pedidos', methods = ['GET']) 
def get_detalles_pedidos():
    connection = mysql.connector.connect(**cadena_conexion)
    cursor = connection.cursor(dictionary=True)
    cursor.execute("select * from detalles_pedidos")
    detalles_pedidos = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(detalles_pedidos)

#GET detalles de pedidos por id
@detalles_pedidos_bp.route('/get_detalles_pedidos/<int:idDetallePedido>', methods = ['GET'])
def get_detalles_pedido_id(idDetallePedido):
    connection = mysql.connector.connect(**cadena_conexion)
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM detalles_pedidos WHERE idDetallePedido = %s", (idDetallePedido,))
    platos = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(idDetallePedido)

#PUT/Actualizar un detalle de pedido
@detalles_pedidos_bp.route('/actualizar_detalles_pedidos/<int:idDetallePedido>', methods=['PUT'])
def update_detalles_pedido(idDetallePedido):
    try:
        data = request.get_json()
        connection = mysql.connector.connect(**cadena_conexion)  # Utilizamos tu función para crear la conexión
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE detalles_pedidos SET idPedido = %s, idPlato = %s, cantidad = %s WHERE idDetallePedido = %s",
            (data['idPedido'], data['idPlato'], data['cantidad'], idDetallePedido)
        )
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({'message': 'El Detalle del Pedido se actualizó correctamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
#Insert/POST pedidos
@detalles_pedidos_bp.route('/insert_detalles_pedido', methods = ['POST'])
def insert_detalles_pedido():
    data = request.get_json()
    idPedido = data.get('idPedido')
    idPlato = data.get('idPlato')
    cantidad = data.get('cantidad')
    precio_unitario = data.get('precio_unitario')
    connection = mysql.connector.connect(**cadena_conexion)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO pedidos (idPedido, idPlato, cantidad, precio_unitario) VALUES (%s, %s, %s, %s)",
                   (idPedido, idPlato, cantidad, precio_unitario))
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({"message": "El detalle del pedido se creó correctamente"}), 201



#Delete detalle de pedidos

@detalles_pedidos_bp.route('/delete_detalles_pedido/<int:idDetallePedido>', methods = ['DELETE'])
def delete_detalles_pedido(idDetallePedido):
    connection = mysql.connector.connect(**cadena_conexion)
    cursor = connection.cursor()
    cursor.execute("DELETE FROM detalles_pedidos WHERE idDetallePedido = %s", (idDetallePedido,))
    connection.commit()
    if cursor.rowcount == 0:
        return jsonify({"message": "No se encontró el detalle del pedido con el id proporcionado"}), 404
    cursor.close()
    connection.close()
    return jsonify({"message": "El detalle del peidido se eliminó correctamente"})