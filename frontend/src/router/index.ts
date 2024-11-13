import { createRouter, createWebHistory } from 'vue-router';

const routes = [
    {
        path: "/", component: () => import("@/components/Home.vue"),
    },
    {
        path: "/students/:studentId", component: () => import("@/components/StudentPortal/StudentPortal.vue"),
    },
    {
        path: "/students/:studentId/request", component: () => import("@/components/StudentPortal/StudentNotetakingRequest.vue"),
    },
    {
        path: "/professors/:professorId", component: () => import("@/components/ProfessorPortal/ProfessorStudentsPortal.vue"),
    },
    {
        path: "/professors/:professorId/courses", component: () => import("@/components/ProfessorPortal/ProfessorCoursePortal.vue"),
    },
    {
        path: "/professors/:professorId/lectures", component: () => import("@/components/ProfessorPortal/ProfessorPublishingPortal.vue"),
    },
    {
        path: "/sdscoordinators/:sdscoordinatorId", component: () => import("@/components/SDSPortal/SDSStudentsPortal.vue"),
    },
    {
        path: "/sdscoordinators/:sdscoordinatorId/courses", component: () => import("@/components/SDSPortal/SDSCoursesPortal.vue"),
    },
    {
        path: "/sdscoordinators/:sdscoordinatorId/professors", component: () => import("@/components/SDSPortal/SDSProfessorsPortal.vue"),
    },
    {
        path: "/tas/:taId", component: () => import("@/components/TAPortal/TAPortal.vue")
    },
    {
        path: "/notepackets/:notepacketId/", component: () => import("@/components/NotePackets/NotePacketView.vue")
    },
    {
        path: "/notepackets/:notepacketId/edit", component: () => import("@/components/NotePackets/NotePacketEditView.vue")
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes: routes
});

export default router;
