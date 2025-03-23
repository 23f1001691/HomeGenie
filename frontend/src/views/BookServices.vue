<template>
    <div>
        <CustomerNav />
        <div class="alert alert-danger" role="alert" v-if="showError">
            {{ error }}
        </div>
        <div class="alert alert-success" role="alert" v-if="showMessage">
            {{ message }}
        </div>
        <nav class="navbar navbar-light bg-light my-4">
            <div class="container-fluid">
                <div class="d-flex">
                    <input class="form-control me-2" type="search" v-model="searchQuery" placeholder="Search"
                        aria-label="Search">
                    <button class="btn btn-outline-secondary" type="button" @click="applyFilter">
                        <i class="fa-solid fa-magnifying-glass"></i>
                    </button>
                </div>
                <div class="d-flex">
                    <label for="filter" class="col-form-label me-2">Filter By : </label>
                    <select id="filter" class="form-select" v-model="selectedFilter" style="width: 200px;">
                        <option disabled value="">Select Option</option>
                        <option value="Service Name">Service Name</option>
                        <option value="Pincode">Pincode</option>
                        <option value="Rating">Rating</option>
                        <option value="Category">Category</option>
                    </select>
                </div>
            </div>
        </nav>
        <div class="table-responsive m-3" v-if="services.length">
            <h4 class="text-center mb-4">BOOK YOUR SERVICE</h4>
            <table class="table table-hover table-bordered">
                <thead>
                    <tr>
                        <th scope="col" width="20%">Service Name</th>
                        <th scope="col" width="20%">Professional Name</th>
                        <th scope="col" width="20%">Base Price</th>
                        <th scope="col" width="20%">Rating</th>
                        <th scope="col" width="20%">Action</th>
                    </tr>
                </thead>
                <tbody>
                    <template v-for="(service) in services">
                        <tr v-for="(prof, i) in service.professionals" :key="i">
                            <td scope="row">{{ service.name }}</td>
                            <td>{{ prof.name }}</td>
                            <td>{{ service.base_price }}</td>
                            <td>{{ prof.rating ? prof.rating : '0' }}</td>
                            <td>
                                <div class="btn-group" role="group">
                                    <button type="button" class="btn btn-info btn-sm" data-bs-toggle="modal"
                                        data-bs-target="#viewService" @click="viewDetails(service, prof)">
                                        View
                                    </button>
                                    <div class="modal fade" id="viewService" tabindex="-1"
                                        aria-labelledby="viewServiceLabel" aria-hidden="true">
                                        <div class="modal-dialog modal-dialog-centered">
                                            <div class="modal-content">
                                                <div class="modal-header">
                                                    <h1 class="modal-title fs-5" id="viewServiceLabel">Service Info
                                                    </h1>
                                                    <button type="button" @click="initForm" class="btn-close"
                                                        data-bs-dismiss="modal" aria-label="Close"></button>
                                                </div>
                                                <div class="modal-body">
                                                    <p>Service Name: {{ viewInfo.name }}</p>
                                                    <p>Description: {{ viewInfo.description }}</p>
                                                    <p>Price Range: {{ viewInfo.base_price }}</p>
                                                    <p>Minimum time: {{ viewInfo.time_req }}</p>
                                                    <div v-if="viewInfo.professionals">
                                                        <p>Professional Name: {{ viewInfo.professionals.name }}</p>
                                                        <p>Contact Number: {{ viewInfo.professionals.contact_no }}</p>
                                                        <p v-if="viewInfo.professionals.experience">Experience: {{
                                                            viewInfo.professionals.experience }}</p>
                                                        <p v-else>Experience: Not provided</p>
                                                        <p>Rating: {{ viewInfo.professionals.rating }}</p>
                                                        <p>Pincode: {{ viewInfo.professionals.pincode }}</p>
                                                    </div>
                                                </div>
                                                <div class="modal-footer">
                                                    <button type="button" @click="initForm" class="btn btn-secondary"
                                                        data-bs-dismiss="modal">Close</button>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                    <button type="button" class="btn btn-success btn-sm" data-bs-toggle="modal"
                                        data-bs-target="#confirmBookingModal">
                                        Book Service
                                    </button>
                                    <div class="modal fade" id="confirmBookingModal" tabindex="-1"
                                        aria-labelledby="confirmBookingModalLabel" aria-hidden="true">
                                        <div class="modal-dialog modal-dialog-centered">
                                            <div class="modal-content">
                                                <div class="modal-header bg-success text-white">
                                                    <h5 class="modal-title" id="confirmBookingModalLabel">Confirm Booking</h5>
                                                    <button type="button" class="btn-close btn-close-white"
                                                        data-bs-dismiss="modal" aria-label="Close"></button>
                                                </div>
                                                <div class="modal-body">
                                                    <p class="mb-0">Are you sure to book this service? 
                                                        Booking cannot be undone.</p>
                                                </div>
                                                <div class="modal-footer">
                                                    <button type="button" class="btn btn-secondary"
                                                        data-bs-dismiss="modal">Cancel</button>
                                                    <button type="button" class="btn btn-success" 
                                                        @click="bookService(service, prof)" 
                                                        data-bs-dismiss="modal">Book</button>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </td>
                        </tr>
                    </template>
                </tbody>
            </table>
        </div>
        <div v-else>
            <ErrorPage />
        </div>
    </div>


</template>

<script>
import { ref, onMounted, watch, computed } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';
import CustomerNav from "@/components/CustomerNav.vue";
import { useStore } from "vuex";
import ErrorPage from "@/components/404Page.vue"

export default {
    name: "BookServices",
    components: {
        CustomerNav,
        ErrorPage
        
    },
    setup() {
        const services = ref([]);
        const viewInfo = ref({});
        const searchQuery = ref('');
        const selectedFilter = ref('');
        const message = ref('');
        const showMessage = ref(false);
        const route = useRoute();
        const error = ref('');
        const showError = ref(false);
        const store = useStore();

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
            viewInfo.value = {}
        };

        const userID = computed(() => {
            return store.state.userID;
        });

        const getServices = async (filterBy = '', searchKey = '') => {

            selectedFilter.value = filterBy;
            searchQuery.value = searchKey;

            try {
                const response = await axios.get('http://localhost:5000/api/filter-services', {
                    params: {
                        filter_by: filterBy,
                        search_query: searchKey,
                    },
                });
                services.value = response.data;
            } 
            catch (err) {
                error.value = err;
                showError.value = true;
            }
        };

        const viewDetails = async (service, prof) => {
            try {
                const response = await axios.get(`http://localhost:5000/api/view-service/${service.id}/${prof.id}`);
                viewInfo.value = response.data;
            } catch (err) {
                error.value = err;
                showError.value = true;
            }
        };

        const applyFilter = () => {
            getServices(selectedFilter.value, searchQuery.value);
        };

        const bookService = async (service, prof) => {
            try {
                console.log(userID.value)
                const response = await axios.post('http://localhost:5000/api/service-requests', {
                    service_id: service.id,
                    customer_id: userID.value,
                    professional_id: prof.id,
                });
                message.value = response.data.message;
                showMessage.value = true;
                getServices();
            } catch (err) {
                error.value = err.response?.data?.message || 'An error occurred';
                showError.value = true;
                getServices();
            }
        };

        onMounted(() => {
            const filterBy = route.query.filterBy || '';
            const searchKey = route.query.searchQuery || '';
            getServices(filterBy, searchKey);
        });

        return {
            services,
            searchQuery,
            selectedFilter,
            message,
            showMessage,
            error,
            showError,
            getServices,
            applyFilter,
            bookService,
            viewDetails,
            viewInfo,
            initForm
        };
    },
};
</script>