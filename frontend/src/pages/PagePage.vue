<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { contentApi } from '@/api'

const route = useRoute()

const content = ref<any>(null)
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  await fetchContent()
})

async function fetchContent() {
  loading.value = true
  try {
    const response = await contentApi.getBySlug(route.params.slug as string)
    content.value = response.data
  } catch (e: any) {
    error.value = e.response?.data?.detail || '页面不存在'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="max-w-4xl mx-auto px-4 py-8">
    <div v-if="loading" class="text-center py-12 text-gray-500">加载中...</div>
    <div v-else-if="error" class="text-center py-12 text-red-500">{{ error }}</div>
    <div v-else-if="content" class="bg-white rounded-lg shadow-sm border p-8">
      <h1 class="text-3xl font-bold text-gray-800 mb-6">{{ content.title }}</h1>
      <div class="prose max-w-none" v-html="content.content"></div>
    </div>
  </div>
</template>