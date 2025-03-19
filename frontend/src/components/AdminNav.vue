<template>
  <div>
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
      <div class="container-fluid">
        <router-link :to="{ name: 'AdminDashboard' }" class="navbar-brand">HomeGenie</router-link>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarTogglerDemo02"
          aria-controls="navbarTogglerDemo02" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarTogglerDemo02">
          <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
            <li class="nav-item px-3" style="align-self: center; display: flex; align-items: center" @click="createCSV">
              <i class="fa-solid fa-circle-down" style="font-size: 20px; margin-right: 10px"></i>
              <span>Export CSV</span>
            </li>
            <li class="nav-item px-3" style="align-self: center">
              <router-link :to="{ name: 'Services' }" class="nav-link">Services</router-link>
            </li>
            <li class="nav-item px-3" style="align-self: center">
              <router-link :to="{ name: 'Users' }" class="nav-link">Users</router-link>
            </li>
            <li class="nav-item px-3 menu">
              <button @click="toggleDropdown" class="menu-icon">
                <img class="img-profile rounded-circle" src="../assets/undraw_profile.svg"
                  style="width: 35px; height: 35px" />
              </button>

              <div v-if="showDropdown" class="dropdown-menu">
                <button @click="handleLogout" class="dropdown-item">
                  Logout
                </button>
              </div>
            </li>
          </ul>
        </div>
      </div>
    </nav>
    <div class="alert alert-danger" role="alert" v-if="showError">
      {{ error }}
    </div>
    <div class="alert alert-success" role="alert" v-if="showMessage">
      {{ message }}
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
  /* background-color: white; */
  /* border: 1px solid #ccc; */
  /* border-radius: 4px; */
  /* padding: 0.5em; */
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
import { ref, watch } from "vue";
import axios from "axios";
import useAuth from "@/composables/useAuth";

export default {
  name: "AdminNav",
  setup() {
    const showDropdown = ref(false);
    const { error, showError, logOutUser } = useAuth();
    const showMessage = ref(false);
    const message = ref("");

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
      error.value = "";
      message.value = "";
      showMessage.value = false;
    };

    const toggleDropdown = () => {
      showDropdown.value = !showDropdown.value;
    };

    const handleLogout = () => {
      logOutUser(showDropdown);
    };

    const createCSV = async () => {
      try {
        const response = await axios.get("http://localhost:5000/admin/create-csv");
        const task_id = response.data.task_id;
        const interval = setInterval(async () => {
          try {
            const res = await axios.get(`http://localhost:5000/admin/get-csv/${task_id}`);

            if (res.status == 200) {
              window.open(`http://localhost:5000/admin/get-csv/${task_id}`);
              message.value = "File is downloaded successfully!";
              showMessage.value = true;
              clearInterval(interval);
            }
          }
          catch (err) {
            console.error('Error fetching CSV task:', err);

            if (err.response && err.response.data) {
              error.value = err.response.data.message || 'An unexpected error occurred.';
            }
            else {
              error.value = 'An unexpected error occurred.';
            }
            showError.value = true;
            clearInterval(interval);
          }
        }, 1000);
      }
      catch (err) {
        console.error('Error creating CSV:', err);

        if (err.response && err.response.data) {
          error.value = err.response.data.message || 'An error occurred while creating the CSV.';
        } else {
          error.value = 'An unexpected error occurred.';
        }
        showError.value = true;
      }
    };

    return {
      message,
      showMessage,
      error,
      showError,
      showDropdown,
      toggleDropdown,
      handleLogout,
      createCSV,
    };
  },
};
</script>
