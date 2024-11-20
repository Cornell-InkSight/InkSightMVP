<template>
    <div class="landing-page">
      <!-- Header -->
      <header class="header">
        <h1 class="title">Inksight</h1>
        <nav class="nav">
          <ul>
            <li><router-link to="/students/1" target="_blank">Students</router-link></li>
            <li><router-link to="/professors/1" target="_blank">Professors</router-link></li>
            <li><router-link to="/sdscoordinators/1" target="_blank">SDS Coordinators</router-link></li>
            <li><router-link to="/tas/1" target="_blank">TAs</router-link></li>
          </ul>
        </nav>
      </header>
  
      <!-- Hero Section -->
      <section class="hero">
        <div class="hero-content">
          <h2>Revolutionizing Accessibility in STEM Education</h2>
          <p>
            Inksight empowers students with disabilities by offering cutting-edge tools for capturing real-time, editable lecture notes, including mathematical equations and STEM-specific content.
          </p>
          <button class="cta-button">Discover Inksight</button>
        </div>
      </section>
  
      <!-- Features Section -->
      <section class="features">
        <div class="feature">
          <div class="icon">🔗</div>
          <h3>Real-Time Note-Taking</h3>
          <p>Capture STEM lectures seamlessly, including complex equations.</p>
        </div>
        <div class="feature">
          <div class="icon">💡</div>
          <h3>Cost-Effective Solutions</h3>
          <p>An affordable alternative to inaccessible tools.</p>
        </div>
        <div class="feature">
          <div class="icon">⚙️</div>
          <h3>Tailored for Accessibility</h3>
          <p>Built with inclusivity at its core, meeting diverse student needs.</p>
        </div>
      </section>
  
      <!-- Comparison Section -->
      <section class="comparison">
        <h2 class="comparison-title">Compare Features</h2>
        <div class="comparison-table">
          <div class="row header-row">
            <div class="cell">Feature</div>
            <div class="cell">Inksight</div>
            <div class="cell">Other Tools</div>
          </div>
          <div class="row">
            <div class="cell">Real-Time Equations</div>
            <div class="cell">✅</div>
            <div class="cell">❌</div>
          </div>
          <div class="row">
            <div class="cell">Accessibility First</div>
            <div class="cell">✅</div>
            <div class="cell">⚠️ Limited</div>
          </div>
          <div class="row">
            <div class="cell">Cost-Effective</div>
            <div class="cell">✅</div>
            <div class="cell">❌</div>
          </div>
        </div>
      </section>
  
      <!-- Footer -->
      <footer class="footer">
        <p>© 2024 Inksight. Designed for accessibility, powered by innovation.</p>
      </footer>
    </div>
  </template>
  
  <script setup>
  // No logic needed for this static landing page.
  </script>
  
  <style>
  /* General Styles */
  body {
    margin: 0;
    font-family: 'Poppins', sans-serif;
    background-color: #f9fafb;
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
    background: linear-gradient(90deg, #0057b8, #00c7d7);
    color: white;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }
  
  .header .title {
    font-size: 2rem;
    font-weight: bold;
  }
  
  .header .nav ul {
    list-style: none;
    display: flex;
    gap: 20px;
    padding: 0;
    margin: 0;
  }
  
  .header .nav ul li a {
    text-decoration: none;
    color: white;
    font-weight: 500;
    transition: color 0.3s;
  }
  
  .header .nav ul li a:hover {
    color: #ffd700;
  }
  
  /* Hero Section */
  .hero {
    width: 100%;
    background: url('https://source.unsplash.com/1600x900/?technology') no-repeat center center/cover;
    color: white;
    text-align: center;
    padding: 50px 20px;
  }
  
  .hero .hero-content h2 {
    font-size: 2.5rem;
    margin-bottom: 20px;
    font-weight: 700;
  }
  
  .hero .cta-button {
    background: #ffd700;
    padding: 12px 24px;
    border: none;
    border-radius: 8px;
    color: #333;
    font-weight: bold;
    transition: transform 0.3s;
  }
  
  .hero .cta-button:hover {
    transform: scale(1.05);
  }
  
  /* Features Section */
  .features {
    display: flex;
    justify-content: space-around;
    padding: 40px;
    background: #f4f4f4;
  }
  
  .features .feature {
    background: white;
    padding: 20px;
    border-radius: 10px;
    text-align: center;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s, box-shadow 0.3s;
  }
  
  .features .feature:hover {
    transform: translateY(-5px);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
  }
  
  .features .icon {
    font-size: 2rem;
    margin-bottom: 10px;
    color: #0057b8;
  }
  
  .features h3 {
    font-size: 1.5rem;
    margin-bottom: 10px;
  }
  
  /* Comparison Section */
  .comparison {
    background: #fff;
    padding: 40px 20px;
    width: 100%;
  }
  
  .comparison-title {
    font-size: 2rem;
    text-align: center;
    margin-bottom: 20px;
  }
  
  .comparison-table {
    display: grid;
    gap: 10px;
  }
  
  .row {
    display: flex;
    justify-content: space-between;
    padding: 10px 20px;
    background: #f9f9f9;
    border-radius: 8px;
  }
  
  .header-row {
    font-weight: bold;
    background: #0057b8;
    color: white;
  }
  
  .cell {
    flex: 1;
    text-align: center;
  }
  
  /* Footer */
  .footer {
    text-align: center;
    padding: 20px;
    background: #333;
    color: white;
  }
  </style>
  