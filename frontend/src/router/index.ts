import { createRouter, createWebHistory } from 'vue-router';

const routes = [
    {
        path: "/", component: () => import("@/components/Home.vue"),
    },
    {
        path: "/students/:studentId", component: () => import("@/components/StudentPortal/StudentPortal.vue"),
    },
    {
        path: "/professors/:professorId", component: () => import("@/components/ProfessorPortal/ProfessorPortal.vue"),
    },
    {
        path: "/sdscoordinators/:sdscoordinatorId", component: () => import("@/components/SDSPortal/SDSPortal.vue"),
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes: routes
});

export default router;
