<script lang="ts">
  import { compressVideo } from "$lib/client/Video";
	import Icon from "@iconify/svelte";
	import { fade, fly } from "svelte/transition";

	let file = $state<File | null>(null);
	let size = $state(8); // taille cible en Mo
	let speed = $state(1.0);
	let responseMessage = $state('');
	let downloadUrl = $state('');
	let loading = $state(false);
	let compressionDone = $state(false);

	async function handleSubmit() {
		loading = true;
		compressionDone = false;
		responseMessage = '';
		downloadUrl = '';

		if (!file) {
			responseMessage = "Veuillez choisir une vidéo.";
			loading = false;
			return;
		}

		try {
			const compressedVideo = await compressVideo(file, size, speed);
			const url = URL.createObjectURL(compressedVideo);
			downloadUrl = url;
			responseMessage = "Compression terminée ! Vous pouvez télécharger votre vidéo.";
			compressionDone = true;
		} catch (error) {
			responseMessage = "Une erreur est survenue pendant la compression.";
		} finally {
			loading = false;
		}
	}
</script>

<!-- Hero Section -->
<section class="min-h-screen px-4 py-20 bg-gradient-to-br from-pink-400/20 to-violet-400/20 flex items-center justify-center">
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
</section>

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

<!-- Main Section -->
<section class="py-20 px-4">
  <div class="max-w-4xl mx-auto">
    <div class="flex flex-col gap-12">
      <div class="space-y-8">
        <div class="p-8 bg-white rounded-2xl shadow-sm border border-gray-100" in:fly={{ x: -20, duration: 800 }}>
          <h2 class="text-2xl font-semibold mb-6 text-violet-400">Import</h2>
          
          <div 
            class="relative border-2 border-dashed border-violet-400/30 rounded-xl p-8 transition-colors
                   hover:border-violet-400/50 hover:bg-violet-400/5"
						aria-label="Déposez votre vidéo ici"
						role="button"
						tabindex="0"
            ondragover={(e:any) => e.preventDefault()}
            ondrop={(e:any) => {
							e.preventDefault();
              const droppedFile = e.dataTransfer?.files[0];
              if (droppedFile?.type.startsWith('video/')) {
                file = droppedFile;
              }
            }}
          >
            <input type="file" accept="video/*" onchange={(e:any) => file = e.target?.files[0]} class="hidden" id="videoInput" />
            
            {#if file}
              <label for="videoInput" class="block w-full text-center cursor-pointer">
                <div class="flex items-center justify-center gap-3 mb-3">
                  <Icon icon="lucide:check-circle" class="text-3xl text-rose-400" />
                  <span class="text-lg font-medium text-pink-400">Vidéo sélectionnée</span>
                </div>
                <p class="text-gray-600">{file.name}</p>
                <p class="mt-2 text-sm text-pink-400">Cliquez ou glissez une autre vidéo pour changer</p>
              </label>
            {:else}
              <label for="videoInput" class="block w-full text-center cursor-pointer">
                <div class="flex items-center justify-center gap-3 mb-3">
                  <Icon icon="lucide:upload-cloud" class="text-4xl text-pink-400" />
                  <span class="text-lg font-medium text-pink-400">Déposez votre vidéo ici</span>
                </div>
                <p class="text-gray-600">ou cliquez pour sélectionner un fichier</p>
              </label>
            {/if}
          </div>

        </div>

        <div class="p-8 bg-white rounded-2xl shadow-sm border border-gray-100" in:fly={{ x: -20, duration: 800, delay: 200 }}>
          <h2 class="text-2xl font-semibold mb-6 text-violet-400">Configuration</h2>
          <div class="space-y-4">
            <label class="block">
              <span class="text-gray-600 mb-2 block">Taille cible (MB)</span>
              <input type="number" bind:value={size} min="1" class="w-full px-4 py-2 rounded-xl border border-gray-200 focus:border-violet-400 focus:ring-1 focus:ring-violet-400" />
            </label>
            <label class="block">
              <span class="text-gray-600 mb-2 block">Vitesse de lecture</span>
              <input type="number" step="0.1" bind:value={speed} min="0.1" class="w-full px-4 py-2 rounded-xl border border-gray-200 focus:border-violet-400 focus:ring-1 focus:ring-violet-400" />
            </label>
          </div>
        </div>
      </div>

      <div class="space-y-8">
        <div class="p-8 bg-white rounded-2xl shadow-sm border border-gray-100 relative" in:fly={{ x: 20, duration: 800 }}>
          <h2 class="text-2xl font-semibold mb-6 text-violet-400">Export</h2>

          {#if loading}
            <div class="absolute inset-0 bg-white/80 backdrop-blur-sm flex items-center justify-center rounded-2xl" transition:fade>
              <div class="flex flex-col items-center gap-4">
                <Icon icon="lucide:loader-2" class="text-4xl text-violet-400 animate-spin" />
                <p class="text-violet-400 font-medium">Compression en cours...</p>
              </div>
            </div>
          {:else}
            <button 
              onclick={handleSubmit} 
              class="w-full px-6 py-3 bg-emerald-400 text-white rounded-xl hover:bg-emerald-500 transition cursor-pointer" 
              aria-label="Compresser la vidéo" 
              transition:fade
            >
              Compresser la vidéo
            </button>
          {/if}
          
          {#if responseMessage}
            <p class="mt-4 text-gray-600" transition:fade>{responseMessage}</p>
          {/if}
          
          {#if downloadUrl}
            <a 
              href={downloadUrl} 
              download="compressed.mp4" 
              class="mt-4 inline-block w-full px-6 py-3 bg-violet-400 text-white rounded-xl hover:bg-violet-500 transition text-center"
              transition:fade
            >
              <Icon icon="lucide:download" class="inline mr-2" /> Télécharger
            </a>
          {/if}
        </div>
      </div>
    </div>
  </div>
</section>

<!-- Footer -->
<footer class="py-8 px-4 border-t border-gray-100 bg-gray-50">
  <div class="max-w-4xl mx-auto flex flex-col md:flex-row justify-between items-center gap-4">
    <div class="flex items-center gap-3">
      <img src="/favicon.svg" alt="TinyClip" class="w-8 h-8" />
      <span class="font-medium text-violet-400">TinyClip</span>
    </div>
    <div class="flex items-center gap-6">
      <a href="https://github.com/Naorah/tinyclip" target="_blank" class="text-gray-400 hover:text-violet-400 transition">
        <Icon icon="lucide:github" class="w-6 h-6" />
      </a>
    </div>
  </div>
</footer>

<style>
	input[type="file"] {
		display: none !important;
	}
</style>