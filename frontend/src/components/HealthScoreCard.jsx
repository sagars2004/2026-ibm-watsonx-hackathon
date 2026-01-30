import { useEffect, useState } from 'react';
import './HealthScoreCard.css';

function HealthScoreCard({ score, status, trends }) {
    const [animatedScore, setAnimatedScore] = useState(0);

    useEffect(() => {
        let start = 0;
        const duration = 1200;
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

    const circumference = 2 * Math.PI * 54;
    const strokeDashoffset = circumference - (animatedScore / 100) * circumference;

    const getStatusColor = () => {
        if (status === 'healthy') return 'var(--status-success)';
        if (status === 'warning') return 'var(--status-warning)';
        return 'var(--status-error)';
    };

    const getStatusLabel = () => {
        if (status === 'healthy') return 'Healthy';
        if (status === 'warning') return 'Needs Attention';
        return 'Critical';
    };

    return (
        <div className="card health-score-card">
            <div className="card-header">
                <h3 className="card-title">Team Health</h3>
                {trends && (
                    <div className={`trend-badge ${trends.health_score_change >= 0 ? 'positive' : 'negative'}`}>
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            {trends.health_score_change >= 0 ? (
                                <path d="M7 17l5-5 5 5M7 7l5 5 5-5" />
                            ) : (
                                <path d="M7 7l5 5 5-5M7 17l5-5 5 5" />
                            )}
                        </svg>
                        <span>{Math.abs(trends.health_score_change)}%</span>
                    </div>
                )}
            </div>

            <div className="health-score-content">
                <div className="score-ring-container">
                    <svg className="score-ring" viewBox="0 0 120 120">
                        <circle
                            className="ring-bg"
                            cx="60"
                            cy="60"
                            r="54"
                        />
                        <circle
                            className="ring-progress"
                            cx="60"
                            cy="60"
                            r="54"
                            style={{
                                strokeDasharray: circumference,
                                strokeDashoffset,
                                stroke: getStatusColor(),
                            }}
                        />
                    </svg>
                    <div className="score-value">
                        <span className="score-number">{animatedScore}</span>
                        <span className="score-label">/ 100</span>
                    </div>
                </div>

                <div
                    className="status-indicator"
                    style={{ '--status-color': getStatusColor() }}
                >
                    <span className="status-dot" style={{ background: getStatusColor() }}></span>
                    <span>{getStatusLabel()}</span>
                </div>
            </div>
        </div>
    );
}

export default HealthScoreCard;
