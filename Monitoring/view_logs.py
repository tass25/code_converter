#!/usr/bin/env python3
"""
Elasticsearch Logs Viewer
==========================

View conversion logs, agent performance, and errors from Elasticsearch.

Usage:
    python view_logs.py
"""

from elasticsearch import Elasticsearch
from elasticsearch_logger import get_logger
from datetime import datetime
import json

def view_conversions(limit=10):
    """View recent conversions"""
    try:
        es = Elasticsearch(["http://localhost:9200"])
        
        result = es.search(
            index="conversions",
            body={
                "size": limit,
                "sort": [{"timestamp": "desc"}]
            }
        )
        
        print("\n" + "="*80)
        print("📊 RECENT CONVERSIONS")
        print("="*80)
        
        if result['hits']['total']['value'] == 0:
            print("\n⚠️  No conversions found. Run some conversions first:")
            print("   python convert.py test_script.r output.py")
            return
        
        for hit in result['hits']['hits']:
            doc = hit['_source']
            timestamp = datetime.fromisoformat(doc['timestamp'].replace('Z', '+00:00'))
            
            status_emoji = "✅" if doc['status'] == 'success' else "❌"
            
            print(f"\n{status_emoji} {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"   {doc['source_language']} → {doc['target_language']}")
            print(f"   Duration: {doc['duration_seconds']:.2f}s | Iterations: {doc['iterations']} | Code: {doc['code_length']} chars")
            
    except Exception as e:
        print(f"\n❌ Error fetching conversions: {e}")
        print("   Make sure Elasticsearch is running: docker-compose ps")


def view_agent_stats():
    """View agent performance statistics"""
    try:
        es = Elasticsearch(["http://localhost:9200"])
        
        result = es.search(
            index="agents",
            body={
                "size": 0,
                "aggs": {
                    "by_agent": {
                        "terms": {"field": "agent_name", "size": 10},
                        "aggs": {
                            "avg_duration": {"avg": {"field": "duration_seconds"}},
                            "total_calls": {"value_count": {"field": "agent_name"}}
                        }
                    }
                }
            }
        )
        
        print("\n" + "="*80)
        print("🤖 AGENT PERFORMANCE")
        print("="*80)
        
        buckets = result.get('aggregations', {}).get('by_agent', {}).get('buckets', [])
        
        if not buckets:
            print("\n⚠️  No agent data found yet.")
            return
        
        for bucket in buckets:
            agent = bucket['key']
            avg_duration = bucket.get('avg_duration', {}).get('value')
            total_calls = bucket['doc_count']
            
            print(f"\n📌 {agent}")
            print(f"   Calls: {total_calls}")
            if avg_duration:
                print(f"   Avg Duration: {avg_duration:.2f}s")
            else:
                print(f"   Avg Duration: N/A")
                
    except Exception as e:
        print(f"\n❌ Error fetching agent stats: {e}")


def view_stats():
    """View overall statistics"""
    try:
        logger = get_logger()
        stats = logger.get_stats(hours=24)
        
        print("\n" + "="*80)
        print("📈 STATISTICS (Last 24 Hours)")
        print("="*80)
        
        print(f"\n📊 Total Conversions: {stats['total_conversions']}")
        print(f"✅ Successful: {stats['successful_conversions']}")
        print(f"📈 Success Rate: {stats['success_rate']:.1f}%")
        
        if stats['avg_duration_seconds']:
            print(f"⚡ Avg Duration: {stats['avg_duration_seconds']:.2f}s")
        else:
            print(f"⚡ Avg Duration: N/A")
        
        if stats['by_language']:
            print("\n🌐 By Language:")
            for lang in stats['by_language']:
                print(f"   • {lang['key']}: {lang['doc_count']} conversions")
        else:
            print("\n🌐 By Language: No data yet")
            
    except Exception as e:
        print(f"\n❌ Error fetching stats: {e}")


def view_errors(limit=5):
    """View recent errors"""
    try:
        es = Elasticsearch(["http://localhost:9200"])
        
        result = es.search(
            index="errors",
            body={
                "size": limit,
                "sort": [{"timestamp": "desc"}]
            }
        )
        
        print("\n" + "="*80)
        print("🔴 RECENT ERRORS")
        print("="*80)
        
        if result['hits']['total']['value'] == 0:
            print("\n✅ No errors! System is running smoothly.")
            return
        
        for hit in result['hits']['hits']:
            doc = hit['_source']
            timestamp = datetime.fromisoformat(doc['timestamp'].replace('Z', '+00:00'))
            
            print(f"\n❌ {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"   Type: {doc['error_type']}")
            print(f"   Agent: {doc.get('agent_name', 'N/A')}")
            print(f"   Message: {doc['message'][:80]}...")
            
    except Exception as e:
        print(f"\n❌ Error fetching errors: {e}")


def view_all():
    """View everything"""
    print("\n" + "="*80)
    print("🔍 ELASTICSEARCH LOGS VIEWER")
    print("="*80)
    
    try:
        # Check Elasticsearch connection
        es = Elasticsearch(["http://localhost:9200"])
        if not es.ping():
            print("\n❌ Cannot connect to Elasticsearch!")
            print("   Make sure it's running: docker-compose ps")
            print("   Or start it: docker-compose up -d")
            return
        
        print("\n✅ Connected to Elasticsearch\n")
        
        # View all data
        view_stats()
        view_conversions(limit=5)
        view_agent_stats()
        view_errors(limit=5)
        
        # Help text
        print("\n" + "="*80)
        print("✅ View complete!")
        print("="*80)
        print("\n📚 More options:")
        print("   • Web Dashboard: Open dashboard.html in browser")
        print("   • API Stats: curl http://localhost:8000/stats")
        print("   • Elasticsearch: http://localhost:9200/conversions/_search?pretty")
        print("   • Test failures: python test_failures.py")
        print("="*80 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n💡 Troubleshooting:")
        print("   1. Check if Elasticsearch is running: docker-compose ps")
        print("   2. Start services: docker-compose up -d")
        print("   3. Initialize indices: python elasticsearch_logger.py")
        print("   4. Run conversions: python convert.py test_script.r output.py")


if __name__ == "__main__":
    view_all()