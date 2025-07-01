# Google Sheets API Generator

Transform your Google Sheets into RESTful JSON APIs with full CRUD operations, similar to [SheetDB.io](https://sheetdb.io/).

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- PostgreSQL
- Google Sheets API credentials

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd sheetsapi
   ```

2. **Backend Setup**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   ```

4. **Environment Variables**
   ```bash
   # Backend (.env)
   DATABASE_URL=postgresql://user:password@localhost/sheetsapi
   JWT_SECRET_KEY=your-secret-key
   GOOGLE_CREDENTIALS={"type": "service_account", ...}
   
   # Frontend (.env.local)
   NEXT_PUBLIC_API_URL=http://localhost:8000
   NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=your-clerk-key
   ```

5. **Run the application**
   ```bash
   # Backend
   cd backend && uvicorn main:app --reload
   
   # Frontend
   cd frontend && npm run dev
   ```

## 📖 Project Status

**Current Phase**: Phase 1 - Core API Generation  
**Progress**: 40% Complete

### ✅ Completed Features
- Basic FastAPI backend with Google Sheets integration
- Next.js frontend with Clerk authentication
- Database models for API endpoints
- Basic sheet reading functionality
- User authentication and dashboard

### 🔄 In Progress
- Dynamic API endpoints (core feature)
- CRUD operations (Create, Update, Delete)
- Google Sheets write permissions

### 🔄 Upcoming Features
- Query parameters and filtering
- Advanced search functionality
- Real-time data preview
- API testing interface
- Performance optimization

## 📖 Documentation

- **[Product Requirements Document (PRD)](PRD.md)** - Complete project roadmap and specifications
- **[API Reference](PRD.md#api-reference-target-implementation)** - Target API endpoints and usage
- **[Implementation Plan](PRD.md#detailed-implementation-plan)** - Detailed development roadmap

## 📖 Architecture

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - Database ORM
- **Google Sheets API** - Sheet data access
- **Clerk** - Authentication

### Frontend
- **Next.js** - React framework
- **TypeScript** - Type safety
- **Clerk** - Authentication UI
- **CSS-in-JS** - Styling

## 📄 Testing

```bash
# Backend tests
cd backend && python -m pytest

# Frontend tests
cd frontend && npm test
```

## 📊 API Examples

### Create an API
```bash
POST /api/v1/sheets
{
  "name": "My Users API",
  "sheet_url": "https://docs.google.com/spreadsheets/d/...",
  "sheet_range": "A1:Z1000"
}
```

### Use the Generated API
```bash
# Get all data
GET /api/v1/data/{endpoint_id}

# Get with pagination
GET /api/v1/data/{endpoint_id}?limit=10&offset=20

# Add new row
POST /api/v1/data/{endpoint_id}
{
  "name": "John Doe",
  "age": 30
}
```

## 🤝 Contributing

1. Check the [PRD](PRD.md) for current development priorities
2. Follow the implementation roadmap
3. Write tests for new features
4. Submit pull requests with detailed descriptions

## 📄 License

MIT License - see LICENSE file for details

## 🔗 References

- [SheetDB.io](https://sheetdb.io/) - Inspiration and feature reference
- [SheetDB Documentation](https://docs.sheetdb.io/) - API design reference
- [Google Sheets API](https://developers.google.com/sheets/api) - Official documentation
