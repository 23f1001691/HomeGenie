<template>
    <div>
        <CustomerNav />

        <div class="alert alert-danger" role="alert" v-if="showError">
            {{ error }}
        </div>
        <div class="alert alert-success" role="alert" v-if="showMessage">
            {{ message }}
        </div>

        <h4 class="text-center mt-5 mb-2">Looking For?</h4>
        <div class="carousel slide container-fluid mb-4 mt-3" ref="carouselContainer">
            <div class="carousel-inner mx-3">
                <div class="carousel-item" v-for="(chunk, index) in chunkedCategories" :key="index"
                    :class="{ active: index === currentIndex }">
                    <div class="row">
                        <div class="col-md-3" v-for="category in chunk" :key="category.id"
                            @click="goToCategory(category.name)">
                            <div class="card service-card">
                                <img :src="category.image_url" class="card-img-top">
                                <div class="card-body">
                                    <h6 class="card-title">{{ category.name }}</h6>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <button class="carousel-control-prev" @click="prevSlide(chunkedCategories)" 
                    :disabled="currentIndex === 0">
                <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                <span class="visually-hidden">Previous</span>
            </button>
            <button class="carousel-control-next" @click="nextSlide(chunkedCategories)"
                :disabled="currentIndex === chunkedCategories.length - 1">
                <span class="carousel-control-next-icon" aria-hidden="true"></span>
                <span class="visually-hidden">Next</span>
            </button>
        </div>

        <Snippet :isOpen="isProfileOpen" title="Complete Your Profile" @close="submitProfile" buttonName="Submit"
             :disabled="!isFormValid">
            <form>
                <div class="mb-3">
                    <label for="profile" class="form-label">Profile Picture</label>
                    <input class="form-control" type="file" @change="handleProfileUpload" accept="image/*" id="profile">
                </div>
                <div class="mb-3">
                    <label for="address" class="col-form-label">Address</label>
                    <textarea class="form-control" id="address" v-model="profileDetails.address" required></textarea>
                </div>
                <div class="row mb-3">
                    <label for="pincode" class="col-sm-3 col-form-label">Pincode</label>
                    <div class="col-sm-9">
                        <input type="number" class="form-control" id="pincode" v-model="profileDetails.pincode" required>
                    </div>
                </div>
            </form>
        </Snippet>
    </div>
</template>

<style scoped>
.slide {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
}

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

.service-card {
    width: 250px;
    border: 1px solid black;
}

.service-card img {
    height: 200px;
    object-fit: cover;
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
import { onMounted, computed, ref, watch } from 'vue';
import axios from 'axios';
import CustomerNav from '@/components/CustomerNav.vue';
import fetchCategories from '@/composables/fetchCategories';
import useCarousel from '@/composables/useCarousel';
import { useRouter } from 'vue-router';
import { useStore } from "vuex";
import Snippet from '@/components/Snippet.vue';

export default {
    name: 'CustomerDashboard',
    components: {
        CustomerNav,
        Snippet
    },
    setup() {

        const { chunkedCategories, categoryError, loadCategories } = fetchCategories()
        const { currentIndex, nextSlide, prevSlide } = useCarousel();

        const router = useRouter();
        const store = useStore();

        const message = ref('');
        const showMessage = ref(false);
        const error = ref('');
        const showError = ref(false);

        const customerID = ref(null)

        const isProfileOpen = ref(false);
        const profileDetails = ref({
            profile:null,
            pincode:'',
            address:'',
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
            showError.value = false;
            error.value = ''
            showMessage.value = false;
            message.value = ''
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
                getCustomerID();
            }
        };

        const isFormValid = computed(() => {
            const pincodeValue = profileDetails.value.pincode ? profileDetails.value.pincode.toString().trim() : '';
            const addressValue = profileDetails.value.address ? profileDetails.value.address.trim() : '';

            return (
                addressValue !== '' &&  
                pincodeValue !== '' && 
                pincodeValue.length === 6  
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
                formData.append('address', profileDetails.value.address);
                formData.append('pincode', profileDetails.value.pincode);
                if (profileDetails.value.profile !== null) {
                    formData.append('profile_pic', profileDetails.value.profile);
                }
                formData.append('is_profile_completed', true);
                formData.append('is_first_session', false);

                if(!customerID.value){
                    showError.value = true;
                    error.value = "Error fetching customerID";
                    return;
                }

                const response = await axios.put(`http://localhost:5000/api/customer/${customerID.value}`, formData ,
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

        const goToCategory = (categoryName) => {
            router.push({
                name: 'BookServices',
                params: { userID: userID.value },
                query: { filterBy: 'Category', searchQuery: categoryName }
            });
        };

        const getCustomerID = async () => {
            try {
                const response = await axios.get(`http://localhost:5000/get-customer-id/${userID.value}`);
                customerID.value = response.data.customerID;
            } catch (err) {
                error.value = 'Could not fetch customerID';
                showError.value = true;
            }
        };

        

        onMounted(() => {
            loadCategories();
            checkFirstSession();
        });

        return {
            prevSlide,
            nextSlide,
            currentIndex,
            chunkedCategories,
            categoryError,
            goToCategory,
            isProfileOpen,
            submitProfile,
            profileDetails,
            message,
            error,
            showError,
            showMessage,
            handleProfileUpload,
            isFormValid
        };
    }
};
</script>