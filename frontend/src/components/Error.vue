<template>
    <div class="custom-bg text-dark" v-if="showError" 
        :style="{ height: errorHeight + 'px', border: '1px solid black' }">
        <div class="d-flex justify-content-center px-2 align-items-center">
            <div class="text-center mt-5 pt-3">
                <h4 class="display-1 fw-medium fs-1">{{ title }}</h4>
                <p class="fs-3 mt-4">{{ content }}</p>
            </div>
        </div>
    </div>
</template>

<script setup>
import { defineProps } from 'vue';

const props = defineProps({
  showError: {
    type: Boolean,
    required: true
  },
  title: {
    type: String,
    required: true
  },
  content: {
    type: String,
    required: true
  },
  errorHeight: {
    type: Number,
    required: true
  }
});
</script>

<style scoped>

.custom-bg {
  background: linear-gradient(to right, #e2e8f0, #e5e7eb);
}

@media (prefers-color-scheme: dark) {
  .custom-bg {
    background: linear-gradient(to right, #e2e8f0, #e5e7eb);
      color: black !important;
  }
}

</style>