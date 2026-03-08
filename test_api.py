#!/usr/bin/env python3
"""Test script to verify the API is working."""

import json
import urllib.request
import urllib.error

def test_health():
    """Test health endpoint."""
    try:
        req = urllib.request.Request('http://localhost:8000/health')
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            print("✓ Health check passed:", data)
            return True
    except Exception as e:
        print("✗ Health check failed:", e)
        return False

def test_onboard():
    """Test onboarding endpoint."""
    try:
        payload = {
            "quiz_answers": {
                "music_album": ["Prateek Kuhad - cold/mess"],
                "music_3am": ["Lo-fi Hindustani beats"],
                "film_feel": ["Masaan (ghat scene)"]
            },
            "goal": "Build something that matters"
        }
        
        req = urllib.request.Request(
            'http://localhost:8000/api/onboard',
            data=json.dumps(payload).encode(),
            headers={'Content-Type': 'application/json'}
        )
        
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            print("✓ Onboard passed:", data)
            return data.get('session_id')
    except Exception as e:
        print("✗ Onboard failed:", e)
        return None

def test_dna(session_id):
    """Test DNA generation endpoint."""
    try:
        req = urllib.request.Request(f'http://localhost:8000/api/dna/{session_id}')
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            print("✓ DNA generation passed:")
            print(f"  Archetype: {data.get('archetype')}")
            print(f"  Vibe: {data.get('vibe_summary')[:60]}...")
            return True
    except Exception as e:
        print("✗ DNA generation failed:", e)
        return False

def test_path(session_id):
    """Test growth path endpoint."""
    try:
        payload = {
            "session_id": session_id,
            "mood": "calm",
            "goal": "explore",
            "time_available": 30
        }
        
        req = urllib.request.Request(
            'http://localhost:8000/api/path',
            data=json.dumps(payload).encode(),
            headers={'Content-Type': 'application/json'}
        )
        
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            items = data.get('items', [])
            print(f"✓ Growth path passed: {len(items)} items generated")
            if items:
                print(f"  First item: {items[0].get('title')}")
            return True
    except Exception as e:
        print("✗ Growth path failed:", e)
        return False

def test_analytics(session_id):
    """Test analytics endpoint."""
    try:
        req = urllib.request.Request(f'http://localhost:8000/api/analytics/{session_id}')
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            print("✓ Analytics passed:")
            print(f"  Goal alignment: {data.get('goal_alignment_pct')}%")
            print(f"  Items done: {data.get('items_done')}")
            return True
    except Exception as e:
        print("✗ Analytics failed:", e)
        return False

if __name__ == '__main__':
    print("Testing MoodMash API...\n")
    
    # Test health
    if not test_health():
        print("\n❌ Health check failed. Is the server running?")
        exit(1)
    
    print()
    
    # Test onboard
    session_id = test_onboard()
    if not session_id:
        print("\n❌ Onboarding failed")
        exit(1)
    
    print()
    
    # Test DNA
    if not test_dna(session_id):
        print("\n❌ DNA generation failed")
        exit(1)
    
    print()
    
    # Test path
    if not test_path(session_id):
        print("\n❌ Growth path failed")
        exit(1)
    
    print()
    
    # Test analytics
    if not test_analytics(session_id):
        print("\n❌ Analytics failed")
        exit(1)
    
    print("\n✅ All API tests passed!")
    print(f"\n🎉 Session ID for manual testing: {session_id}")
    print(f"   Visit: http://localhost:3000/dna/{session_id}")
