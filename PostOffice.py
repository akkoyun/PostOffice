# Library Imports
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from Functions import Log, FastApi_Functions
from Setup import Database, Models

# Define FastAPI Tags
FastAPI_Tags = [
    {
        "name": "Root",
        "description": "This endpoint is the root of the PostOffice API.",
    }
]

# Define FastAPI Object
PostOffice = FastAPI(version="02.04.00", title="PostOffice", openapi_tags=FastAPI_Tags)

# Define Middleware
PostOffice.add_middleware(FastApi_Functions.Pre_Request)

# Define Event Handlers
@PostOffice.on_event("startup")
def on_startup():

	# Create Tables
	Database.Base.metadata.create_all(bind=Database.DB_Engine)

# Main Root Get Method
@PostOffice.get("/", tags=["Root"])
def Main_Root(request: Request):

	# Set up Jinja2 Environment
	Templates_Directory = Path("Templates")
	Jinja_ENV = Environment(loader=FileSystemLoader(Templates_Directory))

	# Define the error message
	Error_Message = f"Hata: İsteğiniz geçersiz. Yardım için destek ekibimize başvurun. [{request.client.host}]"

    # Load the HTML template
	Template = Jinja_ENV.get_template("HTML_Response.html")

    # Render the template with the footer message
	Rendered_HTML = Template.render(error_message=Error_Message)

	# Log Message
	Log.Terminal_Log("WARNING", f"New Root Request.")

	# Return the HTML content
	return HTMLResponse(content=Rendered_HTML)
