<script setup lang="ts">
import { computed, ref, onMounted } from 'vue'
import { useRoute, RouterLink, RouterView, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useThemeStore } from '@/stores/theme'
import Notification from '@/components/Notification.vue'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const themeStore = useThemeStore()

const isAdminPage = computed(() => route.path.startsWith('/admin'))

// Admin menu items with role-based visibility
const menuItems = computed(() => [
  { path: '/admin', name: '仪表盘', icon: 'dashboard', roles: ['user', 'reviewer', 'admin'] },
  { path: '/admin/users', name: '用户管理', icon: 'users', roles: ['admin'] },
  { path: '/admin/teams', name: '队伍管理', icon: 'team', roles: ['user', 'reviewer', 'admin'] },
  { path: '/admin/works', name: '作品管理', icon: 'works', roles: ['user', 'reviewer', 'admin'] },
  { path: '/admin/reviews', name: '评审管理', icon: 'review', roles: ['reviewer', 'admin'] },
  { path: '/admin/votes', name: '投票管理', icon: 'votes', roles: ['reviewer', 'admin'] },
  { path: '/admin/contents', name: '内容管理', icon: 'content', roles: ['reviewer', 'admin'] },
  { path: '/admin/permissions', name: '权限管理', icon: 'permission', roles: ['admin'] },
  { path: '/admin/settings', name: '配置管理', icon: 'settings', roles: ['admin'] },
  { path: '/admin/logs', name: '日志管理', icon: 'logs', roles: ['reviewer', 'admin'] },
])

const filteredMenuItems = computed(() => {
  if (!authStore.user) return []
  return menuItems.value.filter(item => item.roles.includes(authStore.user!.role))
})

const sidebarCollapsed = ref(false)
</script>

<template>
  <div class="min-h-screen bg-gray-50 flex flex-col">
    <!-- Admin Layout -->
    <template v-if="isAdminPage">
      <div class="flex h-screen overflow-hidden">
        <!-- Sidebar with dynamic gradient -->
        <aside :class="[
          'relative flex flex-col transition-all duration-500',
          sidebarCollapsed ? 'w-20' : 'w-72'
        ]">
          <!-- Dynamic gradient background -->
          <div class="absolute inset-0 bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900"></div>
          <!-- Animated gradient overlay -->
          <div class="absolute inset-0 bg-gradient-to-tr from-blue-600/20 via-transparent to-purple-600/20 animate-pulse"></div>
          <!-- Noise texture overlay -->
          <div class="absolute inset-0 opacity-10" style="background-image: url('data:image/svg+xml,%3Csvg viewBox=%220 0 400 400%22 xmlns=%22http://www.w3.org/2000/svg%22%3E%3Cfilter id=%22noiseFilter%22%3E%3CfeTurbulence type=%22fractalNoise%22 baseFrequency=%220.9%22 numOctaves=%223%22 stitchTiles=%22stitch%22/%3E%3C/filter%3E%3Crect width=%22100%25%22 height=%22100%25%22 filter=%22url(%23noiseFilter)%22/%3E%3C/svg%3E');"></div>

          <!-- Logo -->
          <div class="relative h-20 flex items-center px-4 border-b border-white/10 backdrop-blur-sm">
            <RouterLink to="/" class="flex items-center gap-3 group">
              <div class="w-12 h-12 bg-gradient-to-br from-blue-500 via-purple-500 to-indigo-500 rounded-2xl flex items-center justify-center flex-shrink-0 shadow-lg shadow-purple-500/30 group-hover:scale-110 transition-transform duration-300">
                <span class="text-white font-bold text-xl">🤖</span>
              </div>
              <div v-if="!sidebarCollapsed" class="flex flex-col">
                <span class="text-white font-bold text-lg whitespace-nowrap bg-gradient-to-r from-white to-blue-200 bg-clip-text text-transparent">
                  智能体大赛
                </span>
                <span class="text-xs text-blue-300/70 whitespace-nowrap">管理后台</span>
              </div>
            </RouterLink>
          </div>

          <!-- Menu -->
          <nav class="relative flex-1 py-6 overflow-y-auto">
            <ul class="space-y-2 px-3">
              <li v-for="(item, index) in filteredMenuItems" :key="item.path">
                <RouterLink
                  :to="item.path"
                  :style="{ animationDelay: `${index * 50}ms` }"
                  :class="[
                    'group relative flex items-center gap-3 px-4 py-3.5 rounded-2xl transition-all duration-300 hover:scale-[1.02]',
                    route.path === item.path || (item.path !== '/admin' && route.path.startsWith(item.path))
                      ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white shadow-lg shadow-purple-500/30'
                      : 'text-slate-300 hover:bg-white/10 hover:text-white'
                  ]"
                >
                  <!-- Bubble effect -->
                  <span class="absolute inset-0 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-500">
                    <span class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-20 h-20 bg-white/10 rounded-full blur-xl animate-pulse"></span>
                    <span class="absolute top-2 right-2 w-3 h-3 bg-blue-400/50 rounded-full animate-ping"></span>
                    <span class="absolute bottom-2 left-2 w-2 h-2 bg-purple-400/50 rounded-full animate-ping" style="animation-delay: 0.5s"></span>
                  </span>
                  <!-- Icons with gradient background -->
                  <div :class="[
                    'relative z-10 w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0 transition-all duration-300',
                    route.path === item.path || (item.path !== '/admin' && route.path.startsWith(item.path))
                      ? 'bg-white/20 shadow-inner'
                      : 'bg-white/5 group-hover:bg-white/10'
                  ]">
                    <svg v-if="item.icon === 'dashboard'" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"/>
                    </svg>
                    <svg v-else-if="item.icon === 'users'" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"/>
                    </svg>
                    <svg v-else-if="item.icon === 'team'" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/>
                    </svg>
                    <svg v-else-if="item.icon === 'works'" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/>
                    </svg>
                    <svg v-else-if="item.icon === 'review'" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                    </svg>
                    <svg v-else-if="item.icon === 'content'" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                    </svg>
                    <svg v-else-if="item.icon === 'permission'" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
                    </svg>
                    <svg v-else-if="item.icon === 'settings'" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/>
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                    </svg>
                    <svg v-else-if="item.icon === 'logs'" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"/>
                    </svg>
                    <svg v-else-if="item.icon === 'votes'" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/>
                    </svg>
                  </div>
                  <span v-if="!sidebarCollapsed" class="whitespace-nowrap font-medium">{{ item.name }}</span>
                </RouterLink>
              </li>
            </ul>
          </nav>

          <!-- Collapse Button -->
          <div class="relative p-4 border-t border-white/10">
            <button
              @click="sidebarCollapsed = !sidebarCollapsed"
              class="w-full flex items-center justify-center gap-2 px-4 py-3 text-slate-400 hover:text-white hover:bg-white/10 rounded-xl transition-all duration-300"
            >
              <svg :class="['w-5 h-5 transition-transform duration-300', sidebarCollapsed ? 'rotate-180' : '']" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 19l-7-7 7-7m8 14l-7-7 7-7"/>
              </svg>
              <span v-if="!sidebarCollapsed" class="text-sm">收起</span>
            </button>
          </div>
        </aside>

        <!-- Main Content -->
        <div class="flex-1 flex flex-col overflow-hidden">
          <!-- Header -->
          <header class="bg-white shadow-sm border-b h-16 flex items-center justify-between px-6">
            <div class="flex items-center gap-4">
              <h1 class="text-lg font-semibold text-gray-800">
                {{ route.meta?.title || '管理后台' }}
              </h1>
            </div>
            <div class="flex items-center gap-4">
              <!-- Dark Mode Toggle -->
              <button
                @click="themeStore.toggleDark()"
                class="relative w-14 h-8 rounded-full transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-blue-500/50"
                :class="themeStore.isDark ? 'bg-indigo-600' : 'bg-gray-300'"
                :title="themeStore.isDark ? '切换亮色模式' : '切换暗黑模式'"
              >
                <span
                  class="absolute top-1 left-1 w-6 h-6 bg-white rounded-full shadow-md flex items-center justify-center transition-all duration-300"
                  :class="themeStore.isDark ? 'translate-x-6' : 'translate-x-0'"
                >
                  <svg v-if="themeStore.isDark" class="w-4 h-4 text-amber-500" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"/>
                  </svg>
                  <svg v-else class="w-4 h-4 text-gray-600" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"/>
                  </svg>
                </span>
              </button>
              <RouterLink to="/" class="text-sm text-gray-500 hover:text-blue-600 flex items-center gap-1">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/>
                </svg>
                前台
              </RouterLink>
              <div class="flex items-center gap-2">
                <div class="w-8 h-8 bg-gradient-to-r from-blue-500 to-indigo-500 rounded-full flex items-center justify-center text-white text-sm font-medium">
                  {{ (authStore.user?.nickname || authStore.user?.username || 'U')[0].toUpperCase() }}
                </div>
                <span class="text-sm text-gray-700">{{ authStore.user?.nickname || authStore.user?.username }}</span>
                <span class="text-xs px-2 py-0.5 rounded-full" :class="{
                  'bg-blue-100 text-blue-700': authStore.isAdmin,
                  'bg-purple-100 text-purple-700': authStore.isReviewer,
                  'bg-gray-100 text-gray-700': !authStore.isAdmin && !authStore.isReviewer
                }">
                  {{ authStore.isAdmin ? '管理员' : authStore.isReviewer ? '评审' : '用户' }}
                </span>
              </div>
              <button @click="() => { authStore.logout(); router.push('/') }" class="text-sm text-red-500 hover:text-red-600 flex items-center gap-1">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
                </svg>
                退出
              </button>
            </div>
          </header>

          <!-- Content -->
          <main class="flex-1 overflow-y-auto p-6 bg-gray-50">
            <RouterView />
          </main>
        </div>
      </div>
    </template>

    <!-- Frontend Layout -->
    <template v-else>
      <!-- Modern Header -->
      <header class="bg-white/80 backdrop-blur-md border-b border-gray-100 sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4">
          <div class="flex items-center justify-between h-16">
            <!-- Logo -->
            <RouterLink to="/" class="flex items-center gap-2">
              <div class="w-9 h-9 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-xl flex items-center justify-center">
                <span class="text-white font-bold text-lg">🤖</span>
              </div>
              <span class="text-xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
                智能体大赛
              </span>
            </RouterLink>

            <!-- Navigation -->
            <nav class="hidden md:flex items-center gap-1">
              <RouterLink to="/" class="px-4 py-2 text-sm font-medium text-gray-600 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition" active-class="text-blue-600 bg-blue-50">
                首页
              </RouterLink>
              <RouterLink to="/works" class="px-4 py-2 text-sm font-medium text-gray-600 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition" active-class="text-blue-600 bg-blue-50">
                作品展览
              </RouterLink>
              <RouterLink to="/agent-center" class="px-4 py-2 text-sm font-medium text-gray-600 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition" active-class="text-blue-600 bg-blue-50">
                智能体中心
              </RouterLink>
            </nav>

            <!-- Auth Buttons -->
            <div class="flex items-center gap-3">
              <!-- Dark Mode Toggle -->
              <button
                @click="themeStore.toggleDark()"
                class="relative w-14 h-8 rounded-full transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-blue-500/50"
                :class="themeStore.isDark ? 'bg-indigo-600' : 'bg-gray-300'"
                :title="themeStore.isDark ? '切换亮色模式' : '切换暗黑模式'"
              >
                <span
                  class="absolute top-1 left-1 w-6 h-6 bg-white rounded-full shadow-md flex items-center justify-center transition-all duration-300"
                  :class="themeStore.isDark ? 'translate-x-6' : 'translate-x-0'"
                >
                  <svg v-if="themeStore.isDark" class="w-4 h-4 text-amber-500" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"/>
                  </svg>
                  <svg v-else class="w-4 h-4 text-gray-600" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"/>
                  </svg>
                </span>
              </button>
              <template v-if="authStore.isLoggedIn">
                <RouterLink to="/admin" class="px-4 py-2 text-sm font-medium text-white bg-gradient-to-r from-blue-600 to-indigo-600 rounded-lg hover:shadow-lg transition">
                  管理后台
                </RouterLink>
                <button @click="() => { authStore.logout(); router.push('/') }" class="text-sm text-gray-500 hover:text-red-500">退出</button>
              </template>
              <template v-else>
                <RouterLink to="/login" class="px-4 py-2 text-sm font-medium text-blue-600 hover:bg-blue-50 rounded-lg transition">
                  登录
                </RouterLink>
                <RouterLink to="/login" class="px-4 py-2 text-sm font-medium text-white bg-gradient-to-r from-blue-600 to-indigo-600 rounded-lg hover:shadow-lg transition">
                  立即报名
                </RouterLink>
              </template>
            </div>
          </div>
        </div>
      </header>

      <!-- Main Content -->
      <main class="flex-1">
        <RouterView />
      </main>

      <!-- Modern Footer -->
      <footer class="bg-gray-900 text-gray-300 py-12">
        <div class="max-w-7xl mx-auto px-4">
          <div class="grid md:grid-cols-4 gap-8 mb-8">
            <div>
              <div class="flex items-center gap-2 mb-4">
                <span class="text-2xl">🤖</span>
                <span class="text-xl font-bold text-white">智能体大赛</span>
              </div>
              <p class="text-sm text-gray-400">激发创意，展现智能体开发的无限可能</p>
            </div>
            <div>
              <h4 class="font-semibold text-white mb-4">快速链接</h4>
              <ul class="space-y-2 text-sm">
                <li><RouterLink to="/" class="hover:text-blue-400 transition">首页</RouterLink></li>
                <li><RouterLink to="/works" class="hover:text-blue-400 transition">作品展览</RouterLink></li>
                <li><RouterLink to="/agent-center" class="hover:text-blue-400 transition">智能体中心</RouterLink></li>
                <li><RouterLink to="/login" class="hover:text-blue-400 transition">报名参赛</RouterLink></li>
              </ul>
            </div>
            <div>
              <h4 class="font-semibold text-white mb-4">参赛须知</h4>
              <ul class="space-y-2 text-sm">
                <li><span class="text-gray-500">参赛人数：1-5人/队</span></li>
                <li><span class="text-gray-500">作品提交：PDF/视频/URL</span></li>
                <li><span class="text-gray-500">投票规则：每日5票</span></li>
              </ul>
            </div>
            <div>
              <h4 class="font-semibold text-white mb-4">联系方式</h4>
              <ul class="space-y-2 text-sm text-gray-400">
                <li>Email: contact@agent-contest.com</li>
                <li>电话: 400-XXX-XXXX</li>
              </ul>
            </div>
          </div>
          <div class="border-t border-gray-800 pt-8 text-center text-sm text-gray-500">
            <p>&copy; 2026 智能体创新大赛. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </template>
  </div>

  <!-- Global Notification -->
  <Notification />
</template>