<script setup>
import { ref, computed, onMounted } from 'vue'
import { useEnrollmentStore } from '../stores/enrollment'
import CourseCard from '../components/CourseCard.vue'

const courses = ref([])
const searchTerm = ref('')
const loading = ref(true)
const error = ref(null)

const store = useEnrollmentStore()

onMounted(async () => {
  try {
    loading.value = true
    error.value = null
    const response = await fetch('https://jsonplaceholder.typicode.com/posts')
    if (!response.ok) throw new Error('API fetch failed')
    const data = await response.json()
    const grades = ['A', 'B+', 'A-', 'B', 'A']
    courses.value = data.slice(0, 5).map((post, idx) => ({
      id: post.id,
      name: post.title.split(' ').slice(0, 2).map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' '),
      code: `CS10${post.id}`,
      credits: (post.id % 3) + 2,
      grade: grades[idx % grades.length]
    }))
  } catch (err) {
    error.value = err.message
    // Fallback to static 5 courses
    courses.value = [
      { id: 1, name: 'Data Structures', code: 'CS101', credits: 4, grade: 'A' },
      { id: 2, name: 'Database Systems', code: 'CS102', credits: 3, grade: 'B+' },
      { id: 3, name: 'Web Development', code: 'CS103', credits: 4, grade: 'A-' },
      { id: 4, name: 'Cloud Computing', code: 'CS104', credits: 3, grade: 'B' },
      { id: 5, name: 'UI/UX Design', code: 'CS105', credits: 2, grade: 'A' }
    ]
  } finally {
    loading.value = false
  }
})

const filteredCourses = computed(() => {
  const query = searchTerm.value.trim().toLowerCase()
  return courses.value.filter(c => 
    c.name.toLowerCase().includes(query) || 
    c.code.toLowerCase().includes(query)
  )
})

const isEnrolled = (courseId) => {
  return store.enrolledCourses.some(c => c.id === courseId)
}
</script>

<template>
  <div class="page-container">
    <h2 class="section-title">Course Catalog</h2>
    
    <div class="controls-container">
      <input
        type="text"
        class="search-input glass"
        placeholder="Search courses by name or code..."
        v-model="searchTerm"
      />
    </div>

    <div v-if="loading" class="state-message">
      <div class="loading-spinner"></div>
      <p>Loading course information from API...</p>
    </div>

    <div v-else-if="error" class="state-message">
      <p class="error-text">Failed to fetch courses: {{ error }}</p>
      <p>Showing offline fallback data.</p>
      <div class="course-grid" style="margin-top: 1.5rem">
        <CourseCard
          v-for="course in filteredCourses"
          :key="course.id"
          v-bind="course"
          :isEnrolled="isEnrolled(course.id)"
          @enroll="store.enroll(course)"
        />
      </div>
    </div>

    <div v-else class="course-grid">
      <template v-if="filteredCourses.length > 0">
        <CourseCard
          v-for="course in filteredCourses"
          :key="course.id"
          v-bind="course"
          :isEnrolled="isEnrolled(course.id)"
          @enroll="store.enroll(course)"
        />
      </template>
      <div v-else class="state-message">
        <p>No courses matched your search criteria.</p>
      </div>
    </div>
  </div>
</template>
