<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { contentApi, workApi } from '@/api'

const contents = ref<any[]>([])
const works = ref<any[]>([])
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  try {
    const [contentsRes, worksRes] = await Promise.all([
      contentApi.list({ type: 'page', is_published: true, page_size: 5 }),
      workApi.list({ status: 'approved', page_size: 6 })
    ])
    contents.value = contentsRes.data.items || []
    works.value = worksRes.data.items || []
  } catch (e: any) {
    console.error('HomePage error:', e)
    error.value = e.message || '加载失败'
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="overflow-hidden">
    <!-- Hero Section with animated gradient -->
    <section class="relative bg-gradient-to-br from-indigo-600 via-blue-600 to-cyan-500 text-white py-24 md:py-32 overflow-hidden">
      <!-- Animated background elements -->
      <div class="absolute inset-0 overflow-hidden">
        <div class="absolute -top-40 -right-40 w-80 h-80 bg-white/10 rounded-full blur-3xl animate-pulse"></div>
        <div class="absolute -bottom-40 -left-40 w-80 h-80 bg-purple-500/20 rounded-full blur-3xl animate-pulse" style="animation-delay: 1s;"></div>
      </div>

      <div class="relative max-w-7xl mx-auto px-4 text-center">
        <div class="inline-flex items-center gap-2 bg-white/10 backdrop-blur-sm px-4 py-2 rounded-full mb-6">
          <span class="w-2 h-2 bg-green-400 rounded-full animate-pulse"></span>
          <span class="text-sm font-medium">2026 智能体创新大赛火热进行中</span>
        </div>

        <h1 class="text-4xl md:text-6xl font-bold mb-6 tracking-tight">
          智能体创新大赛
        </h1>
        <p class="text-xl md:text-2xl opacity-90 mb-10 max-w-2xl mx-auto leading-relaxed">
          激发创意，展现智能体开发的无限可能<br/>
          <span class="text-lg opacity-75">与全国开发者同台竞技，共创AI未来</span>
        </p>

        <div class="flex flex-col sm:flex-row gap-4 justify-center items-center">
          <RouterLink to="/works" class="group bg-white text-indigo-600 px-8 py-4 rounded-xl font-semibold hover:bg-indigo-50 transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1">
            <span class="flex items-center gap-2">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
              </svg>
              查看作品
            </span>
          </RouterLink>
          <RouterLink to="/login" class="group border-2 border-white/30 bg-white/10 backdrop-blur-sm text-white px-8 py-4 rounded-xl font-semibold hover:bg-white/20 transition-all duration-300">
            <span class="flex items-center gap-2">
              立即报名
              <svg class="w-5 h-5 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"/>
              </svg>
            </span>
          </RouterLink>
        </div>

        <!-- Stats -->
        <div class="flex flex-wrap justify-center gap-8 mt-16">
          <div class="text-center">
            <div class="text-4xl font-bold">{{ works.length }}+</div>
            <div class="text-white/70 text-sm mt-1">参赛作品</div>
          </div>
          <div class="text-center">
            <div class="text-4xl font-bold">5</div>
            <div class="text-white/70 text-sm mt-1">奖项设置</div>
          </div>
          <div class="text-center">
            <div class="text-4xl font-bold">30</div>
            <div class="text-white/70 text-sm mt-1">万元奖金</div>
          </div>
        </div>
      </div>

      <!-- Wave divider -->
      <div class="absolute bottom-0 left-0 right-0">
        <svg viewBox="0 0 1440 120" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M0 120L60 110C120 100 240 80 360 70C480 60 600 60 720 65C840 70 960 80 1080 85C1200 90 1320 90 1380 90L1440 90V120H1380C1320 120 1200 120 1080 120C960 120 840 120 720 120C600 120 480 120 360 120C240 120 120 120 60 120H0Z" fill="#f9fafb"/>
        </svg>
      </div>
    </section>

    <!-- Dynamic Content -->
    <section v-if="contents.length > 0" class="py-16 bg-gray-50">
      <div class="max-w-7xl mx-auto px-4">
        <div class="text-center mb-12">
          <h2 class="text-3xl font-bold text-gray-800 mb-3">最新动态</h2>
          <div class="w-20 h-1 bg-gradient-to-r from-blue-500 to-indigo-500 mx-auto rounded-full"></div>
        </div>
        <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          <RouterLink
            v-for="content in contents"
            :key="content.id"
            :to="`/page/${content.slug}`"
            class="group bg-white p-6 rounded-2xl shadow-sm border border-gray-100 hover:shadow-xl hover:border-blue-200 transition-all duration-300 transform hover:-translate-y-1"
          >
            <div class="w-12 h-12 bg-gradient-to-br from-blue-500 to-indigo-500 rounded-xl flex items-center justify-center mb-4">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
              </svg>
            </div>
            <h3 class="text-lg font-semibold mb-2 text-gray-800 group-hover:text-blue-600 transition-colors">{{ content.title }}</h3>
            <p class="text-gray-600 text-sm line-clamp-3">{{ content.content?.substring(0, 100) }}...</p>
          </RouterLink>
        </div>
      </div>
    </section>

    <!-- Works Section -->
    <section class="py-16 bg-white">
      <div class="max-w-7xl mx-auto px-4">
        <div class="flex justify-between items-center mb-12">
          <div>
            <h2 class="text-3xl font-bold text-gray-800">参赛作品</h2>
            <div class="w-16 h-1 bg-gradient-to-r from-blue-500 to-indigo-500 mt-2 rounded-full"></div>
          </div>
          <RouterLink to="/works" class="group flex items-center gap-2 text-blue-600 hover:text-blue-700 font-medium">
            查看全部
            <svg class="w-5 h-5 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
            </svg>
          </RouterLink>
        </div>

        <div v-if="loading" class="text-center py-12">
          <div class="inline-block w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
          <p class="mt-4 text-gray-500">加载中...</p>
        </div>

        <div v-else-if="works.length === 0" class="text-center py-12 bg-gray-50 rounded-2xl">
          <div class="w-16 h-16 bg-gray-200 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"/>
            </svg>
          </div>
          <p class="text-gray-500 text-lg">暂无参赛作品</p>
          <p class="text-gray-400 text-sm mt-1">快来上传你的作品吧！</p>
        </div>

        <div v-else class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          <RouterLink
            v-for="work in works"
            :key="work.id"
            :to="`/works/${work.id}`"
            class="group bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden hover:shadow-xl hover:border-blue-200 transition-all duration-300 transform hover:-translate-y-1"
          >
            <div class="h-48 bg-gradient-to-br from-blue-50 via-indigo-50 to-cyan-50 flex items-center justify-center relative overflow-hidden">
              <div class="absolute inset-0 bg-gradient-to-br from-blue-500/5 to-indigo-500/5"></div>
              <div class="relative z-10 text-6xl">🤖</div>
              <div v-if="work.vote_count > 0" class="absolute top-3 right-3 bg-white/90 backdrop-blur-sm px-3 py-1 rounded-full text-sm font-medium text-blue-600 shadow-sm">
                ❤️ {{ work.vote_count }}
              </div>
            </div>
            <div class="p-5">
              <h3 class="font-bold text-gray-800 mb-2 text-lg group-hover:text-blue-600 transition-colors">{{ work.name }}</h3>
              <p class="text-gray-600 text-sm mb-4 line-clamp-2">{{ work.description }}</p>
              <div class="flex items-center justify-between text-sm">
                <span class="inline-flex items-center gap-1 text-gray-500">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"/>
                  </svg>
                  {{ work.theme_name || '未设置' }}
                </span>
                <span class="text-blue-600 font-medium">查看详情 →</span>
              </div>
            </div>
          </RouterLink>
        </div>
      </div>
    </section>

    <!-- Timeline Section -->
    <section class="py-16 bg-gradient-to-br from-gray-50 to-blue-50">
      <div class="max-w-7xl mx-auto px-4">
        <div class="text-center mb-12">
          <h2 class="text-3xl font-bold text-gray-800 mb-3">大赛流程</h2>
          <div class="w-20 h-1 bg-gradient-to-r from-blue-500 to-indigo-500 mx-auto rounded-full"></div>
        </div>

        <div class="grid md:grid-cols-4 gap-6">
          <div class="text-center">
            <div class="w-16 h-16 bg-gradient-to-br from-blue-500 to-indigo-500 rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-lg">
              <span class="text-2xl text-white font-bold">1</span>
            </div>
            <h3 class="font-semibold text-gray-800 mb-2">注册报名</h3>
            <p class="text-gray-500 text-sm">创建账号，填写队伍信息</p>
          </div>
          <div class="text-center">
            <div class="w-16 h-16 bg-gradient-to-br from-indigo-500 to-purple-500 rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-lg">
              <span class="text-2xl text-white font-bold">2</span>
            </div>
            <h3 class="font-semibold text-gray-800 mb-2">提交作品</h3>
            <p class="text-gray-500 text-sm">上传智能体及相关材料</p>
          </div>
          <div class="text-center">
            <div class="w-16 h-16 bg-gradient-to-br from-purple-500 to-pink-500 rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-lg">
              <span class="text-2xl text-white font-bold">3</span>
            </div>
            <h3 class="font-semibold text-gray-800 mb-2">专家评审</h3>
            <p class="text-gray-500 text-sm">专家打分，评选入围作品</p>
          </div>
          <div class="text-center">
            <div class="w-16 h-16 bg-gradient-to-br from-pink-500 to-red-500 rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-lg">
              <span class="text-2xl text-white font-bold">4</span>
            </div>
            <h3 class="font-semibold text-gray-800 mb-2">颁奖典礼</h3>
            <p class="text-gray-500 text-sm">公布获奖名单，颁发奖金</p>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="py-20 bg-white">
      <div class="max-w-4xl mx-auto px-4 text-center">
        <div class="bg-gradient-to-br from-blue-600 to-indigo-600 rounded-3xl p-12 text-white relative overflow-hidden">
          <div class="absolute inset-0 bg-white/5"></div>
          <div class="relative z-10">
            <h2 class="text-3xl font-bold mb-4">准备好展示你的智能体了吗？</h2>
            <p class="text-xl opacity-90 mb-8">立即报名参赛，与全国的开发者一决高下</p>
            <RouterLink to="/login" class="inline-flex items-center gap-2 bg-white text-blue-600 px-8 py-4 rounded-xl font-semibold hover:bg-blue-50 transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
              </svg>
              立即报名
            </RouterLink>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>