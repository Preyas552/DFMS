import React, { useState, useEffect } from 'react';
import ServerStatus from './components/ServerStatus';
import FileExplorer from './components/FileExplorer';
import LogViewer from './components/LogViewer';
import { Cloud } from 'lucide-react';

const API_BASE = 'http://localhost:3000/api';

function App() {
  const [servers, setServers] = useState([]);
  const [files, setFiles] = useState([]);
  const [logs, setLogs] = useState([]);
  const [selectedFile, setSelectedFile] = useState(null);

  const fetchData = async () => {
    try {
      const statusRes = await fetch(`${API_BASE}/status`);
      const statusData = await statusRes.json();
      setServers(statusData.servers || []);

      const filesRes = await fetch(`${API_BASE}/files`);
      const filesData = await filesRes.json();
      setFiles(filesData.files || []);

      const logsRes = await fetch(`${API_BASE}/logs`);
      const logsData = await logsRes.json();
      setLogs(logsData.logs || []);
    } catch (e) {
      console.error("Failed to fetch data", e);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 2000); // Poll every 2s
    return () => clearInterval(interval);
  }, []);

  const handleReadFile = async (filename) => {
    try {
      const res = await fetch(`${API_BASE}/files/${filename}`);
      const data = await res.json();
      setSelectedFile(data);
    } catch (e) {
      alert("Failed to read file");
    }
  };

  const handleWriteFile = async (filename, content) => {
    try {
      const res = await fetch(`${API_BASE}/files`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ filename, content })
      });
      if (!res.ok) throw new Error(await res.text());
      fetchData(); // Refresh immediately
    } catch (e) {
      alert(`Write failed: ${e.message}`);
    }
  };

  return (
    <div className="app-container" style={{ padding: '2rem', maxWidth: '1200px', margin: '0 auto' }}>
      <header style={{ marginBottom: '2rem', textAlign: 'center' }}>
        <h1 style={{ fontSize: '2.5rem', fontWeight: 'bold', background: 'linear-gradient(to right, #60a5fa, #a78bfa)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', display: 'inline-flex', alignItems: 'center', gap: '1rem', justifyContent: 'center' }}>
          <Cloud size={48} color="#60a5fa" /> Distributed File Storage
        </h1>
        <p style={{ color: 'var(--text-secondary)' }}>Quorum Consistency • Primary-Based Replication • Client Caching</p>
      </header>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem', marginBottom: '1.5rem' }}>
        <ServerStatus servers={servers} />
        <LogViewer logs={logs} />
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '1.5rem', height: '500px' }}>
        <FileExplorer
          files={files}
          onReadFile={handleReadFile}
          onWriteFile={handleWriteFile}
          refresh={fetchData}
        />

        <div className="glass-panel" style={{ padding: '1.5rem', display: 'flex', flexDirection: 'column' }}>
          <h2 style={{ fontSize: '1.25rem', fontWeight: 'bold', marginBottom: '1rem' }}>File Content</h2>
          {selectedFile ? (
            <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
              <div style={{ marginBottom: '1rem', paddingBottom: '1rem', borderBottom: '1px solid var(--border)' }}>
                <div style={{ fontSize: '1.1rem', fontWeight: 'bold' }}>{selectedFile.filename}</div>
                <div style={{ fontSize: '0.875rem', color: selectedFile.source === 'CACHE HIT' ? '#34d399' : '#fbbf24' }}>
                  Source: {selectedFile.source}
                </div>
              </div>
              <pre style={{
                flex: 1,
                background: 'rgba(0,0,0,0.3)',
                padding: '1rem',
                borderRadius: '0.5rem',
                overflow: 'auto',
                fontFamily: 'monospace'
              }}>
                {selectedFile.content}
              </pre>
            </div>
          ) : (
            <div style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--text-secondary)' }}>
              Select a file to view content
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
