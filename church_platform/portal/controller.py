"""
Portal Controller - Handles portal page rendering and context preparation
"""

import frappe
from frappe import _
from frappe.utils import getdate, add_days
from church_platform.hierarchy.permissions import get_user_hierarchy_scope


def get_portal_context():
    """Get context for portal pages"""
    user = frappe.session.user
    
    if user == "Guest":
        frappe.throw(_("You must be logged in to access the portal"), frappe.PermissionError)
    
    # Determine user type (Member vs Leader)
    user_type = get_user_type(user)
    hierarchy_scope = get_user_hierarchy_scope(user)
    
    return {
        "user": user,
        "user_type": user_type,
        "hierarchy_scope": hierarchy_scope,
        "portal_title": "Church Platform Portal",
        "version": frappe.get_meta("App").get_version() or "1.0.0",
    }


def get_user_type(user):
    """Determine if user is a Member or Church Leader"""
    
    # Check if user is a Member
    member = frappe.db.get_value("Member", {"user": user}, "name")
    if member:
        return "Member"
    
    # Check if user is a Church Leader
    leader = frappe.db.get_value("Church Leader", {"user": user}, "name")
    if leader:
        return "Leader"
    
    return "Guest"


@frappe.route("/portal/home", methods=["GET"])
def member_page():
    """Member dashboard/home page"""
    
    context = get_portal_context()
    user = frappe.session.user
    
    # Get member document
    member = frappe.get_doc("Member", {"user": user})
    
    # Get recent activities
    recent_posts = get_recent_posts(member.name)
    upcoming_events = get_upcoming_events(member.name)
    recent_comments = get_member_comments(member.name, limit=5)
    
    context.update({
        "member": member,
        "recent_posts": recent_posts,
        "upcoming_events": upcoming_events,
        "recent_comments": recent_comments,
        "page_title": _("Home"),
    })
    
    return frappe.render_template("church_platform/portal/templates/home.html", context)


@frappe.route("/portal/feed", methods=["GET"])
def feed_page():
    """Personalized content feed"""
    
    context = get_portal_context()
    user = frappe.session.user
    member = frappe.get_doc("Member", {"user": user})
    
    # Get paginated feed
    page = frappe.request.args.get("page", 1)
    page = int(page) if isinstance(page, str) else page
    limit = 20
    offset = (page - 1) * limit
    
    # Get hierarchy-filtered content
    feed_items = get_personalized_feed(member.name, limit, offset)
    
    context.update({
        "member": member,
        "feed_items": feed_items,
        "page": page,
        "page_title": _("My Feed"),
    })
    
    return frappe.render_template("church_platform/portal/templates/feed.html", context)


@frappe.route("/portal/events", methods=["GET"])
def events_page():
    """Events listing and calendar"""
    
    context = get_portal_context()
    user = frappe.session.user
    member = frappe.get_doc("Member", {"user": user})
    
    # Get upcoming events
    upcoming = get_upcoming_events(member.name, limit=50)
    
    # Get member's RSVPs
    member_rsvps = get_member_rsvps(member.name)
    
    context.update({
        "member": member,
        "upcoming_events": upcoming,
        "member_rsvps": member_rsvps,
        "page_title": _("Events"),
    })
    
    return frappe.render_template("church_platform/portal/templates/events.html", context)


@frappe.route("/portal/event/<event_id>", methods=["GET"])
def event_detail_page(event_id):
    """Single event detail view"""
    
    context = get_portal_context()
    user = frappe.session.user
    member = frappe.get_doc("Member", {"user": user})
    
    # Get event
    event = frappe.get_doc("Event", event_id)
    
    # Check if member has RSVP'd
    rsvp = frappe.db.get_value(
        "Event Attendance",
        {"parent": event_id, "member": member.name},
        "status"
    )
    
    # Get event comments
    comments = get_event_comments(event_id, status="Approved")
    
    context.update({
        "member": member,
        "event": event,
        "member_rsvp_status": rsvp,
        "comments": comments,
        "page_title": event.title,
    })
    
    return frappe.render_template("church_platform/portal/templates/event_detail.html", context)


@frappe.route("/portal/post/<post_id>", methods=["GET"])
def post_detail_page(post_id):
    """Single blog post detail view"""
    
    context = get_portal_context()
    user = frappe.session.user
    member = frappe.get_doc("Member", {"user": user})
    
    # Get post
    post = frappe.get_doc("Church Blog Post", post_id)
    
    # Check read permission
    if not post.has_permission("read"):
        frappe.throw(_("You don't have permission to view this post"), frappe.PermissionError)
    
    # Log readership
    log_readership(member.name, post_id, "Church Blog Post")
    
    # Get approved comments
    comments = get_post_comments(post_id, status="Approved")
    
    # Get share links
    share_links = frappe.call("church_platform.sharing.api.get_share_links", 
                               args={"content_type": "Church Blog Post", "content_id": post_id})
    
    context.update({
        "member": member,
        "post": post,
        "comments": comments,
        "share_links": share_links,
        "page_title": post.title,
    })
    
    return frappe.render_template("church_platform/portal/templates/post_detail.html", context)


@frappe.route("/portal/profile", methods=["GET"])
def profile_page():
    """Member profile and settings"""
    
    context = get_portal_context()
    user = frappe.session.user
    member = frappe.get_doc("Member", {"user": user})
    
    # Get member achievements
    achievements = get_member_achievements(member.name)
    
    # Get member statistics
    stats = get_member_stats(member.name)
    
    context.update({
        "member": member,
        "achievements": achievements,
        "stats": stats,
        "page_title": _("My Profile"),
    })
    
    return frappe.render_template("church_platform/portal/templates/profile.html", context)


@frappe.route("/portal/notifications", methods=["GET"])
def notifications_page():
    """Member notifications"""
    
    context = get_portal_context()
    user = frappe.session.user
    member = frappe.get_doc("Member", {"user": user})
    
    # Get notifications
    notifications = get_member_notifications(member.name)
    
    context.update({
        "member": member,
        "notifications": notifications,
        "page_title": _("Notifications"),
    })
    
    return frappe.render_template("church_platform/portal/templates/notifications.html", context)


def get_recent_posts(member_id, limit=5):
    """Get recent posts visible to member"""
    
    member = frappe.get_doc("Member", member_id)
    
    posts = frappe.db.sql("""
        SELECT 
            name, title, author, published_date, views,
            target_level, content
        FROM `tabChurch Blog Post`
        WHERE status = 'Published'
        ORDER BY published_date DESC
        LIMIT %s
    """, (limit,), as_dict=True)
    
    # Filter by visibility (hierarchy)
    visible_posts = []
    for post in posts:
        if member.has_permission("read", post.get("name")):
            visible_posts.append(post)
    
    return visible_posts[:limit]


def get_upcoming_events(member_id, limit=10):
    """Get upcoming events for member"""
    
    member = frappe.get_doc("Member", member_id)
    today = getdate()
    
    events = frappe.db.sql("""
        SELECT 
            name, title, event_date, target_level,
            organized_by, target_church
        FROM `tabEvent`
        WHERE status = 'Published' AND event_date >= %s
        ORDER BY event_date ASC
        LIMIT %s
    """, (today, limit), as_dict=True)
    
    # Filter by visibility
    visible_events = []
    for event in events:
        if event.get("target_level") == "Local" or event.get("target_church") == member.parent_church:
            visible_events.append(event)
        elif event.get("target_level") in ["Sub-Regional", "Regional", "National"]:
            visible_events.append(event)
    
    return visible_events


def get_personalized_feed(member_id, limit=20, offset=0):
    """Get personalized content feed for member"""
    
    member = frappe.get_doc("Member", member_id)
    
    # Blog posts
    posts = frappe.db.sql("""
        SELECT 
            'Blog Post' as type,
            name, title, author, published_date, views,
            content, target_level
        FROM `tabChurch Blog Post`
        WHERE status = 'Published'
    """, as_dict=True)
    
    # Events
    events = frappe.db.sql("""
        SELECT 
            'Event' as type,
            name, title, event_date, organized_by,
            target_level
        FROM `tabEvent`
        WHERE status = 'Published' AND event_date >= CURDATE()
    """, as_dict=True)
    
    # Announcements
    announcements = frappe.db.sql("""
        SELECT 
            'Announcement' as type,
            name, subject as title, announcement_date as published_date,
            content, target_level
        FROM `tabAnnouncement`
        WHERE status = 'Published'
    """, as_dict=True)
    
    # Combine and sort by date
    feed = posts + events + announcements
    feed = sorted(feed, key=lambda x: x.get("published_date") or x.get("event_date"), reverse=True)
    
    # Filter by visibility and paginate
    visible_feed = []
    for item in feed:
        if member.has_permission("read"):
            visible_feed.append(item)
    
    return visible_feed[offset:offset+limit]


def get_member_comments(member_id, limit=10):
    """Get member's recent comments"""
    
    comments = frappe.db.sql("""
        SELECT 
            name, blog_post, content, status, created_on
        FROM `tabBlog Comment`
        WHERE commenter = %s
        ORDER BY created_on DESC
        LIMIT %s
    """, (member_id, limit), as_dict=True)
    
    return comments


def get_post_comments(post_id, status="Approved"):
    """Get comments for a post"""
    
    comments = frappe.db.sql("""
        SELECT 
            name, content, commenter, created_on, status
        FROM `tabBlog Comment`
        WHERE blog_post = %s AND status = %s
        ORDER BY created_on ASC
    """, (post_id, status), as_dict=True)
    
    return comments


def get_event_comments(event_id, status="Approved"):
    """Get comments for an event"""
    
    comments = frappe.db.sql("""
        SELECT 
            name, content, commenter, created_on, status
        FROM `tabBlog Comment`
        WHERE blog_post IN (SELECT name FROM `tabChurch Blog Post` WHERE target_event = %s)
        AND status = %s
        ORDER BY created_on ASC
    """, (event_id, status), as_dict=True)
    
    return comments


def get_member_rsvps(member_id):
    """Get member's event RSVPs"""
    
    rsvps = frappe.db.sql("""
        SELECT 
            parent as event_id, status, attended
        FROM `tabEvent Attendance`
        WHERE member = %s
        ORDER BY creation DESC
    """, (member_id,), as_dict=True)
    
    return rsvps


def get_member_achievements(member_id):
    """Get member's achievements"""
    
    achievements = frappe.db.sql("""
        SELECT 
            name, title, description, awarded_date
        FROM `tabAchievement`
        WHERE recipient = %s AND docstatus = 1
        ORDER BY awarded_date DESC
    """, (member_id,), as_dict=True)
    
    return achievements


def get_member_stats(member_id):
    """Get member statistics"""
    
    stats = frappe.db.sql("""
        SELECT 
            (SELECT COUNT(*) FROM `tabReadership Log` WHERE reader = %s) as posts_read,
            (SELECT COUNT(*) FROM `tabBlog Comment` WHERE commenter = %s AND status = 'Approved') as approved_comments,
            (SELECT COUNT(*) FROM `tabContent Share` WHERE shared_by = %s) as items_shared,
            (SELECT COUNT(*) FROM `tabEvent Attendance` WHERE member = %s AND status = 'Confirmed') as events_attended,
            (SELECT COUNT(*) FROM `tabAchievement` WHERE recipient = %s AND docstatus = 1) as achievements
    """, (member_id, member_id, member_id, member_id, member_id), as_dict=True)
    
    return stats[0] if stats else {}


def log_readership(reader_id, content_id, content_type):
    """Log content readership"""
    
    readership_log = frappe.get_doc({
        "doctype": "Readership Log",
        "reader": reader_id,
        "content_id": content_id,
        "content_type": content_type,
        "read_date": frappe.utils.today(),
    })
    
    readership_log.insert(ignore_permissions=True)


def get_member_notifications(member_id):
    """Get member notifications"""
    
    # For now, return sample notifications
    # In production, create a Notification DocType
    return [
        {
            "type": "comment",
            "message": "Someone replied to your comment",
            "created": frappe.utils.now_datetime(),
        },
        {
            "type": "event",
            "message": "Your RSVP'd event is happening tomorrow",
            "created": frappe.utils.now_datetime(),
        },
    ]
