"""
Events Analytics Report - Track event attendance, engagement, and regional breakdown
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
            "fieldname": "event_name",
            "label": "Event",
            "fieldtype": "Link",
            "options": "Event",
            "width": 200,
        },
        {
            "fieldname": "event_title",
            "label": "Title",
            "fieldtype": "Data",
            "width": 200,
        },
        {
            "fieldname": "event_date",
            "label": "Date",
            "fieldtype": "Date",
            "width": 120,
        },
        {
            "fieldname": "organized_by",
            "label": "Organizer",
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "fieldname": "target_level",
            "label": "Target Level",
            "fieldtype": "Data",
            "width": 120,
        },
        {
            "fieldname": "rsvp_count",
            "label": "RSVPs",
            "fieldtype": "Int",
            "width": 80,
        },
        {
            "fieldname": "views",
            "label": "Views",
            "fieldtype": "Int",
            "width": 80,
        },
        {
            "fieldname": "status",
            "label": "Status",
            "fieldtype": "Data",
            "width": 100,
        },
    ]


def get_data(filters):
    """Query event analytics"""
    
    start_date = filters.get("from_date")
    end_date = filters.get("to_date")
    target_level = filters.get("target_level")
    status = filters.get("status")
    
    query = """
        SELECT 
            e.name as event_name,
            e.title as event_title,
            e.event_date,
            e.organized_by,
            e.target_level,
            e.status,
            COALESCE(e.views, 0) as views,
            (SELECT COUNT(*) FROM `tabEvent Attendance` 
             WHERE parent = e.name AND status = 'Confirmed') as rsvp_count
        FROM `tabEvent` e
        WHERE 1=1
    """
    
    params = []
    
    if start_date:
        query += " AND e.event_date >= %s"
        params.append(start_date)
    
    if end_date:
        query += " AND e.event_date <= %s"
        params.append(end_date)
    
    if target_level:
        query += " AND e.target_level = %s"
        params.append(target_level)
    
    if status:
        query += " AND e.status = %s"
        params.append(status)
    
    query += " ORDER BY e.event_date DESC LIMIT 100"
    
    data = frappe.db.sql(query, params, as_dict=True)
    
    return data


def get_event_by_region(region=None):
    """Get events broken down by region"""
    
    query = """
        SELECT 
            e.target_region,
            COUNT(e.name) as total_events,
            SUM(COALESCE(e.views, 0)) as total_views,
            (SELECT COUNT(*) FROM `tabEvent Attendance` ea 
             WHERE ea.parent IN (SELECT name FROM `tabEvent` WHERE target_region = e.target_region)) as total_attendees
        FROM `tabEvent` e
        WHERE e.status = 'Published'
    """
    
    params = []
    
    if region:
        query += " AND e.target_region = %s"
        params.append(region)
    
    query += " GROUP BY e.target_region ORDER BY total_views DESC"
    
    data = frappe.db.sql(query, params, as_dict=True)
    
    return data


def get_top_events(limit=10):
    """Get top events by attendance and engagement"""
    
    top_events = frappe.db.sql("""
        SELECT 
            e.name,
            e.title,
            e.event_date,
            COUNT(DISTINCT ea.parent) as rsvp_count,
            COALESCE(e.views, 0) as views
        FROM `tabEvent` e
        LEFT JOIN `tabEvent Attendance` ea ON ea.parent = e.name
        WHERE e.status = 'Published'
        GROUP BY e.name, e.title
        ORDER BY rsvp_count DESC, views DESC
        LIMIT %s
    """, (limit,), as_dict=True)
    
    return top_events
