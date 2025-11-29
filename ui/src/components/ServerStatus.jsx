import React from 'react';
import { Database, Activity } from 'lucide-react';

export default function ServerStatus({ servers }) {
    return (
        <div className="glass-panel" style={{ padding: '1.5rem' }}>
            <h2 style={{ fontSize: '1.25rem', fontWeight: 'bold', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <Activity color="var(--accent-primary)" /> System Status
            </h2>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))', gap: '1rem' }}>
                {servers.map((server) => (
                    <div key={server.name} className="glass-panel" style={{ padding: '1rem', display: 'flex', flexDirection: 'column', alignItems: 'center', textAlign: 'center', background: 'rgba(255,255,255,0.03)' }}>
                        <div style={{ width: '3rem', height: '3rem', borderRadius: '50%', background: 'rgba(16, 185, 129, 0.2)', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '0.5rem', color: '#10b981' }}>
                            <Database size={24} />
                        </div>
                        <h3 style={{ fontWeight: 'bold' }}>{server.name}</h3>
                        <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>{server.host}:{server.port}</p>
                        <div style={{ marginTop: '0.5rem', fontSize: '0.75rem', padding: '0.25rem 0.5rem', borderRadius: '9999px', background: 'rgba(16, 185, 129, 0.1)', color: '#34d399' }}>
                            Online
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}
