<template>
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>InkSight</title>
  </head>
  
  <body>
    <div class="row">
      <div class="col"></div>
  
      <nav>
        <a href="">
          <h3>InkSight</h3>
        </a>
  
        <ul>
          <li>
            <a href="#why">Challenges</a>
          </li>
  
          <li>
            <a href="#features">Features</a>
          </li>
  
          <li>
            <a href="#team">Team</a>
          </li>
  
          <li>
            <router-link to = "/signin">
              <a href="" class="button">Get demo</a>
            </router-link>
          </li>
        </ul>
      </nav>
  
      <div class="col"></div>
    </div>
  
    <div class="row">
      <div class="col"></div>
  
      <section class="hero">
        <div class="text">
          <h1>Make <span class="accent circle">STEM</span> classroom learning <span
              class="accent underline">accessible</span> to
            all.</h1>
  
          <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut et massa mi. Aliquam in hendrerit urna.
            Pellentesque sit amet sapien fringilla, mattis ligula consectetur, ultrices mauris.</p>
        </div>
  
        <div class="buttons">
          <router-link to = "/signin">
            <a href="" class="button">Get demo</a>
          </router-link>
  
          <a href="#why" class="button secondary">Why we built this</a>
        </div>
      </section>
  
      <div class="col"></div>
    </div>
  
    <div class="row">
      <div class="col"></div>
  
      <section class="first">
        <img src="" alt="" id="why">
  
        <div class="row">
          <div class="item">
            <div class="icon-wrapper">
            </div>
  
            <div class="text">
              <h3>Challenge 1</h3>
  
              <p>Incomplete capture – current existing tools don’t work well with STEM.</p>
            </div>
          </div>
  
  
          <div class="item">
            <div class="icon-wrapper">
            </div>
  
            <div class="text">
              <h3>Challenge 1</h3>
  
              <p>Incomplete capture – current existing tools don’t work well with STEM.</p>
            </div>
          </div>
  
          <div class="item">
            <div class="icon-wrapper">
            </div>
  
  
            <div class="text">
              <h3>Challenge 1</h3>
  
              <p>Incomplete capture – current existing tools don’t work well with STEM.</p>
            </div>
          </div>
        </div>
      </section>
  
      <div class="col"></div>
    </div>
  
    <div class="row dark">
      <div class="col"></div>
  
      <section class="introducing">
        <div class="header">
          <p>Introducing...</p>
        </div>
  
        <div class="main">
          <h2>InkSight</h2>
        </div>
  
        <div class="footer">
          <p>Some text here to get users excited.</p>
  
          <router-link to = "/signin">
            <a href="" class="button">Get demo</a>
          </router-link>
        </div>
      </section>
  
      <div class="col"></div>
    </div>
  
    <div class="row">
      <div class="col"></div>
  
      <section class="features" id="features">
        <div class="feature">
          <h2>Features</h2>
        </div>
  
        <div class="feature">
          <img src="" alt="">
  
          <div class="right">
            <div class="icon-wrapper">
            </div>
  
            <div class="text">
              <h3>Feature 1</h3>
  
              <p>Organic chemistry, multi-variable calculus, you name it! Works for chalkboards & lecture slides.</p>
            </div>
          </div>
        </div>
  
        <div class="feature alt">
          <img src="" alt="">
  
          <div class="right">
            <div class="icon-wrapper">
            </div>
  
            <div class="text">
              <h3>Feature 1</h3>
  
              <p>Organic chemistry, multi-variable calculus, you name it! Works for chalkboards & lecture slides.</p>
            </div>
          </div>
        </div>
  
        <div class="feature">
          <img src="" alt="">
  
          <div class="right">
            <div class="icon-wrapper">
            </div>
  
            <div class="text">
              <h3>Feature 1</h3>
  
              <p>Organic chemistry, multi-variable calculus, you name it! Works for chalkboards & lecture slides.</p>
            </div>
          </div>
        </div>
      </section>
  
      <div class="col"></div>
    </div>
  
    <div class="row">
      <div class="col"></div>
  
      <section class="team" id="team">
        <div class="ppl">
          <h2>Our team</h2>
  
          <div class="row">
            <div class="sub">
              <div class="person">
                <img src="" alt="">
  
                <div class="text">
                  <h3>Clément Rozé</h3>
  
                  <p>UX Designer</p>
                </div>
              </div>
  
              <div class="person">
                <img src="" alt="">
  
                <div class="text">
                  <h3>Clément Rozé</h3>
  
                  <p>UX Designer</p>
                </div>
              </div>
            </div>
  
            <div class="sub">
              <div class="person">
                <img src="" alt="">
  
                <div class="text">
                  <h3>Clément Rozé</h3>
  
                  <p>UX Designer</p>
                </div>
              </div>
  
              <div class="person">
                <img src="" alt="">
  
                <div class="text">
                  <h3>Clément Rozé</h3>
  
                  <p>UX Designer</p>
                </div>
              </div>
            </div>
          </div>
        </div>
  
        <div class="groups">
          <div class="group">
            <img src="" alt="">
  
            <h3>Cornell eLab accelerator</h3>
          </div>
  
          <div class="group">
            <img src="" alt="">
  
            <h3>Cornell eLab accelerator</h3>
          </div>
        </div>
      </section>
  
      <div class="col"></div>
    </div>
  
    <footer class="row dark">
      <div class="col"></div>
  
      <section class="footer">
        <h2>InkSight</h2>
  
        <div class="right">
          <div class="column">
            <a href="#why">Challenges</a>
  
            <a href="#features">Features</a>
  
            <a href="#team">Team</a>
          </div>
  
          <div class="column">
            <router-link to = "/signin">
              <a href="" class="button">Get demo</a>
            </router-link>
  
            <a href="#why" class="button secondary">Why we built this</a>
          </div>
        </div>
      </section>
  
      <div class="col"></div>
    </footer>
  </body>
</template>
  
  <style>
  @font-face {
    font-family: Satoshi Bold;
    src: url(Fonts/Satoshi-Bold.otf);
  }
  
  @font-face {
    font-family: Satoshi Medium;
    src: url(Fonts/Satoshi-Medium.otf);
  }
  
  :root {
    --page: #F6F6F6;
    --surface: #FFFFFF;
    --outline-light: #cccccc;
    --outline-dark: #2e2e2e;
    --foreground-1: #000000;
    --foreground-2: #7B7B7B;
  }
  
  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }
  
  body,
  html {
    height: 100%;
    width: 100%;
    background: var(--page);
    color: var(--foreground-1);
    font-family: Satoshi Medium, sans-serif;
    scroll-behavior: smooth;
  }
  
  h1 {
    font-size: 48px;
    line-height: 150%;
    font-family: Satoshi Bold, sans-serif;
  }
  
  h2 {
    font-size: 32px;
    line-height: 150%;
    font-family: Satoshi Bold, sans-serif;
  }
  
  h3 {
    font-size: 20px;
    line-height: 150%;
    font-family: Satoshi Bold, sans-serif;
  }
  
  p {
    font-size: 16px;
    color: var(--foreground-2);
    line-height: 150%;
  }
  
  a:focus-visible {
    outline: 2px solid var(--foreground-1);
    outline-offset: 2px;
  }
  
  a:not(a.button):focus-visible {
    border-radius: 4px;
  }
  
  .dark a:focus-visible {
    outline-color: var(--surface);
  }
  
  .row {
    display: flex;
    width: 100%;
  }
  
  .row .col {
    outline: 0.5px solid var(--outline-light);
    flex: 1;
    background: var(--page);
  }
  
  .row.dark .col {
    outline-color: var(--outline-dark);
    background: var(--foreground-1);
  }
  
  .row section,
  .row nav {
    width: 800px;
    background: var(--page);
  }
  
  nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px 24px;
    outline: 0.5px solid var(--outline-light);
    background: var(--page);
  }
  
  nav h3 {
    color: var(--foreground-1);
    transition: opacity 120ms ease-out;
  }
  
  nav h3:hover {
    opacity: 0.7;
  }
  
  nav ul {
    display: flex;
    align-items: center;
    gap: 32px;
  }
  
  nav ul li {
    list-style-type: none;
  }
  
  nav ul li a:not(a.button) {
    color: var(--foreground-2);
    transition: color 120ms ease-out;
  }
  
  nav ul li a:not(a.button):hover {
    color: var(--foreground-1);
  }
  
  nav a.button {
    padding: 8px 16px;
  }
  
  a {
    text-decoration: none;
  }
  
  a.button {
    background: var(--foreground-1);
    color: var(--surface);
    padding: 12px 24px;
    border-radius: 32px;
    font-size: 16px;
    display: flex;
    justify-content: center;
    align-items: center;
    transition: opacity 120ms ease-out !important;
  }
  
  a.button:hover {
    opacity: 0.8;
  }
  
  .dark a.button {
    background: var(--surface);
    color: var(--foreground-1);
  }
  
  a.button.secondary {
    background: var(--surface);
    border: 1px solid var(--outline-light);
    color: var(--foreground-1);
  }
  
  a.button.secondary:hover {
    opacity: 0.6;
  }
  
  .dark a.button.secondary {
    background: var(--foreground-1);
    border-color: var(--outline-dark);
    color: var(--surface);
  }
  
  .row section {
    padding: 64px 16px;
    display: flex;
    flex-direction: column;
    outline: 0.5px solid var(--outline-light);
  }
  
  .hero {
    justify-content: center;
    align-items: center;
    text-align: center;
    gap: 32px;
  }
  
  .hero .text {
    display: flex;
    flex-direction: column;
    gap: 16px;
    justify-content: center;
    align-items: center;
  }
  
  .hero .text p {
    font-size: 20px;
  }
  
  .hero .text>*,
  .hero h1 span.accent {
    color: var(--foreground-1);
    max-width: 570px;
  }
  
  .hero .text h1 {
    color: var(--foreground-2);
    position: relative;
  }
  
  .hero .text h1 span.circle {
    margin: 0 4px;
  }
  
  .hero .text h1 .circle::after {
    content: '';
    position: absolute;
    background: url(Media/Decorators/circle.svg);
    width: 151px;
    height: 86px;
    top: -9px;
    left: 156px;
    background-repeat: no-repeat;
  }
  
  .hero .text h1 .underline::after {
    content: '';
    position: absolute;
    background: url(Media/Decorators/underline.svg);
    width: 232px;
    height: 7px;
    bottom: 7px;
    left: 199px;
    background-repeat: no-repeat;
  }
  
  .hero .buttons {
    display: flex;
    gap: 16px;
  }
  
  .hero .buttons a {
    width: 173px;
  }
  
  .row .first {
    padding: 0
  }
  
  .first img {
    width: 100%;
    height: 432px;
    background: var(--surface);
    border: none;
  }
  
  .first .row {
    display: flex;
  }
  
  .first .row .item {
    display: flex;
    flex-direction: column;
    gap: 8px;
    outline: 0.5px solid var(--outline-light);
    background: var(--page);
    padding: 24px;
  }
  
  .first .row .item .text {
    display: flex;
    flex-direction: column;
    gap: 4px;
  }
  
  .first .row .item .icon-wrapper {
    width: 40px;
    height: 40px;
    background: var(--surface);
    border: 1px solid var(--outline-light);
    border-radius: 50%;
  }
  
  .row .introducing {
    padding: 0;
    outline-color: var(--outline-dark);
  }
  
  .introducing {
    height: 100vh;
  }
  
  .introducing>* {
    background: var(--foreground-1);
    outline: 0.5px solid var(--outline-dark);
  }
  
  .introducing .header {
    text-align: center;
    padding: 24px 16px;
  }
  
  .introducing .main {
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .introducing .main h2 {
    font-size: 128px;
  }
  
  .introducing .footer {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 24px;
  }
  
  .introducing p,
  .introducing h2 {
    color: var(--surface);
  }
  
  .row .features {
    padding: 0;
  }
  
  .features .feature {
    display: flex;
    background: var(--page);
    outline: 0.5px solid var(--outline-light);
  }
  
  .features .feature:first-child {
    padding: 24px;
    text-align: center;
  }
  
  .features .feature h2 {
    outline: none;
  }
  
  .features .feature.alt {
    flex-direction: row-reverse;
  }
  
  .features .feature>* {
    flex: 1;
    background: var(--page);
    outline: 0.5px solid var(--outline-light);
  }
  
  .features .feature img {
    width: 400px;
    height: 400px;
    background: var(--surface);
  }
  
  .features .feature .right {
    display: flex;
    flex-direction: column;
    gap: 8px;
    padding: 24px;
    justify-content: center;
  }
  
  .features .feature .text {
    display: flex;
    flex-direction: column;
    gap: 4px;
  }
  
  .features .feature .icon-wrapper {
    width: 40px;
    height: 40px;
    background: var(--surface);
    border: 1px solid var(--outline-light);
    border-radius: 50%;
  }
  
  .row .team {
    padding: 0;
  }
  
  .row .team>* {
    background: var(--page);
    outline: 0.5px solid var(--outline-light)
  }
  
  .row .team .ppl {
    padding: 24px;
    display: flex;
    flex-direction: column;
    gap: 32px;
  }
  
  .row .team .ppl h2 {
    text-align: center;
  }
  
  .row .team .ppl .row,
  .row .team .ppl .row .sub {
    display: flex;
    gap: 16px;
    flex: 1;
  }
  
  .row .team .ppl .row .person {
    display: flex;
    flex-direction: column;
    gap: 8px;
    align-items: center;
    justify-content: center;
    flex: 1;
  }
  
  .row .team .ppl .row .person .text {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    gap: 4px;
  }
  
  .row .team .ppl .row .person img {
    width: 128px;
    height: 128px;
    background: var(--surface);
    border: 1px solid var(--outline-light);
    border-radius: 8px;
  }
  
  .row .team .groups {
    display: flex;
  }
  
  
  .row .team .groups>* {
    background: var(--page);
    outline: 0.5px solid var(--outline-light)
  }
  
  .row .team .groups .group {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    gap: 8px;
    flex: 1;
    padding: 24px;
  }
  
  .row .team .groups .group img {
    width: 128px;
    height: 128px;
    background: var(--surface);
    border: 1px solid var(--outline-light);
    border-radius: 50%;
  }
  
  .row .footer {
    background: var(--foreground-1);
    outline: 0.5px solid var(--outline-dark);
  }
  
  .row .footer {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
  }
  
  .row .footer .right {
    display: flex;
    gap: 32px;
  }
  
  .row .footer .column {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }
  
  .row .footer .column:last-child {
    gap: 16px;
  }
  
  .row .footer a:not(a.button) {
    color: var(--foreground-2);
    transition: color 120ms ease-out;
    width: fit-content;
  }
  
  .row .footer a:not(a.button):hover {
    color: var(--surface) !important;
  }
  
  .row .footer a.button {
    color: var(--foreground-1);
  }
  
  .row .footer a.button.secondary {
    color: var(--surface);
  }
  
  .row .footer h2 {
    font-size: 100px;
    color: var(--surface)
  }
  
  #why,
  #features,
  #team {
    scroll-margin-top: 32px;
  }
  
  @media screen and (max-width: 832px) {
  
    .row section,
    .row nav {
      width: 100%;
    }
  
    .row .col {
      min-width: 16px;
    }
  
    .hero h1 span {
      margin: 0;
    }
  
    .hero h1 {
      line-height: 120%;
      font-size: 32px;
    }
  
    .hero h1 span::after {
      display: none;
    }
  
    .hero .text p {
      font-size: 16px;
    }
  
    .first .row {
      flex-direction: column;
    }
  
    .features .feature {
      flex-direction: column !important;
    }
  
    .features .feature img {
      width: 100%;
      height: 300px;
    }
  
    .row .team .ppl .row {
      flex-direction: column;
    }
  
    .row .footer,
    .row .footer .right,
    .row .footer .column {
      flex-direction: column;
      gap: 16px;
    }
  
    .row .footer h2 {
      font-size: 48px;
    }
  
    .introducing .main h2 {
      font-size: 96px;
    }
  }
  
  @media screen and (max-width: 600px) {
    nav ul li:not(li:last-child) {
      /* lol one day, implement an actual hamburger menu */
      /* instead of doing this shit */
      display: none;
    }
  }
  
  @media screen and (max-width: 432px) {
  
    .row .team .ppl .row .sub,
    .row .team .groups {
      flex-direction: column;
    }
  
    .row .footer {
      align-items: flex-start;
    }
  
    .row .footer .right {
      flex: 1;
      width: 100%;
    }
  
    .hero .buttons {
      flex-direction: column;
    }
  
    .hero .buttons,
    .hero .buttons>a {
      width: 100%;
    }
  
    .introducing .main h2 {
      font-size: 48px;
    }
  
    .row .footer a.button {
      width: 100%;
    }
  }
</style>