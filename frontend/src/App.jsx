import { useState, useEffect, useCallback } from 'react';
import './App.css';
import Dashboard from './components/Dashboard';
import LoadingOverlay from './components/LoadingOverlay';

const API_BASE = 'http://localhost:5001/api';

// SVG Icons as components
const Icons = {
    Search: () => (
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="11" cy="11" r="8" />
            <path d="m21 21-4.35-4.35" />
        </svg>
    ),
    Refresh: () => (
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M21 12a9 9 0 1 1-9-9c2.52 0 4.93 1 6.74 2.74L21 8" />
            <path d="M21 3v5h-5" />
        </svg>
    ),
    AlertCircle: () => (
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="12" cy="12" r="10" />
            <line x1="12" y1="8" x2="12" y2="12" />
            <line x1="12" y1="16" x2="12.01" y2="16" />
        </svg>
    ),
    X: () => (
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <line x1="18" y1="6" x2="6" y2="18" />
            <line x1="6" y1="6" x2="18" y2="18" />
        </svg>
    ),
};

function App() {
    const [analysis, setAnalysis] = useState(null);
    const [metrics, setMetrics] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);
    const [lastUpdated, setLastUpdated] = useState(null);

    const fetchMetrics = useCallback(async () => {
        try {
            const response = await fetch(`${API_BASE}/metrics`);
            if (!response.ok) throw new Error('Failed to fetch metrics');
            const data = await response.json();
            setMetrics(data);
        } catch (err) {
            console.error('Metrics fetch error:', err);
        }
    }, []);

    const runAnalysis = useCallback(async () => {
        setIsLoading(true);
        setError(null);

        try {
            const response = await fetch(`${API_BASE}/analyze`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ days: 30, save: true }),
            });

            if (!response.ok) throw new Error('Analysis failed');

            const data = await response.json();
            setAnalysis(data);
            setLastUpdated(new Date());
            await fetchMetrics();
        } catch (err) {
            setError(err.message);
            console.error('Analysis error:', err);
        } finally {
            setIsLoading(false);
        }
    }, [fetchMetrics]);

    useEffect(() => {
        const loadInitialData = async () => {
            setIsLoading(true);
            try {
                await fetchMetrics();
                const response = await fetch(`${API_BASE}/analyze/quick`);
                if (response.ok) {
                    const data = await response.json();
                    setAnalysis(data);
                    setLastUpdated(new Date());
                }
            } catch (err) {
                console.error('Initial load error:', err);
            } finally {
                setIsLoading(false);
            }
        };

        loadInitialData();

        // ⚡️ Auto-Polling (15s) to avoid congestion with Live AI
        const intervalId = setInterval(async () => {
            await fetchMetrics();
            // Also refresh quick analysis to update header stats
            try {
                const response = await fetch(`${API_BASE}/analyze/quick`);
                if (response.ok) {
                    const data = await response.json();
                    setAnalysis(data);
                    setLastUpdated(new Date());
                }
            } catch (e) { console.log("Polling error", e); }
        }, 2000);

        return () => clearInterval(intervalId); // Cleanup
    }, [fetchMetrics]);

    const formatTime = (date) => {
        return date.toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit',
            hour12: true
        });
    };

    return (
        <div className="app">
            <header className="header" style={{ justifyContent: 'flex-end', paddingRight: '2rem' }}>
                <div className="header-logo" style={{ flexDirection: 'row-reverse', textAlign: 'right' }}>
                    <div className="logo-icon" style={{ marginLeft: '1rem', marginRight: 0 }}>
                        <Icons.Search />
                    </div>
                    <div>
                        <h1>Silent Bottleneck Detector</h1>
                        <p className="last-updated">
                            {lastUpdated
                                ? `Updated ${formatTime(lastUpdated)}`
                                : 'Awaiting analysis'}
                        </p>
                    </div>
                </div>
            </header>

            {error && (
                <div className="error-banner">
                    <Icons.AlertCircle className="error-icon" />
                    <div className="error-content">
                        <strong>Analysis Error</strong>
                        <p>{error}</p>
                    </div>
                    <button className="btn-ghost" onClick={() => setError(null)}>
                        <Icons.X />
                    </button>
                </div>
            )}

            {isLoading && <LoadingOverlay />}

            <main>
                <Dashboard
                    analysis={analysis}
                    metrics={metrics}
                    onRunAnalysis={runAnalysis}
                    isLoading={isLoading}
                />
            </main>

            <footer className="footer">
                <p>Built for IBM watsonx Hackathon 2026</p>
                <p className="footer-tech">
                    Powered by watsonx.ai · watsonx Orchestrate · IBM Cloudant
                </p>
            </footer>
        </div>
    );
}

export default App;
