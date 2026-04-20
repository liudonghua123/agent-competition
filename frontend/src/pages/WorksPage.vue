<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { workApi } from '@/api'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const works = ref<any[]>([])
const loading = ref(true)
const page = ref(1)
const total = ref(0)
const pageSize = 12

// 投票状态
const votingStatus = ref<any>({
  max_votes_per_day: 5,
  used_votes: 0,
  remaining_votes: 5,
  voted_works: [],
  total_works: 0
})
const votingLoading = ref(false)

const totalPages = computed(() => Math.ceil(total.value / pageSize))

onMounted(async () => {
  await fetchWorks()
  if (authStore.isLoggedIn) {
    await fetchVotingStatus()
  }
})

async function fetchWorks() {
  loading.value = true
  try {
    const response = await workApi.list({ page: page.value, page_size: pageSize })
    works.value = response.data.items || []
    total.value = response.data.total || 0
  } finally {
    loading.value = false
  }
}

async function fetchVotingStatus() {
  votingLoading.value = true
  try {
    const response = await fetch('/api/works/voting-status', {
      headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
    })
    if (response.ok) {
      const data = await response.json()
      votingStatus.value = data
    }
  } catch (e) {
    console.error(e)
  } finally {
    votingLoading.value = false
  }
}

async function handleVote(workId: number) {
  if (!authStore.isLoggedIn) {
    router.push('/login')
    return
  }
  try {
    await workApi.vote(workId)
    await fetchWorks()
    await fetchVotingStatus()
  } catch (error: any) {
    alert(error.response?.data?.detail || '投票失败')
  }
}

function hasVoted(workId: number): boolean {
  return votingStatus.value.voted_works?.some((w: any) => w.id === workId)
}

function openUrl(url: string) {
  if (url) window.open(url, '_blank')
}

function handlePageChange(newPage: number) {
  page.value = newPage
  fetchWorks()
}

function getCleanPath(path: string): string {
  if (!path) return ''
  const cleanPath = path.replace(/^\.\//, '').replace(/^\//, '')
  return '/' + cleanPath
}
</script>

<template>
  <div class="max-w-7xl mx-auto px-4 py-12">
    <!-- Voting Status Banner -->
    <div v-if="authStore.isLoggedIn" class="mb-8">
      <div class="bg-gradient-to-r from-blue-600 to-indigo-600 rounded-2xl p-6 text-white shadow-lg">
        <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div>
            <h2 class="text-xl font-bold mb-1">投票信息</h2>
            <p class="text-blue-100 text-sm">每个作品只能投1票，每人有 {{ votingStatus.max_votes_per_day }} 票/天</p>
          </div>
          <div class="flex items-center gap-8">
            <div class="text-center">
              <p class="text-3xl font-bold">{{ votingStatus.used_votes }}</p>
              <p class="text-blue-100 text-sm">已投票</p>
            </div>
            <div class="text-center">
              <p class="text-3xl font-bold">{{ votingStatus.remaining_votes }}</p>
              <p class="text-blue-100 text-sm">剩余票数</p>
            </div>
            <div class="text-center">
              <p class="text-3xl font-bold">{{ votingStatus.voted_works?.length || 0 }}</p>
              <p class="text-blue-100 text-sm">已投票作品</p>
            </div>
            <div class="text-center">
              <p class="text-3xl font-bold">{{ votingStatus.total_works }}</p>
              <p class="text-blue-100 text-sm">总作品数</p>
            </div>
          </div>
        </div>
        <!-- Voted Works List -->
        <div v-if="votingStatus.voted_works?.length" class="mt-4 pt-4 border-t border-white/20">
          <p class="text-sm text-blue-100 mb-2">已投票作品：</p>
          <div class="flex flex-wrap gap-2">
            <span
              v-for="work in votingStatus.voted_works"
              :key="work.id"
              class="px-3 py-1 bg-white/20 rounded-full text-sm"
            >
              {{ work.name }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- Header -->
    <div class="text-center mb-12">
      <h1 class="text-4xl font-bold text-gray-800 mb-3">作品展览</h1>
      <div class="w-20 h-1 bg-gradient-to-r from-blue-500 to-indigo-500 mx-auto rounded-full"></div>
      <p class="text-gray-600 mt-4">为你喜欢的作品投票，每人有5票</p>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-20">
      <div class="inline-block w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
      <p class="mt-4 text-gray-500">加载中...</p>
    </div>

    <!-- Empty State -->
    <div v-else-if="works.length === 0" class="text-center py-20 bg-gray-50 rounded-2xl">
      <div class="w-20 h-20 bg-gray-200 rounded-full flex items-center justify-center mx-auto mb-4">
        <svg class="w-10 h-10 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1.994 1.994 0 006.586 13H4"/>
        </svg>
      </div>
      <p class="text-gray-500 text-lg">暂无参赛作品</p>
      <p class="text-gray-400 text-sm mt-1">快来上传你的作品吧！</p>
    </div>

    <!-- Works Grid -->
    <div v-else class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div
        v-for="work in works"
        :key="work.id"
        class="group bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden hover:shadow-xl hover:border-blue-200 transition-all duration-300 transform hover:-translate-y-1"
      >
        <RouterLink :to="`/works/${work.id}`">
          <div class="h-48 bg-gradient-to-br from-blue-50 via-indigo-50 to-cyan-50 flex items-center justify-center relative overflow-hidden">
            <div class="absolute inset-0 bg-gradient-to-br from-blue-500/5 to-indigo-500/5"></div>
            <div class="relative z-10 text-6xl">🤖</div>
            <div v-if="work.vote_count > 0" class="absolute top-3 right-3 bg-white/90 backdrop-blur-sm px-3 py-1 rounded-full text-sm font-medium text-blue-600 shadow-sm">
              ❤️ {{ work.vote_count }}
            </div>
            <div v-if="authStore.isLoggedIn && hasVoted(work.id)" class="absolute top-3 left-3 bg-green-500 text-white px-3 py-1 rounded-full text-sm font-medium shadow-sm">
              ✓ 已投票
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
        <div class="px-5 pb-5">
          <button
            @click.prevent="handleVote(work.id)"
            :disabled="authStore.isLoggedIn && hasVoted(work.id)"
            class="w-full py-2.5 px-4 rounded-xl font-medium transition-all duration-200 flex items-center justify-center gap-2"
            :class="hasVoted(work.id)
              ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
              : 'bg-gradient-to-r from-blue-500 to-indigo-500 text-white hover:shadow-lg hover:shadow-blue-500/25'"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/>
            </svg>
            {{ hasVoted(work.id) ? '已投票' : '投票支持' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Pagination -->
    <div v-if="totalPages > 1" class="flex justify-center items-center gap-2 mt-12">
      <button
        @click="handlePageChange(page - 1)"
        :disabled="page === 1"
        class="px-4 py-2 rounded-lg border hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition"
      >
        上一页
      </button>
      <span class="px-4 py-2 text-gray-600">
        第 {{ page }} / {{ totalPages }} 页
      </span>
      <button
        @click="handlePageChange(page + 1)"
        :disabled="page === totalPages"
        class="px-4 py-2 rounded-lg border hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition"
      >
        下一页
      </button>
    </div>
  </div>
</template>