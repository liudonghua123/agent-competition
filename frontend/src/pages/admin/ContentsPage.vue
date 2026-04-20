<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '@/api'
import ConfirmDialog from '@/components/ConfirmDialog.vue'
import { useNotification } from '@/composables/useNotification'

const { success, error } = useNotification()

const contents = ref<any[]>([])
const loading = ref(true)
const page = ref(1)
const total = ref(0)
const pageSize = 20
const typeFilter = ref('')

const showModal = ref(false)

// Confirm dialog state
const showConfirm = ref(false)
const confirmMessage = ref('')
const confirmCallback = ref<(() => void) | null>(null)
const editingContent = ref<any>(null)
const formData = ref({
  title: '',
  slug: '',
  type: 'page',
  content: '',
  content_format: 'markdown',
  is_published: false,
  order: 0
})

onMounted(() => {
  fetchContents()
})

async function fetchContents() {
  loading.value = true
  try {
    const res = await api.get('/contents', {
      params: {
        page: page.value,
        page_size: pageSize,
        type: typeFilter.value || undefined
      }
    })
    contents.value = res.data.items || []
    total.value = res.data.total || 0
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

function openCreate() {
  editingContent.value = null
  formData.value = {
    title: '',
    slug: '',
    type: 'page',
    content: '',
    content_format: 'markdown',
    is_published: false,
    order: 0
  }
  showModal.value = true
}

function openEdit(content: any) {
  editingContent.value = content
  formData.value = {
    title: content.title,
    slug: content.slug,
    type: content.type,
    content: content.content || '',
    content_format: content.content_format,
    is_published: content.is_published,
    order: content.order
  }
  showModal.value = true
}

async function handleSave() {
  try {
    if (editingContent.value) {
      await api.put(`/contents/${editingContent.value.id}`, formData.value)
    } else {
      await api.post('/contents', formData.value)
    }
    showModal.value = false
    success('保存成功')
    await fetchContents()
  } catch (e: any) {
    error('操作失败', e.response?.data?.detail)
  }
}

async function handleDelete(content: any) {
  confirmMessage.value = `确定删除内容 "${content.title}" 吗？此操作不可恢复。`
  showConfirm.value = true
  confirmCallback.value = async () => {
    try {
      await api.delete(`/contents/${content.id}`)
      success('删除成功')
      await fetchContents()
    } catch (e: any) {
      error('删除失败', e.response?.data?.detail)
    }
  }
}

async function handleGenerateStatic(content: any) {
  try {
    const res = await api.post(`/contents/${content.id}/generate-static`)
    success('生成成功', `静态页面已生成: ${res.data.path}`)
  } catch (e: any) {
    error('生成失败', e.response?.data?.detail)
  }
}

function handlePageChange(newPage: number) {
  page.value = newPage
  fetchContents()
}
</script>

<template>
  <div>
    <!-- Header -->
    <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 mb-6">
      <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 class="text-2xl font-bold text-gray-800">内容管理</h1>
          <p class="text-sm text-gray-500 mt-1">管理页面与栏目内容</p>
        </div>
        <button
          @click="openCreate"
          class="inline-flex items-center gap-2 px-5 py-2.5 bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-xl hover:from-blue-700 hover:to-blue-800 transition-all shadow-lg shadow-blue-600/20 font-medium"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"/>
          </svg>
          创建内容
        </button>
      </div>
    </div>

    <!-- Filters -->
    <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-4 mb-6">
      <div class="flex gap-4">
        <select
          v-model="typeFilter"
          class="px-4 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all bg-white min-w-[140px]"
          @change="fetchContents"
        >
          <option value="">全部类型</option>
          <option value="page">页面</option>
          <option value="category">栏目</option>
        </select>
      </div>
    </div>

    <!-- Table -->
    <div class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
      <table class="w-full">
        <thead>
          <tr class="bg-gradient-to-r from-gray-50 to-gray-100 border-b border-gray-200">
            <th class="px-6 py-4 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">ID</th>
            <th class="px-6 py-4 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">标题</th>
            <th class="px-6 py-4 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Slug</th>
            <th class="px-6 py-4 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">类型</th>
            <th class="px-6 py-4 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">状态</th>
            <th class="px-6 py-4 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">操作</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
          <tr
            v-for="content in contents"
            :key="content.id"
            class="hover:bg-blue-50/50 transition-colors"
          >
            <td class="px-6 py-4 text-sm font-medium text-gray-900">{{ content.id }}</td>
            <td class="px-6 py-4 text-sm text-gray-800 font-medium">{{ content.title }}</td>
            <td class="px-6 py-4 text-sm text-gray-600 font-mono text-xs">{{ content.slug }}</td>
            <td class="px-6 py-4 text-sm">
              <span
                class="inline-flex items-center px-2.5 py-1 rounded-lg text-xs font-medium"
                :class="content.type === 'page' ? 'bg-blue-100 text-blue-700' : 'bg-purple-100 text-purple-700'"
              >
                <span class="w-1.5 h-1.5 rounded-full mr-1.5" :class="content.type === 'page' ? 'bg-blue-500' : 'bg-purple-500'"></span>
                {{ content.type === 'page' ? '页面' : '栏目' }}
              </span>
            </td>
            <td class="px-6 py-4 text-sm">
              <span
                class="inline-flex items-center gap-1.5"
                :class="content.is_published ? 'text-green-600' : 'text-gray-400'"
              >
                <span class="w-2 h-2 rounded-full" :class="content.is_published ? 'bg-green-500' : 'bg-gray-400'"></span>
                {{ content.is_published ? '已发布' : '草稿' }}
              </span>
            </td>
            <td class="px-6 py-4 text-sm">
              <div class="flex items-center gap-2">
                <button @click="openEdit(content)" class="text-blue-600 hover:text-blue-700 font-medium transition-colors">编辑</button>
                <span class="text-gray-300">|</span>
                <button @click="handleGenerateStatic(content)" class="text-green-600 hover:text-green-700 font-medium transition-colors">生成静态</button>
                <span class="text-gray-300">|</span>
                <button @click="handleDelete(content)" class="text-red-600 hover:text-red-700 font-medium transition-colors">删除</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>

      <div v-if="loading" class="text-center py-12">
        <div class="inline-flex items-center gap-2 text-gray-500">
          <svg class="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          加载中...
        </div>
      </div>
      <div v-else-if="contents.length === 0" class="text-center py-12 text-gray-500">
        <svg class="w-12 h-12 mx-auto text-gray-300 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
        </svg>
        暂无数据
      </div>

      <div v-if="total > pageSize" class="px-6 py-4 border-t border-gray-100 flex justify-center">
        <div class="flex items-center gap-1">
          <button
            @click="handlePageChange(page - 1)"
            :disabled="page === 1"
            class="px-3 py-1.5 rounded-lg border border-gray-200 text-sm font-medium text-gray-600 hover:bg-gray-50 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
          >
            上一页
          </button>
          <div class="px-4 py-1.5 bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-lg text-sm font-medium shadow-md">
            {{ page }} / {{ Math.ceil(total / pageSize) }}
          </div>
          <button
            @click="handlePageChange(page + 1)"
            :disabled="page * pageSize >= total"
            class="px-3 py-1.5 rounded-lg border border-gray-200 text-sm font-medium text-gray-600 hover:bg-gray-50 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
          >
            下一页
          </button>
        </div>
      </div>
    </div>

    <!-- Modal -->
    <div v-if="showModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-2xl max-h-[90vh] flex flex-col overflow-hidden">
        <div class="bg-gradient-to-r from-blue-600 to-blue-700 px-6 py-4">
          <h3 class="text-lg font-semibold text-white">{{ editingContent ? '编辑内容' : '创建内容' }}</h3>
          <p class="text-blue-100 text-sm">{{ editingContent ? '修改内容信息' : '创建新的页面或栏目' }}</p>
        </div>
        <form @submit.prevent="handleSave" class="p-6 space-y-5 overflow-y-auto flex-1">
          <div class="grid md:grid-cols-2 gap-5">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">标题 <span class="text-red-500">*</span></label>
              <input
                v-model="formData.title"
                type="text"
                required
                class="w-full px-4 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">Slug <span class="text-red-500">*</span></label>
              <input
                v-model="formData.slug"
                type="text"
                required
                class="w-full px-4 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all font-mono text-sm"
              />
            </div>
          </div>

          <div class="grid md:grid-cols-2 gap-5">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">类型</label>
              <select
                v-model="formData.type"
                class="w-full px-4 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all bg-white"
              >
                <option value="page">页面</option>
                <option value="category">栏目</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">排序</label>
              <input
                v-model.number="formData.order"
                type="number"
                class="w-full px-4 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all"
              />
            </div>
          </div>

          <div class="grid md:grid-cols-2 gap-5">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">内容格式</label>
              <select
                v-model="formData.content_format"
                class="w-full px-4 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all bg-white"
              >
                <option value="markdown">Markdown</option>
                <option value="html">HTML</option>
              </select>
            </div>
            <div class="flex items-center pt-5">
              <label class="flex items-center gap-3 cursor-pointer">
                <div class="relative">
                  <input v-model="formData.is_published" type="checkbox" class="sr-only peer" />
                  <div class="w-11 h-6 bg-gray-200 rounded-full peer peer-checked:bg-blue-600 transition-colors"></div>
                  <div class="absolute left-0.5 top-0.5 w-5 h-5 bg-white rounded-full shadow peer-checked:translate-x-5 transition-transform"></div>
                </div>
                <span class="text-sm font-medium text-gray-700">立即发布</span>
              </label>
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">内容</label>
            <textarea
              v-model="formData.content"
              rows="10"
              class="w-full px-4 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all font-mono text-sm"
            ></textarea>
            <p class="text-xs text-gray-500 mt-1.5">支持 Markdown 或 HTML 格式</p>
          </div>

          <div class="flex justify-end gap-3 pt-4 border-t border-gray-100">
            <button
              type="button"
              @click="showModal = false"
              class="px-5 py-2.5 border border-gray-200 rounded-xl hover:bg-gray-50 font-medium text-gray-700 transition-colors"
            >
              取消
            </button>
            <button
              type="submit"
              class="px-5 py-2.5 bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-xl hover:from-blue-700 hover:to-blue-800 transition-all shadow-lg shadow-blue-600/20 font-medium"
            >
              保存
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Confirm Dialog -->
    <ConfirmDialog
      :show="showConfirm"
      title="确认删除"
      :message="confirmMessage"
      confirm-text="删除"
      cancel-text="取消"
      type="danger"
      @confirm="() => { if (confirmCallback) confirmCallback(); showConfirm = false }"
      @cancel="showConfirm = false"
      @close="showConfirm = false"
    />
  </div>
</template>