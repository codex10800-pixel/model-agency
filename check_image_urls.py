#!/usr/bin/env python
"""
Diagnostic script to check image URLs in the database.
Shows which images are stored as local paths vs Cloudinary URLs.
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agency.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from core.models import ModelProfile, ActorProfile, PortfolioImage, ActorPortfolioImage, Application

def check_urls():
    print("\n" + "="*70)
    print("DATABASE IMAGE URL AUDIT")
    print("="*70 + "\n")
    
    local_count = 0
    cloudinary_count = 0
    empty_count = 0
    
    # Check ModelProfile profile images
    print("📸 ModelProfile Images:")
    for profile in ModelProfile.objects.all():
        url = str(profile.profile_image) if profile.profile_image else None
        if not url:
            empty_count += 1
            print(f"  ❌ {profile.name}: (empty)")
        elif url.startswith('http'):
            cloudinary_count += 1
            print(f"  ✅ {profile.name}: {url[:60]}...")
        else:
            local_count += 1
            print(f"  ⚠️  {profile.name}: {url}")
    
    # Check ActorProfile profile images
    print("\n🎭 ActorProfile Images:")
    for profile in ActorProfile.objects.all():
        url = str(profile.profile_image) if profile.profile_image else None
        if not url:
            empty_count += 1
            print(f"  ❌ {profile.name}: (empty)")
        elif url.startswith('http'):
            cloudinary_count += 1
            print(f"  ✅ {profile.name}: {url[:60]}...")
        else:
            local_count += 1
            print(f"  ⚠️  {profile.name}: {url}")
    
    # Check PortfolioImage
    print("\n🖼️  ModelProfile Portfolio Images:")
    for portfolio in PortfolioImage.objects.all():
        url = str(portfolio.image) if portfolio.image else None
        if not url:
            empty_count += 1
            print(f"  ❌ {portfolio.model.name} portfolio: (empty)")
        elif url.startswith('http'):
            cloudinary_count += 1
            print(f"  ✅ {portfolio.model.name} portfolio: {url[:60]}...")
        else:
            local_count += 1
            print(f"  ⚠️  {portfolio.model.name} portfolio: {url}")
    
    # Check ActorPortfolioImage
    print("\n🎬 ActorProfile Portfolio Images:")
    for portfolio in ActorPortfolioImage.objects.all():
        url = str(portfolio.image) if portfolio.image else None
        if not url:
            empty_count += 1
            print(f"  ❌ {portfolio.actor.name} portfolio: (empty)")
        elif url.startswith('http'):
            cloudinary_count += 1
            print(f"  ✅ {portfolio.actor.name} portfolio: {url[:60]}...")
        else:
            local_count += 1
            print(f"  ⚠️  {portfolio.actor.name} portfolio: {url}")
    
    # Check Application images
    print("\n📋 Application Images:")
    for app in Application.objects.all():
        url = str(app.images) if app.images else None
        if not url:
            empty_count += 1
            print(f"  ❌ {app.name}: (empty)")
        elif url.startswith('http'):
            cloudinary_count += 1
            print(f"  ✅ {app.name}: {url[:60]}...")
        else:
            local_count += 1
            print(f"  ⚠️  {app.name}: {url}")
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY:")
    print(f"  ✅ Cloudinary URLs: {cloudinary_count}")
    print(f"  ⚠️  Local paths: {local_count}")
    print(f"  ❌ Empty: {empty_count}")
    print("="*70 + "\n")
    
    if local_count > 0:
        print("⚠️  WARNING: Found local file paths in database!")
        print("   These will NOT persist after server restart on Render.")
        print("   Use 'python manage.py upload_media_to_cloudinary' to migrate them.\n")
    else:
        print("✅ All images are using Cloudinary or empty. Safe for Render!\n")

if __name__ == '__main__':
    check_urls()
