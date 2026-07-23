"""
Engagement Report - Query readership, comments, and shares by date range and criteria
"""

import frappe
from frappe.utils import getdate


def execute(filters=None):
    filters = filters or {}
    
    columns = get_columns()
    data = get_data(filters)
    
    return columns, data


def get_columns():
    return [
        {
            "fieldname": "date",
            "label": "Date",
            "fieldtype": "Date",
            "width": 120,
        },
        {
            "fieldname": "engagement_type",
            "label": "Type",
            "fieldtype": "Data",
            "width": 100,
        },
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
            "fieldname": "user",
            "label": "User",
            "fieldtype": "Link",
            "options": "User",
            "width": 150,
        },
        {
            "fieldname": "count",
            "label": "Count",
            "fieldtype": "Int",
            "width": 80,
        },
    ]


def get_data(filters):
    """Query engagement data"""
    
    start_date = filters.get("from_date") or frappe.utils.add_days(frappe.utils.getdate(), -30)
    end_date = filters.get("to_date") or frappe.utils.getdate()
    content_type = filters.get("content_type")
    author = filters.get("author")
    
    data = []
    
    # Get readership data
    readership = frappe.db.sql("""
        SELECT 
            read_date as date,
            'Read' as engagement_type,
            content_id,
            reader as user,
            COUNT(*) as count
        FROM `tabReadership Log`
        WHERE read_date BETWEEN %s AND %s
        GROUP BY read_date, content_id, reader
        ORDER BY read_date DESC
    """, (start_date, end_date), as_dict=True)
    
    # Get comments data
    comments = frappe.db.sql("""
        SELECT 
            DATE(created_on) as date,
            'Comment' as engagement_type,
            blog_post as content_id,
            commenter as user,
            COUNT(*) as count
        FROM `tabBlog Comment`
        WHERE created_on BETWEEN %s AND %s
        GROUP BY DATE(created_on), blog_post, commenter
        ORDER BY created_on DESC
    """, (start_date, end_date), as_dict=True)
    
    # Get shares data
    shares = frappe.db.sql("""
        SELECT 
            DATE(created_at) as date,
            'Share' as engagement_type,
            content_id,
            shared_by as user,
            COUNT(*) as count
        FROM `tabContent Share`
        WHERE created_at BETWEEN %s AND %s
        GROUP BY DATE(created_at), content_id, shared_by
        ORDER BY created_at DESC
    """, (start_date, end_date), as_dict=True)
    
    data = readership + comments + shares
    
    # Enrich with content titles
    for row in data:
        if row.get("content_id"):
            try:
                doc = frappe.get_doc("Church Blog Post", row["content_id"])
                row["content_title"] = doc.title
            except:
                row["content_title"] = "Content Not Found"
    
    return sorted(data, key=lambda x: x.get("date"), reverse=True)
