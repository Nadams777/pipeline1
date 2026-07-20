#!/usr/bin/env python3
"""Parse Snyk output and extract vulnerabilities"""
import json
import os
import re
from pathlib import Path

def parse_snyk_sarif():
    """Parse Snyk SARIF output if available"""
    sarif_file = 'snyk-results.sarif'
    vulnerabilities = []
    
    if os.path.exists(sarif_file):
        try:
            with open(sarif_file, 'r') as f:
                sarif_data = json.load(f)
            
            for run in sarif_data.get('runs', []):
                for result in run.get('results', []):
                    vuln = {
                        'id': result.get('ruleId', 'UNKNOWN'),
                        'title': result.get('message', {}).get('text', 'Unknown vulnerability'),
                        'severity': result.get('level', 'note').upper(),
                        'file': result.get('locations', [{}])[0].get('physicalLocation', {}).get('artifactLocation', {}).get('uri', 'unknown'),
                        'line': result.get('locations', [{}])[0].get('physicalLocation', {}).get('region', {}).get('startLine', 0),
                    }
                    vulnerabilities.append(vuln)
        except Exception as e:
            print(f"Error parsing SARIF: {e}")
    
    return vulnerabilities

def get_code_snippet(file_path, line_number):
    """Extract code snippet from file"""
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                lines = f.readlines()
            
            if 0 < line_number <= len(lines):
                return lines[line_number - 1].strip()
    except:
        pass
    
    return ""

def get_demo_vulnerabilities():
    """Return demo vulnerabilities from actual files in repo"""
    return [
        {
            'id': 'SNYK-PYTHON-001',
            'severity': 'HIGH',
            'title': 'Hardcoded Secret Detected',
            'description': 'API tokens and secrets found in source code',
            'file': 'backend/config/settings.py',
            'line': 9,
            'code_snippet': 'SNYK_API_TOKEN = "snyk_1234567890abcdef1234567890abcdef"',
            'remediation': 'Move secrets to environment variables or use a secrets manager like GitHub Secrets, AWS Secrets Manager, or HashiCorp Vault',
            'cwe': 'CWE-798: Use of Hard-coded Credentials'
        },
        {
            'id': 'SNYK-PYTHON-002',
            'severity': 'HIGH',
            'title': 'SQL Injection Risk',
            'description': 'SQL query built via string concatenation without parameterization',
            'file': 'backend/db/queries.py',
            'line': 10,
            'code_snippet': 'query = "SELECT * FROM users WHERE id=" + str(user_id)',
            'remediation': 'Use parameterized queries or an ORM like SQLAlchemy to prevent SQL injection attacks',
            'cwe': 'CWE-89: Improper Neutralization of Special Elements used in an SQL Command'
        },
        {
            'id': 'SNYK-PYTHON-003',
            'severity': 'HIGH',
            'title': 'Insecure Deserialization',
            'description': 'Unsafe pickle usage can lead to arbitrary code execution',
            'file': 'backend/utils/cache.py',
            'line': 8,
            'code_snippet': 'data = pickle.loads(cached_data)',
            'remediation': 'Use JSON or MessagePack instead of pickle for serialization. If you must use pickle, validate the data source',
            'cwe': 'CWE-502: Deserialization of Untrusted Data'
        },
        {
            'id': 'SNYK-PYTHON-004',
            'severity': 'MEDIUM',
            'title': 'Hardcoded AWS Credentials',
            'description': 'AWS secret key exposed in configuration',
            'file': 'backend/config/settings.py',
            'line': 11,
            'code_snippet': 'AWS_SECRET_KEY = "AKIA1234567890ABCDEF"',
            'remediation': 'Use AWS IAM roles and temporary credentials instead of hardcoded keys',
            'cwe': 'CWE-798: Use of Hard-coded Credentials'
        },
        {
            'id': 'SNYK-PYTHON-005',
            'severity': 'MEDIUM',
            'title': 'SQL Injection in Search Query',
            'description': 'F-string SQL query without parameterization',
            'file': 'backend/db/queries.py',
            'line': 18,
            'code_snippet': 'query = f"SELECT * FROM users WHERE email LIKE \"\"\"\"'{search_term}'\"\"\"\""',
            'remediation': 'Use parameterized queries with placeholders instead of string interpolation',
            'cwe': 'CWE-89: Improper Neutralization of Special Elements used in an SQL Command'
        },
        {
            'id': 'SNYK-PYTHON-006',
            'severity': 'MEDIUM',
            'title': 'Insecure Session Secret',
            'description': 'Session secret is hardcoded and weak',
            'file': 'backend/config/settings.py',
            'line': 15,
            'code_snippet': 'SESSION_SECRET = "super_secret_key_123456789"',
            'remediation': 'Generate a strong random secret and store it in environment variables',
            'cwe': 'CWE-798: Use of Hard-coded Credentials'
        }
    ]

if __name__ == '__main__':
    # Try to parse real Snyk results, fall back to demo
    vulns = parse_snyk_sarif()
    if not vulns:
        vulns = get_demo_vulnerabilities()
    
    # Enrich with code snippets
    for vuln in vulns:
        if not vuln.get('code_snippet'):
            vuln['code_snippet'] = get_code_snippet(vuln['file'], vuln['line'])
    
    # Output as JSON
    print(json.dumps(vulns, indent=2))
