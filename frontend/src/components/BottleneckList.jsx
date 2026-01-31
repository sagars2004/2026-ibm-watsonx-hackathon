import './BottleneckList.css';

const TypeIcon = ({ type }) => {
    const icons = {
        single_point_of_failure: (
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
                <path d="M12 8v4M12 16h.01" />
            </svg>
        ),
        hidden_delay: (
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                <circle cx="12" cy="12" r="10" />
                <polyline points="12 6 12 12 16 14" />
            </svg>
        ),
        flaky_process: (
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                <path d="M22 12h-4l-3 9L9 3l-3 9H2" />
            </svg>
        ),
        knowledge_silo: (
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
                <circle cx="9" cy="7" r="4" />
                <path d="M23 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75" />
            </svg>
        ),
        meeting_overload: (
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                <rect x="3" y="4" width="18" height="18" rx="2" ry="2" />
                <line x1="16" y1="2" x2="16" y2="6" />
                <line x1="8" y1="2" x2="8" y2="6" />
                <line x1="3" y1="10" x2="21" y2="10" />
            </svg>
        ),
        blocked_work: (
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
                <path d="M7 11V7a5 5 0 0 1 10 0v4" />
            </svg>
        ),
    };
    return icons[type] || icons.hidden_delay;
};

function BottleneckList({ bottlenecks }) {
    if (!bottlenecks || bottlenecks.length === 0) {
        return (
            <div className="card bottleneck-list">
                <div className="card-header">
                    <h3 className="card-title">Detected Issues</h3>
                </div>
                <div className="empty-state">
                    <p>No bottlenecks detected</p>
                </div>
            </div>
        );
    }

    const getSeverityClass = (severity) => {
        if (severity === 'high') return 'error';
        if (severity === 'medium') return 'warning';
        return 'info';
    };

    return (
        <div className="card bottleneck-list-card" style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
            <div className="card-header">
                <h3 className="card-title">Detected Issues</h3>
                <span className="badge">{bottlenecks.length} found</span>
            </div>

            <div className="bottleneck-list">
                {bottlenecks.map((bottleneck, index) => (
                    <div key={index} className={`bottleneck-item ${bottleneck.severity}`}>
                        <div className="bottleneck-icon">
                            <TypeIcon type={bottleneck.type} />
                        </div>
                        <div className="bottleneck-content">
                            <div className="bottleneck-header">
                                <h4 className="bottleneck-title">{bottleneck.title}</h4>
                                <span className="bottleneck-severity">
                                    {bottleneck.severity}
                                </span>
                            </div>
                            {bottleneck.metric_value && (
                                <div className="bottleneck-meta" style={{ marginBottom: '4px', color: 'var(--text-primary)', fontSize: '0.8rem' }}>
                                    Impact: <strong>{bottleneck.metric_value}</strong>
                                </div>
                            )}
                            <p className="bottleneck-description" style={{ fontSize: '0.75rem', margin: 0 }}>
                                {bottleneck.description}
                            </p>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default BottleneckList;
