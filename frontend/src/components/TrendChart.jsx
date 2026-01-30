import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts';
import './TrendChart.css';

const COLORS = ['#ef4444', '#f59e0b', '#3b82f6'];

function TrendChart({ data }) {
    const chartData = [
        { name: 'High', value: data?.filter((b) => b.severity === 'high').length || 0 },
        { name: 'Medium', value: data?.filter((b) => b.severity === 'medium').length || 0 },
        { name: 'Low', value: data?.filter((b) => b.severity === 'low').length || 0 },
    ].filter((d) => d.value > 0);

    if (chartData.length === 0) {
        return (
            <div className="card trend-chart">
                <div className="card-header">
                    <h3 className="card-title">Severity Distribution</h3>
                </div>
                <div className="empty-state">
                    <p>No data to display</p>
                </div>
            </div>
        );
    }

    return (
        <div className="card trend-chart">
            <div className="card-header">
                <h3 className="card-title">Severity Distribution</h3>
            </div>
            <div className="chart-container">
                <ResponsiveContainer width="100%" height={150}>
                    <PieChart>
                        <Pie
                            data={chartData}
                            cx="50%"
                            cy="50%"
                            innerRadius={40}
                            outerRadius={60}
                            paddingAngle={5}
                            dataKey="value"
                        >
                            {chartData.map((entry, index) => (
                                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                            ))}
                        </Pie>
                        <Tooltip
                            contentStyle={{
                                background: 'var(--bg-card)',
                                border: '1px solid var(--border-color)',
                                borderRadius: 'var(--radius-md)',
                                color: 'var(--text-primary)',
                            }}
                        />
                    </PieChart>
                </ResponsiveContainer>
                <div className="chart-legend">
                    {chartData.map((entry, index) => (
                        <div key={entry.name} className="legend-item">
                            <span className="legend-color" style={{ background: COLORS[index] }}></span>
                            <span>{entry.name}</span>
                            <span className="legend-value">{entry.value}</span>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}

export default TrendChart;
