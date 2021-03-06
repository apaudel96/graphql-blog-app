import os
import uvicorn
from app.app import app


if __name__ == "__main__":
    port = os.getenv("PORT", "8000")
    port = int(port)
    uvicorn.run(app, port=port)
    