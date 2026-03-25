import { FormEvent, useState } from "react";
import { useNavigate } from "react-router-dom";
import { setToken } from "../api";

export default function Login() {
  const nav = useNavigate();
  const [email, setEmail] = useState("triager@local.dev");
  const [password, setPassword] = useState("triager123");
  const [err, setErr] = useState("");

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    setErr("");
    const body = new URLSearchParams({ username: email, password });
    const res = await fetch("/auth/login", { method: "POST", body });
    if (!res.ok) {
      setErr("Login failed");
      return;
    }
    const data = await res.json();
    setToken(data.access_token);
    nav("/projects");
  }

  return (
    <div className="layout">
      <div className="card" style={{ maxWidth: 420, margin: "3rem auto" }}>
        <h1>SprintDesk</h1>
        <p>Sign in to your workspace.</p>
        <form onSubmit={onSubmit}>
          <label>Email<br /><input value={email} onChange={(e) => setEmail(e.target.value)} /></label>
          <br /><br />
          <label>Password<br /><input type="password" value={password} onChange={(e) => setPassword(e.target.value)} /></label>
          <br /><br />
          <button type="submit">Login</button>
        </form>
        {err && <p style={{ color: "crimson" }}>{err}</p>}
      </div>
    </div>
  );
}
