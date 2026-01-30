import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import './TrendChart.css';

const COLORS = ['#6366f1', '#8b5cf6', '#a855f7', '#3b82f6', '#10b981', '#f59e0b'];

function TrendChart({ type, data, title }) {
    // Generate mock chart data if not provided
    const chartData = generateChartData(type, data);

    if (type === 'pie') {
        return (
            <div className="chart-wrapper">
                <ResponsiveContainer width="100%" height={250}>
                    <PieChart>
                        <Pie
                            data={chartData}
                            cx="50%"
                            cy="50%"
                            innerRadius={60}
                            outerRadius={90}
                            paddingAngle={2}
                            dataKey="value"
                            label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                            labelLine={false}
                        >
                            {chartData.map((entry, index) => (
                                <Cell
                                    key={`cell-${index}`}
                                    fill={COLORS[index % COLORS.length]}
                                    style={{ filter: 'drop-shadow(0 0 4px rgba(99, 102, 241, 0.3))' }}
                                />
                            ))}
                        </Pie>
                        <Tooltip
                            contentStyle={{
                                background: '#1a1a25',
                                border: '1px solid rgba(148, 163, 184, 0.1)',
                                borderRadius: '8px',
                                color: '#f8fafc',
                            }}
                        />
                        <Legend
                            verticalAlign="bottom"
                            height={36}
                            formatter={(value) => <span style={{ color: '#94a3b8' }}>{value}</span>}
                        />
                    </PieChart>
                </ResponsiveContainer>
            </div>
        );
    }

    if (type === 'bar') {
        return (
            <div className="chart-wrapper">
                <ResponsiveContainer width="100%" height={250}>
                    <BarChart data={chartData} barSize={30}>
                        <XAxis
                            dataKey="name"
                            axisLine={false}
                            tickLine={false}
                            tick={{ fill: '#94a3b8', fontSize: 12 }}
                        />
                        <YAxis
                            axisLine={false}
                            tickLine={false}
                            tick={{ fill: '#94a3b8', fontSize: 12 }}
                        />
                        <Tooltip
                            contentStyle={{
                                background: '#1a1a25',
                                border: '1px solid rgba(148, 163, 184, 0.1)',
                                borderRadius: '8px',
                                color: '#f8fafc',
                            }}
                            cursor={{ fill: 'rgba(99, 102, 241, 0.1)' }}
                        />
                        <Bar
                            dataKey="success"
                            name="Success"
                            fill="#10b981"
                            radius={[4, 4, 0, 0]}
                        />
                        <Bar
                            dataKey="failed"
                            name="Failed"
                            fill="#ef4444"
                            radius={[4, 4, 0, 0]}
                        />
                        <Legend
                            verticalAlign="top"
                            height={36}
                            formatter={(value) => <span style={{ color: '#94a3b8' }}>{value}</span>}
                        />
                    </BarChart>
                </ResponsiveContainer>
            </div>
        );
    }

    return <div className="chart-placeholder">Chart not available</div>;
}

function generateChartData(type, data) {
    if (type === 'pie') {
        // PR Review distribution mock data
        return [
            { name: 'Sarah', value: 78 },
            { name: 'Mike', value: 12 },
            { name: 'Alex', value: 5 },
            { name: 'Emma', value: 3 },
            { name: 'Others', value: 2 },
        ];
    }

    if (type === 'bar') {
        // CI/CD pipeline data mock
        return [
            { name: 'Mon', success: 8, failed: 3 },
            { name: 'Tue', success: 10, failed: 4 },
            { name: 'Wed', success: 7, failed: 5 },
            { name: 'Thu', success: 9, failed: 2 },
            { name: 'Fri', success: 6, failed: 6 },
            { name: 'Sat', success: 3, failed: 1 },
            { name: 'Sun', success: 2, failed: 0 },
        ];
    }

    return [];
}

export default TrendChart;
