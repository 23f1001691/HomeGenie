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
          <div class="card border-0 shadow-sm">
            <div class="card-body">
              <div class="d-flex justify-content-between align-items-center mb-4">
                <div class="col-md-6 card border-0 shadow-sm">
                    <h5 style="margin-top: 20px;text-align: center;" class="card-title mb-0">Overall Distribution</h5>
                    <!-- <canvas id="chart1" ref="canvasRef1"></canvas> -->
                </div>
                <div class="col-md-6 card border-0 shadow-sm">
                    <h5 style="margin-top: 20px;text-align: center;" class="card-title mb-0">Service Requests</h5>
                    <!-- <canvas id="chart2" ref="canvasRef2"></canvas> -->
                </div>
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

export default {
  name: "AdminDashboard",
  components: {
    AdminNav,
  },
};
</script>
