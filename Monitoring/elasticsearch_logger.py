"""
Elasticsearch Logger for Code Converter
Logs all agent activities, metrics, and errors to Elasticsearch
"""

import os
from datetime import datetime
from elasticsearch import Elasticsearch
from dotenv import load_dotenv
import json

load_dotenv()

class ElasticsearchLogger:
    """
    Centralized logging to Elasticsearch for monitoring and debugging.
    
    Logs include:
    - Agent activities and outputs
    - Conversion requests and results
    - Performance metrics (latency, iterations)
    - Errors and validation failures
    """
    
    def __init__(self, host=None):
        """
        Initialize Elasticsearch connection.
        
        Args:
            host: Elasticsearch host (default: from env or localhost:9200)
        """
        self.host = host or os.getenv("ELASTICSEARCH_HOST", "localhost:9200")
        
        try:
            self.es = Elasticsearch(
                [f"http://{self.host}"],
                request_timeout=30
            )
            
            # Test connection
            if self.es.ping():
                print(f"✅ Connected to Elasticsearch at {self.host}")
                self._create_indices()
            else:
                print(f"⚠️  Could not connect to Elasticsearch at {self.host}")
                self.es = None
                
        except Exception as e:
            print(f"⚠️  Elasticsearch connection failed: {e}")
            self.es = None
    
    def _create_indices(self):
        """Create indices with proper mappings if they don't exist"""
        
        indices = {
            "conversions": {
                "mappings": {
                    "properties": {
                        "timestamp": {"type": "date"},
                        "source_language": {"type": "keyword"},
                        "target_language": {"type": "keyword"},
                        "status": {"type": "keyword"},
                        "duration_seconds": {"type": "float"},
                        "iterations": {"type": "integer"},
                        "code_length": {"type": "integer"}
                    }
                }
            },
            "agents": {
                "mappings": {
                    "properties": {
                        "timestamp": {"type": "date"},
                        "agent_name": {"type": "keyword"},
                        "action": {"type": "keyword"},
                        "duration_seconds": {"type": "float"},
                        "status": {"type": "keyword"}
                    }
                }
            },
            "errors": {
                "mappings": {
                    "properties": {
                        "timestamp": {"type": "date"},
                        "error_type": {"type": "keyword"},
                        "agent_name": {"type": "keyword"},
                        "message": {"type": "text"}
                    }
                }
            }
        }
        
        for index_name, settings in indices.items():
            try:
                if not self.es.indices.exists(index=index_name):
                    self.es.indices.create(index=index_name, body=settings)
                    print(f"  Created index: {index_name}")
            except Exception as e:
                print(f"  Warning: Could not create index {index_name}: {e}")
    
    def log_conversion(self, source_lang, target_lang, status, duration=0, 
                      iterations=0, code_length=0, metadata=None):
        """
        Log a conversion event.
        
        Args:
            source_lang: Source programming language
            target_lang: Target programming language
            status: 'success' or 'failed'
            duration: Processing time in seconds
            iterations: Number of validation iterations
            code_length: Length of generated code
            metadata: Additional data (intent graph, validation results, etc.)
        """
        if not self.es:
            return
        
        doc = {
            "timestamp": datetime.utcnow().isoformat(),
            "source_language": source_lang,
            "target_language": target_lang,
            "status": status,
            "duration_seconds": duration,
            "iterations": iterations,
            "code_length": code_length,
            "metadata": metadata or {}
        }
        
        try:
            self.es.index(index="conversions", document=doc)
        except Exception as e:
            print(f"Failed to log conversion: {e}")
    
    def log_agent_activity(self, agent_name, action, duration=0, status="success", 
                          input_data=None, output_data=None):
        """
        Log agent activity.
        
        Args:
            agent_name: Name of the agent (parser, intent_extractor, etc.)
            action: What the agent did
            duration: Time spent
            status: success/failed
            input_data: What the agent received
            output_data: What the agent produced
        """
        if not self.es:
            return
        
        doc = {
            "timestamp": datetime.utcnow().isoformat(),
            "agent_name": agent_name,
            "action": action,
            "duration_seconds": duration,
            "status": status,
            "input_summary": str(input_data)[:500] if input_data else None,
            "output_summary": str(output_data)[:500] if output_data else None
        }
        
        try:
            self.es.index(index="agents", document=doc)
        except Exception as e:
            print(f"Failed to log agent activity: {e}")
    
    def log_error(self, error_type, message, agent_name=None, context=None):
        """
        Log an error.
        
        Args:
            error_type: Type of error (validation_failed, api_error, etc.)
            message: Error message
            agent_name: Which agent encountered the error
            context: Additional context
        """
        if not self.es:
            return
        
        doc = {
            "timestamp": datetime.utcnow().isoformat(),
            "error_type": error_type,
            "agent_name": agent_name,
            "message": message,
            "context": context or {}
        }
        
        try:
            self.es.index(index="errors", document=doc)
        except Exception as e:
            print(f"Failed to log error: {e}")
    
    def get_stats(self, hours=24):
        """
        Get conversion statistics for the last N hours.
        
        Returns:
            dict: Statistics including total conversions, success rate, avg duration
        """
        if not self.es:
            return {}
        
        try:
            # Query for conversions in the last N hours
            query = {
                "query": {
                    "range": {
                        "timestamp": {
                            "gte": f"now-{hours}h",
                            "lte": "now"
                        }
                    }
                }
            }
            
            result = self.es.search(index="conversions", body=query, size=0, aggs={
                "total": {"value_count": {"field": "timestamp"}},
                "successful": {
                    "filter": {"term": {"status": "success"}},
                    "aggs": {"count": {"value_count": {"field": "timestamp"}}}
                },
                "avg_duration": {"avg": {"field": "duration_seconds"}},
                "by_language": {
                    "terms": {"field": "source_language", "size": 10}
                }
            })
            
            aggs = result.get("aggregations", {})
            total = aggs.get("total", {}).get("value", 0)
            successful = aggs.get("successful", {}).get("count", {}).get("value", 0)
            
            return {
                "total_conversions": total,
                "successful_conversions": successful,
                "success_rate": (successful / total * 100) if total > 0 else 0,
                "avg_duration_seconds": aggs.get("avg_duration", {}).get("value", 0),
                "by_language": aggs.get("by_language", {}).get("buckets", [])
            }
            
        except Exception as e:
            print(f"Failed to get stats: {e}")
            return {}


# Global logger instance
_logger = None

def get_logger():
    """Get or create the global Elasticsearch logger"""
    global _logger
    if _logger is None:
        _logger = ElasticsearchLogger()
    return _logger


# ============================================================================
# TEST THE LOGGER
# ============================================================================

if __name__ == "__main__":
    print("="*70)
    print("TESTING ELASTICSEARCH LOGGER")
    print("="*70)
    
    logger = ElasticsearchLogger()
    
    # Test logging
    print("\n1. Logging test conversion...")
    logger.log_conversion(
        source_lang="R",
        target_lang="Python",
        status="success",
        duration=3.5,
        iterations=1,
        code_length=250
    )
    
    print("\n2. Logging test agent activity...")
    logger.log_agent_activity(
        agent_name="parser",
        action="parse_code",
        duration=0.8,
        status="success"
    )
    
    print("\n3. Logging test error...")
    logger.log_error(
        error_type="validation_failed",
        message="Intent extraction incomplete",
        agent_name="validator"
    )
    
    print("\n4. Getting statistics...")
    stats = logger.get_stats(hours=24)
    print(json.dumps(stats, indent=2))
    
    print("\n" + "="*70)
    print("✅ Logger test complete!")
    print("="*70)
    print("\nView logs at: http://localhost:9200/conversions/_search?pretty")