<template>
  <div class="app-shell">
    <header class="topbar">
      <div class="brand">Meeting Plunger</div>
      <nav class="nav">
        <RouterLink class="nav-link" to="/">Transcribe</RouterLink>
        <RouterLink class="nav-link" to="/racing">Racing</RouterLink>
      </nav>
    </header>

    <main class="content">
      <RouterView />
    </main>
  </div>
</template>

<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router';
</script>

<style scoped>
.app-shell {
  min-height: 100vh;
}

.topbar {
  position: sticky;
  top: 0;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 14px 18px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.08);
  background: rgba(255, 255, 255, 0.86);
  backdrop-filter: blur(10px);
}

.brand {
  font-weight: 700;
  letter-spacing: 0.2px;
}

.nav {
  display: flex;
  gap: 10px;
}

.nav-link {
  padding: 8px 10px;
  border-radius: 10px;
  color: inherit;
  text-decoration: none;
  font-weight: 600;
}

.nav-link.router-link-active {
  background: rgba(0, 102, 204, 0.12);
  color: #004ea3;
}

.content {
  max-width: 980px;
  margin: 0 auto;
  padding: 22px 18px 40px;
}
</style>
