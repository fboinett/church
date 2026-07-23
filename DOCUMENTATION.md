# Church Platform Documentation

Complete documentation for the Church Platform ERPNext Custom App.

## 📚 Documentation Sections

1. **[Admin Setup Guide](./ADMIN_SETUP.md)** - Installation, configuration, initial data setup
2. **[User Guides](#user-guides)** - Role-specific guides for each user type
3. **[API Reference](./API_REFERENCE.md)** - Complete API documentation (42 endpoints)
4. **[Database Schema](./DATABASE_SCHEMA.md)** - DocType definitions and relationships
5. **[Architecture Overview](./ARCHITECTURE.md)** - System design and components
6. **[Contributing Guide](./CONTRIBUTING.md)** - Development workflow and code standards

---

## User Guides

### 🏛️ **National Leader Guide** - [GUIDE_NATIONAL.md](./GUIDE_NATIONAL.md)
- Organization overview (all regions, churches, members)
- Dashboard & statistics
- Content management across all levels
- User & permission management
- Financial reports

### 🌍 **Regional Leader Guide** - [GUIDE_REGIONAL.md](./GUIDE_REGIONAL.md)
- Regional overview (sub-regions, churches)
- Regional dashboard
- Managing regional content
- Sub-regional coordination
- Event & announcement publishing

### 🏘️ **Sub-Regional Leader Guide** - [GUIDE_SUBREGIONAL.md](./GUIDE_SUBREGIONAL.md)
- Sub-region overview
- Church management
- Content coordination
- Event planning
- Local leader support

### ⛪ **Local Leader Guide** - [GUIDE_LOCAL.md](./GUIDE_LOCAL.md)
- Church management
- Member management
- Local announcements & events
- Blog post creation
- Community engagement

### 👥 **Member Guide** - [GUIDE_MEMBER.md](./GUIDE_MEMBER.md)
- Member portal overview
- Viewing content
- RSVPs & participation
- Profile management
- Social sharing

---

## Quick Start

1. **Installation**: See [ADMIN_SETUP.md](./ADMIN_SETUP.md)
2. **Load Sample Data**: `bench execute church_platform.fixtures.sample_data.create_all_fixtures`
3. **Access Portal**: Visit `/member-portal` (requires login)
4. **Dashboard**: Each role has personalized dashboard

---

## Features by Role

| Feature | National | Regional | Sub-Regional | Local | Member |
|---------|----------|----------|--------------|-------|--------|
| View All Content | ✓ | ✓* | ✓* | ✓* | ✓* |
| Create Content | ✓ | ✓ | ✓ | ✓ | ✗ |
| Approve Comments | ✓ | ✓ | ✓ | ✓ | ✗ |
| Manage Users | ✓ | ✓ | ✓ | ✓ | ✗ |
| View Reports | ✓ | ✓ | ✓ | ✓ | ✓ |
| RSVP Events | ✓ | ✓ | ✓ | ✓ | ✓ |
| Post Comments | ✓ | ✓ | ✓ | ✓ | ✓ |
| Share Content | ✓ | ✓ | ✓ | ✓ | ✓ |

*Hierarchy-filtered

---

## Key Concepts

### Hierarchy Levels
- **National**: Sees and manages entire organization
- **Regional**: Manages one region and all sub-regions/churches within
- **Sub-Regional**: Manages sub-region and its churches
- **Local**: Manages single church and its members

### Content Visibility
- **National**: Visible to entire organization
- **Regional**: Visible to region + all lower levels
- **Sub-Regional**: Visible to sub-region + churches within
- **Local**: Visible to specific church only

### Comment Moderation
- Members submit comments (Pending status)
- Authors/Admins can Approve or Reject
- Only Approved comments visible to members

---

## Support & Troubleshooting

### Common Issues

**Q: How do I reset a user's password?**  
A: Use the Frappe User DocType and reset password option.

**Q: How do I give a user leader access?**  
A: Create a Church Leader record and assign to hierarchy level.

**Q: How do I export member data?**  
A: Use Frappe's built-in export feature on Member list.

**Q: Members cannot see events**  
A: Check event status is "Published" and target_level matches member's hierarchy.

---

## Performance & Optimization

- Hierarchy checks cached per session
- Content queries filtered by hierarchy level
- Readership/share logs indexed by date
- Dashboard queries optimized for large datasets

---

## Version History

| Version | Date | Notes |
|---------|------|-------|
| 1.0.0 | 2024-07-23 | Initial release: 5 phases, 14 DocTypes, 42 APIs |

---

## License

Church Platform is licensed under the MIT License. See LICENSE file for details.

---

## Credits

Built with Frappe Framework | ERPNext  
Developed for church organization & community engagement
