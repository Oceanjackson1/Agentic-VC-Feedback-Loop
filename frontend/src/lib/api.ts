const API_BASE = process.env.NEXT_PUBLIC_API_URL || "";

function getToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("auth_token");
}

export async function apiFetch(path: string, options: RequestInit = {}) {
  const token = getToken();
  const headers: Record<string, string> = {
    ...(options.headers as Record<string, string>),
  };
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }
  const res = await fetch(`${API_BASE}${path}`, { ...options, headers });
  return res;
}

export interface ScenarioMeta {
  id: string;
  name_zh: string;
  name_en: string;
  description_zh: string;
  description_en: string;
  icon: string;
}

export async function fetchScenarios(): Promise<ScenarioMeta[]> {
  const res = await apiFetch("/api/scenarios");
  if (!res.ok) throw new Error("获取场景列表失败");
  return res.json();
}

export async function analyzeFile(
  file: File,
  scenario: string,
  language: string,
  contextFile?: File | null
): Promise<Blob> {
  const form = new FormData();
  form.append("file", file);
  form.append("scenario", scenario);
  form.append("language", language);
  if (contextFile) {
    form.append("context_file", contextFile);
  }
  const res = await apiFetch("/api/analyze", { method: "POST", body: form });
  if (!res.ok) {
    const text = await res.text();
    let msg = text;
    try {
      const j = JSON.parse(text);
      msg = j.detail || j.message || text;
    } catch {}
    throw new Error(msg);
  }
  return res.blob();
}

export async function googleLogin(code: string, redirectUri: string) {
  const res = await fetch(`${API_BASE}/api/auth/google`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ code, redirect_uri: redirectUri }),
  });
  if (!res.ok) {
    const data = await res.json().catch(() => ({}));
    throw new Error(data.detail || "登录失败");
  }
  return res.json();
}
