import { createApp } from 'vue'
import './main.css'
import App from './App.vue'
import router from './router'
import VueTippy from 'vue-tippy'
import VueSweetalert2 from 'vue-sweetalert2';
import 'sweetalert2/dist/sweetalert2.min.css';
import '@fortawesome/fontawesome-free/css/all.css';

const app = createApp(App).use(router);
app.use(
    VueTippy,
    {
        directive: 'tippy',
        component: 'tippy',
    }
)
app.use(VueSweetalert2);

  
app.mount('#app');