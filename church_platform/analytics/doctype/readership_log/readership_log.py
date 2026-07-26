"""
Readership Log DocType - Track content views and engagement
"""

import frappe
from frappe.model.document import Document
from frappe import _
from datetime import datetime


class ReadershipLog(Document):
	"""Log content views and track engagement metrics"""
	
	def validate(self):
		"""Validate readership log data"""
		# Set view_date to now if not provided
		if not self.view_date:
			self.view_date = datetime.now()
	
	@staticmethod
	def log_view(content_type, content_id, member, device_type=None, view_source="Portal"):
		"""
		Log a content view.
		
		Args:
			content_type: Type of content (Announcement, Event, Blog Post, Achievement)
			content_id: ID of the content
			member: Member viewing the content
			device_type: Desktop, Mobile, or Tablet
			view_source: Portal, Email, Social Share, Direct Link
		"""
		log = frappe.get_doc({
			"doctype": "Readership Log",
			"content_type": content_type,
			"content_id": content_id,
			"member": member,
			"view_date": datetime.now(),
			"device_type": device_type,
			"view_source": view_source
		})
		log.insert(ignore_permissions=True)
		
		return log
	
	@staticmethod
	def get_content_views(content_type, content_id):
		"""Get total views for a piece of content"""
		return frappe.db.count(
			"Readership Log",
			{
				"content_type": content_type,
				"content_id": content_id
			}
		)
	
	@staticmethod
	def get_member_views(member):
		"""Get all views for a member"""
		return frappe.db.get_list(
			"Readership Log",
			filters={"member": member},
			fields=["content_type", "content_id", "view_date", "device_type"],
			order_by="view_date desc"
		)
