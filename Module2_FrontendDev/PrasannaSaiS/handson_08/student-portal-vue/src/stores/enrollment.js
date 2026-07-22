import { ref, computed } from 'vue';
import { defineStore } from 'pinia';

export const useEnrollmentStore = defineStore('enrollment', () => {
  const enrolledCourses = ref([]);

  const totalCredits = computed(() => {
    return enrolledCourses.value.reduce((sum, course) => sum + course.credits, 0);
  });

  const enroll = (course) => {
    if (!enrolledCourses.value.some(c => c.id === course.id)) {
      enrolledCourses.value.push(course);
    }
  };

  const unenroll = (courseId) => {
    enrolledCourses.value = enrolledCourses.value.filter(c => c.id !== courseId);
  };

  return { enrolledCourses, totalCredits, enroll, unenroll };
});
