import { createApp } from 'vue'
import './main.css'
import App from './App.vue'
import router from './router'

const app = createApp(App).use(router);
app.mount('#app');