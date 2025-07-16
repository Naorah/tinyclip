<script lang="ts">
  import Icon from "@iconify/svelte";
  import { fade, fly } from "svelte/transition";
  import { onMount } from "svelte";

  let isDisplayed = $state(false);

  onMount(() => {
    isDisplayed = true;
  });
</script>

<!-- Hero Section -->
<section class="min-h-screen px-4 py-20 bg-gradient-to-br from-pink-400/40 to-violet-400/40 flex items-center justify-center" transition:fade={{ duration: 1000, delay: 200 }}>
  {#if isDisplayed}
  <div class="max-w-4xl mx-auto text-center" in:fade={{ duration: 1000, delay: 200 }}>
    <h1 class="text-5xl font-bold text-violet-400 mb-6" in:fly={{ y: -20, duration: 800, delay: 300 }}>
      TinyClip <Icon icon="lucide:video" class="inline" />
    </h1>
    <p class="text-xl text-gray-600 mb-12" in:fly={{ y: 20, duration: 800, delay: 500 }}>
      Compressez vos vidéos en toute simplicité, directement dans votre navigateur
    </p>
    
    <div class="flex flex-col justify-center items-center gap-8 mb-16">
      <div class="text-center w-full" in:fly={{ x: -20, duration: 800, delay: 700 }}>
        <div class="w-full p-8 bg-pink-400/10 rounded-2xl flex items-center gap-4">
          <Icon icon="lucide:video" class="text-4xl text-pink-400" />
          <div class="text-left">
            <h3 class="text-lg font-semibold text-pink-400">Import</h3>
            <p class="text-gray-600">Sélectionnez votre vidéo à compresser</p>
          </div>
        </div>
      </div>

      <div class="text-center w-full" in:fly={{ x: 20, duration: 800, delay: 900 }}>
        <div class="w-full p-8 bg-violet-400/10 rounded-2xl flex items-center gap-4">
          <Icon icon="lucide:zap" class="text-4xl text-violet-400" />
          <div class="text-left">
            <h3 class="text-lg font-semibold text-violet-400">Compression</h3>
            <p class="text-gray-600">Compression rapide et efficace</p>
          </div>
        </div>
      </div>

      <div class="text-center w-full" in:fly={{ x: -20, duration: 800, delay: 1100 }}>
        <div class="w-full p-8 bg-emerald-400/10 rounded-2xl flex items-center gap-4">
          <Icon icon="lucide:shield" class="text-4xl text-emerald-400" />
          <div class="text-left">
            <h3 class="text-lg font-semibold text-emerald-400">Sécurité</h3>
            <p class="text-gray-600">Traitement 100% local, aucun upload de fichier</p>
          </div>
        </div>
      </div>

      <div class="text-center w-full" in:fly={{ x: 20, duration: 800, delay: 1300 }}>
        <div class="w-full p-8 bg-blue-400/10 rounded-2xl flex items-center gap-4">
          <Icon icon="lucide:download" class="text-4xl text-blue-400" />
          <div class="text-left">
            <h3 class="text-lg font-semibold text-blue-400">Export</h3>
            <p class="text-gray-600">Téléchargez votre vidéo compressée</p>
          </div>
        </div>
      </div>
      </div>
    </div>
  {/if}
</section>
