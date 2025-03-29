<template>  
    <div v-if="isVisible" class="modal fade show d-block" tabindex="-1" aria-labelledby="editServiceLabel" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
            <div class="modal-header">
                <h1 class="modal-title fs-5" id="editServiceLabel">Update Service</h1>
                <button type="button" @click="closeModal" class="btn-close" aria-label="Close"></button>
            </div>
            <div class="modal-body">
                <div class="mb-3 row">
                <label for="service_name" class="col-auto col-form-label">Service Name</label>
                <div class="col-auto">
                    <input type="text" class="form-control" id="service_name" v-model="editService.name">
                </div>
                </div>
                <div class="mb-3 row">
                <label for="description" class="col-auto col-form-label">Description</label>
                <div class="col-auto">
                    <input type="text" class="form-control" id="description" v-model="editService.description">
                </div>
                </div>
                <div class="mb-3 row">
                <label for="base_price" class="col-auto col-form-label">Base Price</label>
                <div class="col-auto">
                    <input type="text" class="form-control" id="base_price" v-model="editService.base_price">
                </div>
                </div>
                <div class="mb-3 row">
                <label for="time_req" class="col-auto col-form-label">Time Required</label>
                <div class="col-auto">
                    <input type="text" class="form-control" id="time_req" v-model="editService.time_req">
                </div>
                </div>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-primary" @click="updateService" data-bs-dismiss="modal">Save Changes</button>
            </div>
        </div>
      </div>
    </div>
</template>

<script>
import { ref, watch, onMounted } from 'vue';

export default {
    props: {
        service: {
            type: Object,
            required: true
        },
        isVisible: {
            type: Boolean,
            required: true
        }
    },
    setup(props, { emit }) {
        const editService = ref({
            id: null,
            category_id: null,
            name: '',
            description: '',
            base_price: '',
            time_req: ''
        });

        watch(() => props.service,
            (newService) => {
                editService.value = { ...newService };
            },
            { deep: true }
        );

        const closeModal = () => {
        editService.value = ''
        emit('close');
        };

        const updateService = () => {
        emit('update', editService.value);
        };

        onMounted(() => {
        editService.value = { ...props.service };
        });

        return {
            editService,
            closeModal,
            updateService
        };
    }
};
</script>
  
<style scoped>
.modal {
display: block;
}
</style>
  