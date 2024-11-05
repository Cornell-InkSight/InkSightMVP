import { createRouter, createWebHashHistory } from 'vue-router';

const routes = [
    {
        path: "/:studentId", component: () => import("@/components/StudentPortal.vue")
    },
]
const router = createRouter({
    history: createWebHashHistory(),
    routes: routes
});
export default router;
