```python
from fastapi import FastAPI
from pwnagebox.modules import scammer, researcher, pwner, voicepwner

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to PwnageBox"}

@app.post("/scan")
def perform_scan():
    return scammer.scan_environment()

@app.post("/research")
def perform_research():
    return researcher.analyze_vulnerabilities()

@app.post("/exploit")
def perform_exploit():
    return pwner.execute_exploit()

@app.post("/social_engineering")
def perform_social_engineering():
    return voicepwner.conduct_attack()
```
