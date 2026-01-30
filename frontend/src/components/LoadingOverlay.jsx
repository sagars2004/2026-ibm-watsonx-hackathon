import './LoadingOverlay.css';

function LoadingOverlay() {
    return (
        <div className="loading-overlay">
            <div className="loading-content">
                <div className="loading-animation">
                    <div className="loading-ring"></div>
                    <div className="loading-icon">🔍</div>
                </div>
                <h2 className="loading-title">Analyzing Team Patterns</h2>
                <p className="loading-text">
                    Scanning GitHub, Jira, Slack, and CI/CD data...
                </p>
                <div className="loading-steps">
                    <div className="loading-step active">
                        <span className="step-icon">📊</span>
                        <span>Collecting data</span>
                    </div>
                    <div className="loading-step">
                        <span className="step-icon">🤖</span>
                        <span>AI analysis with watsonx</span>
                    </div>
                    <div className="loading-step">
                        <span className="step-icon">💡</span>
                        <span>Generating insights</span>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default LoadingOverlay;
