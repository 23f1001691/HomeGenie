<template>
    <div v-if="props.isOpen" class="modal-overlay">
        <div class="modal-content">
            <header class="modal-header">
                <h2 class="modal-title">{{ props.title }}</h2>
            </header>
            <div class="modal-body">
                <slot></slot>
            </div>
            <footer class="modal-footer">
                <button :class="['btn', 'btn-md', 'green']" @click="closeModal" :disabled=false>{{ props.buttonName }}</button>
            </footer>
        </div>
    </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';

const props = defineProps({
    isOpen: {
        type: Boolean,
        default: false,
    },
    title: {
        type: String,
    },
    buttonName: {
        type: String
    },
    disabled: { 
        type: Boolean,
        default: false
    }

});

const emit = defineEmits();

const closeModal = () => {
    emit('close');
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.3s forwards;
}

.modal-content {
  background: #ffffff;
  border-radius: 12px;
  width: 90%;
  max-width: 500px;
  max-height: 80vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
  position: relative;
  overflow: hidden;
  /* Important for fixed footer */
}

.modal-header {
  padding: 15px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #e0e0e0;
  background-color: #f9f9f9;
}

.modal-title {
  font-size: 1.6em;
  color: #333;
  font-weight: 600;
}

.close-btn {
  font-size: 24px;
  cursor: pointer;
  background: none;
  border: none;
  color: #999;
  transition: color 0.3s;
}

.close-btn:hover {
  color: #ff4d4d;
}

.modal-body {
  padding: 20px;
  overflow-y: auto;
  flex-grow: 1;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  padding: 15px 20px;
  border-top: 1px solid #e0e0e0;
  background-color: #f9f9f9;
  position: sticky;
  bottom: 0;
}

.red {
  color: rgb(39, 39, 39);
  font-weight: 700;
  border-color: rgba(28, 28, 28, 0.133);
  background-color: rgba(227, 24, 24, 0.707);
}

.red:hover {
  background-color: rgba(227, 24, 24, 1);
}

.green {
  color: rgb(39, 39, 39);
  font-weight: 700;
  border-color: rgba(28, 28, 28, 0.133);
  background-color: rgba(95, 227, 24, 0.707);
}

.green:hover {
  background-color: rgba(95, 227, 24, 1);
}

.cancel-btn {
  padding: 10px 20px;
  border-radius: 8px;
  font-size: 0.9rem;
  cursor: pointer;
  border: none;
  transition: background-color 0.3s;
  background-color: #f0f0f0;
  color: #333;
}

.cancel-btn:hover {
  background-color: #e0e0e0;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }

  to {
    opacity: 1;
  }
}
</style>