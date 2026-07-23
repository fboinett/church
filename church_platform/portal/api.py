"""
Portal API Endpoints - Handles form submissions and interactions from the portal
"""

import frappe
from frappe import _
from frappe.utils import getdate, now_datetime


@frappe.whitelist(methods=["POST"])
def submit_comment(blog_post, content, parent_comment=None):
    """Submit a comment on a blog post"""
    
    user = frappe.session.user
    if user == "Guest":
        frappe.throw(_("You must be logged in to comment"), frappe.PermissionError)
    
    # Get member
    member = frappe.db.get_value("Member", {"user": user}, "name")
    if not member:
        frappe.throw(_("You must be a member to comment"), frappe.PermissionError)
    
    # Validate blog post exists and is published
    post = frappe.get_doc("Church Blog Post", blog_post)
    if post.status != "Published":
        frappe.throw(_("This post is not available for commenting"), frappe.PermissionError)
    
    # Check if comments are allowed
    if not post.allow_comments:
        frappe.throw(_("Comments are disabled for this post"), frappe.PermissionError)
    
    try:
        # Create comment in Pending state
        comment = frappe.get_doc({
            "doctype": "Blog Comment",
            "blog_post": blog_post,
            "commenter": member,
            "content": content,
            "status": "Pending",
        })
        
        comment.insert(ignore_permissions=True)
        
        frappe.db.commit()
        
        return {
            "status": "success",
            "message": _("Your comment has been submitted for moderation"),
            "comment_id": comment.name,
        }
    
    except frappe.ValidationError as e:
        frappe.throw(str(e))


@frappe.whitelist(methods=["POST"])
def rsvp_event(event_id, status="Confirmed"):
    """RSVP for an event"""
    
    user = frappe.session.user
    if user == "Guest":
        frappe.throw(_("You must be logged in to RSVP"), frappe.PermissionError)
    
    # Get member
    member = frappe.db.get_value("Member", {"user": user}, "name")
    if not member:
        frappe.throw(_("You must be a member to RSVP"), frappe.PermissionError)
    
    # Validate event
    event = frappe.get_doc("Event", event_id)
    if event.status != "Published":
        frappe.throw(_("This event is not available"), frappe.PermissionError)
    
    try:
        # Check if already RSVP'd
        existing = frappe.db.get_value(
            "Event Attendance",
            {"parent": event_id, "member": member},
            "name"
        )
        
        if existing:
            # Update existing RSVP
            attendance = frappe.get_doc("Event Attendance", existing)
            attendance.status = status
            attendance.save(ignore_permissions=True)
        else:
            # Create new RSVP
            event.append("attendees", {
                "member": member,
                "status": status,
            })
            event.save(ignore_permissions=True)
        
        frappe.db.commit()
        
        return {
            "status": "success",
            "message": _("Your RSVP has been recorded"),
            "rsvp_status": status,
        }
    
    except frappe.ValidationError as e:
        frappe.throw(str(e))


@frappe.whitelist(methods=["POST"])
def update_member_profile(
    first_name=None,
    last_name=None,
    bio=None,
    profile_image=None,
    phone=None,
    location=None
):
    """Update member profile"""
    
    user = frappe.session.user
    if user == "Guest":
        frappe.throw(_("You must be logged in"), frappe.PermissionError)
    
    # Get member
    member = frappe.get_doc("Member", {"user": user})
    
    try:
        # Update allowed fields
        if first_name:
            member.member_name = f"{first_name} {last_name or ''}".strip()
        
        if bio:
            member.bio = bio
        
        if profile_image:
            member.profile_image = profile_image
        
        if phone:
            member.phone = phone
        
        if location:
            member.location = location
        
        member.save(ignore_permissions=True)
        frappe.db.commit()
        
        return {
            "status": "success",
            "message": _("Your profile has been updated"),
        }
    
    except frappe.ValidationError as e:
        frappe.throw(str(e))


@frappe.whitelist()
def get_member_notifications(member_id=None):
    """Get member notifications"""
    
    user = frappe.session.user
    if user == "Guest":
        frappe.throw(_("You must be logged in"), frappe.PermissionError)
    
    # Get member if not specified
    if not member_id:
        member_id = frappe.db.get_value("Member", {"user": user}, "name")
    
    # Check permission
    member = frappe.get_doc("Member", member_id)
    if member.user != user and user != "Administrator":
        frappe.throw(_("You don't have permission to view these notifications"), frappe.PermissionError)
    
    # Get notifications (pending comments on member's posts)
    notifications = []
    
    # Pending comments to approve
    pending_comments = frappe.db.sql("""
        SELECT 
            bc.name as id,
            'pending_comment' as type,
            CONCAT('New comment on: ', cbp.title) as message,
            bc.created_on as created,
            cbp.name as post_id,
            bc.content as preview
        FROM `tabBlog Comment` bc
        JOIN `tabChurch Blog Post` cbp ON bc.blog_post = cbp.name
        WHERE cbp.author = %s AND bc.status = 'Pending'
        ORDER BY bc.created_on DESC
        LIMIT 10
    """, (member_id,), as_dict=True)
    
    notifications.extend(pending_comments)
    
    # Upcoming events RSVP'd
    upcoming_events = frappe.db.sql("""
        SELECT 
            e.name as id,
            'upcoming_event' as type,
            CONCAT('Upcoming event: ', e.title) as message,
            DATE_SUB(e.event_date, INTERVAL 1 DAY) as created,
            e.name as event_id
        FROM `tabEvent` e
        JOIN `tabEvent Attendance` ea ON e.name = ea.parent
        WHERE ea.member = %s AND e.event_date >= CURDATE()
        AND DATEDIFF(e.event_date, CURDATE()) <= 7
        ORDER BY e.event_date ASC
        LIMIT 5
    """, (member_id,), as_dict=True)
    
    notifications.extend(upcoming_events)
    
    # Replies to member's comments
    comment_replies = frappe.db.sql("""
        SELECT 
            bc.name as id,
            'comment_reply' as type,
            CONCAT('Reply to your comment on: ', cbp.title) as message,
            bc.created_on as created,
            cbp.name as post_id
        FROM `tabBlog Comment` bc
        JOIN `tabChurch Blog Post` cbp ON bc.blog_post = cbp.name
        JOIN `tabBlog Comment` parent_bc ON parent_bc.blog_post = cbp.name
        WHERE parent_bc.commenter = %s AND bc.status = 'Approved'
        AND bc.created_on > DATE_SUB(NOW(), INTERVAL 7 DAY)
        ORDER BY bc.created_on DESC
        LIMIT 5
    """, (member_id,), as_dict=True)
    
    notifications.extend(comment_replies)
    
    # Sort by date descending
    notifications = sorted(notifications, key=lambda x: x.get("created"), reverse=True)
    
    return notifications[:15]


@frappe.whitelist(methods=["POST"])
def mark_notification_read(notification_id):
    """Mark notification as read"""
    
    user = frappe.session.user
    if user == "Guest":
        frappe.throw(_("You must be logged in"), frappe.PermissionError)
    
    # This is a placeholder since we don't have a Notification DocType
    # In production, you'd mark a Notification record as read
    
    return {
        "status": "success",
        "message": _("Notification marked as read"),
    }


@frappe.whitelist()
def share_content(content_type, content_id, platform):
    """Log content sharing from portal"""
    
    user = frappe.session.user
    if user == "Guest":
        # Allow guest sharing for tracking
        pass
    
    try:
        # Log the share
        share = frappe.get_doc({
            "doctype": "Content Share",
            "content_type": content_type,
            "content_id": content_id,
            "platform": platform,
            "shared_by": user if user != "Guest" else None,
            "device_type": "Mobile",  # Can be detected from user agent
            "created_at": now_datetime(),
        })
        
        share.insert(ignore_permissions=True)
        frappe.db.commit()
        
        # Get share links for frontend
        from church_platform.sharing.api import get_share_links
        share_links = get_share_links(content_type, content_id)
        
        return {
            "status": "success",
            "message": _("Content shared"),
            "share_links": share_links,
        }
    
    except Exception as e:
        frappe.log_error(str(e), "Portal Share Error")
        return {
            "status": "error",
            "message": _("Failed to log share"),
        }


@frappe.whitelist()
def search_content(query, content_type="all"):
    """Search content in portal"""
    
    user = frappe.session.user
    if user == "Guest":
        frappe.throw(_("You must be logged in to search"), frappe.PermissionError)
    
    # Get member hierarchy scope
    from church_platform.hierarchy.permissions import get_user_hierarchy_scope
    hierarchy = get_user_hierarchy_scope(user)
    
    results = []
    
    if content_type in ["all", "post"]:
        # Search blog posts
        posts = frappe.db.sql("""
            SELECT 
                name, title, author, published_date,
                'Church Blog Post' as doctype
            FROM `tabChurch Blog Post`
            WHERE status = 'Published'
            AND (title LIKE %s OR content LIKE %s)
            LIMIT 10
        """, (f"%{query}%", f"%{query}%"), as_dict=True)
        results.extend(posts)
    
    if content_type in ["all", "event"]:
        # Search events
        events = frappe.db.sql("""
            SELECT 
                name, title, event_date, organized_by,
                'Event' as doctype
            FROM `tabEvent`
            WHERE status = 'Published'
            AND (title LIKE %s OR content LIKE %s)
            LIMIT 10
        """, (f"%{query}%", f"%{query}%"), as_dict=True)
        results.extend(events)
    
    if content_type in ["all", "announcement"]:
        # Search announcements
        announcements = frappe.db.sql("""
            SELECT 
                name, subject as title, announcement_date as event_date,
                'Announcement' as doctype
            FROM `tabAnnouncement`
            WHERE status = 'Published'
            AND (subject LIKE %s OR content LIKE %s)
            LIMIT 10
        """, (f"%{query}%", f"%{query}%"), as_dict=True)
        results.extend(announcements)
    
    return results


@frappe.whitelist()
def get_portal_announcements():
    """Get announcements for portal"""
    
    today = getdate()
    
    announcements = frappe.db.sql("""
        SELECT 
            name, subject, content, announcement_date,
            target_level, status
        FROM `tabAnnouncement`
        WHERE status = 'Published'
        AND announcement_date <= %s
        ORDER BY announcement_date DESC
        LIMIT 20
    """, (today,), as_dict=True)
    
    return announcements
