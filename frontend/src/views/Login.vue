<template>
    <div>
        <NavBar />
        <div class="alert alert-danger" role="alert" v-if="showError">
            {{ error }}
        </div>
        <div class="container-fluid">
            <div class="form-container mt-3">
                <h4 class="text-center text-uppercase">Login</h4>
                <br>
                <form @submit.prevent="submitForm">
                    <div class="mb-2 row g-3 align-items-center">
                        <div class="col-auto">
                            <label for="email" class="col-form-label">Email</label>
                        </div>
                        <div class="col-auto">
                            <input type="email" class="form-control" id="email" v-model="email" required>
                        </div>
                    </div>
                    <div class="mb-3 row g-3 align-items-center">
                        <div class="col-auto">
                            <label for="password" class="col-form-label">Password</label>
                        </div>
                        <div class="col-auto">
                            <input type="password" class="form-control" id="password" v-model="password" required>
                        </div>
                    </div>
                    <button type="submit" class="btn btn-secondary d-md-block mx-auto">Submit</button>
                </form>
                <br>
                <p class="text-center">Don't have an account?
                    <router-link :to="{ name: 'Signup' }">Signup</router-link>
                </p>
            </div>
        </div>
    </div>
</template>

<style scoped>
label {
    width: 130px;
}

input {
    width: 300px;
}
</style>

<script>
import NavBar from '@/components/NavBar.vue';
import axios from 'axios';
import { ref, watch } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";
axios.defaults.withCredentials = true;

export default {
    name: 'Login',
    components: {
        NavBar,
    },
    setup() {
        const email = ref("");
        const password = ref("");
        const error = ref("");
        const showError = ref(false);
        const router = useRouter();
        const store = useStore();

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

        const submitForm = async () => {
            try {
                const response = await axios.post("http://localhost:5000/auth/login", {
                    email: email.value,
                    password: password.value,
                });

                console.log(response.data)

                const { access_token, role, user_id, is_first_session } = response.data;

                if (!role || !user_id || !access_token) {
                    error.value = "Invalid login response. Please try again.";
                    showError.value = true;
                    
                    return router.push({ name: "Login" });
                }

                store.dispatch('logUser', { role, user_id, is_first_session });

                if (role === 'admin') {
                    router.push({ name: "AdminDashboard" });
                } 
                else if (role === 'customer') {
                    router.push({ name: "CustomerDashboard", params: { userID: user_id } });
                } 
                else if (role === 'professional') {
                    router.push({ name: "ProfessionalDashboard", params: { userID: user_id } });
                } 
                else {
                    error.value = 'Unrecognized role. Please try again.';
                    showError.value = true;
                    
                    return router.push({ name: "Login" });
                }
            }
            catch (err) {
                error.value = err.response?.data?.message || "Error occured.";
                showError.value = true;
            }
        };

        return {
            email,
            password,
            error,
            showError,
            hideMessage,
            submitForm,
        };
    },
}
</script>