"""
Workspace configurations for each leadership level.
Each workspace is customized to show role-specific dashboards and content.
"""

import frappe
from frappe import _


def get_archbishop_workspace():
    """National level dashboard - Archbishop/Presiding Bishop view"""
    return {
        "label": "National Dashboard",
        "icon": "fa-crown",
        "pages": [
            {
                "title": _("National Overview"),
                "name": "national-overview",
                "description": _("High-level national statistics and KPIs"),
            },
            {
                "title": _("Regional Performance"),
                "name": "regional-performance",
                "description": _("Performance metrics for all regions"),
            },
        ],
        "widgets": [
            {
                "name": "National Statistics",
                "type": "card",
                "label": "Total Regions",
                "method": "church_platform.dashboards.api.get_national_stats",
            },
            {
                "name": "Engagement Overview",
                "type": "chart",
                "label": "National Engagement Trend",
                "method": "church_platform.dashboards.api.get_engagement_trend",
            },
            {
                "name": "Top Posts",
                "type": "list",
                "label": "Most Shared Content",
                "method": "church_platform.dashboards.api.get_trending_posts",
            },
            {
                "name": "Regional Breakdown",
                "type": "chart",
                "label": "Readership by Region",
                "method": "church_platform.dashboards.api.get_regional_breakdown",
            },
            {
                "name": "Pending Approvals",
                "type": "badge",
                "label": "Comments Awaiting Approval",
                "method": "church_platform.dashboards.api.get_pending_approvals",
            },
            {
                "name": "Announcements",
                "type": "shortcut",
                "label": "Create National Announcement",
                "doctype": "Announcement",
                "filter": "target_level",
                "filter_value": "National",
            },
        ],
        "shortcuts": [
            {"label": "New Announcement", "name": "Announcement", "color": "blue"},
            {"label": "New Event", "name": "Event", "color": "green"},
            {"label": "New Blog Post", "name": "Church Blog Post", "color": "purple"},
            {"label": "View Regions", "name": "Region", "color": "orange"},
            {"label": "Manage Leaders", "name": "Church Leader", "color": "red"},
        ],
    }


def get_bishop_workspace():
    """Regional level dashboard - Bishop view"""
    return {
        "label": "Regional Dashboard",
        "icon": "fa-layer-group",
        "pages": [
            {
                "title": _("Regional Overview"),
                "name": "regional-overview",
                "description": _("Region-specific statistics and performance"),
            },
            {
                "title": _("Sub-Regional Breakdown"),
                "name": "subregional-breakdown",
                "description": _("Performance across sub-regions"),
            },
        ],
        "widgets": [
            {
                "name": "Regional Statistics",
                "type": "card",
                "label": "Churches in Region",
                "method": "church_platform.dashboards.api.get_regional_stats",
            },
            {
                "name": "Engagement This Month",
                "type": "number",
                "label": "Total Engagements",
                "method": "church_platform.dashboards.api.get_monthly_engagement",
            },
            {
                "name": "Recent Content",
                "type": "list",
                "label": "Latest Regional Posts",
                "method": "church_platform.dashboards.api.get_recent_content",
            },
            {
                "name": "Sub-Regional Performance",
                "type": "chart",
                "label": "Performance by Sub-Region",
                "method": "church_platform.dashboards.api.get_subregional_performance",
            },
            {
                "name": "Active Events",
                "type": "number",
                "label": "Upcoming Events",
                "method": "church_platform.dashboards.api.get_active_events",
            },
            {
                "name": "Top Authors",
                "type": "list",
                "label": "Most Active Authors",
                "method": "church_platform.dashboards.api.get_top_authors",
            },
        ],
        "shortcuts": [
            {"label": "New Regional Announcement", "name": "Announcement", "color": "blue"},
            {"label": "New Event", "name": "Event", "color": "green"},
            {"label": "My Posts", "name": "Church Blog Post", "color": "purple"},
            {"label": "Sub-Regions", "name": "Sub Region", "color": "orange"},
            {"label": "Leaders", "name": "Church Leader", "color": "red"},
        ],
    }


def get_archdeacon_workspace():
    """Sub-Regional level dashboard - Archdeacon view"""
    return {
        "label": "Sub-Regional Dashboard",
        "icon": "fa-network-wired",
        "pages": [
            {
                "title": _("Sub-Regional Overview"),
                "name": "subregional-overview",
                "description": _("Sub-regional statistics and activities"),
            },
            {
                "title": _("Church Performance"),
                "name": "church-performance",
                "description": _("Individual church metrics"),
            },
        ],
        "widgets": [
            {
                "name": "Sub-Regional Stats",
                "type": "card",
                "label": "Total Churches",
                "method": "church_platform.dashboards.api.get_subregional_stats",
            },
            {
                "name": "Engagement Metrics",
                "type": "chart",
                "label": "Engagement Trend",
                "method": "church_platform.dashboards.api.get_subregional_engagement",
            },
            {
                "name": "Church Performance",
                "type": "list",
                "label": "Top Performing Churches",
                "method": "church_platform.dashboards.api.get_church_performance",
            },
            {
                "name": "Recent Activities",
                "type": "list",
                "label": "Latest Activities",
                "method": "church_platform.dashboards.api.get_recent_activities",
            },
            {
                "name": "Member Statistics",
                "type": "number",
                "label": "Total Active Members",
                "method": "church_platform.dashboards.api.get_member_stats",
            },
            {
                "name": "Content Calendar",
                "type": "chart",
                "label": "Content Published This Month",
                "method": "church_platform.dashboards.api.get_content_calendar",
            },
        ],
        "shortcuts": [
            {"label": "New Post", "name": "Church Blog Post", "color": "blue"},
            {"label": "New Event", "name": "Event", "color": "green"},
            {"label": "Announcements", "name": "Announcement", "color": "orange"},
            {"label": "Churches", "name": "Church", "color": "purple"},
            {"label": "Members", "name": "Member", "color": "red"},
        ],
    }


def get_vicar_workspace():
    """Local Church level dashboard - Vicar view"""
    return {
        "label": "Church Dashboard",
        "icon": "fa-church",
        "pages": [
            {
                "title": _("Church Overview"),
                "name": "church-overview",
                "description": _("Local church statistics and activities"),
            },
            {
                "title": _("Member Engagement"),
                "name": "member-engagement",
                "description": _("Member activity and engagement metrics"),
            },
        ],
        "widgets": [
            {
                "name": "Church Statistics",
                "type": "card",
                "label": "Active Members",
                "method": "church_platform.dashboards.api.get_church_stats",
            },
            {
                "name": "This Week's Engagement",
                "type": "number",
                "label": "Weekly Engagements",
                "method": "church_platform.dashboards.api.get_weekly_engagement",
            },
            {
                "name": "Upcoming Events",
                "type": "list",
                "label": "Church Events",
                "method": "church_platform.dashboards.api.get_church_events",
            },
            {
                "name": "Member Activity",
                "type": "chart",
                "label": "Member Engagement This Week",
                "method": "church_platform.dashboards.api.get_member_activity",
            },
            {
                "name": "Recent Posts",
                "type": "list",
                "label": "Latest Church Posts",
                "method": "church_platform.dashboards.api.get_church_posts",
            },
            {
                "name": "Pending Moderation",
                "type": "number",
                "label": "Comments to Review",
                "method": "church_platform.dashboards.api.get_pending_moderation",
            },
        ],
        "shortcuts": [
            {"label": "New Event", "name": "Event", "color": "blue"},
            {"label": "New Post", "name": "Church Blog Post", "color": "green"},
            {"label": "Announcement", "name": "Announcement", "color": "orange"},
            {"label": "My Members", "name": "Member", "color": "purple"},
            {"label": "My Leaders", "name": "Church Leader", "color": "red"},
        ],
    }


def get_member_workspace():
    """Member portal dashboard - Personal view"""
    return {
        "label": "Member Dashboard",
        "icon": "fa-user-circle",
        "pages": [
            {
                "title": _("My Dashboard"),
                "name": "member-dashboard",
                "description": _("Personalized content and engagement"),
            },
            {
                "title": _("My Profile"),
                "name": "member-profile",
                "description": _("Profile and achievements"),
            },
        ],
        "widgets": [
            {
                "name": "Member Welcome",
                "type": "card",
                "label": "Welcome Card",
                "method": "church_platform.dashboards.api.get_member_welcome",
            },
            {
                "name": "My Achievements",
                "type": "badge",
                "label": "Achievements Earned",
                "method": "church_platform.dashboards.api.get_my_achievements",
            },
            {
                "name": "Personalized Feed",
                "type": "list",
                "label": "Content For You",
                "method": "church_platform.dashboards.api.get_personalized_feed",
            },
            {
                "name": "My Events",
                "type": "list",
                "label": "My Events",
                "method": "church_platform.dashboards.api.get_member_events",
            },
            {
                "name": "Engagement Stats",
                "type": "chart",
                "label": "My Engagement This Month",
                "method": "church_platform.dashboards.api.get_member_engagement_stats",
            },
            {
                "name": "My Comments",
                "type": "list",
                "label": "My Recent Comments",
                "method": "church_platform.dashboards.api.get_member_comments",
            },
        ],
        "shortcuts": [
            {"label": "View Events", "name": "Event", "color": "blue"},
            {"label": "View Posts", "name": "Church Blog Post", "color": "green"},
            {"label": "My Profile", "name": "Member", "color": "purple"},
            {"label": "Browse Content", "name": "Announcement", "color": "orange"},
        ],
    }
