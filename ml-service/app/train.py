import argparse,json,os
from pathlib import Path
import pandas as pd
from joblib import dump
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score,classification_report,confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC

ROOT=Path(__file__).resolve().parents[1]
ART=ROOT/'artifacts';ART.mkdir(exist_ok=True)

def main():
 p=argparse.ArgumentParser();p.add_argument('--data',default=str(ROOT/'data/health_queries.csv'));a=p.parse_args()
 df=pd.read_csv(a.data).dropna(subset=['text','category']);X=df.text.astype(str);y=df.category.astype(str)
 if y.nunique()<2: raise SystemExit('Need at least two classes.')
 Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.50,random_state=42,stratify=y)
 svm=Pipeline([('tfidf',TfidfVectorizer(ngram_range=(1,2),min_df=1,sublinear_tf=True)),('clf',LinearSVC())]);svm.fit(Xtr,ytr)
 lr=Pipeline([('tfidf',TfidfVectorizer(ngram_range=(1,2),min_df=1,sublinear_tf=True)),('clf',LogisticRegression(max_iter=2000))]);lr.fit(Xtr,ytr)
 pred=svm.predict(Xte);report=classification_report(yte,pred,output_dict=True,zero_division=0)
 metrics={'dataset':os.path.relpath(a.data,ROOT),'samples':len(df),'classes':sorted(y.unique().tolist()),'svm':{'accuracy':accuracy_score(yte,pred),'classification_report':report,'confusion_matrix':confusion_matrix(yte,pred).tolist()},'logistic_regression_accuracy':accuracy_score(yte,lr.predict(Xte))}
 dump(svm,ART/'svm.joblib');dump(lr,ART/'logistic_regression.joblib');(ART/'metrics.json').write_text(json.dumps(metrics,indent=2));print(json.dumps(metrics,indent=2))
if __name__=='__main__':main()
