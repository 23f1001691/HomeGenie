<template>
    <div>
        <ProfessionalNav />
        <div class="container-fluid py-4">
            <div class="d-flex justify-content-between align-items-center mb-4">
                <h4 class="mb-0 px-3">Dashboard Overview</h4>
            </div>

            <div class="bg-light mb-5" v-if="userData">
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
                                                <button class="btn px-4">
                                                    {{ userData.rating }}
                                                </button>
                                            </div>
                                            <div class="d-flex gap-3 mb-4">
                                                <button class="btn btn-secondary px-4 rounded-pill">
                                                    Income Earned
                                                </button>
                                                <button class="btn px-4">
                                                    {{ userData.income }}
                                                </button>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div> 
  
            <div class="row">
                <div class="col-12">
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-center mb-4">
                            <div class="col-md-6 card border-0 shadow-sm px-4 pb-4">
                                <h5 style="margin-top: 20px;text-align: center;" class="card-title mb-4">Monthly Revenue</h5>
                                <Error :showError="showError1" :title="errorTitle" :content="errorContent" errorHeight="285" />
                                <canvas ref="canvasRef1" v-if="!showError1"></canvas>
                            </div>
                            <div class="col-md-6 card border-0 shadow-sm px-4 pb-4">
                                <h5 style="margin-top: 20px;text-align: center;" class="card-title mb-4">Service Requests</h5>
                                <Error :showError="showError2" :title="errorTitle" :content="errorContent" errorHeight="285" />
                                <canvas ref="canvasRef2" v-if="!showError2"></canvas>
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
import { onMounted, ref, computed, watch } from 'vue';
import axios from "axios";
import { useRoute } from 'vue-router';
import Error from '@/components/Error.vue';

export default {
    name: "ProfessionalStats",
    components: {
        ProfessionalNav,
        Error
    },
    setup() {
        const canvasRef1 = ref(null);
        const canvasRef2 = ref(null);
        const ref1Data = ref(null);
        const ref2Data = ref(null);

        const route = useRoute();  
        const profID = ref(null);
        const userData = ref({});

        const showError1 = ref(false)
        const showError2 = ref(false)

        const errorTitle = ref("Sorry!")
        const errorContent = ref("No data available right now.")
        
        const userID = computed(() => {
            return route.params.userID
        });

        const getProfID = async () => {
            try {
                const response = await axios.get(`http://localhost:5000/get-prof-id/${userID.value}`);
                profID.value = response.data.profID;
                getData();
            } 
            catch (err) {
                console.log(err)
            }
        };

        watch(ref1Data, (newData) => {
            showError1.value = newData.every(item => item === 0);
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
                type: 'bar',
                data: {
                    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                    datasets: [{
                        label: 'Revenue',
                        backgroundColor: "#4e73df",
                        hoverBackgroundColor: "#2e59d9",
                        borderColor: "#4e73df",
                        data: ref1Data.value
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
                type: 'doughnut',
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
                const response = await axios.get(`http://localhost:5000/api/prof-dash/${profID.value}`);
                userData.value = response.data;
                ref1Data.value = response.data.rev_data;
                ref2Data.value = response.data.req_data
                console.log(response.data.rev_data, response.data.req_data)
                console.log(ref1Data.value, ref2Data.value)
                getCharts();
            } 
            catch (err) {
                console.log(err)
            }
        };

        onMounted(() => {
            getProfID();
        });

        return {
            userData,
            canvasRef1,
            canvasRef2,
            showError2,
            showError1,
            errorContent,
            errorTitle
        };
    }
};
</script>