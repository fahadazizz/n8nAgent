# Quick Start Guide

## Entry Point: `main.py`

This is your main entry point for the n8n automation agent.

## Usage

### 1. Direct Command (Fastest)
```bash
python main.py "Create a cron job that backs up database daily"
```

### 2. Interactive Mode
```bash
python main.py --interactive
# or
python main.py
```

Then enter your requests interactively:
```
Request: Create a webhook that sends Slack messages
Skip simulation for faster execution? (y/n) [n]: y
```

### 3. With Virtual Environment
```bash
.venv/bin/python main.py "Your automation request here"
```

## Examples

```bash
# Simple webhook
python main.py "Create a webhook that posts to Slack channel #general"

# Scheduled task
python main.py "Create a daily cron job that fetches weather data and emails it"

# Data pipeline
python main.py "When a form is submitted, save to Google Sheets and notify via email"
```

## Output

When successful, you'll get:
```
✅ SUCCESS - Workflow Imported to n8n!
Workflow ID: abc123xyz
Access URL: http://localhost:5678/workflow/abc123xyz
```

Then:
1. Open the URL in your browser
2. Configure credentials (if needed)
3. Activate the workflow
4. Test it!

## Performance Tips

- Use `y` when asked to skip simulation for 3-5x faster execution
- The first run loads models, subsequent runs are faster
- Simple workflows take 30-60s, complex ones may take 2-3 minutes
