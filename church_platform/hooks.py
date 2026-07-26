app_name = "church_platform"
app_title = "Church Platform"
app_publisher = "Church Platform Team"
app_description = "Comprehensive hierarchical content management and engagement system for church organizations"
app_email = "info@instentech.co.ke"
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
		"module": "Church Analytics"
	},
	{
		"report_name": "Share Analytics Report",
		"report_title": "Social Media Sharing Analytics",
		"ref_doctype": "Content Share",
		"module": "Church Analytics"
	},
	{
		"report_name": "Events Analytics Report",
		"report_title": "Event Analytics and Attendance",
		"ref_doctype": "Event",
		"module": "Church Analytics"
	},
	{
		"report_name": "Regional Performance Report",
		"report_title": "Regional Performance Dashboard",
		"ref_doctype": "Region",
		"module": "Church Analytics"
	},
]
