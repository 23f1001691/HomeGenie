<template>
    <div>
        <nav class="navbar navbar-expand-lg bg-body-tertiary">
            <div class="container-fluid">
                <router-link :to="{ name : 'CustomerDashboard', params : { userID:userID } }" class="navbar-brand">HomeGenie</router-link>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarTogglerDemo02"
                    aria-controls="navbarTogglerDemo02" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarTogglerDemo02">
                    <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
                        <li class="nav-item px-3" style="align-self: center;">
                            <router-link :to="{ name : 'BookServices', params : { userID:userID } }" class="nav-link">Book Service</router-link>
                        </li>
                        <li class="nav-item px-3" style="align-self: center;">
                            <router-link :to="{ name : 'CustomerRequests', params : { userID:userID } }" class="nav-link">Service Requests</router-link>                       
                        </li>
                        <li class="nav-item px-3 menu">
                            <button @click="toggleDropdown" class="menu-icon">
                                <img class="img-profile rounded-circle" src="../assets/undraw_profile.svg"
                                    style="width: 35px; height: 35px;">
                            </button>

                            <div v-if="showDropdown" class="dropdown-menu">
                                <button @click="handleLogout" class="dropdown-item">Logout</button>
                            </div>
                        </li>
                    </ul>
                </div>
            </div>
        </nav>
        <div class="alert alert-danger" role="alert" v-if="showError">
            {{ error }}
        </div>
    </div> 
</template>

<style scoped>
.menu {
  position: relative;
}

.menu-icon {
  background: none;
  border: none;
  font-size: 13px;
  cursor: pointer;
}

.dropdown-menu {
  display: block !important;
  position: absolute;
  top: 4em;
  right: 0;
  font-size: 13px;
}

.dropdown-item {
  display: block;
  /* padding: 0.5em 0.5em; */
  cursor: pointer;
  /* width: 100%; */
  text-align: left;
}

.dropdown-item:hover {
  background-color: #f0f0f0;
}

/* .dropdown-menu {
    right: 0 !important;
} */

.navbar {
    position: relative;
    z-index: 1000;
}

.container-fluid {
    overflow: visible;
}
</style>

<script>
import { ref, computed, watch } from 'vue';
import useAuth from '@/composables/useAuth';
import { useStore } from "vuex";

export default {
    name: 'CustomerNav',
    setup() {
        const showDropdown = ref(false);
        const { error, showError, logOutUser } = useAuth();
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
            error.value = "";
        };

        const userID = computed(() => {
            return store.state.userID;
        });

        const role = computed(() => {
            return store.state.role;
        });

        const toggleDropdown = () => {
            showDropdown.value = !showDropdown.value;
        };

        const handleLogout = () => {
            logOutUser(showDropdown);
        };

        return {
            userID,
            role,
            error,
            showError,
            showDropdown,
            toggleDropdown,
            handleLogout
        };
    },
}
</script>