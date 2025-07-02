from typing import Dict, Any
from .base import BaseOperations

class IndexBasedOperations(BaseOperations):
    """Index-based operations for Google Sheets (current approach)"""
    
    async def update_row_by_index(self, spreadsheet_id: str, range_name: str, row_index: int, row_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing row in the Google Sheet by index"""
        try:
            # Get current headers
            headers = await self._get_headers(spreadsheet_id)
            
            # Prepare row data in the correct order
            row_values = self._prepare_row_values(headers, row_data)
            
            # Calculate the actual row range (add 1 for header row, add 1 because sheets are 1-indexed)
            actual_row = row_index + 2  # +2 because: +1 for header, +1 for 1-indexed sheets
            
            # Update the row
            sheet = self.service.spreadsheets()
            result = sheet.values().update(
                spreadsheetId=spreadsheet_id,
                range=f"A{actual_row}:Z{actual_row}",  # Use simple range format
                valueInputOption='RAW',
                body={'values': [row_values]}
            ).execute()
            
            return {
                "message": "Row updated successfully",
                "updated_range": result.get('updatedRange', ''),
                "updated_rows": result.get('updatedRows', 0),
                "method": "index_based",
                "row_index": row_index
            }
            
        except Exception as e:
            raise self._handle_permission_error(e, "updating row by index")

    async def delete_row_by_index(self, spreadsheet_id: str, range_name: str, row_index: int) -> Dict[str, Any]:
        """Delete a row from the Google Sheet by index"""
        try:
            # Calculate the actual row number (add 1 for header row, add 1 because sheets are 1-indexed)
            actual_row = row_index + 2  # +2 because: +1 for header, +1 for 1-indexed sheets
            
            # Delete the row using batchUpdate
            sheet = self.service.spreadsheets()
            result = sheet.batchUpdate(
                spreadsheetId=spreadsheet_id,
                body={
                    'requests': [
                        {
                            'deleteDimension': {
                                'range': {
                                    'sheetId': 0,  # Assuming first sheet, you might need to get actual sheet ID
                                    'dimension': 'ROWS',
                                    'startIndex': actual_row - 1,  # 0-indexed for API
                                    'endIndex': actual_row  # 0-indexed for API
                                }
                            }
                        }
                    ]
                }
            ).execute()
            
            return {
                "message": "Row deleted successfully",
                "deleted_range": f"Row {actual_row}",
                "method": "index_based",
                "row_index": row_index
            }
            
        except Exception as e:
            raise self._handle_permission_error(e, "deleting row by index") 