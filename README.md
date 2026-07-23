# Church Platform - ERPNext Custom App

A comprehensive hierarchical content management and engagement system for church organizations built on Frappe/ERPNext.

## Project Overview

The Church Platform manages a 4-tier organizational hierarchy:
- **National Level**: Archbishop/Admin (Platform administrators)
- **Regional Level**: Bishop (Diocese managers)  
- **Sub-Regional Level**: Archdeacon (Archdeaconry managers)
- **Local Level**: Vicar (Parish/Church leaders)
- **Members**: Portal-only users for content engagement

## Architecture

### Hierarchy Structure
```
Archbishop/National Admin
    ├── Region (Diocese)
    │   ├── Sub-Region (Archdeaconry)
    │   │   ├── Church (Parish)
    │   │   │   └── Members
```

### Core Modules

1. **Hierarchy Management** - Region, Sub-Region, Church
2. **User Management** - Church Leaders, Members
3. **Content Management** - Announcements, Events, Achievements
4. **Publications** - Blog Posts, Comments (moderated)
5. **Analytics** - Readership Logs, Engagement Tracking

## Phase 1: Foundation (Completed ✅)

- [x] Frappe app scaffolding
- [x] Hierarchy DocTypes: Region, Sub-Region, Church
- [x] User DocTypes: Church Leader, Member
- [x] Hierarchy-aware permissions system
- [x] Core business logic

## DocTypes Created

### Hierarchy
- **Region** - Diocese level organizational unit
- **Sub Region** - Archdeaconry level organizational unit  
- **Church** - Parish local church

### User Management
- **Church Leader** - Leaders at each hierarchy level
- **Member** - Church members with portal access

## Key Features

### Hierarchy-Aware Permissions
- Content visibility based on hierarchy level
- Users at higher levels see content from lower levels
- Custom `has_permission()` methods for each DocType
- Automatic scope filtering

### Data Validation
- Hierarchy chain validation (Region → Sub-Region → Church)
- Leader assignment validation
- Automatic code normalization (UPPERCASE)
- Relationship integrity checks

## Installation

1. Clone the repository
2. Add app to bench:
   ```bash
   bench get-app church_platform
   ```
3. Install the app:
   ```bash
   bench install-app church_platform
   ```
4. Migrate:
   ```bash
   bench migrate
   ```

## Project Status

**Current Phase**: Phase 1 - Foundation (✅ Complete)

**Next Phase**: Phase 2 - Content Management (Announcements, Events, Achievements)

## Development Roadmap

- [ ] Phase 2: Content Management DocTypes
- [ ] Phase 3: Blog/Publication Module with moderated comments
- [ ] Phase 4: Social Media Sharing
- [ ] Phase 5: Role-based Dashboards
- [ ] Phase 6: Member Portal
- [ ] Phase 7: Engagement Features & Analytics
- [ ] Phase 8: Polish, Testing & Documentation

## Team

Church Platform Development Team

## License

MIT
Church Platform
