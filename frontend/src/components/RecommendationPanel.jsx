import { useState } from 'react';
import './RecommendationPanel.css';

function RecommendationPanel({ recommendations }) {
    const [expanded, setExpanded] = useState({});

    const toggleExpand = (id) => {
        setExpanded((prev) => ({ ...prev, [id]: !prev[id] }));
    };

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

    return (
        <div className="card recommendation-panel">
            <div className="card-header">
                <h3 className="card-title">AI Recommendations</h3>
                <span className="badge">{recommendations.length} actions</span>
            </div>
            <div className="recommendation-items">
                {recommendations.map((rec, index) => (
                    <div
                        key={rec.id || index}
                        className={`recommendation-item priority-${rec.priority}`}
                    >
                        <div
                            className="recommendation-header"
                            onClick={() => toggleExpand(rec.id || index)}
                        >
                            <div className="recommendation-info">
                                <span className="priority-indicator"></span>
                                <div>
                                    <h4>{rec.title}</h4>
                                    <p className="related-bottleneck">{rec.related_bottleneck}</p>
                                </div>
                            </div>
                            <span className="expand-icon">{expanded[rec.id || index] ? '−' : '+'}</span>
                        </div>
                        {expanded[rec.id || index] && rec.actions && (
                            <div className="recommendation-actions">
                                <h5>Suggested Actions:</h5>
                                {rec.actions.map((action, i) => (
                                    <div key={i} className="action-item">
                                        <span className="action-icon">
                                            {action.type === 'create_jira_ticket' && '📋'}
                                            {action.type === 'slack_message' && '💬'}
                                            {action.type === 'schedule_meeting' && '📅'}
                                        </span>
                                        <span>{action.description}</span>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                ))}
            </div>
        </div>
    );
}

export default RecommendationPanel;
