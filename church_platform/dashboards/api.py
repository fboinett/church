"""
Dashboard API endpoints for fetching widget data.
All methods are whitelisted for frontend access.
"""

import frappe
from frappe.utils import getdate, add_days, now_datetime
from datetime import datetime, timedelta
from .analytics import (
    get_engagement_stats,
    get_share_analytics,
    get_event_analytics,
    get_readership_breakdown,
    get_trending_content,
    get_regional_performance,
    get_author_performance,
    get_member_engagement_metrics,
)


@frappe.whitelist()
def get_national_stats():
    """Get national level statistics"""
    if not frappe.has_permission("Region", "read"):
        frappe.throw("Insufficient permissions", frappe.PermissionError)
    
    stats = frappe.db.sql("""
        SELECT 
            COUNT(DISTINCT r.name) as total_regions,
            COUNT(DISTINCT sr.name) as total_sub_regions,
            COUNT(DISTINCT c.name) as total_churches,
            COUNT(DISTINCT m.name) as total_members
        FROM `tabRegion` r
        LEFT JOIN `tabSub Region` sr ON sr.parent_region = r.name
        LEFT JOIN `tabChurch` c ON c.parent_sub_region = sr.name
        LEFT JOIN `tabMember` m ON m.parent_church = c.name
    """, as_dict=True)
    
    return stats[0] if stats else {}


@frappe.whitelist()
def get_engagement_trend(days=30):
    """Get engagement trend over time"""
    days = int(days) if isinstance(days, str) else days
    start_date = add_days(getdate(), -days)
    
    trend = frappe.db.sql("""
        SELECT 
            DATE(read_date) as date,
            COUNT(*) as reads,
            COUNT(DISTINCT reader) as unique_readers,
            COUNT(DISTINCT content_id) as content_items
        FROM `tabReadership Log`
        WHERE read_date >= %s
        GROUP BY DATE(read_date)
        ORDER BY date ASC
    """, (start_date,), as_dict=True)
    
    return trend


@frappe.whitelist()
def get_trending_posts(limit=5):
    """Get trending posts"""
    limit = int(limit) if isinstance(limit, str) else limit
    trending = get_trending_content(limit)
    return trending


@frappe.whitelist()
def get_regional_breakdown():
    """Get readership breakdown by region"""
    breakdown = get_readership_breakdown("region")
    return breakdown


@frappe.whitelist()
def get_pending_approvals():
    """Get pending comment approvals"""
    if not frappe.has_permission("Blog Comment", "read"):
        return {"count": 0}
    
    pending = frappe.db.sql("""
        SELECT COUNT(*) as count FROM `tabBlog Comment`
        WHERE status = 'Pending'
    """, as_dict=True)
    
    return pending[0] if pending else {"count": 0}


@frappe.whitelist()
def get_regional_stats():
    """Get regional statistics for Bishop dashboard"""
    user = frappe.session.user
    
    # Get user's region from Church Leader doc
    leader = frappe.db.get_value("Church Leader", {"user": user}, "region")
    
    if not leader:
        return {}
    
    stats = frappe.db.sql("""
        SELECT 
            COUNT(DISTINCT sr.name) as total_sub_regions,
            COUNT(DISTINCT c.name) as total_churches,
            COUNT(DISTINCT m.name) as total_members,
            COUNT(DISTINCT cbp.name) as total_posts
        FROM `tabSub Region` sr
        LEFT JOIN `tabChurch` c ON c.parent_sub_region = sr.name
        LEFT JOIN `tabMember` m ON m.parent_church = c.name
        LEFT JOIN `tabChurch Blog Post` cbp ON cbp.target_region = %s
        WHERE sr.parent_region = %s
    """, (leader, leader), as_dict=True)
    
    return stats[0] if stats else {}


@frappe.whitelist()
def get_monthly_engagement():
    """Get engagement for current month"""
    today = getdate()
    month_start = today.replace(day=1)
    
    engagement = frappe.db.sql("""
        SELECT COUNT(*) as total_engagements FROM (
            SELECT reader as user FROM `tabReadership Log` 
            WHERE read_date BETWEEN %s AND %s
            UNION
            SELECT commenter as user FROM `tabBlog Comment`
            WHERE created_on BETWEEN %s AND %s
            UNION
            SELECT shared_by as user FROM `tabContent Share`
            WHERE created_at BETWEEN %s AND %s
        ) as combined_engagement
    """, (month_start, today, month_start, today, month_start, today), as_dict=True)
    
    return engagement[0] if engagement else {"total_engagements": 0}


@frappe.whitelist()
def get_recent_content(limit=5):
    """Get recently published content"""
    limit = int(limit) if isinstance(limit, str) else limit
    
    content = frappe.db.sql("""
        SELECT 
            'Church Blog Post' as doctype,
            name,
            title,
            author,
            published_date,
            views
        FROM `tabChurch Blog Post`
        WHERE status = 'Published'
        ORDER BY published_date DESC
        LIMIT %s
    """, (limit,), as_dict=True)
    
    return content


@frappe.whitelist()
def get_subregional_performance():
    """Get performance breakdown by sub-region"""
    user = frappe.session.user
    leader = frappe.db.get_value("Church Leader", {"user": user}, "parent_sub_region")
    
    if not leader:
        return []
    
    performance = frappe.db.sql("""
        SELECT 
            sr.name as sub_region,
            COUNT(DISTINCT c.name) as churches,
            COUNT(DISTINCT m.name) as members,
            (SELECT COUNT(*) FROM `tabReadership Log` rl 
             WHERE rl.content_type = 'Church Blog Post') as reads
        FROM `tabSub Region` sr
        LEFT JOIN `tabChurch` c ON c.parent_sub_region = sr.name
        LEFT JOIN `tabMember` m ON m.parent_church = c.name
        WHERE sr.name = %s
        GROUP BY sr.name
    """, (leader,), as_dict=True)
    
    return performance


@frappe.whitelist()
def get_active_events():
    """Get count of active upcoming events"""
    today = getdate()
    
    events = frappe.db.sql("""
        SELECT COUNT(*) as count FROM `tabEvent`
        WHERE event_date >= %s AND status = 'Published'
    """, (today,), as_dict=True)
    
    return events[0] if events else {"count": 0}


@frappe.whitelist()
def get_top_authors():
    """Get most active authors"""
    authors = get_author_performance()
    return authors[:5] if authors else []


@frappe.whitelist()
def get_subregional_stats():
    """Get sub-regional statistics"""
    user = frappe.session.user
    sub_region = frappe.db.get_value("Church Leader", {"user": user}, "parent_sub_region")
    
    if not sub_region:
        return {}
    
    stats = frappe.db.sql("""
        SELECT 
            COUNT(DISTINCT c.name) as total_churches,
            COUNT(DISTINCT m.name) as total_members,
            COUNT(DISTINCT cl.name) as total_leaders
        FROM `tabChurch` c
        LEFT JOIN `tabMember` m ON m.parent_church = c.name
        LEFT JOIN `tabChurch Leader` cl ON cl.parent_church = c.name
        WHERE c.parent_sub_region = %s
    """, (sub_region,), as_dict=True)
    
    return stats[0] if stats else {}


@frappe.whitelist()
def get_subregional_engagement():
    """Get engagement trend for sub-region"""
    days = 30
    start_date = add_days(getdate(), -days)
    
    trend = frappe.db.sql("""
        SELECT 
            DATE(read_date) as date,
            COUNT(*) as reads
        FROM `tabReadership Log`
        WHERE read_date >= %s
        GROUP BY DATE(read_date)
        ORDER BY date ASC
    """, (start_date,), as_dict=True)
    
    return trend


@frappe.whitelist()
def get_church_performance():
    """Get top performing churches"""
    user = frappe.session.user
    sub_region = frappe.db.get_value("Church Leader", {"user": user}, "parent_sub_region")
    
    if not sub_region:
        return []
    
    churches = frappe.db.sql("""
        SELECT 
            c.name,
            c.church_name,
            COUNT(m.name) as member_count,
            (SELECT COUNT(*) FROM `tabEvent` e WHERE e.target_church = c.name) as event_count,
            (SELECT SUM(views) FROM `tabReadership Log` rl 
             WHERE rl.content_type = 'Church Blog Post') as total_reads
        FROM `tabChurch` c
        LEFT JOIN `tabMember` m ON m.parent_church = c.name
        WHERE c.parent_sub_region = %s
        GROUP BY c.name
        ORDER BY member_count DESC
        LIMIT 5
    """, (sub_region,), as_dict=True)
    
    return churches


@frappe.whitelist()
def get_recent_activities():
    """Get recent activities across the sub-region"""
    days = 7
    start_date = add_days(getdate(), -days)
    
    activities = frappe.db.sql("""
        SELECT 'Post' as type, title, published_date as date, author 
        FROM `tabChurch Blog Post`
        WHERE published_date >= %s AND status = 'Published'
        UNION ALL
        SELECT 'Event', title, event_date, organized_by 
        FROM `tabEvent`
        WHERE event_date >= %s
        ORDER BY date DESC
        LIMIT 10
    """, (start_date, start_date), as_dict=True)
    
    return activities


@frappe.whitelist()
def get_member_stats():
    """Get member statistics"""
    stats = frappe.db.sql("""
        SELECT COUNT(DISTINCT name) as total_members FROM `tabMember`
        WHERE docstatus = 1
    """, as_dict=True)
    
    return stats[0] if stats else {"total_members": 0}


@frappe.whitelist()
def get_content_calendar():
    """Get content published this month"""
    today = getdate()
    month_start = today.replace(day=1)
    
    calendar = frappe.db.sql("""
        SELECT 
            DATE(published_date) as date,
            COUNT(*) as posts
        FROM `tabChurch Blog Post`
        WHERE published_date BETWEEN %s AND %s AND status = 'Published'
        GROUP BY DATE(published_date)
        ORDER BY date ASC
    """, (month_start, today), as_dict=True)
    
    return calendar


@frappe.whitelist()
def get_church_stats():
    """Get statistics for a specific church (Vicar view)"""
    user = frappe.session.user
    church = frappe.db.get_value("Church Leader", {"user": user}, "parent_church")
    
    if not church:
        return {}
    
    stats = frappe.db.sql("""
        SELECT 
            COUNT(m.name) as active_members,
            COUNT(e.name) as events,
            (SELECT COUNT(*) FROM `tabChurch Blog Post` WHERE target_church = %s) as posts
        FROM `tabChurch` c
        LEFT JOIN `tabMember` m ON m.parent_church = c.name
        LEFT JOIN `tabEvent` e ON e.target_church = c.name
        WHERE c.name = %s
    """, (church, church), as_dict=True)
    
    return stats[0] if stats else {}


@frappe.whitelist()
def get_weekly_engagement():
    """Get engagement for this week"""
    today = getdate()
    week_start = today - timedelta(days=today.weekday())
    
    engagement = frappe.db.sql("""
        SELECT COUNT(*) as count FROM (
            SELECT reader FROM `tabReadership Log` 
            WHERE read_date BETWEEN %s AND %s
            UNION
            SELECT commenter FROM `tabBlog Comment`
            WHERE created_on BETWEEN %s AND %s
        ) as weekly
    """, (week_start, today, week_start, today), as_dict=True)
    
    return engagement[0] if engagement else {"count": 0}


@frappe.whitelist()
def get_church_events():
    """Get upcoming church events"""
    user = frappe.session.user
    church = frappe.db.get_value("Church Leader", {"user": user}, "parent_church")
    
    if not church:
        return []
    
    today = getdate()
    events = frappe.db.sql("""
        SELECT name, title, event_date, status 
        FROM `tabEvent`
        WHERE target_church = %s AND event_date >= %s AND status = 'Published'
        ORDER BY event_date ASC
        LIMIT 10
    """, (church, today), as_dict=True)
    
    return events


@frappe.whitelist()
def get_member_activity():
    """Get member activity chart data for this week"""
    today = getdate()
    week_start = today - timedelta(days=today.weekday())
    
    activity = frappe.db.sql("""
        SELECT 
            DATE(read_date) as date,
            COUNT(*) as activity_count
        FROM `tabReadership Log`
        WHERE read_date BETWEEN %s AND %s
        GROUP BY DATE(read_date)
        ORDER BY date ASC
    """, (week_start, today), as_dict=True)
    
    return activity


@frappe.whitelist()
def get_church_posts():
    """Get recent posts for this church"""
    user = frappe.session.user
    church = frappe.db.get_value("Church Leader", {"user": user}, "parent_church")
    
    if not church:
        return []
    
    posts = frappe.db.sql("""
        SELECT name, title, author, published_date, views, status
        FROM `tabChurch Blog Post`
        WHERE target_church = %s
        ORDER BY published_date DESC
        LIMIT 5
    """, (church,), as_dict=True)
    
    return posts


@frappe.whitelist()
def get_pending_moderation():
    """Get pending comments for moderation by this user"""
    user = frappe.session.user
    
    pending = frappe.db.sql("""
        SELECT COUNT(*) as count FROM `tabBlog Comment` bc
        JOIN `tabChurch Blog Post` cbp ON bc.blog_post = cbp.name
        WHERE cbp.author = %s AND bc.status = 'Pending'
    """, (user,), as_dict=True)
    
    return pending[0] if pending else {"count": 0}


@frappe.whitelist()
def get_member_welcome():
    """Get personalized welcome card for member"""
    user = frappe.session.user
    member = frappe.db.get_value("Member", {"user": user}, "name")
    
    if not member:
        return {"message": "Welcome"}
    
    member_doc = frappe.get_doc("Member", member)
    return {
        "message": f"Welcome back, {member_doc.member_name}!",
        "member_id": member,
        "church": member_doc.parent_church,
    }


@frappe.whitelist()
def get_my_achievements():
    """Get member's achievements"""
    user = frappe.session.user
    member = frappe.db.get_value("Member", {"user": user}, "name")
    
    if not member:
        return []
    
    achievements = frappe.db.sql("""
        SELECT name, title, description, awarded_date
        FROM `tabAchievement`
        WHERE recipient = %s AND docstatus = 1
        ORDER BY awarded_date DESC
    """, (member,), as_dict=True)
    
    return achievements


@frappe.whitelist()
def get_personalized_feed():
    """Get personalized content feed for member"""
    user = frappe.session.user
    member = frappe.db.get_value("Member", {"user": user}, "name")
    
    if not member:
        return []
    
    member_doc = frappe.get_doc("Member", member)
    
    # Get content targeted to member's level and below
    feed = frappe.db.sql("""
        SELECT 
            name, title, author, published_date, views, 
            target_level, status
        FROM `tabChurch Blog Post`
        WHERE status = 'Published'
        AND (
            target_level = 'Local' OR 
            target_level = 'Sub-Regional' OR 
            target_level = 'Regional' OR 
            target_level = 'National'
        )
        ORDER BY published_date DESC
        LIMIT 20
    """, as_dict=True)
    
    return feed


@frappe.whitelist()
def get_member_events():
    """Get events relevant to member"""
    user = frappe.session.user
    member = frappe.db.get_value("Member", {"user": user}, "name")
    
    if not member:
        return []
    
    today = getdate()
    events = frappe.db.sql("""
        SELECT name, title, event_date, status, target_level
        FROM `tabEvent`
        WHERE event_date >= %s AND status = 'Published'
        ORDER BY event_date ASC
        LIMIT 10
    """, (today,), as_dict=True)
    
    return events


@frappe.whitelist()
def get_member_engagement_stats():
    """Get member's engagement statistics"""
    user = frappe.session.user
    member = frappe.db.get_value("Member", {"user": user}, "name")
    
    if not member:
        return {}
    
    metrics = get_member_engagement_metrics(member)
    return metrics


@frappe.whitelist()
def get_member_comments():
    """Get member's recent comments"""
    user = frappe.session.user
    member = frappe.db.get_value("Member", {"user": user}, "name")
    
    if not member:
        return []
    
    comments = frappe.db.sql("""
        SELECT name, blog_post, content, status, created_on
        FROM `tabBlog Comment`
        WHERE commenter = %s
        ORDER BY created_on DESC
        LIMIT 5
    """, (member,), as_dict=True)
    
    return comments
