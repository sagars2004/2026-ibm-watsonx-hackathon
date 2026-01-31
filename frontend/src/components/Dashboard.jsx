import './Dashboard.css';
import HealthScoreCard from './HealthScoreCard';
import BottleneckList from './BottleneckList';
import MetricsGrid from './MetricsGrid';
import RecommendationPanel from './RecommendationPanel';
import TrendChart from './TrendChart';

function Dashboard({ analysis, metrics }) {
    if (!analysis && !metrics) {
        return (
            <div className="empty-state">
                <svg className="empty-state-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1">
                    <circle cx="11" cy="11" r="8" />
                    <path d="m21 21-4.35-4.35" />
                </svg>
                <h3>No Analysis Data</h3>
                <p>Click "Run Analysis" to detect bottlenecks in your workflow</p>
            </div>
        );
    }

    const bottlenecks = analysis?.bottlenecks || [];
    const recommendations = analysis?.recommendations || [];

    return (
        <div className="dashboard">
            <div style={{ marginBottom: '1rem' }}>
                <h2 style={{ fontSize: '1.5rem', fontWeight: '500', color: 'var(--text-primary)' }}>
                    Hello, Sagar... Good luck in the 2026 IBM AI Demystified Hackathon!
                </h2>
            </div>

            <div className="dashboard-row dashboard-top">
                <HealthScoreCard
                    score={analysis?.health_score || 0}
                    status={analysis?.health_status || 'unknown'}
                    trends={analysis?.trends}
                />
                <div className="card summary-card">
                    <div className="card-header">
                        <h3 className="card-title">Analysis Summary</h3>
                    </div>
                    <div className="summary-stats">
                        <div className="summary-stat">
                            <span className="stat-number">{bottlenecks.length}</span>
                            <span className="stat-label">Issues Detected</span>
                        </div>
                        <div className="summary-stat">
                            <span className="stat-number">{bottlenecks.filter(b => b.severity === 'high').length}</span>
                            <span className="stat-label">High Priority</span>
                        </div>
                        <div className="summary-stat">
                            <span className="stat-number">{recommendations.length}</span>
                            <span className="stat-label">Recommendations</span>
                        </div>
                    </div>

                    {/* Predictive Modeling View */}
                    {analysis?.predictions && (
                        <div style={{ marginTop: 'auto', borderTop: '1px solid var(--border-subtle)', paddingTop: '1rem' }}>
                            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontWeight: '600', fontSize: '0.9rem' }}>

                                    <span>Project Forecast</span>
                                </div>
                                <span className={`badge ${analysis.predictions.risk_level === 'low' ? 'success' : 'warning'}`} style={{ fontSize: '0.75rem' }}>
                                    {analysis.predictions.risk_level === 'low' ? 'On Track' : 'At Risk'}
                                </span>
                            </div>
                            <div style={{ fontSize: '1.25rem', fontWeight: '700', color: 'var(--text-primary)' }}>
                                {analysis.predictions.days_to_completion} Days
                            </div>
                            <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                                to completion at current velocity ({analysis.predictions.projected_velocity} pts/sprint)
                            </div>
                        </div>
                    )}
                </div>
                <TrendChart data={bottlenecks} />
            </div>

            <div className="dashboard-row dashboard-bottom">
                <MetricsGrid metrics={metrics} />
            </div>

            <div className="dashboard-row dashboard-middle">
                <BottleneckList bottlenecks={bottlenecks} />
                <RecommendationPanel recommendations={recommendations} />
            </div>
        </div >
    );
}

export default Dashboard;
