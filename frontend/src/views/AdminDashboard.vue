<template>
  <div>
    <AdminNav />

    <div class="container-fluid py-4">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h4 class="mb-0">Dashboard Overview</h4>
      </div>

      <div class="row g-4">
        <div class="col-12 col-md-6 col-lg-3">
          <div class="card stat-card border-0 shadow-sm">
            <div class="card-body">
              <div class="d-flex align-items-center mb-3">
                <div class="stat-icon bg-primary bg-opacity-10 text-primary">
                  <i class="fas fa-shopping-cart"></i>
                </div>
              </div>
              <h6 class="text-muted mb-2">Total Bookings</h6>
              <h4 class="mb-3">$24,589</h4>
            </div>
          </div>
        </div>

        <div class="col-12 col-md-6 col-lg-3">
          <div class="card stat-card border-0 shadow-sm">
            <div class="card-body">
              <div class="d-flex align-items-center mb-3">
                <div class="stat-icon bg-success bg-opacity-10 text-success">
                  <i class="fas fa-users"></i>
                </div>
              </div>
              <h6 class="text-muted mb-2">Active Users</h6>
              <h4 class="mb-3">14,789</h4>
            </div>
          </div>
        </div>

        <div class="col-12 col-md-6 col-lg-3">
          <div class="card stat-card border-0 shadow-sm">
            <div class="card-body">
              <div class="d-flex align-items-center mb-3">
                <div class="stat-icon bg-warning bg-opacity-10 text-warning">
                  <i class="fas fa-box"></i>
                </div>
              </div>
              <h6 class="text-muted mb-2">Running Services</h6>
              <h4 class="mb-3">1,589</h4>
            </div>
          </div>
        </div>

        <div class="col-12 col-md-6 col-lg-3">
          <div class="card stat-card border-0 shadow-sm">
            <div class="card-body">
              <div class="d-flex align-items-center mb-3">
                <div class="stat-icon bg-info bg-opacity-10 text-info">
                  <i class="fas fa-dollar-sign"></i>
                </div>
              </div>
              <h6 class="text-muted mb-2">Revenue</h6>
              <h4 class="mb-3">$45,289</h4>
            </div>
          </div>
        </div>
      </div>

      <!-- <div class="row mt-4">
          <div class="col-md-6 card border-0 shadow-sm">
              <h5 style="margin-top: 20px;text-align: center;" class="card-title mb-0">Overall Distribution</h5>
              <canvas id="chart1" ref="canvasRef1"></canvas>
          </div>
          <div class="col-md-6 card border-0 shadow-sm">
              <h5 style="margin-top: 20px;text-align: center;" class="card-title mb-0">Service Requests</h5>
              <canvas id="chart2" ref="canvasRef2"></canvas>
          </div>
      </div> -->

      <div class="row mt-4">
        <div class="col-12">
            <div class="card-body">
              <div class="d-flex justify-content-between align-items-center mb-4">
                <div class="col-md-6 card border-0 shadow-sm px-4">
                    <h5 style="margin-top: 20px;text-align: center;" class="card-title mb-0">Overall Distribution</h5>
                    <canvas ref="canvasRef1"></canvas>
                </div>
                <div class="col-md-6 card border-0 shadow-sm px-4">
                    <h5 style="margin-top: 20px;text-align: center;" class="card-title mb-0">Service Requests</h5>
                    <canvas ref="canvasRef2"></canvas>
                </div>
              </div>
            </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped></style>

<script>
import AdminNav from "@/components/AdminNav.vue";
import { onMounted, ref } from 'vue';
import axios from "axios";

export default {
  name: "AdminDashboard",
  components: {
    AdminNav,
  },
  setup() {
        const canvasRef1 = ref(null);
        const canvasRef2 = ref(null);
        const ref1Data = ref(null);
        const ref2Data = ref(null);
        // const adChartData = JSON.parse('{{ ref2Data | safe }}'); 

        const getServiceData = async () => {
            try {
                const response = await axios.get('http://localhost:5000/api/request-count');
                ref2Data.value = response.data;
                console.log(response.data)
            } catch (err) {
                // error.value = err.response?.data?.message || err.message;
                // showError.value = true;
            }
        };

        onMounted(() => {

            getServiceData();

            const ctx1 = canvasRef1.value.getContext('2d');
            const ctx2 = canvasRef2.value.getContext('2d');

            const barData = {
                labels: ['Pending', 'Accepted', 'Rejected', 'Closed'],
                datasets: [{
                    label: 'Service Request Status',
                    data: [1, 2, 3, 4, 5],
                    backgroundColor: ['rgba(255, 159, 64, 0.2)', 'rgba(54, 162, 235, 0.2)', 'rgba(75, 192, 192, 0.2)'],
                    borderColor: ['rgba(255, 159, 64, 1)', 'rgba(54, 162, 235, 1)', 'rgba(75, 192, 192, 1)'],
                    borderWidth: 1
                }]
            };

            new Chart(ctx1, {
                type: 'bar',
                data: barData,
                options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });

            // new Chart(ctx2, {
            //     type: 'bar',
            //     data: barData,
            //     options: {
            //         scales: {
            //             y: {
            //                 beginAtZero: true
            //             }
            //         }
            //     }
            // });

            new Chart(ctx2, {
                type: 'bar',
                data: {
                    labels: ["January", "February", "March", "April", "May", "June"],
                    datasets: [{
                        label: "Revenue",
                        backgroundColor: "#4e73df",
                        hoverBackgroundColor: "#2e59d9",
                        borderColor: "#4e73df",
                        data: [4215, 5312, 6251, 7841, 9821, 14984],
                    }],
                },
                options: {
                    // maintainAspectRatio: false,
                    layout: {
                        padding: {
                            left: 10,
                            right: 25,
                            top: 25,
                            bottom: 0
                        }
                    },
                    scales: {
                        // y: {
                        //     beginAtZero: true
                        // },
                        xAxes: [{
                            time: {
                                unit: 'month'
                            },
                            gridLines: {
                                display: false,
                                drawBorder: false
                            },
                            ticks: {
                                maxTicksLimit: 6
                            },
                            maxBarThickness: 25,
                        }],
                        yAxes: [{
                            ticks: {
                                min: 0,
                                max: 15000,
                                maxTicksLimit: 5,
                                padding: 10,
                                // Include a dollar sign in the ticks
                                callback: function (value, index, values) {
                                    return '$' + number_format(value);
                                }
                            },
                            gridLines: {
                                color: "rgb(234, 236, 244)",
                                zeroLineColor: "rgb(234, 236, 244)",
                                drawBorder: false,
                                borderDash: [2],
                                zeroLineBorderDash: [2]
                            }
                        }],
                    },
                    legend: {
                        display: false
                    },
                    tooltips: {
                        titleMarginBottom: 10,
                        titleFontColor: '#6e707e',
                        titleFontSize: 14,
                        backgroundColor: "rgb(255,255,255)",
                        bodyFontColor: "#858796",
                        borderColor: '#dddfeb',
                        borderWidth: 1,
                        xPadding: 15,
                        yPadding: 15,
                        displayColors: false,
                        caretPadding: 10,
                        callbacks: {
                            label: function (tooltipItem, chart) {
                                var datasetLabel = chart.datasets[tooltipItem.datasetIndex].label || '';
                                return datasetLabel + ': $' + number_format(tooltipItem.yLabel);
                            }
                        }
                    },
                }
            });

        });

        return {
            canvasRef1,
            canvasRef2
        };
    }
};
</script>
