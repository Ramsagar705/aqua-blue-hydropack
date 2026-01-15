# Quick Setup Guide - Aqua Blue

## 🚀 Quick Start (5 minutes)

### Method 1: Static Website (No Backend)

1. Open `index.html` in your web browser
2. That's it! All pages work without a server
3. Forms save to browser's localStorage

### Method 2: With Backend (Full Features)

1. **Install Python 3.7+** if not already installed
   - Download from: https://www.python.org/downloads/

2. **Open terminal/command prompt** in the project folder

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the server**:
   ```bash
   python app.py
   ```
   Or double-click `run.bat` (Windows) or `run.sh` (Mac/Linux)

5. **Open browser** and visit:
   - Website: http://localhost:5000
   - Admin Panel: http://localhost:5000/admin

## 📝 Before Going Live

### Update Contact Information

1. **Phone Numbers**: 
   - Search for `+919876543210` in all HTML files
   - Replace with your actual phone number

2. **Email Addresses**:
   - Search for `info@aquablue.in` and `support@aquablue.in`
   - Replace with your actual email addresses

3. **Address**:
   - Edit `contact.html` and footer sections
   - Update with your business address

4. **WhatsApp Number**:
   - In all HTML files, find: `wa.me/919876543210`
   - Replace `919876543210` with your WhatsApp number (without +)

### Configure Email (Optional)

1. Create a `.env` file in the project root:
   ```
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USER=your-email@gmail.com
   SMTP_PASSWORD=your-app-password
   ADMIN_EMAIL=admin@aquablue.in
   ```

2. For Gmail, you'll need an "App Password":
   - Go to Google Account → Security → 2-Step Verification → App Passwords
   - Generate a password for "Mail"

### Customize Branding

1. **Logo/Name**: 
   - Search for "Aqua Blue" in HTML files
   - Replace with your brand name

2. **Colors**: 
   - Edit `css/style.css`
   - Modify CSS variables in `:root` section

3. **Content**: 
   - Edit text in HTML files
   - Update service descriptions, pricing, etc.

## 🎨 Customization Tips

- **Change Colors**: Edit CSS variables in `css/style.css`
- **Add Services**: Add new service cards in `services.html`
- **Modify Forms**: Edit form fields in `order.html` and `contact.html`
- **Update Images**: Replace placeholder icons with your logo/images

## 📱 Testing

1. Test all pages load correctly
2. Test order form submission
3. Test contact form submission
4. Test mobile responsiveness
5. Test WhatsApp and call buttons
6. Check admin panel (if using backend)

## 🌐 Deployment Options

### Static Hosting (Frontend Only)
- **Netlify**: Drag and drop the folder
- **Vercel**: Connect GitHub repo
- **GitHub Pages**: Push to GitHub and enable Pages
- **AWS S3**: Upload files to S3 bucket

### Full Stack (With Backend)
- **Heroku**: Connect GitHub repo, add PostgreSQL
- **DigitalOcean**: Deploy Flask app
- **AWS EC2**: Set up EC2 instance
- **PythonAnywhere**: Upload files and run

## ❓ Troubleshooting

**Port already in use?**
- Change port in `app.py`: `app.run(port=5001)`

**Database errors?**
- Delete `aqua_blue.db` and restart server
- Database will be recreated automatically

**CSS not loading?**
- Check file paths in HTML files
- Ensure `css/style.css` exists

**Forms not submitting?**
- Check browser console for errors
- Ensure Flask server is running (for backend)
- Check network tab for API calls

## 📞 Need Help?

Check the main `README.md` for detailed documentation.

---

**Happy Launching! 🎉**

