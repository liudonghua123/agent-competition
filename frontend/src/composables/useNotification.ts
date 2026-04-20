import { ref } from 'vue'

// Global notification functions
export function useNotification() {
  const notify = (window as any).$notify

  function success(title: string, message?: string) {
    notify?.success(title, message)
  }

  function error(title: string, message?: string) {
    notify?.error(title, message)
  }

  function warning(title: string, message?: string) {
    notify?.warning(title, message)
  }

  function info(title: string, message?: string) {
    notify?.info(title, message)
  }

  return {
    success,
    error,
    warning,
    info
  }
}