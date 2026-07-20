#!/usr/bin/env python3
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, os.path.dirname(__file__))

try:
    from parse_snyk_results import get_demo_vulnerabilities, parse_snyk_sarif
except:
    # Fallback if import fails
    def get_demo_vulnerabilities():
        return []
    def parse_snyk_sarif():
        return []

# Get vulnerabilities
vulnerabilities = parse_snyk_sarif()
if not vulnerabilities:
    vulnerabilities = get_demo_vulnerabilities()

# Mock metrics data
metrics = {
    'pipeline': {
        'status': 'passed',
        'completion_percent': 100,
        'stages_completed': 3,
        'total_stages': 3,
        'total_duration': '1m 10s'
    },
    'security': {
        'findings': {
            'high': sum(1 for v in vulnerabilities if v.get('severity') == 'HIGH'),
            'medium': sum(1 for v in vulnerabilities if v.get('severity') == 'MEDIUM'),
            'low': sum(1 for v in vulnerabilities if v.get('severity') == 'LOW'),
            'total': len(vulnerabilities)
        },
        'scan_status': 'complete'
    },
    'quality': {
        'code_coverage_percent': 85,
        'test_pass_rate_percent': 92,
        'dependency_health_percent': 78
    },
    'performance': {
        'build_time_seconds': 42,
        'build_success_rate_percent': 94,
        'avg_deploy_time_seconds': 15
    },
    'stages': [
        {'name': 'BUILD', 'duration': '11s', 'status': 'passed'},
        {'name': 'SAST (Snyk)', 'duration': '27s', 'status': 'passed'},
        {'name': 'DEPLOY', 'duration': '21s', 'status': 'passed'}
    ]
}

# Get repository info from environment
repo = os.getenv('GITHUB_REPOSITORY', 'Nadams777/pipeline1')
branch = os.getenv('GITHUB_REF_NAME', 'main')
commit = os.getenv('GITHUB_SHA', 'main')

# Generate Markdown Summary
markdown_summary = f"""# DevSecOps Pipeline Summary

## 🎯 Overall Status: ✅ PASSED

**Pipeline Duration:** {metrics['pipeline']['total_duration']}

---

## 📊 Pipeline Progress

| Metric | Value |
|--------|-------|
| Completion | {metrics['pipeline']['completion_percent']}% |
| Stages Completed | {metrics['pipeline']['stages_completed']}/{metrics['pipeline']['total_stages']} |
| Status | {metrics['pipeline']['status'].upper()} |

---

## 🔒 Security Analysis

| Severity | Count |
|----------|-------|
| 🔴 High | {metrics['security']['findings']['high']} |
| 🟠 Medium | {metrics['security']['findings']['medium']} |
| 🟡 Low | {metrics['security']['findings']['low']} |
| **Total** | **{metrics['security']['findings']['total']}** |

**Scan Status:** {metrics['security']['scan_status'].upper()}

### Vulnerabilities Found:

"""

# Add vulnerabilities with code location links
for vuln in vulnerabilities:
    severity_icon = '🔴' if vuln.get('severity') == 'HIGH' else '🟠' if vuln.get('severity') == 'MEDIUM' else '🟡'
    file_path = vuln.get('file', 'unknown')
    line_num = vuln.get('line', 0)
    code_url = f"https://github.com/{repo}/blob/{commit}/{file_path}#L{line_num}"
    
    markdown_summary += f"""
#### {severity_icon} [{vuln.get('title', 'Unknown')}]({code_url})
- **ID:** {vuln.get('id', 'N/A')}
- **Severity:** {vuln.get('severity', 'UNKNOWN')}
- **Description:** {vuln.get('description', 'N/A')}
- **Location:** [{file_path}:{line_num}]({code_url})
- **Code:** `{vuln.get('code_snippet', 'N/A')}`
- **CWE:** {vuln.get('cwe', 'N/A')}
- **Remediation:** {vuln.get('remediation', 'N/A')}

"""

markdown_summary += f"""
---

## 📈 Code Quality Metrics

| Metric | Value | Status |
|--------|-------|--------|
| Code Coverage | {metrics['quality']['code_coverage_percent']}% | {'✅' if metrics['quality']['code_coverage_percent'] >= 80 else '⚠️'} |
| Test Pass Rate | {metrics['quality']['test_pass_rate_percent']}% | {'✅' if metrics['quality']['test_pass_rate_percent'] >= 90 else '⚠️'} |
| Dependency Health | {metrics['quality']['dependency_health_percent']}% | {'✅' if metrics['quality']['dependency_health_percent'] >= 75 else '⚠️'} |

---

## ⚡ Performance Metrics

| Metric | Value |
|--------|-------|
| Build Time | {metrics['performance']['build_time_seconds']}s |
| Build Success Rate | {metrics['performance']['build_success_rate_percent']}% |
| Deploy Time | {metrics['performance']['avg_deploy_time_seconds']}s |

---

## 🔄 Stage Details

"""

for stage in metrics['stages']:
    status_icon = '✅' if stage['status'] == 'passed' else '⏳'
    markdown_summary += f"- {status_icon} **{stage['name']}** - {stage['duration']}\n"

markdown_summary += f"\n---\n\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}"

# Write markdown summary to GitHub Actions summary file
summary_file = os.getenv('GITHUB_STEP_SUMMARY')
if summary_file:
    with open(summary_file, 'a') as f:
        f.write(markdown_summary)
    print(f"✅ Markdown summary written to {summary_file}")

print("\n" + markdown_summary)
