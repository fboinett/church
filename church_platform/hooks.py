app_name = "church_platform"
app_title = "Church Platform"
app_publisher = "Church Platform Team"
app_description = "Comprehensive hierarchical content management and engagement system for church organizations"
app_email = "support@churchplatform.local"
app_license = "MIT"
app_version = "1.0.0"

# Fixtures
fixtures = [
	{"dt": "Region", "filters": [["name", "!=", ""]]},
	{"dt": "Sub Region", "filters": [["name", "!=", ""]]},
	{"dt": "Church", "filters": [["name", "!=", ""]]},
	{"dt": "Church Leader", "filters": [["name", "!=", ""]]},
	{"dt": "Member", "filters": [["name", "!=", ""]]},
	{"dt": "Announcement", "filters": [["status", "=", "Published"]]},
	{"dt": "Event", "filters": [["status", "!=", "Cancelled"]]},
	{"dt": "Church Blog Post", "filters": [["status", "=", "Published"]]},
	{"dt": "Content Share", "filters": [["name", "!=", ""]]},
]

# Whitelisted API methods
standard_queries = {
	"church_platform.sharing.api.get_share_links",
	"church_platform.sharing.api.log_share",
	"church_platform.sharing.api.get_share_stats",
	"church_platform.sharing.api.get_trending_content",
	# Dashboard APIs
	"church_platform.dashboards.api.get_national_stats",
	"church_platform.dashboards.api.get_engagement_trend",
	"church_platform.dashboards.api.get_trending_posts",
	"church_platform.dashboards.api.get_regional_breakdown",
	"church_platform.dashboards.api.get_pending_approvals",
	"church_platform.dashboards.api.get_regional_stats",
	"church_platform.dashboards.api.get_monthly_engagement",
	"church_platform.dashboards.api.get_recent_content",
	"church_platform.dashboards.api.get_subregional_performance",
	"church_platform.dashboards.api.get_active_events",
	"church_platform.dashboards.api.get_top_authors",
	"church_platform.dashboards.api.get_subregional_stats",
	"church_platform.dashboards.api.get_subregional_engagement",
	"church_platform.dashboards.api.get_church_performance",
	"church_platform.dashboards.api.get_recent_activities",
	"church_platform.dashboards.api.get_member_stats",
	"church_platform.dashboards.api.get_content_calendar",
	"church_platform.dashboards.api.get_church_stats",
	"church_platform.dashboards.api.get_weekly_engagement",
	"church_platform.dashboards.api.get_church_events",
	"church_platform.dashboards.api.get_member_activity",
	"church_platform.dashboards.api.get_church_posts",
	"church_platform.dashboards.api.get_pending_moderation",
	"church_platform.dashboards.api.get_member_welcome",
	"church_platform.dashboards.api.get_my_achievements",
	"church_platform.dashboards.api.get_personalized_feed",
	"church_platform.dashboards.api.get_member_events",
	"church_platform.dashboards.api.get_member_engagement_stats",
	"church_platform.dashboards.api.get_member_comments",
	# Portal APIs
	"church_platform.portal.api.submit_comment",
	"church_platform.portal.api.rsvp_event",
	"church_platform.portal.api.update_member_profile",
	"church_platform.portal.api.get_member_notifications",
	"church_platform.portal.api.mark_notification_read",
	"church_platform.portal.api.share_content",
	"church_platform.portal.api.search_content",
	"church_platform.portal.api.get_portal_announcements",
}

# Permissions for hierarchy and content
has_permission = {
	"Region": "church_platform.hierarchy.permissions.region_has_permission",
	"Sub Region": "church_platform.hierarchy.permissions.subregion_has_permission",
	"Church": "church_platform.hierarchy.permissions.church_has_permission",
	"Announcement": "church_platform.content_management.permissions.announcement_has_permission",
	"Event": "church_platform.content_management.permissions.event_has_permission",
	"Church Blog Post": "church_platform.content_management.permissions.blog_post_has_permission",
}

# Custom Reports
reports = [
	{
		"report_name": "Engagement Report",
		"report_title": "Engagement Analytics",
		"ref_doctype": "Church Blog Post",
		"module": "Church Platform"
	},
	{
		"report_name": "Share Analytics Report",
		"report_title": "Social Media Sharing Analytics",
		"ref_doctype": "Content Share",
		"module": "Church Platform"
	},
	{
		"report_name": "Events Analytics Report",
		"report_title": "Event Analytics and Attendance",
		"ref_doctype": "Event",
		"module": "Church Platform"
	},
	{
		"report_name": "Regional Performance Report",
		"report_title": "Regional Performance Dashboard",
		"ref_doctype": "Region",
		"module": "Church Platform"
	},
]

