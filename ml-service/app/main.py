import json,os
from pathlib import Path
from typing import Literal
from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse
from .rate_limit import SlidingWindowLimiter
from pydantic import BaseModel,Field
from joblib import load
from .routing import route
ROOT=Path(__file__).resolve().parents[1];ART=ROOT/'artifacts';MODEL=ART/'logistic_regression.joblib';VERSION='1.0.0'
app=FastAPI(title='SehatSetu ML Service',version=VERSION,description='Healthcare query classification and intelligent routing API')
app.add_middleware(CORSMiddleware,allow_origins=os.getenv('CORS_ORIGINS','http://localhost:5173').split(','),allow_credentials=True,allow_methods=['GET','POST'],allow_headers=['Content-Type','Authorization'])
limiter=SlidingWindowLimiter(limit=int(os.getenv('RATE_LIMIT_PER_MINUTE','30')))
@app.middleware('http')
async def rate_limit(request: Request, call_next):
    if request.url.path.startswith('/api/'):
        client=request.client.host if request.client else 'unknown'
        if not limiter.allow(client): return JSONResponse({'detail':'Rate limit exceeded. Please retry shortly.'},status_code=429)
    return await call_next(request)
class Query(BaseModel): text:str=Field(min_length=5,max_length=1000)
@app.get('/health')
def health(): return {'status':'ok','model_ready':MODEL.exists(),'model_version':VERSION}
@app.get('/api/v1/model/metrics')
def metrics():
 p=ART/'metrics.json'
 if not p.exists(): raise HTTPException(404,'No evaluation report. Run the training pipeline first.')
 return json.loads(p.read_text())
@app.post('/api/v1/classify')
def classify(q:Query):
 if not MODEL.exists(): raise HTTPException(503,'Model is not trained. Run: python -m app.train --data data/health_queries.csv')
 model=load(MODEL);proba=None
 pred=model.predict([q.text])[0]
 try:
  confidence=float(model.predict_proba([q.text]).max())
 except Exception: confidence=.5
 classes=list(model.classes_);explanation=[]
 vec=model.named_steps['tfidf'];clf=model.named_steps['clf'];row=vec.transform([q.text]);coef=clf.coef_[classes.index(pred)] if clf.coef_.ndim>1 else clf.coef_[0];terms=vec.get_feature_names_out();weights=row.toarray()[0]*coef;top=weights.argsort()[::-1][:4];explanation=[f"Relevant phrase: {terms[i]}" for i in top if weights[i]>0][:3] or ['Classification was based on the learned TF-IDF representation.']
 result=route(pred,confidence,q.text)
 if result.get('safety_override'):
  explanation=['A high-risk safety phrase triggered the emergency routing safeguard.']
 result.update({'explanation':explanation,'model_version':VERSION});return result
