import json
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from typing import List, Dict, Any

class GoogleSheetsService:
    def __init__(self):
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
        
        # Get credentials from environment variable
        credentials_dict = json.loads(os.getenv('GOOGLE_CREDENTIALS'))
        
        credentials = service_account.Credentials.from_service_account_info(
            credentials_dict,
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
