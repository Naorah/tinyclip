<script lang="ts">
  import Hero from "$lib/components/Hero.svelte";
  import HowItWorks from "$lib/components/HowItWorks.svelte";
  import Footer from "$lib/components/Footer.svelte";


  import { compressVideo, compressVideoStream, downloadVideo } from "$lib/client/Video";
	import Icon from "@iconify/svelte";
	import { fade, fly } from "svelte/transition";

	let file = $state<File | null>(null);
	let size = $state(8); // taille cible en Mo
	let speed = $state(1.0);
	let responseMessage = $state('');
	let loading = $state(false);
	let compressionDone = $state(false);
  
  let isDownloadable = $state(false);
	let downloadUrl = $state('');
  /**
   * Compress a video file
   * @returns The compressed video file
   */
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

  let progress = $state(0);
  let eta = $state('');
  let isCompressing = $state(false);

  async function handleSubmitStream() {
    isDownloadable = false;
    if (!file) {
      responseMessage = "Veuillez choisir une vidéo.";
      return;
    }

    const stream_response = await compressVideoStream(file, size, speed);

    const reader = stream_response?.getReader();
    const decoder = new TextDecoder('utf-8');

    if (!reader) return;

    let buffer = '';
    isCompressing = true;
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });

      // Découper en événements individuels
      const events = buffer.split('\n\n');
      buffer = events.pop() || '';

      for (const event of events) {
        const lines = event.split('\n');
        const typeLine = lines.find(line => line.startsWith('event:'));
        const dataLine = lines.find(line => line.startsWith('data:'));

        if (!typeLine || !dataLine) continue;

        const type = typeLine.slice(7).trim();
        const data = dataLine.slice(6).trim();

        if (type === 'progress') {
          try {
            const { percent, eta: etaVal } = JSON.parse(data);
            progress = percent;
            eta = etaVal;
          } catch (e) {
            console.error('Erreur parsing progress:', e);
          }
        } else if (type === 'done') {
          // Le backend renvoie le nom du fichier ou autre info
          isCompressing = false;
          progress = 100;
          eta = 'Terminé !';
          isDownloadable = true;
          downloadUrl = data;
        } else if (type === 'error') {
          isCompressing = false;
          eta = 'Erreur : ' + data;
        }
      }
    }
  }

  async function handleDownloadVideo() {
    const blob = await downloadVideo(downloadUrl);
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'compressed.mp4';
    a.click();
  }
</script>

<Hero />

<!-- Main Section -->
<section class="py-20 px-4">
  <div class="max-w-4xl mx-auto">
    <div class="flex flex-col gap-12">
      <div class="space-y-8">

          <div class="p-8 bg-white rounded-2xl shadow-sm border border-gray-100" in:fly={{ x: -20, duration: 800 }}>
            <div class="flex gap-4">
              <Icon icon="lucide:video" class="text-3xl text-pink-400" />
              <h2 class="text-2xl font-semibold mb-6 text-pink-400">Import</h2>
            </div>
            
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


            <div class="flex gap-4 mt-8">
              <Icon icon="lucide:zap" class="text-3xl text-violet-400" />
              <h2 class="text-2xl font-semibold mb-6 text-violet-400">Compression</h2>
            </div>

              <div class="space-y-4 mb-4">
                <label class="block">
                  <span class="text-gray-600 mb-2 block">Taille cible (MB)</span>
                  <input type="number" bind:value={size} min="1" class="w-full px-4 py-2 rounded-xl border border-gray-200 focus:border-violet-400 focus:ring-1 focus:ring-violet-400" />
                </label>
                <label class="block">
                  <span class="text-gray-600 mb-2 block">Vitesse de lecture</span>
                  <input type="number" step="0.1" bind:value={speed} min="0.1" class="w-full px-4 py-2 rounded-xl border border-gray-200 focus:border-violet-400 focus:ring-1 focus:ring-violet-400" />
                </label>
              </div>

            <!-- handleSubmit -->

              <button 
                onclick={handleSubmitStream} 
                class="w-full px-6 py-3 bg-violet-400 text-white rounded-xl hover:bg-violet-500 transition cursor-pointer" 
                aria-label="Compresser la vidéo" 
                transition:fade
              >
                Compresser la vidéo
              </button>

            {#if isCompressing || isDownloadable}

              <div class="flex gap-4 mt-8">
                <Icon icon="lucide:download" class="text-3xl text-blue-400" />
                <h2 class="text-2xl font-semibold mb-6 text-blue-400">Export</h2>
              </div>

              {#if isCompressing}
                <div class="flex flex-col gap-4 w-full p-4 rounded-2xl" transition:fade>
                  <div class="flex items-center gap-4">
                    <Icon icon="lucide:loader-2" class="text-blue-400 animate-spin" />
                    <p class="text-blue-400 font-medium">Compression en cours...</p>
                  </div>
                  <div class="w-full bg-gray-200 rounded-full h-2.5">
                    <div class="bg-blue-400 h-2.5 rounded-full transition-all duration-300" style="width: {progress}%"></div>
                  </div>
                  <p class="text-blue-400 font-medium text-sm text-right">Prêt dans {eta} secondes</p>
                </div>
              {/if}

              {#if isDownloadable}
                <button
                  onclick={handleDownloadVideo}
                  class="mt-4 inline-block w-full px-6 py-3 bg-violet-400 text-white rounded-xl hover:bg-violet-500 transition text-center"
                  transition:fade
                >
                  <Icon icon="lucide:download" class="inline mr-2" /> Télécharger
                </button>
              {/if}
            {/if}
            </div>
        </div>

        {#if responseMessage}
          <div class="p-4 bg-white rounded-2xl border border-blue-100 relative flex gap-4 items-center" in:fly={{ x: 20, duration: 800 }}>
            <Icon icon="lucide:alert-triangle" class="text-blue-400 text-2xl" />
            <p class="text-center text-lg text-blue-400" transition:fade>{responseMessage}</p>
          </div>
        {/if}
      </div>
    </div>
  </section>

<HowItWorks />

<Footer />

<style>
	input[type="file"] {
		display: none !important;
	}
</style>