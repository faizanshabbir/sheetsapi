import json
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from typing import List, Dict, Any, Optional
import re
from app.core.config import settings
from app.services.operations.index_based import IndexBasedOperations
from app.services.operations.field_based import FieldBasedOperations

class GoogleSheetsService(IndexBasedOperations, FieldBasedOperations):
    def __init__(self):
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']  # Full read/write access
        
        self.credentials = service_account.Credentials.from_service_account_info(
            settings.google_credentials_dict,
            scopes=SCOPES
        )
        
        self.service = build('sheets', 'v4', credentials=self.credentials)
        
        # Initialize operation mixins
        IndexBasedOperations.__init__(self, self.service)
        FieldBasedOperations.__init__(self, self.service)
    
    async def get_sheet_data(self, spreadsheet_id: str, range_name: str) -> List[Dict[Any, Any]]:
        try:
            sheet = self.service.spreadsheets()
            result = sheet.values().get(
                spreadsheetId=spreadsheet_id,
                range=range_name
            ).execute()
            
            values = result.get('values', [])
            if not values:
                return []
            
            # Convert to JSON-friendly format
            headers = values[0]
            rows = values[1:]
            
            return [
                dict(zip(headers, row))
                for row in rows
            ]
        except Exception as e:
            raise Exception(f"Error fetching sheet data: {str(e)}")

    @staticmethod
    def extract_sheet_id(url: str) -> str:
        """Extract the sheet ID from a Google Sheets URL."""
        # Pattern for both old and new Google Sheets URLs
        patterns = [
            r"/spreadsheets/d/([a-zA-Z0-9-_]+)",
            r"spreadsheet:([a-zA-Z0-9-_]+)",
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
                
        raise ValueError("Invalid Google Sheets URL")

    @staticmethod
    def validate_sheet_access(sheet_id: str) -> bool:
        """Validate if we can access the sheet."""
        # TODO: Implement actual Google Sheets API validation
        return True

    async def get_raw_data(self, spreadsheet_id: str) -> List[List]:
        """Get raw sheet data as list of lists"""
        try:
            sheet = self.service.spreadsheets()
            result = sheet.values().get(
                spreadsheetId=spreadsheet_id,
                range="A1:Z1000"  # Default range
            ).execute()
            
            return result.get('values', [])
        except Exception as e:
            raise Exception(f"Error fetching raw sheet data: {str(e)}")

    async def add_row_at_position(self, spreadsheet_id: str, range_name: str, row_data: Dict[str, Any], position: str = "end") -> Dict[str, Any]:
        """Add a new row to the Google Sheet at specified position"""
        try:
            # Get current headers to ensure data alignment
            headers = await self._get_headers(spreadsheet_id)
            
            # Prepare row data in the correct order
            row_values = []
            for header in headers:
                row_values.append(str(row_data.get(header, "")))
            
            # Determine insert position
            if position == "end":
                # Add at the end (current behavior)
                sheet = self.service.spreadsheets()
                result = sheet.values().append(
                    spreadsheetId=spreadsheet_id,
                    range=range_name,
                    valueInputOption='RAW',
                    insertDataOption='INSERT_ROWS',
                    body={'values': [row_values]}
                ).execute()
                
                return {
                    "message": "Row added successfully at end",
                    "updated_range": result.get('updates', {}).get('updatedRange', ''),
                    "updated_rows": result.get('updates', {}).get('updatedRows', 0),
                    "position": "end"
                }
                
            elif position == "beg":
                # Insert at beginning (row 2, after headers)
                sheet = self.service.spreadsheets()
                
                # Get the sheet ID
                sheet_metadata = sheet.get(spreadsheetId=spreadsheet_id).execute()
                sheet_id = sheet_metadata['sheets'][0]['properties']['sheetId']
                
                # First insert a row at position 2
                result1 = sheet.batchUpdate(
                    spreadsheetId=spreadsheet_id,
                    body={
                        'requests': [
                            {
                                'insertDimension': {
                                    'range': {
                                        'sheetId': sheet_id,
                                        'dimension': 'ROWS',
                                        'startIndex': 1,  # 0-indexed, so row 2
                                        'endIndex': 2
                                    }
                                }
                            }
                        ]
                    }
                ).execute()
                
                # Then add the data to the new row
                result2 = sheet.values().update(
                    spreadsheetId=spreadsheet_id,
                    range="A2:Z2",  # Insert at row 2, covering all columns
                    valueInputOption='RAW',
                    body={'values': [row_values]}
                ).execute()
                
                return {
                    "message": "Row added successfully at beginning",
                    "updated_range": result2.get('updates', {}).get('updatedRange', ''),
                    "updated_rows": result2.get('updates', {}).get('updatedRows', 0),
                    "position": "beg"
                }
                
            else:
                # Insert at specific row index
                try:
                    row_index = int(position)
                    if row_index < 1:
                        raise ValueError("Row index must be 1 or greater")
                except ValueError:
                    raise Exception(f"Invalid position '{position}'. Use 'beg', 'end', or a number.")
                
                # Calculate actual row (add 1 for header row)
                actual_row = row_index + 1
                
                sheet = self.service.spreadsheets()
                
                # Use batchUpdate to insert row and add data in one operation
                # First, we need to get the sheet ID
                sheet_metadata = sheet.get(spreadsheetId=spreadsheet_id).execute()
                sheet_id = sheet_metadata['sheets'][0]['properties']['sheetId']
                
                # Create the batch update request
                batch_request = {
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
                
                # Execute the batch update to insert the row
                result1 = sheet.batchUpdate(
                    spreadsheetId=spreadsheet_id,
                    body=batch_request
                ).execute()
                
                # Now add the data to the newly inserted row
                result2 = sheet.values().update(
                    spreadsheetId=spreadsheet_id,
                    range=f"A{actual_row}:Z{actual_row}",
                    valueInputOption='RAW',
                    body={'values': [row_values]}
                ).execute()
                
                return {
                    "message": f"Row added successfully at position {row_index}",
                    "updated_range": result2.get('updates', {}).get('updatedRange', ''),
                    "updated_rows": result2.get('updates', {}).get('updatedRows', 0),
                    "position": str(row_index)
                }
            
        except Exception as e:
            error_msg = str(e)
            if "403" in error_msg and "permission" in error_msg.lower():
                raise Exception(f"Permission denied: Service account needs Editor role. Current error: {error_msg}")
            else:
                raise Exception(f"Error adding row: {error_msg}")

    async def add_row(self, spreadsheet_id: str, range_name: str, row_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a new row to the Google Sheet (legacy method for backward compatibility)"""
        return await self.add_row_at_position(spreadsheet_id, range_name, row_data, "end")

    # Note: update_row and delete_row methods are now in IndexBasedOperations mixin
    # Use update_row_by_index() and delete_row_by_index() instead

    def get_service_account_email(self) -> str:
        """Get the service account email for sharing sheets"""
        try:
            return self.credentials.service_account_email
        except Exception as e:
            raise Exception(f"Error getting service account email: {str(e)}")

    async def check_sheet_permissions(self, spreadsheet_id: str) -> Dict[str, Any]:
        """Check if we have read access to a sheet"""
        try:
            # Try to get sheet metadata
            sheet = self.service.spreadsheets()
            result = sheet.get(spreadsheetId=spreadsheet_id).execute()
            
            return {
                "has_access": True,
                "sheet_title": result.get('properties', {}).get('title', 'Unknown'),
                "service_account_email": self.get_service_account_email(),
                "message": "✅ Sheet accessible with read permissions. Write operations will be tested when you try them."
            }
        except Exception as e:
            return {
                "has_access": False,
                "error": str(e),
                "service_account_email": self.get_service_account_email(),
                "message": "❌ Cannot access sheet. Add service account as editor."
            }
