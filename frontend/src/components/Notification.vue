<script setup lang="ts">
import { ref, computed } from 'vue'

const notifications = ref<Array<{
  id: number
  type: 'success' | 'error' | 'warning' | 'info'
  title: string
  message?: string
  duration?: number
}>>([])

let nextId = 1

function addNotification(type: 'success' | 'error' | 'warning' | 'info', title: string, message?: string, duration = 3000) {
  const id = nextId++
  notifications.value.push({ id, type, title, message, duration })

  if (duration > 0) {
    setTimeout(() => {
      removeNotification(id)
    }, duration)
  }
}

function removeNotification(id: number) {
  const index = notifications.value.findIndex(n => n.id === id)
  if (index > -1) {
    notifications.value.splice(index, 1)
  }
}

function getIcon(type: string) {
  switch (type) {
    case 'success': return 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z'
    case 'error': return 'M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z'
    case 'warning': return 'M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z'
    default: return 'M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z'
  }
}

function getColors(type: string) {
  switch (type) {
    case 'success': return 'bg-green-50 border-green-200 text-green-800'
    case 'error': return 'bg-red-50 border-red-200 text-red-800'
    case 'warning': return 'bg-amber-50 border-amber-200 text-amber-800'
    default: return 'bg-blue-50 border-blue-200 text-blue-800'
  }
}

function getIconColors(type: string) {
  switch (type) {
    case 'success': return 'text-green-500'
    case 'error': return 'text-red-500'
    case 'warning': return 'text-amber-500'
    default: return 'text-blue-500'
  }
}

// Expose methods globally
defineExpose({
  success: (title: string, message?: string) => addNotification('success', title, message),
  error: (title: string, message?: string) => addNotification('error', title, message, 5000),
  warning: (title: string, message?: string) => addNotification('warning', title, message),
  info: (title: string, message?: string) => addNotification('info', title, message)
})

// Also expose to window for global usage
if (typeof window !== 'undefined') {
  ;(window as any).$notify = {
    success: (title: string, message?: string) => addNotification('success', title, message),
    error: (title: string, message?: string) => addNotification('error', title, message, 5000),
    warning: (title: string, message?: string) => addNotification('warning', title, message),
    info: (title: string, message?: string) => addNotification('info', title, message)
  }
}
</script>

<template>
  <Teleport to="body">
    <div class="fixed top-4 right-4 z-[100] space-y-3 max-w-sm w-full pointer-events-none">
      <TransitionGroup name="notification">
        <div
          v-for="notification in notifications"
          :key="notification.id"
          class="pointer-events-auto p-4 rounded-xl border shadow-lg flex items-start gap-3"
          :class="getColors(notification.type)"
        >
          <svg class="w-5 h-5 flex-shrink-0" :class="getIconColors(notification.type)" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="getIcon(notification.type)" />
          </svg>
          <div class="flex-1 min-w-0">
            <p class="font-medium">{{ notification.title }}</p>
            <p v-if="notification.message" class="text-sm opacity-80 mt-0.5">{{ notification.message }}</p>
          </div>
          <button
            @click="removeNotification(notification.id)"
            class="flex-shrink-0 p-1 rounded-lg hover:bg-black/5 transition-colors"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </TransitionGroup>
    </div>
  </Teleport>
</template>

<style scoped>
.notification-enter-active {
  transition: all 0.3s ease;
}

.notification-leave-active {
  transition: all 0.2s ease;
}

.notification-enter-from {
  opacity: 0;
  transform: translateX(100%);
}

.notification-leave-to {
  opacity: 0;
  transform: translateX(100%);
}

.notification-move {
  transition: transform 0.2s ease;
}
</style>