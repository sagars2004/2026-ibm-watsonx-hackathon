import { useState } from 'react';
import './RecommendationPanel.css';

function RecommendationPanel({ recommendations }) {
    const [expandedId, setExpandedId] = useState(null);

    if (!recommendations || recommendations.length === 0) {
        return (
            <div className="empty-state">
                <div className="empty-state-icon">💡</div>
                <h3>No Recommendations</h3>
                <p>Run an analysis to get AI-powered suggestions.</p>
            </div>
        );
    }

    return (
        <div className="recommendation-list">
            {recommendations.map((rec, index) => (
                <div
                    key={rec.id || index}
                    className={`recommendation-item ${expandedId === rec.id ? 'expanded' : ''}`}
                >
                    <div
                        className="recommendation-header"
                        onClick={() => setExpandedId(expandedId === rec.id ? null : rec.id)}
                    >
                        <div className="recommendation-main">
                            <span className={`priority-indicator ${rec.priority}`}></span>
                            <div className="recommendation-info">
                                <h4 className="recommendation-title">{rec.title}</h4>
                                <p className="recommendation-related">
                                    Related: {rec.related_bottleneck}
                                </p>
                            </div>
                        </div>
                        <button className="expand-btn">
                            {expandedId === rec.id ? '−' : '+'}
                        </button>
                    </div>

                    {expandedId === rec.id && rec.actions && (
                        <div className="recommendation-details">
                            <p className="actions-label">Suggested Actions:</p>
                            <div className="recommendation-actions">
                                {rec.actions.map((action, actionIndex) => (
                                    <div key={actionIndex} className="action-chip">
                                        <span className="action-icon">
                                            {getActionIcon(action.type)}
                                        </span>
                                        <span className="action-text">{action.description}</span>
                                    </div>
                                ))}
                            </div>

                            <div className="recommendation-cta">
                                <button className="btn btn-primary btn-sm">
                                    🤖 Execute with Orchestrate
                                </button>
                                <button className="btn btn-ghost btn-sm">
                                    Dismiss
                                </button>
                            </div>
                        </div>
                    )}
                </div>
            ))}
        </div>
    );
}

function getActionIcon(type) {
    const icons = {
        create_jira_ticket: '🎫',
        slack_message: '💬',
        schedule_meeting: '📅',
        update_config: '⚙️',
        create_document: '📄',
    };
    return icons[type] || '📋';
}

export default RecommendationPanel;
