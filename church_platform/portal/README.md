# Church Platform Portal

Member-facing web interface for content consumption, engagement, and participation.

## Features

### Pages

- **Home Dashboard** (`/portal/home`)
  - Welcome card with member greeting
  - Recent posts listing
  - Upcoming events preview
  - Recent comments activity
  - Quick statistics sidebar

- **Content Feed** (`/portal/feed`)
  - Personalized content feed (paginated)
  - Filter by content type (posts, events, announcements)
  - Hierarchy-aware content filtering
  - View statistics (reads, shares)

- **Events** (`/portal/events`)
  - Event calendar view
  - RSVP management
  - Event filtering by date and level
  - Upcoming events countdown

- **Event Detail** (`/portal/event/<event_id>`)
  - Full event information
  - Event location and time
  - RSVP form (Confirmed/Maybe/Declined)
  - Event statistics
  - Share buttons

- **Blog Post Detail** (`/portal/post/<post_id>`)
  - Full blog post content
  - Author and publication date
  - Readership tracking
  - Comment form (with moderation preview)
  - Approved comments listing
  - Share buttons (WhatsApp, Facebook, Twitter, Email)
  - Attachments download links

- **Member Profile** (`/portal/profile`)
  - Member information display
  - Bio and contact details
  - Activity statistics
  - Achievements and badges
  - Edit profile form
  - Account settings

- **Notifications** (`/portal/notifications`)
  - Pending comments to approve (for authors)
  - Upcoming events reminders
  - Comment replies notifications
  - Notification management

### API Endpoints

All endpoints are whitelisted and require member authentication.

#### Comments
- `submit_comment(blog_post, content)` - Submit a comment
  - Returns: `{status, message, comment_id}`
  - Comments start in "Pending" state
  - Requires "allow_comments" on the blog post

#### Events
- `rsvp_event(event_id, status)` - RSVP for an event
  - Status: "Confirmed", "Maybe", "Declined"
  - Returns: `{status, message, rsvp_status}`
  - Tracks attendance via Event Attendance table

#### Member Profile
- `update_member_profile(first_name, last_name, bio, phone, location)` - Update profile
  - Returns: `{status, message}`
  - Updates allowed fields only

#### Notifications
- `get_member_notifications()` - Get member notifications
  - Returns array of notifications with type, message, created time
  - Types: pending_comment, upcoming_event, comment_reply

- `mark_notification_read(notification_id)` - Mark as read
  - Returns: `{status, message}`

#### Content Discovery
- `search_content(query, content_type)` - Search portal content
  - content_type: "all", "post", "event", "announcement"
  - Returns matching content with titles and metadata

- `get_portal_announcements()` - Get current announcements
  - Filters by published status and date
  - Returns announcements with content and targets

- `share_content(content_type, content_id, platform)` - Log content sharing
  - Tracks shares to Content Share DocType
  - Returns share links for frontend redirects

## Security

### Authentication
- All pages require member login (Guest access blocked)
- Session-based authentication via Frappe user system
- Automatic permission checks on all data access

### Permissions
- Content filtering by hierarchy level (National/Regional/Sub-Regional/Local)
- Members see only content targeted to their level
- Authors can moderate comments on their posts
- Members cannot access other members' private data

### Data Protection
- Input validation on all forms
- CSRF protection via Frappe framework
- SQL injection prevention via prepared statements
- XSS protection via template escaping

## Styling

### CSS Files
- `static/css/portal.css` - Main portal stylesheet (responsive, mobile-first)

### Design Principles
- **Color Scheme**:
  - Primary: #667eea (Purple)
  - Secondary: #764ba2 (Dark Purple)
  - Success: #28a745 (Green)
  - Info: #d4edda (Light Green)
  
- **Typography**: System fonts (Apple System Font, Segoe UI, etc.)
- **Layout**: 12-column grid system, responsive breakpoints
- **Spacing**: Modular spacing scale (5px, 10px, 15px, 20px, 30px)
- **Cards**: White cards with subtle shadows on light gray background

## Data Queries

### Content Visibility
```sql
-- Blog posts visible to member
SELECT * FROM `tabChurch Blog Post`
WHERE status = 'Published'
  AND (target_level = 'National' OR target_region = member_region, etc.)
```

### Readership Tracking
```sql
-- Log readership on post view
INSERT INTO `tabReadership Log` 
  (reader, content_id, content_type, read_date)
VALUES (..., post_id, 'Church Blog Post', TODAY())
```

### Comments Workflow
```sql
-- Get pending comments for author
SELECT * FROM `tabBlog Comment`
WHERE blog_post IN (SELECT name FROM `tabChurch Blog Post` WHERE author = user)
  AND status = 'Pending'
```

### Event RSVPs
```sql
-- Track event attendance
INSERT INTO `tabEvent Attendance` 
  (parent, member, status)
VALUES (event_id, member_id, 'Confirmed')
```

## Frontend Integration

### Frappe Framework Integration
- Uses Frappe's `frappe.route()` decorator for routing
- Uses Frappe's `frappe.call()` for AJAX API calls
- Uses Frappe's permission system for access control
- Uses Frappe's form rendering for input validation

### Example AJAX Call
```javascript
frappe.call({
    method: 'church_platform.portal.api.submit_comment',
    args: {
        blog_post: post_id,
        content: comment_text
    },
    callback: function(r) {
        if (r.message.status === 'success') {
            // Reload page or update UI
        }
    }
});
```

## Future Enhancements

- [ ] Member-to-member messaging
- [ ] User notifications DocType
- [ ] Real-time notifications via Socket.io
- [ ] Content recommendations engine
- [ ] Advanced search with filters
- [ ] Member activity feed
- [ ] Social features (follow, like)
- [ ] Mobile app integration
- [ ] Export content as PDF
- [ ] Multi-language support

## File Structure

```
church_platform/portal/
├── __init__.py                  # Module initialization
├── controller.py                # Page controllers and context
├── api.py                       # API endpoints
├── templates/
│   ├── home.html               # Home dashboard
│   ├── feed.html               # Content feed
│   ├── events.html             # Events listing
│   ├── event_detail.html       # Event detail page
│   ├── post_detail.html        # Blog post detail
│   ├── profile.html            # Member profile
│   └── notifications.html      # Notifications
└── static/
    └── css/
        └── portal.css          # Stylesheet
```

## Development Notes

- Portal pages are rendered server-side using Jinja2 templates
- Styling uses CSS custom properties for theming
- Responsive design supports mobile (320px+) to desktop (1400px+)
- All database queries use prepared statements
- Error handling includes user-friendly messages
- Logging for debugging and monitoring
