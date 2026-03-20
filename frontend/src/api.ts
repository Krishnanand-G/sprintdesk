const tokenKey = "sprintdesk_token";

export function getToken(): string | null {
  return localStorage.getItem(tokenKey);
}

export function setToken(t: string | null) {
  if (t) localStorage.setItem(tokenKey, t);
  else localStorage.removeItem(tokenKey);
}

export async function api<T>(path: string, init: RequestInit = {}): Promise<T> {
  const headers = new Headers(init.headers || {});
  const token = getToken();
  if (token) headers.set("Authorization", `Bearer ${token}`);
  if (init.body && !(init.body instanceof FormData)) headers.set("Content-Type", "application/json");
  const res = await fetch(path, { ...init, headers });
  if (!res.ok) throw new Error(await res.text());
  return res.json() as Promise<T>;
}

export type Project = { id: number; name: string; key: string };
export type Sprint = { id: number; project_id: number; name: string; status: string };
export type Ticket = { id: number; title: string; status: string; ticket_type: string; sprint_id: number | null };
export type BoardSummary = { backlog: number; todo: number; doing: number; done: number };
