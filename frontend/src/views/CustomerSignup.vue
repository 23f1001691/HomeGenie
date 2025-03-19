<template>
    <div>
        <NavBar />
        <div class="alert alert-danger" role="alert" v-if="showError">
            {{ error }}
        </div>
        <div class="container-fluid">
            <div class="form-container mt-3">
                <h4 class="text-center text-uppercase">Customer Signup</h4>
                <br />
                <form @submit.prevent="submitForm">
                    <div class="mb-2 row g-3 align-items-center">
                        <div class="col-auto">
                            <label for="name" class="col-form-label">Full Name</label>
                        </div>
                        <div class="col-auto">
                            <input type="text" class="form-control" id="name" v-model="name" required />
                        </div>
                    </div>
                    <div class="mb-2 row g-3 align-items-center">
                        <div class="col-auto">
                            <label for="email" class="col-form-label">Email</label>
                        </div>
                        <div class="col-auto">
                            <input type="email" class="form-control" id="email" v-model="email" required />
                        </div>
                    </div>
                    <div class="mb-3 row g-3 align-items-center">
                        <div class="col-auto">
                            <label for="password" class="col-form-label">Password</label>
                        </div>
                        <div class="col-auto">
                            <input type="password" class="form-control" id="password" v-model="password" required />
                        </div>
                    </div>
                    <div class="mb-3 row g-3 align-items-center">
                        <div class="col-auto">
                            <label for="contactNumber" class="col-form-label">Contact Number</label>
                        </div>
                        <div class="col-auto">
                            <input type="number" class="form-control" id="contactNumber" v-model="contactNumber" required />
                        </div>
                    </div>
                    <button type="submit" class="btn btn-secondary d-md-block mx-auto">
                        Submit
                    </button>
                </form>
                <br />
                <p class="text-center">
                    Already have an account?
                    <router-link :to="{ name: 'Login' }">Login</router-link>
                </p>
            </div>
        </div>
    </div>
</template>

<style scoped>
label {
    width: 150px;
}

input {
    width: 300px;
}
</style>

<script>
import NavBar from "@/components/NavBar.vue";
import axios from "axios";
import { ref, watch } from "vue";
import { useRouter } from "vue-router";

export default {
    name: "CustomerSignup",
    components: {
        NavBar,
    },
    setup() {
        const name = ref('');
        const email = ref('');
        const password = ref('');
        const contactNumber = ref('');
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

        const submitForm = async () => {
            try {
                await axios.post("http://localhost:5000/api/customers", {
                    name: name.value,
                    email: email.value,
                    password: password.value,
                    contact_no: contactNumber.value,
                });
                router.push({ name: "Login" });
            } 
            catch (err) {
                error.value = "An error occurred";
                showError.value = true;
            }
        };

        return {
            name,
            email,
            password,
            contactNumber,
            error,
            showError,
            hideMessage,
            submitForm
        };
    },
};
</script>
