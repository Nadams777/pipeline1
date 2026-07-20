# DevSecOps Pipeline Dashboard

A modern, interactive CI/CD pipeline dashboard with real-time visualization of build, SAST scanning, and deployment stages.

## Features

- **Interactive Dashboard**: Real-time visualization of pipeline stages with animated logs
- **REST API**: Backend API to fetch pipeline status, logs, and security findings
- **Docker Deployment**: Multi-container setup with Nginx frontend and Flask backend
- **SAST Integration**: Snyk security scanning integrated into the pipeline
- **GitHub Actions**: Automated CI/CD workflow for building and deploying

## Architecture

```
┌────────────────────────────────────────────┐
│     Nginx Frontend (port 80)                │
│  Serves index.html Dashboard                │
└────────────────────┬───────────────────────┘
                     │
                     │ /api/* requests
                     ▼
┌────────────────────────────────────────────┐
│  Flask API Backend (port 5000)              │
│ Handles pipeline state & logs               │
└────────────────────────────────────────────┘
```

## Quick Start

### Using Docker Compose (Recommended)

```bash
# Build and start all services
docker-compose up --build

# Access the dashboard
open http://localhost:80
```

### Local Development

**Backend:**
```bash
cd backend
pip install -r requirements.txt
flask run  # Runs on port 5000
```

**Frontend:**
In another terminal:
```bash
python -m http.server 8000
# Update index.html to point to http://localhost:5000 for API calls
```

## API Endpoints

### Health Check
```
GET /api/health
```
Response: `{"status": "ok", "timestamp": "..."}`

### Get Pipeline Stages
```
GET /api/stages
```
Response: Array of stage definitions with names and descriptions

### Get Pipeline Status
```
GET /api/pipeline/status
```
Response: Current pipeline state (running, stage index, phase per stage)

### Get Logs for a Stage
```
GET /api/pipeline/logs?stage=0
```
Response: Logs for the specified stage (0=BUILD, 1=SAST, 2=DEPLOY)

### Get Security Findings
```
GET /api/pipeline/findings
```
Response: High, medium, and low severity findings count

### Trigger Pipeline Run
```
POST /api/pipeline/run
```
Response: `{"status": "started", "timestamp": "..."}`
**Note:** This is a mock endpoint that simulates a pipeline run. It does not trigger actual GitHub Actions.

### Reset Pipeline State
```
POST /api/pipeline/reset
```
Response: `{"status": "reset", "timestamp": "..."}`

## Project Structure

```
.
├── index.html                 # Interactive dashboard UI
├── nginx.conf                 # Nginx configuration
├── docker-compose.yml         # Docker Compose configuration
├── Dockerfile                 # Original Dockerfile (kept for compatibility)
├── Dockerfile.frontend        # Frontend Nginx Dockerfile
├── backend/
│   ├── app.py                # Flask application
│   ├── requirements.txt       # Python dependencies
│   ├── Dockerfile            # Backend Dockerfile
│   └── .dockerignore         # Docker ignore rules
├── .github/workflows/
│   └── devsecops-pipeline.yml # GitHub Actions workflow
└── README.md                 # This file
```

## Development

### Adding New API Endpoints

1. Add a route to `backend/app.py`:
```python
@app.route('/api/your-endpoint', methods=['GET', 'POST'])
def your_endpoint():
    return jsonify({'data': 'response'})
```

2. Update the frontend to call it:
```javascript
fetch('/api/your-endpoint')
  .then(r => r.json())
  .then(data => console.log(data))
```

### Running Tests

```bash
cd backend
pip install pytest pytest-flask
pytest
```

## Deployment

### GitHub Container Registry (GHCR)

The GitHub Actions workflow automatically builds and pushes Docker images:

```bash
# Build locally
docker build -t ghcr.io/nadams777/pipeline1:latest .

# Push to GHCR
docker push ghcr.io/nadams777/pipeline1:latest
```

### Environment Variables

- `SNYK_TOKEN`: Snyk API token for security scanning (required for SAST stage)
- `FLASK_ENV`: Set to `production` in production deployments

## Next Steps

- [ ] Connect to real GitHub Actions runs
- [ ] Integrate Snyk API for live vulnerability data
- [ ] Add database for pipeline history
- [ ] Implement authentication/authorization
- [ ] Add more detailed logging and metrics
- [ ] Create test suite

## License

MIT
