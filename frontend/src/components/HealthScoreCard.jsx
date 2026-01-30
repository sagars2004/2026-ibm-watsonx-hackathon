import { useEffect, useRef } from 'react';
import './HealthScoreCard.css';

function HealthScoreCard({ score, status, trend }) {
    const circleRef = useRef(null);

    useEffect(() => {
        if (circleRef.current) {
            // Animate the progress ring
            const circumference = 2 * Math.PI * 70; // radius = 70
            const offset = circumference - (score / 100) * circumference;
            circleRef.current.style.strokeDasharray = circumference;
            circleRef.current.style.strokeDashoffset = offset;
        }
    }, [score]);

    const getStatusColor = () => {
        if (score >= 80) return 'var(--status-success)';
        if (score >= 60) return 'var(--status-warning)';
        return 'var(--status-error)';
    };

    const getStatusLabel = () => {
        if (score >= 80) return 'Healthy';
        if (score >= 60) return 'Needs Attention';
        return 'Critical';
    };

    return (
        <div className="card health-score-card">
            <div className="health-score-ring">
                <svg width="180" height="180" viewBox="0 0 180 180">
                    {/* Background circle */}
                    <circle
                        cx="90"
                        cy="90"
                        r="70"
                        fill="none"
                        stroke="var(--bg-tertiary)"
                        strokeWidth="12"
                    />
                    {/* Progress circle */}
                    <circle
                        ref={circleRef}
                        cx="90"
                        cy="90"
                        r="70"
                        fill="none"
                        stroke={getStatusColor()}
                        strokeWidth="12"
                        strokeLinecap="round"
                        transform="rotate(-90 90 90)"
                        style={{
                            transition: 'stroke-dashoffset 1s ease-out',
                        }}
                    />
                </svg>
                <div className="health-score-value" style={{ color: getStatusColor() }}>
                    {score}
                </div>
                <div className="health-score-max">/100</div>
            </div>

            <div className="health-score-info">
                <span className={`health-status ${status}`}>
                    {getStatusLabel()}
                </span>

                {trend !== undefined && trend !== 0 && (
                    <div className={`health-trend ${trend >= 0 ? 'positive' : 'negative'}`}>
                        {trend >= 0 ? '↑' : '↓'} {Math.abs(trend)} pts from last week
                    </div>
                )}
            </div>

            <p className="health-description">
                Team Health Score based on workflow analysis across GitHub, Jira, Slack, and CI/CD.
            </p>
        </div>
    );
}

export default HealthScoreCard;
