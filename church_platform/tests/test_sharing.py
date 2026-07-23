"""
Unit Tests for Social Sharing System

Tests:
- Short URL generation
- Social platform URL formatting
- Open Graph metadata generation
- Share analytics tracking
"""

import frappe
from frappe.test_runner import FrappeTestCase
from church_platform.sharing.utils import (
    ShareURLGenerator,
    SocialMediaSharing,
    OpenGraphMeta,
    ContentSharingManager
)


class TestShareURLGenerator(FrappeTestCase):
    """Test URL shortening and generation"""
    
    def setUp(self):
        """Create test data"""
        super().setUp()
        self.generator = ShareURLGenerator()
    
    def test_create_short_code(self):
        """Short codes are generated and unique"""
        code1 = self.generator.create_short_url('post-1', 'Church Blog Post')
        code2 = self.generator.create_short_url('post-2', 'Church Blog Post')
        
        self.assertIsNotNone(code1)
        self.assertIsNotNone(code2)
        self.assertNotEqual(code1, code2)
    
    def test_get_full_url(self):
        """Full URLs are correctly formatted"""
        short_code = self.generator.create_short_url('post-1', 'Church Blog Post')
        full_url = self.generator.get_full_url(short_code)
        
        self.assertIn('http', full_url)
        self.assertIn(short_code, full_url)


class TestSocialMediaSharing(FrappeTestCase):
    """Test social media URL generation"""
    
    def setUp(self):
        """Create sharing utility"""
        super().setUp()
        self.sharing = SocialMediaSharing()
    
    def test_whatsapp_url_format(self):
        """WhatsApp share URL is properly formatted"""
        url = self.sharing.get_whatsapp_share_url(
            'Test Post',
            'http://church.local/posts/test',
            'My thoughts'
        )
        
        self.assertIn('api.whatsapp.com', url)
        self.assertIn('Test Post', url)
    
    def test_facebook_url_format(self):
        """Facebook share URL is properly formatted"""
        url = self.sharing.get_facebook_share_url(
            'http://church.local/posts/test',
            'Test Post'
        )
        
        self.assertIn('facebook.com', url)
    
    def test_twitter_url_format(self):
        """Twitter share URL is properly formatted"""
        url = self.sharing.get_twitter_share_url(
            'Test Post',
            'http://church.local/posts/test',
            'My thoughts'
        )
        
        self.assertIn('twitter.com', url)


class TestOpenGraphMeta(FrappeTestCase):
    """Test Open Graph metadata generation"""
    
    def setUp(self):
        """Create OG metadata generator"""
        super().setUp()
        self.og = OpenGraphMeta()
    
    def test_generate_og_tags(self):
        """OG tags dictionary is generated correctly"""
        tags = self.og.generate_tags(
            title='Test Post',
            description='Test description',
            url='http://church.local/posts/test',
            image='http://church.local/images/test.jpg',
            content_type='blog_post'
        )
        
        self.assertEqual(tags['og:title'], 'Test Post')
        self.assertEqual(tags['og:description'], 'Test description')
    
    def test_generate_html_meta_tags(self):
        """HTML meta tags are properly formatted"""
        tags = {
            'og:title': 'Test Post',
            'og:description': 'Test description'
        }
        
        html = self.og.generate_html_meta_tags(tags)
        
        self.assertIn('<meta', html)
        self.assertIn('Test Post', html)
