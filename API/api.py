"""
FASTAPI BACKEND - REST API for Code Conversion 🌐
==================================================

Provides HTTP endpoints for the code conversion service.

Endpoints:
- POST /convert - Convert code
- POST /convert/file - Convert code from uploaded file
- GET /health - Health check
- GET /languages - List supported languages
- GET /stats - Conversion statistics from Elasticsearch
"""

from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn
import time

from Orchestration.workflow import convert_with_workflow
from Monitoring.elasticsearch_logger import get_logger

# ============================================================================ 
# FASTAPI APP
# ============================================================================ 

app = FastAPI(
    title="Code Converter API",
    description="AI-powered intentions-based code conversion",
    version="1.0.0"
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================ 
# REQUEST/RESPONSE MODELS
# ============================================================================ 

class ConversionRequest(BaseModel):
    """Request model for code conversion"""
    source_code: str
    source_language: str = "R"
    target_language: str = "Python"
    max_iterations: Optional[int] = 3
    
    class Config:
        json_schema_extra = {
            "example": {
                "source_code": "data <- read.csv('file.csv')\nresult <- mean(data$value)",
                "source_language": "R",
                "target_language": "Python",
                "max_iterations": 3
            }
        }


class ConversionResponse(BaseModel):
    """Response model for code conversion"""
    success: bool
    generated_code: Optional[str] = None
    intent_graph: Optional[dict] = None
    validation_result: Optional[dict] = None
    iterations: int = 0
    processing_time: float = 0.0
    error_message: Optional[str] = None


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    timestamp: float


class LanguagesResponse(BaseModel):
    """Supported languages response"""
    source_languages: list[str]
    target_languages: list[str]


# ============================================================================ 
# ENDPOINTS
# ============================================================================ 

@app.get("/", tags=["General"])
async def root():
    """Root endpoint"""
    return {
        "message": "Code Converter API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthResponse, tags=["General"])
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        timestamp=time.time()
    )


@app.get("/languages", response_model=LanguagesResponse, tags=["General"])
async def get_languages():
    """Get list of supported languages"""
    return LanguagesResponse(
        source_languages=["R", "Python"],
        target_languages=["Python", "R"]
    )


@app.get("/stats", tags=["Monitoring"])
async def get_stats(hours: int = 24):
    """
    Get conversion statistics from Elasticsearch.
    
    Args:
        hours: Number of hours to look back (default: 24)
        
    Returns:
        Statistics including total conversions, success rate, etc.
    """
    logger = get_logger()
    stats = logger.get_stats(hours=hours)
    return stats


@app.post("/convert", response_model=ConversionResponse, tags=["Conversion"])
async def convert_code(request: ConversionRequest):
    """
    Convert code from source language to target language using the multi-agent workflow.
    Logs conversions to Elasticsearch.
    """
    start_time = time.time()
    logger = get_logger()
    
    try:
        # Validate input
        if not request.source_code or not request.source_code.strip():
            raise HTTPException(status_code=400, detail="Source code cannot be empty")
        
        if request.max_iterations < 1 or request.max_iterations > 10:
            raise HTTPException(status_code=400, detail="max_iterations must be between 1 and 10")
        
        # Run conversion workflow
        result = convert_with_workflow(
            source_code=request.source_code,
            source_lang=request.source_language,
            target_lang=request.target_language,
            max_iterations=request.max_iterations
        )
        
        processing_time = time.time() - start_time
        
        if result:
            # Log successful conversion
            logger.log_conversion(
                source_lang=request.source_language,
                target_lang=request.target_language,
                status="success",
                duration=processing_time,
                iterations=result.get("iteration_count", 0),
                code_length=len(result.get("generated_code", ""))
            )
            
            return ConversionResponse(
                success=True,
                generated_code=result.get("generated_code", ""),
                intent_graph=result.get("intent_graph", {}),
                validation_result=result.get("validation_result", {}),
                iterations=result.get("iteration_count", 0),
                processing_time=processing_time,
                error_message=result.get("error_message")
            )
        else:
            raise HTTPException(status_code=500, detail="Conversion workflow failed")
        
    except HTTPException:
        raise
    except Exception as e:
        processing_time = time.time() - start_time
        # Log failed conversion
        logger.log_conversion(
            source_lang=request.source_language,
            target_lang=request.target_language,
            status="failed",
            duration=processing_time
        )
        logger.log_error(
            error_type="api_error",
            message=str(e)
        )
        return ConversionResponse(
            success=False,
            error_message=str(e),
            processing_time=processing_time
        )


@app.post("/convert/file", response_model=ConversionResponse, tags=["Conversion"])
async def convert_file(
    file: UploadFile = File(...),
    target_language: str = "Python",
    max_iterations: int = 3
):
    """
    Convert code from uploaded file.
    """
    try:
        # Read file
        content = await file.read()
        source_code = content.decode('utf-8')
        
        # Detect source language from extension
        filename = file.filename.lower()
        if filename.endswith('.r'):
            source_language = "R"
        elif filename.endswith('.py'):
            source_language = "Python"
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type. Use .r or .py files")
        
        # Create request
        request = ConversionRequest(
            source_code=source_code,
            source_language=source_language,
            target_language=target_language,
            max_iterations=max_iterations
        )
        
        # Convert
        return await convert_code(request)
        
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="File must be valid UTF-8 text")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================ 
# RUN SERVER
# ============================================================================ 

if __name__ == "__main__":
    print("="*70)
    print("🚀 Starting Code Converter API Server")
    print("="*70)
    print("📍 API: http://localhost:8000")
    print("📚 Docs: http://localhost:8000/docs")
    print("💚 Health: http://localhost:8000/health")
    print("="*70)
    
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # Auto-reload on code changes
    )
