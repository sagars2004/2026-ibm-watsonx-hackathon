import './MetricsGrid.css';

function MetricsGrid({ metrics }) {
    if (!metrics) return null;

    const cards = [
        {
            icon: '📊',
            title: 'GitHub',
            stats: [
                { label: 'Total PRs', value: metrics.github?.total_prs || 0 },
                { label: 'Avg Review Time', value: `${metrics.github?.avg_review_time_hours || 0}h` },
                { label: 'Pending Reviews', value: metrics.github?.pending_reviews || 0 },
            ],
        },
        {
            icon: '📋',
            title: 'Jira',
            stats: [
                { label: 'Total Tickets', value: metrics.jira?.total_tickets || 0 },
                { label: 'Blocked', value: metrics.jira?.blocked_count || 0 },
                { label: 'Velocity', value: `${metrics.jira?.velocity || 0} pts` },
            ],
        },
        {
            icon: '💬',
            title: 'Slack',
            stats: [
                { label: 'Meeting Time', value: `${metrics.slack?.meeting_percentage || 0}%` },
                { label: 'Msgs/Day', value: metrics.slack?.avg_messages_per_day || 0 },
                { label: 'After Hours', value: `${metrics.slack?.after_hours_activity_rate || 0}%` },
            ],
        },
        {
            icon: '🔧',
            title: 'CI/CD',
            stats: [
                { label: 'Success Rate', value: `${metrics.cicd?.success_rate || 0}%` },
                { label: 'Total Runs', value: metrics.cicd?.total_runs || 0 },
                { label: 'Avg Duration', value: `${metrics.cicd?.avg_duration_minutes || 0}m` },
            ],
        },
    ];

    return (
        <div className="card metrics-grid">
            <div className="card-header">
                <h3 className="card-title">Data Sources</h3>
            </div>
            <div className="metrics-cards">
                {cards.map((card, i) => (
                    <div key={i} className="metric-card">
                        <div className="metric-card-header">
                            <span className="metric-icon">{card.icon}</span>
                            <span>{card.title}</span>
                        </div>
                        <div className="metric-stats">
                            {card.stats.map((stat, j) => (
                                <div key={j} className="stat">
                                    <span className="stat-value">{stat.value}</span>
                                    <span className="stat-label">{stat.label}</span>
                                </div>
                            ))}
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default MetricsGrid;
