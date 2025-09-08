from fastapi import FastAPI
import uvicorn
import yaml
import os
from database.database import init_database
from endpoints.echo import router as echo_router
from endpoints.delete import router as delete_router
from endpoints.computation import router as computation_router

# Load configuration from config.yaml
def load_config():
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.yaml')
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

config = load_config()

# Initialize database
init_database()

# Create FastAPI instance
app = FastAPI(
    title=config['app']['title'],
    description=config['app']['description'],
    version=config['app']['version']
)

# Include routers
app.include_router(echo_router)
app.include_router(delete_router)
app.include_router(computation_router)

# Run the server
if __name__ == "__main__":
    # When running directly, reload should be False to avoid the warning
    # Use the uvicorn command line for reload functionality
    uvicorn.run(
        app, 
        host=config['server']['host'], 
        port=config['server']['port'],
        reload=False
    )