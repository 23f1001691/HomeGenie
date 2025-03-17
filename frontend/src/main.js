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

createApp(App).use(store).use(router).mount('#app')
