<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import api from '@/api'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

// 统计数据
const stats = ref<any>({
  total_votes: 0,
  total_voted_users: 0,
  total_voted_works: 0,
  today_votes: 0,
  daily_trend: {},
  top_works: [],
  top_users: []
})

// 按用户视角
const userVotes = ref<any[]>([])
const userLoading = ref(true)

// 按作品视角
const workVotes = ref<any[]>([])
const workLoading = ref(true)

// 分页
const page = ref(1)
const total = ref(0)
const pageSize = 20

// 筛选
const activeTab = ref('statistics')
const keyword = ref('')
const statusFilter = ref('')
const loading = ref(true)

onMounted(async () => {
  await fetchStatistics()
  await fetchVotesByWork()
  loading.value = false
})

async function fetchStatistics() {
  try {
    const res = await api.get('/votes/statistics', { params: { days: 30 } })
    stats.value = res.data || {}
  } catch (e) {
    console.error(e)
  }
}

async function fetchVotesByUser(pageNum: number = 1) {
  userLoading.value = true
  try {
    const params: any = { page: pageNum, page_size: pageSize }
    if (keyword.value) params.keyword = keyword.value
    const res = await api.get('/votes/by-user', { params })
    userVotes.value = res.data.items || []
    total.value = res.data.total || 0
    page.value = pageNum
  } catch (e) {
    console.error(e)
  } finally {
    userLoading.value = false
  }
}

async function fetchVotesByWork(pageNum: number = 1) {
  workLoading.value = true
  try {
    const params: any = { page: pageNum, page_size: pageSize }
    if (keyword.value) params.keyword = keyword.value
    if (statusFilter.value) params.status = statusFilter.value
    const res = await api.get('/votes/by-work', { params })
    workVotes.value = res.data.items || []
    total.value = res.data.total || 0
    page.value = pageNum
  } catch (e) {
    console.error(e)
  } finally {
    workLoading.value = false
  }
}

function handleTabChange(tab: string) {
  activeTab.value = tab
  page.value = 1
  if (tab === 'by-user') {
    fetchVotesByUser()
  } else if (tab === 'by-work') {
    fetchVotesByWork()
  }
}

function handleSearch() {
  page.value = 1
  if (activeTab.value === 'by-user') {
    fetchVotesByUser()
  } else if (activeTab.value === 'by-work') {
    fetchVotesByWork()
  }
}

function handlePageChange(newPage: number) {
  if (activeTab.value === 'by-user') {
    fetchVotesByUser(newPage)
  } else if (activeTab.value === 'by-work') {
    fetchVotesByWork(newPage)
  }
}

function formatDate(dateStr: string): string {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleString('zh-CN', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const statusOptions = [
  { value: '', label: '全部状态' },
  { value: 'pending', label: '待审核' },
  { value: 'approved', label: '已通过' },
  { value: 'rejected', label: '已拒绝' }
]

const statusColors: Record<string, string> = {
  pending: 'bg-yellow-100 text-yellow-700',
  approved: 'bg-green-100 text-green-700',
  rejected: 'bg-red-100 text-red-700'
}
</script>

<template>
  <div>
    <!-- Welcome Header -->
    <div class="mb-8">
      <h1 class="text-2xl font-bold text-gray-800">投票管理</h1>
      <p class="text-gray-500 mt-1">查看投票统计数据和记录</p>
    </div>

    <!-- Tabs -->
    <div class="flex gap-2 mb-6">
      <button
        @click="handleTabChange('statistics')"
        :class="[
          'px-4 py-2 rounded-lg font-medium transition-all',
          activeTab === 'statistics'
            ? 'bg-blue-600 text-white'
            : 'bg-white text-gray-600 hover:bg-gray-50 border border-gray-200'
        ]"
      >
        统计概览
      </button>
      <button
        @click="handleTabChange('by-user')"
        :class="[
          'px-4 py-2 rounded-lg font-medium transition-all',
          activeTab === 'by-user'
            ? 'bg-blue-600 text-white'
            : 'bg-white text-gray-600 hover:bg-gray-50 border border-gray-200'
        ]"
      >
        按用户
      </button>
      <button
        @click="handleTabChange('by-work')"
        :class="[
          'px-4 py-2 rounded-lg font-medium transition-all',
          activeTab === 'by-work'
            ? 'bg-blue-600 text-white'
            : 'bg-white text-gray-600 hover:bg-gray-50 border border-gray-200'
        ]"
      >
        按作品
      </button>
    </div>

    <!-- Statistics Tab -->
    <div v-if="activeTab === 'statistics'" class="space-y-6">
      <!-- Stats Cards -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 hover:shadow-lg transition-shadow duration-300">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-gray-500 mb-1">总投票数</p>
              <p class="text-3xl font-bold text-gray-800">{{ stats.total_votes }}</p>
            </div>
            <div class="w-14 h-14 rounded-2xl bg-gradient-to-br from-pink-500 to-rose-500 flex items-center justify-center shadow-lg">
              <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/>
              </svg>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 hover:shadow-lg transition-shadow duration-300">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-gray-500 mb-1">投票用户数</p>
              <p class="text-3xl font-bold text-gray-800">{{ stats.total_voted_users }}</p>
            </div>
            <div class="w-14 h-14 rounded-2xl bg-gradient-to-br from-purple-500 to-violet-500 flex items-center justify-center shadow-lg">
              <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"/>
              </svg>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 hover:shadow-lg transition-shadow duration-300">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-gray-500 mb-1">被投票作品数</p>
              <p class="text-3xl font-bold text-gray-800">{{ stats.total_voted_works }}</p>
            </div>
            <div class="w-14 h-14 rounded-2xl bg-gradient-to-br from-green-500 to-emerald-500 flex items-center justify-center shadow-lg">
              <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/>
              </svg>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 hover:shadow-lg transition-shadow duration-300">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-gray-500 mb-1">今日投票</p>
              <p class="text-3xl font-bold text-gray-800">{{ stats.today_votes }}</p>
            </div>
            <div class="w-14 h-14 rounded-2xl bg-gradient-to-br from-red-500 to-orange-500 flex items-center justify-center shadow-lg">
              <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
            </div>
          </div>
        </div>
      </div>

      <!-- Top Lists -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Top Works -->
        <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
          <h3 class="font-semibold text-gray-800 mb-4">投票最多的作品</h3>
          <div v-if="stats.top_works?.length === 0" class="text-center py-8 text-gray-500">
            暂无数据
          </div>
          <div v-else class="space-y-3">
            <div
              v-for="(work, index) in stats.top_works"
              :key="work.work_id"
              class="flex items-center gap-4 p-3 rounded-xl hover:bg-gray-50 transition"
            >
              <span class="w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium"
                :class="Number(index) < 3 ? 'bg-yellow-100 text-yellow-700' : 'bg-gray-100 text-gray-600'">
                {{ Number(index) + 1 }}
              </span>
              <div class="flex-1 min-w-0">
                <p class="font-medium text-gray-800 truncate">{{ work.work_name }}</p>
                <p class="text-sm text-gray-500">{{ work.team_name }}</p>
              </div>
              <div class="text-right">
                <p class="text-xl font-bold text-pink-600">{{ work.vote_count }}</p>
                <p class="text-xs text-gray-400">票</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Top Users -->
        <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
          <h3 class="font-semibold text-gray-800 mb-4">投票最多的用户</h3>
          <div v-if="stats.top_users?.length === 0" class="text-center py-8 text-gray-500">
            暂无数据
          </div>
          <div v-else class="space-y-3">
            <div
              v-for="(user, index) in stats.top_users"
              :key="user.user_id"
              class="flex items-center gap-4 p-3 rounded-xl hover:bg-gray-50 transition"
            >
              <span class="w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium"
                :class="Number(index) < 3 ? 'bg-yellow-100 text-yellow-700' : 'bg-gray-100 text-gray-600'">
                {{ Number(index) + 1 }}
              </span>
              <div class="flex-1 min-w-0">
                <p class="font-medium text-gray-800 truncate">{{ user.nickname || user.username }}</p>
              </div>
              <div class="text-right">
                <p class="text-xl font-bold text-pink-600">{{ user.vote_count }}</p>
                <p class="text-xs text-gray-400">票</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- By User Tab -->
    <div v-if="activeTab === 'by-user'" class="space-y-6">
      <!-- Search & Quick Actions -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Search -->
        <div class="lg:col-span-2 bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
          <h3 class="font-semibold text-gray-800 mb-4">搜索用户</h3>
          <div class="flex gap-3">
            <input
              v-model="keyword"
              @keyup.enter="handleSearch"
              type="text"
              placeholder="搜索用户名..."
              class="flex-1 px-4 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500"
            />
            <button
              @click="handleSearch"
              class="px-6 py-2.5 bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-xl hover:from-blue-700 hover:to-blue-800 transition-all shadow-lg shadow-blue-600/20 font-medium"
            >
              搜索
            </button>
          </div>
        </div>

        <!-- Stats Summary -->
        <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
          <h3 class="font-semibold text-gray-800 mb-4">统计</h3>
          <div class="text-center">
            <p class="text-4xl font-bold text-pink-600">{{ stats.total_voted_users }}</p>
            <p class="text-gray-500">参与投票用户</p>
          </div>
        </div>
      </div>

      <!-- User List -->
      <div class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
        <table class="w-full">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-4 text-left text-sm font-medium text-gray-500">用户</th>
              <th class="px-6 py-4 text-left text-sm font-medium text-gray-500">投票数</th>
              <th class="px-6 py-4 text-left text-sm font-medium text-gray-500">最近投票</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100">
            <tr v-if="userLoading">
              <td colspan="3" class="px-6 py-12 text-center text-gray-500">加载中...</td>
            </tr>
            <tr v-else-if="userVotes.length === 0">
              <td colspan="3" class="px-6 py-12 text-center text-gray-500">暂无数据</td>
            </tr>
            <tr v-else v-for="item in userVotes" :key="item.user_id" class="hover:bg-gray-50 transition">
              <td class="px-6 py-4">
                <div class="flex items-center gap-3">
                  <div class="w-10 h-10 rounded-full bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center text-white font-medium">
                    {{ (item.nickname || item.username)?.charAt(0).toUpperCase() }}
                  </div>
                  <div>
                    <p class="font-medium text-gray-800">{{ item.nickname || item.username }}</p>
                    <p class="text-sm text-gray-500">@{{ item.username }}</p>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4">
                <span class="text-2xl font-bold text-pink-600">{{ item.vote_count }}</span>
              </td>
              <td class="px-6 py-4">
                <div v-if="item.recent_votes?.length" class="space-y-1">
                  <p v-for="vote in item.recent_votes" :key="vote.work_id" class="text-sm text-gray-600">
                    {{ vote.work_name }} ({{ vote.team_name }})
                    <span class="text-gray-400 text-xs block">{{ formatDate(vote.created_at) }}</span>
                  </p>
                </div>
                <span v-else class="text-gray-400">-</span>
              </td>
            </tr>
          </tbody>
        </table>

        <!-- Pagination -->
        <div class="px-6 py-4 border-t border-gray-100 flex justify-center">
          <div class="flex gap-2">
            <button
              @click="handlePageChange(page - 1)"
              :disabled="page === 1"
              class="px-4 py-2 border border-gray-200 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50 transition"
            >
              上一页
            </button>
            <span class="px-4 py-2 text-gray-600">第 {{ page }} 页</span>
            <button
              @click="handlePageChange(page + 1)"
              :disabled="userVotes.length < pageSize"
              class="px-4 py-2 border border-gray-200 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50 transition"
            >
              下一页
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- By Work Tab -->
    <div v-if="activeTab === 'by-work'" class="space-y-6">
      <!-- Search & Quick Actions -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Search -->
        <div class="lg:col-span-2 bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
          <h3 class="font-semibold text-gray-800 mb-4">搜索作品</h3>
          <div class="flex gap-3">
            <input
              v-model="keyword"
              @keyup.enter="handleSearch"
              type="text"
              placeholder="搜索作品名/队伍名..."
              class="flex-1 px-4 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500"
            />
            <select
              v-model="statusFilter"
              @change="handleSearch"
              class="px-4 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500"
            >
              <option v-for="opt in statusOptions" :key="opt.value" :value="opt.value">
                {{ opt.label }}
              </option>
            </select>
            <button
              @click="handleSearch"
              class="px-6 py-2.5 bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-xl hover:from-blue-700 hover:to-blue-800 transition-all shadow-lg shadow-blue-600/20 font-medium"
            >
              搜索
            </button>
          </div>
        </div>

        <!-- Stats Summary -->
        <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
          <h3 class="font-semibold text-gray-800 mb-4">统计</h3>
          <div class="text-center">
            <p class="text-4xl font-bold text-pink-600">{{ stats.total_voted_works }}</p>
            <p class="text-gray-500">被投票作品</p>
          </div>
        </div>
      </div>

      <!-- Work List -->
      <div class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
        <table class="w-full">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-4 text-left text-sm font-medium text-gray-500">作品</th>
              <th class="px-6 py-4 text-left text-sm font-medium text-gray-500">队伍</th>
              <th class="px-6 py-4 text-left text-sm font-medium text-gray-500">状态</th>
              <th class="px-6 py-4 text-left text-sm font-medium text-gray-500">投票数</th>
              <th class="px-6 py-4 text-left text-sm font-medium text-gray-500">最近投票者</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100">
            <tr v-if="workLoading">
              <td colspan="5" class="px-6 py-12 text-center text-gray-500">加载中...</td>
            </tr>
            <tr v-else-if="workVotes.length === 0">
              <td colspan="5" class="px-6 py-12 text-center text-gray-500">暂无数据</td>
            </tr>
            <tr v-else v-for="item in workVotes" :key="item.work_id" class="hover:bg-gray-50 transition">
              <td class="px-6 py-4">
                <RouterLink :to="`/works/${item.work_id}`" class="font-medium text-blue-600 hover:underline">
                  {{ item.work_name }}
                </RouterLink>
              </td>
              <td class="px-6 py-4 text-gray-600">{{ item.team_name }}</td>
              <td class="px-6 py-4">
                <span :class="['px-3 py-1 rounded-full text-xs font-medium', statusColors[item.status] || 'bg-gray-100 text-gray-600']">
                  {{ item.status === 'pending' ? '待审核' : item.status === 'approved' ? '已通过' : item.status === 'rejected' ? '已拒绝' : item.status }}
                </span>
              </td>
              <td class="px-6 py-4">
                <span class="text-2xl font-bold text-pink-600">{{ item.vote_count }}</span>
              </td>
              <td class="px-6 py-4">
                <div v-if="item.recent_voters?.length" class="space-y-1">
                  <p v-for="voter in item.recent_voters" :key="voter.user_id" class="text-sm text-gray-600">
                    {{ voter.nickname || voter.username }}
                    <span class="text-gray-400 text-xs block">{{ formatDate(voter.created_at) }}</span>
                  </p>
                </div>
                <span v-else class="text-gray-400">-</span>
              </td>
            </tr>
          </tbody>
        </table>

        <!-- Pagination -->
        <div class="px-6 py-4 border-t border-gray-100 flex justify-center">
          <div class="flex gap-2">
            <button
              @click="handlePageChange(page - 1)"
              :disabled="page === 1"
              class="px-4 py-2 border border-gray-200 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50 transition"
            >
              上一页
            </button>
            <span class="px-4 py-2 text-gray-600">第 {{ page }} 页</span>
            <button
              @click="handlePageChange(page + 1)"
              :disabled="workVotes.length < pageSize"
              class="px-4 py-2 border border-gray-200 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50 transition"
            >
              下一页
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>