"""
Entry point for the AI Presentation Builder service.

## Traceability
- Feature: F000 (Application Bootstrap)
"""

import uvicorn

if __name__ == "__main__":
    uvicorn.run("core.loader:app", host="0.0.0.0", port=8000, reload=True)
