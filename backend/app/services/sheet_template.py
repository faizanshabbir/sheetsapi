from enum import Enum
from typing import List, Dict, Optional
from pydantic import BaseModel

class SheetType(Enum):
    TABLE = "table"  # Standard table with headers
    KEY_VALUE = "key_value"  # Key-value pairs
    MULTI_TABLE = "multi_table"  # Multiple tables in one sheet

class SheetTemplate(BaseModel):
    required_headers: List[str]
    sheet_type: SheetType
    validation_rules: Optional[Dict] = None
    
class SheetValidator:
    def validate_structure(self, data: List[List], template: SheetTemplate) -> Dict:
        if not data:
            return {"valid": False, "error": "Empty sheet"}
            
        if template.sheet_type == SheetType.TABLE:
            return self._validate_table(data, template)
        elif template.sheet_type == SheetType.KEY_VALUE:
            return self._validate_key_value(data, template)
            
    def _validate_table(self, data: List[List], template: SheetTemplate) -> Dict:
        headers = [h.strip().lower() for h in data[0] if h]
        missing_headers = set(template.required_headers) - set(headers)
        
        return {
            "valid": len(missing_headers) == 0,
            "headers": headers,
            "missing_headers": list(missing_headers),
            "suggestions": self._generate_suggestions(headers, template.required_headers)
        }
