import { createRouter, createWebHistory } from 'vue-router';
import TranscribeHome from '../views/TranscribeHome.vue';
import RacingGame from '../views/RacingGame.vue';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'transcribe', component: TranscribeHome },
    { path: '/racing', name: 'racing', component: RacingGame },
  ],
});

export default router;
