import './LoadingOverlay.css';

const steps = [
    { label: 'Collecting GitHub data', icon: 'git' },
    { label: 'Analyzing Jira patterns', icon: 'ticket' },
    { label: 'Processing Slack activity', icon: 'message' },
    { label: 'Evaluating CI/CD pipelines', icon: 'pipeline' },
    { label: 'Running AI analysis', icon: 'cpu' },
];

const StepIcon = ({ type }) => {
    const icons = {
        git: (
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                <circle cx="12" cy="12" r="3" />
                <path d="M12 3v6m0 6v6" />
                <path d="M6 9a3 3 0 1 0 0-6 3 3 0 0 0 0 6z" />
                <path d="M6 6h6" />
            </svg>
        ),
        ticket: (
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                <rect x="3" y="5" width="18" height="14" rx="2" />
                <path d="M7 10h10M7 14h4" />
            </svg>
        ),
        message: (
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z" />
            </svg>
        ),
        pipeline: (
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                <path d="M22 12h-4l-3 9L9 3l-3 9H2" />
            </svg>
        ),
        cpu: (
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                <rect x="4" y="4" width="16" height="16" rx="2" />
                <rect x="9" y="9" width="6" height="6" />
                <path d="M9 1v3M15 1v3M9 20v3M15 20v3M20 9h3M20 14h3M1 9h3M1 14h3" />
            </svg>
        ),
    };
    return icons[type] || null;
};

function LoadingOverlay() {
    return (
        <div className="loading-overlay">
            <div className="loading-content">
                <div className="loading-pulse">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                        <circle cx="11" cy="11" r="8" />
                        <path d="m21 21-4.35-4.35" />
                    </svg>
                </div>
                <h2>Detecting Bottlenecks</h2>
                <p className="loading-subtitle">Analyzing workflow patterns across your team</p>
                <div className="loading-steps">
                    {steps.map((step, i) => (
                        <div
                            key={i}
                            className="loading-step"
                            style={{ animationDelay: `${i * 0.4}s` }}
                        >
                            <div className="step-icon">
                                <StepIcon type={step.icon} />
                            </div>
                            <span>{step.label}</span>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}

export default LoadingOverlay;
