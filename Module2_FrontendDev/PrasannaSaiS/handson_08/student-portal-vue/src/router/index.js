import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import CoursesView from '../views/CoursesView.vue';
import ProfileView from '../views/ProfileView.vue';
import CourseDetailView from '../views/CourseDetailView.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/courses',
      name: 'courses',
      component: CoursesView
    },
    {
      path: '/profile',
      name: 'profile',
      component: ProfileView
    },
    {
      path: '/courses/:id',
      name: 'course-detail',
      component: CourseDetailView
    }
  ]
});

// Navigation guard (Task 2)
router.beforeEach((to, from) => {
  console.log(`Navigating to: ${to.path}`);
});

export default router;
