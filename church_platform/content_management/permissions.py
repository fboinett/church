"""
Content-specific permissions for Church Platform
"""

import frappe
from church_platform.hierarchy.permissions import get_user_hierarchy_scope, check_hierarchy_access


def announcement_has_permission(doc, perm_type="read", user=None):
	"""Permission handler for Announcement DocType"""
	if not user:
		user = frappe.session.user
	
	if user == "Administrator":
		return True
	
	user_scope = get_user_hierarchy_scope()
	if not user_scope:
		return False
	
	# Everyone can read published announcements visible to them
	if perm_type == "read":
		if doc.status != "Published":
			# Only authors and admin can see drafts/archived
			author = frappe.db.get_value("Church Leader", doc.author, "user")
			return user == author or user == "Administrator"
		
		return check_hierarchy_access(
			doc,
			user_scope,
			doc.target_level,
			doc.target_region,
			doc.target_sub_region,
			doc.target_church
		)
	
	# Only author and higher-level leaders can write
	elif perm_type == "write":
		author_scope = get_user_hierarchy_scope_for_leader(doc.author)
		if not author_scope:
			return False
		
		# User must be at same level or higher
		return user_level_can_edit(user_scope, author_scope)
	
	return False


def event_has_permission(doc, perm_type="read", user=None):
	"""Permission handler for Event DocType"""
	if not user:
		user = frappe.session.user
	
	if user == "Administrator":
		return True
	
	user_scope = get_user_hierarchy_scope()
	if not user_scope:
		return False
	
	if perm_type == "read":
		return check_hierarchy_access(
			doc,
			user_scope,
			doc.target_level,
			doc.target_region,
			doc.target_sub_region,
			doc.target_church
		)
	
	elif perm_type == "write":
		organizer_scope = get_user_hierarchy_scope_for_leader(doc.organizer)
		if not organizer_scope:
			return False
		
		return user_level_can_edit(user_scope, organizer_scope)
	
	return False


def blog_post_has_permission(doc, perm_type="read", user=None):
	"""Permission handler for Church Blog Post DocType"""
	if not user:
		user = frappe.session.user
	
	if user == "Administrator":
		return True
	
	user_scope = get_user_hierarchy_scope()
	if not user_scope:
		return False
	
	if perm_type == "read":
		if doc.status != "Published":
			# Only authors and admin can see drafts/archived
			author = frappe.db.get_value("Church Leader", doc.author, "user")
			return user == author or user == "Administrator"
		
		return check_hierarchy_access(
			doc,
			user_scope,
			doc.target_level,
			doc.target_region,
			doc.target_sub_region,
			doc.target_church
		)
	
	elif perm_type == "write":
		author_scope = get_user_hierarchy_scope_for_leader(doc.author)
		if not author_scope:
			return False
		
		return user_level_can_edit(user_scope, author_scope)
	
	return False


def get_user_hierarchy_scope_for_leader(leader_id):
	"""Get hierarchy scope for a specific leader"""
	leader = frappe.db.get_value(
		"Church Leader",
		leader_id,
		["leadership_level", "region", "sub_region", "church"]
	)
	
	if leader:
		return {
			'level': leader[0],
			'region': leader[1],
			'sub_region': leader[2],
			'church': leader[3]
		}
	
	return None


def user_level_can_edit(user_scope, content_scope):
	"""Check if user's hierarchy level can edit content at content's level"""
	level_hierarchy = ["National", "Regional", "Sub-Regional", "Local"]
	
	user_level_idx = level_hierarchy.index(user_scope['level']) if user_scope['level'] in level_hierarchy else -1
	content_level_idx = level_hierarchy.index(content_scope['level']) if content_scope['level'] in level_hierarchy else -1
	
	# User must be at same level or higher (lower index = higher level)
	if user_level_idx > content_level_idx:
		return False
	
	# If same level, must be in same scope
	if user_level_idx == content_level_idx:
		if user_scope['level'] == 'National':
			return True
		elif user_scope['level'] == 'Regional':
			return user_scope['region'] == content_scope['region']
		elif user_scope['level'] == 'Sub-Regional':
			return user_scope['sub_region'] == content_scope['sub_region']
		elif user_scope['level'] == 'Local':
			return user_scope['church'] == content_scope['church']
	
	# User is at higher level
	if user_scope['level'] == 'National':
		return True
	elif user_scope['level'] == 'Regional':
		return user_scope['region'] == content_scope.get('region')
	elif user_scope['level'] == 'Sub-Regional':
		return user_scope['sub_region'] == content_scope.get('sub_region')
	
	return False
