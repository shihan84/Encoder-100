# 🔥 Firebase License & Subscription System

## 📋 **Why Firebase is Perfect for This**

### **Advantages:**
✅ **No server code needed** - Firebase handles everything  
✅ **Built-in authentication** - User management included  
✅ **Real-time database** - Firestore updates instantly  
✅ **Cloud Functions** - Serverless automation  
✅ **Free tier available** - Cost-effective  
✅ **Scalable** - Handles millions of users  

---

## 🏗️ **Architecture with Firebase**

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│   User App  │─────────>│   Firebase  │─────────>│    Stripe   │
│  (IBE-100)  │         │   (Cloud)   │         │  (Payment)  │
└─────────────┘         └─────────────┘         └─────────────┘
        │                       │                       │
        │                       │                       │
        v                       v                       v
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│ License File│         │   Firestore │         │  Webhook    │
│  (Local)    │         │  Database   │         │  Trigger    │
└─────────────┘         └─────────────┘         └─────────────┘
```

---

## 🎯 **Components We'll Use**

1. **Firebase Authentication** - User login/registration
2. **Firestore Database** - Store licenses and subscriptions
3. **Cloud Functions** - Automatic license validation
4. **Stripe Extension** - Payment processing (optional)

---

## 📦 **Step 1: Set Up Firebase Project**

### **Create Firebase Project:**

1. Go to https://console.firebase.google.com
2. Create new project: "IBE-100 Licenses"
3. Enable these services:
   - ✅ Authentication
   - ✅ Firestore Database
   - ✅ Cloud Functions
   - ✅ Hosting (optional)

### **Install Firebase Tools:**

```bash
npm install -g firebase-tools
firebase login
firebase init
```

---

## 💻 **Step 2: Database Schema (Firestore)**

### **Collections Structure:**

```
users/
  └── {userId}/
      ├── email: string
      ├── tier: 'trial' | 'professional' | 'enterprise'
      ├── license_key: string
      ├── activated_at: timestamp
      ├── expires_at: timestamp
      └── status: 'active' | 'expired' | 'cancelled'

licenses/
  └── {licenseKey}/
      ├── user_id: string
      ├── tier: string
      ├── created_at: timestamp
      ├── expires_at: timestamp
      └── hardware_id: string (optional)

subscriptions/
  └── {userId}/
      ├── stripe_subscription_id: string
      ├── status: string
      ├── next_payment: timestamp
      └── plan: string
```

---

## 🔧 **Step 3: Python Client Implementation**

Create `firebase_license_manager.py`:

```python
import firebase_admin
from firebase_admin import credentials, firestore, auth
import requests
from datetime import datetime, timedelta
import json
from pathlib import Path

class FirebaseLicenseManager:
    """License manager using Firebase backend"""
    
    def __init__(self):
        self.license_file = Path("license.json")
        self.db = None
        self.user_id = None
        
        # Initialize Firebase
        self.init_firebase()
        
    def init_firebase(self):
        """Initialize Firebase Admin SDK"""
        try:
            # Load service account key
            if not firebase_admin._apps:
                cred_path = "firebase_service_account.json"
                if not Path(cred_path).exists():
                    # Create from config
                    self.create_service_account_config()
                
                cred = credentials.Certificate(cred_path)
                firebase_admin.initialize_app(cred)
            
            self.db = firestore.client()
            print("[INFO] Firebase initialized successfully")
        except Exception as e:
            print(f"[ERROR] Firebase initialization failed: {e}")
    
    def create_service_account_config(self):
        """Create service account file from config"""
        config = {
            "type": "service_account",
            "project_id": "your-project-id",
            "private_key_id": "your-key-id",
            "private_key": "your-private-key",
            "client_email": "your-service-account@project.iam.gserviceaccount.com",
            "client_id": "your-client-id",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token"
        }
        
        with open("firebase_service_account.json", 'w') as f:
            json.dump(config, f)
    
    def validate_license(self, license_key):
        """Validate license against Firebase"""
        try:
            # Get license from Firestore
            license_ref = self.db.collection('licenses').document(license_key)
            license_doc = license_ref.get()
            
            if not license_doc.exists:
                return False, "License not found"
            
            license_data = license_doc.to_dict()
            
            # Check expiry
            expires_at = license_data.get('expires_at')
            if expires_at:
                if datetime.now() > expires_at:
                    return False, "License expired"
            
            # Check status
            user_id = license_data.get('user_id')
            user_ref = self.db.collection('users').document(user_id)
            user_doc = user_ref.get()
            
            if user_doc.exists:
                user_data = user_doc.to_dict()
                status = user_data.get('status')
                
                if status != 'active':
                    return False, f"License {status}"
            
            return True, "Valid license"
            
        except Exception as e:
            print(f"[ERROR] License validation error: {e}")
            return False, str(e)
    
    def activate_license(self, license_key, user_email, password):
        """Activate license with user credentials"""
        try:
            # Authenticate user
            user = auth.create_user(
                email=user_email,
                password=password
            )
            
            # Get license from Firestore
            license_ref = self.db.collection('licenses').document(license_key)
            license_doc = license_ref.get()
            
            if not license_doc.exists:
                return False, "Invalid license key"
            
            license_data = license_doc.to_dict()
            
            # Update license with user info
            license_ref.update({
                'user_id': user.uid,
                'activated_at': datetime.now(),
                'status': 'active'
            })
            
            # Create user document
            user_ref = self.db.collection('users').document(user.uid)
            user_ref.set({
                'email': user_email,
                'license_key': license_key,
                'tier': license_data.get('tier', 'professional'),
                'activated_at': datetime.now(),
                'expires_at': datetime.now() + timedelta(days=30),  # Monthly
                'status': 'active'
            })
            
            # Save to local file
            self.save_local_license(user.uid, license_key)
            
            return True, "License activated"
            
        except Exception as e:
            print(f"[ERROR] License activation error: {e}")
            return False, str(e)
    
    def save_local_license(self, user_id, license_key):
        """Save license to local file"""
        self.user_id = user_id
        
        license_data = {
            'user_id': user_id,
            'license_key': license_key,
            'activated': datetime.now().isoformat()
        }
        
        with open(self.license_file, 'w') as f:
            json.dump(license_data, f)
    
    def check_license_status(self):
        """Check license status from Firebase"""
        if not self.user_id:
            self.load_local_license()
        
        if not self.user_id:
            return False
        
        try:
            user_ref = self.db.collection('users').document(self.user_id)
            user_doc = user_ref.get()
            
            if not user_doc.exists:
                return False
            
            user_data = user_doc.to_dict()
            
            # Check expiry
            expires_at = user_data.get('expires_at')
            if expires_at and datetime.now() > expires_at:
                return False
            
            # Check status
            status = user_data.get('status')
            if status != 'active':
                return False
            
            return True
            
        except Exception as e:
            print(f"[ERROR] License check error: {e}")
            return False
    
    def load_local_license(self):
        """Load license from local file"""
        if not self.license_file.exists():
            return False
        
        try:
            with open(self.license_file, 'r') as f:
                data = json.load(f)
                self.user_id = data.get('user_id')
                return True
        except:
            return False
    
    def get_remaining_days(self):
        """Get days until expiry"""
        if not self.user_id:
            return 0
        
        try:
            user_ref = self.db.collection('users').document(self.user_id)
            user_doc = user_ref.get()
            
            if not user_doc.exists:
                return 0
            
            user_data = user_doc.to_dict()
            expires_at = user_data.get('expires_at')
            
            if not expires_at:
                return 0
            
            if isinstance(expires_at, str):
                expires_at = datetime.fromisoformat(expires_at)
            
            remaining = expires_at - datetime.now()
            return max(0, remaining.days)
            
        except:
            return 0
```

---

## ☁️ **Step 4: Cloud Functions (Automation)**

Create `functions/index.js`:

```javascript
const functions = require('firebase-functions');
const admin = require('firebase-admin');
admin.initializeApp();

// Auto-expire licenses
exports.checkExpiredLicenses = functions.pubsub
    .schedule('every 1 hours')
    .onRun(async (context) => {
        const db = admin.firestore();
        const now = new Date();
        
        // Get all active licenses
        const usersSnapshot = await db.collection('users')
            .where('status', '==', 'active')
            .get();
        
        const batch = db.batch();
        
        usersSnapshot.forEach(doc => {
            const data = doc.data();
            const expiresAt = data.expires_at.toDate();
            
            if (expiresAt < now) {
                batch.update(doc.ref, { status: 'expired' });
                console.log(`Expired license: ${doc.id}`);
            }
        });
        
        await batch.commit();
        console.log('Expired licenses updated');
    });

// Send renewal reminders
exports.sendRenewalReminders = functions.pubsub
    .schedule('every 24 hours')
    .onRun(async (context) => {
        const db = admin.firestore();
        const in7Days = new Date();
        in7Days.setDate(in7Days.getDate() + 7);
        
        const usersSnapshot = await db.collection('users')
            .where('expires_at', '<=', in7Days)
            .where('status', '==', 'active')
            .get();
        
        // Send email reminders
        usersSnapshot.forEach(async (doc) => {
            const data = doc.data();
            // Send email using SendGrid, etc.
            console.log(`Sending renewal reminder to: ${data.email}`);
        });
    });
```

---

## 🔐 **Step 5: Integrate with App**

Add to `main.py`:

```python
from firebase_license_manager import FirebaseLicenseManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Initialize Firebase license manager
        self.license_manager = FirebaseLicenseManager()
        
        # Check license
        if not self.check_license():
            self.show_license_dialog()
            return
        
        self.setup_ui()
        self.setup_connections()
        
        # Add license status to UI
        self.update_license_status()
    
    def check_license(self):
        """Check if license is valid"""
        return self.license_manager.check_license_status()
    
    def update_license_status(self):
        """Update license status in UI"""
        days_left = self.license_manager.get_remaining_days()
        
        if days_left < 7:
            # Show warning
            self.statusBar().showMessage(
                f"⚠️ License expires in {days_left} days. Please renew.",
                30000
            )
    
    def show_license_dialog(self):
        """Show license activation dialog"""
        from PyQt6.QtWidgets import (
            QDialog, QVBoxLayout, QLineEdit, QPushButton, 
            QLabel, QMessageBox
        )
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Activate License")
        dialog.setFixedSize(450, 400)
        
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Activate Your License")
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        # Info
        info = QLabel(
            "Enter your license key and account details to activate IBE-100"
        )
        layout.addWidget(info)
        
        # License key
        layout.addWidget(QLabel("License Key:"))
        license_input = QLineEdit()
        license_input.setPlaceholderText("Enter your 32-character license key")
        layout.addWidget(license_input)
        
        # Email
        layout.addWidget(QLabel("Email:"))
        email_input = QLineEdit()
        email_input.setPlaceholderText("your.email@example.com")
        layout.addWidget(email_input)
        
        # Password
        layout.addWidget(QLabel("Password:"))
        password_input = QLineEdit()
        password_input.setEchoMode(QLineEdit.EchoMode.Password)
        password_input.setPlaceholderText("Create a password")
        layout.addWidget(password_input)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        activate_btn = QPushButton("Activate")
        activate_btn.clicked.connect(
            lambda: self.activate_license(
                license_input.text(),
                email_input.text(),
                password_input.text()
            )
        )
        btn_layout.addWidget(activate_btn)
        
        purchase_btn = QPushButton("Purchase License")
        purchase_btn.clicked.connect(self.open_purchase_page)
        btn_layout.addWidget(purchase_btn)
        
        layout.addLayout(btn_layout)
        
        # Status
        self.license_status_label = QLabel("")
        layout.addWidget(self.license_status_label)
        
        dialog.setLayout(layout)
        dialog.exec()
    
    def activate_license(self, key, email, password):
        """Activate license"""
        if not all([key, email, password]):
            self.license_status_label.setText(
                "⚠️ Please fill all fields"
            )
            return
        
        success, message = self.license_manager.activate_license(
            key, email, password
        )
        
        if success:
            self.license_status_label.setText("✅ " + message)
            self.license_status_label.setStyleSheet("color: green;")
            QTimer.singleShot(2000, lambda: (self.close(), self.__init__()))
        else:
            self.license_status_label.setText("❌ " + message)
            self.license_status_label.setStyleSheet("color: red;")
```

---

## 💳 **Step 6: Payment Integration (Optional)**

### **Firebase + Stripe Extension:**

1. Install Stripe extension in Firebase Console
2. It automatically handles:
   - Payment processing
   - Subscription management
   - License creation on payment

### **Or Use Cloud Functions:**

```javascript
exports.createStripeSubscription = functions.https.onCall(async (data, context) => {
    const stripe = require('stripe')(functions.config().stripe.secret);
    
    const session = await stripe.checkout.sessions.create({
        payment_method_types: ['card'],
        line_items: [{
            price: 'price_your_professional_monthly',
            quantity: 1,
        }],
        mode: 'subscription',
        success_url: 'https://yourapp.com/success',
        cancel_url: 'https://yourapp.com/cancel',
        metadata: {
            user_id: context.auth.uid
        }
    });
    
    return { sessionId: session.id };
});
```

---

## 🎯 **Advantages of Firebase Approach**

### **✅ Pros:**
1. **No server management** - Firebase handles everything
2. **Real-time updates** - License status updates instantly
3. **Automatic scaling** - Handles any number of users
4. **Built-in security** - Firebase security rules
5. **Cloud Functions** - Automate renewal, expiry, reminders
6. **Free tier** - Generous free usage
7. **Easy integration** - Just Firebase SDK

### **⚠️ Cons:**
1. **Requires internet** - Can't work offline
2. **Firebase dependency** - Vendor lock-in
3. **Setup time** - Initial configuration needed
4. **Cost scaling** - Costs increase with usage

---

## 📦 **Required Packages**

```bash
pip install firebase-admin
```

Add to `requirements.txt`:
```
firebase-admin==6.0.0
```

---

## ✅ **Implementation Checklist**

- [ ] Create Firebase project
- [ ] Set up Firestore database
- [ ] Enable Authentication
- [ ] Create Cloud Functions
- [ ] Create `firebase_license_manager.py`
- [ ] Add to `main.py`
- [ ] Create activation dialog
- [ ] Test activation flow
- [ ] Test validation flow
- [ ] Set up Stripe (optional)
- [ ] Deploy Cloud Functions
- [ ] Test end-to-end

---

## 💰 **Cost Estimate**

### **Firebase Free Tier (Spark):**
- Firestore: 50k reads/day, 20k writes/day
- Cloud Functions: 125k invocations/month
- Authentication: Free (unlimited)

### **Typical Monthly Cost:**
- **< 100 users**: $0 (free tier)
- **100-1000 users**: $10-20/month
- **1000+ users**: $20-50/month

---

**Would you like me to implement the complete Firebase license system?**

