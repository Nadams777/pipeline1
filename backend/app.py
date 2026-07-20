from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import json

app = Flask(__name__)
CORS(app)

# Mock data for pipeline stages and runs
PIPELINE_STATE = {
    'running': False,
    'stageIdx': -1,
    'stagePhase': ['pending', 'pending', 'pending'],  # pending | running | pass
    'logsByStage': [[], [], []],
}

STAGE_DEFS = [
    {'name': 'BUILD', 'subLabel': 'docker build', 'num': '1'},
    {'name': 'SAST', 'subLabel': 'snyk code scan', 'num': '2'},
    {'name': 'DEPLOY', 'subLabel': 'databricks', 'num': '3'},
]

BUILD_LOGS = [
    ['$ docker build -t pipeline1:a3f9c2e .', 'plain'],
    ['[+] Building 4.2s (11/11) FINISHED', 'plain'],
    [' => [internal] load build definition from Dockerfile', 'dim'],
    [' => [1/6] FROM python:3.12-slim', 'dim'],
    [' => [2/6] WORKDIR /app', 'dim'],
    [' => [3/6] COPY requirements.txt .', 'dim'],
    [' => [4/6] RUN pip install -r requirements.txt', 'dim'],
    [' => [5/6] COPY . .', 'dim'],
    [' => exporting to image', 'dim'],
    ['✓ image built: pipeline1:a3f9c2e', 'green'],
]

SAST_LOGS = [
    ['$ snyk code test --severity-threshold=medium', 'plain'],
    ['Testing /app for known issues...', 'dim'],
    ['✗ [High] Hardcoded secret detected — config/settings.py:14', 'red'],
    ['✗ [Medium] SQL built via string concat — db/queries.py:52', 'amber'],
    ['✗ [Medium] Insecure deserialization — utils/cache.py:9', 'amber'],
    ['! 3 issues found (1 high, 2 medium)', 'amber'],
    ['✓ scan complete — report uploaded to Snyk dashboard', 'green'],
]

DEPLOY_LOGS = [
    ['$ databricks bundle deploy -t staging', 'plain'],
    ['Uploading pipeline1 bundle...', 'dim'],
    ['Deploying resources...', 'dim'],
    ['✓ job "pipeline1-etl" updated', 'green'],
    ['✓ deployed to staging workspace', 'green'],
]

ALL_LOGS = [BUILD_LOGS, SAST_LOGS, DEPLOY_LOGS]

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'timestamp': datetime.now().isoformat()})

@app.route('/api/stages', methods=['GET'])
def get_stages():
    """Get pipeline stage definitions"""
    return jsonify(STAGE_DEFS)

@app.route('/api/pipeline/status', methods=['GET'])
def get_pipeline_status():
    """Get current pipeline status"""
    return jsonify({
        'running': PIPELINE_STATE['running'],
        'stageIdx': PIPELINE_STATE['stageIdx'],
        'stagePhase': PIPELINE_STATE['stagePhase'],
        'timestamp': datetime.now().isoformat(),
    })

@app.route('/api/pipeline/logs', methods=['GET'])
def get_logs():
    """Get logs for a specific stage"""
    stage_idx = request.args.get('stage', 0, type=int)
    if stage_idx < 0 or stage_idx >= len(ALL_LOGS):
        return jsonify({'error': 'Invalid stage index'}), 400
    
    logs = PIPELINE_STATE['logsByStage'][stage_idx]
    return jsonify({
        'stage': STAGE_DEFS[stage_idx]['name'],
        'logs': logs,
        'timestamp': datetime.now().isoformat(),
    })

@app.route('/api/pipeline/findings', methods=['GET'])
def get_findings():
    """Get security findings from SAST scan"""
    stage_phase = PIPELINE_STATE['stagePhase']
    all_pass = all(p == 'pass' for p in stage_phase)
    
    return jsonify({
        'high': 1 if all_pass or stage_phase[1] != 'pending' else 0,
        'medium': 2 if all_pass or stage_phase[1] != 'pending' else 0,
        'low': 0,
        'timestamp': datetime.now().isoformat(),
    })

@app.route('/api/pipeline/run', methods=['POST'])
def run_pipeline():
    """Trigger a pipeline run"""
    if PIPELINE_STATE['running']:
        return jsonify({'error': 'Pipeline already running'}), 409
    
    PIPELINE_STATE['running'] = True
    PIPELINE_STATE['stageIdx'] = 0
    PIPELINE_STATE['stagePhase'] = ['running', 'pending', 'pending']
    PIPELINE_STATE['logsByStage'] = [[], [], []]
    
    return jsonify({
        'status': 'started',
        'timestamp': datetime.now().isoformat(),
    }), 202

@app.route('/api/pipeline/reset', methods=['POST'])
def reset_pipeline():
    """Reset pipeline state"""
    global PIPELINE_STATE
    PIPELINE_STATE = {
        'running': False,
        'stageIdx': -1,
        'stagePhase': ['pending', 'pending', 'pending'],
        'logsByStage': [[], [], []],
    }
    return jsonify({'status': 'reset', 'timestamp': datetime.now().isoformat()})

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
