"""
Regional Performance Report - Compare performance across regions
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
            "fieldname": "region_name",
            "label": "Region",
            "fieldtype": "Link",
            "options": "Region",
            "width": 150,
        },
        {
            "fieldname": "sub_regions",
            "label": "Sub-Regions",
            "fieldtype": "Int",
            "width": 100,
        },
        {
            "fieldname": "churches",
            "label": "Churches",
            "fieldtype": "Int",
            "width": 100,
        },
        {
            "fieldname": "members",
            "label": "Members",
            "fieldtype": "Int",
            "width": 100,
        },
        {
            "fieldname": "leaders",
            "label": "Leaders",
            "fieldtype": "Int",
            "width": 100,
        },
        {
            "fieldname": "total_posts",
            "label": "Posts",
            "fieldtype": "Int",
            "width": 80,
        },
        {
            "fieldname": "total_events",
            "label": "Events",
            "fieldtype": "Int",
            "width": 80,
        },
        {
            "fieldname": "total_reads",
            "label": "Reads",
            "fieldtype": "Int",
            "width": 80,
        },
        {
            "fieldname": "total_shares",
            "label": "Shares",
            "fieldtype": "Int",
            "width": 80,
        },
    ]


def get_data(filters):
    """Query regional performance data"""
    
    data = frappe.db.sql("""
        SELECT 
            r.name as region_name,
            COUNT(DISTINCT sr.name) as sub_regions,
            COUNT(DISTINCT c.name) as churches,
            COUNT(DISTINCT m.name) as members,
            COUNT(DISTINCT cl.name) as leaders,
            COUNT(DISTINCT cbp.name) as total_posts,
            COUNT(DISTINCT e.name) as total_events,
            (SELECT COUNT(*) FROM `tabReadership Log` rl 
             WHERE rl.content_type IN ('Church Blog Post', 'Event', 'Announcement')) as total_reads,
            (SELECT COUNT(*) FROM `tabContent Share` cs 
             WHERE cs.content_id IN (SELECT name FROM `tabChurch Blog Post` WHERE target_region = r.name)) as total_shares
        FROM `tabRegion` r
        LEFT JOIN `tabSub Region` sr ON sr.parent_region = r.name
        LEFT JOIN `tabChurch` c ON c.parent_sub_region = sr.name
        LEFT JOIN `tabMember` m ON m.parent_church = c.name
        LEFT JOIN `tabChurch Leader` cl ON cl.parent_church = c.name
        LEFT JOIN `tabChurch Blog Post` cbp ON cbp.target_region = r.name
        LEFT JOIN `tabEvent` e ON e.target_region = r.name
        GROUP BY r.name
        ORDER BY total_reads DESC
    """, as_dict=True)
    
    return data


def get_regional_engagement_trend():
    """Get engagement trend by region"""
    
    trend = frappe.db.sql("""
        SELECT 
            DATE(read_date) as date,
            'Engagement' as metric,
            COUNT(*) as value
        FROM `tabReadership Log`
        GROUP BY DATE(read_date)
        ORDER BY date DESC
        LIMIT 30
    """, as_dict=True)
    
    return trend


def get_region_member_breakdown():
    """Get member count breakdown by region"""
    
    breakdown = frappe.db.sql("""
        SELECT 
            r.name as region,
            COUNT(DISTINCT m.name) as members
        FROM `tabRegion` r
        LEFT JOIN `tabSub Region` sr ON sr.parent_region = r.name
        LEFT JOIN `tabChurch` c ON c.parent_sub_region = sr.name
        LEFT JOIN `tabMember` m ON m.parent_church = c.name
        GROUP BY r.name
        ORDER BY members DESC
    """, as_dict=True)
    
    return breakdown
