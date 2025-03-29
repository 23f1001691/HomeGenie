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
              <h4 class="mb-3">{{ total_bookings }}</h4>
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
              <h4 class="mb-3">{{ active_users }}</h4>
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
              <h4 class="mb-3">{{ running_services }}</h4>
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
              <h4 class="mb-3">{{ revenue }}</h4>
            </div>
          </div>
        </div>
      </div>

      <div class="row mt-4">
        <div class="col-12">
            <div class="card-body">
              <div class="d-flex justify-content-between align-items-center mb-4">
                <div class="col-md-6 card border-0 shadow-sm px-4 pb-4">
                    <h5 style="margin-top: 20px;text-align: center;" class="card-title mb-4">Revenue By Services</h5>
                    <Error :showError="showError1" :title="errorTitle" :content="errorContent" errorHeight="287" />
                    <canvas ref="canvasRef1" v-if="!showError1"></canvas>
                </div>
                <div class="col-md-6 card border-0 shadow-sm px-4 pb-4">
                    <h5 style="margin-top: 20px;text-align: center;" class="card-title mb-4">Service Requests</h5>
                    <Error :showError="showError2" :title="errorTitle" :content="errorContent" errorHeight="287" />
                    <canvas ref="canvasRef2" v-if="!showError2"></canvas>
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
import { onMounted, ref, watch, computed } from 'vue';
import axios from "axios";
import Error from '@/components/Error.vue';

export default {
  name: "AdminDashboard",
  components: {
    AdminNav,
    Error
  },
  setup() {
        const canvasRef1 = ref(null);
        const canvasRef2 = ref(null);

        const total_bookings = ref(null);
        const revenue = ref(null);
        const running_services = ref(null);
        const active_users = ref(null);

        const ref1Data = ref(null);
        const ref2Data = ref(null);

        const showError1 = ref(false)
        const showError2 = ref(false)

        const errorTitle = ref("Sorry!")
        const errorContent = ref("No data available right now.")

        watch(ref1Data, (newData) => {
            showError1.value = newData.values.every(item => item === 0);
            console.log(showError1.value)
        });

        watch(ref2Data, (newData) => {
            showError2.value = newData.every(item => item === 0);
            console.log(showError2.value)
        });

        const getCharts = () => {
            const ctx1 = canvasRef1.value.getContext('2d');
            const ctx2 = canvasRef2.value.getContext('2d');

            new Chart(ctx1, {
                type: 'line',
                data: {
                    labels: ref1Data.value.labels,
                    datasets: [{
                        label: 'Revenue',
                        data: ref1Data.value.values,
                        borderColor: '#4e73df',
                        tension: 0.1
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });

            new Chart(ctx2, {
                type: 'pie',
                data: {
                    labels: ['Pending', 'Accepted', 'Rejected', 'Closed'],
                    datasets: [{
                        data: ref2Data.value,
                        backgroundColor: [
                            'rgb(255, 99, 132)',
                            'rgb(54, 162, 235)',
                            'rgb(255, 206, 86)',
                            'rgb(75, 192, 192)',
                        ]
                    }]
                },
                options: {
                    aspectRatio: 2,
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'right',
                        }
                    }
                }
            });
        }

        const getData = async () => {
            try {
                const response = await axios.get('http://localhost:5000/api/admin-dash');
                total_bookings.value = response.data.total_bookings;
                revenue.value = response.data.revenue;
                running_services.value = response.data.running_services;
                active_users.value = response.data.active_users;
                ref1Data.value = response.data.rev_data;
                ref2Data.value = response.data.req_data;
                console.log(ref1Data.value)
                console.log(ref2Data.value)
                getCharts();
            } 
            catch (err) {
                console.log(err)
            }
        };

        onMounted(() => {

            getData();

        });

        return {
            total_bookings,
            revenue,
            running_services,
            active_users,
            canvasRef1,
            canvasRef2,
            errorTitle,
            errorContent,
            showError1,
            showError2
        };
    }
};
</script>
