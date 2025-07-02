from fastapi import APIRouter, HTTPException, Query, Depends, Request
from typing import Dict, Any
from app.services.google_sheets import GoogleSheetsService
from app.models.api_endpoint import APIEndpoint
from sqlalchemy.orm import Session
from app.db.session import get_db

router = APIRouter()
sheets_service = GoogleSheetsService()

@router.put("/data/{endpoint_id}/field/update")
async def update_dynamic_rows_by_field(
    endpoint_id: str,
    request: Request,
    db: Session = Depends(get_db)
):
    """Update rows in the Google Sheet that match field criteria (SheetDB.io approach)"""
    try:
        # 1. Look up the endpoint
        api_endpoint = db.query(APIEndpoint).filter(APIEndpoint.endpoint_path == f"/api/v1/data/{endpoint_id}").first()
        
        if not api_endpoint:
            raise HTTPException(status_code=404, detail="API endpoint not found")
        
        # 2. Get the request body (row_data)
        try:
            body = await request.json()
            row_data = body
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid JSON in request body")
        
        # 3. Convert query parameters to field criteria dict
        criteria_dict = {}
        query_params = dict(request.query_params)
        
        for field, value in query_params.items():
            # Handle URL encoding for field names with spaces
            decoded_field = field.replace('%20', ' ')
            criteria_dict[decoded_field] = value
        
        if not criteria_dict:
            raise HTTPException(status_code=400, detail="At least one field criteria must be provided")
        
        # 4. Update rows in Google Sheet
        result = await sheets_service.update_rows_by_field(
            api_endpoint.sheet_id,
            api_endpoint.sheet_range,
            criteria_dict,
            row_data
        )
        
        return {
            "message": result["message"],
            "endpoint_id": endpoint_id,
            "data": row_data,
            "criteria": criteria_dict,
            "result": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating rows: {str(e)}")

@router.delete("/data/{endpoint_id}/field/delete")
async def delete_dynamic_rows_by_field(
    endpoint_id: str,
    request: Request,
    db: Session = Depends(get_db)
):
    """Delete rows from the Google Sheet that match field criteria (SheetDB.io approach)"""
    try:
        # 1. Look up the endpoint
        api_endpoint = db.query(APIEndpoint).filter(APIEndpoint.endpoint_path == f"/api/v1/data/{endpoint_id}").first()
        
        if not api_endpoint:
            raise HTTPException(status_code=404, detail="API endpoint not found")
        
        # 2. Convert query parameters to field criteria dict
        criteria_dict = {}
        query_params = dict(request.query_params)
        
        for field, value in query_params.items():
            # Handle URL encoding for field names with spaces
            decoded_field = field.replace('%20', ' ')
            criteria_dict[decoded_field] = value
        
        if not criteria_dict:
            raise HTTPException(status_code=400, detail="At least one field criteria must be provided")
        
        # 3. Delete rows from Google Sheet
        result = await sheets_service.delete_rows_by_field(
            api_endpoint.sheet_id,
            api_endpoint.sheet_range,
            criteria_dict
        )
        
        return {
            "message": result["message"],
            "endpoint_id": endpoint_id,
            "criteria": criteria_dict,
            "result": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting rows: {str(e)}")

@router.post("/data/{endpoint_id}/field/insert")
async def insert_dynamic_row_by_field(
    endpoint_id: str,
    row_data: Dict[str, Any],
    request: Request,
    db: Session = Depends(get_db)
):
    """Insert a new row after rows that match field criteria (SheetDB.io approach)"""
    try:
        # 1. Look up the endpoint
        api_endpoint = db.query(APIEndpoint).filter(APIEndpoint.endpoint_path == f"/api/v1/data/{endpoint_id}").first()
        
        if not api_endpoint:
            raise HTTPException(status_code=404, detail="API endpoint not found")
        
        # 2. Get the request body (row_data)
        try:
            body = await request.json()
            row_data = body
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid JSON in request body")
        
        # 3. Convert query parameters to field criteria dict
        criteria_dict = {}
        query_params = dict(request.query_params)
        
        for field, value in query_params.items():
            # Handle URL encoding for field names with spaces
            decoded_field = field.replace('%20', ' ')
            criteria_dict[decoded_field] = value
        
        if not criteria_dict:
            raise HTTPException(status_code=400, detail="At least one field criteria must be provided")
        
        # 4. Insert row after matching rows in Google Sheet
        result = await sheets_service.insert_row_after_field_match(
            api_endpoint.sheet_id,
            api_endpoint.sheet_range,
            criteria_dict,
            row_data
        )
        
        return {
            "message": result["message"],
            "endpoint_id": endpoint_id,
            "data": row_data,
            "criteria": criteria_dict,
            "result": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inserting row: {str(e)}") 