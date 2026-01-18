# n8n Integration Setup

## Current Status
The autonomous agent successfully generates n8n workflows but requires authentication configuration to import them.

## Setup Instructions

### Option 1: Use n8n with Disabled Authentication (Development Only)
Start n8n with API authentication disabled:

```bash
N8N_API_AUTH_DISABLED=true n8n start
```

Or set environment variable permanently:
```bash
export N8N_API_AUTH_DISABLED=true
```

### Option 2: Use API Key Authentication
1. In n8n UI, go to **Settings** → **API**
2. Create an API key
3. Set the environment variable:
   ```bash
   export N8N_API_KEY="your-api-key-here"
   ```

### Option 3: Update the Code
If you have an API key, update `src/utils/n8n_api.py` or set the environment variable:

```python
n8n = N8nAPI(api_key="your-key-here")
```

## Testing the Integration

Once n8n is configured, run:

```bash
# Test API directly
python test_n8n_api.py

# Test full pipeline
python test_import.py
```

## Expected Output
```
✓ Workflow imported successfully. ID: abc123
  Access at: http://localhost:5678/workflow/abc123
```
