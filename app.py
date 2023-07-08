from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)
app.app_context().push()

class Product(db.Model):
    # database columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(200))

    def __repr__(self):
        return f'{self.name} - {self.description}'
 
@app.route('/')
def index():
    return 'Welcome! this is a home page'

@app.route('/items')
def get_items():
    products = Product.query.all()

    result = []
    for item in products:
        itemData = {'name': item.name, "description": item.description}
        result.append(itemData)
    return {'products': result}

@app.route('/items/<id>')
def get_item(id):
    product = Product.query.get_or_404(id)
    return {"name": product.name, "description": product.description}

@app.route('/items', methods=['POST'])
def add_item():
    product = Product(name=request.json['name'], description=request.json['description'])
    db.session.add(product)
    db.session.commit()
    return {'id', product.id}

