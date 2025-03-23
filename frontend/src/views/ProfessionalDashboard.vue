<template>
    <div>
        <ProfessionalNav />

        <div class="alert alert-danger" role="alert" v-if="showError">
            {{ error }}
        </div>
        <div class="alert alert-success" role="alert" v-if="showMessage">
            {{ message }}
        </div>

        <div class="table-responsive m-3" v-if="pendingServices.length">
            <h4>SERVICE REQUESTS</h4>
            <table class="table table-hover table-bordered">
                <thead>
                    <tr>
                        <th scope="col" width="20%">ID</th>
                        <th scope="col" width="20%">Customer Name</th>
                        <th scope="col" width="20%">Phone Number</th>
                        <th scope="col" width="20%">Location (PINCODE)</th>
                        <th scope="col" width="20%">Action</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="request in pendingServices" :key="request.id">
                        <td scope="row">{{ request.id }}</td>
                        <td>{{ request.customer_name }}</td>
                        <td>{{ request.customer_no }}</td>
                        <td>{{ request.customer_pincode }}</td>
                        <td>
                            <div class="btn-group" role="group">
                                <button type="button" class="btn btn-success btn-sm" @click="acceptRequest(request.id)">
                                    Accept
                                </button>
                                <button type="button" class="btn btn-danger btn-sm" @click="rejectRequest(request.id)">
                                    Reject
                                </button>
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div class="table-responsive m-3" v-if="currentServices.length">
            <h4>ONGOING SERVICES</h4>
            <table class="table table-hover table-bordered">
                <thead>
                    <tr>
                        <th scope="col" width="20%">ID</th>
                        <th scope="col" width="20%">Customer Name</th>
                        <th scope="col" width="20%">Phone Number</th>
                        <th scope="col" width="20%">Location (PINCODE)</th>
                        <th scope="col" width="20%">Action</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="request in currentServices" :key="request.id">
                        <td scope="row">{{ request.id }}</td>
                        <td>{{ request.customer_name }}</td>
                        <td>{{ request.customer_no }}</td>
                        <td>{{ request.customer_pincode }}</td>
                        <td>
                            <div class="btn-group" role="group">
                                <button type="button" class="btn btn-info btn-sm" data-bs-toggle="modal"
                                    data-bs-target="#viewCurrentRequest" @click="viewCurrentSR(request.id)">
                                    View
                                </button>
                                <div class="modal fade" id="viewCurrentRequest" tabindex="-1"
                                    aria-labelledby="viewCurrentRequestLabel" aria-hidden="true">
                                    <div class="modal-dialog modal-dialog-centered">
                                        <div class="modal-content">
                                            <div class="modal-header">
                                                <h1 class="modal-title fs-5" id="viewCurrentRequestLabel">Service
                                                    Request Info
                                                </h1>
                                                <button type="button" @click="initForm" class="btn-close"
                                                    data-bs-dismiss="modal" aria-label="Close"></button>
                                            </div>
                                            <div class="modal-body">
                                                <p>Customer Name: {{ viewCurrentService.customer_name }}</p>
                                                <p>Service Name: {{ viewCurrentService.service_name }}</p>
                                                <p>Customer Number: {{ viewCurrentService.customer_no }}</p>
                                                <p>Location (PINCODE): {{ viewCurrentService.customer_pincode }}</p>
                                                <p>Status: {{ viewCurrentService.status }}</p>
                                            </div>
                                            <div class="modal-footer">
                                                <button type="button" @click="initForm" class="btn btn-secondary"
                                                    data-bs-dismiss="modal">Close</button>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <button type="button" v-if="request.status === 'Paid'" class="btn btn-success btn-sm" data-bs-toggle="modal"
                                        data-bs-target="#closeServiceModal">
                                        Close
                                </button>
                                <div class="modal fade" id="closeServiceModal" tabindex="-1"
                                    aria-labelledby="closeServiceModalLabel" aria-hidden="true">
                                    <div class="modal-dialog modal-dialog-centered">
                                        <div class="modal-content">
                                            <div class="modal-header bg-success text-white">
                                                <h5 class="modal-title" id="closeServiceModalLabel">Wanna close it?</h5>
                                                <button type="button" class="btn-close btn-close-white"
                                                    data-bs-dismiss="modal" aria-label="Close"></button>
                                            </div>
                                            <div class="modal-body">
                                                <p class="mb-0">Are you sure about closing the request?</p>
                                            </div>
                                            <div class="modal-footer">
                                                <button type="button" class="btn btn-secondary"
                                                    data-bs-dismiss="modal">Cancel</button>
                                                <button type="button" class="btn btn-success" 
                                                    @click="closeService(request.id)" 
                                                    data-bs-dismiss="modal">Book</button>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <Snippet :isOpen="isProfileOpen" title="Complete Your Profile" @close="submitProfile" buttonName="Submit"
             :disabled="!isFormValid">
            <form>
                <div class="mb-3">
                    <label for="profile" class="form-label">Profile Picture</label>
                    <input class="form-control" type="file" @change="handleProfileUpload" accept="image/*" id="profile">
                </div>
                <div class="mb-3">
                    <label for="description" class="col-form-label">Bio</label>
                    <textarea class="form-control" id="description" v-model="profileDetails.description" required></textarea>
                </div>
                <div class="row mb-3">
                    <label for="contact_no" class="col-sm-5 col-form-label">Contact Number</label>
                    <div class="col-sm-7">
                        <input type="number" class="form-control" id="contact_no" v-model="profileDetails.contact_no" required>
                    </div>
                </div>
                <div class="row g-3">
                    <div class="col-md-6">
                        <label for="experience" class="form-label">Experience</label>
                        <input type="text" class="form-control" id="experience" v-model="profileDetails.experience" required>
                    </div>
                    <div class="col-md-6">
                        <label for="pincode" class="form-label">Pincode</label>
                        <input type="number" class="form-control" id="pincode" v-model="profileDetails.pincode" required>
                    </div>
                </div>
                <div class="mb-3">
                    <label for="address" class="col-form-label">Address</label>
                    <textarea class="form-control" id="address" v-model="profileDetails.address" required></textarea>
                </div>
            </form>
        </Snippet>
    </div>
</template>

<script>
import ProfessionalNav from "@/components/ProfessionalNav.vue";
import Snippet from "@/components/Snippet.vue";
import { ref, onMounted, watch, computed } from 'vue';
import axios from 'axios';
import { useStore } from "vuex";

export default {
    name: "ProfessionalDashboard",
    components: {
        ProfessionalNav,
        Snippet
    },
    setup() {
        const pendingServices = ref([])
        const currentServices = ref([])
        const viewCurrentService = ref({})
        
        const message = ref('');
        const showMessage = ref(false);
        const error = ref('');
        const showError = ref(false);
        
        const store = useStore();

        const profID = ref(null)

        const isProfileOpen = ref(false);
        const profileDetails = ref({
            profile:null,
            experience:'',
            contact_no:'',
            pincode:'',
            address:'',
            description:'', 
        })

        watch(showError, (newValue) => {
            if (newValue) {
                setTimeout(() => {
                    hideMessage();
                }, 8000);
            }
        });

        watch(showMessage, (newValue) => {
            if (newValue) {
                setTimeout(() => {
                    hideMessage();
                }, 8000);
            }
        });

        const hideMessage = () => {
            showMessage.value = false;
            showError.value = false;
            error.value = '';
            message.value = ''
        };

        const initForm = () => {
            viewCurrentService.value = {}
        };

        const handleProfileUpload = (event) => {
            profileDetails.value.profile = event.target.files[0];
        };

        const userID = computed(() => {
            return store.state.userID;
        });

        const isFirstSession = computed(() => {
            return store.state.isFirstSession;
        });

        const checkFirstSession = () => {
            if (isFirstSession.value) {
                isProfileOpen.value = true;
                const firstSessionStatus  = false;
                store.dispatch('firstSession', { isFirstSession: firstSessionStatus }); 
                getProfID();
            }
        };

        const isFormValid = computed(() => {
            const pincodeValue = profileDetails.value.pincode ? profileDetails.value.pincode.toString().trim() : '';
            const addressValue = profileDetails.value.address ? profileDetails.value.address.trim() : '';
            const contactValue = profileDetails.value.contact_no ? profileDetails.value.contact_no.toString().trim() : '';
            const descriptionValue = profileDetails.value.description ? profileDetails.value.description.trim() : '';
            const experienceValue = profileDetails.value.experience ? profileDetails.value.experience.trim() : '';

            return (
                addressValue !== '' &&  
                descriptionValue !== '' &&
                pincodeValue !== '' && 
                pincodeValue.length === 6 &&
                contactValue !== '' &&
                contactValue.length === 10 &&
                experienceValue !== ''
            );
        });

        const submitProfile = async () => {
            if (!isFormValid.value) {
                showError.value = true;
                error.value = "Please fill in all required fields.";
                return;
            }

            try {
                const formData = new FormData();
                formData.append('experience', profileDetails.value.experience);
                formData.append('contact_no', profileDetails.value.contact_no);
                formData.append('address', profileDetails.value.address);
                formData.append('pincode', profileDetails.value.pincode);
                formData.append('description', profileDetails.value.description);
                formData.append('profile_pic', profileDetails.value.profile);
                formData.append('is_profile_completed', true)
                formData.append('is_first_session', false);

                if(!profID.value){
                    showError.value = true;
                    error.value = "Error fetching profID";
                    return;
                }

                const response = await axios.put(`http://localhost:5000/api/professional/${profID.value}`, formData ,
                {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                    }
                });

                isProfileOpen.value = false;
                message.value = "You updated the profile" || response.data.message;
                showMessage.value = true;
            } 
            catch (err) {
                error.value = "Error updating the profile" || err.response?.data?.message || err.message;
                showError.value = true;
            }
        };

        const requestedServices = async () => {
            try {
                const response = await axios.get('http://localhost:5000/api/professional/requests', {
                    params: {
                        status: 'Requested'
                    },
                });
                pendingServices.value = response.data.service_requests;
            } 
            catch (err) {
                console.log(err)
            }
        };

        const acceptedServices = async () => {
            try {
                const response = await axios.get('http://localhost:5000/api/professional/requests', {
                    params: {
                        status: ['Assigned', 'Paid']
                    },
                    paramsSerializer: (params) => {
                        return Object.keys(params)
                            .map((key) =>
                                Array.isArray(params[key])
                                    ? params[key].map((val) => `${key}=${val}`).join('&')
                                    : `${key}=${params[key]}`
                            )
                            .join('&');
                    },
                });
                currentServices.value = response.data.service_requests;
            } 
            catch (err) {
                console.log(err)
            }
        };

        const acceptRequest = async (id) => {
            try {
                const response = await axios.put(`http://localhost:5000/api/service-request/${id}`, {
                    status: 'Assigned'
                });
                message.value = "You accepted the customer request" || response.data.message;
                showMessage.value = true;
                requestedServices();
                acceptedServices();
            } 
            catch (err) {
                error.value = 'Error accepting the request';
                showError.value = true;
                requestedServices();
                acceptedServices();
            }
        };

        const rejectRequest = async (id) => {

            try {
                const response = await axios.put(`http://localhost:5000/api/service-request/${id}`, {
                    status: 'Rejected'
                });
                message.value = "You rejected the customer request" || response.data.message;
                showMessage.value = true;
                requestedServices();
                acceptedServices();
            } 
            catch (err) {
                error.value = 'Error rejecting the request';
                showError.value = true;
                requestedServices();
                acceptedServices();
            }
        };

        const viewCurrentSR = async (id) => {
            try {
                const response = await axios.get(`http://localhost:5000/api/professional/request/${id}`);
                viewCurrentService.value = response.data;
            } 
            catch (err) {
                error.value = 'Error loading request details';
                showError.value = true;
            }
        };

        const closeService = async (id) => {
            try {
                const response = await axios.put(`http://localhost:5000/api/service-request/${id}`, {
                    status: "Closed",
                    status_updated_by: "Professional",
                });
                message.value = "You closed the service" || response.data.message;
                showMessage.value = true;
                requestedServices();
                acceptedServices();
            } 
            catch (err) {
                error.value = 'Error closing the service' || err.response?.data?.message || err.message;
                showError.value = true;
                requestedServices();
                acceptedServices();
            }
        };

        const getProfID = async () => {
            try {
                const response = await axios.get(`http://localhost:5000/get-prof-id/${userID.value}`);
                profID.value = response.data.profID;
            } 
            catch (err) {
                error.value = 'Could not fetch profID';
                showError.value = true;
            }
        };

        onMounted(() => {
            requestedServices();
            acceptedServices();
            checkFirstSession();
        });

        return {
            pendingServices,
            currentServices,
            acceptRequest,
            rejectRequest,
            viewCurrentSR,
            viewCurrentService,
            message,
            error,
            showError,
            showMessage,
            initForm,
            closeService,
            isProfileOpen,
            submitProfile,
            profileDetails,
            handleProfileUpload,
            isFormValid
        };
    },
};
</script>

<style scoped>
.filter-buttons {
    display: flex;
    gap: 15px;
    border-radius: 7px;
    flex-direction: row;
    padding: 5px 10px;
    align-items: center;
}

.filter-buttons label {
    display: flex;
    align-items: center;
    cursor: pointer;
}

.filter-buttons input[type="radio"] {
    display: none;
}

.filter-buttons span {
    font-size: 16px;
    color: #333;
}

.filter-buttons input[type="radio"]:checked+span {
    font-weight: bold;
    color: rgb(109, 74, 255);
    background-color: white;
    padding: 3px 5px;
    border-radius: 7px;
}

.table-hover tbody tr:hover {
    background-color: #f1f5f9;
}

.table thead th {
    font-weight: bold;
    font-size: 0.9rem;
    color: #666;
}

.badge {
    font-size: 0.8rem;
    padding: 4px 8px;
    border-radius: 8px;
}

.btn-outline-secondary {
    border: none;
    background-color: #e7e9ec;
    color: #555;
}

.rating-container {
    display: flex;
    gap: 0.5rem;
    justify-content: center;
}

.star {
    font-size: 2rem;
    cursor: pointer;
    transition: transform 0.2s ease, color 0.2s ease;
    color: #d3d3d3;
}

.star.filled {
    color: #8f07ff;
}

.star.hover {
    color: #d380ff;
}

.star:hover {
    transform: scale(1.2);
}

.rating-container:hover .star {
    transform: scale(1);
    opacity: 0.7;
}

.rating-container .star:hover {
    opacity: 1;
}
</style>