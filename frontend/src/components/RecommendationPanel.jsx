import './RecommendationPanel.css';

const PriorityIcon = ({ priority }) => {
    if (priority === 'high') {
        return (
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M12 19V5M5 12l7-7 7 7" />
            </svg>
        );
    }
    if (priority === 'medium') {
        return (
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <circle cx="12" cy="12" r="1" />
                <circle cx="12" cy="5" r="1" />
                <circle cx="12" cy="19" r="1" />
            </svg>
        );
    }
    return (
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M12 5v14M5 12l7 7 7-7" />
        </svg>
    );
};

function RecommendationPanel({ recommendations }) {
    if (!recommendations || recommendations.length === 0) {
        return (
            <div className="card recommendation-panel">
                <div className="card-header">
                    <h3 className="card-title">Recommendations</h3>
                </div>
                <div className="empty-state">
                    <p>No recommendations available</p>
                </div>
            </div>
        );
    }

    const getPriorityClass = (priority) => {
        if (priority === 'high') return 'high';
        if (priority === 'medium') return 'medium';
        return 'low';
    };

    return (
        <div className="card recommendation-panel">
            <div className="card-header">
                <h3 className="card-title">Recommendations</h3>
                <span className="badge">{recommendations.length} actions</span>
            </div>

            <div className="recommendation-list">
                {recommendations.map((rec, index) => (
                    <div key={index} className="recommendation-item">
                        <div className={`priority-indicator ${getPriorityClass(rec.priority)}`}>
                            <PriorityIcon priority={rec.priority} />
                        </div>
                        <div className="recommendation-content">
                            <h4 className="recommendation-title">{rec.title}</h4>
                            <p className="recommendation-related">
                                Related: {rec.related_bottleneck}
                            </p>
                            {rec.actions && rec.actions.length > 0 && (
                                <ul className="action-list">
                                    {rec.actions.slice(0, 2).map((action, i) => (
                                        <li key={i} className="action-item">
                                            <span className="action-type">{action.type}</span>
                                            <span className="action-description">{action.description}</span>
                                        </li>
                                    ))}
                                </ul>
                            )}
                        </div>
                        <div className={`priority-badge ${getPriorityClass(rec.priority)}`}>
                            {rec.priority}
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default RecommendationPanel;
