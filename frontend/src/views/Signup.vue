<template>
    <div>
        <NavBar />
        <div class="container-fluid d-flex vh-100 w-100">
        <div class="signup d-flex justify-content-center align-items-center flex-column w-50 v-100">
            <h2>For Customers</h2>
            <router-link :to="{ name : 'CustomerSignup' }" class="btn btn-secondary text-uppercase my-3">Register</router-link>
            <p class="text-center my-3">Already have an account? <router-link :to="{ name : 'Login' }">Login</router-link></p>
        </div>
        <div class="signup d-flex justify-content-center align-items-center flex-column w-50 v-100">
            <h2>For Professionals</h2>
            <router-link :to="{ name : 'ProfessionalSignup' }" class="btn btn-secondary text-uppercase my-3">Register</router-link>
            <p class="text-center my-3">Already have an account? <router-link :to="{ name : 'Login' }">Login</router-link></p>
        </div>
        </div>
    </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue';

export default {
  name: 'Signup',
  components: {
    NavBar,
  }
}
</script>