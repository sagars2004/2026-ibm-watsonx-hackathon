import './BottleneckList.css';

function BottleneckList({ bottlenecks }) {
    if (!bottlenecks || bottlenecks.length === 0) {
        return (
            <div className="card bottleneck-list">
                <div className="card-header">
                    <h3 className="card-title">Detected Bottlenecks</h3>
                </div>
                <div className="empty-state">
                    <p>No bottlenecks detected</p>
                </div>
            </div>
        );
    }

    return (
        <div className="card bottleneck-list">
            <div className="card-header">
                <h3 className="card-title">Detected Bottlenecks</h3>
                <span className="badge">{bottlenecks.length} issues</span>
            </div>
            <div className="bottleneck-items">
                {bottlenecks.map((bottleneck, index) => (
                    <div key={index} className={`bottleneck-item severity-${bottleneck.severity}`}>
                        <div className="bottleneck-icon">{bottleneck.icon}</div>
                        <div className="bottleneck-content">
                            <div className="bottleneck-header">
                                <h4>{bottleneck.title}</h4>
                                <span className={`severity-badge ${bottleneck.severity}`}>
                                    {bottleneck.severity}
                                </span>
                            </div>
                            <p className="bottleneck-description">{bottleneck.description}</p>
                            <div className="bottleneck-metric">
                                <span className="metric-value">{bottleneck.metric_value}</span>
                                <span className="metric-label">{bottleneck.metric_label}</span>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default BottleneckList;
