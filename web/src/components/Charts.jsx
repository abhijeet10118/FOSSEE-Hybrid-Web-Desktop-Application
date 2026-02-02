import React from 'react'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
} from 'chart.js'
import { Bar, Doughnut } from 'react-chartjs-2'

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
)

const CHART_COLORS = [
  '#58a6ff',
  '#3fb950',
  '#d29922',
  '#f85149',
  '#a371f7',
  '#79c0ff',
  '#7ee787',
  '#ffa657',
]

export default function Charts({ summary, rawData }) {
  if (!summary) return null

  const { type_distribution, averages } = summary

  const typeLabels = type_distribution ? Object.keys(type_distribution) : []
  const typeValues = type_distribution ? Object.values(type_distribution) : []

  const doughnutData = {
    labels: typeLabels,
    datasets: [
      {
        data: typeValues,
        backgroundColor: CHART_COLORS.slice(0, typeLabels.length),
        borderWidth: 0,
      },
    ],
  }

  const avgLabels = averages ? Object.keys(averages) : []
  const avgValues = averages ? Object.values(averages).map(Number) : []

  const barData = {
    labels: avgLabels,
    datasets: [
      {
        label: 'Average value',
        data: avgValues,
        backgroundColor: CHART_COLORS[0],
      },
    ],
  }

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { position: 'top' },
    },
    scales: {
      y: { beginAtZero: true },
    },
  }

  const doughnutOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { position: 'right' },
    },
  }

  return (
    <section className="charts-section">
      <h2>Charts</h2>
      <div className="charts-grid">
        {typeLabels.length > 0 && (
          <div className="chart-box">
            <h3>Equipment type distribution</h3>
            <div className="chart-container">
              <Doughnut data={doughnutData} options={doughnutOptions} />
            </div>
          </div>
        )}
        {avgLabels.length > 0 && (
          <div className="chart-box">
            <h3>Parameter averages</h3>
            <div className="chart-container">
              <Bar data={barData} options={chartOptions} />
            </div>
          </div>
        )}
      </div>
    </section>
  )
}
