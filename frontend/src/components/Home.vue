<template>
    <div class="min-h-screen flex items-center justify-center bg-gray-100">
      <div class="w-full max-w-md p-8 space-y-6 bg-white rounded-lg shadow-lg">
        <h2 class="text-3xl font-bold text-gray-900 text-center">Welcome back!</h2>
        
        <!-- Email and Password Fields -->
        <form class="space-y-4">
          <div>
            <label for="email" class="sr-only">Email address</label>
            <input 
              id="email" 
              name="email" 
              type="email" 
              placeholder="student@cornell.edu" 
              class="w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring focus:border-blue-300" 
            />
          </div>
          
          <div>
            <label for="password" class="sr-only">Password</label>
            <input 
              id="password" 
              name="password" 
              type="password" 
              placeholder="••••••••" 
              class="w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring focus:border-blue-300" 
            />
          </div>
          
          <!-- Login Button -->
          <button 
            type="submit" 
            class="w-full py-2 bg-black text-white font-semibold rounded-md hover:bg-gray-800"
          >
            Log in
          </button>
        </form>
        
        <!-- Divider -->
        <div class="flex items-center justify-center space-x-2 text-gray-400 mt-4">
          <span class="w-1/4 border-b"></span>
          <span>Or</span>
          <span class="w-1/4 border-b"></span>
        </div>
        
        <!-- Social Login Options -->
        <div class="flex space-x-4 mt-4">
          <button class="flex-1 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-100">
            Google
          </button>
          <button class="flex-1 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-100">
            Cornell NetID
          </button>
        </div>
        
        <!-- Create New Account Link -->
        <div class="text-center mt-4 text-gray-500">
          Or, <a href="#" class="text-blue-600 hover:underline font-semibold">create a new account</a>
        </div>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  // No authentication logic added yet, as per instructions
  </script>
  