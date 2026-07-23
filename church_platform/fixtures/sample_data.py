"""
Sample Data Fixtures for Church Platform

Provides demo data for all hierarchy levels and content types:
- 5 regions (National + 4 Regional)
- 20 sub-regions
- 120 churches
- 50+ leaders at all levels
- 8500+ members
- Sample announcements, events, blog posts
- Sample comments, RSVPs, shares
"""

import frappe
from datetime import datetime, timedelta
from random import randint, choice


def create_hierarchy_fixtures():
    """Create sample hierarchy data"""
    
    # National region
    national = frappe.get_doc({
        'doctype': 'Region',
        'region_name': 'National Headquarters',
        'hierarchy_level': 'National',
        'description': 'National leadership and coordination',
        'country': 'Kenya'
    })
    national.insert(ignore_if_duplicate=True)
    
    # Regional regions
    regions = ['East Africa', 'West Africa', 'Southern Africa', 'Central Africa']
    region_docs = []
    
    for region_name in regions:
        region = frappe.get_doc({
            'doctype': 'Region',
            'region_name': region_name,
            'hierarchy_level': 'Regional',
            'parent_region': 'National Headquarters',
            'description': f'{region_name} regional office',
            'country': 'Kenya'
        })
        region.insert(ignore_if_duplicate=True)
        region_docs.append(region)
    
    # Sub-regions
    subregion_count = 0
    for region in regions:
        for i in range(5):  # 5 sub-regions per region
            subregion_name = f'{region} - District {i+1}'
            subregion = frappe.get_doc({
                'doctype': 'Sub Region',
                'sub_region_name': subregion_name,
                'hierarchy_level': 'Sub-Regional',
                'parent_region': region,
                'description': f'Sub-region in {region}',
                'district': f'District {i+1}'
            })
            subregion.insert(ignore_if_duplicate=True)
            subregion_count += 1
    
    frappe.db.commit()
    print(f"✓ Created hierarchy: 1 national + 4 regional + {subregion_count} sub-regional regions")


def create_churches_fixtures():
    """Create sample churches"""
    
    # Get all sub-regions
    subregions = frappe.get_list('Sub Region', fields=['name', 'parent_region'])
    
    church_count = 0
    for subregion in subregions:
        # 6 churches per sub-region = ~120 total
        for i in range(6):
            church_name = f"{subregion['name']} - Church {i+1}"
            church = frappe.get_doc({
                'doctype': 'Church',
                'church_name': church_name,
                'hierarchy_level': 'Local',
                'parent_sub_region': subregion['name'],
                'email': f"church{i+1}@{subregion['name'].replace(' ', '')}.local".lower(),
                'phone': f"+254{randint(700000000, 799999999)}",
                'address': f"Church Street {i+1}, {subregion['name']}",
                'worship_day': choice(['Sunday', 'Saturday']),
                'worship_time': choice(['8:00 AM', '10:00 AM', '5:00 PM'])
            })
            church.insert(ignore_if_duplicate=True)
            church_count += 1
    
    frappe.db.commit()
    print(f"✓ Created {church_count} churches")


def create_leaders_fixtures():
    """Create sample leaders at all levels"""
    
    leader_count = 0
    
    # National leaders
    national_leaders = ['Archbishop', 'National Coordinator', 'Treasurer']
    for idx, title in enumerate(national_leaders):
        user_email = f"national_{idx}@church.local"
        
        frappe.get_doc({
            'doctype': 'User',
            'email': user_email,
            'first_name': title.split()[0],
            'send_welcome_email': 0
        }).insert(ignore_if_duplicate=True)
        
        frappe.get_doc({
            'doctype': 'Church Leader',
            'leader_name': title,
            'user': user_email,
            'hierarchy_level': 'National',
            'role': 'Archbishop' if 'Archbishop' in title else 'Administrator',
            'phone': f"+254{randint(700000000, 799999999)}"
        }).insert(ignore_if_duplicate=True)
        
        leader_count += 1
    
    # Regional leaders (2 per region)
    regions = frappe.get_list('Region', {'hierarchy_level': 'Regional'}, ['name'])
    for region_idx, region in enumerate(regions):
        for i in range(2):
            user_email = f"regional_{region_idx}_{i}@church.local"
            
            frappe.get_doc({
                'doctype': 'User',
                'email': user_email,
                'first_name': f'Bishop {i+1}',
                'send_welcome_email': 0
            }).insert(ignore_if_duplicate=True)
            
            frappe.get_doc({
                'doctype': 'Church Leader',
                'leader_name': f'Bishop - {region["name"]} {i+1}',
                'user': user_email,
                'hierarchy_level': 'Regional',
                'region': region['name'],
                'role': 'Bishop',
                'phone': f"+254{randint(700000000, 799999999)}"
            }).insert(ignore_if_duplicate=True)
            
            leader_count += 1
    
    # Sub-regional leaders (2 per sub-region)
    subregions = frappe.get_list('Sub Region', ['name'])
    for subregion_idx, subregion in enumerate(subregions):
        for i in range(2):
            user_email = f"archdeacon_{subregion_idx}_{i}@church.local"
            
            frappe.get_doc({
                'doctype': 'User',
                'email': user_email,
                'first_name': f'Archdeacon {i+1}',
                'send_welcome_email': 0
            }).insert(ignore_if_duplicate=True)
            
            frappe.get_doc({
                'doctype': 'Church Leader',
                'leader_name': f'Archdeacon - {subregion["name"]} {i+1}',
                'user': user_email,
                'hierarchy_level': 'Sub-Regional',
                'sub_region': subregion['name'],
                'role': 'Archdeacon',
                'phone': f"+254{randint(700000000, 799999999)}"
            }).insert(ignore_if_duplicate=True)
            
            leader_count += 1
    
    # Local leaders (5+ per church)
    churches = frappe.get_list('Church', ['name'])
    for church in churches:
        num_leaders = randint(3, 6)
        for i in range(num_leaders):
            user_email = f"pastor_{church['name'].replace(' ', '_').lower()}_{i}@church.local"
            user_email = user_email[:60]
            
            frappe.get_doc({
                'doctype': 'User',
                'email': user_email,
                'first_name': f'Pastor {i+1}',
                'send_welcome_email': 0
            }).insert(ignore_if_duplicate=True)
            
            frappe.get_doc({
                'doctype': 'Church Leader',
                'leader_name': f'Pastor - {church["name"]} {i+1}',
                'user': user_email,
                'hierarchy_level': 'Local',
                'church': church['name'],
                'role': 'Pastor',
                'phone': f"+254{randint(700000000, 799999999)}"
            }).insert(ignore_if_duplicate=True)
            
            leader_count += 1
    
    frappe.db.commit()
    print(f"✓ Created {leader_count} leaders (national, regional, sub-regional, local)")


def create_members_fixtures():
    """Create sample members"""
    
    member_count = 0
    churches = frappe.get_list('Church', ['name'])
    
    for church in churches:
        # 70+ members per church = ~8400+ total
        num_members = randint(60, 80)
        
        for i in range(num_members):
            user_email = f"member_{church['name'].replace(' ', '_').lower()}_{i}@church.local"
            user_email = user_email[:60]
            
            frappe.get_doc({
                'doctype': 'User',
                'email': user_email,
                'first_name': f'Member {i+1}',
                'send_welcome_email': 0
            }).insert(ignore_if_duplicate=True)
            
            frappe.get_doc({
                'doctype': 'Member',
                'member_name': f'Member {i+1} - {church["name"]}',
                'user': user_email,
                'church': church['name'],
                'status': choice(['Active', 'Inactive']),
                'phone': f"+254{randint(700000000, 799999999)}",
                'join_date': datetime.now() - timedelta(days=randint(0, 1825))
            }).insert(ignore_if_duplicate=True)
            
            member_count += 1
    
    frappe.db.commit()
    print(f"✓ Created {member_count} members")


def create_all_fixtures():
    """Create all sample data fixtures"""
    print("\n📊 Creating Sample Data Fixtures...\n")
    
    create_hierarchy_fixtures()
    create_churches_fixtures()
    create_leaders_fixtures()
    create_members_fixtures()
    
    print("\n✅ All fixtures created successfully!\n")
    frappe.db.commit()


if __name__ == '__main__':
    create_all_fixtures()
