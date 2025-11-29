import React, { useEffect, useRef } from 'react';
import { Terminal } from 'lucide-react';

export default function LogViewer({ logs }) {
    const endRef = useRef(null);

    useEffect(() => {
        endRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [logs]);

    return (
        <div className="glass-panel" style={{ padding: '1.5rem', height: '100%', display: 'flex', flexDirection: 'column' }}>
            <h2 style={{ fontSize: '1.25rem', fontWeight: 'bold', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <Terminal color="#eab308" /> System Logs
            </h2>
            <div style={{
                flex: 1,
                overflowY: 'auto',
                fontFamily: 'monospace',
                fontSize: '0.875rem',
                padding: '0.5rem',
                background: 'rgba(0,0,0,0.3)',
                borderRadius: '0.5rem'
            }}>
                {logs.map((log, i) => (
                    <div key={i} style={{ color: '#4ade80', borderBottom: '1px solid rgba(255,255,255,0.05)', paddingBottom: '0.25rem', marginBottom: '0.25rem' }}>
                        {log}
                    </div>
                ))}
                <div ref={endRef} />
            </div>
        </div>
    );
}
