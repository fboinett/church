"""
Configuration module for Church Platform
"""

def get_data():
	return {
		"Hierarchy Management": {
			"color": "#FF6B6B",
			"icon": "sitemap",
			"items": [
				{
					"type": "doctype",
					"name": "Region",
					"description": "Diocese - Regional level in church hierarchy",
				},
				{
					"type": "doctype",
					"name": "Sub Region",
					"description": "Archdeaconry - Sub-regional level in church hierarchy",
				},
				{
					"type": "doctype",
					"name": "Church",
					"description": "Parish - Local church in hierarchy",
				},
			]
		},
		"User Management": {
			"color": "#4ECDC4",
			"icon": "users",
			"items": [
				{
					"type": "doctype",
					"name": "Church Leader",
					"description": "Leaders at each hierarchy level",
				},
				{
					"type": "doctype",
					"name": "Member",
					"description": "Church members with portal access",
				},
			]
		},
	}
