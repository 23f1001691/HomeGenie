<template>
    <div>
        <NavBar />
        <div class="alert alert-danger" role="alert" v-if="showError">
            {{ error }}
        </div>
        <div class="container-fluid">
            <div class="form-container mt-3">
                <h4 class="text-center text-uppercase">Professional Signup</h4>
                <br>
                <form @submit.prevent="submitForm">
                    <div class="mb-2 row g-3 align-items-center">
                        <div class="col-auto">
                            <label for="name" class="col-form-label">Full Name</label>
                        </div>
                        <div class="col-auto">
                            <input type="text" class="form-control" id="name" v-model="name" required>
                        </div>
                    </div>
                    <div class="mb-2 row g-3 align-items-center">
                        <div class="col-auto">
                            <label for="email" class="col-form-label">Email</label>
                        </div>
                        <div class="col-auto">
                            <input type="email" class="form-control" id="email" v-model="email" required>
                        </div>
                    </div>
                    <div class="mb-2 row g-3 align-items-center">
                        <div class="col-auto">
                            <label for="password" class="col-form-label">Password</label>
                        </div>
                        <div class="col-auto">
                            <input type="password" class="form-control" id="password" v-model="password" required>
                        </div>
                    </div>
                    <div class="mb-2 row g-3 align-items-center">
                        <div class="col-auto">
                            <label for="category" class="col-form-label">Category</label>
                        </div>
                        <div class="col-auto">
                            <select class="form-select" id="category" v-model="category" required>
                                <option disabled value="">Select Category</option>
                                <option v-for="(category) in categories" :key="category.id" :value="category.name">
                                    {{ category.name }}
                                </option>
                            </select>
                        </div>
                    </div>
                    <div class="mb-2 row g-3 align-items-center">
                        <div class="col-auto">
                            <label for="serviceName" class="col-form-label">Service Name</label>
                        </div>
                        <div class="col-auto">
                            <input type="text" class="form-control" id="serviceName" v-model="serviceName" required>
                        </div>
                    </div>
                    <div class="mb-3 row g-3 align-items-center">
                        <div class="col-auto">
                            <label for="resume" class="col-form-label">Upload Resume</label>
                        </div>
                        <div class="col-auto">
                            <input class="form-control" type="file" @change="handleResumeUpload" accept=".pdf"
                                id="resume" required>
                        </div>
                    </div>
                    <button type="submit" class="btn btn-secondary d-md-block mx-auto">Submit</button>
                </form>
                <br>
                <p class="text-center">Already have an account? <router-link :to="{ name: 'Login' }">Login</router-link>
                </p>
            </div>
        </div>
    </div>
</template>

<style scoped>
.line-input {
    margin-left: 150px;
    border: none;
    border-bottom: 2px solid #000000;
    outline: none;
    padding: 0;
    width: 100%;
}

.line-input:focus {
    box-shadow: none;
}

label {
    width: 130px;
}

input,
select,
.line-input {
    width: 300px;
}
</style>

<script>
import NavBar from '@/components/NavBar.vue';
import axios from 'axios';
import { ref, watch, onMounted } from 'vue';
import { useRouter } from "vue-router";

export default {
    name: 'ProfessionalSignup',
    components: {
        NavBar,
    },
    setup() {
        const name = ref('');
        const email = ref('');
        const password = ref('');
        const serviceName = ref('');
        const resume = ref(null);
        const category = ref('');
        const categories = ref([]);
        const error = ref('');
        const showError = ref(false);
        const router = useRouter();

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

        const handleResumeUpload = (event) => {
            resume.value = event.target.files[0];
        };

        const getServiceCategory = async () => {
            try {
                const response = await axios.get('http://localhost:5000/api/categories');
                categories.value = response.data;
            } catch (err) {
                error.value = 'Reload the page or wait for sometime.';
                showError.value = true;
            }
        };

        const submitForm = async () => {
            if (!resume.value) {
                error.value = 'Please select a file to upload.';
                showError.value = true;
                return;
            }

            try {
                const formData = new FormData();
                formData.append('name', name.value);
                formData.append('email', email.value);
                formData.append('password', password.value);
                formData.append('category', category.value);
                formData.append('service_name', serviceName.value);
                formData.append('resume', resume.value);

                await axios.post('http://127.0.0.1:5000/api/professionals', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                    },
                });

                router.push({ name: "Login" });
            }
            catch (err) {
                error.value = 'An error occurred';
                showError.value = true;
            }
        };  

        onMounted(() => {
            getServiceCategory();
        });

        return {
            name,
            email,
            password,
            serviceName,
            category,
            resume,
            categories,
            error,
            showError,
            hideMessage,
            handleResumeUpload,
            submitForm,
        };
    }
}
</script>