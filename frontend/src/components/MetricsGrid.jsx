import './MetricsGrid.css';

function MetricsGrid({ metrics }) {
    const stats = [
        {
            id: 'github',
            icon: '📊',
            label: 'Avg Review Time',
            value: metrics?.github?.avg_review_time_hours
                ? `${metrics.github.avg_review_time_hours}h`
                : '--',
            sublabel: 'hours per PR',
            color: 'github',
        },
        {
            id: 'jira',
            icon: '🎫',
            label: 'Blocked Tickets',
            value: metrics?.jira?.blocked_count ?? '--',
            sublabel: 'waiting for action',
            color: 'jira',
        },
        {
            id: 'slack',
            icon: '💬',
            label: 'Meeting Time',
            value: metrics?.slack?.meeting_percentage
                ? `${metrics.slack.meeting_percentage}%`
                : '--',
            sublabel: 'of work hours',
            color: 'slack',
        },
        {
            id: 'cicd',
            icon: '🚀',
            label: 'Pipeline Success',
            value: metrics?.cicd?.success_rate
                ? `${metrics.cicd.success_rate}%`
                : '--',
            sublabel: 'success rate',
            color: 'cicd',
        },
    ];

    return (
        <>
            {stats.map((stat) => (
                <div key={stat.id} className="card stat-card">
                    <div className={`stat-icon ${stat.color}`}>
                        {stat.icon}
                    </div>
                    <div className="stat-content">
                        <div className="stat-value">{stat.value}</div>
                        <div className="stat-label">{stat.label}</div>
                        <div className="stat-sublabel">{stat.sublabel}</div>
                    </div>
                </div>
            ))}
        </>
    );
}

export default MetricsGrid;
