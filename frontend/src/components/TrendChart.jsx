import { useMemo } from 'react';
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import './TrendChart.css';

function TrendChart({ data }) {
    // Generate simulated trend data based on bottleneck count
    const trendData = useMemo(() => {
        const points = [];
        const days = ['Mon', 'Tues', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun'];
        const baseScore = data?.length ? Math.max(30, 100 - data.length * 15) : 75;

        for (let i = 0; i < 7; i++) {
            // Deterministic "randomness" based on index
            const variance = ((i * 7 + 3) % 15) - 7;
            points.push({
                day: days[i],
                score: Math.max(0, Math.min(100, baseScore + variance + (i * 2))),
                issues: Math.max(0, (data?.length || 3)),
            });
        }
        return points;
    }, [data?.length]); // Only re-generate if number of bottlenecks changes

    const CustomTooltip = ({ active, payload, label }) => {
        if (active && payload && payload.length) {
            return (
                <div className="chart-tooltip">
                    <p className="tooltip-label">{label}</p>
                    <p className="tooltip-value">
                        Score: <strong>{payload[0].value}</strong>
                    </p>
                </div>
            );
        }
        return null;
    };

    return (
        <div className="card trend-chart">
            <div className="card-header">
                <h3 className="card-title">Weekly Trend</h3>
                <div className="chart-legend">
                    <span className="legend-dot"></span>
                    <span>Health Score</span>
                </div>
            </div>
            <div className="chart-container" style={{ height: "100%", flex: 1 }}>
                <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={trendData} margin={{ top: 5, right: 5, left: 0, bottom: 0 }}>
                        <defs>
                            <linearGradient id="scoreGradient" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor="var(--accent-blue)" stopOpacity={0.15} />
                                <stop offset="95%" stopColor="var(--accent-blue)" stopOpacity={0} />
                            </linearGradient>
                        </defs>
                        <XAxis
                            dataKey="day"
                            axisLine={false}
                            tickLine={false}
                            tick={{ fill: 'var(--text-muted)', fontSize: 11 }}
                        />
                        <YAxis
                            domain={[0, 100]}
                            axisLine={false}
                            tickLine={false}
                            tick={{ fill: 'var(--text-muted)', fontSize: 11, dx: -5 }}
                            width={40}
                        />
                        <Tooltip content={<CustomTooltip />} />
                        <Area
                            type="monotone"
                            dataKey="score"
                            stroke="var(--accent-blue)"
                            strokeWidth={2}
                            fill="url(#scoreGradient)"
                        />
                    </AreaChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
}

export default TrendChart;
