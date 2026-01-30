import './BottleneckList.css';

function BottleneckList({ bottlenecks }) {
    if (!bottlenecks || bottlenecks.length === 0) {
        return (
            <div className="empty-state">
                <div className="empty-state-icon">🎉</div>
                <h3>No Bottlenecks Detected!</h3>
                <p>Your team is running smoothly.</p>
            </div>
        );
    }

    return (
        <div className="bottleneck-list">
            {bottlenecks.map((bottleneck, index) => (
                <div
                    key={index}
                    className={`bottleneck-item severity-${bottleneck.severity}`}
                >
                    <div className="bottleneck-icon">
                        {bottleneck.icon || getDefaultIcon(bottleneck.type)}
                    </div>

                    <div className="bottleneck-content">
                        <div className="bottleneck-title">
                            <span>{bottleneck.title}</span>
                            <span className={`severity-badge ${bottleneck.severity}`}>
                                {bottleneck.severity}
                            </span>
                        </div>

                        <p className="bottleneck-description">
                            {bottleneck.description}
                        </p>

                        {bottleneck.metric_value && (
                            <div className="bottleneck-metric">
                                <span className="bottleneck-metric-value">
                                    {bottleneck.metric_value}
                                </span>
                                <span className="bottleneck-metric-label">
                                    {bottleneck.metric_label}
                                </span>
                            </div>
                        )}

                        {bottleneck.impact && (
                            <p className="bottleneck-impact">
                                <strong>Impact:</strong> {bottleneck.impact}
                            </p>
                        )}
                    </div>
                </div>
            ))}
        </div>
    );
}

function getDefaultIcon(type) {
    const icons = {
        single_point_of_failure: '🚨',
        hidden_delay: '⏰',
        flaky_process: '🔄',
        knowledge_silo: '🔐',
        meeting_overload: '💬',
        blocked_work: '🚫',
    };
    return icons[type] || '⚠️';
}

export default BottleneckList;
