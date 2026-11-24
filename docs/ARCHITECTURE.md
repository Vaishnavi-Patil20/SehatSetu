# SehatSetu 2.0 architecture

```mermaid
flowchart LR
U[User] --> R[React + TypeScript + Vite]
R --> A[FastAPI ML Service]
R --> S[Supabase Auth + PostgreSQL]
A --> P[Preprocess + TF-IDF]
P --> M[Logistic Regression inference]
P --> B[Linear SVM baseline]
M --> E[Confidence + explanation]
E --> Q[Safety layer]
Q --> RT[Configurable routing engine]
RT --> R
S --> D[Query history / appointments / profiles]
```

## Boundaries
- React is responsible for presentation and authenticated client workflows.
- FastAPI owns NLP inference, safety checks and routing decisions.
- Supabase owns identity, persistence and row-level authorization.
- The ML service never claims to diagnose or prescribe.
