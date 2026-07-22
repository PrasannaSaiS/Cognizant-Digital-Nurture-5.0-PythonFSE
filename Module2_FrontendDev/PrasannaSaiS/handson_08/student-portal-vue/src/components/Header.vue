<script setup>
import { RouterLink } from 'vue-router'
import { useEnrollmentStore } from '../stores/enrollment'

const store = useEnrollmentStore()
</script>

<template>
  <header class="site-header glass">
    <RouterLink to="/" class="site-title">Student Portal</RouterLink>
    <nav aria-label="Primary navigation">
      <ul class="nav-links">
        <li><RouterLink to="/">Home</RouterLink></li>
        <li>
          <RouterLink to="/courses">
            Courses
            <span v-if="store.enrolledCourses.length > 0" class="badge">
              {{ store.enrolledCourses.length }}
            </span>
          </RouterLink>
        </li>
        <li><RouterLink to="/profile">Profile</RouterLink></li>
      </ul>
    </nav>
  </header>
</template>
