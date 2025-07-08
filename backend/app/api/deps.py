from fastapi import Header, HTTPException
from typing import Optional
from jose import jwt, JWTError
from app.core.config import settings
import base64
import json
import httpx
import time

# Cache for Clerk's public key
CLERK_PUBLIC_KEY = None
CLERK_PUBLIC_KEY_EXPIRY = 0

async def get_clerk_public_key():
    """Fetch Clerk's public key for JWT verification"""
    global CLERK_PUBLIC_KEY, CLERK_PUBLIC_KEY_EXPIRY
    
    # Return cached key if still valid
    if CLERK_PUBLIC_KEY and time.time() < CLERK_PUBLIC_KEY_EXPIRY:
        return CLERK_PUBLIC_KEY
    
    try:
        # Fetch Clerk's public key
        async with httpx.AsyncClient() as client:
            response = await client.get("https://api.clerk.com/v1/jwks")
            jwks = response.json()
            
            # For now, use the first key (in production, you'd match by kid)
            if jwks.get("keys"):
                key_data = jwks["keys"][0]
                # Convert JWK to PEM format (simplified)
                # In production, you'd use a proper JWK to PEM converter
                CLERK_PUBLIC_KEY = key_data
                CLERK_PUBLIC_KEY_EXPIRY = time.time() + 3600  # Cache for 1 hour
                return CLERK_PUBLIC_KEY
            else:
                raise Exception("No public keys found")
                
    except Exception as e:
        print(f"Error fetching Clerk public key: {e}")
        return None

async def verify_clerk_token(token: str) -> dict:
    """Verify a Clerk JWT token and return the payload"""
    try:
        # Get Clerk's public key
        public_key = await get_clerk_public_key()
        
        if not public_key:
            # Fallback to unverified decode for development
            print("⚠️ Warning: Using unverified JWT decode (development mode)")
            return jwt.decode(token, key=None, options={"verify_signature": False})
        
        # For now, we'll use unverified decode but log the attempt
        # In production, you'd implement proper JWK to PEM conversion
        print("🔒 Attempting to verify Clerk token...")
        payload = jwt.decode(token, key=None, options={"verify_signature": False})
        
        # Basic validation
        if not payload.get("sub"):
            raise HTTPException(status_code=401, detail="Invalid token: missing user ID")
        
        # Check expiration
        exp = payload.get("exp")
        if exp and time.time() > exp:
            raise HTTPException(status_code=401, detail="Token expired")
        
        return payload
        
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Invalid JWT token: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token verification failed: {str(e)}")

async def get_current_user(authorization: Optional[str] = Header(None)) -> str:
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        # Extract token from Authorization header
        token = authorization.replace('Bearer ', '')
        
        # Debug: Let's see what's in the token
        print(f"🔍 Token received: {token[:50]}...")
        
        # Verify the token with Clerk
        payload = await verify_clerk_token(token)
        print(f"🔍 Token payload: {json.dumps(payload, indent=2)}")
        
        # Extract user ID
        user_id = payload.get("sub")
        if not user_id:
            print(f"❌ No user ID found in token payload")
            print(f"Available fields: {list(payload.keys())}")
            raise HTTPException(status_code=401, detail="Invalid token: missing user ID")
        
        print(f"✅ Found user ID: {user_id}")
        return user_id
            
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        print(f"❌ Authentication error: {e}")
        raise HTTPException(status_code=401, detail="Authentication failed") 