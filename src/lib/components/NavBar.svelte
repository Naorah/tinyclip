<script lang="ts">
  import { onMount } from 'svelte';
  import Icon from '@iconify/svelte';
  import themeMode from "$lib/rune/ThemeMode.svelte";

  onMount(() => {
    const saved = localStorage.getItem('theme');
    if (saved === 'dark') {
      themeMode.isDark = true;
    } else if (saved === 'light') {
      themeMode.isDark = false;
    } else {
      themeMode.isDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    }
    document.documentElement.classList.toggle('dark', themeMode.isDark);
  });
  
  function toggleTheme() {
    themeMode.isDark = !themeMode.isDark;
    document.documentElement.classList.toggle('dark', themeMode.isDark);
    localStorage.setItem('theme', themeMode.isDark === true ? 'dark' : 'light');
  }
</script>

<nav class="fixed top-4 left-1/2 -translate-x-1/2 z-50 w-[90%] max-w-lg">
  <div class="flex items-center justify-between px-6 py-3 bg-white/80 dark:bg-gray-900/50 backdrop-blur-sm rounded-2xl shadow-lg">
    <div class="flex items-center gap-2">
      <img src="/favicon.svg" alt="TinyClip" class="w-8 h-8" />
      <span class="font-semibold text-gray-800 dark:text-white">TinyClip</span>
    </div>

    <button 
      class="p-2 rounded-xl hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors cursor-pointer"
      onclick={toggleTheme}
      aria-label="Toggle theme"
    >
      <Icon 
        icon={themeMode.isDark ? "lucide:sun" : "lucide:moon"} 
        class="text-xl text-gray-600 dark:text-gray-300" 
      />
    </button>
  </div>
</nav>
