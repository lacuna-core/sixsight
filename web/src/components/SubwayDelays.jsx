import { useMemo } from 'react'
import {
  BarChart, Bar, XAxis, YAxis, Tooltip,
  ResponsiveContainer, Cell,
} from 'recharts'
import { useCSV } from '../hooks/useCSV'

const COLORS = {
  total:  '#4c85c8',
  delays: '#38b87c',
  major:  '#e0622a',
}

function fmt(n) {
  return n.toLocaleString('en-CA')
}

function XTick({ x, y, payload }) {
  if (!payload.value?.startsWith('Jan')) return null
  return (
    <text x={x} y={y + 14} textAnchor="middle" fill="var(--text-3)" fontSize={11}>
      {payload.value.split(' ')[1]}
    </text>
  )
}

function YTick({ x, y, payload, formatter }) {
  return (
    <text x={x - 4} y={y + 4} textAnchor="end" fill="var(--text-3)" fontSize={11}>
      {formatter(payload.value)}
    </text>
  )
}

function ChartTooltip({ active, payload, label, formatter }) {
  if (!active || !payload?.length) return null
  return (
    <div className="tooltip">
      <div className="tooltip-label">{label}</div>
      <div className="tooltip-value">{formatter(payload[0].value)}</div>
    </div>
  )
}

function ChartCard({ data, dataKey, color, title, subtitle, yFormatter, tooltipFormatter }) {
  return (
    <div className="chart-card">
      <div className="chart-header">
        <div className="chart-title">{title}</div>
        <div className="chart-subtitle">{subtitle}</div>
      </div>
      <ResponsiveContainer width="100%" height={190}>
        <BarChart data={data} barSize={6} margin={{ top: 4, right: 16, left: 8, bottom: 0 }}>
          <XAxis
            dataKey="month_label"
            tick={<XTick />}
            axisLine={false}
            tickLine={false}
            interval={0}
            height={28}
          />
          <YAxis
            tick={<YTick formatter={yFormatter} />}
            axisLine={false}
            tickLine={false}
            width={48}
          />
          <Tooltip
            content={<ChartTooltip formatter={tooltipFormatter} />}
            cursor={{ fill: 'rgba(255,255,255,0.04)' }}
          />
          <Bar dataKey={dataKey} radius={[2, 2, 0, 0]}>
            {data.map((_, i) => (
              <Cell key={i} fill={color} fillOpacity={0.85} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
      <div className="chart-source">Source: City of Toronto Open Data — TTC Subway Delay Data</div>
    </div>
  )
}

function StatCard({ value, label, color }) {
  return (
    <div className="stat-card" style={{ '--stat-color': color }}>
      <div className="stat-value">{value}</div>
      <div className="stat-label">{label}</div>
    </div>
  )
}

export default function SubwayDelays() {
  const { data, loading, error } = useCSV(`${import.meta.env.BASE_URL}data/monthly.csv`)

  const chartData = useMemo(() => {
    if (!data) return []
    return data.map(row => ({
      ...row,
      total_delay_days: +(row.total_delay / 1440).toFixed(2),
    }))
  }, [data])

  const stats = useMemo(() => {
    if (!data?.length) return null
    const totalIncidents  = data.reduce((s, r) => s + r.delays, 0)
    const totalDelayDays  = Math.round(data.reduce((s, r) => s + r.total_delay, 0) / 1440)
    const totalMajor      = data.reduce((s, r) => s + r.major_delays, 0)
    const period = `${data[0].month_label} – ${data[data.length - 1].month_label}`
    return { totalIncidents, totalDelayDays, totalMajor, period }
  }, [data])

  return (
    <section className="section" id="subway-delays">
      <div className="container">
        <div className="section-header">
          <div className="section-label">Transit performance</div>
          <h2 className="section-title">TTC Subway Delays</h2>
          <p className="section-subtitle">
            Every logged delay on the TTC subway system, aggregated by month.
            A delay is any incident that holds a train beyond schedule; a major delay exceeds 20 minutes.
          </p>
        </div>

        {loading && <div className="loading">Loading data…</div>}
        {error   && <div className="loading">Failed to load data.</div>}

        {stats && (
          <div className="stats-row">
            <StatCard
              value={fmt(stats.totalIncidents)}
              label="Total incidents"
              color={COLORS.delays}
            />
            <StatCard
              value={`${fmt(stats.totalDelayDays)} days`}
              label="Cumulative delay"
              color={COLORS.total}
            />
            <StatCard
              value={fmt(stats.totalMajor)}
              label="Major delays (≥ 20 min)"
              color={COLORS.major}
            />
            <StatCard
              value={stats.period}
              label="Data coverage"
              color="var(--text-3)"
            />
          </div>
        )}

        {chartData.length > 0 && (
          <div className="charts">
            <ChartCard
              data={chartData}
              dataKey="total_delay_days"
              color={COLORS.total}
              title="Total Delay per Month"
              subtitle="Sum of all delay minutes, converted to days"
              yFormatter={v => `${v}d`}
              tooltipFormatter={v => `${v} days`}
            />
            <ChartCard
              data={chartData}
              dataKey="delays"
              color={COLORS.delays}
              title="Number of Incidents per Month"
              subtitle="Count of all logged delay events"
              yFormatter={v => fmt(v)}
              tooltipFormatter={v => `${fmt(v)} incidents`}
            />
            <ChartCard
              data={chartData}
              dataKey="major_delays"
              color={COLORS.major}
              title="Major Delays per Month  (≥ 20 min)"
              subtitle="Count of incidents with a delay of 20 minutes or more"
              yFormatter={v => fmt(v)}
              tooltipFormatter={v => `${fmt(v)} major delays`}
            />
          </div>
        )}
      </div>
    </section>
  )
}
