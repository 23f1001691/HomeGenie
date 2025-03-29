<template>
    <div>
        <AdminNav />
        <div class="alert alert-danger" role="alert" v-if="showError">
            {{ error }}
        </div>
        <div class="alert alert-success" role="alert" v-if="showMessage">
            {{ message }}
        </div>
        <div class="table-responsive m-4">
            <div class="d-flex justify-content-between mb-3">
                <h4>SERVICES</h4>
                <button type="button" class="btn btn-success btn-sm" data-bs-toggle="modal"
                    data-bs-target="#newService">New
                    Service</button>
                <div class="modal fade" id="newService" tabindex="-1" aria-labelledby="newServiceLabel"
                    aria-hidden="true">
                    <div class="modal-dialog modal-dialog-centered">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h1 class="modal-title fs-5" id="newServiceLabel">New Service</h1>
                                <button type="button" @click="initForm" class="btn-close" data-bs-dismiss="modal"
                                    aria-label="Close"></button>
                            </div>
                            <div class="modal-body">
                                <div class="mb-3 row">
                                    <label for="category" class="col-auto col-form-label">Category</label>
                                    <div class="col-auto">
                                        <select class="form-select" id="category" 
                                            v-model="newService.category" required>
                                            <option disabled value="">Select Category</option>
                                            <option v-for="(category) in categories" :key="category.id" 
                                                            :value="category.name">
                                                {{ category.name }}
                                            </option>
                                        </select>
                                    </div>
                                </div>
                                <div class="mb-3 row">
                                    <label for="service_name" class="col-auto col-form-label">Service Name</label>
                                    <div class="col-auto">
                                        <input type="text" class="form-control" id="service_name"
                                            v-model="newService.name">
                                    </div>
                                </div>
                                <div class="mb-3 row">
                                    <label for="description" class="col-auto col-form-label">Description</label>
                                    <div class="col-auto">
                                        <input type="text" class="form-control" id="description"
                                            v-model="newService.description">
                                    </div>
                                </div>
                                <div class="mb-3 row">
                                    <label for="base_price" class="col-auto col-form-label">Base Price</label>
                                    <div class="col-auto">
                                        <input type="text" class="form-control" id="base_price"
                                            v-model="newService.base_price">
                                    </div>
                                </div>
                                <div class="mb-3 row">
                                    <label for="time_req" class="col-auto col-form-label">Time Required</label>
                                    <div class="col-auto">
                                        <input type="text" class="form-control" id="time_req"
                                            v-model="newService.time_req">
                                    </div>
                                </div>
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-primary" @click="addService"
                                    data-bs-dismiss="modal">Add
                                    Service</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <table class="table table-hover table-bordered" v-if="services.length">
                <thead>
                    <tr>
                        <th scope="col" width="25%">ID</th>
                        <th scope="col" width="25%">Service Name</th>
                        <th scope="col" width="25%">Base Price</th>
                        <th scope="col" width="25%">Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="service in services" :key="service.id">
                        <td scope="row">{{ service.id }}</td>
                        <td>{{ service.name }}</td>
                        <td>{{ service.base_price }}</td>
                        <td>
                            <div class="btn-group" role="group">
                                <button type="button" class="btn btn-info btn-sm" data-bs-toggle="modal"
                                    data-bs-target="#viewService" @click="viewService(service)">
                                    View
                                </button>
                                <div class="modal fade" id="viewService" tabindex="-1"
                                    aria-labelledby="viewServiceLabel" aria-hidden="true">
                                    <div class="modal-dialog modal-dialog-centered">
                                        <div class="modal-content">
                                            <div class="modal-header">
                                                <h1 class="modal-title fs-5" id="viewServiceLabel">Service Info</h1>
                                                <button type="button" @click="initForm" class="btn-close"
                                                    data-bs-dismiss="modal" aria-label="Close"></button>
                                            </div>
                                            <div class="modal-body">
                                                <p>Name: {{ viewServiceInfo.name }}</p>
                                                <p>Description: {{ viewServiceInfo.description }}</p>
                                                <p>Base Price: {{ viewServiceInfo.base_price }}</p>
                                                <p>Time Required: {{ viewServiceInfo.time_req }}</p>
                                            </div>
                                            <div class="modal-footer">
                                                <button type="button" @click="initForm" class="btn btn-secondary"
                                                    data-bs-dismiss="modal">Close</button>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <button type="button" class="btn btn-warning btn-sm" @click="displayInfo(service)">
                                    Edit
                                </button>
                                <EditService
                                    :service="selectedService"
                                    :isVisible="isModalVisible"
                                    @close="closeModal"
                                    @update="updateService"
                                />
                                <button type="button" class="btn btn-danger btn-sm" @click="deleteService(service)">
                                    Delete
                                </button>
                            </div>
                        </td>

                    </tr>
                </tbody>
            </table>
        </div>

        <div class="table-responsive m-4" v-if="professionals.length">
            <h4 class="mb-3">NEW PROFESSIONALS</h4>

            <table class="table table-hover table-bordered">
                <thead>
                    <tr>
                        <th scope="col" width="25%">ID</th>
                        <th scope="col" width="25%">Name</th>
                        <th scope="col" width="25%">Service Name</th>
                        <th scope="col" width="25%">Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="prof in professionals" :key="prof.id">
                        <td scope="row">{{ prof.id }}</td>
                        <td>{{ prof.name }}</td>
                        <td>{{ prof.service_name }}</td>
                        <td>
                            <div class="btn-group" role="group">
                                <button type="button" class="btn btn-info btn-sm" data-bs-toggle="modal"
                                    data-bs-target="#viewProf" @click="viewProf(prof)">
                                    View
                                </button>
                                <div class="modal fade" id="viewProf" tabindex="-1" aria-labelledby="viewProfLabel"
                                    aria-hidden="true">
                                    <div class="modal-dialog modal-dialog-centered">
                                        <div class="modal-content">
                                            <div class="modal-header">
                                                <h1 class="modal-title fs-5" id="viewProfLabel">Professional Info
                                                </h1>
                                                <button type="button" @click="initForm" class="btn-close"
                                                    data-bs-dismiss="modal" aria-label="Close"></button>
                                            </div>
                                            <div class="modal-body">
                                                <p>Name: {{ viewProfInfo.name }}</p>
                                                <p>Category: {{ viewProfInfo.category }}</p>
                                                <p v-if="!serviceExists" class="me-2 text-danger fw-bold mb-3">
                                                    NEW SERVICE ALERT!</p>
                                                <div class="d-flex align-items-center">
                                                    <p class="me-2">Service: {{ viewProfInfo.service_name }}</p>
                                                    <button type="button" v-if="!serviceExists"
                                                        class="btn btn-link btn-sm" style="margin-top: -15px;"
                                                        data-bs-toggle="modal" data-bs-target="#newService">
                                                        Add Service
                                                    </button>
                                                </div>
                                                <p v-if="viewProfInfo.experience">Experience: {{
                                                    viewProfInfo.experience
                                                }} years</p>
                                                <p v-if="viewProfInfo.address">Address: {{ viewProfInfo.address }}
                                                </p>
                                                <p v-if="viewProfInfo.pincode">Pincode: {{ viewProfInfo.pincode }}
                                                </p>
                                                <div>
                                                    Attachment:
                                                    <button class="btn btn-link btn-sm" v-if="viewProfInfo.resume"
                                                        @click="viewResume">
                                                        View Resume
                                                    </button>
                                                </div>
                                            </div>
                                            <div class="modal-footer">
                                                <button type="button" @click="initForm" class="btn btn-secondary"
                                                    data-bs-dismiss="modal">Close</button>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <button type="button" class="btn btn-success btn-sm" @click="approveProf(prof)">
                                    Approve
                                </button>
                                <button type="button" class="btn btn-danger btn-sm" @click="rejectProf(prof)">
                                    Reject
                                </button>
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<style scoped>
.line-input {
    margin-left: 100px;
    margin-top: 5px;
    border: none;
    border-bottom: 2px solid #000000;
    outline: none;
    padding: 0;
    width: 60%;
}

.line-input:focus {
    box-shadow: none;
}
</style>

<script>
import { ref, onMounted, watch, computed } from 'vue';
import AdminNav from '@/components/AdminNav.vue';
import axios from 'axios';
import EditService from '@/components//EditService.vue';

export default {
    name: 'Services',
    components: {
        AdminNav,
        EditService
    },
    setup() {
        const professionals = ref([]);
        const services = ref([]);
        const categories = ref([]);
        const serviceDetails = ref({});
        const viewProfInfo = ref({});
        const viewServiceInfo = ref({});
        const newService = ref({
            category: '',
            name: '',
            description: '',
            base_price: '',
            time_req: '',
        });
        const error = ref('');
        const showError = ref(false);
        const message = ref('');
        const showMessage = ref(false);
        const isModalVisible = ref(false);
        const selectedService = ref(null);

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
            newService.value = {
                category: '',
                name: '',
                description: '',
                base_price: '',
                time_req: ''
            };
            viewProfInfo.value = {};
            viewServiceInfo.value = {};
        };

        const serviceExists = computed(() => {
            return services.value.some(service => service.name === viewProfInfo.value.service_name);
        });

        const getProfs = async () => {
            try {
                const response = await axios.get('http://localhost:5000/api/professionals');
                if (!response.data) {
                    throw Error('Error in fetching professionals data')
                }
                professionals.value = response.data.filter(prof => prof.status === 'Unapproved');
            } catch (err) {
                console.log(err)
            }
        };

        const getServices = async () => {
            try {
                const response = await axios.get('http://localhost:5000/api/services');
                if (!response.data) {
                    throw Error('Error in fetching services data')
                }
                services.value = response.data;
            } catch (err) {
                console.log(err)
            }
        };;

        const getCategories = async () => {
            try {
                const response = await axios.get('http://localhost:5000/api/categories');
                if (!response.data) {
                    throw Error('Error in fetching categories')
                }
                categories.value = response.data
            } catch (err) {
                console.log(err)
            }
        };

        const viewService = async (service) => {
            try {
                const response = await axios.get(`http://localhost:5000/api/service/${service.id}`);
                if (!response.data) {
                    throw Error('Error in fetching this service data')
                }
                viewServiceInfo.value = response.data
            }
            catch (err) {
                error.value = err.response?.data?.message || err.message;
                showError.value = true;
            }
        };

        const addService = async () => {
            try {

                const response = await axios.post('http://localhost:5000/api/services', newService.value);

                if (!response.data) {
                    throw Error('Service is not posted')
                }
                message.value = response.data.message;
                showMessage.value = true;
                initForm();
                getServices();
            } 
            catch (err) {
                error.value = err.response?.data?.message || err.message;
                showError.value = true;
                initForm();
                getServices(); 
            }
        };

        const openModal = (service) => {
            selectedService.value = { ...service };
            isModalVisible.value = true;
        };

        const closeModal = () => {
            isModalVisible.value = false;
        };

        const displayInfo = async (service) => {
            try {
                const response = await axios.get(`http://localhost:5000/api/service/${service.id}`);
                if (!response.data) {
                    throw Error(response.data.message || 'Error in fetching this service data. Try again')
                }
                serviceDetails.value = response.data;
                openModal(serviceDetails.value);
                serviceDetails.value = ''
            } 
            catch (err) {
                error.value = err.response?.data?.message || err.message || 'An error occurred';
                showError.value = true;
            }
        };

        const updateService = async (service) => {
            try {
                const response = await axios.put(`http://localhost:5000/api/service/${service.id}`, service);
                if (!response.data) {
                    throw Error(response.data.message || 'Service is not updated. Try again')
                }
                closeModal();
                message.value = response.data.message || "Service Updated";
                showMessage.value = true;
                initForm();
                getServices();
            } 
            catch (err) {
                error.value = err.response?.data?.message || err.message || 'An error occurred';
                showError.value = true;
                initForm();
                getServices();
            }
        };

        const deleteService = async (service) => {
            try {
                const response = await axios.delete(`http://localhost:5000/api/service/${service.id}`);
                if (response.status != 204) {
                    throw Error(response.data.message || 'Service is not deleted. Try again')
                }
                getServices();
                message.value = response.data.message || "Service Deleted";
                showMessage.value = true;
            }
            catch (err) {
                getServices();
                error.value = err.response?.data?.message || err.message || 'An error occurred';
                showError.value = true;
            }
        }

        const viewProf = async (prof) => {
            try {
                const response = await axios.get(`http://localhost:5000/api/professional/${prof.id}`);
                if (!response.data) {
                    throw Error('Error in fetching this professional data')
                }
                viewProfInfo.value = response.data
            }
            catch (err) {
                error.value = err.response?.data?.message || err.message;
                showError.value = true;
            }
        }

        const viewResume = async () => {
            const resume = viewProfInfo.value.resume;
            try {
                const response = await axios.get(resume, { responseType: 'blob' });
                if (!response.data) {
                    throw Error('Resume link is not found')
                }
                const blob = response.data;
                const url = URL.createObjectURL(blob);
                window.open(url, '_blank');
            } 
            catch (err) {
                error.value = err.response?.data?.message || err.message;
                showError.value = true;
            }
        }

        const approveProf = async (prof) => {
            try {
                const response = await axios.put(`http://localhost:5000/api/professional/${prof.id}`,{
                    status: "Approved"
                });
                if (!response.data) {
                    throw Error('Professional is not approved. Try again')
                }
                message.value = "Professional approved and notified by email";
                showMessage.value = true;
                getProfs();
            }
            catch (err) {
                error.value = err.response?.data?.message || err.message;
                showError.value = true;
                getProfs();
            }
        }

        const rejectProf = async (prof) => {
            try {
                const response = await axios.put(`http://localhost:5000/api/professional/${prof.id}`,{
                    status: "Rejected"
                });
                if (!response.data) {
                    throw Error('Professional is not rejected. Try again')
                }
                message.value = "Professional rejected and notified by email";
                showMessage.value = true;
                getProfs();

            }
            catch (err) {
                error.value = err.response?.data?.message || err.message;
                showError.value = true;
                getProfs();
            }
        }

        onMounted(() => {
            getServices();
            getProfs();
            getCategories();
        });

        return {
            professionals,
            services,
            categories,
            error,
            showError,
            message,
            showMessage,
            approveProf,
            rejectProf,
            viewProf,
            viewResume,
            viewProfInfo,
            viewServiceInfo,
            viewService,
            deleteService,
            initForm,
            serviceExists,
            displayInfo,
            addService,
            updateService,
            newService,
            isModalVisible,
            selectedService,
            closeModal
        }
    }
}

</script>