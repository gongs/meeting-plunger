import { createRouter, createWebHistory } from 'vue-router';
import { getToken } from '../auth';
import TranscribeHome from '../views/TranscribeHome.vue';
import RacingGame from '../views/RacingGame.vue';
import Login from '../views/Login.vue';
import Register from '../views/Register.vue';
import VenueList from '../views/VenueList.vue';
import VenueRoom from '../views/VenueRoom.vue';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'transcribe', component: TranscribeHome },
    { path: '/racing', name: 'racing', component: RacingGame },
    { path: '/login', name: 'login', component: Login },
    { path: '/register', name: 'register', component: Register },
    {
      path: '/venues',
      name: 'venues',
      component: VenueList,
      meta: { requiresAuth: true },
    },
    {
      path: '/venue/:id',
      name: 'venue',
      component: VenueRoom,
      meta: { requiresAuth: true },
    },
  ],
});

router.beforeEach((to) => {
  if (to.meta.requiresAuth && !getToken()) {
    return { name: 'login', query: { redirect: to.fullPath } };
  }
  return true;
});

export default router;
