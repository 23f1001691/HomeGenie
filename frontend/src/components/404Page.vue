<template>
    <div class="custom-bg text-dark">
        <div class="d-flex justify-content-center min-vh-100 px-2">
            <!-- <div class="text-center">
                <h1 class="display-1 fw-bold">404</h1>
                <p class="fs-2 fw-medium mt-4">Oops! Page not found</p>
                <p class="mt-4 mb-5">The page you're looking for doesn't exist or has been moved.</p>
                <router-link :to="{ name : 'Home' }" 
                    class="btn btn-light fw-semibold rounded-pill px-4 py-2 custom-btn">
                    Go Home
                </router-link>
            </div> -->
            <div class="text-center mt-5">
                <h1 class="display-1 fw-medium">Sorry!</h1>
                <p class="fs-2 fw-small mt-4">No services available right now.</p>
                <router-link :to="{ name : 'CustomerDashboard', params : { userID:userID } }" 
                    class="btn btn-light fw-semibold rounded-pill px-4 mt-3 py-2 custom-btn">
                    Go Back
                </router-link>
            </div>
        </div>
    </div>
</template>

<script>
import { useStore } from "vuex";
import { computed } from 'vue';


export default {
  name: '404Page',
  setup() {
        const store = useStore();
        const userID = computed(() => {
            return store.state.userID;
        });
        return {
            userID
        };
  }
}
</script>

<style scoped>

.custom-bg {
  background: linear-gradient(to right, #e2e8f0, #e5e7eb);
}

.custom-btn:hover {
  background-color: #f3e8ff !important;
  transition: background-color 0.3s ease-in-out;
}

@media (prefers-color-scheme: dark) {
  .custom-bg {
      background: linear-gradient(to right, #1f2937, #111827);
      color: white !important;
  }

  .custom-btn {
      background-color: #374151 !important;
      color: white !important;
  }

  .custom-btn:hover {
      background-color: #4b5563 !important;
  }
}

</style>