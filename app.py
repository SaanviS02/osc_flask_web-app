import json
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'bananaleclerc'

def calculate_total(cart):
    total = sum(item['price'] * item['quantity'] for item in cart.values())
    return total

def load_data():
    with open('data/flowers.json') as file:
        flowers = json.load(file)

    with open('data/addons.json') as file:
        addons = json.load(file)

    return flowers, addons

# load index.html
@app.route('/')
def index():
    flowers, addons = load_data()
    cart = session.get('cart', {})
    total = calculate_total(cart)
    selected_addons = session.get('selected_addons', {})
    return render_template('index.html', flowers=flowers, addons=addons, cart=cart, total=total, selected_addons=selected_addons)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/order_history')
def order_history():
    return render_template('order_history.html')

@app.route('/invoice')
def invoices():
    return render_template('invoices.html')

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
        cart[flower] ['quantity'] += quantity #add existing quantity
    else:
        cart[flower] = {
            'price': flowers[flower] ['price'],
            'quantity': quantity
        }

    session['cart'] = cart # update session
    session.modified = True # force flask to save it
    flash(f"{quantity} {flower}(s) added to cart.")
    return redirect(url_for('index'))

# add selected add ons to the session
@app.route('/select_addon', methods=['POST'])
def select_addon():
    selected_addons = session.get('selected_addons', {}) # Get existing addons from session or start afresh
    _, addons = load_data()

    selected_keys = request.form.getlist('addons')

    if not selected_keys:
        flash("No add-ons selected")
    else:
        for addon in selected_keys:
            if addon in addons:
                selected_addons[addon] = float(addons[addon]['price'])
    
        session['selected_addons'] = selected_addons
        session.modified = True
        print(session)
        flash(f"{selected_addons} add-ons added to cart")
    return redirect(url_for('index'))

# remove an item from the shopping cart
@app.route('/remove_from_cart/<item>')
def remove_from_cart(item):
    cart = session.get('cart', {})

    if item in cart:
        del cart[item]
        session['cart'] = cart
        session.modified = True
        flash(f"Removed all {item.capitalize()} from the cart.")
    else:
        flash("Item not found in cart")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)