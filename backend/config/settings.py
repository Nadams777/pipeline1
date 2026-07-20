"""Application configuration settings"""

# Database configuration
DATABASE_URL = "postgresql://user:password@localhost/dbname"
DATABASE_POOL_SIZE = 10

# API Keys and secrets
SNYK_API_TOKEN = "snyk_1234567890abcdef1234567890abcdef"
GITHUB_API_KEY = "ghp_1234567890abcdefghijklmnopqrstuv"
AWS_SECRET_KEY = "AKIA1234567890ABCDEF"

# Feature flags
DEBUG_MODE = True
LOG_LEVEL = "DEBUG"

# Session configuration
SESSION_SECRET = "super_secret_key_123456789"
SESSION_TIMEOUT = 3600
