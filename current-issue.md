Current State: Incomplete Authentication

How it SHOULD work:
Frontend: User logs in with Clerk → gets JWT token
Frontend: Sends requests with Authorization: Bearer <token> header
Backend: get_current_user() dependency extracts user_id from JWT token
Backend: Uses that user_id to filter data per user

How it's CURRENTLY broken:
✅ Database: Has user_id column in APIEndpoint table
✅ Models: APIEndpoint model includes user_id field
✅ Dependencies: get_current_user() function exists in deps.py
❌ Missing: The endpoints don't actually use the get_current_user() dependency
❌ Missing: JWT verification is incomplete in deps.py
