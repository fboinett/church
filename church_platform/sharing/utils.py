"""
Social sharing utilities for Church Platform
Handles URL shortening, share link generation, and social media integration
"""

import frappe
import hashlib
import secrets
from urllib.parse import quote, urlencode
from datetime import datetime


class ShareURLGenerator:
	"""Generate short URLs for content sharing"""
	
	BASE_URL = "church.local"  # Should be configured in settings
	SHORT_URL_PREFIX = "s"
	
	@staticmethod
	def generate_short_code():
		"""Generate a random short code for URL"""
		return secrets.token_urlsafe(6)
	
	@staticmethod
	def create_short_url(content_type, content_id):
		"""
		Create a short URL for content.
		
		Args:
			content_type: Type of content (Announcement, Event, Blog Post, etc)
			content_id: ID of the content
			
		Returns:
			Short URL like: church.local/s/abc123
		"""
		short_code = ShareURLGenerator.generate_short_code()
		
		# Store mapping in database (would use a Share URL DocType in production)
		# For now, we'll use a simple format
		return f"https://{ShareURLGenerator.BASE_URL}/{ShareURLGenerator.SHORT_URL_PREFIX}/{short_code}"
	
	@staticmethod
	def get_full_url(content_type, content_id):
		"""Get full URL for content"""
		return f"https://{ShareURLGenerator.BASE_URL}/content/{content_type.lower()}/{content_id}"


class SocialMediaSharing:
	"""Generate social media share URLs and content"""
	
	@staticmethod
	def get_whatsapp_share_url(content_title, share_url, excerpt=""):
		"""
		Generate WhatsApp share URL
		
		Args:
			content_title: Title of the content
			share_url: URL to share
			excerpt: Short excerpt (optional)
			
		Returns:
			WhatsApp share URL with pre-filled message
		"""
		message = f"📖 {content_title}\n\n{excerpt}\n\n{share_url}"
		return f"https://wa.me/?text={quote(message)}"
	
	@staticmethod
	def get_facebook_share_url(share_url, quote_text=""):
		"""
		Generate Facebook share URL
		
		Args:
			share_url: URL to share
			quote_text: Optional quote to include
			
		Returns:
			Facebook share URL with parameters
		"""
		params = {
			"u": share_url,
			"quote": quote_text or "Check out this content from Church Platform!"
		}
		return f"https://www.facebook.com/sharer/sharer.php?{urlencode(params)}"
	
	@staticmethod
	def get_twitter_share_url(content_title, share_url, hashtags=None):
		"""
		Generate Twitter share URL
		
		Args:
			content_title: Title of the content
			share_url: URL to share
			hashtags: List of hashtags (optional)
			
		Returns:
			Twitter share URL with parameters
		"""
		text = f"{content_title} {share_url}"
		if hashtags:
			text += f" {' '.join([f'#{tag}' for tag in hashtags])}"
		
		params = {
			"text": text,
			"url": share_url
		}
		return f"https://twitter.com/intent/tweet?{urlencode(params)}"
	
	@staticmethod
	def get_email_share_url(recipient_email, content_title, share_url, excerpt="", author=""):
		"""
		Generate email share URL
		
		Args:
			recipient_email: Email address to send to
			content_title: Title of the content
			share_url: URL to share
			excerpt: Content excerpt
			author: Content author name
			
		Returns:
			Email share URL with subject and body
		"""
		subject = f"Check out: {content_title}"
		body = f"""
Hello,

I wanted to share this content with you:

Title: {content_title}
Author: {author}

{excerpt}

Read more: {share_url}

Shared via Church Platform
"""
		params = {
			"to": recipient_email,
			"subject": subject,
			"body": body
		}
		return f"mailto:{recipient_email}?{urlencode(params)}"
	
	@staticmethod
	def get_direct_link(share_url):
		"""
		Get direct link for copying to clipboard
		
		Args:
			share_url: URL to share
			
		Returns:
			The URL itself
		"""
		return share_url


class OpenGraphMeta:
	"""Generate Open Graph meta tags for rich preview cards"""
	
	@staticmethod
	def generate_tags(content_type, content_id, title, description, image_url, author=""):
		"""
		Generate Open Graph meta tags for social preview cards
		
		Args:
			content_type: Type of content
			content_id: Content ID
			title: Content title
			description: Content description/excerpt
			image_url: Featured image URL
			author: Content author name
			
		Returns:
			Dictionary of OG meta tags
		"""
		content_url = f"https://church.local/content/{content_type.lower()}/{content_id}"
		
		return {
			"og:title": title,
			"og:description": description[:160],  # Limit to 160 chars
			"og:image": image_url,
			"og:url": content_url,
			"og:type": "article",
			"og:site_name": "Church Platform",
			"twitter:card": "summary_large_image",
			"twitter:title": title,
			"twitter:description": description[:160],
			"twitter:image": image_url,
			"twitter:creator": f"@{author.replace(' ', '')}" if author else "@churchplatform"
		}
	
	@staticmethod
	def generate_html_meta_tags(og_tags):
		"""
		Generate HTML meta tag strings
		
		Args:
			og_tags: Dictionary from generate_tags()
			
		Returns:
			HTML meta tag strings
		"""
		meta_tags = []
		for key, value in og_tags.items():
			if key.startswith("og:"):
				meta_tags.append(f'<meta property="{key}" content="{value}" />')
			else:
				meta_tags.append(f'<meta name="{key}" content="{value}" />')
		
		return "\n".join(meta_tags)


class ContentSharingManager:
	"""Unified interface for all sharing operations"""
	
	@staticmethod
	def create_share_links(content_type, content_id, content_title, excerpt, featured_image_url, author=""):
		"""
		Create all share links for content
		
		Args:
			content_type: Type of content
			content_id: Content ID
			content_title: Title of content
			excerpt: Short excerpt
			featured_image_url: URL of featured image
			author: Content author name
			
		Returns:
			Dictionary with all share links and metadata
		"""
		short_url = ShareURLGenerator.create_short_url(content_type, content_id)
		full_url = ShareURLGenerator.get_full_url(content_type, content_id)
		
		return {
			"short_url": short_url,
			"full_url": full_url,
			"social_links": {
				"whatsapp": SocialMediaSharing.get_whatsapp_share_url(content_title, short_url, excerpt),
				"facebook": SocialMediaSharing.get_facebook_share_url(short_url, content_title),
				"twitter": SocialMediaSharing.get_twitter_share_url(content_title, short_url),
				"email": SocialMediaSharing.get_email_share_url("", content_title, short_url, excerpt, author),
				"direct": SocialMediaSharing.get_direct_link(short_url)
			},
			"og_meta": OpenGraphMeta.generate_tags(content_type, content_id, content_title, excerpt, featured_image_url, author)
		}
	
	@staticmethod
	def log_share(content_type, content_id, shared_by, platform, share_url, device_type=None):
		"""
		Log a share event and update analytics
		
		Args:
			content_type: Type of content
			content_id: Content ID
			shared_by: Member who shared
			platform: Social platform
			share_url: URL that was shared
			device_type: Device type (optional)
		"""
		from church_platform.doctypes.content_share.content_share import ContentShare
		
		return ContentShare.log_share(
			content_type, content_id, shared_by, platform, share_url, device_type
		)
	
	@staticmethod
	def get_share_analytics(content_type, content_id):
		"""
		Get analytics for content shares
		
		Args:
			content_type: Type of content
			content_id: Content ID
			
		Returns:
			Dictionary with share statistics
		"""
		from church_platform.doctypes.content_share.content_share import ContentShare
		
		return ContentShare.get_share_stats(content_type, content_id)
