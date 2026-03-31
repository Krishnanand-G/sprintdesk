import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { api, Ticket } from "../api";

export default function TicketList() {
  const { projectId } = useParams();
  const pid = Number(projectId);
  const [tickets, setTickets] = useState<Ticket[]>([]);

  useEffect(() => {
    api<Ticket[]>(`/projects/${pid}/tickets`).then(setTickets).catch(console.error);
  }, [pid]);

  return (
    <div className="layout">
      <p><Link to={`/projects/${pid}`}>Board</Link></p>
      <h1>Tickets</h1>
      <div className="card">
        <table width="100%">
          <thead><tr><th>Title</th><th>Type</th><th>Status</th></tr></thead>
          <tbody>
            {tickets.map((t) => (
              <tr key={t.id}><td>{t.title}</td><td>{t.ticket_type}</td><td>{t.status}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
