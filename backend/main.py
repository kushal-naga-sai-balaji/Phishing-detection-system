from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import services.detector as detector
import services.ip_manager as ip_manager
import services.ml_engine as ml_engine
import os

# Initialize ML Model
ml_engine.load_model()

app = FastAPI(title="Phishing Detection System")

# Mount Static Files (Frontend)
# Robust path resolution
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(os.path.dirname(BASE_DIR), "frontend")

if os.path.exists(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class URLScanRequest(BaseModel):
    url: str

class EmailScanRequest(BaseModel):
    subject: str
    body: str
    sender: str

@app.middleware("http")
async def ip_filtering_middleware(request: Request, call_next):
    client_ip = request.client.host
    
    if request.url.path.startswith("/admin"):
        response = await call_next(request)
        return response

    if ip_manager.is_blocked(client_ip):
         return JSONResponse(status_code=403, content={"detail": "Your IP has been temporarily blocked due to suspicious activity."})
    
    response = await call_next(request)
    return response

@appindex_path = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return JSONResponse(content={"detail": "Frontend index.html not found"}, status_code=404
def read_root():
    # Return the index.html from frontend
    return FileResponse("../frontend/index.html")

@app.post("/scan/url")
def scan_url(request: URLScanRequest, client_request: Request):
    client_ip = client_request.client.host
    result = detector.detect_url(request.url)
    
    # Record activity if suspicious
    if result["status"] == "phishing":
        ip_manager.record_activity(client_ip, is_suspicious=True)
    else:
        # Just record presence or ignore
        ip_manager.record_activity(client_ip, is_suspicious=False)
        
    return result

@app.post("/scan/email")
def scan_email(request: EmailScanRequest, client_request: Request):
    client_ip = client_request.client.host
    result = detector.detect_email(request.subject, request.body, request.sender)
    
    if result["status"] == "phishing":
        ip_manager.record_activity(client_ip, is_suspicious=True)
    else:
        ip_manager.record_activity(client_ip, is_suspicious=False)
        
    return result

@app.post("/scan/file")
async def scan_file(client_request: Request, file: UploadFile = File(...)):
    client_ip = client_request.client.host
    content = await file.read()
    result = detector.detect_file(file.filename, content)
    
    if result["status"] == "malicious":
        ip_manager.record_activity(client_ip, is_suspicious=True)
    else:
        ip_manager.record_activity(client_ip, is_suspicious=False)
        
    return result

@app.get("/ip/status")
def get_ip_status(request: Request):
    client_ip = request.client.host
    history = ip_manager.get_ip_data(client_ip)
    return {"ip": client_ip, "status": "blocked" if ip_manager.is_blocked(client_ip) else "allowed", "history": history}

@app.get("/admin/ips")
def get_all_ips():
    return ip_manager.get_all_ips()

@app.post("/admin/unblock/{ip}")
def unblock_ip(ip: str):
    ip_manager.unblock_ip(ip)
    return {"message": f"IP {ip} unblocked"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
