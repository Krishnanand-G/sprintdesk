import { Navigate, Route, Routes } from "react-router-dom";
import { getToken } from "./api";
import Login from "./pages/Login";
import Projects from "./pages/Projects";
import SprintBoard from "./pages/SprintBoard";
import TicketList from "./pages/TicketList";

function Private({ children }: { children: JSX.Element }) {
  if (!getToken()) return <Navigate to="/login" replace />;
  return children;
}

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/projects" element={<Private><Projects /></Private>} />
      <Route path="/projects/:projectId" element={<Private><SprintBoard /></Private>} />
      <Route path="/projects/:projectId/tickets" element={<Private><TicketList /></Private>} />
      <Route path="*" element={<Navigate to="/login" replace />} />
    </Routes>
  );
}
