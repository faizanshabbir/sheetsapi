from fastapi import APIRouter, HTTPException, Query, Depends
from typing import Optional, List, Dict, Any
from app.services.google_sheets import GoogleSheetsService
from app.models.api_endpoint import APIEndpoint
from sqlalchemy.orm import Session
from app.db.session import get_db

router = APIRouter()
sheets_service = GoogleSheetsService()

@router.get("/data/{endpoint_id}")
async def get_dynamic_data(
    endpoint_id: str,
    limit: Optional[int] = Query(100, ge=1, le=1000),
    offset: Optional[int] = Query(0, ge=0),
    sort_by: Optional[str] = None,
    sort_order: Optional[str] = Query("asc", regex="^(asc|desc)$"),
    debug: Optional[bool] = Query(False, description="Show debug information"),
    db: Session = Depends(get_db)
):
    """Get data from a Google Sheet via dynamic endpoint"""
    try:
        # 1. Look up the endpoint in database
        api_endpoint = db.query(APIEndpoint).filter(APIEndpoint.endpoint_path == f"/api/v1/data/{endpoint_id}").first()
        
        if not api_endpoint:
            raise HTTPException(status_code=404, detail="API endpoint not found")
        
        # 2. Get data from Google Sheets
        sheet_data = await sheets_service.get_sheet_data(
            api_endpoint.sheet_id, 
            api_endpoint.sheet_range
        )
        
        # 3. Apply basic filtering and pagination
        if sort_by and sheet_data:
            # Improved sorting with case-insensitive column matching and better handling of missing values
            reverse = sort_order == "desc"
            
            # Find the actual column name (case-insensitive)
            actual_column = None
            if sheet_data:
                available_columns = list(sheet_data[0].keys())
                print(f"Debug: Looking for column '{sort_by}' in available columns: {available_columns}")
                
                for col in available_columns:
                    if col.lower() == sort_by.lower():
                        actual_column = col
                        print(f"Debug: Found matching column '{col}' for '{sort_by}'")
                        break
                
                if not actual_column:
                    print(f"Debug: No exact match found for '{sort_by}'. Available columns: {available_columns}")
            
            if actual_column:
                # Sort with proper handling of missing values and data types
                def sort_key(item):
                    value = item.get(actual_column, "")
                    # Handle numeric values
                    if isinstance(value, str) and value.replace('.', '').replace('-', '').isdigit():
                        return float(value) if '.' in value else int(value)
                    # Handle empty/missing values
                    if value == "" or value is None:
                        return "" if not reverse else "zzzzzzzzzz"  # Put empty values at end for desc
                    return str(value).lower()  # Case-insensitive string comparison
                
                sheet_data = sorted(sheet_data, key=sort_key, reverse=reverse)
            else:
                # If column not found, return error or ignore sorting
                print(f"Warning: Column '{sort_by}' not found in data. Available columns: {list(sheet_data[0].keys()) if sheet_data else []}")
        
        # Apply pagination
        total_count = len(sheet_data)
        sheet_data = sheet_data[offset:offset + limit]
        
        # 4. Return JSON response
        response = {
            "data": sheet_data,
            "pagination": {
                "total": total_count,
                "limit": limit,
                "offset": offset,
                "has_more": offset + limit < total_count
            },
            "endpoint_info": {
                "name": api_endpoint.name,
                "sheet_id": api_endpoint.sheet_id,
                "created_at": api_endpoint.created_at
            }
        }
        
        # Add debug information if requested
        if debug and sheet_data:
            response["debug"] = {
                "available_columns": list(sheet_data[0].keys()) if sheet_data else [],
                "sort_by_requested": sort_by,
                "sort_order_requested": sort_order,
                "total_rows": len(sheet_data),
                "sample_data": sheet_data[:2] if len(sheet_data) >= 2 else sheet_data
            }
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {str(e)}")

@router.post("/data/{endpoint_id}")
async def create_dynamic_row(
    endpoint_id: str,
    row_data: Dict[str, Any],
    position: Optional[str] = Query("end", description="Insert position: 'beg', 'end', or row index number"),
    db: Session = Depends(get_db)
):
    """Add a new row to the Google Sheet"""
    try:
        # 1. Look up the endpoint
        api_endpoint = db.query(APIEndpoint).filter(APIEndpoint.endpoint_path == f"/api/v1/data/{endpoint_id}").first()
        
        if not api_endpoint:
            raise HTTPException(status_code=404, detail="API endpoint not found")
        
        # 2. Add row to Google Sheet at specified position
        result = await sheets_service.add_row_at_position(
            api_endpoint.sheet_id,
            api_endpoint.sheet_range,
            row_data,
            position
        )
        
        return {
            "message": "Row created successfully",
            "endpoint_id": endpoint_id,
            "data": row_data,
            "result": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating row: {str(e)}")

@router.put("/data/{endpoint_id}/{row_id}")
async def update_dynamic_row(
    endpoint_id: str,
    row_id: str,
    row_data: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """Update a row in the Google Sheet"""
    try:
        # 1. Look up the endpoint
        api_endpoint = db.query(APIEndpoint).filter(APIEndpoint.endpoint_path == f"/api/v1/data/{endpoint_id}").first()
        
        if not api_endpoint:
            raise HTTPException(status_code=404, detail="API endpoint not found")
        
        # 2. Convert row_id to integer (assuming it's the row index)
        try:
            row_index = int(row_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid row_id. Must be a number.")
        
        # 3. Update row in Google Sheet
        result = await sheets_service.update_row_by_index(
            api_endpoint.sheet_id,
            api_endpoint.sheet_range,
            row_index,
            row_data
        )
        
        return {
            "message": "Row updated successfully",
            "endpoint_id": endpoint_id,
            "row_id": row_id,
            "data": row_data,
            "result": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating row: {str(e)}")

@router.delete("/data/{endpoint_id}/{row_id}")
async def delete_dynamic_row(
    endpoint_id: str,
    row_id: str,
    db: Session = Depends(get_db)
):
    """Delete a row from the Google Sheet"""
    try:
        # 1. Look up the endpoint
        api_endpoint = db.query(APIEndpoint).filter(APIEndpoint.endpoint_path == f"/api/v1/data/{endpoint_id}").first()
        
        if not api_endpoint:
            raise HTTPException(status_code=404, detail="API endpoint not found")
        
        # 2. Convert row_id to integer (assuming it's the row index)
        try:
            row_index = int(row_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid row_id. Must be a number.")
        
        # 3. Delete row from Google Sheet
        result = await sheets_service.delete_row_by_index(
            api_endpoint.sheet_id,
            api_endpoint.sheet_range,
            row_index
        )
        
        return {
            "message": "Row deleted successfully",
            "endpoint_id": endpoint_id,
            "row_id": row_id,
            "result": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting row: {str(e)}")

@router.get("/data/{endpoint_id}/debug")
async def debug_endpoint(
    endpoint_id: str,
    db: Session = Depends(get_db)
):
    """Debug endpoint to check permissions and service account info"""
    try:
        # 1. Look up the endpoint
        api_endpoint = db.query(APIEndpoint).filter(APIEndpoint.endpoint_path == f"/api/v1/data/{endpoint_id}").first()
        
        if not api_endpoint:
            raise HTTPException(status_code=404, detail="API endpoint not found")
        
        # 2. Check permissions
        permissions = await sheets_service.check_sheet_permissions(api_endpoint.sheet_id)
        
        # Determine setup instructions based on permissions
        # TODO: review the below, maybe too verbose and confusign for users
        if permissions.get("has_access", False):
            setup_instructions = {
                "status": "✅ Read access confirmed",
                "message": "Your sheet is accessible for reading. Write permissions will be tested when you try POST, PUT, or DELETE operations.",
                "service_account_email": permissions.get('service_account_email', 'Unknown'),
                "setup_for_write": {
                    "step1": f"Share your Google Sheet with: {permissions.get('service_account_email', 'Unknown')}",
                    "step2": "Give it 'Editor' permissions (not Viewer or Commenter)",
                    "step3": "Try a write operation (POST/PUT/DELETE) to test permissions"
                },
                "note": "If write operations fail, you'll get a clear error message explaining the permission issue."
            }
        else:
            setup_instructions = {
                "status": "❌ No access",
                "message": "Cannot access sheet. Service account needs to be added as editor.",
                "step1": f"Share your Google Sheet with: {permissions.get('service_account_email', 'Unknown')}",
                "step2": "Give it 'Editor' permissions",
                "step3": "Try the debug endpoint again to verify access"
            }
        
        return {
            "endpoint_info": {
                "name": api_endpoint.name,
                "sheet_id": api_endpoint.sheet_id,
                "sheet_range": api_endpoint.sheet_range
            },
            "permissions": permissions,
            "setup_instructions": setup_instructions
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking permissions: {str(e)}") 