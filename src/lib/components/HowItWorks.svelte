<script lang="ts">
  import Icon from "@iconify/svelte";
  import { fly } from "svelte/transition";
</script>

<!-- Comment ça marche -->
<section class="py-20 px-4 bg-gray-50">
  <div class="max-w-4xl mx-auto text-center mb-16">
    <h2 class="text-3xl font-bold text-violet-400 mb-6" in:fly={{ y: -20, duration: 800 }}>
      Comment ça fonctionne ?
    </h2>
    <p class="text-xl text-gray-600" in:fly={{ y: 20, duration: 800 }}>
      Une solution simple, sécurisée et respectueuse de votre vie privée
    </p>
  </div>

  <div class="max-w-4xl mx-auto grid md:grid-cols-2 gap-12">
    <div class="p-8 bg-white rounded-2xl shadow-sm border border-gray-100" in:fly={{ x: -20, duration: 800 }}>
      <h3 class="text-2xl font-semibold mb-6 text-violet-400">Sécurité maximale</h3>
      <ul class="space-y-4">
        <li class="flex items-center gap-3">
          <Icon icon="lucide:check" class="text-emerald-400" />
          <span class="text-gray-600">Aucun upload de fichier sur nos serveurs</span>
        </li>
        <li class="flex items-center gap-3">
          <Icon icon="lucide:check" class="text-emerald-400" />
          <span class="text-gray-600">Compression 100% locale dans votre navigateur</span>
        </li>
        <li class="flex items-center gap-3">
          <Icon icon="lucide:check" class="text-emerald-400" />
          <span class="text-gray-600">Aucune donnée personnelle collectée</span>
        </li>
      </ul>
    </div>

    <div class="p-8 bg-white rounded-2xl shadow-sm border border-gray-100" in:fly={{ x: 20, duration: 800 }}>
      <h3 class="text-2xl font-semibold mb-6 text-violet-400">Simple et efficace</h3>
      <ul class="space-y-4">
        <li class="flex items-center gap-3">
          <Icon icon="lucide:check" class="text-emerald-400" />
          <span class="text-gray-600">Interface intuitive et rapide</span>
        </li>
        <li class="flex items-center gap-3">
          <Icon icon="lucide:check" class="text-emerald-400" />
          <span class="text-gray-600">Paramètres de compression personnalisables</span>
        </li>
        <li class="flex items-center gap-3">
          <Icon icon="lucide:check" class="text-emerald-400" />
          <span class="text-gray-600">Résultats rapide et maitrisés</span>
        </li>
      </ul>
    </div>

		<div class="p-8 bg-white rounded-2xl shadow-sm border border-gray-100" in:fly={{ x: 20, duration: 800, delay: 200 }}>
			<h2 class="text-2xl font-semibold mb-6 text-violet-400">Avantages</h2>
			<ul class="space-y-4">
				<li class="flex items-center gap-3">
					<Icon icon="lucide:check" class="text-emerald-400" />
					<span class="text-gray-600">100% gratuit et sans inscription</span>
				</li>
				<li class="flex items-center gap-3">
					<Icon icon="lucide:check" class="text-emerald-400" />
					<span class="text-gray-600">Traitement local et sécurisé</span>
				</li>
				<li class="flex items-center gap-3">
					<Icon icon="lucide:check" class="text-emerald-400" />
					<span class="text-gray-600">Compatible format MP4</span>
				</li>
			</ul>
		</div>

		<div class="p-8 bg-white rounded-2xl shadow-sm border border-gray-100" in:fly={{ x: 20, duration: 800, delay: 200 }}>
			<h2 class="text-2xl font-semibold mb-6 text-violet-400">Usage</h2>
			<ul class="space-y-4">
				<li class="flex items-center gap-3">
					<Icon icon="lucide:check" class="text-emerald-400" />
					<span class="text-gray-600">Compresser des vidéos pour les partager</span>
				</li>
				<li class="flex items-center gap-3">
					<Icon icon="lucide:check" class="text-emerald-400" />
					<span class="text-gray-600">Stockage optimisé pour plus de rapidité</span>
				</li>
				<li class="flex items-center gap-3">
					<Icon icon="lucide:check" class="text-emerald-400" />
					<span class="text-gray-600">Compatible avec tous les navigateurs</span>
				</li>
			</ul>
		</div>
  </div>
</section>