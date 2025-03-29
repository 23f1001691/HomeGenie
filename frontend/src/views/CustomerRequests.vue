<template>
    <div>
        <CustomerNav />
        <Error :showError="showErrorComponent" title="Sorry!" content="No requests is made" errorHeight="523" />
        <div class="table-responsive m-3" v-if="pendingServices.length">
            <h4>PENDING SERVICES</h4>
            <table class="table table-hover table-bordered">
                <thead>
                    <tr>
                        <th scope="col" width="20%">ID</th>
                        <th scope="col" width="20%">Service Name</th>
                        <th scope="col" width="20%">Professional Name</th>
                        <th scope="col" width="20%">Status</th>
                        <th scope="col" width="20%">Action</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="request in pendingServices" :key="request.id">
                        <td scope="row">{{ request.id }}</td>
                        <td>{{ request.service_name }}</td>
                        <td>{{ request.professional_name }}</td>
                        <td>{{ request.status }}</td>
                        <td>
                            <div class="btn-group" role="group">
                                <button type="button" v-if="request.status==='Requested'" class="btn btn-danger btn-sm"  @click="cancelRequest(request.id)">
                                    Cancel Request
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
                        <th scope="col" width="20%">Service Name</th>
                        <th scope="col" width="20%">Professional Name</th>
                        <th scope="col" width="20%">Status</th>
                        <th scope="col" width="20%">Action</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="request in currentServices" :key="request.id">
                        <td scope="row">{{ request.id }}</td>
                        <td>{{ request.service_name }}</td>
                        <td>{{ request.professional_name }}</td>
                        <td>{{ request.status }}</td>
                        <td>
                            <div class="btn-group" role="group">
                                <button type="button" class="btn btn-info btn-sm" data-bs-toggle="modal"
                                        data-bs-target="#viewRequest" @click="viewDetails(request.id)">
                                    View
                                </button>
                                <button type="button" v-if="request.status==='Assigned'" 
                                        class="btn btn-success btn-sm" @click="createOrder(request.id)">
                                    Pay
                                </button>
                                <button type="button" v-if="request.status==='Paid'" class="btn btn-success btn-sm" data-bs-toggle="modal" 
                                        data-bs-target="#feedback">
                                    Close
                                </button>
                                <div class="modal fade" id="feedback" tabindex="-1" aria-labelledby="feedbackLabel"
                                    aria-hidden="true">
                                    <div class="modal-dialog modal-dialog-centered">
                                        <div class="modal-content">
                                            <div class="modal-header">
                                                <h1 class="modal-title fs-5" id="feedbackLabel">Feedback</h1>
                                                <button type="button" @click="initForm" class="btn-close"
                                                    data-bs-dismiss="modal" aria-label="Close"></button>
                                            </div>
                                            <div class="modal-body">
                                                <div class="mb-3 row g-3 align-items-center">
                                                    <div class="col-auto">
                                                        <label for="remarks" class="col-form-label">Remarks</label>
                                                    </div>
                                                    <div class="col-auto">
                                                        <input class="form-control" type="text" id="remarks" v-model="remarks" required>
                                                    </div>
                                                </div>
                                                <div class="mb-3 row g-3 align-items-center">
                                                    <div class="col-auto">
                                                        <label for="rating" class="col-form-label">Rating</label>
                                                    </div>
                                                    <div class="col-auto">
                                                        <div class="rate">
                                                            <input type="radio" id="star1" v-model="rating" value="1" />
                                                            <label for="star1" title="text">1 star</label>
                                                            <input type="radio" id="star2" v-model="rating" value="2" />
                                                            <label for="star2" title="text">2 stars</label>
                                                            <input type="radio" id="star3" v-model="rating" value="3" />
                                                            <label for="star3" title="text">3 stars</label>
                                                            <input type="radio" id="star4" v-model="rating" value="4" />
                                                            <label for="star4" title="text">4 stars</label>
                                                            <input type="radio" id="star5" v-model="rating" value="5" />
                                                            <label for="star5" title="text">5 stars</label>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                            <div class="modal-footer">
                                                <button type="button" @click="closeService(request.id)" class="btn btn-secondary"
                                                    data-bs-dismiss="modal">Submit</button>
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
        <div class="table-responsive m-3" v-if="oldServices.length">
            <h4>SERVICE HISTORY</h4>
            <table class="table table-hover table-bordered">
                <thead>
                    <tr>
                        <th scope="col" width="20%">ID</th>
                        <th scope="col" width="20%">Service Name</th>
                        <th scope="col" width="20%">Professional Name</th>
                        <th scope="col" width="20%">Date</th>
                        <th scope="col" width="20%">Action</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="request in oldServices" :key="request.id">
                        <td scope="row">{{ request.id }}</td>
                        <td>{{ request.service_name }}</td>
                        <td>{{ request.professional_name }}</td>
                        <td>{{ request.date_of_completion }}</td>
                        <td>
                            <div class="btn-group" role="group">
                                <button type="button" class="btn btn-info btn-sm" data-bs-toggle="modal"
                                        data-bs-target="#viewRequest" @click="viewDetails(request.id)">
                                    View
                                </button>
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
        <div class="modal fade" id="viewRequest" tabindex="-1" aria-labelledby="viewRequestLabel"
                                    aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h1 class="modal-title fs-5" id="viewRequestLabel">Service Request Info</h1>
                        <button type="button" @click="initForm" class="btn-close"
                                data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <p>Professional Name: {{ viewInfo.professional_name }}</p>
                        <p>Service Name:  {{ viewInfo.service_name }}</p>
                        <p>Professional Number:  {{ viewInfo.professional_number }}</p>
                        <p>Professional Rating:  {{ viewInfo.professional_rating }}</p>
                        <p>Status: {{ viewInfo.status }}</p>
                    </div>
                    <div class="modal-footer">
                        <button type="button" @click="initForm" class="btn btn-secondary"
                                data-bs-dismiss="modal">Close</button>
                    </div>
                </div>
            </div>
        </div>      
    </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue';
import axios from 'axios';
import CustomerNav from "@/components/CustomerNav.vue";
import Error from '@/components/Error.vue';

export default {
    name: "CustomerRequests",
    components: {
        CustomerNav,
        Error
    },
    setup() {
        const message = ref('');
        const showMessage = ref(false);
        const error = ref('');
        const showError = ref(false);

        const showErrorComponent = ref(false);

        const oldServices = ref([]);
        const pendingServices = ref([])
        const currentServices = ref([])

        const remarks = ref('');
        const rating = ref('');

        const viewInfo = ref({});

        const razorpayOrder = ref(null);
        const addOns = ref(null);

        watch([pendingServices, currentServices, oldServices], () => {
            showErrorComponent.value = !pendingServices.value.length && !currentServices.value.length && !oldServices.value.length;
        }, { immediate: true }); 

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
            remarks.value = ''
            rating.value = ''
            viewInfo.value = {}
        };

        const requestedServices = async () => {
            try {
                const response = await axios.get('http://localhost:5000/api/customer/requests', {
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
                const response = await axios.get('http://localhost:5000/api/customer/requests', {
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

        const closedServices = async () => {
            try {
                const response = await axios.get('http://localhost:5000/api/customer/requests', {
                    params: {
                        status: 'Closed'
                    },
                });
                oldServices.value = response.data.service_requests;
            } 
            catch (err) {
                console.log(err)
            }
        }; 

        const cancelRequest = async (id) => {
            try {
                const response = await axios.delete(`http://localhost:5000/api/service-request/${id}`);
                message.value = "Your service request is cancelled" || response.data.message;
                showMessage.value = true;
                requestedServices();
            } catch (err) {
                error.value = err.response?.data?.message || 'Failed to cancel your request';
                showError.value = true;
                requestedServices();
            }
        };

        const createOrder = async (id) => {
            try {
                const response = await axios.get(`http://localhost:5000/api/payment/${id}`, {
                    withCredentials: true
                });
                const { order, add_on } = response.data;
                razorpayOrder.value = order;
                addOns.value = add_on;
                openRazorpayModal(order, add_on);
            } 
            catch (err) {
                error.value = err.response?.data?.message || err.message;
                showError.value = true;
            }
        };

        const openRazorpayModal = (order, add_on) => {
            const options = {
                key: add_on.key,  
                amount: order.amount,
                currency: order.currency,
                name: 'HomeGenie',
                description: 'Payment for Service',
                order_id: order.id,
                handler: paymentHandler,
                // prefill: {
                //     name: 'Customer Name',
                //     email: 'customer@example.com',
                //     contact: '1234567890'
                // },
                notes: {
                    service_request_id: add_on.id
                },
                theme: {
                    color: '#F37254'
                }
            };
            const razorpay = new Razorpay(options);
            razorpay.open();
        };

        const paymentHandler = async (response) => {
            const paymentId = response.razorpay_payment_id;
            const orderId = response.razorpay_order_id;
            const signature = response.razorpay_signature;

            try {
                const paymentData = {
                    service_request_id: addOns.value.id,
                    payment_id: paymentId,
                    order_id: orderId,
                    signature: signature
                };
                const response = await axios.post('http://localhost:5000/api/payment',paymentData);
                message.value = response?.data?.message || "Payment successful!";
                showMessage.value = true;
                acceptedServices();
            } 
            catch (err) {
                error.value = err.response?.data?.message || "Payment unsuccessful!"
                showError.value = true;
                acceptedServices();
            }
        };

        const submitReview = async (id) => {
            try {
                const response = await axios.post(`http://localhost:5000/api/review`,{
                    service_request_id:id,
                    feedback:remarks.value,
                    rating:parseInt(rating.value, 10)
                });
            } 
            catch (err) {
                console.log(err)
            }
        };

        const closeService = async (id) => {
            try {
                submitReview(id)
                const response = await axios.put(`http://localhost:5000/api/service-request/${id}`,{
                    status:"Closed",
                    status_updated_by:"Customer",
                });
                message.value = "You closed the service" || response.data.message;
                showMessage.value = true;
                acceptedServices();
                closedServices();
                initForm();
            } 
            catch (err) {
                error.value = err.response?.data?.message || 'Error occured';
                showError.value = true;
                acceptedServices();
                closedServices();
                initForm();
            }
        };

        const viewDetails = async (id) => {

            try {
                const response = await axios.get(`http://localhost:5000/api/customer/request/${id}`);
                viewInfo.value = response.data;
            } catch (err) {
                console.log(err)
            }
        };

        onMounted(() => {
            requestedServices();
            acceptedServices();
            closedServices();
        });

        return {
            message,
            showMessage,
            error,
            showError,
            initForm,
            oldServices,
            pendingServices,
            currentServices,
            cancelRequest,
            closeService,
            remarks,
            rating,
            viewDetails,
            viewInfo,
            createOrder,
            showErrorComponent
        };
    }
};
</script>