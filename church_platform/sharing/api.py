"""
API methods for content sharing
Exposes sharing functionality to the frontend
"""

import frappe
from frappe.utils import get_request_header
from church_platform.sharing.utils import ContentSharingManager


@frappe.whitelist()
def get_share_links(doctype, docname):
	"""
	Get all share links for a piece of content
	
	Args:
		doctype: DocType name (Church Blog Post, Event, Announcement, etc)
		docname: Document name/ID
		
	Returns:
		Dictionary with all share links and metadata
	"""
	doc = frappe.get_doc(doctype, docname)
	
	# Check if user can read this document
	if not frappe.has_permission(doctype, "read", docname):
		frappe.throw(frappe.PermissionError("Not permitted to share this content"))
	
	# Get content details
	title = doc.get("title") or doc.get("name")
	excerpt = doc.get("excerpt") or doc.get("description", "")
	featured_image = doc.get("featured_image") or ""
	author = doc.get("author") or doc.get("organizer", "")
	
	# Limit excerpt to 160 chars
	if len(excerpt) > 160:
		excerpt = excerpt[:157] + "..."
	
	# Generate full share links
	share_links = ContentSharingManager.create_share_links(
		doctype,
		docname,
		title,
		excerpt,
		featured_image,
		author
	)
	
	return {
		"doctype": doctype,
		"docname": docname,
		"title": title,
		"excerpt": excerpt,
		"featured_image": featured_image,
		"share_links": share_links
	}


@frappe.whitelist()
def log_share(doctype, docname, platform):
	"""
	Log a share event when user shares content
	
	Args:
		doctype: DocType name
		docname: Document name/ID
		platform: Social platform (whatsapp, facebook, twitter, email, direct)
		
	Returns:
		Success message
	"""
	doc = frappe.get_doc(doctype, docname)
	
	# Get current user (must be a member)
	user = frappe.session.user
	member = frappe.db.get_value("Member", {"user": user}, "name")
	
	if not member:
		# Try to get from Church Leader for testing
		member = frappe.db.get_value("Church Leader", {"user": user}, "name")
		if not member:
			frappe.throw("You must be a Member or Church Leader to share content")
	
	# Get share URL
	device_type = get_request_header("X-Device-Type") or "Desktop"
	
	# Log the share
	ContentSharingManager.log_share(
		doctype,
		docname,
		member,
		platform,
		share_url=frappe.utils.get_request_header("X-Share-URL"),
		device_type=device_type
	)
	
	frappe.msgprint(f"Shared on {platform}!", indicator="green")
	return {"status": "success", "message": f"Shared to {platform}"}


@frappe.whitelist()
def get_share_stats(doctype, docname):
	"""
	Get share statistics for content
	
	Args:
		doctype: DocType name
		docname: Document name/ID
		
	Returns:
		Dictionary with share statistics
	"""
	# Check if user can read this document
	if not frappe.has_permission(doctype, "read", docname):
		frappe.throw(frappe.PermissionError("Not permitted to view stats"))
	
	stats = ContentSharingManager.get_share_analytics(doctype, docname)
	return stats


@frappe.whitelist()
def get_trending_content(doctype, days=7):
	"""
	Get trending content based on shares
	
	Args:
		doctype: DocType name (Church Blog Post, Event, etc)
		days: Number of days to look back
		
	Returns:
		List of trending content with share counts
	"""
	from church_platform.doctypes.content_share.content_share import ContentShare
	
	trending = ContentShare.get_trending_content(doctype, int(days))
	return trending
