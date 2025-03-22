#!/bin/bash

# Export other environment variables
export SECRET_KEY="your-secret-key"
export DATABASE_URL="sqlite:///./test.db"

export GOOGLE_CLIENT_ID="goog-client-id"
export GOOGLE_CLIENT_SECRET="goog-client-secret"
export GOOGLE_REDIRECT_URI="http://localhost:8000/api/v1/auth/google/callback"

# Export Google credentials from file
export GOOGLE_CREDENTIALS=$(cat secret.json)