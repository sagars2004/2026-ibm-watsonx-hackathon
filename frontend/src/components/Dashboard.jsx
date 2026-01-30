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
                    <div className="severity-legend">
                        <div className="legend-item">
                            <span className="status-dot error"></span>
                            <span>High: {bottlenecks.filter(b => b.severity === 'high').length}</span>
                        </div>
                        <div className="legend-item">
                            <span className="status-dot warning"></span>
                            <span>Medium: {bottlenecks.filter(b => b.severity === 'medium').length}</span>
                        </div>
                        <div className="legend-item">
                            <span className="status-dot info"></span>
                            <span>Low: {bottlenecks.filter(b => b.severity === 'low').length}</span>
                        </div>
                    </div>
                </div>
                <TrendChart data={bottlenecks} />
            </div>

            <div className="dashboard-row dashboard-middle">
                <BottleneckList bottlenecks={bottlenecks} />
                <RecommendationPanel recommendations={recommendations} />
            </div>

            <div className="dashboard-row dashboard-bottom">
                <MetricsGrid metrics={metrics} />
            </div>
        </div>
    );
}

export default Dashboard;
