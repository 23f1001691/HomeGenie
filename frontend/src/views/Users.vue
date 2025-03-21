<template>
    <div>
        <AdminNav />

        <div class="alert alert-danger" role="alert" v-if="showError">
            {{ error }}
        </div>

        <nav class="navbar navbar-light bg-light my-4">
            <div class="container-fluid">
                <div class="d-flex">
                    <input class="form-control me-2" type="search" v-model="searchQuery"
                        placeholder="Search" aria-label="Search">
                    <button class="btn btn-outline-secondary" type="button" @click="applyFilter">
                        <i class="fa-solid fa-magnifying-glass"></i>
                    </button>
                </div>
                <div class="d-flex">
                    <label for="filter" class="col-form-label me-2">Filter By : </label>
                    <select id="filter" class="form-select" v-model="selectedFilter" style="width: 200px;">
                        <option disabled value="">Select Option</option>
                        <option value="All">All</option>
                        <option value="Customers">Customers</option>
                        <option value="Professionals">Professionals</option>
                    </select>
                </div>
            </div>
        </nav>

        <div class="customers m-4" v-if="chunkedCustomers.length">
            <h4>CUSTOMERS</h4>

            <div class="carousel slide container-fluid my-4">
                <div class="carousel-inner mx-3">
                    <div class="carousel-item" v-for="(chunk, index) in chunkedCustomers" :key="index"
                        :class="{ active: index === customerIndex }">
                        <div class="row">
                            <div class="col-md-3" v-for="customer in chunk" :key="customer.id">
                                <div class="card card-wrapper">
                                    <img :src="customer.profile_pic" class="card-img-top">
                                    <div class="card-body;">
                                        <h6 class="card-title text-center my-3">{{ customer.name }}</h6>
                                        <div class="btn-group d-flex justify-content-center" role="group">
                                            <button type="button" class="btn btn-info btn-sm py-2" data-bs-toggle="modal"
                                                data-bs-target="#viewCustomer" @click="viewCustomer(customer)">
                                                VIEW
                                            </button>
                                            <button type="button" v-if="customer.flag==false" class="btn btn-danger btn-sm py-2" @click="flagCustomer(customer)">
                                                FLAG
                                            </button>
                                            <button type="button" v-if="customer.flag==true" class="btn btn-danger btn-sm py-2" @click="unflagCustomer(customer)">
                                                UNFLAG
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <button class="carousel-control-prev" @click="prevCustomerSlide(chunkedCustomers)"
                    :disabled="customerIndex === 0">
                    <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                    <span class="visually-hidden">Previous</span>
                </button>
                <button class="carousel-control-next" @click="nextCustomerSlide(chunkedCustomers)"
                    :disabled="customerIndex === chunkedCustomers.length - 1">
                    <span class="carousel-control-next-icon" aria-hidden="true"></span>
                    <span class="visually-hidden">Next</span>
                </button>

                <div class="modal fade" id="viewCustomer" tabindex="-1" aria-labelledby="viewCustomerLabel"
                    aria-hidden="true">
                    <div class="modal-dialog modal-dialog-centered">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h1 class="modal-title fs-5" id="viewCustomerLabel">Customer
                                    Info</h1>
                                <button type="button" @click="initForm" class="btn-close" data-bs-dismiss="modal"
                                    aria-label="Close"></button>
                            </div>
                            <div class="modal-body">
                                <p>Name: {{ viewCustomerInfo.name }}</p>
                                <p v-if="viewCustomerInfo.contact_no">Contact Number: {{ viewCustomerInfo.contact_no
                                    }}</p>
                                <p v-if="viewCustomerInfo.address">Address: {{ viewCustomerInfo.address
                                    }}</p>
                                <p v-if="viewCustomerInfo.pincode">Pincode: {{ viewCustomerInfo.pincode
                                    }}</p>
                            </div>
                            <div class="modal-footer">
                                <button type="button" @click="initForm" class="btn btn-secondary"
                                    data-bs-dismiss="modal">Close</button>
                            </div>
                        </div>
                    </div>
                </div>

            </div>
        </div>

        <div class="professionals m-4" v-if="chunkedProfessionals.length">
            <h4>PROFESSIONALS</h4>

            <div class="carousel slide container-fluid my-4">
                <div class="carousel-inner mx-3">
                    <div class="carousel-item" v-for="(chunk, index) in chunkedProfessionals" :key="index"
                        :class="{ active: index === professionalIndex }">
                        <div class="row">
                            <div class="col-md-3" v-for="prof in chunk" :key="prof.id">
                                <div class="card card-wrapper">
                                    <img :src="prof.profile_pic" class="card-img-top">
                                    <div class="card-body;">
                                        <h6 class="card-title text-center my-3">{{ prof.name }}</h6>
                                        <div class="btn-group d-flex justify-content-center" role="group">
                                            <button type="button" class="btn btn-info btn-sm py-2" data-bs-toggle="modal"
                                                data-bs-target="#viewProf" @click="viewProf(prof)">
                                                VIEW
                                            </button>
                                            <button type="button" v-if="prof.flag==false" class="btn btn-danger btn-sm py-2" @click="flagProf(prof)">
                                                FLAG
                                            </button>
                                            <button type="button" v-if="prof.flag==true" class="btn btn-danger btn-sm py-2" @click="unflagProf(prof)">
                                                UNFLAG
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <button class="carousel-control-prev" @click="prevProfessionalSlide(chunkedProfessionals)"
                    :disabled="professionalIndex === 0">
                    <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                    <span class="visually-hidden">Previous</span>
                </button>
                <button class="carousel-control-next" @click="nextProfessionalSlide(chunkedProfessionals)"
                    :disabled="professionalIndex === chunkedProfessionals.length - 1">
                    <span class="carousel-control-next-icon" aria-hidden="true"></span>
                    <span class="visually-hidden">Next</span>
                </button>

                <div class="modal fade" id="viewProf" tabindex="-1" aria-labelledby="viewProfLabel" aria-hidden="true">
                    <div class="modal-dialog modal-dialog-centered">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h1 class="modal-title fs-5" id="viewProfLabel">Professional
                                    Info</h1>
                                <button type="button" @click="initForm" class="btn-close" data-bs-dismiss="modal"
                                    aria-label="Close"></button>
                            </div>
                            <div class="modal-body">
                                <p>Name: {{ viewProfInfo.name }}</p>
                                <p>Service: {{ viewProfInfo.service_name }}</p>
                                <p v-if="viewProfInfo.experience">Experience: {{
                                    viewProfInfo.experience
                                }}</p>
                                <p v-if="viewProfInfo.contact_no">Contact Number: {{ viewProfInfo.contact_no
                                    }}</p>
                                <p v-if="viewProfInfo.rating">Rating: {{ viewProfInfo.rating
                                    }}</p>
                                <p v-if="viewProfInfo.address">Address: {{ viewProfInfo.address
                                    }}</p>
                                <p v-if="viewProfInfo.pincode">Pincode: {{ viewProfInfo.pincode
                                    }}</p>
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

            </div>
        </div>
    </div>
</template>

<style scoped>
.carousel-inner {
    /* position: relative; */
    display: flex;
    overflow: hidden;
}

.carousel-item {
    display: none;
    transition: transform 0.5s ease-in-out, opacity 0.5s ease-in-out;
    /* width: 100%;  */
    justify-content: center;
}

.carousel-item.active {
    display: block;
    opacity: 1;
}

.card-wrapper {
    width: 250px;
    border: 1px solid black;
}

.card-wrapper img {
    object-fit: cover;
    display: block;
    padding: 5px 0;
    width: 130px !important;
    height: 150px !important; 
    border-radius: 50%; 
    margin: 0 auto; 
    /* height: 200px; */
}

.carousel-control-prev,
.carousel-control-next {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    width: 40px;
    height: 40px;
    background-color: rgba(0, 0, 0, 0.5);
    border-radius: 50%;
}

.carousel-control-prev {
    left: 15px;
}

.carousel-control-next {
    right: 15px;
}

.carousel-control-prev:disabled,
.carousel-control-next:disabled {
    display: none;
    opacity: 0.5;
    cursor: not-allowed;
}

.carousel-control-prev-icon,
.carousel-control-next-icon {
    background-image: none;
    width: 10px;
    height: 10px;
    border: solid white;
    border-width: 0 3px 3px 0;
    display: inline-block;
    padding: 3px;
}

.carousel-control-prev-icon {
    transform: rotate(135deg);
}

.carousel-control-next-icon {
    transform: rotate(-45deg);
}
</style>

<script>
import { ref, onMounted, watch} from 'vue';
import axios from 'axios';
import AdminNav from '@/components/AdminNav.vue';
import useCarousel from '@/composables/useCarousel';
import fetchProfessionals from '@/composables/fetchProfessionals';
import fetchCustomers from '@/composables/fetchCustomers';

export default {
    name: 'Users',
    components: {
        AdminNav
    },
    setup() {

        const { chunkedProfessionals, professionalError, loadProfessionals } = fetchProfessionals()
        const { chunkedCustomers, customerError, loadCustomers } = fetchCustomers()

        const { currentIndex: professionalIndex, nextSlide: nextProfessionalSlide, prevSlide: prevProfessionalSlide } = useCarousel();
        const { currentIndex: customerIndex, nextSlide: nextCustomerSlide, prevSlide: prevCustomerSlide } = useCarousel();

        const viewProfInfo = ref({});
        const viewCustomerInfo = ref({});
        const error = ref('');
        const showError = ref(false);
        const searchQuery = ref('');
        const selectedFilter = ref('');

        watch(showError, (newValue) => {
            if (newValue) {
                setTimeout(() => {
                    hideMessage();
                }, 8000);
            }
        });

        const hideMessage = () => {
            showError.value = false;
            error.value = ''
        };

        const initForm = () => {
            viewProfInfo.value = {};
            viewCustomerInfo.value = {};
        };

        const viewCustomer = async (customer) => {
            try {
                const response = await axios.get(`http://localhost:5000/api/customer/${customer.id}`);
                if (!response.data) {
                    throw Error('Error in fetching this customer data')
                }
                viewCustomerInfo.value = response.data;
            } catch (err) {
                error.value = err.message;
                showError.value = true;
            }
        };

        const viewProf = async (prof) => {
            try {
                const response = await axios.get(`http://localhost:5000/api/professional/${prof.id}`);
                if (!response.data) {
                    throw Error('Error in fetching this professional data')
                }
                viewProfInfo.value = response.data;

            } catch (err) {
                error.value = err.message;
                showError.value = true;
            }
        };

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
        };

        const flagCustomer = async (customer) => {
            try {
                const response = await axios.put(`http://localhost:5000/api/customer/${customer.id}`,{
                    flag:true
                });
                if (!response.data) {
                    throw Error('Error in flagging the customer')
                }
                loadCustomers();
            } 
            catch (err) {
                error.value = err.message;
                showError.value = true;
                loadCustomers();
            }
        };

        const unflagCustomer = async (customer) => {
            try {
                const response = await axios.put(`http://localhost:5000/api/customer/${customer.id}`,{
                    flag:false
                });
                if (!response.data) {
                    throw Error('Error in un-flagging the customer')
                }
                loadCustomers();
            } 
            catch (err) {
                error.value = err.message;
                showError.value = true;
                loadCustomers();
            }
        };

        const applyFilter = async () => {
            try {

                if(selectedFilter.value === 'Customers'){
                    await loadCustomers(searchQuery.value, selectedFilter.value);
                    chunkedProfessionals.value = []
                }
                    
                else if(selectedFilter.value === 'Professionals'){
                    await loadProfessionals(searchQuery.value, selectedFilter.value);
                    chunkedCustomers.value =[]
                }

                else{
                    searchQuery.value = ""
                    await loadCustomers();
                    await loadProfessionals();
                }      
            } 
            catch (err) {
                error.value = 'No such user exists';
                showError.value = true;
            }
        };

        const flagProf = async (prof) => {
            try {
                const response = await axios.put(`http://localhost:5000/api/professional/${prof.id}`,{
                    flag:true
                });
                if (!response.data) {
                    throw Error('Error in flagging the professional')
                }
                loadProfessionals();
            } 
            catch (err) {
                error.value = err.message;
                showError.value = true;
                loadProfessionals();
            }
        };

        const unflagProf = async (prof) => {
            try {
                const response = await axios.put(`http://localhost:5000/api/professional/${prof.id}`,{
                    flag:false
                });
                if (!response.data) {
                    throw Error('Error in un-flagging the professional')
                }
                loadProfessionals();
            } 
            catch (err) {
                error.value = err.message;
                showError.value = true;
                loadProfessionals();
            }
        };

        onMounted(() => {
            loadProfessionals();
            loadCustomers();
        });

        return {

            chunkedProfessionals,
            professionalError,
            professionalIndex,
            nextProfessionalSlide,
            prevProfessionalSlide,

            chunkedCustomers,
            customerError,
            customerIndex,
            nextCustomerSlide,
            prevCustomerSlide,

            viewProf,
            viewProfInfo,
            flagProf,
            unflagProf,
            viewResume,

            viewCustomer,
            viewCustomerInfo,
            flagCustomer,
            unflagCustomer,
            
            error,
            showError,
            initForm,
            
            applyFilter,
            searchQuery,
            selectedFilter
        };




    }
};
</script>

