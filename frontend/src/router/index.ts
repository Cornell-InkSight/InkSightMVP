import { createRouter, createWebHistory } from 'vue-router';

const routes = [
    {
        path: "/", component: () => import("@/components/Home.vue"),
    },
    {
        path: "/students/:studentId", component: () => import("@/components/StudentPortal.vue"),
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes: routes
});

export default router;
