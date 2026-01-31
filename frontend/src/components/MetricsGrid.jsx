import './MetricsGrid.css';

const MetricIcon = ({ type }) => {
    const icons = {
        github: (
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                <path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22" />
            </svg>
        ),
        jira: (
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                <rect x="3" y="3" width="18" height="18" rx="2" />
                <path d="M7 8h10M7 12h10M7 16h6" />
            </svg>
        ),
        slack: (
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                <rect x="13" y="2" width="3" height="8" rx="1.5" />
                <path d="M19 8.5V10h1.5A1.5 1.5 0 1 0 19 8.5" />
                <rect x="8" y="14" width="3" height="8" rx="1.5" />
                <path d="M5 15.5V14H3.5A1.5 1.5 0 1 0 5 15.5" />
                <rect x="14" y="13" width="8" height="3" rx="1.5" />
                <path d="M15.5 19H14v1.5a1.5 1.5 0 1 0 1.5-1.5" />
                <rect x="2" y="8" width="8" height="3" rx="1.5" />
                <path d="M8.5 5H10V3.5A1.5 1.5 0 1 0 8.5 5" />
            </svg>
        ),
        cicd: (
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                <circle cx="12" cy="12" r="10" />
                <path d="M8 12l2 2 4-4" />
            </svg>
        ),
    };
    return icons[type] || icons.github;
};

function MetricsGrid({ metrics }) {
    if (!metrics) return null;

    const metricCards = [
        {
            id: 'github',
            title: 'Code Reviews',
            icon: 'github',
            stats: metrics.github ? [
                { label: 'Total PRs', value: metrics.github.total_prs },
                { label: 'Avg Review Time', value: `${metrics.github.avg_review_time_hours}h` },
                { label: 'Pending', value: metrics.github.pending_reviews },
            ] : [],
        },
        {
            id: 'jira',
            title: 'Issue Tracking',
            icon: 'jira',
            stats: metrics.jira ? [
                { label: 'Total Tickets', value: metrics.jira.total_tickets },
                { label: 'Blocked', value: metrics.jira.blocked_count },
                { label: 'Velocity', value: `${metrics.jira.velocity} pts` },
            ] : [],
        },
        {
            id: 'slack',
            title: 'Communication',
            icon: 'slack',
            stats: metrics.slack ? [
                { label: 'Daily Msgs', value: Math.round(metrics.slack.avg_messages_per_day) },
                { label: 'Meeting Load', value: `${metrics.slack.meeting_percentage}%` },
                {
                    label: 'Team Mood',
                    value: `${metrics.slack.sentiment_score || '--'}/100`,
                    isScore: true,
                    score: metrics.slack.sentiment_score
                },
            ] : [],
        },
        {
            id: 'cicd',
            title: 'CI/CD Pipeline',
            icon: 'cicd',
            stats: metrics.cicd ? [
                { label: 'Success Rate', value: `${metrics.cicd.success_rate}%` },
                { label: 'Avg Duration', value: `${metrics.cicd.avg_duration_minutes}m` },
                { label: 'Runs/Day', value: (metrics.cicd.total_runs / 30).toFixed(1) },
            ] : [],
        },
    ];

    const getScoreColor = (score) => {
        if (!score) return 'inherit';
        if (score >= 75) return '#4ade80'; // Green
        if (score >= 50) return '#fbbf24'; // Orange
        return '#f87171'; // Red
    };

    return (
        <div className="card metrics-grid-container">
            <div className="card-header">
                <h3 className="card-title">Data Sources</h3>
                <span className="badge">Live Metrics</span>
            </div>
            <div className="metrics-grid">
                {metricCards.map((card) => (
                    <div key={card.id} className="metric-card">
                        <div className="metric-card-header">
                            <div className="metric-icon">
                                <MetricIcon type={card.icon} />
                            </div>
                            <h4>{card.title}</h4>
                        </div>
                        <div className="metric-stats">
                            {card.stats.map((stat, i) => (
                                <div key={i} className="metric-stat">
                                    <span
                                        className="metric-stat-value"
                                        style={stat.isScore ? { color: getScoreColor(stat.score) } : {}}
                                    >
                                        {stat.value}
                                    </span>
                                    <span className="metric-stat-label">{stat.label}</span>
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
