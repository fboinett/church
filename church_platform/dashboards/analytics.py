"""
Analytics functions for dashboard data aggregation.
Provides statistics, trends, and engagement metrics for each dashboard level.
"""

import frappe
from frappe.utils import getdate, get_datetime, now_datetime, add_days
from datetime import datetime, timedelta
from collections import defaultdict


def get_engagement_stats(filters=None):
    """Get engagement statistics for a given period and scope"""
    filters = filters or {}
    start_date = filters.get("start_date") or add_days(getdate(), -30)
    end_date = filters.get("end_date") or getdate()
    
    # Get readership data
    readership = frappe.db.sql("""
        SELECT 
            COUNT(*) as total_reads,
            COUNT(DISTINCT reader) as unique_readers,
            COUNT(DISTINCT content_id) as content_viewed
        FROM `tabReadership Log`
        WHERE read_date BETWEEN %s AND %s
    """, (start_date, end_date), as_dict=True)
    
    # Get comment data
    comments = frappe.db.sql("""
        SELECT 
            COUNT(*) as total_comments,
            COUNT(DISTINCT commenter) as unique_commenters
        FROM `tabBlog Comment`
        WHERE created_on BETWEEN %s AND %s
    """, (start_date, end_date), as_dict=True)
    
    # Get share data
    shares = frappe.db.sql("""
        SELECT 
            COUNT(*) as total_shares,
            COUNT(DISTINCT shared_by) as unique_sharers
        FROM `tabContent Share`
        WHERE created_at BETWEEN %s AND %s
    """, (start_date, end_date), as_dict=True)
    
    return {
        "readership": readership[0] if readership else {},
        "comments": comments[0] if comments else {},
        "shares": shares[0] if shares else {},
        "period": {
            "start": str(start_date),
            "end": str(end_date),
        }
    }


def get_share_analytics(content_type=None, limit=10):
    """Get sharing analytics grouped by content and platform"""
    query = """
        SELECT 
            content_id,
            platform,
            COUNT(*) as share_count,
            COUNT(DISTINCT shared_by) as unique_sharers,
            MAX(created_at) as last_shared
        FROM `tabContent Share`
    """
    params = []
    
    if content_type:
        query += " WHERE content_type = %s"
        params.append(content_type)
    
    query += """ 
        GROUP BY content_id, platform
        ORDER BY share_count DESC
        LIMIT %s
    """
    params.append(limit)
    
    results = frappe.db.sql(query, params, as_dict=True)
    
    # Enrich with content titles
    for result in results:
        doc = frappe.get_doc(result["content_type"], result["content_id"])
        result["title"] = doc.get("title") or doc.get("subject") or "Untitled"
    
    return results


def get_event_analytics(filters=None):
    """Get event analytics including attendance and engagement"""
    filters = filters or {}
    
    # Get event stats
    events = frappe.db.sql("""
        SELECT 
            name,
            title,
            event_date,
            status,
            target_level,
            target_region,
            (SELECT COUNT(*) FROM `tabEvent Attendance` 
             WHERE parent = `tabEvent`.name) as rsvp_count
        FROM `tabEvent`
        WHERE docstatus = 1
        ORDER BY event_date DESC
        LIMIT 10
    """, as_dict=True)
    
    # Get event engagement
    engagement = frappe.db.sql("""
        SELECT 
            content_id as event_id,
            COUNT(*) as total_reads,
            COUNT(DISTINCT reader) as unique_readers
        FROM `tabReadership Log`
        WHERE content_type = 'Event'
        GROUP BY content_id
        ORDER BY total_reads DESC
        LIMIT 5
    """, as_dict=True)
    
    return {
        "upcoming_events": events,
        "top_engaged_events": engagement,
    }


def get_readership_breakdown(group_by="region", filters=None):
    """Get readership broken down by region, author, or content type"""
    filters = filters or {}
    
    query = "SELECT "
    if group_by == "region":
        query += "r.name as category, COUNT(*) as reads, COUNT(DISTINCT reader) as unique_readers "
        query += "FROM `tabReadership Log` rl "
        query += "LEFT JOIN `tabChurch Blog Post` cbp ON rl.content_id = cbp.name "
        query += "LEFT JOIN `tabChurch` c ON cbp.target_church = c.name "
        query += "LEFT JOIN `tabSub Region` sr ON c.parent_sub_region = sr.name "
        query += "LEFT JOIN `tabRegion` r ON sr.parent_region = r.name "
        query += "WHERE r.name IS NOT NULL "
        query += "GROUP BY r.name ORDER BY reads DESC"
    
    elif group_by == "author":
        query += "cbp.author as category, COUNT(*) as reads, COUNT(DISTINCT reader) as unique_readers "
        query += "FROM `tabReadership Log` rl "
        query += "LEFT JOIN `tabChurch Blog Post` cbp ON rl.content_id = cbp.name "
        query += "WHERE cbp.author IS NOT NULL "
        query += "GROUP BY cbp.author ORDER BY reads DESC LIMIT 10"
    
    elif group_by == "content_type":
        query += "rl.content_type as category, COUNT(*) as reads, COUNT(DISTINCT reader) as unique_readers "
        query += "FROM `tabReadership Log` rl "
        query += "GROUP BY rl.content_type ORDER BY reads DESC"
    
    results = frappe.db.sql(query, as_dict=True)
    return results


def get_trending_content(limit=5):
    """Get trending content based on recent shares and reads"""
    
    # Recent shares + reads combined
    trending = frappe.db.sql("""
        SELECT 
            rl.content_id as content_id,
            rl.content_type as content_type,
            COUNT(DISTINCT CASE WHEN DATE(rl.read_date) = CURDATE() THEN rl.reader END) as today_reads,
            COUNT(DISTINCT CASE WHEN DATE(rl.read_date) >= DATE_SUB(CURDATE(), INTERVAL 7 DAY) 
                THEN rl.reader END) as week_reads,
            (SELECT COUNT(*) FROM `tabContent Share` cs 
             WHERE cs.content_id = rl.content_id AND DATE(cs.created_at) = CURDATE()) as today_shares,
            (SELECT COUNT(*) FROM `tabContent Share` cs 
             WHERE cs.content_id = rl.content_id) as total_shares
        FROM `tabReadership Log` rl
        GROUP BY rl.content_id, rl.content_type
        ORDER BY today_reads DESC, week_reads DESC
        LIMIT %s
    """, (limit,), as_dict=True)
    
    # Enrich with content details
    for item in trending:
        try:
            doc = frappe.get_doc(item["content_type"], item["content_id"])
            item["title"] = doc.get("title") or doc.get("subject") or "Untitled"
            item["excerpt"] = doc.get("content")[:100] if doc.get("content") else ""
        except:
            item["title"] = "Content Not Found"
            item["excerpt"] = ""
    
    return trending


def get_regional_performance(filters=None):
    """Compare performance across regions"""
    filters = filters or {}
    
    performance = frappe.db.sql("""
        SELECT 
            r.name as region_name,
            COUNT(DISTINCT c.name) as total_churches,
            COUNT(DISTINCT m.name) as total_members,
            COUNT(DISTINCT cbp.name) as total_posts,
            COUNT(DISTINCT e.name) as total_events,
            (SELECT COUNT(*) FROM `tabReadership Log` rl 
             WHERE rl.content_type = 'Church Blog Post' 
             AND rl.content_id IN (SELECT name FROM `tabChurch Blog Post` WHERE target_region = r.name)
            ) as region_reads
        FROM `tabRegion` r
        LEFT JOIN `tabSub Region` sr ON sr.parent_region = r.name
        LEFT JOIN `tabChurch` c ON c.parent_sub_region = sr.name
        LEFT JOIN `tabMember` m ON m.parent_church = c.name
        LEFT JOIN `tabChurch Blog Post` cbp ON cbp.target_region = r.name
        LEFT JOIN `tabEvent` e ON e.target_region = r.name
        GROUP BY r.name
        ORDER BY region_reads DESC
    """, as_dict=True)
    
    return performance


def get_author_performance(filters=None):
    """Get author engagement metrics"""
    filters = filters or {}
    
    authors = frappe.db.sql("""
        SELECT 
            cbp.author as author_name,
            COUNT(cbp.name) as posts_created,
            SUM(COALESCE(cbp.views, 0)) as total_views,
            (SELECT COUNT(*) FROM `tabContent Share` cs 
             WHERE cs.content_id = cbp.name) as total_shares,
            (SELECT COUNT(*) FROM `tabBlog Comment` bc 
             WHERE bc.blog_post = cbp.name AND bc.status = 'Approved') as approved_comments,
            MAX(cbp.published_date) as last_published
        FROM `tabChurch Blog Post` cbp
        WHERE cbp.status = 'Published'
        GROUP BY cbp.author
        ORDER BY total_views DESC
        LIMIT 10
    """, as_dict=True)
    
    return authors


def get_member_engagement_metrics(member_name):
    """Get personal engagement metrics for a member"""
    
    # Posts read
    reads = frappe.db.sql("""
        SELECT COUNT(*) as total_reads FROM `tabReadership Log`
        WHERE reader = %s
    """, (member_name,), as_dict=True)
    
    # Comments posted
    comments = frappe.db.sql("""
        SELECT COUNT(*) as pending, 
               SUM(CASE WHEN status = 'Approved' THEN 1 ELSE 0 END) as approved
        FROM `tabBlog Comment`
        WHERE commenter = %s
    """, (member_name,), as_dict=True)
    
    # Content shared
    shares = frappe.db.sql("""
        SELECT platform, COUNT(*) as count FROM `tabContent Share`
        WHERE shared_by = %s
        GROUP BY platform
    """, (member_name,), as_dict=True)
    
    # Achievements
    achievements = frappe.db.sql("""
        SELECT * FROM `tabAchievement`
        WHERE recipient = %s AND docstatus = 1
        ORDER BY created_on DESC
    """, (member_name,), as_dict=True)
    
    return {
        "reads": reads[0] if reads else {},
        "comments": comments[0] if comments else {},
        "shares": shares or [],
        "achievements": achievements or [],
    }
