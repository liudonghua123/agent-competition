<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { agentCenterApi } from '@/api'

const router = useRouter()
const route = useRoute()

const allAgents = ref<any[]>([])
const filteredAgents = ref<any[]>([])
const loading = ref(true)
const error = ref('')
const page = ref(1)
const pageSize = 50

// Categories list
const categories = [
  { Code: '', Name: '全部' },
  { Code: '2026_agent_competition', Name: '2026智能体大赛' },
  { Code: 'Logistics', Name: '物流' },
  { Code: 'WorkAssistant', Name: '工作助手' },
  { Code: 'TextCreation', Name: '文本创作' },
  { Code: 'BusinessAssistant', Name: '商业助手' },
  { Code: 'Manufacture', Name: '制造业' },
  { Code: 'Finance', Name: '金融' },
  { Code: 'Law', Name: '法律' },
  { Code: 'Medical', Name: '医疗健康' },
  { Code: 'Scientific', Name: '科研' },
  { Code: 'Education', Name: '教育' }
]

// Filters
const selectedCategory = ref<string>('')
const keyword = ref('')
const sort = ref<'latest' | 'popular'>('latest')

// Debounce
let searchTimeout: number | null = null

const totalPages = computed(() => Math.ceil(filteredAgents.value.length / pageSize))

onMounted(async () => {
  if (route.query.category) {
    selectedCategory.value = route.query.category as string
  }
  if (route.query.sort) {
    sort.value = route.query.sort as 'latest' | 'popular'
  }
  await fetchAgents()
})

async function fetchAgents() {
  loading.value = true
  error.value = ''
  try {
    const res = await agentCenterApi.listAgents({
      page: 1,
      page_size: 100,
      sort: sort.value
    })
    allAgents.value = res.data.Result?.Items || []
    applyFilters()
  } catch (e: any) {
    error.value = e.response?.data?.detail || e.message || '加载失败'
  } finally {
    loading.value = false
  }
}

function applyFilters() {
  let result = [...allAgents.value]

  // Category filter
  if (selectedCategory.value) {
    result = result.filter(agent =>
      agent.CategoryList?.some((c: any) => c.CategoryCode === selectedCategory.value)
    )
  }

  // Keyword filter (search name and description)
  if (keyword.value.trim()) {
    const kw = keyword.value.toLowerCase()
    result = result.filter(agent =>
      agent.Name?.toLowerCase().includes(kw) ||
      agent.Description?.toLowerCase().includes(kw)
    )
  }

  // Sort
  if (sort.value === 'latest') {
    result.sort((a, b) => (b.SubmitTimestamp || 0) - (a.SubmitTimestamp || 0))
  } else {
    result.sort((a, b) => (b.FavoriteCount || 0) - (a.FavoriteCount || 0))
  }

  // Paginate
  const start = (page.value - 1) * pageSize
  filteredAgents.value = result.slice(start, start + pageSize)
}

function handleKeywordInput() {
  if (searchTimeout) clearTimeout(searchTimeout)
  searchTimeout = window.setTimeout(() => {
    page.value = 1
    applyFilters()
  }, 300)
}

function selectCategory(code: string) {
  selectedCategory.value = code
  page.value = 1
  updateUrl()
  applyFilters()
}

function handleSortChange(newSort: 'latest' | 'popular') {
  sort.value = newSort
  page.value = 1
  updateUrl()
  applyFilters()
}

function handlePageChange(newPage: number) {
  page.value = newPage
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

function updateUrl() {
  const query: any = {}
  if (selectedCategory.value) query.category = selectedCategory.value
  if (sort.value !== 'latest') query.sort = sort.value
  router.replace({ query })
}

function openAgent(appId: string) {
  window.open(`https://agent.ynu.edu.cn/product/llm/mall/application/${appId}/chat`, '_blank')
}

watch(keyword, handleKeywordInput)
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 text-white py-10">
      <div class="max-w-7xl mx-auto px-4">
        <h1 class="text-3xl font-bold mb-2">智能体中心</h1>
        <p class="text-blue-100 text-sm">同步智能体开放平台上的智能体中心</p>
      </div>
    </div>

    <div class="max-w-7xl mx-auto px-4 py-6">
      <!-- Search and Sort -->
      <div class="flex flex-col sm:flex-row gap-3 mb-5">
        <div class="flex-1">
          <div class="relative">
            <input
              v-model="keyword"
              type="text"
              placeholder="搜索智能体名称或描述..."
              class="w-full pl-10 pr-4 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
            />
            <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
            </svg>
          </div>
        </div>
        <div class="flex gap-2">
          <button
            @click="handleSortChange('latest')"
            class="px-3 py-2 rounded-lg text-sm font-medium transition-all"
            :class="sort === 'latest' ? 'bg-blue-600 text-white' : 'bg-white text-gray-600 hover:bg-gray-100'"
          >
            最新上架
          </button>
          <button
            @click="handleSortChange('popular')"
            class="px-3 py-2 rounded-lg text-sm font-medium transition-all"
            :class="sort === 'popular' ? 'bg-blue-600 text-white' : 'bg-white text-gray-600 hover:bg-gray-100'"
          >
            最受欢迎
          </button>
        </div>
      </div>

      <!-- Category Tabs -->
      <div class="mb-5 flex flex-wrap gap-2">
        <button
          v-for="cat in categories"
          :key="cat.Code"
          @click="selectCategory(cat.Code)"
          class="px-3 py-1.5 rounded-full text-xs font-medium transition-all"
          :class="selectedCategory === cat.Code ? 'bg-blue-600 text-white' : 'bg-white text-gray-600 hover:bg-gray-100 border border-gray-200'"
        >
          {{ cat.Name }}
        </button>
      </div>

      <!-- Results Count -->
      <div class="text-sm text-gray-500 mb-4">
        共 {{ filteredAgents.length }} 个智能体
        <span v-if="keyword"> · 搜索 "{{ keyword }}"</span>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="text-center py-16">
        <div class="inline-block w-10 h-10 border-3 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
        <p class="mt-3 text-gray-500 text-sm">加载中...</p>
      </div>

      <!-- Error -->
      <div v-else-if="error" class="text-center py-12 bg-white rounded-xl">
        <p class="text-red-500 mb-1">{{ error }}</p>
        <p class="text-gray-400 text-xs">请检查火山引擎 API 配置是否正确</p>
      </div>

      <!-- Empty -->
      <div v-else-if="filteredAgents.length === 0" class="text-center py-16 bg-white rounded-xl">
        <p class="text-gray-500">暂无智能体</p>
        <p class="text-gray-400 text-xs mt-1">换个关键词试试</p>
      </div>

      <!-- Agent List -->
      <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        <div
          v-for="agent in filteredAgents"
          :key="agent.AppID"
          class="bg-white rounded-xl p-4 border border-gray-100 hover:border-blue-200 hover:shadow-sm transition-all cursor-pointer"
          @click="openAgent(agent.AppID)"
        >
          <div class="flex flex-col h-full">
            <div class="flex-1">
              <h3 class="font-medium text-gray-800 hover:text-blue-600 transition-colors line-clamp-1">
                {{ agent.Name }}
              </h3>
              <p class="text-gray-500 text-sm mt-1 line-clamp-2 min-h-[2.5rem]">
                {{ agent.Description || '暂无描述' }}
              </p>
            </div>
            <div class="flex flex-wrap items-center gap-1 mt-3">
              <span
                v-for="cat in agent.CategoryList"
                :key="cat.CategoryCode"
                class="px-2 py-0.5 bg-gray-100 text-gray-600 text-xs rounded"
              >
                {{ cat.CategoryName }}
              </span>
            </div>
            <div class="flex items-center gap-4 mt-3 pt-2 border-t border-gray-100 text-xs text-gray-400">
              <span class="flex items-center gap-1">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/>
                </svg>
                {{ agent.FavoriteCount || 0 }}
              </span>
              <span class="flex items-center gap-1">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                </svg>
                {{ agent.UseCount || 0 }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Pagination -->
      <div v-if="totalPages > 1" class="flex justify-center items-center gap-2 mt-6">
        <button
          @click="handlePageChange(page - 1)"
          :disabled="page === 1"
          class="px-3 py-1.5 rounded-lg border text-sm hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          上一页
        </button>
        <span class="px-3 py-1.5 text-sm text-gray-600">
          {{ page }} / {{ totalPages }}
        </span>
        <button
          @click="handlePageChange(page + 1)"
          :disabled="page === totalPages"
          class="px-3 py-1.5 rounded-lg border text-sm hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          下一页
        </button>
      </div>
    </div>
  </div>
</template>