import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import CreateTicketForm from "../components/CreateTicketForm";
import { api, BoardSummary, Sprint, Ticket } from "../api";

const COLS = ["backlog", "todo", "doing", "done"] as const;

export default function SprintBoard() {
  const { projectId } = useParams();
  const pid = Number(projectId);
  const [sprints, setSprints] = useState<Sprint[]>([]);
  const [sprintId, setSprintId] = useState<number | null>(null);
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [summary, setSummary] = useState<BoardSummary | null>(null);

  async function reload() {
    const s = await api<Sprint[]>(`/projects/${pid}/sprints`);
    setSprints(s);
    const sid = sprintId ?? s[0]?.id ?? null;
    setSprintId(sid);
    const all = await api<Ticket[]>(`/projects/${pid}/tickets`);
    setTickets(sid ? all.filter((t) => t.sprint_id === sid) : all);
    if (sid) setSummary(await api<BoardSummary>(`/projects/${pid}/sprints/${sid}/board-summary`));
  }

  useEffect(() => {
    reload().catch(console.error);
  }, [pid]);

  useEffect(() => {
    if (sprintId) reload().catch(console.error);
  }, [sprintId]);

  return (
    <div className="layout">
      <p><Link to="/projects">Projects</Link> / board</p>
      <h1>Sprint board</h1>
      <label>
        Sprint{" "}
        <select value={sprintId ?? ""} onChange={(e) => setSprintId(Number(e.target.value))}>
          {sprints.map((s) => (
            <option key={s.id} value={s.id}>{s.name} ({s.status})</option>
          ))}
        </select>
      </label>
      {summary && (
        <p>Totals: backlog {summary.backlog}, todo {summary.todo}, doing {summary.doing}, done {summary.done}</p>
      )}
      <CreateTicketForm projectId={pid} sprintId={sprintId ?? undefined} onCreated={reload} />
      <div className="board">
        {COLS.map((col) => (
          <div className="column" key={col}>
            <h3>{col}</h3>
            {tickets.filter((t) => t.status === col).map((t) => (
              <div className="ticket" key={t.id}>{t.title} <small>({t.ticket_type})</small></div>
            ))}
          </div>
        ))}
      </div>
      <p><Link to={`/projects/${pid}/tickets`}>Ticket list</Link></p>
    </div>
  );
}
