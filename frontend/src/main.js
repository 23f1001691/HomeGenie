import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from "axios";
import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap"
import "./assets/main.css";

axios.defaults.withCredentials = true;
axios.defaults.headers.common["Content-Type"] = "application/json";

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
}

axios.interceptors.request.use(
  (config) => {
    const csrfToken = getCookie("csrf_access_token");
    if (csrfToken) {
      config.headers["X-CSRF-TOKEN"] = csrfToken;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

createApp(App).use(store).use(router).mount('#app')
