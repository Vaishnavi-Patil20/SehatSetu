const API = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export type Classification = {
  category: string;
  confidence: number;
  urgency: string;
  requires_human_review: boolean;
  destination: string;
  explanation: string[];
  model_version: string;
};

async function detailFromResponse(response: Response): Promise<string> {
  try {
    const body = await response.json();
    return typeof body?.detail === 'string' ? body.detail : 'Classification service unavailable.';
  } catch {
    return 'Classification service unavailable.';
  }
}

export async function classifyQuery(text: string): Promise<Classification> {
  const response = await fetch(`${API}/api/v1/classify`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text }),
  });
  if (!response.ok) throw new Error(await detailFromResponse(response));
  return response.json() as Promise<Classification>;
}

export async function health() {
  const response = await fetch(`${API}/health`);
  if (!response.ok) throw new Error('Classification service health check failed.');
  return response.json();
}
