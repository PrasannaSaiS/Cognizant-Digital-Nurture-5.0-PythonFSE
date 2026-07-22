<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter, RouterLink } from 'vue-router'
import { useEnrollmentStore } from '../stores/enrollment'

const route = useRoute()
const router = useRouter()
const store = useEnrollmentStore()

const courseId = route.params.id
const course = ref(null)
const loading = ref(true)

onMounted(async () => {
  try {
    loading.value = true
    const response = await fetch(`https://jsonplaceholder.typicode.com/posts/${courseId}`)
    if (!response.ok) throw new Error('Failed to fetch details')
    const post = await response.json()
    const grades = ['A', 'B+', 'A-', 'B', 'A']
    course.value = {
      id: post.id,
      name: post.title.split(' ').slice(0, 2).map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' '),
      code: `CS10${post.id}`,
      credits: (post.id % 3) + 2,
      grade: grades[post.id % grades.length],
      description: post.body
    }
  } catch (err) {
    const fallbackCourses = [
      { id: 1, name: 'Data Structures', code: 'CS101', credits: 4, grade: 'A' },
      { id: 2, name: 'Database Systems', code: 'CS102', credits: 3, grade: 'B+' },
      { id: 3, name: 'Web Development', code: 'CS103', credits: 4, grade: 'A-' },
      { id: 4, name: 'Cloud Computing', code: 'CS104', credits: 3, grade: 'B' },
      { id: 5, name: 'UI/UX Design', code: 'CS105', credits: 2, grade: 'A' }
    ]
    const numericId = parseInt(courseId, 10)
    const found = fallbackCourses.find(c => c.id === numericId)
    if (found) {
      course.value = {
        ...found,
        description: `This course covers foundational principles of ${found.name} (${found.code}), with an emphasis on practical implementation, standard paradigms, and industry applications.`
      }
    }
  } finally {
    loading.value = false
  }
})

const handleEnroll = () => {
  if (course.value) {
    store.enroll(course.value)
    router.push('/profile')
  }
}
</script>

<template>
  <div class="page-container">
    <div v-if="loading" class="state-message">
      <div class="loading-spinner"></div>
      <p>Loading course details...</p>
    </div>

    <div v-else-if="!course" class="state-message">
      <p class="error-text">Course with ID {{ courseId }} not found.</p>
      <RouterLink to="/courses" class="btn btn-primary" style="margin-top: 1.5rem; width: auto; display: inline-flex; text-decoration: none">
        Back to Courses
      </RouterLink>
    </div>

    <div v-else class="course-detail-container glass">
      <div style="display: flex; justify-content: space-between; align-items: center">
        <h2 style="margin: 0">{{ course.name }}</h2>
        <span class="course-code">{{ course.code }}</span>
      </div>
      
      <div class="detail-row">
        <span>Credits</span>
        <strong>{{ course.credits }} Credits</strong>
      </div>

      <div class="detail-row">
        <span>Expected Grade</span>
        <strong class="grade-badge">{{ course.grade }}</strong>
      </div>

      <div style="margin-top: 1rem">
        <h4 style="margin-bottom: 0.5rem; color: var(--accent-secondary)">Course Description</h4>
        <p style="color: var(--text-secondary); line-height: 1.6">
          {{ course.description }}
        </p>
      </div>

      <div style="display: flex; gap: 1rem; margin-top: 1.5rem">
        <RouterLink to="/courses" class="btn" style="flex: 1; backgroundColor: rgba(255,255,255,0.05); color: var(--text-primary); text-decoration: none; border: 1px solid var(--border-color)">
          Back to Catalog
        </RouterLink>
        <button class="btn btn-primary" style="flex: 1" @click="handleEnroll">
          Enroll & View Profile
        </button>
      </div>
    </div>
  </div>
</template>
