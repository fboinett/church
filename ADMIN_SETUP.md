# Church Platform - Admin Setup Guide

Complete step-by-step guide for administrators to install, configure, and deploy the Church Platform.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Initial Data Setup](#initial-data-setup)
5. [User & Permission Setup](#user--permission-setup)
6. [Deployment](#deployment)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### System Requirements
- **ERPNext**: v14.0 or higher
- **Frappe**: Latest version
- **Python**: 3.8+
- **Database**: MariaDB 10.3+ or PostgreSQL 10+
- **Node.js**: 14+
- **Git**: For version control

### Dependencies
```bash
# Core ERPNext setup complete
bench setup requirements
```

---

## Installation

### Step 1: Clone the App

```bash
# Navigate to your bench directory
cd /path/to/bench

# Clone the Church Platform app
git clone https://github.com/fboinett/church.git apps/church_platform

# Or if using a different repository
git clone https://github.com/your-org/church.git apps/church_platform
```

### Step 2: Install the App

```bash
# Install app into your site
bench --site your-site.local install-app church_platform

# If the site doesn't exist, create it first
bench new-site your-site.local
bench --site your-site.local install-app church_platform
```

### Step 3: Migrate the Database

```bash
# Run migrations (creates all DocTypes)
bench --site your-site.local migrate

# Reload app to register all components
bench --site your-site.local reload-doc
```

### Step 4: Install Dependencies (if any)

```bash
# Most dependencies are built into Frappe, but if needed:
pip install -r apps/church_platform/requirements.txt
```

---

## Configuration

### Step 1: Configure Global Settings

Navigate to **Setup > Global Settings** and configure:

```
Organization Name: Your Church Organization
Organization Abbreviation: CHURCH
Country: Kenya (or your country)
Timezone: Africa/Nairobi (or your timezone)
```

### Step 2: Configure App Defaults

Edit `church_platform/config.py`:

```python
# Base URL for share links (currently church.local)
BASE_URL = "https://church.yourdomain.com"

# Email configuration for notifications
NOTIFICATION_EMAIL = "admin@yourdomain.com"

# Social media share settings
SOCIAL_PLATFORMS = ['whatsapp', 'facebook', 'twitter', 'email']
```

### Step 3: Setup Email Service

Navigate to **Setup > Email Domain** and configure:

```
Domain: yourdomain.com
Email ID: noreply@yourdomain.com
SMTP Settings: Configure for your mail provider
```

### Step 4: Configure File Uploads

Navigate to **Setup > File Upload Settings**:

```
Max Upload Size: 10 MB
Allowed Extensions: jpg, jpeg, png, pdf, mp3, mp4, doc, docx
Upload Path: /files/
```

---

## Initial Data Setup

### Option A: Using Sample Data (Recommended for Demo)

```bash
# Login to your site
bench --site your-site.local console

# Then run:
from church_platform.fixtures.sample_data import create_all_fixtures
create_all_fixtures()

# This creates:
# - 1 national + 4 regional + 20 sub-regional regions
# - 120 churches
# - 50+ leaders at all levels
# - 8500+ sample members
# - Sample content and engagement data
```

### Option B: Manual Setup

#### 1. Create Hierarchy

Navigate to **Church Platform > Hierarchy > Region** and create:

**National Region**
```
Name: National Headquarters
Level: National
Country: Kenya
```

**Regional Regions** (4)
```
Name: East Africa / West Africa / etc.
Level: Regional
Parent Region: National Headquarters
```

**Sub-Regional Regions** (20)
```
Name: District names
Level: Sub-Regional
Parent Region: Regional regions (above)
```

#### 2. Create Churches

Navigate to **Church Platform > Hierarchy > Church** and create:

```
Name: Church Name
Level: Local
Parent Sub-Region: Sub-region (above)
Email: church@domain.local
Phone: +254700000000
Address: Church address
Worship Day: Sunday
Worship Time: 10:00 AM
```

---

## User & Permission Setup

### Step 1: Create National Leader

1. Navigate to **Setup > User** and create:
```
Email: archbishop@church.local
First Name: Archbishop
Last Name: Your Organization
Role: System Manager
```

2. Navigate to **Church Platform > Users > Church Leader**:
```
Name: Archbishop
User: archbishop@church.local
Level: National
Role: Archbishop
```

### Step 2: Create Regional Leaders

Repeat for each region:

1. Create **User**:
```
Email: bishop_east@church.local
First Name: Bishop
Last Name: East Africa
```

2. Create **Church Leader**:
```
Name: Bishop - East Africa
User: bishop_east@church.local
Level: Regional
Region: East Africa
Role: Bishop
```

### Step 3: Create Sub-Regional Leaders

1. Create **User**
2. Create **Church Leader** with:
```
Level: Sub-Regional
Sub-Region: District name
Role: Archdeacon
```

### Step 4: Create Local Leaders

1. Create **User**
2. Create **Church Leader** with:
```
Level: Local
Church: Church name
Role: Pastor
```

### Step 5: Create Members

1. Create **User** (optional if using portal login only)
2. Navigate to **Church Platform > Users > Member**:
```
Name: Member name
User: member@church.local
Church: Church name
Status: Active
Phone: +254700000000
Join Date: 2024-01-01
```

---

## Deployment

### For Production

#### Step 1: Setup SSL Certificate

```bash
# Using Let's Encrypt with bench
bench setup ssl yourdomain.com
```

#### Step 2: Setup Nginx

```bash
# If not already done
bench setup nginx

# Restart nginx
sudo systemctl restart nginx
```

#### Step 3: Setup Supervisor

```bash
# Setup background job processing
bench setup supervisor

# Start supervisor
sudo systemctl restart supervisor
```

#### Step 4: Configure Backups

```bash
# Setup daily backups
bench setup backups yourdomain.com

# Verify backup location
ls -la /home/frappe/frappe-bench/sites/backups/
```

#### Step 5: Performance Optimization

Edit `bench/config/common_site_config.json`:

```json
{
  "db_host": "localhost",
  "db_port": 3306,
  "redis_cache": "redis://localhost:6379/1",
  "redis_queue": "redis://localhost:6379/2",
  "redis_socketio": "redis://localhost:6379/3",
  "frappe_password": "your-password",
  "enable_scheduler": 1,
  "enable_auto_update_scheduler": 0,
  "maintenance_mode": 0
}
```

### For Development

```bash
# Start dev server
bench start

# In another terminal, watch for changes
bench watch

# Run tests
bench --site your-site.local run-tests --module church_platform
```

---

## Post-Installation Checklist

- [ ] All DocTypes installed (14 total)
- [ ] Permissions configured
- [ ] Initial hierarchy created
- [ ] National leader account created
- [ ] SSL certificate installed (production)
- [ ] Email service configured
- [ ] Backups scheduled
- [ ] Sample data loaded (if demo)
- [ ] Portal accessible at `/member-portal`
- [ ] Dashboards working for all roles

---

## Troubleshooting

### Issue: DocTypes Not Appearing

**Solution:**
```bash
# Reload all app components
bench --site your-site.local bench reload-doc
bench --site your-site.local migrate
bench --site your-site.local build
```

### Issue: Permission Denied Errors

**Solution:**
1. Check user has correct Church Leader record
2. Verify hierarchy levels match
3. Clear cache:
```bash
bench --site your-site.local clear-cache
```

### Issue: Members Cannot Access Portal

**Solution:**
1. Verify Member record exists
2. Check User has "Website User" role
3. Test portal route:
```bash
# Site must be accessible at
http://your-domain.com/member-portal
```

### Issue: Slow Dashboard Loading

**Solution:**
1. Add database indexes:
```sql
CREATE INDEX idx_readership_date ON readership_log(read_date);
CREATE INDEX idx_content_share_date ON content_share(created_on);
```

2. Clear cache and restart:
```bash
bench --site your-site.local clear-cache
bench restart
```

### Issue: Email Notifications Not Sending

**Solution:**
1. Verify SMTP settings in **Setup > Email Domain**
2. Check logs:
```bash
# View error log
tail -f ~/frappe-bench/logs/error.log
```

3. Test SMTP connection
4. Verify sender email is allowed

---

## Support

For issues or questions:
1. Check GitHub Issues: https://github.com/fboinett/church/issues
2. Consult Frappe Documentation: https://frappeframework.com/docs
3. Contact the development team

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2024-07-23 | Initial production release |

