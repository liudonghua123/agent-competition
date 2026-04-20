<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { teamApi } from '@/api'

const route = useRoute()
const team = ref<any>(null)
const loading = ref(true)

onMounted(async () => {
  try {
    const response = await teamApi.get(Number(route.params.id))
    team.value = response.data
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div>
    <RouterLink to="/admin/teams" class="text-blue-600 hover:text-blue-700 mb-4 inline-block">← 返回队伍列表</RouterLink>

    <div v-if="loading" class="text-center py-12 text-gray-500">加载中...</div>
    <div v-else-if="team" class="bg-white rounded-lg shadow-sm border p-6">
      <h1 class="text-2xl font-bold text-gray-800 mb-4">{{ team.name }}</h1>
      <p class="text-gray-600 mb-6">{{ team.description || '暂无描述' }}</p>

      <h2 class="text-lg font-semibold mb-4">队伍成员</h2>
      <table class="w-full">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-4 py-2 text-left">姓名</th>
            <th class="px-4 py-2 text-left">学工号</th>
            <th class="px-4 py-2 text-left">角色</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="member in team.members" :key="member.id" class="border-t">
            <td class="px-4 py-2">{{ member.name }}</td>
            <td class="px-4 py-2">{{ member.student_id }}</td>
            <td class="px-4 py-2">{{ member.is_leader ? '队长' : '成员' }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>