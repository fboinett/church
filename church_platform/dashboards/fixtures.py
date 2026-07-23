"""
Dashboard Fixtures - Sample data for demo dashboards
"""

def get_sample_dashboard_stats():
    """Sample statistics for demonstration"""
    return {
        "national": {
            "total_regions": 5,
            "total_sub_regions": 15,
            "total_churches": 120,
            "total_members": 8500,
            "total_posts": 450,
            "total_events": 280,
            "total_reads": 125000,
            "total_shares": 15000,
        },
        "regional": {
            "total_sub_regions": 3,
            "total_churches": 24,
            "total_members": 1700,
            "total_posts": 90,
            "total_events": 56,
            "total_reads": 25000,
            "total_shares": 3000,
        },
        "subregional": {
            "total_churches": 8,
            "total_members": 550,
            "total_leaders": 8,
            "total_posts": 30,
            "total_events": 18,
            "total_reads": 8000,
            "total_shares": 1000,
        },
        "local": {
            "active_members": 70,
            "events": 4,
            "posts": 12,
            "weekly_engagement": 450,
            "pending_moderation": 5,
        },
    }


def get_trending_content_sample():
    """Sample trending content data"""
    return [
        {
            "content_id": "post-001",
            "title": "Sunday Sermon - The Power of Faith",
            "author": "Archbishop",
            "today_reads": 250,
            "week_reads": 1200,
            "today_shares": 45,
            "total_shares": 200,
        },
        {
            "content_id": "post-002",
            "title": "Annual Church Conference 2024",
            "author": "Bishop",
            "today_reads": 180,
            "week_reads": 850,
            "today_shares": 35,
            "total_shares": 150,
        },
        {
            "content_id": "post-003",
            "title": "Community Service Initiative",
            "author": "Archdeacon",
            "today_reads": 120,
            "week_reads": 650,
            "today_shares": 28,
            "total_shares": 100,
        },
    ]


def get_engagement_trend_sample():
    """Sample engagement trend data"""
    return [
        {"date": "2024-07-14", "reads": 1200, "unique_readers": 450, "content_items": 15},
        {"date": "2024-07-15", "reads": 1350, "unique_readers": 520, "content_items": 18},
        {"date": "2024-07-16", "reads": 980, "unique_readers": 380, "content_items": 12},
        {"date": "2024-07-17", "reads": 1500, "unique_readers": 580, "content_items": 20},
        {"date": "2024-07-18", "reads": 1650, "unique_readers": 620, "content_items": 22},
        {"date": "2024-07-19", "reads": 1200, "unique_readers": 450, "content_items": 15},
        {"date": "2024-07-20", "reads": 850, "unique_readers": 320, "content_items": 10},
        {"date": "2024-07-21", "reads": 1400, "unique_readers": 530, "content_items": 19},
        {"date": "2024-07-22", "reads": 1100, "unique_readers": 420, "content_items": 14},
        {"date": "2024-07-23", "reads": 1300, "unique_readers": 500, "content_items": 17},
    ]


def get_regional_performance_sample():
    """Sample regional performance data"""
    return [
        {
            "region_name": "Northern Region",
            "sub_regions": 3,
            "churches": 28,
            "members": 2100,
            "leaders": 12,
            "total_posts": 125,
            "total_events": 85,
            "total_reads": 42000,
            "total_shares": 5200,
        },
        {
            "region_name": "Central Region",
            "sub_regions": 3,
            "churches": 32,
            "members": 2400,
            "leaders": 14,
            "total_posts": 145,
            "total_events": 95,
            "total_reads": 48000,
            "total_shares": 5800,
        },
        {
            "region_name": "Eastern Region",
            "sub_regions": 3,
            "churches": 26,
            "members": 1900,
            "leaders": 11,
            "total_posts": 110,
            "total_events": 75,
            "total_reads": 38000,
            "total_shares": 4500,
        },
        {
            "region_name": "Western Region",
            "sub_regions": 3,
            "churches": 24,
            "members": 1700,
            "leaders": 10,
            "total_posts": 95,
            "total_events": 65,
            "total_reads": 32000,
            "total_shares": 3800,
        },
        {
            "region_name": "Southern Region",
            "sub_regions": 3,
            "churches": 10,
            "members": 400,
            "leaders": 5,
            "total_posts": 50,
            "total_events": 30,
            "total_reads": 15000,
            "total_shares": 1700,
        },
    ]


def get_share_analytics_sample():
    """Sample social sharing analytics"""
    return [
        {
            "content_id": "post-001",
            "content_title": "Sunday Sermon - The Power of Faith",
            "platform": "WhatsApp",
            "share_count": 85,
            "unique_sharers": 45,
            "last_shared": "2024-07-23T18:30:00",
        },
        {
            "content_id": "post-001",
            "content_title": "Sunday Sermon - The Power of Faith",
            "platform": "Facebook",
            "share_count": 65,
            "unique_sharers": 35,
            "last_shared": "2024-07-23T16:45:00",
        },
        {
            "content_id": "post-002",
            "content_title": "Annual Church Conference 2024",
            "platform": "WhatsApp",
            "share_count": 72,
            "unique_sharers": 38,
            "last_shared": "2024-07-23T17:20:00",
        },
        {
            "content_id": "post-002",
            "content_title": "Annual Church Conference 2024",
            "platform": "Email",
            "share_count": 45,
            "unique_sharers": 28,
            "last_shared": "2024-07-23T14:10:00",
        },
    ]


def get_member_engagement_sample():
    """Sample member engagement metrics"""
    return {
        "reads": {"total_reads": 185, "latest_date": "2024-07-23"},
        "comments": {"pending": 3, "approved": 12},
        "shares": [
            {"platform": "WhatsApp", "count": 15},
            {"platform": "Facebook", "count": 8},
            {"platform": "Email", "count": 5},
        ],
        "achievements": [
            {
                "title": "First Post",
                "description": "Published your first blog post",
                "awarded_date": "2024-06-15",
            },
            {
                "title": "Engagement Star",
                "description": "100 reads on a single post",
                "awarded_date": "2024-07-10",
            },
        ],
    }
