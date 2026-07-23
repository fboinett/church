# Church Platform - API Reference

Complete documentation for all 42 REST API endpoints of the Church Platform.

---

## Authentication

All API requests require authentication via:
- **Session-based**: Login via `/api/method/login` (for web)
- **Token-based**: X-Frappe-CSRF-Token header (for AJAX)

All endpoints return JSON responses.

---

## Endpoint Categories

1. [Sharing APIs (4 endpoints)](#sharing-apis)
2. [Dashboard APIs (34 endpoints)](#dashboard-apis)
   - National (5)
   - Regional (6)
   - Sub-Regional (6)
   - Local (6)
   - Member (6)
3. [Portal APIs (8 endpoints)](#portal-apis)

---

## Sharing APIs

### 1. GET /api/method/get_share_links

Get all share links for a content item.

**Parameters:**
```
doctype (string, required): "Church Blog Post", "Event", or "Announcement"
name (string, required): Document name/ID
```

**Response:**
```json
{
  "message": {
    "whatsapp": "https://api.whatsapp.com/send?text=...",
    "facebook": "https://www.facebook.com/sharer/sharer.php?u=...",
    "twitter": "https://twitter.com/intent/tweet?text=...",
    "email": "mailto:?subject=...",
    "direct": "http://church.local/posts/abc123"
  }
}
```

**Example:**
```bash
curl -X GET "https://church.local/api/method/get_share_links?doctype=Church+Blog+Post&name=My+First+Post"
```

---

### 2. POST /api/method/log_share

Log a share action for analytics.

**Parameters:**
```json
{
  "doctype": "Church Blog Post",
  "name": "My First Post",
  "platform": "whatsapp",
  "shared_by": "member@church.local"
}
```

**Response:**
```json
{
  "message": {
    "success": true,
    "share_id": "cs-001"
  }
}
```

**Example:**
```bash
curl -X POST "https://church.local/api/method/log_share" \
  -H "Content-Type: application/json" \
  -d '{
    "doctype": "Church Blog Post",
    "name": "My First Post",
    "platform": "whatsapp"
  }'
```

---

### 3. GET /api/method/get_share_stats

Get sharing statistics for content.

**Parameters:**
```
doctype (string, required): Document type
name (string, required): Document name
```

**Response:**
```json
{
  "message": {
    "total_shares": 45,
    "shares_by_platform": {
      "whatsapp": 20,
      "facebook": 15,
      "twitter": 7,
      "email": 3,
      "direct": 0
    },
    "shares_by_date": {
      "2024-07-20": 10,
      "2024-07-21": 15,
      "2024-07-22": 20
    }
  }
}
```

---

### 4. GET /api/method/get_trending_content

Get trending content across platform.

**Parameters:**
```
limit (integer, optional): Max results (default: 10)
content_type (string, optional): Filter by type
days (integer, optional): Last N days (default: 30)
```

**Response:**
```json
{
  "message": [
    {
      "doctype": "Church Blog Post",
      "name": "Post Title",
      "shares": 150,
      "views": 450,
      "comments": 32,
      "engagement_score": 0.85
    }
  ]
}
```

---

## Dashboard APIs

### National Leader Dashboards (5 endpoints)

#### 1. GET /api/method/get_national_stats

Get national-level statistics.

**Response:**
```json
{
  "message": {
    "total_regions": 4,
    "total_churches": 120,
    "total_leaders": 65,
    "total_members": 8500,
    "active_members": 7850,
    "engagement_rate": 0.92
  }
}
```

---

#### 2. GET /api/method/get_national_engagement

Get national engagement metrics.

**Response:**
```json
{
  "message": {
    "total_posts": 250,
    "total_comments": 1200,
    "total_shares": 3400,
    "total_rsvps": 5600,
    "avg_comment_rate": 0.15,
    "avg_share_rate": 0.42
  }
}
```

---

#### 3. GET /api/method/get_engagement_trend

Get engagement trends over time.

**Parameters:**
```
days (integer, optional): Number of days (default: 30)
```

**Response:**
```json
{
  "message": [
    {
      "date": "2024-07-20",
      "posts": 5,
      "comments": 45,
      "shares": 120,
      "rsvps": 200
    }
  ]
}
```

---

#### 4. GET /api/method/get_pending_approvals

Get pending comments for approval.

**Response:**
```json
{
  "message": [
    {
      "comment_id": "bc-001",
      "post": "Post Title",
      "author": "Member Name",
      "content": "Comment text...",
      "submitted_on": "2024-07-22 10:30:00"
    }
  ]
}
```

---

#### 5. GET /api/method/get_trending_posts

Get trending posts and engagement leaders.

**Response:**
```json
{
  "message": {
    "top_posts": [
      {
        "title": "Post Title",
        "shares": 150,
        "comments": 32,
        "views": 450
      }
    ],
    "top_authors": [
      {
        "name": "Author Name",
        "posts": 25,
        "engagement_score": 0.89
      }
    ]
  }
}
```

---

### Regional Leader Dashboards (6 endpoints)

#### 6. GET /api/method/get_regional_stats

Get regional statistics (filtered to user's region).

**Response:**
```json
{
  "message": {
    "region": "East Africa",
    "sub_regions": 5,
    "churches": 30,
    "leaders": 18,
    "members": 2100,
    "engagement_rate": 0.89
  }
}
```

---

#### 7-11. Similar endpoints for regional level

- `get_regional_engagement`: Regional engagement metrics
- `get_regional_pending_approvals`: Pending comments in region
- `get_regional_performance`: Performance by sub-region
- `get_regional_trending`: Trending content in region
- `get_regional_members`: Member statistics

---

### Sub-Regional Leader Dashboards (6 endpoints)

#### 12. GET /api/method/get_subregional_stats

Get sub-regional statistics.

**Response:**
```json
{
  "message": {
    "sub_region": "East Africa - District 1",
    "churches": 6,
    "leaders": 25,
    "members": 450,
    "engagement_rate": 0.87
  }
}
```

---

### Local Leader Dashboards (6 endpoints)

#### 18. GET /api/method/get_local_stats

Get church-level statistics.

**Response:**
```json
{
  "message": {
    "church": "Church Name",
    "members": 75,
    "active_members": 68,
    "announcements": 12,
    "events": 8,
    "posts": 20,
    "engagement_rate": 0.91
  }
}
```

---

### Member Dashboards (6 endpoints)

#### 24. GET /api/method/get_personalized_feed

Get personalized member feed.

**Parameters:**
```
limit (integer): Items per page (default: 20)
offset (integer): Pagination offset (default: 0)
```

**Response:**
```json
{
  "message": [
    {
      "doctype": "Church Blog Post",
      "name": "Post Title",
      "author": "Author Name",
      "content": "Post content...",
      "created_on": "2024-07-22 10:30:00",
      "comments": 5,
      "shares": 12
    }
  ]
}
```

---

#### 25. GET /api/method/get_member_events

Get upcoming events for member.

**Response:**
```json
{
  "message": [
    {
      "name": "Event Title",
      "date": "2024-08-05",
      "time": "10:00 AM",
      "location": "Church",
      "rsvp_count": 25,
      "your_rsvp": "Yes"
    }
  ]
}
```

---

## Portal APIs

### 1. POST /api/method/submit_comment

Submit a comment on content.

**Parameters:**
```json
{
  "post_id": "post-001",
  "content": "Great post!",
  "member_id": "member-001"
}
```

**Response:**
```json
{
  "message": {
    "success": true,
    "comment_id": "bc-002",
    "status": "Pending"
  }
}
```

---

### 2. POST /api/method/rsvp_event

RSVP to an event.

**Parameters:**
```json
{
  "event_id": "event-001",
  "response": "Yes",
  "member_id": "member-001"
}
```

**Response:**
```json
{
  "message": {
    "success": true,
    "rsvp_id": "rsvp-001"
  }
}
```

---

### 3. POST /api/method/update_member_profile

Update member profile.

**Parameters:**
```json
{
  "phone": "+254700000000",
  "bio": "Member bio",
  "profile_photo": "base64-encoded-image"
}
```

**Response:**
```json
{
  "message": {
    "success": true,
    "profile_updated": true
  }
}
```

---

### 4. GET /api/method/get_member_notifications

Get member notifications.

**Parameters:**
```
limit (integer): Items per page (default: 20)
unread_only (boolean): Only unread (default: false)
```

**Response:**
```json
{
  "message": [
    {
      "id": "notif-001",
      "type": "comment_approved",
      "message": "Your comment was approved",
      "created_on": "2024-07-22 14:30:00",
      "read": false
    }
  ]
}
```

---

### 5. POST /api/method/mark_notification_read

Mark notification as read.

**Parameters:**
```json
{
  "notification_id": "notif-001"
}
```

---

### 6. POST /api/method/share_content

Share content from portal.

**Parameters:**
```json
{
  "content_type": "Church Blog Post",
  "content_id": "post-001",
  "platform": "whatsapp",
  "message": "Check this out!"
}
```

---

### 7. GET /api/method/search_content

Search for content.

**Parameters:**
```
q (string): Search query
content_type (string): Filter by type
limit (integer): Results limit
```

**Response:**
```json
{
  "message": [
    {
      "doctype": "Church Blog Post",
      "name": "Matching Post Title",
      "excerpt": "First 100 chars of content..."
    }
  ]
}
```

---

### 8. GET /api/method/get_portal_announcements

Get announcements for member's church.

**Response:**
```json
{
  "message": [
    {
      "name": "Announcement",
      "title": "Important Announcement",
      "content": "Announcement content...",
      "created_on": "2024-07-22"
    }
  ]
}
```

---

## Error Responses

All endpoints use standard HTTP status codes:

```json
{
  "exc": "[403 Frappe__PermissionError]: Permission Denied",
  "message": null
}
```

Common error codes:
- **401**: Unauthorized (not logged in)
- **403**: Forbidden (no permission)
- **404**: Not Found
- **500**: Server Error

---

## Rate Limiting

API endpoints are rate-limited to:
- **Authenticated users**: 1000 requests/hour
- **Anonymous**: 100 requests/hour

---

## Example Integration

### JavaScript Fetch

```javascript
// Get share links
async function getShareLinks(doctype, name) {
  const response = await fetch(
    `/api/method/get_share_links?doctype=${doctype}&name=${name}`
  );
  const data = await response.json();
  return data.message;
}

// Log a share
async function logShare(doctype, name, platform) {
  const response = await fetch('/api/method/log_share', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      doctype, name, platform
    })
  });
  return await response.json();
}
```

### Python Integration

```python
import frappe
import requests

# Using Frappe's built-in client
frappe.call(
    method='church_platform.sharing.api.get_share_links',
    args={'doctype': 'Church Blog Post', 'name': 'My Post'},
    callback=lambda r: print(r.message)
)

# Using direct API
response = requests.get(
    'https://church.local/api/method/get_share_links',
    params={'doctype': 'Church Blog Post', 'name': 'My Post'},
    cookies={'sid': session_id}
)
print(response.json())
```

---

## Versioning

Current API version: **1.0.0**

Future versions will maintain backward compatibility where possible.

---

## Support

For API issues:
1. Check endpoint status in `church_platform/hooks.py`
2. Review error logs: `~/frappe-bench/logs/error.log`
3. File issue: https://github.com/fboinett/church/issues

