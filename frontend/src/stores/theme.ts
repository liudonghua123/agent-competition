import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

export const useThemeStore = defineStore('theme', () => {
  // 暗黑模式
  const isDark = ref(false)

  // 主题色
  const themeColor = ref('#3b82f6') // 默认蓝色

  // 从 localStorage 初始化
  function init() {
    const savedDark = localStorage.getItem('theme-dark')
    const savedColor = localStorage.getItem('theme-color')

    if (savedDark !== null) {
      isDark.value = savedDark === 'true'
    } else {
      // 默认跟随系统
      isDark.value = window.matchMedia('(prefers-color-scheme: dark)').matches
    }

    if (savedColor) {
      themeColor.value = savedColor
    }

    applyTheme()
  }

  // 应用主题
  function applyTheme() {
    const root = document.documentElement

    // 暗黑模式
    if (isDark.value) {
      root.classList.add('dark')
    } else {
      root.classList.remove('dark')
    }

    // 主题色
    root.style.setProperty('--theme-primary', themeColor.value)
  }

  // 切换暗黑模式
  function toggleDark() {
    isDark.value = !isDark.value
    localStorage.setItem('theme-dark', String(isDark.value))
    applyTheme()
  }

  // 设置主题色
  function setThemeColor(color: string) {
    themeColor.value = color
    localStorage.setItem('theme-color', color)
    applyTheme()
  }

  // 监听变化
  watch(isDark, applyTheme)
  watch(themeColor, applyTheme)

  return {
    isDark,
    themeColor,
    init,
    toggleDark,
    setThemeColor,
    applyTheme
  }
})