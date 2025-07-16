<script lang="ts">
  import Icon from "@iconify/svelte";
  import { fly } from "svelte/transition";
</script>

<!-- Comment ça marche -->
<section class="py-20 px-4 bg-[#F9FAFB] dark:bg-[#0F172A]">
  <div class="max-w-4xl mx-auto text-center mb-16">
    <h2 class="text-3xl font-bold text-[#2563EB] dark:text-[#3B82F6] mb-6" in:fly={{ y: -20, duration: 800 }}>
      Comment ça fonctionne ?
    </h2>
    <p class="text-xl text-[#111827] dark:text-[#F1F5F9]" in:fly={{ y: 20, duration: 800 }}>
      Une solution simple, sécurisée et respectueuse de votre vie privée
    </p>
  </div>

  <div class="max-w-4xl mx-auto grid md:grid-cols-2 gap-12">
    <div class="p-8 bg-white dark:bg-gray-800 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700" in:fly={{ x: -20, duration: 800 }}>
      <div class="flex flex-row items-center gap-3 mb-6">
        <Icon icon="lucide:heart" class="text-[#2563EB] dark:text-[#3B82F6]" width="32" height="32"/>
        <h3 class="text-2xl font-semibold text-[#2563EB] dark:text-[#3B82F6]">Concept</h3>
      </div>
      <ul class="space-y-4">
        <li class="flex items-center gap-3">
          <Icon icon="lucide:check" class="text-[#2563EB] dark:text-[#3B82F6]" />
          <span class="text-[#111827] dark:text-[#F1F5F9]">Compression ciblée sans perte majeure</span>
        </li>
        <li class="flex items-center gap-3">
          <Icon icon="lucide:check" class="text-[#2563EB] dark:text-[#3B82F6]" />
          <span class="text-[#111827] dark:text-[#F1F5F9]">Interface minimale épurée et intuitive</span>
        </li>
        <li class="flex items-center gap-3">
          <Icon icon="lucide:check" class="text-[#2563EB] dark:text-[#3B82F6]" />
          <span class="text-[#111827] dark:text-[#F1F5F9]">Usage rapide et sans installation</span>
        </li>
      </ul>
    </div>

    <div class="p-8 bg-white dark:bg-gray-800 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700" in:fly={{ x: 20, duration: 800 }}>
      <div class="flex flex-row items-center gap-3 mb-6">
        <Icon icon="lucide:cog" class="text-[#2563EB] dark:text-[#3B82F6]" width="32" height="32"/>
        <h3 class="text-2xl font-semibold text-[#2563EB] dark:text-[#3B82F6]">Fonctionnement</h3>
      </div>
      <ul class="space-y-4">
        <li class="flex items-center gap-3">
          <Icon icon="lucide:check" class="text-[#2563EB] dark:text-[#3B82F6]" />
          <span class="text-[#111827] dark:text-[#F1F5F9]">Compression en deux passes pour une qualité optimale</span>
        </li>
        <li class="flex items-center gap-3">
          <Icon icon="lucide:check" class="text-[#2563EB] dark:text-[#3B82F6]" />
          <span class="text-[#111827] dark:text-[#F1F5F9]">Choix de la compression pour l'utilisation</span>
        </li>
        <li class="flex items-center gap-3">
          <Icon icon="lucide:check" class="text-[#2563EB] dark:text-[#3B82F6]" />
          <span class="text-[#111827] dark:text-[#F1F5F9]">Progression en temps réel pour le meilleur feedback</span>
        </li>
      </ul>
    </div>

    <div class="p-8 bg-white dark:bg-gray-800 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700" in:fly={{ x: 20, duration: 800, delay: 200 }}>
      <div class="flex flex-row items-center gap-3 mb-6">
        <Icon icon="lucide:venetian-mask" class="text-[#2563EB] dark:text-[#3B82F6]" width="32" height="32"/>
        <h3 class="text-2xl font-semibold text-[#2563EB] dark:text-[#3B82F6]">Confidentialité</h3>
      </div>
      <ul class="space-y-4">
        <li class="flex items-center gap-3">
          <Icon icon="lucide:check" class="text-[#2563EB] dark:text-[#3B82F6]" />
          <span class="text-[#111827] dark:text-[#F1F5F9]">Pas de stockage permanent</span>
        </li>
        <li class="flex items-center gap-3">
          <Icon icon="lucide:check" class="text-[#2563EB] dark:text-[#3B82F6]" />
          <span class="text-[#111827] dark:text-[#F1F5F9]">Pas de tracking, ni de récupération de donnée</span>
        </li>
        <li class="flex items-center gap-3">
          <Icon icon="lucide:check" class="text-[#2563EB] dark:text-[#3B82F6]" />
          <span class="text-[#111827] dark:text-[#F1F5F9]">Open source et transparent</span>
        </li>
      </ul>
    </div>

    <div class="p-8 bg-white dark:bg-gray-800 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700" in:fly={{ x: 20, duration: 800, delay: 200 }}>
      <div class="flex flex-row items-center gap-3 mb-6">
        <Icon icon="lucide:palette" class="text-[#2563EB] dark:text-[#3B82F6]" width="32" height="32"/>
        <h3 class="text-2xl font-semibold text-[#2563EB] dark:text-[#3B82F6]">Design et accessibilité</h3>
      </div>
      <ul class="space-y-4">
        <li class="flex items-center gap-3">
          <Icon icon="lucide:check" class="text-[#2563EB] dark:text-[#3B82F6]" />
          <span class="text-[#111827] dark:text-[#F1F5F9]">Compatible mobile</span>
        </li>
        <li class="flex items-center gap-3">
          <Icon icon="lucide:check" class="text-[#2563EB] dark:text-[#3B82F6]" />
          <span class="text-[#111827] dark:text-[#F1F5F9]">Contraste forts</span>
        </li>
        <li class="flex items-center gap-3">
          <Icon icon="lucide:check" class="text-[#2563EB] dark:text-[#3B82F6]" />
          <span class="text-[#111827] dark:text-[#F1F5F9]">Design minimaliste</span>
        </li>
      </ul>
    </div>
  </div>
</section>