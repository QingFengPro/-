<template>
  <div id="app" class="app-container">
    <!-- 导航栏 -->
    <nav class="navbar">
      <div class="nav-content">
        <h1 class="app-title">📊 微博情感分析系统</h1>
        <div class="nav-links">
          <router-link to="/" class="nav-link">首页</router-link>
          <router-link to="/analysis" class="nav-link">分析</router-link>
          <router-link to="/comments" class="nav-link">评论</router-link>
        </div>
      </div>
    </nav>

    <!-- 主容器 -->
    <main class="main-content">
      <router-view></router-view>
    </main>

    <!-- 页脚 -->
    <footer class="footer">
      <p>&copy; 2025 微博情感分析系统 | FastAPI + Vue 3</p>
    </footer>
  </div>
</template>

<script setup>
</script>

<style scoped>
.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: #f5f5f5;
}

.navbar {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1rem 2rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.nav-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.app-title {
  font-size: 1.5rem;
  margin: 0;
  font-weight: bold;
}

.nav-links {
  display: flex;
  gap: 2rem;
}

.nav-link {
  color: white;
  text-decoration: none;
  transition: opacity 0.3s;
  font-weight: 500;
}

.nav-link:hover {
  opacity: 0.8;
}

.nav-link.router-link-active {
  border-bottom: 2px solid white;
  padding-bottom: 5px;
}

.main-content {
  flex: 1;
  max-width: 1200px;
  width: 100%;
  margin: 2rem auto;
  padding: 0 20px;
}

.footer {
  background: #f5f5f5;
  color: #666;
  text-align: center;
  padding: 2rem;
  margin-top: 2rem;
  border-top: 1px solid #ddd;
}

.footer p {
  margin: 0;
  font-size: 0.9rem;
}
</style>
