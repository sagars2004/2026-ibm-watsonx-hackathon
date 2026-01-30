import { useEffect, useState } from 'react';
import './HealthScoreCard.css';

function HealthScoreCard({ score, status, trends }) {
    const [animatedScore, setAnimatedScore] = useState(0);

    useEffect(() => {
        let start = 0;
        const duration = 1500;
        const increment = score / (duration / 16);

        const timer = setInterval(() => {
            start += increment;
            if (start >= score) {
                setAnimatedScore(score);
                clearInterval(timer);
            } else {
                setAnimatedScore(Math.floor(start));
            }
        }, 16);

        return () => clearInterval(timer);
    }, [score]);

    const circumference = 2 * Math.PI * 45;
    const strokeDashoffset = circumference - (animatedScore / 100) * circumference;

    const getStatusColor = () => {
        if (status === 'healthy') return 'var(--status-success)';
        if (status === 'warning') return 'var(--status-warning)';
        return 'var(--status-error)';
    };

    return (
        <div className="card health-score-card">
            <div className="card-header">
                <h3 className="card-title">Team Health Score</h3>
                {trends && (
                    <span className={`trend ${trends.health_score_change >= 0 ? 'up' : 'down'}`}>
                        {trends.health_score_change >= 0 ? '↗' : '↘'} {Math.abs(trends.health_score_change)}%
                    </span>
                )}
            </div>
            <div className="health-score-content">
                <div className="score-ring">
                    <svg viewBox="0 0 100 100">
                        <circle className="ring-bg" cx="50" cy="50" r="45" />
                        <circle
                            className="ring-progress"
                            cx="50"
                            cy="50"
                            r="45"
                            style={{
                                strokeDasharray: circumference,
                                strokeDashoffset,
                                stroke: getStatusColor(),
                            }}
                        />
                    </svg>
                    <div className="score-value">
                        <span className="score-number">{animatedScore}</span>
                        <span className="score-max">/100</span>
                    </div>
                </div>
                <div className={`status-badge ${status}`}>
                    {status === 'healthy' ? '✓ Healthy' : status === 'warning' ? '⚠ Warning' : '✗ Critical'}
                </div>
            </div>
        </div>
    );
}

export default HealthScoreCard;
