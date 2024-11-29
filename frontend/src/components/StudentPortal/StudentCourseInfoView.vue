<template>
<!-- Course Details -->
<div class="border p-4 rounded-lg bg-gray-50">
    <!-- Request Status -->
    <div class="mb-4">
    <h3 class="text-sm font-semibold text-gray-700">Request Status:</h3>
    <p class="text-sm" :class="course.isApprovedForCourse ? 'text-green-600' : 'text-yellow-600'">
        {{ course.isApprovedForCourse ? 'Approved' : 'Pending Approval' }}
    </p>
    </div>

    <!-- Course Information -->
    <div class="mb-4">
    <h3 class="text-sm font-semibold text-gray-700">Course Information:</h3>
    <ul class="text-sm text-gray-600 space-y-1">
        <li><strong>Term:</strong> {{ course.term }}</li>
        <li><strong>Course ID:</strong> {{ course.course_uid }}</li>
        <li><strong>Type:</strong> {{ course.type }}</li>
        <li><strong>Campus:</strong> {{ course.campus }}</li>
        <li><strong>Meeting Time:</strong> {{ course.meeting_time }}</li>
    </ul>
    </div>
</div>
</template>

<script setup>
const props = defineProps({
course: {
    type: Object,
    required: true,
},
});
</script>