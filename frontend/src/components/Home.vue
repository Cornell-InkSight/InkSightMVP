<template>
    <div class="landing-page">
      <!-- Header -->
      <header class="header">
        <h1 class="title">Inksight</h1>
        <nav class="nav">
          <ul>
            <li><router-link to="/students/1">Students</router-link></li>
            <li><router-link to="/professors/1">Professors</router-link></li>
            <li><router-link to="/sdscoordinators/1">SDS Coordinators</router-link></li>
            <li><router-link to="/tas/1">TAs</router-link></li>
          </ul>
        </nav>
      </header>
  
      <!-- Hero Section -->
      <section class="hero">
        <div class="hero-content">
          <h2>Accessible Note-Taking for STEM Students</h2>
          <p>
            Empowering students with disabilities through real-time, structured, and editable note-taking solutions.
            Inksight bridges the gap in accessibility, capturing everything from mathematical equations to lecture notes.
          </p>
          <button class="cta-button">Learn More</button>
        </div>
      </section>
  
      <!-- Features Section -->
      <section class="features">
        <div class="feature">
          <h3>Real-Time Accessibility</h3>
          <p>Capture live lectures, including complex mathematical equations and STEM content.</p>
        </div>
        <div class="feature">
          <h3>Cost-Effective Solution</h3>
          <p>An affordable alternative to traditional accessibility tools like peer note-takers or expensive software.</p>
        </div>
        <div class="feature">
          <h3>Personalized for You</h3>
          <p>
            Designed with students' unique needs in mind, ensuring efficiency and adaptability in every lecture.
          </p>
        </div>
      </section>
  
      <!-- Footer -->
      <footer class="footer">
        <p>© 2024 Inksight. All Rights Reserved.</p>
      </footer>
    </div>
  </template>
  
  <script setup>
  // No logic is needed for a static landing page
  </script>
  
  <style>
  /* General Styles */
  body {
    margin: 0;
    font-family: Arial, sans-serif;
    color: #333;
    line-height: 1.6;
  }
  
  .landing-page {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  /* Header */
  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    padding: 20px 40px;
    background-color: #0047AB;
    color: white;
  }
  
  .header .title {
    font-size: 1.8em;
    font-weight: bold;
  }
  
  .header .nav ul {
    list-style: none;
    display: flex;
    gap: 20px;
    padding: 0;
    margin: 0;
  }
  
  .header .nav ul li {
    display: inline;
  }
  
  .header .nav ul li a {
    text-decoration: none;
    color: white;
    font-weight: bold;
    transition: color 0.3s;
  }
  
  .header .nav ul li a:hover {
    color: #FFD700;
  }
  
  /* Hero Section */
  .hero {
    width: 100%;
    background-color: #f4f4f4;
    text-align: center;
    padding: 60px 20px;
  }
  
  .hero .hero-content h2 {
    font-size: 2.5em;
    color: #0047AB;
  }
  
  .hero .hero-content p {
    font-size: 1.2em;
    margin: 20px 0;
    color: #555;
  }
  
  .hero .cta-button {
    padding: 10px 20px;
    background-color: #0047AB;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 1em;
    transition: background-color 0.3s;
  }
  
  .hero .cta-button:hover {
    background-color: #00337A;
  }
  
  /* Features Section */
  .features {
    display: flex;
    justify-content: space-around;
    text-align: center;
    width: 100%;
    padding: 40px 20px;
    background-color: #fff;
  }
  
  .features .feature {
    max-width: 300px;
  }
  
  .features .feature h3 {
    font-size: 1.5em;
    color: #0047AB;
    margin-bottom: 10px;
  }
  
  .features .feature p {
    font-size: 1em;
    color: #555;
  }
  
  /* Footer */
  .footer {
    text-align: center;
    padding: 20px 0;
    background-color: #0047AB;
    color: white;
    width: 100%;
    font-size: 0.9em;
  }
  </style>
  