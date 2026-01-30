import HealthScoreCard from './HealthScoreCard';
import BottleneckList from './BottleneckList';
import MetricsGrid from './MetricsGrid';
import RecommendationPanel from './RecommendationPanel';
import TrendChart from './TrendChart';
import './Dashboard.css';

function Dashboard({ analysis, metrics, onRunAnalysis, isLoading }) {
    if (isLoading) {
        return (
            <div className="dashboard-loading">
                <div className="skeleton-grid">
                    <div className="skeleton-card large"></div>
                    <div className="skeleton-card"></div>
                    <div className="skeleton-card"></div>
                    <div className="skeleton-card wide"></div>
                </div>
            </div>
        );
    }

    return (
        <div className="dashboard">
            {/* Top Section - Health Score and Quick Stats */}
            <section className="dashboard-section dashboard-top">
                <div className="dashboard-grid grid-cols-3">
                    <HealthScoreCard
                        score={analysis?.health_score || 0}
                        status={analysis?.health_status || 'unknown'}
                        trend={analysis?.trends?.health_score_change}
                    />
                    <div className="quick-stats-grid">
                        <MetricsGrid metrics={metrics} />
                    </div>
                </div>
            </section>

            {/* Main Content - Bottlenecks and Recommendations */}
            <section className="dashboard-section">
                <div className="dashboard-grid grid-cols-2">
                    <div className="card bottlenecks-card">
                        <div className="card-header">
                            <h2 className="card-title">
                                🚨 Detected Bottlenecks
                                {analysis?.bottlenecks?.length > 0 && (
                                    <span className="badge">{analysis.bottlenecks.length}</span>
                                )}
                            </h2>
                        </div>
                        <BottleneckList bottlenecks={analysis?.bottlenecks || []} />
                    </div>

                    <div className="card recommendations-card">
                        <div className="card-header">
                            <h2 className="card-title">💡 AI Recommendations</h2>
                        </div>
                        <RecommendationPanel
                            recommendations={analysis?.recommendations || []}
                        />
                    </div>
                </div>
            </section>

            {/* Charts Section */}
            <section className="dashboard-section">
                <div className="dashboard-grid grid-cols-2">
                    <div className="card chart-card">
                        <div className="card-header">
                            <h2 className="card-title">📈 PR Review Distribution</h2>
                        </div>
                        <TrendChart
                            type="pie"
                            data={metrics?.github?.reviewer_distribution}
                            title="Reviews by Team Member"
                        />
                    </div>

                    <div className="card chart-card">
                        <div className="card-header">
                            <h2 className="card-title">⏱️ CI/CD Pipeline Health</h2>
                        </div>
                        <TrendChart
                            type="bar"
                            data={metrics?.cicd}
                            title="Pipeline Success Rate"
                        />
                    </div>
                </div>
            </section>

            {/* Improvement Tracking */}
            {analysis?.trends && (
                <section className="dashboard-section">
                    <div className="card improvements-card">
                        <div className="card-header">
                            <h2 className="card-title">📊 Week-over-Week Changes</h2>
                        </div>
                        <div className="improvements-grid">
                            <div className="improvement-item">
                                <span className="improvement-label">Health Score</span>
                                <span className={`improvement-value ${analysis.trends.health_score_change >= 0 ? 'positive' : 'negative'}`}>
                                    {analysis.trends.health_score_change >= 0 ? '↑' : '↓'}
                                    {Math.abs(analysis.trends.health_score_change)} points
                                </span>
                            </div>
                            <div className="improvement-item">
                                <span className="improvement-label">New Issues</span>
                                <span className="improvement-value neutral">
                                    {analysis.trends.new_bottlenecks} detected
                                </span>
                            </div>
                            <div className="improvement-item">
                                <span className="improvement-label">Resolved</span>
                                <span className="improvement-value positive">
                                    ✓ {analysis.trends.resolved_bottlenecks} fixed
                                </span>
                            </div>
                        </div>
                    </div>
                </section>
            )}
        </div>
    );
}

export default Dashboard;
