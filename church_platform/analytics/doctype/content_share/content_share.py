"""
Content Share DocType - Track social media shares and engagement
"""

import frappe
from frappe.model.document import Document
from frappe import _
from datetime import datetime


class ContentShare(Document):
	"""Track when and where content is shared on social media"""
	
	def validate(self):
		"""Validate share data"""
		# Set share_date to now if not provided
		if not self.share_date:
			self.share_date = datetime.now()
	
	def on_update(self):
		"""Log share event"""
		frappe.msgprint(
			_("Share logged: {0} on {1}").format(self.content_type, self.platform),
			indicator="green",
			alert=True
		)
	
	@staticmethod
	def log_share(content_type, content_id, shared_by, platform, share_url=None, device_type=None, shared_to_email=None):
		"""
		Log a content share event.
		
		Args:
			content_type: Type of content (Announcement, Event, Blog Post, Achievement)
			content_id: ID of the content
			shared_by: Member who shared
			platform: Social platform (WhatsApp, Facebook, Twitter, Email, Direct Link, QR Code)
			share_url: URL that was shared (optional)
			device_type: Desktop, Mobile, or Tablet (optional)
			shared_to_email: Email address if shared via email (optional)
		"""
		share = frappe.get_doc({
			"doctype": "Content Share",
			"content_type": content_type,
			"content_id": content_id,
			"shared_by": shared_by,
			"platform": platform,
			"share_url": share_url,
			"device_type": device_type,
			"shared_to_email": shared_to_email,
			"share_date": datetime.now()
		})
		share.insert(ignore_permissions=True)
		
		return share
	
	@staticmethod
	def get_share_stats(content_type, content_id):
		"""Get share statistics for content"""
		shares = frappe.db.get_list(
			"Content Share",
			filters={
				"content_type": content_type,
				"content_id": content_id
			},
			fields=["platform", "share_date"],
			order_by="share_date desc"
		)
		
		# Count shares by platform
		platform_counts = {}
		for share in shares:
			platform = share.get("platform")
			platform_counts[platform] = platform_counts.get(platform, 0) + 1
		
		return {
			"total_shares": len(shares),
			"shares_by_platform": platform_counts,
			"recent_shares": shares[:10]
		}
	
	@staticmethod
	def get_trending_content(content_type, days=7):
		"""Get most shared content in the last N days"""
		from datetime import timedelta, datetime
		
		date_filter = datetime.now() - timedelta(days=days)
		
		result = frappe.db.sql("""
			SELECT content_id, COUNT(*) as share_count
			FROM `tabContent Share`
			WHERE content_type = %s AND share_date >= %s
			GROUP BY content_id
			ORDER BY share_count DESC
			LIMIT 10
		""", (content_type, date_filter), as_dict=True)
		
		return result
