"""
Aqua Blue - Water Delivery Service
Flask Backend Application
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, send_from_directory, send_file, make_response
from flask_cors import CORS
import sqlite3
import os
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# Disable caching for HTML files in development
@app.after_request
def add_no_cache_headers(response):
    """Add no-cache headers to prevent browser caching during development"""
    if request.endpoint and request.endpoint in ['index', 'about', 'services', 'order', 'contact']:
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
    return response

# Database configuration
DATABASE = 'aqua_blue.db'

def init_db():
    """Initialize the database with required tables"""
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    # Orders table
    c.execute('''CREATE TABLE IF NOT EXISTS orders
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  mobile TEXT NOT NULL,
                  email TEXT,
                  address TEXT NOT NULL,
                  product_type TEXT NOT NULL,
                  quantity INTEGER NOT NULL,
                  delivery_time TEXT NOT NULL,
                  delivery_date TEXT NOT NULL,
                  notes TEXT,
                  status TEXT DEFAULT 'pending',
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    # Contact messages table
    c.execute('''CREATE TABLE IF NOT EXISTS contact_messages
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  email TEXT NOT NULL,
                  phone TEXT NOT NULL,
                  subject TEXT NOT NULL,
                  message TEXT NOT NULL,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def serve_html_file(filename):
    """Serve HTML file with no caching - reads file fresh each time"""
    try:
        # Get file modification time for ETag
        file_path = os.path.join(os.getcwd(), filename)
        if os.path.exists(file_path):
            mtime = os.path.getmtime(file_path)
        else:
            mtime = datetime.now().timestamp()
        
        # Read file fresh from disk (this happens on EVERY request)
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Debug: Print when file is served (only in debug mode)
        if app.debug:
            print(f"[DEBUG] Serving {filename} - File size: {len(content)} bytes - Modified: {datetime.fromtimestamp(mtime)}")
        
        response = make_response(content)
        response.headers['Content-Type'] = 'text/html; charset=utf-8'
        # Aggressive no-cache headers
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0, private'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        response.headers['Last-Modified'] = datetime.fromtimestamp(mtime).strftime('%a, %d %b %Y %H:%M:%S GMT')
        # Use file mtime as ETag to force browser to check for updates
        response.headers['ETag'] = f'"{int(mtime)}"'
        # Prevent any proxy caching
        response.headers['X-Accel-Expires'] = '0'
        return response
    except FileNotFoundError:
        return f"File not found: {filename}", 404
    except Exception as e:
        return f"Error reading file: {str(e)}", 500

@app.route('/')
def index():
    """Serve the home page"""
    return serve_html_file('index.html')

@app.route('/about')
def about():
    """Serve the about page"""
    return serve_html_file('about.html')

@app.route('/services')
def services():
    """Serve the services page"""
    return serve_html_file('services.html')

@app.route('/order')
def order():
    """Serve the order page"""
    return serve_html_file('order.html')

@app.route('/contact')
def contact():
    """Serve the contact page"""
    return serve_html_file('contact.html')

@app.route('/contact.html')
def contact_html():
    """Serve the contact page (direct HTML access)"""
    return serve_html_file('contact.html')

@app.route('/api/orders', methods=['POST'])
def create_order():
    """Handle order submission"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'mobile', 'address', 'productType', 'quantity', 'deliveryTime', 'deliveryDate']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Insert into database
        conn = get_db_connection()
        c = conn.cursor()
        
        c.execute('''INSERT INTO orders 
                     (name, mobile, email, address, product_type, quantity, delivery_time, delivery_date, notes)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  (data['name'], data['mobile'], data.get('email', ''),
                   data['address'], data['productType'], int(data['quantity']),
                   data['deliveryTime'], data['deliveryDate'], data.get('notes', '')))
        
        order_id = c.lastrowid
        conn.commit()
        conn.close()
        
        # Generate order ID
        order_id_str = f'AQB-{order_id:08d}'
        
        # Send email notification (optional - configure SMTP settings)
        try:
            send_order_email(data, order_id_str)
        except Exception as e:
            print(f"Email sending failed: {e}")
        
        return jsonify({
            'success': True,
            'message': 'Order placed successfully',
            'order_id': order_id_str
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/contact', methods=['POST'])
def create_contact():
    """Handle contact form submission"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email', 'phone', 'subject', 'message']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Insert into database
        conn = get_db_connection()
        c = conn.cursor()
        
        c.execute('''INSERT INTO contact_messages 
                     (name, email, phone, subject, message)
                     VALUES (?, ?, ?, ?, ?)''',
                  (data['name'], data['email'], data['phone'],
                   data['subject'], data['message']))
        
        conn.commit()
        conn.close()
        
        # Send email notification (optional)
        try:
            send_contact_email(data)
        except Exception as e:
            print(f"Email sending failed: {e}")
        
        return jsonify({
            'success': True,
            'message': 'Message sent successfully'
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/admin')
def admin():
    """Admin panel to view orders and messages"""
    conn = get_db_connection()
    
    # Get orders
    orders = conn.execute('SELECT * FROM orders ORDER BY created_at DESC LIMIT 50').fetchall()
    
    # Get contact messages
    messages = conn.execute('SELECT * FROM contact_messages ORDER BY created_at DESC LIMIT 50').fetchall()
    
    conn.close()
    
    return render_template('admin.html', orders=orders, messages=messages)

@app.route('/api/orders', methods=['GET'])
def get_orders():
    """Get all orders (API endpoint)"""
    conn = get_db_connection()
    orders = conn.execute('SELECT * FROM orders ORDER BY created_at DESC').fetchall()
    conn.close()
    
    orders_list = []
    for order in orders:
        orders_list.append({
            'id': order['id'],
            'name': order['name'],
            'mobile': order['mobile'],
            'email': order['email'],
            'address': order['address'],
            'product_type': order['product_type'],
            'quantity': order['quantity'],
            'delivery_time': order['delivery_time'],
            'delivery_date': order['delivery_date'],
            'status': order['status'],
            'created_at': order['created_at']
        })
    
    return jsonify(orders_list)

def send_order_email(order_data, order_id):
    """Send email notification for new order"""
    # Configure your SMTP settings here
    # For production, use environment variables
    SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
    SMTP_USER = os.getenv('SMTP_USER', '')
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', '')
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'admin@aquablue.in')
    
    if not SMTP_USER or not SMTP_PASSWORD:
        print("SMTP credentials not configured. Skipping email.")
        return
    
    try:
        msg = MIMEMultipart()
        msg['From'] = SMTP_USER
        msg['To'] = ADMIN_EMAIL
        msg['Subject'] = f'New Order Received - {order_id}'
        
        body = f"""
        New Order Received!
        
        Order ID: {order_id}
        Name: {order_data['name']}
        Mobile: {order_data['mobile']}
        Email: {order_data.get('email', 'N/A')}
        Address: {order_data['address']}
        Product: {order_data['productType']}
        Quantity: {order_data['quantity']}
        Delivery Date: {order_data['deliveryDate']}
        Delivery Time: {order_data['deliveryTime']}
        Notes: {order_data.get('notes', 'None')}
        
        Order placed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        print(f"Order email sent successfully for {order_id}")
    except Exception as e:
        print(f"Failed to send order email: {e}")

def send_contact_email(contact_data):
    """Send email notification for contact form"""
    SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
    SMTP_USER = os.getenv('SMTP_USER', '')
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', '')
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'admin@aquablue.in')
    
    if not SMTP_USER or not SMTP_PASSWORD:
        print("SMTP credentials not configured. Skipping email.")
        return
    
    try:
        msg = MIMEMultipart()
        msg['From'] = SMTP_USER
        msg['To'] = ADMIN_EMAIL
        msg['Subject'] = f'New Contact Message - {contact_data["subject"]}'
        
        body = f"""
        New Contact Form Submission!
        
        Name: {contact_data['name']}
        Email: {contact_data['email']}
        Phone: {contact_data['phone']}
        Subject: {contact_data['subject']}
        
        Message:
        {contact_data['message']}
        
        Received at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        print("Contact email sent successfully")
    except Exception as e:
        print(f"Failed to send contact email: {e}")

if __name__ == '__main__':
    # Initialize database on startup
    init_db()
    
    print("=" * 50)
    print("Aqua Blue Server Starting...")
    print("Debug Mode: ENABLED")
    print("Auto-reload: ENABLED")
    print("Cache-busting: ENABLED")
    print("=" * 50)
    print(f"Server running at: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    print("=" * 50)
    
    # Run the application with explicit reloader
    app.run(debug=True, use_reloader=True, host='0.0.0.0', port=5000)

