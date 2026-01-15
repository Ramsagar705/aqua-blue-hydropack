# Aqua Blue - Water Delivery Service Website

A modern, responsive water delivery service website similar to onlinepaniwala.in. Built with HTML, CSS, JavaScript, and Flask backend.

## 🌊 Features

- **Modern & Responsive Design**: Clean, professional UI with blue & white theme
- **Mobile-Friendly**: Fully responsive layout that works on all devices
- **Fast Delivery**: Same-day delivery options
- **Multiple Services**: 
  - 20 Litre Water Jar
  - Bottled Drinking Water
  - Bulk Water Supply
  - Office & Commercial Supply
- **Easy Ordering**: Simple order form with validation
- **Contact System**: Contact form for customer inquiries
- **WhatsApp Integration**: Quick order via WhatsApp
- **Click-to-Call**: Direct phone call functionality
- **Admin Panel**: View and manage orders (optional)
- **Email Notifications**: Automatic email alerts on order submission (optional)

## 📁 Project Structure

```
aqua-blue/
│
├── index.html          # Home page
├── about.html          # About Us page
├── services.html       # Services/Products page
├── order.html         # Order Water page
├── contact.html       # Contact Us page
│
├── css/
│   └── style.css      # Main stylesheet
│
├── js/
│   ├── main.js        # Main JavaScript (navigation, animations)
│   ├── order.js       # Order form handling
│   └── contact.js     # Contact form handling
│
├── app.py             # Flask backend application
├── requirements.txt   # Python dependencies
├── aqua_blue.db       # SQLite database (created automatically)
│
└── templates/
    └── admin.html     # Admin panel (optional)
```

## 🚀 Getting Started

### Option 1: Frontend Only (Static Website)

1. Simply open `index.html` in your web browser
2. All pages are linked and functional without a backend
3. Forms will save to browser's localStorage

### Option 2: With Flask Backend

1. **Install Python** (3.7 or higher)

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Flask application**:
   ```bash
   python app.py
   ```

4. **Access the website**:
   - Open your browser and go to: `http://localhost:5000`
   - Admin panel: `http://localhost:5000/admin`

## ⚙️ Configuration

### Email Notifications (Optional)

To enable email notifications, set these environment variables:

```bash
export SMTP_SERVER=smtp.gmail.com
export SMTP_PORT=587
export SMTP_USER=your-email@gmail.com
export SMTP_PASSWORD=your-app-password
export ADMIN_EMAIL=admin@aquablue.in
```

Or create a `.env` file (not included in repo for security).

### Phone Numbers & Contact Info

Update the following in HTML files:
- Phone numbers: Search for `+919876543210` and replace with your number
- Email addresses: Search for `info@aquablue.in` and replace
- Address: Update in contact.html and footer sections
- WhatsApp link: Update in WhatsApp float button

## 📱 Pages Overview

### Home Page (`index.html`)
- Hero section with call-to-action
- Service highlights
- How it works section
- Services preview

### About Us (`about.html`)
- Company information
- Values and mission
- Why choose us section

### Services (`services.html`)
- Detailed service descriptions
- Pricing information
- Service benefits

### Order Water (`order.html`)
- Order form with validation
- Product selection
- Delivery date/time selection
- Success message with order ID

### Contact Us (`contact.html`)
- Contact information
- Contact form
- Social media links

## 🎨 Design Features

- **Color Scheme**: Blue (#0066cc) and white theme
- **Typography**: Modern, clean fonts (Segoe UI)
- **Animations**: Smooth fade-in and hover effects
- **Icons**: Font Awesome icons throughout
- **Responsive**: Mobile-first design approach

## 🔧 Customization

### Change Colors

Edit CSS variables in `css/style.css`:
```css
:root {
    --primary-blue: #0066cc;
    --dark-blue: #004499;
    --light-blue: #3399ff;
    --accent-blue: #00aaff;
}
```

### Add New Services

1. Add service card in `services.html`
2. Add option in order form dropdown
3. Update service details as needed

## 📊 Database Schema

### Orders Table
- id (Primary Key)
- name, mobile, email
- address
- product_type, quantity
- delivery_time, delivery_date
- notes
- status (pending/confirmed/delivered)
- created_at

### Contact Messages Table
- id (Primary Key)
- name, email, phone
- subject, message
- created_at

## 🌐 Deployment

### Static Hosting (Frontend Only)
- Upload all HTML, CSS, and JS files to any static hosting service
- Examples: Netlify, Vercel, GitHub Pages, AWS S3

### Full Stack Deployment
- Deploy Flask app to: Heroku, AWS, DigitalOcean, etc.
- Set up database (SQLite for small scale, PostgreSQL for production)
- Configure environment variables
- Set up domain and SSL certificate

## 📝 License

This project is open source and available for use.

## 🤝 Support

For support, email info@aquablue.in or call +91 98765 43210

## 🎯 Future Enhancements

- User authentication and accounts
- Payment gateway integration
- Order tracking system
- Subscription plans
- Mobile app
- SMS notifications
- Advanced admin features

---

**Built with ❤️ for Aqua Blue Water Delivery Service**

