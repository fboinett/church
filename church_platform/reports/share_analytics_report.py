"""
Share Analytics Report - Track shares by platform, content, and trends
"""

import frappe


def execute(filters=None):
    filters = filters or {}
    
    columns = get_columns()
    data = get_data(filters)
    
    return columns, data


def get_columns():
    return [
        {
            "fieldname": "content_id",
            "label": "Content",
            "fieldtype": "Link",
            "options": "Church Blog Post",
            "width": 150,
        },
        {
            "fieldname": "content_title",
            "label": "Title",
            "fieldtype": "Data",
            "width": 200,
        },
        {
            "fieldname": "platform",
            "label": "Platform",
            "fieldtype": "Data",
            "width": 100,
        },
        {
            "fieldname": "share_count",
            "label": "Shares",
            "fieldtype": "Int",
            "width": 80,
        },
        {
            "fieldname": "unique_sharers",
            "label": "Unique Sharers",
            "fieldtype": "Int",
            "width": 120,
        },
        {
            "fieldname": "last_shared",
            "label": "Last Shared",
            "fieldtype": "Datetime",
            "width": 150,
        },
        {
            "fieldname": "avg_shares_per_day",
            "label": "Avg/Day",
            "fieldtype": "Float",
            "width": 100,
        },
    ]


def get_data(filters):
    """Query share analytics"""
    
    platform = filters.get("platform")
    content_type = filters.get("content_type")
    sort_by = filters.get("sort_by") or "share_count"
    
    query = """
        SELECT 
            content_id,
            platform,
            COUNT(*) as share_count,
            COUNT(DISTINCT shared_by) as unique_sharers,
            MAX(created_at) as last_shared,
            ROUND(COUNT(*) / DATEDIFF(MAX(created_at), MIN(created_at) + 1), 2) as avg_shares_per_day
        FROM `tabContent Share`
        WHERE 1=1
    """
    
    params = []
    
    if platform:
        query += " AND platform = %s"
        params.append(platform)
    
    query += """
        GROUP BY content_id, platform
        ORDER BY %s DESC
        LIMIT 100
    """ % sort_by
    
    data = frappe.db.sql(query, params, as_dict=True)
    
    # Enrich with content titles
    for row in data:
        if row.get("content_id"):
            try:
                doc = frappe.get_doc("Church Blog Post", row["content_id"])
                row["content_title"] = doc.title
            except:
                row["content_title"] = "Content Not Found"
    
    return data


def get_trending_content():
    """Get trending content based on recent shares"""
    
    trending = frappe.db.sql("""
        SELECT 
            content_id,
            COUNT(*) as total_shares,
            COUNT(DISTINCT shared_by) as unique_sharers,
            DATE(created_at) as share_date
        FROM `tabContent Share`
        WHERE DATE(created_at) = CURDATE()
        GROUP BY content_id
        ORDER BY total_shares DESC
        LIMIT 10
    """, as_dict=True)
    
    # Enrich with content details
    for item in trending:
        try:
            doc = frappe.get_doc("Church Blog Post", item["content_id"])
            item["title"] = doc.title
            item["author"] = doc.author
            item["views"] = doc.views or 0
        except:
            pass
    
    return trending
