import './LoadingOverlay.css';

function LoadingOverlay() {
    const steps = [
        { icon: '📊', text: 'Collecting GitHub data...' },
        { icon: '📋', text: 'Analyzing Jira patterns...' },
        { icon: '💬', text: 'Processing Slack activity...' },
        { icon: '🔧', text: 'Evaluating CI/CD pipelines...' },
        { icon: '🤖', text: 'Running watsonx.ai analysis...' },
    ];

    return (
        <div className="loading-overlay">
            <div className="loading-content">
                <div className="loading-icon">🔍</div>
                <h2>Detecting Hidden Bottlenecks</h2>
                <div className="loading-steps">
                    {steps.map((step, i) => (
                        <div key={i} className="loading-step" style={{ animationDelay: `${i * 0.5}s` }}>
                            <span className="step-icon">{step.icon}</span>
                            <span className="step-text">{step.text}</span>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}

export default LoadingOverlay;
