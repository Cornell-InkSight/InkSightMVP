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

    <!-- Footer -->
    <footer class="footer">
    <p>© 2024 Inksight. Designed for accessibility, powered by innovation.</p>
    </footer>
</div>
</template>

<script setup>
// No logic needed for a static landing page
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
background: linear-gradient(90deg, #7f9bbb, #007AFF);
color: white;
box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.header .title {
font-size: 1.8rem;
font-weight: 700;
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
font-weight: 600;
font-size: 1rem;
transition: color 0.3s;
}

.header .nav ul li a:hover {
color: #ffcc00;
}

/* Hero Section */
.hero {
width: 80%;
height: 50vh;
display: flex;
justify-content: center;
align-items: center;
background: url('https://source.unsplash.com/1600x900/?technology,education') no-repeat center center/cover;
color: rgb(0, 0, 0);
text-align: center;
padding: 40px 20px;
}

.hero .hero-content h2 {
font-size: 2.8rem;
font-weight: bold;
margin-bottom: 20px;
text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.3);
}

.hero .hero-content p {
font-size: 1.2rem;
margin-bottom: 30px;
text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.2);
}

.hero .cta-button {
padding: 12px 24px;
background-color: #ffcc00;
color: #333;
border: none;
border-radius: 5px;
cursor: pointer;
font-size: 1rem;
font-weight: bold;
transition: all 0.3s ease;
}

.hero .cta-button:hover {
background-color: #e6b800;
transform: scale(1.05);
}

/* Features Section */
.features {
display: flex;
justify-content: space-around;
text-align: center;
width: 100%;
padding: 60px 20px;
background: linear-gradient(90deg, #f6f9fc, #ffffff);
}

.features .feature {
max-width: 300px;
padding: 20px;
background: white;
border-radius: 8px;
box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.features .feature:hover {
transform: translateY(-10px);
box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
}

.features .feature .icon {
font-size: 2rem;
margin-bottom: 10px;
color: #4A90E2;
}

.features .feature h3 {
font-size: 1.5rem;
color: #333;
margin-bottom: 10px;
}

.features .feature p {
font-size: 1rem;
color: #555;
}

/* Footer */
.footer {
text-align: center;
padding: 20px;
background: #333;
color: white;
width: 100%;
font-size: 0.9rem;
}

.footer p {
margin: 0;
}
</style>
  