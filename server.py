from flask import Flask, render_template, request, redirect, url_for, flash,  session, jsonify
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database configuration
db ={
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'project'
}

# Connect to the database
def connect_db():
    try:
        connection = mysql.connector.connect(**db)
        return connection
    except mysql.connector.Error as e:
        print("Error connecting to MySQL database:", e)
        return None
    


@app.route('/')
def login_form():
    if 'username' in session:
        user_details = {
            'username': session.get('username'),
            'name': session.get('name'),
            'phone': session.get('phone'),
            'address': session.get('address'),
            'gender': session.get('gender'),
            'mail': session.get('mail')
        }
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = connect_db()
        if conn:
            cursor = conn.cursor(dictionary=True)
            try:
                query = "SELECT * FROM register WHERE username = %s AND password = %s"
                cursor.execute(query, (username, password))
                user = cursor.fetchone()
                
                if user:
                    session['username'] = user['username']  # Store the username in the session
                    session['name'] = user['name']
                    session['phone'] = user['phone']
                    session['address'] = user['address']
                    session['gender'] = user['gender']
                    session['mail'] = user['mail']
                    flash('Login successful!', 'success')
                    return redirect(url_for('index'))
                else:
                    flash('No such username or wrong password!', 'error')
                    return redirect(url_for('login'))
            except mysql.connector.Error as e:
                print("Error executing query:", e)
                flash('An error occurred. Please try again later.', 'error')
                return redirect(url_for('login'))
            finally:
                cursor.close()
                conn.close()
        else:
            flash('Failed to connect to the database. Please try again later.', 'error')
            return redirect(url_for('login'))
    else:
        return render_template('login.html')
@app.route('/seller_loginprocess', methods=['POST'])
def seller_loginprocess():

        shopid = request.form['shopid']
        password = request.form['password']
        print(shopid,'////////////////////////////////////////')
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                query = "SELECT * FROM seller WHERE shopid = %s AND password = %s"
                cursor.execute(query, (shopid, password))
                user = cursor.fetchone()
                
                if user:
                    session['shopid'] = shopid  # Store the username in the session
                    return redirect(url_for('seller_index'))
                else:
                    flash('No such username or wrong password!', 'error')
                    return redirect(url_for('seller_login'))
            except mysql.connector.Error as e:
                print("Error executing query:", e)
                flash('An error occurred. Please try again later.', 'error')
                return redirect(url_for('seller_login'))
            finally:
                cursor.close()
                conn.close()
        else:
            flash('Failed to connect to the database. Please try again later.', 'error')
            return redirect(url_for('seller_login'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        gender = request.form['gender']
        address = request.form['address']
        mail = request.form['mail']
        username = request.form['user']
        password = request.form['password']
        
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                insert_query = "INSERT INTO register (name, phone, gender, address, mail, username, password) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(insert_query, (name, phone, gender, address, mail, username, password))
                conn.commit()
                flash('Signup successful!', 'success')
                return redirect(url_for('login_form'))
            except mysql.connector.Error as e:
                print("Error executing query:", e)
                flash('An error occurred. Please try again later.', 'error')
                return redirect(url_for('signup'))
            finally:
                cursor.close()
                conn.close()
        else:
            flash('Failed to connect to the database. Please try again later.', 'error')
            return redirect(url_for('signup'))
    
    return render_template('signup.html')

@app.route('/seller', methods=['GET', 'POST'])
def seller():
    if request.method == 'POST':
        shopname = request.form['shopname']
        sellername = request.form['sellername']
        phone = request.form['phone']
        address = request.form['address']
        category = request.form['category']
        shopid = request.form['shopid']
        
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                insert_query = "INSERT INTO seller (shopname, sellername, phone, address, category, shopid) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(insert_query, (shopname, sellername, phone, address, category, shopid))
                conn.commit()
                flash('Register successful!', 'success')
                return redirect(url_for('seller_index'))
            except mysql.connector.Error as e:
                print("Error executing query:", e)
                flash('An error occurred. Please try again later.', 'error')
                return redirect(url_for('seller'))
            finally:
                cursor.close()
                conn.close()
        else:
            flash('Failed to connect to the database. Please try again later.', 'error')
            return redirect(url_for('seller'))
    
    return render_template('seller.html')

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                query = "SELECT * FROM register WHERE mail = %s"
                cursor.execute(query, (email,))
                user = cursor.fetchone()
                
                if user:
                    # Allow user to reset password
                    return render_template('reset_password.html', email=email)
                else:
                    flash('Email not found!', 'error')
                    return redirect(url_for('forgot_password'))
            except mysql.connector.Error as e:
                print("Error executing query:", e)
                flash('An error occurred. Please try again later.', 'error')
                return redirect(url_for('forgot_password'))
            finally:
                cursor.close()
                conn.close()
        else:
            flash('Failed to connect to the database. Please try again later.', 'error')
            return redirect(url_for('forgot_password'))
    
    return render_template('forgot_password.html')

@app.route('/reset-password', methods=['POST'])
def reset_password():
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']

    if password != confirm_password:
        flash('Passwords do not match!', 'error')
        return redirect(url_for('forgot_password'))

    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            update_query = "UPDATE register SET password = %s WHERE mail = %s"
            cursor.execute(update_query, (password, email))
            conn.commit()
            flash('Password updated successfully!', 'success')
            return redirect(url_for('login_form'))
        except mysql.connector.Error as e:
            print("Error executing query:", e)
            flash('An error occurred. Please try again later.', 'error')
            return redirect(url_for('forgot_password'))
        finally:
            cursor.close()
            conn.close()
    else:
        flash('Failed to connect to the database. Please try again later.', 'error')
        return redirect(url_for('forgot_password'))

@app.route('/index')
def index():
    return render_template('index.html')

# Function to query database for seller details based on category
def query_database(category):
    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM seller WHERE category = %s"
            cursor.execute(query, (category,))
            details = cursor.fetchall()
            cursor.close()
            conn.close()
            return details
        else:
            return None
    except mysql.connector.Error as error:
        print("Error while querying database:", error)
        return None

# Route to handle POST request for fetching details based on category
@app.route('/get_details', methods=['POST'])
def get_details():
    data = request.json
    category = data.get('category')

    if not category:
        flash("No category provided", "error")
        return redirect(url_for('details_page'))

    details = query_database(category)
    if details:
        return render_template('category.html', categories=details)
    else:
        flash("Error fetching details from the database", "error")
        return redirect(url_for('details_page'))

# Route to display details page based on category
@app.route('/details_page')
def details_page():
    category = request.args.get('category')
    print(category,"-------------------------------------------------")
    if not category:
        flash("No category provided", "error")
        return redirect(url_for('index'))

    details = query_database(category)
    if details:
        return render_template('category.html', categories=details)
    else:
        flash("Error fetching details from the database", "error")
        return redirect(url_for('index'))

@app.route('/profile', methods=['GET', 'POST'])
def profile_page():
    # Check if the user is logged in
    if 'username' in session:
        username = session['username']
        if request.method == 'POST':
            # Retrieve updated profile information from the form
            name = request.form['name']
            phone = request.form['phone']
            gender = request.form['gender']
            address = request.form['address']
            mail = request.form['mail']
            # Update the database with the new information
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                try:
                    update_query = "UPDATE register SET name = %s, phone = %s, gender = %s, address = %s, mail = %s WHERE username = %s"
                    cursor.execute(update_query, (name, phone, gender, address, mail, username))
                    conn.commit()
                    flash('Profile updated successfully!', 'success')
                except mysql.connector.Error as e:
                    print("Error updating profile:", e)
                    flash('Failed to update profile', 'error')
                finally:
                    cursor.close()
                    conn.close()
        # Fetch user details from the database
        user_details = fetch_user_details(username)
        if user_details:
            return render_template('profile.html', user_details=user_details)
        else:
            flash('Failed to fetch user details', 'error')
            return redirect(url_for('index'))
    else:
        flash('You must log in first', 'error')
        return redirect(url_for('login_form'))

@app.route('/sellerprofile', methods=['GET', 'POST'])
def sellerprofile_page():
    # Check if the user is logged in
    if 'username' in session:
        shopid = session['shopid']
        if request.method == 'POST':
            # Retrieve updated profile information from the form
            shopname = request.form['shopname']
            phone = request.form['phone']
            address = request.form['address']
            mail = request.form['mail']
            # Update the database with the new information
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                try:
                    update_query = "UPDATE register SET name = %s, phone = %s, gender = %s, address = %s, mail = %s WHERE username = %s"
                    cursor.execute(update_query, (shopname, phone, address, mail, shopid))
                    conn.commit()
                    flash('Profile updated successfully!', 'success')
                except mysql.connector.Error as e:
                    print("Error updating profile:", e)
                    flash('Failed to update profile', 'error')
                finally:
                    cursor.close()
                    conn.close()
        # Fetch user details from the database
        user_details = fetch_user_details(shopid)
        if user_details:
            return render_template('profile.html', user_details=user_details)
        else:
            flash('Failed to fetch user details', 'error')
            return redirect(url_for('index'))
    else:
        flash('You must log in first', 'error')
        return redirect(url_for('login_form'))
    

# Function to fetch user details from the database based on the username
def fetch_user_details(username):
    conn = connect_db()
    if conn:
        cursor = conn.cursor(dictionary=True)
        try:
            query = "SELECT * FROM register WHERE username = %s"
            cursor.execute(query, (username,))
            user_details = cursor.fetchone()
            return user_details
        except mysql.connector.Error as e:
            print("Error fetching user details:", e)
            return None
        finally:
            cursor.close()
            conn.close()
    else:
        return None

@app.route('/logout')
def logout():
    # Clear user data from session
    session.pop('username', None)
    session.pop('name', None)
    session.pop('phone', None)
    session.pop('address', None)
    session.pop('gender', None)
    session.pop('mail', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

@app.route('/forgot')
def forgot():
     return render_template('forgot_password.html')

@app.route('/shop')
def shop():
     return render_template('shop.html')

@app.route('/shop_detail')
def shop_detail():
     return render_template('shop_detail.html')

@app.route('/cart')
def cart():
     return render_template('cart.html')

@app.route('/testimonial')
def testimonial():
     return render_template('testimonial.html')

@app.route('/contact')
def contact():
     return render_template('contact.html')

@app.route('/seller_index')
def seller_index():
     return render_template('seller_index.html')

@app.route('/seller_login')
def seller_login():
     return render_template('seller_login.html')

@app.route('/orders')
def order():
     orderDetails = fetch_orders()
     print(orderDetails,'++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
     return render_template('order.html',orderDetails=orderDetails)

@app.route('/cus_order')
def cus_order():
     orderDetails = fetch_orders()
     print(orderDetails,'++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
     return render_template('cus_order.html',orderDetails=orderDetails)

@app.route('/get_products', methods=['POST'])
def get_products():
    # Extract shopname from the form data
    shopname = request.form.get('shopname')

    # Fetch products from the database based on shopname
    products = fetch_products_and_quantity_and_prices_from_database(shopname)

    # Render HTML page with products
    if products is None:
        return jsonify({'error': 'No products found for this shop'})
    else:
        return render_template('products.html', products=products)

# Function to fetch products and prices from the database based on shop name
def fetch_products_and_quantity_and_prices_from_database(shopname):
    conn = connect_db()
    if conn:
        cursor = conn.cursor(dictionary=True)  # Returns results as dictionaries
        try:
            query = "SELECT * FROM products WHERE shopname = %s"
            cursor.execute(query, (shopname,))
            products = cursor.fetchall()
            return products  # Returns a list of dictionaries
        except mysql.connector.Error as e:
            print("Error fetching products from database:", e)
            return None
        finally:
            cursor.close()
            conn.close()
    else:
        return None
    
def fetch_orders():
    shopid = session.get('shopid')
    print(shopid,'*********************************')
    conn = connect_db()
    if conn:
        cursor = conn.cursor(dictionary=True)  # Returns results as dictionaries
        try:
            query = "SELECT * FROM `order` WHERE shopid = %s"
            cursor.execute(query, (shopid,))
            products = cursor.fetchall()
            print(products,'----------------------------')
            return products  # Returns a list of dictionaries
        except mysql.connector.Error as e:
            print("Error fetching products from database:", e)
            return None
        finally:
            cursor.close()
            conn.close()
    else:
        return None
    


@app.route('/order', methods=['POST'])
def place_order():
    username = session.get('username')
    name = session.get('name')
    phone = session.get('phone')
    address = session.get('address')
    product = request.form['product']
    quantity = request.form['quantity']
    price = request.form['price']
    shopname = request.form['shop']
    shopid = request.form['shopid']
    print(username, name, phone, address, shopname, shopid, product, quantity, price)

    try:
        # Connect to MySQL
        conn = mysql.connector.connect(**db)
        cursor = conn.cursor()

        # Execute INSERT query
        query = "INSERT INTO `order` (username, name, phone, address, shopname, shopid, product, quantity, price) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (username, name, phone, address, shopname, shopid, product, quantity, price))

        # Commit the transaction
        conn.commit()

        # Close the cursor and connection
        cursor.close()
        conn.close()

        # Return a success response
        return jsonify({'success': True})

    except mysql.connector.Error as err:
        # Handle MySQL errors
        print("MySQL Error:", err)
        return jsonify({'error': str(err)})
    
@app.route('/deliver_order', methods=['POST'])
def deliver_order():
    data = request.json
    order_id = data.get('order_id')
    print(order_id)
    conn = mysql.connector.connect(**db)
    cursor = conn.cursor()

    # Update the order status to "Delivered"
    cursor.execute("UPDATE `order` SET status = 'Delivered' WHERE id = %s", (order_id,))
    conn.commit()

    return jsonify({'message': 'Order marked as delivered successfully'})

@app.route('/cancel_order', methods=['POST'])
def cancel_order():
    data = request.json
    order_id = data.get('order_id')
    print(order_id)
    conn = mysql.connector.connect(**db)
    cursor = conn.cursor()

    # Update the order status to "Canceled"
    cursor.execute("UPDATE `order` SET status = 'Canceled' WHERE id = %s", (order_id,))
    conn.commit()

    return jsonify({'message': 'Order Canceled'})

# Route for adding a product
@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        # Retrieve form data
        productName = request.form['productName']
        productPrice = request.form['productPrice']
        productquantity = request.form['productquantity']

        # Retrieve shopid and shopname from session
        shopid = session.get('shopid')  # Use session.get() to avoid KeyError if 'shopid' is not set
        shopname = session.get('shopname')

        # Ensure shopid and shopname are available in the session
        if shopid is None or shopname is None:
            flash('Shop information not available. Please log in first.', 'error')
            return redirect(url_for('login'))

        # Connect to the database
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                # Insert product into the database
                insert_query = "INSERT INTO products (shopid, shopname, product, price, quantity) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(insert_query, (shopid, shopname, productName, productPrice, productquantity))
                conn.commit()
                flash('Product added successfully!', 'success')
                return redirect(url_for('product_list'))  # Redirect to a product list page or any other page
            except mysql.connector.Error as e:
                print("Error executing query:", e)
                flash('An error occurred while adding the product. Please try again later.', 'error')
                return redirect(url_for('add_product'))
            finally:
                cursor.close()
                conn.close()
        else:
            flash('Failed to connect to the database. Please try again later.', 'error')
            return redirect(url_for('add_product'))

    return render_template('add_product.html')


if __name__ == '__main__':
    app.run(debug=True)
