import { createRouter, createWebHistory } from 'vue-router';

const routes = [
    {
        path: "/", component: () => import("@/components/Home.vue"),
    },
    {
        path: "/auth/callback", component: () => import("@/components/Authentication/LoginRedirect.vue")
    },
    {
        path: "/signin", component: () => import("@/components/Authentication/SignIn.vue"),
    },
    {
        path: "/students", component: () => import("@/components/StudentPortal/StudentPortal.vue"),
    },
    {
        path: "/students/request", component: () => import("@/components/StudentPortal/StudentNotetakingRequest.vue"),
    },
    {
        path: "/students/:courseId/lecture", component: () => import("@/components/StudentPortal/StudentRecordingView.vue"),
    },    
    {
        path: "/students/hub", component: () => import("@/components/StudentPortal/StudentRecordingHub.vue"),
    },    
    { 
        path: "/professors", component: () => import("@/components/ProfessorPortal/ProfessorStudentsPortal.vue"),
    },
    {
        path: "/professors/courses", component: () => import("@/components/ProfessorPortal/ProfessorCoursePortal.vue"),
    },
    {
        path: "/professors/lectures", component: () => import("@/components/ProfessorPortal/ProfessorPublishingPortal.vue"),
    },
    {
        path: "/sdscoordinators", component: () => import("@/components/SDSPortal/SDSStudentsPortal.vue"),
    },
    {
        path: "/sdscoordinators/courses", component: () => import("@/components/SDSPortal/SDSCoursesPortal.vue"),
    },
    {
        path: "/sdscoordinators/professors", component: () => import("@/components/SDSPortal/SDSProfessorsPortal.vue"),
    },
    {
        path: "/tas", component: () => import("@/components/TAPortal/TAPortal.vue")
    },
    {
        path: "/notepackets/:notepacketId/", component: () => import("@/components/NotePackets/NotePacketView.vue")
    },
    {
        path: "/notepackets/:notepacketId/edit", component: () => import("@/components/NotePackets/NotePacketEditView.vue")
    },
    {
        path: "/studentnotepackets/:notepacketId/", component: () => import("@/components/NotePackets/StudentNotePacketView.vue")
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes: routes
});

router.beforeEach((to, from, next) => {
    const authToken = localStorage.getItem("authToken");

    if (to.meta.requiresAuth && !authToken) {
        next("/signin");
    } else {
        next();
    }
});  

export default router;

