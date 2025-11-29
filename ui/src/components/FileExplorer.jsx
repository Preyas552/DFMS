import React, { useState } from 'react';
import { FileText, Upload, RefreshCw } from 'lucide-react';

export default function FileExplorer({ files, onReadFile, onWriteFile, refresh }) {
    const [isUploading, setIsUploading] = useState(false);
    const [newFileName, setNewFileName] = useState('');
    const [newFileContent, setNewFileContent] = useState('');

    const handleUpload = async () => {
        if (!newFileName || !newFileContent) return;
        await onWriteFile(newFileName, newFileContent);
        setIsUploading(false);
        setNewFileName('');
        setNewFileContent('');
    };

    return (
        <div className="glass-panel" style={{ padding: '1.5rem', height: '100%', display: 'flex', flexDirection: 'column' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                <h2 style={{ fontSize: '1.25rem', fontWeight: 'bold', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <FileText color="var(--accent-secondary)" /> Files
                </h2>
                <div style={{ display: 'flex', gap: '0.5rem' }}>
                    <button onClick={refresh} className="btn btn-secondary"><RefreshCw size={16} /></button>
                    <button onClick={() => setIsUploading(!isUploading)} className="btn btn-primary">
                        <Upload size={16} /> {isUploading ? 'Cancel' : 'Upload'}
                    </button>
                </div>
            </div>

            {isUploading && (
                <div className="glass-panel" style={{ marginBottom: '1rem', padding: '1rem', background: 'rgba(59, 130, 246, 0.1)' }}>
                    <input
                        placeholder="Filename (e.g. file1.txt)"
                        style={{ marginBottom: '0.5rem' }}
                        value={newFileName}
                        onChange={e => setNewFileName(e.target.value)}
                    />
                    <textarea
                        placeholder="Content..."
                        style={{ marginBottom: '0.5rem', height: '6rem' }}
                        value={newFileContent}
                        onChange={e => setNewFileContent(e.target.value)}
                    />
                    <button onClick={handleUpload} className="btn btn-primary" style={{ width: '100%' }}>Submit Write (Quorum)</button>
                </div>
            )}

            <div style={{ flex: 1, overflowY: 'auto' }}>
                {files.length === 0 ? (
                    <p style={{ color: 'var(--text-secondary)', textAlign: 'center', marginTop: '2.5rem' }}>No files found.</p>
                ) : (
                    <div style={{ display: 'grid', gap: '0.5rem' }}>
                        {files.map(file => (
                            <div key={file} onClick={() => onReadFile(file)}
                                style={{
                                    padding: '0.75rem',
                                    borderRadius: '0.5rem',
                                    cursor: 'pointer',
                                    display: 'flex',
                                    alignItems: 'center',
                                    gap: '0.75rem',
                                    border: '1px solid transparent',
                                    transition: 'background 0.2s'
                                }}
                                onMouseEnter={(e) => e.currentTarget.style.background = 'rgba(255,255,255,0.05)'}
                                onMouseLeave={(e) => e.currentTarget.style.background = 'transparent'}
                            >
                                <FileText size={20} color="#60a5fa" />
                                <span>{file}</span>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
}
