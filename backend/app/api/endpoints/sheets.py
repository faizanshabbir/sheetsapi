from fastapi import APIRouter, HTTPException, Query, Depends, Request
from typing import List
from pydantic import BaseModel
from datetime import datetime
import uuid
from app.services.google_sheets import GoogleSheetsService
from app.services.sheet_template import SheetValidator, SheetTemplate, SheetType
from app.models.api_endpoint import APIEndpoint
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user

router = APIRouter()
sheets_service = GoogleSheetsService()
validator = SheetValidator()

# Helper functions (moved to top)
async def log_request_body(request: Request):
    body = await request.json()  # or request.body() for raw bytes
    print("Request Body:", body)
    return body

async def log_request_query(request: Request):
    query_params = request.query_params
    print("Query Parameters:", query_params)
    return query_params

class SheetCreate(BaseModel):
    sheet_url: str
    name: str
    sheet_range: str = "A1:Z1000"  # Default range

class SheetResponse(BaseModel):
    id: int
    name: str
    sheet_id: str
    endpoint_path: str
    created_at: datetime

@router.get("/auth/debug")
async def debug_auth(current_user: str = Depends(get_current_user)):
    """Debug endpoint to test JWT authentication"""
    return {
        "message": "Authentication successful!",
        "user_id": current_user,
        "timestamp": datetime.now().isoformat(),
        "status": "authenticated"
    }

@router.get("/auth/debug-no-auth")
async def debug_no_auth():
    """Debug endpoint without authentication for comparison"""
    return {
        "message": "No authentication required",
        "timestamp": datetime.now().isoformat(),
        "status": "unauthenticated"
    }

@router.get("/sheets/{sheet_id}")
async def read_sheet(
    sheet_id: str,
    range: str = None
):
    try:
        sheet = sheets_service.service.spreadsheets()
        
        # If no range specified, read all data
        if not range:
            metadata = sheet.get(spreadsheetId=sheet_id).execute()
            sheet_name = metadata['sheets'][0]['properties']['title']
            range = f"{sheet_name}"
            
        result = sheet.values().get(
            spreadsheetId=sheet_id,
            range=range
        ).execute()
        
        values = result.get('values', [])
        
        # Debug information
        return {
            "raw_data": values,  # Show the raw data
            "num_rows": len(values),
            "row_lengths": [len(row) for row in values] if values else [],
            "first_row": values[0] if values else [],
            "sample_rows": values[1:5] if len(values) > 1 else []  # Show first few rows
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error fetching sheet data: {str(e)}")

@router.get("/sheets/{sheet_id}/analyze")
async def analyze_sheet(
    sheet_id: str,
    sheet_type: SheetType = SheetType.TABLE
):
    """Analyzes sheet structure and provides guidance"""
    try:
        data = await sheets_service.get_raw_data(sheet_id)
        
        # Basic template for analysis
        template = SheetTemplate(
            required_headers=["id", "name", "created_at"],  # Example headers
            sheet_type=sheet_type
        )
        
        analysis = validator.validate_structure(data, template)
        
        return {
            "analysis": analysis,
            "suggestions": {
                "structure": "Consider adding headers in row 1" if not analysis["headers"] else None,
                "format": "Use consistent data types per column",
                "missing": f"Add required columns: {analysis['missing_headers']}" if analysis["missing_headers"] else None,
            },
            "sample_data": data[:5] if data else [],
            "detected_structure": {
                "has_headers": bool(analysis["headers"]),
                "num_columns": len(data[0]) if data else 0,
                "num_rows": len(data) - 1 if data else 0
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/sheets/{sheet_id}/validate")
async def validate_sheet(
    sheet_id: str,
    template: SheetTemplate
):
    """Validates sheet against a specific template"""
    # Implementation for template validation

@router.post("/sheets", response_model=SheetResponse)
async def create_sheet_api(
    sheet: SheetCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    # Extract sheet ID from URL
    try:
        sheet_id = GoogleSheetsService.extract_sheet_id(sheet.sheet_url)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid Google Sheet URL")

    # Generate unique endpoint ID
    endpoint_id = str(uuid.uuid4())
    endpoint_path = f"/api/v1/data/{endpoint_id}"

    # Create new API endpoint with the actual user ID
    db_endpoint = APIEndpoint(
        user_id=current_user,
        name=sheet.name,
        sheet_id=sheet_id,
        sheet_range=sheet.sheet_range,
        endpoint_path=endpoint_path
    )
    
    db.add(db_endpoint)
    db.commit()
    db.refresh(db_endpoint)

    return SheetResponse(
        id=db_endpoint.id,
        name=db_endpoint.name,
        sheet_id=db_endpoint.sheet_id,
        endpoint_path=db_endpoint.endpoint_path,
        created_at=db_endpoint.created_at
    )

@router.get("/sheets", response_model=List[SheetResponse])
async def get_sheets(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Get all API endpoints for the current user"""
    try:
        # Filter sheets by current user
        sheets = db.query(APIEndpoint).filter(
            APIEndpoint.user_id == current_user
        ).all()
        
        return [
            SheetResponse(
                id=sheet.id,
                name=sheet.name,
                sheet_id=sheet.sheet_id,
                endpoint_path=sheet.endpoint_path,
                created_at=sheet.created_at
            ) for sheet in sheets
        ]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
