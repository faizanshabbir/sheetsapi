import json
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from typing import List, Dict, Any, Optional
import re
from app.core.config import settings

class GoogleSheetsService:
    def __init__(self):
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
        
        credentials = service_account.Credentials.from_service_account_info(
            settings.google_credentials_dict,
            scopes=SCOPES
        )
        
        self.service = build('sheets', 'v4', credentials=credentials)
    
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
