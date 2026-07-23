"""
Hierarchy-aware permissions for Church Platform
"""

import frappe


def get_user_hierarchy_scope():
	"""
	Get the current user's hierarchy scope.
	Returns: {
		'level': 'National' | 'Regional' | 'Sub-Regional' | 'Local',
		'region': region_id or None,
		'sub_region': sub_region_id or None,
		'church': church_id or None,
	}
	"""
	user = frappe.session.user
	
	# Check if user is a Church Leader
	church_leader = frappe.db.get_value(
		"Church Leader",
		{"user": user, "is_active": 1},
		["leadership_level", "region", "sub_region", "church"]
	)
	
	if church_leader:
		return {
			'level': church_leader[0],
			'region': church_leader[1],
			'sub_region': church_leader[2],
			'church': church_leader[3],
			'type': 'leader'
		}
	
	# Check if user is a Member
	member = frappe.db.get_value(
		"Member",
		{"user": user, "is_active": 1},
		["church"]
	)
	
	if member:
		# Get church hierarchy
		church_data = frappe.db.get_value(
			"Church",
			member[0],
			["sub_region"]
		)
		sub_region = church_data[0] if church_data else None
		
		# Get sub-region hierarchy
		sub_region_data = frappe.db.get_value(
			"Sub Region",
			sub_region,
			["region"]
		) if sub_region else None
		region = sub_region_data[0] if sub_region_data else None
		
		return {
			'level': 'Local',
			'region': region,
			'sub_region': sub_region,
			'church': member[0],
			'type': 'member'
		}
	
	# User is a Frappe Admin
	if frappe.session.user == "Administrator":
		return {
			'level': 'National',
			'region': None,
			'sub_region': None,
			'church': None,
			'type': 'admin'
		}
	
	return None


def check_hierarchy_access(doc, user_scope, target_level, target_region=None, target_sub_region=None, target_church=None):
	"""
	Check if user has access to content based on hierarchy rules.
	"""
	if not user_scope:
		return False
	
	user_level = user_scope['level']
	
	# National content visible to everyone
	if target_level == 'National':
		return True
	
	# Regional content
	if target_level == 'Regional':
		if user_level in ['National', 'Regional']:
			if user_level == 'National':
				return True
			return user_scope['region'] == target_region
		elif user_level in ['Sub-Regional', 'Local']:
			return user_scope['region'] == target_region
		return False
	
	# Sub-Regional content
	if target_level == 'Sub-Regional':
		if user_level in ['National', 'Regional']:
			if user_level == 'National':
				return True
			return user_scope['region'] == target_region
		elif user_level == 'Sub-Regional':
			return user_scope['sub_region'] == target_sub_region
		elif user_level == 'Local':
			return user_scope['sub_region'] == target_sub_region
		return False
	
	# Local content
	if target_level == 'Local':
		if user_level == 'National':
			return True
		elif user_level == 'Regional':
			return target_region == user_scope['region']
		elif user_level == 'Sub-Regional':
			return target_sub_region == user_scope['sub_region']
		elif user_level == 'Local':
			return user_scope['church'] == target_church
		return False
	
	return False


def region_has_permission(doc, perm_type="read", user=None):
	"""Permission handler for Region DocType"""
	if not user:
		user = frappe.session.user
	
	if user == "Administrator":
		return True
	
	user_scope = get_user_hierarchy_scope()
	if not user_scope:
		return False
	
	user_level = user_scope['level']
	
	if perm_type == "read":
		if user_level == 'National':
			return True
		if user_level == 'Regional':
			return doc.name == user_scope['region']
		if user_level in ['Sub-Regional', 'Local']:
			return doc.name == user_scope['region']
		return False
	
	elif perm_type == "write":
		if user_level == 'National':
			return True
		if user_level == 'Regional':
			return doc.name == user_scope['region']
		return False
	
	return False


def subregion_has_permission(doc, perm_type="read", user=None):
	"""Permission handler for Sub Region DocType"""
	if not user:
		user = frappe.session.user
	
	if user == "Administrator":
		return True
	
	user_scope = get_user_hierarchy_scope()
	if not user_scope:
		return False
	
	user_level = user_scope['level']
	
	if perm_type == "read":
		if user_level == 'National':
			return True
		if user_level == 'Regional':
			return doc.region == user_scope['region']
		if user_level == 'Sub-Regional':
			return doc.name == user_scope['sub_region']
		if user_level == 'Local':
			return doc.name == user_scope['sub_region']
		return False
	
	elif perm_type == "write":
		if user_level == 'National':
			return True
		if user_level == 'Regional':
			return doc.region == user_scope['region']
		if user_level == 'Sub-Regional':
			return doc.name == user_scope['sub_region']
		return False
	
	return False


def church_has_permission(doc, perm_type="read", user=None):
	"""Permission handler for Church DocType"""
	if not user:
		user = frappe.session.user
	
	if user == "Administrator":
		return True
	
	user_scope = get_user_hierarchy_scope()
	if not user_scope:
		return False
	
	user_level = user_scope['level']
	
	if perm_type == "read":
		if user_level == 'National':
			return True
		if user_level == 'Regional':
			return doc.region == user_scope['region'] or \
				   frappe.db.get_value("Sub Region", doc.sub_region, "region") == user_scope['region']
		if user_level == 'Sub-Regional':
			return doc.sub_region == user_scope['sub_region']
		if user_level == 'Local':
			return doc.name == user_scope['church']
		return False
	
	elif perm_type == "write":
		if user_level == 'National':
			return True
		if user_level == 'Regional':
			sub_region = frappe.db.get_value("Sub Region", doc.sub_region, "region")
			return sub_region == user_scope['region']
		if user_level == 'Sub-Regional':
			return doc.sub_region == user_scope['sub_region']
		if user_level == 'Local':
			return doc.name == user_scope['church']
		return False
	
	return False
