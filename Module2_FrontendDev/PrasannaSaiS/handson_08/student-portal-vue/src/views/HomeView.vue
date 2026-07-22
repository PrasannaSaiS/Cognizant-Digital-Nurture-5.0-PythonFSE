<script setup>
import { RouterLink } from 'vue-router'
import { useEnrollmentStore } from '../stores/enrollment'

const store = useEnrollmentStore()
</script>

<template>
  <div class="page-container">
    <section class="hero">
      <h1>Welcome to your Vue Student Dashboard</h1>
      <p>Manage your academic journey, track course enrollments, and update your profile.</p>
    </section>

    <div class="home-dashboard">
      <div class="stat-card glass">
        <h3>Enrolled Courses</h3>
        <p class="stat-val">{{ store.enrolledCourses.length }}</p>
        <p style="color: var(--text-secondary)">Currently active courses</p>
        <RouterLink to="/profile" class="btn btn-primary" style="margin-top: 1.5rem; text-decoration: none">
          View Enrolled List
        </RouterLink>
      </div>

      <div class="stat-card glass">
        <h3>Total Credits</h3>
        <p class="stat-val">{{ store.totalCredits }}</p>
        <p style="color: var(--text-secondary)">Earned towards graduation</p>
        <RouterLink to="/courses" class="btn btn-primary" style="margin-top: 1.5rem; text-decoration: none">
          Explore Courses
        </RouterLink>
      </div>

      <div class="stat-card glass">
        <h3>Profile Status</h3>
        <p class="stat-val" style="font-size: 1.75rem; margin: 1.1rem 0">Verified</p>
        <p style="color: var(--text-secondary)">Semester 4 Student</p>
        <RouterLink to="/profile" class="btn btn-primary" style="margin-top: 1.5rem; text-decoration: none">
          Edit Profile
        </RouterLink>
      </div>
    </div>
  </div>
</template>
