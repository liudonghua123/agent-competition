<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { workApi } from '@/api'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const work = ref<any>(null)
const loading = ref(true)
const error = ref('')
const votingStatus = ref<any>(null)
const votedWorks = ref<any[]>([])

onMounted(async () => {
  await fetchWork()
  if (authStore.isLoggedIn) {
    await fetchVotingStatus()
  }
})

async function fetchWork() {
  loading.value = true
  try {
    const response = await workApi.get(Number(route.params.id))
    work.value = response.data
  } catch (e: any) {
    error.value = e.response?.data?.detail || '加载失败'
  } finally {
    loading.value = false
  }
}

async function fetchVotingStatus() {
  try {
    const response = await fetch('/api/works/voting-status', {
      headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
    })
    if (response.ok) {
      const data = await response.json()
      votingStatus.value = data
      votedWorks.value = data.voted_works || []
    }
  } catch (e) {
    console.error(e)
  }
}

async function handleVote() {
  if (!authStore.isLoggedIn) {
    router.push('/login')
    return
  }
  try {
    await workApi.vote(work.value.id)
    await fetchWork()
    await fetchVotingStatus()
  } catch (err: any) {
    alert(err.response?.data?.detail || '投票失败')
  }
}

function openUrl(url: string) {
  if (url) {
    window.open(url, '_blank')
  }
}

function getCleanPath(path: string): string {
  if (!path) return ''
  const cleanPath = path.replace(/^\.\//, '').replace(/^\//, '')
  return '/' + cleanPath
}

function hasVoted(): boolean {
  return votedWorks.value.some(w => w.id === work.value?.id)
}
</script>

<template>
  <div class="max-w-4xl mx-auto px-4 py-8">
    <!-- Back Link -->
    <RouterLink to="/works" class="text-blue-600 hover:text-blue-700 mb-6 inline-flex items-center gap-2">
      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
      </svg>
      返回作品列表
    </RouterLink>

    <!-- Loading -->
    <div v-if="loading" class="text-center py-12">
      <div class="inline-block w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
      <p class="mt-4 text-gray-500">加载中...</p>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="text-center py-12">
      <div class="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
        <svg class="w-8 h-8 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
        </svg>
      </div>
      <p class="text-red-500 text-lg">{{ error }}</p>
    </div>

    <!-- Work Content -->
    <div v-else-if="work">
      <!-- Header Card -->
      <div class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden mb-6">
        <div class="h-48 bg-gradient-to-br from-blue-50 via-indigo-50 to-cyan-50 flex items-center justify-center relative">
          <div class="absolute inset-0 bg-gradient-to-br from-blue-500/5 to-indigo-500/5"></div>
          <div class="relative z-10 text-7xl">🤖</div>
          <div class="absolute bottom-4 left-4">
            <span class="px-3 py-1 bg-white/90 backdrop-blur-sm rounded-full text-sm font-medium text-gray-600">
              {{ work.theme_name || '未设置主题' }}
            </span>
          </div>
        </div>

        <div class="p-6">
          <h1 class="text-3xl font-bold text-gray-800 mb-3">{{ work.name }}</h1>

          <div class="flex items-center gap-4 mb-6">
            <div class="flex items-center gap-2">
              <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z"/>
              </svg>
              <span class="text-gray-600">{{ work.team_name }}</span>
            </div>
            <span class="text-gray-300">|</span>
            <div class="flex items-center gap-2">
              <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"/>
              </svg>
              <span class="text-gray-600">{{ work.theme_name || '未设置' }}</span>
            </div>
          </div>

          <div class="mb-6">
            <h3 class="font-semibold text-gray-800 mb-2 flex items-center gap-2">
              <svg class="w-5 h-5 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
              </svg>
              作品描述
            </h3>
            <p class="text-gray-600 whitespace-pre-wrap leading-relaxed">{{ work.description || '暂无描述' }}</p>
          </div>
        </div>
      </div>

      <!-- Team Members -->
      <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 mb-6">
        <h3 class="font-semibold text-gray-800 mb-4 flex items-center gap-2">
          <svg class="w-5 h-5 text-purple-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"/>
          </svg>
          队伍成员
        </h3>
        <div class="grid md:grid-cols-2 gap-3">
          <div
            v-for="member in work.team_members"
            :key="member.id"
            class="flex items-center gap-3 p-3 bg-gray-50 rounded-xl"
          >
            <div class="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-500 rounded-full flex items-center justify-center text-white font-medium">
              {{ (member.name || member.student_id)?.charAt(0).toUpperCase() }}
            </div>
            <div>
              <p class="font-medium text-gray-800">{{ member.name }}</p>
              <p class="text-sm text-gray-500">{{ member.student_id }} {{ member.is_leader ? '(队长)' : '' }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Work Links -->
      <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 mb-6">
        <h3 class="font-semibold text-gray-800 mb-4 flex items-center gap-2">
          <svg class="w-5 h-5 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"/>
          </svg>
          作品资源
        </h3>
        <div class="grid md:grid-cols-2 gap-4">
          <div v-if="work.agent_url" class="p-4 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl">
            <div class="flex items-center justify-between">
              <div>
                <p class="font-medium text-gray-800">智能体URL</p>
                <p class="text-sm text-gray-500 truncate">{{ work.agent_url }}</p>
              </div>
              <button
                @click="openUrl(work.agent_url)"
                class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors text-sm font-medium"
              >
                打开链接
              </button>
            </div>
          </div>

          <div v-if="work.agent_editor_url" class="p-4 bg-gradient-to-r from-purple-50 to-pink-50 rounded-xl">
            <div class="flex items-center justify-between">
              <div>
                <p class="font-medium text-gray-800">编排URL</p>
                <p class="text-sm text-gray-500 truncate">{{ work.agent_editor_url }}</p>
              </div>
              <button
                @click="openUrl(work.agent_editor_url)"
                class="px-4 py-2 bg-purple-500 text-white rounded-lg hover:bg-purple-600 transition-colors text-sm font-medium"
              >
                打开链接
              </button>
            </div>
          </div>

          <div v-if="work.pdf_file" class="p-4 bg-gradient-to-r from-red-50 to-orange-50 rounded-xl">
            <div class="flex items-center justify-between">
              <div>
                <p class="font-medium text-gray-800">PDF文档</p>
                <p class="text-sm text-gray-500">{{ work.pdf_file.split('/').pop() }}</p>
              </div>
              <button
                @click="openUrl(getCleanPath(work.pdf_file))"
                class="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors text-sm font-medium"
              >
                查看PDF
              </button>
            </div>
          </div>

          <div v-if="work.video_file" class="p-4 bg-gradient-to-r from-pink-50 to-rose-50 rounded-xl">
            <div class="flex items-center justify-between">
              <div>
                <p class="font-medium text-gray-800">演示视频</p>
                <p class="text-sm text-gray-500">{{ work.video_file.split('/').pop() }}</p>
              </div>
              <button
                @click="openUrl(getCleanPath(work.video_file))"
                class="px-4 py-2 bg-pink-500 text-white rounded-lg hover:bg-pink-600 transition-colors text-sm font-medium"
              >
                播放视频
              </button>
            </div>
          </div>
        </div>

        <div v-if="!work.agent_url && !work.agent_editor_url && !work.pdf_file && !work.video_file" class="text-center py-6 text-gray-500">
          暂无作品资源
        </div>
      </div>

      <!-- Score -->
      <div v-if="work.score" class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 mb-6">
        <h3 class="font-semibold text-gray-800 mb-4 flex items-center gap-2">
          <svg class="w-5 h-5 text-yellow-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z"/>
          </svg>
          作品评分
        </h3>
        <div class="flex items-center gap-4">
          <span class="text-5xl font-bold text-yellow-500">{{ work.score.toFixed(1) }}</span>
          <span class="text-xl text-gray-400">/ 100分</span>
        </div>
      </div>

      <!-- Vote Section -->
      <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-4">
            <div class="text-center">
              <p class="text-4xl font-bold text-pink-500">❤️ {{ work.vote_count }}</p>
              <p class="text-gray-500 text-sm">票</p>
            </div>
            <div v-if="votingStatus" class="text-sm text-gray-500">
              <p>今日已投: {{ votingStatus.used_votes }} / {{ votingStatus.max_votes_per_day }}</p>
              <p>剩余票数: {{ votingStatus.remaining_votes }}</p>
            </div>
          </div>
          <button
            @click="handleVote"
            :disabled="hasVoted()"
            class="px-8 py-3 rounded-xl font-medium transition-all duration-200 flex items-center gap-2"
            :class="hasVoted()
              ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
              : 'bg-gradient-to-r from-pink-500 to-rose-500 text-white hover:shadow-lg hover:shadow-pink-500/25'"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/>
            </svg>
            {{ hasVoted() ? '已投票' : '投票支持' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>