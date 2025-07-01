# Product Requirements Document (PRD)
## Google Sheets API Generator

**Version**: 1.0  
**Last Updated**: January 2025  
**Status**: In Development  
**Reference**: [SheetDB.io](https://sheetdb.io/) - [Documentation](https://docs.sheetdb.io/)

---

## Executive Summary

A web application that transforms Google Sheets into RESTful JSON APIs, similar to SheetDB.io. Users can create, manage, and consume APIs from their Google Sheets with full CRUD operations, authentication, and real-time synchronization.

### Product Vision
Enable non-technical users to create production-ready APIs from Google Sheets without coding, while providing developers with powerful tools for data management and integration.

### Current Status: **Phase 1 - Core Development**
- ✅ Basic FastAPI backend with Google Sheets integration
- ✅ Next.js frontend with Clerk authentication
- ✅ Database models for API endpoints
- ✅ Basic sheet reading functionality
- ❌ **MISSING**: Dynamic API endpoints (core feature)
- ❌ **MISSING**: CRUD operations (Create, Update, Delete)
- ❌ **MISSING**: Query parameters and filtering

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

### **Phase 1: Core API Generation** (Priority: HIGH) - **CURRENT PHASE**
**Goal**: Create functional dynamic endpoints that users can actually call

#### 1.1 Dynamic Route Handler ✅ **NEXT TASK**
- [ ] Create dynamic endpoint router (`/api/v1/data/{endpoint_id}`)
- [ ] Implement GET requests with basic JSON response
- [ ] Add error handling for invalid endpoints

#### 1.2 Google Sheets Write Permissions
- [ ] Extend Google Sheets service to support write operations
- [ ] Update service account permissions
- [ ] Implement sheet data modification methods

#### 1.3 Basic CRUD Operations
- [ ] **GET**: Read all data with basic filtering
- [ ] **POST**: Create new rows
- [ ] **PUT**: Update existing rows
- [ ] **DELETE**: Remove rows

### **Phase 2: Advanced Query Features** (Priority: HIGH)
**Goal**: Match SheetDB.io's query capabilities

#### 2.1 Query Parameters
- [ ] `limit` and `offset` for pagination
- [ ] `sort_by` and `sort_order` for sorting
- [ ] `search` for text search
- [ ] `filter` for conditional filtering

#### 2.2 Search & Filtering
- [ ] Column-based filtering
- [ ] Multiple condition support
- [ ] Text search across columns
- [ ] Date range filtering

### **Phase 3: User Experience** (Priority: MEDIUM)
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

### **Sprint 1: Dynamic API Endpoints** (Week 1-2) - **CURRENT SPRINT**
**Deliverable**: Users can create APIs and actually call them

#### Tasks:
1. **Create Dynamic Router** ✅ **START HERE**
   ```python
   # New file: backend/app/api/endpoints/dynamic.py
   @router.get("/data/{endpoint_id}")
   async def get_dynamic_data(endpoint_id: str, ...)
   ```

2. **Extend Google Sheets Service**
   ```python
   # Update: backend/app/services/google_sheets.py
   async def write_sheet_data(self, spreadsheet_id: str, data: dict)
   async def update_sheet_row(self, spreadsheet_id: str, row_id: str, data: dict)
   async def delete_sheet_row(self, spreadsheet_id: str, row_id: str)
   ```

3. **Add CRUD Endpoints**
   ```python
   # New endpoints in dynamic.py
   @router.post("/data/{endpoint_id}")
   @router.put("/data/{endpoint_id}/{row_id}")
   @router.delete("/data/{endpoint_id}/{row_id}")
   ```

#### Acceptance Criteria:
- [ ] Users can create an API and get a working endpoint
- [ ] GET requests return JSON data from Google Sheets
- [ ] POST requests add new rows to sheets
- [ ] Basic error handling for invalid requests

### **Sprint 2: Query Parameters** (Week 3-4)
**Deliverable**: Advanced filtering and pagination

#### Tasks:
1. **Implement Query Parameters**
   ```python
   # Parameters to support:
   limit: int = 100
   offset: int = 0
   sort_by: str = None
   sort_order: str = "asc"
   search: str = None
   filter: str = None
   ```

2. **Add Search Functionality**
   ```python
   # Search across all columns
   async def search_sheet_data(self, spreadsheet_id: str, query: str)
   ```

3. **Implement Filtering**
   ```python
   # Support filters like: "age>18,name=John"
   async def filter_sheet_data(self, spreadsheet_id: str, filters: str)
   ```

#### Acceptance Criteria:
- [ ] `?limit=10&offset=20` works for pagination
- [ ] `?sort_by=name&sort_order=desc` sorts data
- [ ] `?search=john` finds matching rows
- [ ] `?filter=age>18` filters data

### **Sprint 3: Frontend Enhancements** (Week 5-6)
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
│ │ │ └── dynamic.py # ⚠️ NEEDS TO BE CREATED - Dynamic API endpoints
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
