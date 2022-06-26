import Vue from 'vue';
import VueRouter from 'vue-router';
import Home from '../views/Home.vue';
import Ping from '../components/Ping.vue';
import Users from '../components/Users.vue';
import Links from '../components/Links.vue';
import Tree from '../components/Tree.vue';
import Familytree from '../components/Familytree.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue'),
  },
  {
    path: '/ping',
    name: 'Ping',
    component: Ping,
  },
  {
    path: '/users',
    name: 'Users',
    component: Users,
  },
  {
    path: '/links',
    name: 'Links',
    component: Links,
  },
  {
    path: '/tree',
    name: 'Tree',
    component: Tree,
  },
  {
    path: '/familytree',
    name: 'Familytree',
    component: Familytree,
  },
];

const router = new VueRouter({
  routes,
});

export default router;
