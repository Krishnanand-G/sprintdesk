import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api, Project } from "../api";

export default function Projects() {
  const [items, setItems] = useState<Project[]>([]);

  useEffect(() => {
    api<Project[]>("/projects").then(setItems).catch(console.error);
  }, []);

  return (
    <div className="layout">
      <h1>Projects</h1>
      <div className="card">
        <ul>
          {items.map((p) => (
            <li key={p.id}>
              <Link to={`/projects/${p.id}`}>{p.name}</Link> ({p.key})
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
