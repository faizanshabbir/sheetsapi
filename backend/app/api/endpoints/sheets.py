from fastapi import APIRouter, HTTPException, Query
from app.services.google_sheets import GoogleSheetsService
from app.services.sheet_template import SheetValidator, SheetTemplate, SheetType

router = APIRouter()
sheets_service = GoogleSheetsService()
validator = SheetValidator()

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
