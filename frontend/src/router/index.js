// router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import CoverManagement from '../views/CoverManagement.vue';
import model from "@/views/model.vue";
import upload from "@/views/upload.vue";
import Login from  "@/views/Login.vue";
import app2 from "@/views/app2.vue";
import video from "@/views/video.vue"
import App from "@/App.vue";
const routes = [
    {
        path: '/app',
        name: 'app2',
        component: app2
    },
    {
        path: '/covers',
        name: 'CoverManagement',
        component: CoverManagement
    }
    ,
    {
        path: '/model',
        name: 'model',
        component: model
    }
    ,
    {
        path: '/ab',
        name: 'upload',
        component: upload
    },

    {
        path: '/home',
        name: 'Home',
        component: Home
    }
    ,
    {
        path: '/',
        name: 'Login',
        component: Login
    },
    {
        path: '/video',
        name: 'video',
        component: video
    }
    // ...其他路由...
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
