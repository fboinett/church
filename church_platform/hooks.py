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
]

# Permissions for hierarchy
has_permission = {
	"Region": "church_platform.hierarchy.permissions.region_has_permission",
	"Sub Region": "church_platform.hierarchy.permissions.subregion_has_permission",
	"Church": "church_platform.hierarchy.permissions.church_has_permission",
}
