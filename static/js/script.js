// Mobile navigation menu toggle.
const menuToggle = document.getElementById("menuToggle");
const navLinks = document.getElementById("navLinks");

if (menuToggle && navLinks) {
  menuToggle.addEventListener("click", () => {
    navLinks.classList.toggle("open");
  });
}

// Dark/light theme toggle (persisted in localStorage).
const themeToggle = document.getElementById("themeToggle");

if (themeToggle) {
  const root = document.documentElement;

  const syncThemeButton = (theme) => {
    const isDark = theme === "dark";
    themeToggle.setAttribute("aria-pressed", String(isDark));
    themeToggle.setAttribute("aria-label", isDark ? "Switch to light mode" : "Switch to dark mode");
  };

  const applyTheme = (theme) => {
    root.dataset.theme = theme;
    syncThemeButton(theme);
    try {
      localStorage.setItem("theme", theme);
    } catch (e) {
      // Storage may be unavailable (e.g. private mode); the theme still applies for this page.
    }
  };

  // The inline <head> script already set data-theme; just sync the button state.
  syncThemeButton(root.dataset.theme === "dark" ? "dark" : "light");

  themeToggle.addEventListener("click", () => {
    applyTheme(root.dataset.theme === "dark" ? "light" : "dark");
  });
}

// Highlight current page in navbar.
const currentPath = window.location.pathname;
document.querySelectorAll(".nav-links a").forEach((link) => {
  const href = link.getAttribute("href");
  if (!href) return;
  if (href === currentPath || (href !== "/" && currentPath.startsWith(href))) {
    link.classList.add("nav-active");
  }
});

// Subtle shadow on navbar when scrolling.
const siteHeader = document.querySelector("header");
if (siteHeader) {
  const onScroll = () => {
    siteHeader.classList.toggle("nav-scrolled", window.scrollY > 12);
  };
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });
}

// Fade-in sections as they enter the viewport (home page + other pages).
const revealSections = document.querySelectorAll(".section-reveal");
if (revealSections.length > 0) {
  const revealObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          revealObserver.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
  );

  revealSections.forEach((section) => revealObserver.observe(section));
}

// If hero video cannot load, show CSS slideshow fallback.
const heroFrame = document.querySelector(".hero-live-frame");
const heroVideo = document.querySelector(".hero-live-video");

if (heroFrame && heroVideo) {
  const useSlides = () => heroFrame.classList.add("video-off");

  heroVideo.addEventListener("error", useSlides);
  heroVideo.addEventListener("stalled", useSlides);

  // Some browsers block autoplay until interaction — still show motion via slides.
  const playPromise = heroVideo.play();
  if (playPromise && typeof playPromise.catch === "function") {
    playPromise.catch(useSlides);
  }
}
