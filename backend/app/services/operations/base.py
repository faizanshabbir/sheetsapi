from typing import List, Dict, Any
from googleapiclient.discovery import Resource

class BaseOperations:
    """Base class for Google Sheets operations with common utilities"""
    
    def __init__(self, service: Resource):
        self.service = service
    
    async def _get_headers(self, spreadsheet_id: str) -> List[str]:
        """Get headers from the sheet"""
        try:
            sheet = self.service.spreadsheets()
            result = sheet.values().get(
                spreadsheetId=spreadsheet_id,
                range="A1:Z1"  # Get first row (headers) from first sheet
            ).execute()
            
            values = result.get('values', [])
            if not values:
                return []
            
            return values[0]
        except Exception as e:
            raise Exception(f"Error getting headers: {str(e)}")
    
    def _prepare_row_values(self, headers: List[str], row_data: Dict[str, Any]) -> List[str]:
        """Prepare row data in the correct order based on headers"""
        row_values = []
        for header in headers:
            row_values.append(str(row_data.get(header, "")))
        return row_values
    
    def _handle_permission_error(self, error: Exception, operation: str) -> Exception:
        """Handle permission errors with helpful messages"""
        error_msg = str(error)
        if "403" in error_msg and "permission" in error_msg.lower():
            return Exception(f"Permission denied: Service account needs Editor role. {operation} error: {error_msg}")
        else:
            return Exception(f"Error in {operation}: {error_msg}") 