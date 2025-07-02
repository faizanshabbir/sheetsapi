from typing import Dict, Any, List
from .base import BaseOperations

class FieldBasedOperations(BaseOperations):
    """Field-based operations for Google Sheets (SheetDB.io approach)"""
    
    async def update_rows_by_field(self, spreadsheet_id: str, range_name: str, field_criteria: Dict[str, str], row_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update rows in the Google Sheet that match field criteria"""
        try:
            # Get current data to find matching rows
            sheet = self.service.spreadsheets()
            result = sheet.values().get(
                spreadsheetId=spreadsheet_id,
                range="A1:Z1000"  # Get all data
            ).execute()
            
            values = result.get('values', [])
            if not values or len(values) < 2:  # Need headers + at least one data row
                return {
                    "message": "No data found to update",
                    "updated_rows": 0,
                    "method": "field_based",
                    "criteria": field_criteria
                }
            
            headers = values[0]
            data_rows = values[1:]
            
            # Find rows that match the criteria
            matching_row_indices = []
            for i, row in enumerate(data_rows):
                if self._row_matches_criteria(row, headers, field_criteria):
                    matching_row_indices.append(i)
            
            if not matching_row_indices:
                return {
                    "message": "No rows found matching criteria",
                    "updated_rows": 0,
                    "method": "field_based",
                    "criteria": field_criteria
                }
            
            # Update each matching row with partial updates
            updated_count = 0
            for row_index in matching_row_indices:
                actual_row = row_index + 2  # +2 because: +1 for header, +1 for 1-indexed sheets
                
                # Get the current row data
                current_row = data_rows[row_index]
                current_row_dict = {}
                for i, header in enumerate(headers):
                    if i < len(current_row):
                        current_row_dict[header] = current_row[i]
                    else:
                        current_row_dict[header] = ""
                
                # Merge with new data (partial update)
                merged_data = current_row_dict.copy()
                merged_data.update(row_data)
                
                # Prepare the merged row values
                merged_row_values = []
                for header in headers:
                    merged_row_values.append(str(merged_data.get(header, "")))
                
                result = sheet.values().update(
                    spreadsheetId=spreadsheet_id,
                    range=f"A{actual_row}:Z{actual_row}",
                    valueInputOption='RAW',
                    body={'values': [merged_row_values]}
                ).execute()
                updated_count += 1
            
            return {
                "message": f"Updated {updated_count} row(s) successfully",
                "updated_rows": updated_count,
                "method": "field_based",
                "criteria": field_criteria,
                "matching_rows": len(matching_row_indices)
            }
            
        except Exception as e:
            raise self._handle_permission_error(e, "updating rows by field")

    async def delete_rows_by_field(self, spreadsheet_id: str, range_name: str, field_criteria: Dict[str, str]) -> Dict[str, Any]:
        """Delete rows from the Google Sheet that match field criteria"""
        try:
            # Get current data to find matching rows
            sheet = self.service.spreadsheets()
            result = sheet.values().get(
                spreadsheetId=spreadsheet_id,
                range="A1:Z1000"  # Get all data
            ).execute()
            
            values = result.get('values', [])
            if not values or len(values) < 2:  # Need headers + at least one data row
                return {
                    "message": "No data found to delete",
                    "deleted_rows": 0,
                    "method": "field_based",
                    "criteria": field_criteria
                }
            
            headers = values[0]
            data_rows = values[1:]
            
            # Find rows that match the criteria
            matching_row_indices = []
            for i, row in enumerate(data_rows):
                if self._row_matches_criteria(row, headers, field_criteria):
                    matching_row_indices.append(i)
            
            if not matching_row_indices:
                return {
                    "message": "No rows found matching criteria",
                    "deleted_rows": 0,
                    "method": "field_based",
                    "criteria": field_criteria
                }
            
            # Delete rows in reverse order to maintain indices
            deleted_count = 0
            for row_index in reversed(matching_row_indices):
                actual_row = row_index + 2  # +2 because: +1 for header, +1 for 1-indexed sheets
                
                result = sheet.batchUpdate(
                    spreadsheetId=spreadsheet_id,
                    body={
                        'requests': [
                            {
                                'deleteDimension': {
                                    'range': {
                                        'sheetId': 0,  # Assuming first sheet
                                        'dimension': 'ROWS',
                                        'startIndex': actual_row - 1,  # 0-indexed for API
                                        'endIndex': actual_row  # 0-indexed for API
                                    }
                                }
                            }
                        ]
                    }
                ).execute()
                deleted_count += 1
            
            return {
                "message": f"Deleted {deleted_count} row(s) successfully",
                "deleted_rows": deleted_count,
                "method": "field_based",
                "criteria": field_criteria,
                "matching_rows": len(matching_row_indices)
            }
            
        except Exception as e:
            raise self._handle_permission_error(e, "deleting rows by field")
    
    def _row_matches_criteria(self, row: List[str], headers: List[str], field_criteria: Dict[str, str]) -> bool:
        """Check if a row matches the given field criteria"""
        # Create a dict from row data
        row_dict = {}
        for i, header in enumerate(headers):
            if i < len(row):
                row_dict[header] = row[i]
            else:
                row_dict[header] = ""
        
        # Check if all criteria match
        for field, value in field_criteria.items():
            if field not in row_dict or row_dict[field] != value:
                return False
        
        return True
    
    async def insert_row_after_field_match(self, spreadsheet_id: str, range_name: str, field_criteria: Dict[str, str], row_data: Dict[str, Any]) -> Dict[str, Any]:
        """Insert a new row after rows that match field criteria"""
        try:
            # Get current data to find matching rows
            sheet = self.service.spreadsheets()
            result = sheet.values().get(
                spreadsheetId=spreadsheet_id,
                range="A1:Z1000"  # Get all data
            ).execute()
            
            values = result.get('values', [])
            if not values or len(values) < 2:  # Need headers + at least one data row
                return {
                    "message": "No data found, inserting at beginning",
                    "inserted_rows": 1,
                    "method": "field_based",
                    "criteria": field_criteria,
                    "position": "beginning"
                }
            
            headers = values[0]
            data_rows = values[1:]
            
            # Find rows that match the criteria
            matching_row_indices = []
            for i, row in enumerate(data_rows):
                if self._row_matches_criteria(row, headers, field_criteria):
                    matching_row_indices.append(i)
            
            if not matching_row_indices:
                return {
                    "message": "No rows found matching criteria, inserting at end",
                    "inserted_rows": 1,
                    "method": "field_based",
                    "criteria": field_criteria,
                    "position": "end"
                }
            
            # Get headers and prepare row data
            headers = await self._get_headers(spreadsheet_id)
            row_values = self._prepare_row_values(headers, row_data)
            
            # Insert after the last matching row
            last_match_index = max(matching_row_indices)
            actual_row = last_match_index + 3  # +3 because: +1 for header, +1 for 1-indexed sheets, +1 to insert after
            
            # Get the sheet ID
            sheet_metadata = sheet.get(spreadsheetId=spreadsheet_id).execute()
            sheet_id = sheet_metadata['sheets'][0]['properties']['sheetId']
            
            # First insert a row at the specified position
            result1 = sheet.batchUpdate(
                spreadsheetId=spreadsheet_id,
                body={
                    'requests': [
                        {
                            'insertDimension': {
                                'range': {
                                    'sheetId': sheet_id,
                                    'dimension': 'ROWS',
                                    'startIndex': actual_row - 1,  # 0-indexed
                                    'endIndex': actual_row
                                }
                            }
                        }
                    ]
                }
            ).execute()
            
            # Then add the data to the new row
            result2 = sheet.values().update(
                spreadsheetId=spreadsheet_id,
                range=f"A{actual_row}:Z{actual_row}",
                valueInputOption='RAW',
                body={'values': [row_values]}
            ).execute()
            
            return {
                "message": f"Row inserted successfully after matching row",
                "inserted_rows": 1,
                "method": "field_based",
                "criteria": field_criteria,
                "position": f"after row {last_match_index + 1}",
                "matching_rows": len(matching_row_indices)
            }
            
        except Exception as e:
            raise self._handle_permission_error(e, "inserting row after field match") 