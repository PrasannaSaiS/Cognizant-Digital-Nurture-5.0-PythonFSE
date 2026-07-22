<script setup>
defineProps({
  id: Number,
  name: String,
  code: String,
  credits: Number,
  grade: String,
  isEnrolled: Boolean
})

const emit = defineEmits(['enroll'])
</script>

<template>
  <article class="course-card glass">
    <div class="course-header">
      <h3 class="course-title">{{ name }}</h3>
      <span class="course-code">{{ code }}</span>
    </div>
    
    <div class="course-details">
      <div class="course-detail-item">
        Credits: <strong>{{ credits }}</strong>
      </div>
      <div class="course-detail-item">
        Grade: <strong class="grade-badge">{{ grade }}</strong>
      </div>
    </div>
    
    <button 
      class="btn btn-primary" 
      @click="emit('enroll')"
      :disabled="isEnrolled"
    >
      {{ isEnrolled ? 'Enrolled' : 'Enroll' }}
    </button>
  </article>
</template>
