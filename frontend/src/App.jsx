import { useState, useEffect, useCallback } from 'react';
import './App.css';
import Dashboard from './components/Dashboard';
import LoadingOverlay from './components/LoadingOverlay';

const API_BASE = 'http://localhost:5001/api';

function App() {
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysis, setAnalysis] = useState(null);
  const [metrics, setMetrics] = useState(null);
  const [error, setError] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(null);

  // Fetch initial data
  const fetchData = useCallback(async () => {
    try {
      const [analysisRes, metricsRes] = await Promise.all([
        fetch(`${API_BASE}/analyze/quick`),
        fetch(`${API_BASE}/metrics`),
      ]);

      if (!analysisRes.ok || !metricsRes.ok) {
        throw new Error('Failed to fetch data');
      }

      const analysisData = await analysisRes.json();
      const metricsData = await metricsRes.json();

      setAnalysis(analysisData);
      setMetrics(metricsData);
      setLastUpdated(new Date());
      setError(null);
    } catch (err) {
      console.error('Error fetching data:', err);
      setError('Unable to connect to the backend. Make sure the Flask server is running on port 5000.');
    }
  }, []);

  // Run full analysis
  const runAnalysis = async () => {
    setIsAnalyzing(true);
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

      // Refresh metrics
      const metricsRes = await fetch(`${API_BASE}/metrics`);
      const metricsData = await metricsRes.json();
      setMetrics(metricsData);
    } catch (err) {
      console.error('Analysis error:', err);
      setError('Failed to run analysis. Please try again.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  // Initial load
  useEffect(() => {
    fetchData();
  }, [fetchData]);

  return (
    <div className="app">
      {isAnalyzing && <LoadingOverlay />}

      <header className="header">
        <div className="header-logo">
          <div className="logo-icon">🔍</div>
          <div>
            <h1>Silent Bottleneck Detector</h1>
            <p className="header-subtitle">AI-Powered Team Efficiency Analysis</p>
          </div>
        </div>

        <div className="header-actions">
          {lastUpdated && (
            <span className="last-updated">
              Last updated: {lastUpdated.toLocaleTimeString()}
            </span>
          )}
          <button
            className="btn btn-secondary"
            onClick={fetchData}
            disabled={isAnalyzing}
          >
            ↻ Refresh
          </button>
          <button
            className="btn btn-primary"
            onClick={runAnalysis}
            disabled={isAnalyzing}
          >
            {isAnalyzing ? (
              <>
                <span className="loading-spinner"></span>
                Analyzing...
              </>
            ) : (
              <>🔬 Run Analysis</>
            )}
          </button>
        </div>
      </header>

      {error ? (
        <div className="error-banner">
          <span className="error-icon">⚠️</span>
          <div className="error-content">
            <strong>Connection Error</strong>
            <p>{error}</p>
          </div>
          <button className="btn btn-ghost" onClick={fetchData}>
            Retry
          </button>
        </div>
      ) : (
        <Dashboard
          analysis={analysis}
          metrics={metrics}
          onRunAnalysis={runAnalysis}
          isLoading={!analysis}
        />
      )}

      <footer className="footer">
        <p>
          Built with <span className="heart">♥</span> for IBM watsonx Hackathon 2026
        </p>
        <p className="footer-tech">
          Powered by watsonx.ai • watsonx Orchestrate • Cloudant
        </p>
      </footer>
    </div>
  );
}

export default App;
