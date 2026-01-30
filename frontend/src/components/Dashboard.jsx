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
                <div className="empty-state-icon">🔍</div>
                <h3>No Analysis Yet</h3>
                <p>Click "Run Analysis" to detect bottlenecks in your workflow</p>
            </div>
        );
    }

    const bottlenecks = analysis?.bottlenecks || [];
    const recommendations = analysis?.recommendations || [];

    return (
        <div className="dashboard">
            {/* Top section */}
            <div className="dashboard-top dashboard-grid grid-cols-3">
                <HealthScoreCard
                    score={analysis?.health_score || 0}
                    status={analysis?.health_status || 'unknown'}
                    trends={analysis?.trends}
                />
                <div className="card bottleneck-summary">
                    <div className="card-header">
                        <h3 className="card-title">Bottlenecks Detected</h3>
                        <span className="bottleneck-count">{bottlenecks.length}</span>
                    </div>
                    <div className="severity-breakdown">
                        <div className="severity-item high">
                            <span className="severity-dot"></span>
                            <span>High: {bottlenecks.filter(b => b.severity === 'high').length}</span>
                        </div>
                        <div className="severity-item medium">
                            <span className="severity-dot"></span>
                            <span>Medium: {bottlenecks.filter(b => b.severity === 'medium').length}</span>
                        </div>
                        <div className="severity-item low">
                            <span className="severity-dot"></span>
                            <span>Low: {bottlenecks.filter(b => b.severity === 'low').length}</span>
                        </div>
                    </div>
                </div>
                <TrendChart data={bottlenecks} />
            </div>

            {/* Middle section */}
            <div className="dashboard-middle dashboard-grid grid-cols-2">
                <BottleneckList bottlenecks={bottlenecks} />
                <RecommendationPanel recommendations={recommendations} />
            </div>

            {/* Bottom section */}
            <div className="dashboard-bottom">
                <MetricsGrid metrics={metrics} />
            </div>
        </div>
    );
}

export default Dashboard;
