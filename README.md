# Church Platform - ERPNext Custom App

A comprehensive Frappe/ERPNext application for managing church hierarchies, content, member engagement, and community organization.

[![GitHub](https://img.shields.io/badge/GitHub-fboinett/church-blue)](https://github.com/fboinett/church)
[![Version](https://img.shields.io/badge/Version-1.0.0-green)](https://github.com/fboinett/church/releases)
[![License](https://img.shields.io/badge/License-MIT-orange)](LICENSE)

---

## 🎯 Overview

Church Platform is a powerful ERPNext custom app designed to enable church organizations to:

- **Organize hierarchically** across national, regional, sub-regional, and local levels
- **Manage members** with role-based access and engagement tracking
- **Create and share content** including announcements, events, and blog posts
- **Moderate community** through comment approval workflows
- **Analyze engagement** with comprehensive dashboards and analytics
- **Empower members** with a dedicated web portal for interaction

Built on **Frappe Framework** with support for 8000+ members, real-time analytics, and multi-platform social sharing.

---

## ✨ Key Features

### 🏛️ Hierarchy Management
- 4-tier organizational hierarchy (National → Regional → Sub-Regional → Local)
- Role-based permissions at each level
- Automatic content visibility cascade

### 📢 Content Management
- **Announcements**: Broadcast to specific hierarchy levels
- **Events**: With RSVP management and attendance tracking
- **Blog Posts**: With rich text editor and multimedia attachments
- **Achievements**: Member recognition system

### 🔄 Moderation & Engagement
- **Comment Moderation**: Pending/Approved/Rejected workflow
- **Readership Tracking**: Analytics on content consumption
- **RSVP Management**: Event attendance tracking
- **Member Activity**: Personalized engagement dashboard

### 📊 Analytics & Dashboards
- **Role-Based Dashboards** (5 workspace layouts)
- **34 API Endpoints** for real-time widget data
- **4 Custom Reports** (Engagement, Share Analytics, Events, Regional Performance)
- **Trending Content** detection
- **Share Distribution** by platform

### 🌐 Social Sharing
- **5 Platforms**: WhatsApp, Facebook, Twitter, Email, Direct Link
- **URL Shortening**: Generated short codes for tracking
- **Open Graph** meta tags for rich previews
- **Share Analytics**: Track shares by platform and date

### 👥 Member Portal
- **7 Portal Pages**: Home, Feed, Events, Event Detail, Post Detail, Profile, Notifications
- **Responsive Design**: Mobile-first (320px+)
- **Personalized Feed**: Hierarchy-filtered content
- **Social Features**: Comments, RSVPs, Sharing

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/fboinett/church.git apps/church_platform

# Install into your Frappe bench
bench --site your-site.local install-app church_platform

# Migrate database
bench --site your-site.local migrate
```

### Load Demo Data

```bash
# Run the sample data fixture
bench --site your-site.local console
>>> from church_platform.fixtures.sample_data import create_all_fixtures
>>> create_all_fixtures()
```

This creates:
- 1 National + 4 Regional + 20 Sub-Regional regions
- 120 churches
- 50+ leaders at all levels
- 8500+ sample members

### Access

- **Admin**: `http://your-site.local/` (Frappe desk)
- **Member Portal**: `http://your-site.local/member-portal`
- **API**: `http://your-site.local/api/method/`

---

## 📚 Documentation

- **[Admin Setup Guide](./ADMIN_SETUP.md)** - Installation & configuration
- **[API Reference](./API_REFERENCE.md)** - All 42 endpoints (sharing, dashboards, portal)
- **[Full Documentation](./DOCUMENTATION.md)** - Complete user guides by role
- **[Architecture](./docs/ARCHITECTURE.md)** - System design & components
- **[Contributing](./docs/CONTRIBUTING.md)** - Development guidelines

---

## 📊 Statistics

- **14 DocTypes** with full business logic
- **42 REST API endpoints** (whitelisted)
- **5 Role-based workspaces** (dashboards)
- **7 Portal pages** with responsive design
- **4 Custom reports** for analytics
- **8000+ lines of code** across all phases
- **80+ test cases** (permissions, sharing, portal, integration)

---

## 🎯 Project Phases (Completed ✅)

- ✅ **Phase 1**: Foundation (Hierarchy & Users)
- ✅ **Phase 2**: Content Management (Announcements, Events, Blog Posts)
- ✅ **Phase 3**: Social Sharing (5 platforms, analytics)
- ✅ **Phase 4**: Dashboards (Role-based workspaces, 34 APIs)
- ✅ **Phase 5**: Member Portal (7 pages, responsive design)
- ✅ **Phase 6**: Testing (Unit & integration tests - 80+ test cases)
- ✅ **Phase 7**: Sample Fixtures (Demo data for 8000+ members)
- ✅ **Phase 8**: Documentation (Admin guides, API reference, user guides)

---

## 🔐 Security Features

- **Hierarchy-aware permissions** - Content visibility cascades down hierarchy
- **Role-based access control** - User roles enforce feature availability
- **Authentication required** - Portal access restricted to logged-in members
- **Input validation** - All forms validated on server-side
- **XSS protection** - Template escaping for user content
- **CSRF protection** - Built-in Frappe security

---

## 🛠️ Technology Stack

- **Backend**: Frappe Framework (Python)
- **Database**: MariaDB / PostgreSQL
- **Frontend**: Jinja2 templates, HTML5, CSS3
- **APIs**: REST (JSON responses)
- **Version Control**: Git

---

## 📋 Requirements

- ERPNext 14.0+
- Frappe Framework (latest)
- Python 3.8+
- MariaDB 10.3+ or PostgreSQL 10+
- Node.js 14+

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](./docs/CONTRIBUTING.md) for guidelines.

**Development Setup:**
```bash
git clone https://github.com/fboinett/church.git apps/church_platform
cd apps/church_platform
git checkout -b feature/your-feature
# Make changes and test
git commit -m "Add your feature"
git push origin feature/your-feature
# Create pull request on GitHub
```

---

## 📝 License

Church Platform is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## 💬 Support

- **Issues**: [GitHub Issues](https://github.com/fboinett/church/issues)
- **Documentation**: [Full Docs](./DOCUMENTATION.md)
- **Email**: admin@church.local

---

## 📦 Release Notes

### v1.0.0 (2024-07-23)

**Initial Production Release**

- 14 DocTypes implemented with full business logic
- 42 REST API endpoints (sharing, dashboards, portal)
- 5 role-based workspaces and dashboards
- 7 member portal pages with responsive design
- Comprehensive test suite (80+ test cases)
- Admin setup guide and API documentation
- Sample data fixtures for demo/testing
- Complete user guides by role

**Project Statistics:**
- 101 files created
- 8000+ lines of code
- 5 git commits (clean history)
- All 8 development phases completed

---

**Happy coding! 🚀**
