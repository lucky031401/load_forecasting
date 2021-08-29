<script>
import { Line } from 'vue-chartjs'

export default {
  extends: Line,
  mounted() {
    const dates = [
      '2020/07/05',
      '2020/07/06',
      '2020/07/07',
      '2020/07/08',
      '2020/07/09',
      '2020/07/10',
    ]
    const totals = [50, 40, 71, 51, 25, 49]

    this.renderChart({
      labels: dates,
      datasets: [
        {
          label: 'demo',
          data: totals,
        },
      ],
    },
    {
      responsive: true,
      maintainAspectRatio: false,
    })
  },
}
</script>