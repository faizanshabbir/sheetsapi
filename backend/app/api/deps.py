from fastapi import Header, HTTPException
from typing import Optional
import jwt
from app.core.config import settings

async def get_current_user(authorization: Optional[str] = Header(None)) -> str:
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        # Verify the JWT token from Clerk
        token = authorization.replace('Bearer ', '')
        # You'll need to implement proper JWT verification here
        # For now, we'll just extract the user ID
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
        return payload.get("sub")
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid authentication token") 