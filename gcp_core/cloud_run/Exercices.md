#### Exercice 1 : API FastAPI avec Documentation

**Objectif** : Déployer une API moderne avec FastAPI

```python
# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import os
from datetime import datetime

app = FastAPI(
    title="Data Processing API",
    description="API de traitement de données sur Cloud Run",
    version="1.0.0"
)

# Modèles Pydantic
class DataItem(BaseModel):
    id: Optional[int] = None
    name: str
    value: float
    category: str

class ProcessingResult(BaseModel):
    original: DataItem
    processed_at: str
    result: dict

# Base de données en mémoire (pour démo)
items_db: List[DataItem] = []
next_id = 1

@app.get("/")
async def root():
    return {
        "message": "Data Processing API",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/items/", response_model=DataItem)
async def create_item(item: DataItem):
    global next_id
    item.id = next_id
    next_id += 1
    items_db.append(item)
    return item

@app.get("/items/", response_model=List[DataItem])
async def list_items(category: Optional[str] = None):
    if category:
        return [item for item in items_db if item.category == category]
    return items_db

@app.get("/items/{item_id}", response_model=DataItem)
async def get_item(item_id: int):
    for item in items_db:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@app.post("/process/", response_model=ProcessingResult)
async def process_data(item: DataItem):
    """Simule un traitement de données"""
    result = {
        "mean": item.value * 1.5,
        "variance": item.value * 0.2,
        "category_upper": item.category.upper()
    }
    
    return ProcessingResult(
        original=item,
        processed_at=datetime.now().isoformat(),
        result=result
    )

@app.get("/stats/")
async def get_statistics():
    if not items_db:
        return {"count": 0, "categories": []}
    
    categories = {}
    total_value = 0
    
    for item in items_db:
        categories[item.category] = categories.get(item.category, 0) + 1
        total_value += item.value
    
    return {
        "count": len(items_db),
        "total_value": total_value,
        "average_value": total_value / len(items_db),
        "categories": categories
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
```

**requirements.txt pour FastAPI** :

```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
```

**Dockerfile pour FastAPI** :

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

CMD exec uvicorn main:app --host 0.0.0.0 --port $PORT --workers 1
```

**Déploiement** :

```bash
gcloud run deploy data-api \
  --source . \
  --region europe-west1 \
  --allow-unauthenticated \
  --memory 512Mi \
  --set-env-vars "ENVIRONMENT=production"

# Obtenir l'URL et tester
SERVICE_URL=$(gcloud run services describe data-api \
  --region europe-west1 \
  --format 'value(status.url)')

echo "Documentation: $SERVICE_URL/docs"
```