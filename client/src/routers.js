import { createRouter, createWebHistory } from "vue-router";
import HomePage from './components/HomePage.vue'
import UserLogin from './components/UserLogin.vue'
import UserDashboard from './components/UserDashboard.vue'
import UserSignup from './components/UserSignup.vue'
import AdminLogin from "./components/AdminLogin.vue";
import CreatorDashboard from "./components/CreatorDashboard.vue";
import UpdatAlbum from "./components/UpdatAlbum.vue";
import AddSongs from "./components/AddSongs.vue";
import UpdateSong from "./components/UpdateSong.vue";
import RegisterCreator from "./components/RegisterCreator.vue";
import ViewAll from "./components/ViewAll.vue";
import AlbumSong from "./components/AlbumSong.vue";
import OneSong from "./components/OneSong.vue";
import AdminDashboard from "./components/AdminDashboard.vue";
import FlagSong from "./components/FlagSong.vue";
import SearchSA from "./components/SearchSA.vue";

const routes = [
    {
        path: '/',
        name: 'homepage',
        component: HomePage
    },
    {
        path: '/login',
        name: 'userlogin',
        component: UserLogin
    },
    {
        path: '/signup',
        name: 'usersignup',
        component: UserSignup
    },
    {
        path: '/adminlogin',
        name: 'adminlogin',
        component: AdminLogin
    },
    {
        path: '/registercreator',
        name: 'registercreator',
        component: RegisterCreator
    },
    {
        path: '/creatordashboard',
        name: 'creatordashboard',
        component: CreatorDashboard
    },
    {
        path: '/userdashboard',
        name: 'userdashboard',
        component: UserDashboard,
    },
    {
        path: '/admindashboard',
        name: 'admindashboard',
        component: AdminDashboard,
    },
    {
        path: '/updatealbum/:Album_id',
        name: 'updatealbum',
        component: UpdatAlbum,
        props: true,
    },
    {
        path: '/addsong/:Album_id',
        name: 'addsong',
        component: AddSongs,
        props: true,
    },
    {
        path: '/updatesong/:Song_id',
        name: 'updatesong',
        component: UpdateSong,
        props: true,
    },
    {
        path: '/song/:Song_id',
        name: 'song',
        component:OneSong,
        props: true,
    },
    {
        path: '/viewall/:what/:ID',
        name: 'viewall',
        component: ViewAll,
        props: true,
    },
    {
        path: '/albumsong/:Name/:ID',
        name: 'albumsong',
        component: AlbumSong,
        props: true,
    },
    {
        path: '/flagsong',
        name: 'flagsong',
        component: FlagSong,
    },
    {
        path: '/search/:What',
        name: 'search',
        component: SearchSA,
        props: true,
    },
]


const router = createRouter({
    history: createWebHistory(),
    routes,
})

export default router;