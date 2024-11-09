<template>
<div class="p-6 max-w-5xl mx-auto bg-gray-100 min-h-screen">
    <button @click="$emit('closePortal')" class="text-blue-500 mb-4">&larr; Back to classes</button>
    
    <h1 class="text-3xl font-bold mb-4">{{ courseName }}</h1>
    
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-4">
    <!-- Live Camera View -->
    <div class="col-span-2">
        <div class="bg-black rounded-lg overflow-hidden relative">
        <img src="https://via.placeholder.com/800x450" alt="Live camera view" class="w-full h-full object-cover" />
        <span class="absolute bottom-2 left-2 bg-red-600 text-white text-sm px-2 py-1 rounded-full">🔴 Live camera view</span>
        </div>
    </div>
    
    <!-- Image to Text Notes -->
    <div>
        <h2 class="text-xl font-semibold mb-2">Image to text notes:</h2>
        <div class="bg-white p-4 rounded-lg shadow-md">
        <p class="text-gray-700 mb-2">Problem 1: A 10m ladder is leaning against a wall. It starts with the top 1m up from ground but starts sliding down...</p>
        <img src="https://via.placeholder.com/300x150" alt="Converted notes" class="rounded-lg mt-2" />
        </div>
    </div>
    </div>
    
    <!-- Captions Section -->
    <div class="mt-6">
    <h2 class="text-xl font-semibold mb-2">Captions</h2>
    <div class="bg-white p-4 rounded-lg shadow-md text-gray-700">
        In theory, we could use exact methods to calculate the best actions the robot should take from every possible position in the maze.
        <br/><br/>
        However, if the maze is enormous, this quickly becomes impractical as it would take forever to compute.
    </div>
    </div>
</div>
</template>
  
<script setup lang="ts">
import { defineProps, defineEmits } from 'vue';

const props = defineProps<{ courseName: string }>();  // Accepts course name as a prop
const emit = defineEmits(['closePortal']);  // Emits an event to close the portal
</script>
