<script setup lang="ts">
import { ref, getCurrentInstance } from 'vue'

// Use instance to call parent notification
const instance = getCurrentInstance()

function getNotification() {
  // Try to find parent Notification component
  let parent = instance?.parent
  while (parent) {
    if (parent.exposed && parent.exposed.success) {
      return parent.exposed
    }
    parent = parent.parent
  }
  // Fallback to global
  return (window as any).$notify
}

function success(title: string, message?: string) {
  getNotification()?.success(title, message)
}

function error(title: string, message?: string) {
  getNotification()?.error(title, message)
}

function warning(title: string, message?: string) {
  getNotification()?.warning(title, message)
}

function info(title: string, message?: string) {
  getNotification()?.info(title, message)
}

defineExpose({
  success,
  error,
  warning,
  info,
  notify: {
    success,
    error,
    warning,
    info
  }
})
</script>

<template>
  <slot :notify="{ success, error, warning, info }"></slot>
</template>