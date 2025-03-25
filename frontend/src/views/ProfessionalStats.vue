<template>
    <div>
        <ProfessionalNav />
        <div class="container-fluid py-4">
            <div class="d-flex justify-content-between align-items-center mb-4">
                <h4 class="mb-0 px-3">Dashboard Overview</h4>
            </div>

            <!-- <div class="bg-light mb-5">
                <div class="container-fluid">
                    <div class="row justify-content-center">
                        <div class="col-lg-12">
                            <div class="contact-card bg-white rounded-4 shadow-sm overflow-hidden">
                                <div class="row g-0">
                                    <div class="col-md-3 bg-secondary bg-gradient d-flex align-items-center justify-content-center p-4">
                                        <img v-if="userData.profile" :src="userData.profile" class="rounded-circle shadow-sm" alt="Profile Image">
                                    </div>
                                    <div class="col-md-9">
                                        <div class="card-body p-4">
                                            <div class="d-flex justify-content-between align-items-center mb-3">
                                                <h3 class="card-title mb-0 text-secondary fw-bold">{{ userData.name }}</h3>
                                                <span class="badge bg-secondary-subtle text-secondary px-3 py-2 rounded-pill">
                                                    {{ userData.service_name }}
                                                </span>
                                            </div>
                                            <p class="card-text text-muted mb-4">
                                                {{ userData.description }}
                                            </p>
                                            <div class="d-flex gap-3 mb-4">
                                                <button class="btn btn-secondary px-4 rounded-pill">
                                                    Rating
                                                </button>
                                                <div class="col-auto">
                                                    <div class="rate">
                                                        <span v-for="star in 5" :key="star" class="star" :class="{ 'filled': userData.rating >= star }">★</span>
                                                    </div>
                                                </div>
                                                <button class="btn btn-outline-secondary px-4 rounded-pill">
                                                    {{ userData.rating }}
                                                </button>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div> -->
  
            <div class="row">
                <div class="col-12">
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-center mb-4">
                            <div class="col-md-6 card border-0 shadow-sm px-4">
                                <h5 style="margin-top: 20px;text-align: center;" class="card-title mb-3">Monthly Revenue</h5>
                                <canvas ref="canvasRef1"></canvas>
                            </div>
                            <div class="col-md-6 card border-0 shadow-sm px-4">
                                <h5 style="margin-top: 20px;text-align: center;" class="card-title mb-3">Service Requests</h5>
                                <canvas ref="canvasRef2"></canvas>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.contact-card {
    transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
}
.contact-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 30px rgba(0,0,0,0.1);
}
.social-icon {
    transition: all 0.3s ease;
    cursor: pointer;
}
.social-icon:hover {
    transform: scale(1.2);
}
</style>


<script>
import ProfessionalNav from "@/components/ProfessionalNav.vue";
import { onMounted, ref, computed } from 'vue';
import axios from "axios";
import { useRoute } from 'vue-router';

export default {
    name: "ProfessionalStats",
    components: {
        ProfessionalNav,
    },
    setup() {
        const canvasRef1 = ref(null);
        const canvasRef2 = ref(null);
        const ref1Data = ref(null);
        const ref2Data = ref(null);

        const route = useRoute();  
        const profID = ref(null);
        const userData = ref({});
        
        const userID = computed(() => {
            return route.params.userID
        });
        
        // const adChartData = JSON.parse('{{ ref2Data | safe }}'); 

        const getProfID = async () => {
            try {
                const response = await axios.get(`http://localhost:5000/get-prof-id/${userID.value}`);
                profID.value = response.data.profID;
                getData();
            } 
            catch (err) {
                error.value = 'Could not fetch profID';
                showError.value = true;
            }
        };

        const getData = async () => {
            try {
                const response = await axios.get(`http://localhost:5000/api/prof-dash/${profID.value}`);
                userData.value = response.data;
                ref1Data.value = response.data.data1;
                console.log(response.data.data1)
                console.log(ref1Data.value)
                console.log(response.data)
                console.log(userData.value)
            } catch (err) {
                console.log(err)
            }
        };

        onMounted(() => {
            getProfID();

            const ctx1 = canvasRef1.value.getContext('2d');
            const ctx2 = canvasRef2.value.getContext('2d');

            // 'rgb(75, 192, 192)'

            new Chart(ctx1, {
                type: 'line',
                data: {
                    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                    datasets: [{
                        label: 'Revenue',
                        data: [5000, 7000, 6500, 8000, 9500, 11000, 12000, 11500, 13000, 14500, 13500, 15000],
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
                type: 'bar',
                data: {
                    labels: ['Pending', 'Accepted', 'Rejected', 'Closed'],
                    datasets: [{
                        label: 'Service Request Status',
                        backgroundColor: "#4e73df",
                        hoverBackgroundColor: "#2e59d9",
                        borderColor: "#4e73df",
                        data: [1, 2, 3, 4],
                    }],
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        });

        return {
            userData,
            canvasRef1,
            canvasRef2
        };
    }
};
</script>