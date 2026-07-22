<script setup>
import { ref } from 'vue'
import { RouterLink } from 'vue-router'
import { useEnrollmentStore } from '../stores/enrollment'

const store = useEnrollmentStore()

const profile = ref({
  name: 'John Doe',
  email: 'john.doe@example.com',
  semester: '4'
})
</script>

<template>
  <div class="page-container" style="display: flex; flex-direction: column; gap: 2.5rem">
    
    <!-- Profile Form Section -->
    <section class="profile-card glass" id="profile">
      <h2 class="section-title">Student Profile</h2>
      
      <div class="form-group">
        <label for="name-input">Full Name</label>
        <input
          id="name-input"
          type="text"
          class="form-control"
          v-model="profile.name"
          placeholder="Enter your name"
        />
      </div>

      <div class="form-group">
        <label for="email-input">Email Address</label>
        <input
          id="email-input"
          type="email"
          class="form-control"
          v-model="profile.email"
          placeholder="Enter your email"
        />
      </div>

      <div class="form-group">
        <label for="semester-input">Current Semester</label>
        <select
          id="semester-input"
          class="form-control"
          v-model="profile.semester"
        >
          <option value="1">Semester 1</option>
          <option value="2">Semester 2</option>
          <option value="3">Semester 3</option>
          <option value="4">Semester 4</option>
          <option value="5">Semester 5</option>
          <option value="6">Semester 6</option>
          <option value="7">Semester 7</option>
          <option value="8">Semester 8</option>
        </select>
      </div>

      <div class="profile-summary">
        <h3>Live Profile View</h3>
        <p>Name: <strong>{{ profile.name || 'N/A' }}</strong></p>
        <p>Email: <strong>{{ profile.email || 'N/A' }}</strong></p>
        <p>Semester: <strong>Semester {{ profile.semester }}</strong></p>
      </div>
    </section>

    <!-- Enrolled Courses Section (Pinia store integration) -->
    <section class="profile-card glass" style="max-width: 800px">
      <h2 class="section-title">My Enrolled Courses</h2>
      
      <div v-if="store.enrolledCourses.length === 0" class="state-message" style="border-style: solid">
        <p style="color: var(--text-secondary)">You are not enrolled in any courses yet.</p>
        <RouterLink to="/courses" class="btn btn-primary" style="margin-top: 1.5rem; width: auto; display: inline-flex; text-decoration: none">
          Browse & Enroll in Courses
        </RouterLink>
      </div>

      <div v-else>
        <div class="course-grid">
          <article v-for="course in store.enrolledCourses" :key="course.id" class="course-card glass" style="border: 1px solid rgba(255,255,255,0.05)">
            <div class="course-header">
              <h3 class="course-title">{{ course.name }}</h3>
              <span class="course-code">{{ course.code }}</span>
            </div>
            
            <div class="course-details">
              <div class="course-detail-item">
                Credits: <strong>{{ course.credits }}</strong>
              </div>
              <div class="course-detail-item">
                Grade: <strong class="grade-badge">{{ course.grade }}</strong>
              </div>
            </div>

            <div style="display: flex; gap: 0.5rem; margin-top: 1rem">
              <RouterLink 
                :to="`/courses/${course.id}`" 
                class="btn" 
                style="flex: 1; backgroundColor: rgba(99, 102, 241, 0.1); color: var(--accent-primary); text-decoration: none; border: 1px solid rgba(99,102,241,0.2)"
              >
                Details
              </RouterLink>
              <button 
                class="btn btn-danger" 
                style="flex: 1"
                @click="store.unenroll(course.id)"
              >
                Remove
              </button>
            </div>
          </article>
        </div>

        <div style="margin-top: 1.5rem; padding-top: 1rem; border-top: 1px solid var(--border-color); text-align: right">
          <p style="font-size: 1.15rem; font-weight: bold">
            Total Credits: <span style="color: var(--accent-primary)">{{ store.totalCredits }}</span>
          </p>
        </div>
      </div>
    </section>
  </div>
</template>
