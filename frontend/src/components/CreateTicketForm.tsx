import { FormEvent, useState } from "react";
import { api } from "../api";

type Props = { projectId: number; sprintId?: number; onCreated: () => void };

export default function CreateTicketForm({ projectId, sprintId, onCreated }: Props) {
  const [title, setTitle] = useState("");
  const [ticketType, setTicketType] = useState("task");
  const [severity, setSeverity] = useState("medium");

  async function submit(e: FormEvent) {
    e.preventDefault();
    const body: Record<string, unknown> = { title, ticket_type: ticketType, body: "" };
    if (sprintId) body.sprint_id = sprintId;
    if (ticketType === "bug") body.severity = severity;
    await api(`/projects/${projectId}/tickets`, { method: "POST", body: JSON.stringify(body) });
    setTitle("");
    onCreated();
  }

  return (
    <form className="card" onSubmit={submit}>
      <h3>New ticket</h3>
      <input placeholder="Title" value={title} onChange={(e) => setTitle(e.target.value)} required />
      {" "}
      <select value={ticketType} onChange={(e) => setTicketType(e.target.value)}>
        <option value="story">Story</option>
        <option value="bug">Bug</option>
        <option value="task">Task</option>
      </select>
      {ticketType === "bug" && (
        <select value={severity} onChange={(e) => setSeverity(e.target.value)}>
          <option value="low">Low</option>
          <option value="medium">Medium</option>
          <option value="high">High</option>
          <option value="critical">Critical</option>
        </select>
      )}
      {" "}
      <button type="submit">Create</button>
    </form>
  );
}
