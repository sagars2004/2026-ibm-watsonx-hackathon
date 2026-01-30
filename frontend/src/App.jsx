import { useState, useEffect, useCallback } from 'react';
import './App.css';
import Dashboard from './components/Dashboard';
import LoadingOverlay from './components/LoadingOverlay';

const API_BASE = 'http://localhost:5001/api';

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
    }, [fetchMetrics]);

    return (
        <div className="app">
            <header className="header">
                <div className="header-logo">
                    <div className="logo-icon">🔍</div>
                    <div>
                        <h1>Silent Bottleneck Detector</h1>
                        <p className="last-updated">
                            {lastUpdated
                                ? `Last updated: ${lastUpdated.toLocaleTimeString()}`
                                : 'Not yet analyzed'}
                        </p>
                    </div>
                </div>
                <div className="header-actions">
                    <button
                        className="btn btn-primary"
                        onClick={runAnalysis}
                        disabled={isLoading}
                    >
                        {isLoading ? (
                            <>
                                <span className="loading-spinner"></span>
                                Analyzing...
                            </>
                        ) : (
                            <>🔄 Run Analysis</>
                        )}
                    </button>
                </div>
            </header>

            {error && (
                <div className="error-banner">
                    <span className="error-icon">⚠️</span>
                    <div className="error-content">
                        <strong>Analysis Error</strong>
                        <p>{error}</p>
                    </div>
                    <button className="btn btn-ghost" onClick={() => setError(null)}>
                        ✕
                    </button>
                </div>
            )}

            {isLoading && <LoadingOverlay />}

            <main>
                <Dashboard analysis={analysis} metrics={metrics} />
            </main>

            <footer className="footer">
                <p>
                    Built with <span className="heart">❤️</span> for the IBM watsonx
                    Hackathon 2026
                </p>
                <p className="footer-tech">
                    Powered by watsonx.ai • watsonx Orchestrate • Cloudant
                </p>
            </footer>
        </div>
    );
}

export default App;
