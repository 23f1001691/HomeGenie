<template>
  <div>
    <ProfessionalNav />
    <div class="alert alert-danger" role="alert" v-if="showError">
      {{ error }}
    </div>
    <div class="table-responsive m-3">
      <h4>CLOSED REQUESTS</h4>
      <table class="table table-hover table-bordered">
        <thead>
          <tr>
            <th scope="col" width="20%">ID</th>
            <th scope="col" width="20%">Customer Name</th>
            <th scope="col" width="20%">Date</th>
            <th scope="col" width="20%">Rating</th>
            <th scope="col" width="20%">Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="request in services" :key="request.id">
            <td scope="row">{{ request.id }}</td>
            <td>{{ request.customer_name }}</td>
            <td>{{ request.date_of_completion }}</td>
            <td>ServiceRequest.rating</td>
            <td>
              <div class="btn-group" role="group">
                <button
                  type="button"
                  class="btn btn-info btn-sm"
                  data-bs-toggle="modal"
                  data-bs-target="#viewClosedRequest"
                  @click="viewService(request.id)"
                >
                  View
                </button>
                <div
                  class="modal fade"
                  id="viewClosedRequest"
                  tabindex="-1"
                  aria-labelledby="viewClosedRequestLabel"
                  aria-hidden="true"
                >
                  <div class="modal-dialog modal-dialog-centered">
                    <div class="modal-content">
                      <div class="modal-header">
                        <h1
                          class="modal-title fs-5"
                          id="viewClosedRequestLabel"
                        >
                          Service Request Info
                        </h1>
                        <button
                          type="button"
                          @click="initForm"
                          class="btn-close"
                          data-bs-dismiss="modal"
                          aria-label="Close"
                        ></button>
                      </div>
                      <div class="modal-body">
                        <p>
                          Customer Name: {{ viewClosedService.customer_name }}
                        </p>
                        <p>
                          Service Name: {{ viewClosedService.service_name }}
                        </p>
                        <p>Status: {{ viewClosedService.status }}</p>
                      </div>
                      <div class="modal-footer">
                        <button
                          type="button"
                          @click="initForm"
                          class="btn btn-secondary"
                          data-bs-dismiss="modal"
                        >
                          Close
                        </button>
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
  </div>
</template>

<script>
import ProfessionalNav from "@/components/ProfessionalNav.vue";
import { ref, onMounted, watch, computed } from "vue";
import axios from "axios";
import { useStore } from "vuex";

export default {
  name: "ProfessionalHistory",
  components: {
    ProfessionalNav,
  },
  setup() {
    const services = ref([]);
    const viewClosedService = ref({});
    const error = ref("");
    const showError = ref(false);
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

    const initForm = () => {
      viewClosedService.value = {};
    };

    const closedServices = async () => {
      try {
        const response = await axios.get(
          "http://localhost:5000/api/professional/requests",
          {
            params: {
              status: "closed",
            },
          }
        );
        services.value = response.data.service_requests;
      } catch (err) {
        error.value = err.response?.data?.message || err.message;
        showError.value = true;
      }
    };

    const viewService = async (id) => {
      try {
        const response = await axios.get(
          `http://localhost:5000/api/professional/request/${id}`
        );
        viewClosedService.value = response.data;
      } catch (err) {
        error.value = err.response?.data?.message || err.message;
        showError.value = true;
      }
    };

    onMounted(() => {
      closedServices();
    });

    return {
      services,
      viewService,
      viewClosedService,
      error,
      showError,
      initForm,
    };
  },
};
</script>