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
