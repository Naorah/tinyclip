<script lang="ts">
  import Icon from "@iconify/svelte";
  import { fade, fly } from "svelte/transition";
  import { onMount } from "svelte";
  import RotateLogo from "$lib/components/RotateLogo.svelte";

  let isDisplayed = $state(false);

  onMount(() => {
    isDisplayed = true;
  });
</script>

<!-- Hero Section -->
<section class="min-h-screen px-4 py-20 bg-gray-50 dark:bg-gray-900 flex items-center justify-center relative" transition:fade={{ duration: 1000, delay: 200 }}>
  <div class="absolute inset-0 bg-gray-50 dark:bg-gray-900">
    <RotateLogo src="/favicon.svg" />
  </div>
  
  {#if isDisplayed}
  <div class="max-w-4xl mx-auto text-center relative z-10" in:fade={{ duration: 1000, delay: 200 }}>
    <h1 class="text-5xl font-bold text-blue-600 dark:text-blue-500 mb-6" in:fly={{ y: -20, duration: 800, delay: 300 }}>
      TinyClip 
    </h1>
    <p class="text-xl text-gray-900 dark:text-gray-100 mb-80" in:fly={{ y: 20, duration: 800, delay: 500 }}>
      Compressez vos vidéos en toute simplicité, directement dans votre navigateur
    </p>
    
    <div class="flex flex-col justify-center items-center gap-8 mb-16">
      <div class="text-center w-full" in:fly={{ x: -20, duration: 800, delay: 700 }}>
        <div class="w-full p-8 bg-blue-100/50 dark:bg-blue-900/20 rounded-2xl flex items-center gap-4 
                    transition-all duration-300 ease-in-out hover:scale-[1.02] hover:shadow-lg hover:bg-blue-200/50 dark:hover:bg-blue-900/30 
                    cursor-pointer hover:border hover:border-blue-300 dark:hover:border-blue-700">
          <Icon icon="lucide:video" class="text-4xl text-blue-600 dark:text-blue-500 transition-transform duration-300 group-hover:scale-110" />
          <div class="text-left">
            <h3 class="text-lg font-semibold text-blue-600 dark:text-blue-500">Import</h3>
            <p class="text-gray-900 dark:text-gray-100">Sélectionnez votre vidéo à compresser</p>
          </div>
        </div>
      </div>

      <div class="text-center w-full" in:fly={{ x: 20, duration: 800, delay: 900 }}>
        <div class="w-full p-8 bg-blue-100/50 dark:bg-blue-900/20 rounded-2xl flex items-center gap-4
                    transition-all duration-300 ease-in-out hover:scale-[1.02] hover:shadow-lg hover:bg-blue-200/50 dark:hover:bg-blue-900/30
                    cursor-pointer hover:border hover:border-blue-300 dark:hover:border-blue-700">
          <Icon icon="lucide:zap" class="text-4xl text-blue-600 dark:text-blue-500 transition-transform duration-300 group-hover:scale-110" />
          <div class="text-left">
            <h3 class="text-lg font-semibold text-blue-600 dark:text-blue-500">Compression</h3>
            <p class="text-gray-900 dark:text-gray-100">Compression rapide et efficace</p>
          </div>
        </div>
      </div>

      <div class="text-center w-full" in:fly={{ x: -20, duration: 800, delay: 1100 }}>
        <div class="w-full p-8 bg-blue-100/50 dark:bg-blue-900/20 rounded-2xl flex items-center gap-4
                    transition-all duration-300 ease-in-out hover:scale-[1.02] hover:shadow-lg hover:bg-blue-200/50 dark:hover:bg-blue-900/30
                    cursor-pointer hover:border hover:border-blue-300 dark:hover:border-blue-700">
          <Icon icon="lucide:shield" class="text-4xl text-blue-600 dark:text-blue-500 transition-transform duration-300 group-hover:scale-110" />
          <div class="text-left">
            <h3 class="text-lg font-semibold text-blue-600 dark:text-blue-500">Sécurité</h3>
            <p class="text-gray-900 dark:text-gray-100">Aucun stockage permanent de vos fichiers</p>
          </div>
        </div>
      </div>

      <div class="text-center w-full" in:fly={{ x: 20, duration: 800, delay: 1300 }}>
        <div class="w-full p-8 bg-blue-100/50 dark:bg-blue-900/20 rounded-2xl flex items-center gap-4
                    transition-all duration-300 ease-in-out hover:scale-[1.02] hover:shadow-lg hover:bg-blue-200/50 dark:hover:bg-blue-900/30
                    cursor-pointer hover:border hover:border-blue-300 dark:hover:border-blue-700">
          <Icon icon="lucide:download" class="text-4xl text-blue-600 dark:text-blue-500 transition-transform duration-300 group-hover:scale-110" />
          <div class="text-left">
            <h3 class="text-lg font-semibold text-blue-600 dark:text-blue-500">Export</h3>
            <p class="text-gray-900 dark:text-gray-100">Téléchargez votre vidéo compressée</p>
          </div>
        </div>
      </div>
      </div>
    </div>
  {/if}
</section>
