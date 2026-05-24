import json
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'bananaleclerc'

def load_data():
    with open('data/flowers.json') as file:
        flowers = json.load(file)

    with open('data/addons.json') as file:
        addons = json.load(file)

    return flowers, addons

@app.route('/')
def index():
    flowers, addons = load_data()
    return render_template('index.html', flowers=flowers, addons=addons)

# add selected flower to shopping cart
@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    flower = request.form['flower'] # get the selected flower name
    quantity = int(request.form['quantity']) #convert the quantity request to an integer
    flowers, addons = load_data() # get the flower data from file (ignoring addon data)
    cart = session.get('cart', {}) # get cart from session or start afresh

    if flower not in flowers:
        flash("Invalid Flower Selected")
        return redirect(url_for('index'))

    if flower in cart:
        cart[flower] ['quantity'] += quantity
    else:
        cart[flower] = {
            'price': flowers[flower] ['price'],
            'quantity': quantity
        }

    session['cart'] = cart
    session.modified = True
    flash(f"{quantity} {flower}(s) added to cart.")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)