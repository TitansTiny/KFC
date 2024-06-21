from flask import Flask
from flask_cors import CORS
from APIRest.Controllers.platosController import platos_bp
from APIRest.Controllers.clientesController import clientes_bp
from APIRest.Controllers.pedidosController import pedidos_bp
from APIRest.Controllers.detalles_pedidosController import detalles_pedidos_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(platos_bp)
app.register_blueprint(clientes_bp)
app.register_blueprint(pedidos_bp)
app.register_blueprint(detalles_pedidos_bp)

if __name__ == '__main__':
    app.run()