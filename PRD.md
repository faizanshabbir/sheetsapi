# Product Requirements Document (PRD)
## Google Sheets API Generator

**Version**: 1.0  
**Last Updated**: January 2025  
**Status**: In Development  
**Reference**: [SheetDB.io](https://sheetdb.io/) - [Documentation](https://docs.sheetdb.io/)

---

## 🚨 **CRITICAL ISSUE IDENTIFIED: Multi-User Support BROKEN** ❌

**Date**: January 2025  
**Status**: **BLOCKING** - Must be fixed before Phase 3

### ❌ **Current Problems**
- **No User Isolation**: All users can see and access each other's APIs
- **Hardcoded User ID**: API creation uses `"test-user-123"` for all users
- **Missing Authentication**: Endpoints don't use `get_current_user()` dependency
- **Incomplete JWT Verification**: Placeholder JWT verification in `deps.py`
- **Security Vulnerability**: Users can access each other's data

### 🔒 **Security Impact**
- **User A** creates APIs → **User B** can see and access them
- **No privacy** between users
- **Broken multi-tenancy**
- **Production deployment unsafe**

---

## 🎉 **MAJOR MILESTONE ACHIEVED: Phase 1 & 2 COMPLETED** ✅

**Date**: January 2025  
**Status**: Core functionality fully implemented and tested

### ✅ **What We've Built**
- **Full CRUD Operations**: Create, Read, Update, Delete with both index-based and field-based approaches
- **Advanced Insertion Options**: Insert at beginning, end, specific position, or after field matches
- **Query Parameters**: Pagination, sorting, debugging with case-insensitive column matching
- **Modular Architecture**: Clean separation of concerns with mixins for different operation types
- **RESTful API Design**: Following best practices with proper HTTP methods and status codes
- **Google Sheets Integration**: Full read/write access with proper error handling

### 🧪 **Tested & Working Features**
- ✅ Dynamic API endpoints (`/api/v1/data/{endpoint_id}`)
- ✅ GET with pagination, sorting, and debug info
- ✅ POST with multiple insertion strategies
- ✅ PUT for both index-based and field-based updates
- ✅ DELETE for both index-based and field-based operations
- ✅ Field-based operations with query parameters
- ✅ Error handling and permission validation

### 📊 **Current Status**
- **Backend**: 100% functional with all core features
- **Frontend**: Basic UI for API creation and management
- **Database**: Proper models and relationships
- **Testing**: All CRUD operations tested and working

---

## Executive Summary

A web application that transforms Google Sheets into RESTful JSON APIs, similar to SheetDB.io. Users can create, manage, and consume APIs from their Google Sheets with full CRUD operations, authentication, and real-time synchronization.

### Product Vision
Enable non-technical users to create production-ready APIs from Google Sheets without coding, while providing developers with powerful tools for data management and integration.

### Current Status: **Phase 1 - Core Development** ✅ **COMPLETED**
- ✅ Basic FastAPI backend with Google Sheets integration
- ✅ Next.js frontend with Clerk authentication
- ✅ Database models for API endpoints
- ✅ Basic sheet reading functionality
- ✅ **COMPLETED**: Dynamic API endpoints (core feature)
- ✅ **COMPLETED**: Full CRUD operations (Create, Read, Update, Delete)
- ✅ **COMPLETED**: Query parameters and filtering
- ✅ **COMPLETED**: Both index-based and field-based operations
- ✅ **COMPLETED**: Advanced insertion options (beginning, end, specific position, field-based)

---

## Core Features & Functionality

### 1. **API Management** 
- **Create API**: Convert Google Sheet to JSON API endpoint
- **List APIs**: View all user's created APIs  
- **Delete API**: Remove API endpoints
- **API Analytics**: Usage statistics and monitoring

### 2. **CRUD Operations** 
- **READ**: GET requests with filtering, sorting, pagination
- **CREATE**: POST requests to add new rows
- **UPDATE**: PUT/PATCH requests to modify existing rows  
- **DELETE**: DELETE requests to remove rows
- **SEARCH**: Advanced search with multiple parameters

### 3. **Authentication & Security**
- Google OAuth integration
- API key management
- Rate limiting
- CORS configuration
- Request validation

### 4. **Advanced Features**
- Multiple sheet support
- Real-time webhooks
- Data validation
- Export functionality
- Caching layer

---

## Technical Architecture

### Backend Stack
- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL with SQLAlchemy
- **Authentication**: Clerk
- **Google Sheets**: Google Sheets API v4
- **Caching**: Redis (future)

### Frontend Stack
- **Framework**: Next.js with TypeScript
- **Authentication**: Clerk
- **Styling**: CSS-in-JS
- **State Management**: React hooks

---

## Implementation Roadmap

### **Phase 1: Core API Generation** (Priority: HIGH) - **COMPLETED** ✅
**Goal**: Create functional dynamic endpoints that users can actually call

#### 1.1 Dynamic Route Handler ✅ **COMPLETED**
- [x] Create dynamic endpoint router (`/api/v1/data/{endpoint_id}`)
- [x] Implement GET requests with basic JSON response
- [x] Add error handling for invalid endpoints
- [x] Add pagination support (`limit` and `offset`)
- [x] Add sorting support (`sort_by` and `sort_order`)
- [x] Add case-insensitive column matching
- [x] Add debug information endpoint

#### 1.2 Google Sheets Write Permissions ✅ **COMPLETED**
- [x] Extend Google Sheets service to support write operations
- [x] Update service account permissions (full read/write scope)
- [x] Implement sheet data modification methods
- [x] Add debug endpoint to check permissions

#### 1.3 Basic CRUD Operations ✅ **COMPLETED**
- [x] **GET**: Read all data with basic filtering, pagination, and sorting
- [x] **POST**: Create new rows with multiple insertion options
- [x] **PUT**: Update existing rows (both index-based and field-based)
- [x] **DELETE**: Remove rows (both index-based and field-based)

#### 1.4 Advanced Insertion Options ✅ **COMPLETED**
- [x] Insert at end (default behavior)
- [x] Insert at beginning (after headers)
- [x] Insert at specific position (row index)
- [x] Field-based insertion (after matching rows)

### **Phase 2: Advanced Query Features** (Priority: HIGH) - **COMPLETED** ✅
**Goal**: Match SheetDB.io's query capabilities

#### 2.1 Query Parameters ✅ **COMPLETED**
- [x] `limit` and `offset` for pagination
- [x] `sort_by` and `sort_order` for sorting
- [x] `debug` for debugging information
- [x] Field-based filtering via query parameters

#### 2.2 Search & Filtering ✅ **COMPLETED**
- [x] Column-based filtering (field-based operations)
- [x] Multiple condition support (field-based criteria)
- [x] Case-insensitive column matching
- [x] Field-based CRUD operations (update, delete, insert)

#### 2.3 Modular Architecture ✅ **COMPLETED**
- [x] Index-based operations mixin
- [x] Field-based operations mixin
- [x] Separate endpoints for different approaches
- [x] RESTful API design following best practices

### **Phase 2.5: Multi-User Authentication & Security** (Priority: **CRITICAL**) - **BLOCKING**
**Goal**: Implement proper user isolation and security before production

#### 2.5.1 Complete JWT Authentication ✅ **PARTIALLY IMPLEMENTED**
- [x] Database model includes `user_id` field
- [x] `get_current_user()` dependency function exists
- [ ] **FIX**: Complete JWT verification in `deps.py`
  - Current implementation has placeholder JWT verification
  - Need to implement proper Clerk JWT verification
  - Must extract and validate user ID from token
  - Handle authentication errors properly

#### 2.5.2 Implement User Isolation ✅ **DATABASE READY**
- [x] Database schema supports user isolation (`user_id` column)
- [ ] **FIX**: Add `get_current_user()` dependency to all endpoints
  - Current implementation returns all users' data
  - Need to filter all queries by current user ID
  - Apply user filtering to GET /sheets endpoint
  - Apply user filtering to all other endpoints

#### 2.5.3 Fix API Creation Endpoint ✅ **PARTIALLY IMPLEMENTED**
- [x] Database model supports user_id
- [ ] **FIX**: Use actual user ID instead of hardcoded value
  - Current implementation uses hardcoded "test-user-123" for all users
  - Need to extract actual user ID from authentication token
  - Apply user ID to all new API endpoint creations
  - Ensure proper user association for all created endpoints

#### 2.5.4 Secure Dynamic Endpoints ✅ **PARTIALLY IMPLEMENTED**
- [ ] **FIX**: Add user validation to dynamic endpoints
  - Current implementation has no user validation
  - Need to verify endpoint ownership before allowing access
  - Add user authentication to all dynamic endpoints
  - Return 404 if endpoint doesn't belong to current user

#### 2.5.5 Frontend Authentication Integration ✅ **PARTIALLY IMPLEMENTED**
- [x] Frontend uses Clerk authentication
- [x] Frontend sends Authorization headers
- [ ] **FIX**: Ensure all API calls include proper Authorization headers
  - Current implementation partially includes auth headers
  - Need to ensure ALL API calls include Authorization headers
  - Verify token is properly sent with every request
  - Handle authentication errors gracefully

#### 2.5.6 Testing & Validation ✅ **NEEDS IMPLEMENTATION**
- [ ] **CREATE**: Multi-user test scenarios
  - Test that User A cannot see User B's APIs
  - Test that users can only access their own endpoints
  - Test unauthenticated requests return 401
  - Test invalid tokens return 401
  - Test cross-user access attempts return 404
- [ ] **CREATE**: Authentication test suite
- [ ] **CREATE**: User isolation test suite
- [ ] **CREATE**: Security penetration testing

#### 2.5.7 Error Handling & Security ✅ **NEEDS IMPLEMENTATION**
- [ ] **CREATE**: Proper error messages for authentication failures
- [ ] **CREATE**: Rate limiting per user
- [ ] **CREATE**: Request logging for security monitoring
- [ ] **CREATE**: Audit trail for API access

#### Acceptance Criteria:
- [ ] Users can only see and access their own APIs
- [ ] Unauthenticated requests return 401
- [ ] Invalid tokens return 401
- [ ] Users cannot access other users' endpoints
- [ ] All API creation uses actual user ID
- [ ] Frontend properly sends authentication headers
- [ ] Comprehensive test coverage for multi-user scenarios

### **Phase 3: User Experience** (Priority: MEDIUM) - **BLOCKED UNTIL 2.5 COMPLETE**
**Goal**: Improve frontend and user management

#### 3.1 Enhanced Dashboard
- [ ] API usage statistics
- [ ] Real-time data preview
- [ ] Quick test interface
- [ ] API documentation generation

#### 3.2 API Management
- [ ] Edit existing APIs
- [ ] Duplicate APIs
- [ ] API versioning
- [ ] Bulk operations

### **Phase 4: Production Features** (Priority: MEDIUM)
**Goal**: Enterprise-ready features

#### 4.1 Performance & Reliability
- [ ] Redis caching layer
- [ ] Rate limiting
- [ ] Request logging
- [ ] Error monitoring

#### 4.2 Advanced Features
- [ ] Webhook support
- [ ] Multiple sheet tabs
- [ ] Data validation rules
- [ ] Export to different formats

### **Phase 5: Developer Experience** (Priority: LOW)
**Goal**: Developer-friendly features

#### 5.1 API Documentation
- [ ] Auto-generated OpenAPI docs
- [ ] Code examples in multiple languages
- [ ] Interactive API explorer

#### 5.2 SDKs & Libraries
- [ ] JavaScript/TypeScript SDK
- [ ] Python SDK
- [ ] PHP SDK
- [ ] Ruby SDK

---

## Detailed Implementation Plan

### **Sprint 1: Dynamic API Endpoints** (Week 1-2) - **COMPLETED** ✅
**Deliverable**: Users can create APIs and actually call them

#### Tasks:
1. **Create Dynamic Router** ✅ **COMPLETED**
   ```python
   # Created: backend/app/api/endpoints/dynamic.py
   @router.get("/data/{endpoint_id}")
   async def get_dynamic_data(endpoint_id: str, ...)
   ```

2. **Extend Google Sheets Service** ✅ **COMPLETED**
   ```python
   # Updated: backend/app/services/google_sheets.py
   async def add_row_at_position(self, spreadsheet_id: str, range_name: str, row_data: Dict[str, Any], position: str = "end")
   async def get_raw_data(self, spreadsheet_id: str) -> List[List]
   async def _get_headers(self, spreadsheet_id: str) -> List[str]
   ```

3. **Add CRUD Endpoints** ✅ **COMPLETED**
   ```python
   # Created: backend/app/api/endpoints/dynamic.py
   @router.post("/data/{endpoint_id}")  # Index-based create
   @router.put("/data/{endpoint_id}/{row_id}")  # Index-based update
   @router.delete("/data/{endpoint_id}/{row_id}")  # Index-based delete
   
   # Created: backend/app/api/endpoints/dynamic_field.py
   @router.put("/data/{endpoint_id}/field/update")  # Field-based update
   @router.delete("/data/{endpoint_id}/field/delete")  # Field-based delete
   @router.post("/data/{endpoint_id}/field/insert")  # Field-based insert
   ```

4. **Create Modular Operations** ✅ **COMPLETED**
   ```python
   # Created: backend/app/services/operations/
   - base.py (BaseOperations)
   - index_based.py (IndexBasedOperations)
   - field_based.py (FieldBasedOperations)
   ```

#### Acceptance Criteria:
- [x] Users can create an API and get a working endpoint ✅ **COMPLETED**
- [x] GET requests return JSON data from Google Sheets ✅ **COMPLETED**
- [x] Basic error handling for invalid requests ✅ **COMPLETED**
- [x] POST requests add new rows to sheets ✅ **COMPLETED**
- [x] PUT requests update existing rows ✅ **COMPLETED**
- [x] DELETE requests remove rows ✅ **COMPLETED**
- [x] Field-based operations work with query parameters ✅ **COMPLETED**
- [x] Advanced insertion options (beg, end, position, field-based) ✅ **COMPLETED**

### **Sprint 2: Query Parameters** (Week 3-4) - **COMPLETED** ✅
**Deliverable**: Advanced filtering and pagination

#### Tasks:
1. **Implement Query Parameters** ✅ **COMPLETED**
   ```python
   # Parameters implemented:
   limit: int = 100 ✅
   offset: int = 0 ✅
   sort_by: str = None ✅
   sort_order: str = "asc" ✅
   debug: bool = False ✅
   ```

2. **Add Field-based Operations** ✅ **COMPLETED**
   ```python
   # Field-based filtering via query parameters
   # URL encoding support for field names with spaces
   # Multiple condition support
   ```

3. **Implement Advanced Sorting** ✅ **COMPLETED**
   ```python
   # Case-insensitive column matching
   # Proper handling of missing values
   # Numeric and string sorting
   ```

#### Acceptance Criteria:
- [x] `?limit=10&offset=20` works for pagination ✅ **COMPLETED**
- [x] `?sort_by=name&sort_order=desc` sorts data ✅ **COMPLETED**
- [x] `?debug=true` shows debug information ✅ **COMPLETED**
- [x] Field-based operations work with query parameters ✅ **COMPLETED**
- [x] Case-insensitive column matching ✅ **COMPLETED**

### **Sprint 2.5: Multi-User Authentication & Security** (Week 5-6) - **CRITICAL** 🔒
**Deliverable**: Secure multi-user system with proper isolation

#### Tasks:
1. **Complete JWT Authentication** 🔒 **CRITICAL**
   - Fix JWT verification in `backend/app/api/deps.py`
   - Implement proper Clerk JWT verification
   - Extract and validate user ID from token
   - Handle authentication errors properly

2. **Implement User Isolation in All Endpoints** 🔒 **CRITICAL**
   - Fix GET /sheets endpoint in `backend/app/api/endpoints/sheets.py`
   - Add user authentication dependency to all endpoints
   - Filter all queries by current user ID
   - Apply user filtering to all API management endpoints

3. **Secure Dynamic Endpoints** 🔒 **CRITICAL**
   - Add user validation to all dynamic endpoints in `backend/app/api/endpoints/dynamic.py`
   - Verify endpoint ownership before allowing access
   - Return 404 if endpoint doesn't belong to current user
   - Apply user authentication to all CRUD operations

4. **Frontend Authentication Integration** 🔒 **CRITICAL**
   - Ensure all API calls include Authorization headers in `frontend/pages/dashboard.tsx`
   - Verify token is properly sent with every request
   - Handle authentication errors gracefully
   - Update all frontend API calls to include auth headers

5. **Create Test Suite** 🔒 **CRITICAL**
   - Test multi-user isolation scenarios
   - Test cross-user access attempts
   - Test unauthenticated and invalid token requests
   - Create comprehensive authentication test suite

#### Acceptance Criteria:
- [ ] Users can only see and access their own APIs
- [ ] Unauthenticated requests return 401
- [ ] Invalid tokens return 401
- [ ] Users cannot access other users' endpoints
- [ ] All API creation uses actual user ID
- [ ] Frontend properly sends authentication headers
- [ ] Comprehensive test coverage for multi-user scenarios
- [ ] Security audit passes

### **Sprint 3: Frontend Enhancements** (Week 7-8) - **BLOCKED UNTIL 2.5 COMPLETE**
**Deliverable**: Better user experience

#### Tasks:
1. **API Testing Interface**
   ```typescript
   // New component: frontend/components/ApiTester.tsx
   // Real-time API testing with query parameters
   ```

2. **Data Preview**
   ```typescript
   // New component: frontend/components/DataPreview.tsx
   // Show live data from Google Sheets
   ```

3. **API Documentation**
   ```typescript
   // Auto-generate API docs for each endpoint
   // Show code examples
   ```

#### Acceptance Criteria:
- [ ] Users can test their APIs directly in the dashboard
- [ ] Real-time data preview shows current sheet data
- [ ] API documentation is auto-generated
- [ ] Code examples are provided

---

## API Reference (Target Implementation)

### Base URL 

### Structure
backend/
├── app/
│ ├── api/
│ │ ├── endpoints/
│ │ │ ├── sheets.py # API management endpoints
│ │ │ └── dynamic.py 
│ │ └── deps.py
│ ├── core/
│ │ └── config.py
│ ├── db/
│ │ ├── base_class.py
│ │ ├── base.py
│ │ ├── init_db.py
│ │ └── session.py
│ ├── models/
│ │ └── api_endpoint.py
│ └── services/
│ ├── google_sheets.py # ⚠️ NEEDS WRITE PERMISSIONS
│ └── sheet_template.py
├── main.py
└── requirements.txt

frontend/
├── components/
│ ├── Layout.tsx
│ ├── ApiTester.tsx # ⚠️ NEEDS TO BE CREATED
│ └── DataPreview.tsx # ⚠️ NEEDS TO BE CREATED
├── pages/
│ ├── app.tsx
│ ├── index.tsx
│ ├── dashboard.tsx
│ └── sheets/
│ ├── [id].tsx # ⚠️ NEEDS TO BE CREATED - API detail page
│ └── new.tsx
├── package.json
└── tsconfig.json
