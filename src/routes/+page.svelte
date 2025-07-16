<script lang="ts">
  import Hero from "$lib/components/Hero.svelte";
  import HowItWorks from "$lib/components/HowItWorks.svelte";
  import Footer from "$lib/components/Footer.svelte";

  import { compressVideoStream, downloadVideo } from "$lib/client/Video";
  import Icon from "@iconify/svelte";
  import { fade, fly } from "svelte/transition";

  let file = $state<File | null>(null);
  let size = $state(8); // taille cible en Mo
  let speed = $state(1.0);
  let responseMessage = $state('');
  
  let isDownloadable = $state(false);
  let downloadToken = $state('');

  let progress = $state(0);
  let eta = $state('');
  let isCompressing = $state(false);

  async function handleSubmitStream() {
    isDownloadable = false;
    isCompressing = true;
    responseMessage = '';
    progress = 0;
    eta = '';

    if (!file) {
      responseMessage = "Veuillez choisir une vidéo.";
      return;
    }

    const stream_response:any = await compressVideoStream(file, size, speed);

    let reader: ReadableStreamDefaultReader<Uint8Array> | null = null;
    try {
      reader = stream_response?.getReader();
    } catch (error) {
      responseMessage = "Le serveur de compression est en cours de maintenance.";
      isCompressing = false;
      isDownloadable = false;
      progress = 0;
      eta = '';
      return;
    }

    const decoder = new TextDecoder('utf-8');

    if (!reader) return;

    let buffer = '';
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

        console.log(type, data);

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
          downloadToken = data;
        } else if (type === 'error') {
          isCompressing = false;
          eta = 'Erreur : ' + data;
        }
      }
    }
  }

  async function handleDownloadVideo() {
    if (!downloadToken) {
      responseMessage = "Le fichier n'a pas pu être récupéré.";
      return;
    }

    const blob = await downloadVideo(downloadToken);
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'compressed.mp4';
    a.click();

    // reset state
    isDownloadable = false;
    isCompressing = false;
    file = null;
    progress = 0;
    eta = '';
    downloadToken = '';
    responseMessage = '';
  }
</script>

<Hero />
<!-- Main Section -->
<section class="py-20 px-4 bg-[#F9FAFB] dark:bg-[#0F172A]">
  <div class="max-w-4xl mx-auto">
    <div class="flex flex-col gap-12">
      <div class="space-y-8">

          <div class="p-8 bg-white dark:bg-gray-800 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700" in:fly={{ x: -20, duration: 800 }}>
            <div class="flex gap-4">
              <Icon icon="lucide:video" class="text-3xl text-[#2563EB] dark:text-[#3B82F6]" />
              <h2 class="text-2xl font-semibold mb-6 text-[#2563EB] dark:text-[#3B82F6]">Import</h2>
            </div>
            
            <div 
              class="relative border-2 border-dashed border-[#2563EB]/30 dark:border-[#3B82F6]/30 rounded-xl transition-colors
                    hover:border-[#2563EB]/50 dark:hover:border-[#3B82F6]/50 hover:bg-[#2563EB]/5 dark:hover:bg-[#3B82F6]/5 cursor-pointer"
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
                <label for="videoInput" class="block w-full text-center cursor-pointer p-8">
                  <div class="flex items-center justify-center gap-3 mb-3">
                    <Icon icon="lucide:check-circle" class="text-3xl text-[#2563EB] dark:text-[#3B82F6]" />
                    <span class="text-lg font-medium text-[#2563EB] dark:text-[#3B82F6]">Vidéo sélectionnée</span>
                  </div>
                  <p class="text-[#111827] dark:text-[#F1F5F9]">{file.name}</p>
                  <p class="mt-2 text-sm text-[#2563EB] dark:text-[#3B82F6]">Cliquez ou glissez une autre vidéo pour changer</p>
                </label>
              {:else}
                <label for="videoInput" class="block w-full text-center cursor-pointer p-8">
                  <div class="flex items-center justify-center gap-3 mb-3">
                    <Icon icon="lucide:upload-cloud" class="text-4xl text-[#2563EB] dark:text-[#3B82F6]" />
                    <span class="text-lg font-medium text-[#2563EB] dark:text-[#3B82F6]">Déposez votre vidéo ici</span>
                  </div>
                  <p class="text-[#111827] dark:text-[#F1F5F9]">ou cliquez pour sélectionner un fichier</p>
                </label>
              {/if}
            </div>

            <div class="flex gap-4 mt-8">
              <Icon icon="lucide:zap" class="text-3xl text-[#2563EB] dark:text-[#3B82F6]" />
              <h2 class="text-2xl font-semibold mb-6 text-[#2563EB] dark:text-[#3B82F6]">Compression</h2>
            </div>

              <div class="space-y-4 mb-4">
                <label class="block">
                  <span class="text-[#111827] dark:text-[#F1F5F9] mb-2 block">Taille cible (MB)</span>
                  <input type="number" bind:value={size} min="1" class="w-full px-4 py-2 rounded-xl border border-gray-200 dark:border-gray-700 focus:border-[#2563EB] dark:focus:border-[#3B82F6] focus:ring-1 focus:ring-[#2563EB] dark:focus:ring-[#3B82F6] bg-white dark:bg-gray-800 text-[#111827] dark:text-[#F1F5F9]" />
                </label>
                <label class="block">
                  <span class="text-[#111827] dark:text-[#F1F5F9] mb-2 block">Vitesse de lecture</span>
                  <input type="number" step="0.1" bind:value={speed} min="0.1" class="w-full px-4 py-2 rounded-xl border border-gray-200 dark:border-gray-700 focus:border-[#2563EB] dark:focus:border-[#3B82F6] focus:ring-1 focus:ring-[#2563EB] dark:focus:ring-[#3B82F6] bg-white dark:bg-gray-800 text-[#111827] dark:text-[#F1F5F9]" />
                </label>
              </div>

              <button 
                onclick={handleSubmitStream} 
                class="w-full px-6 py-3 bg-[#2563EB] dark:bg-[#3B82F6] text-white rounded-xl hover:bg-[#2563EB]/80 dark:hover:bg-[#3B82F6]/80 transition cursor-pointer" 
                aria-label="Compresser la vidéo" 
                transition:fade
              >
                Compresser la vidéo
              </button>

            {#if isCompressing || isDownloadable}

              <div class="flex gap-4 mt-8">
                <Icon icon="lucide:download" class="text-3xl text-[#2563EB] dark:text-[#3B82F6]" />
                <h2 class="text-2xl font-semibold mb-6 text-[#2563EB] dark:text-[#3B82F6]">Export</h2>
              </div>

              {#if isCompressing}
                <div class="flex flex-col gap-4 w-full p-4 rounded-2xl" transition:fade>
                  <div class="flex items-center gap-4">
                    <Icon icon="lucide:loader-2" class="text-[#2563EB] dark:text-[#3B82F6] animate-spin" />
                    <p class="text-[#2563EB] dark:text-[#3B82F6] font-medium">Compression en cours...</p>
                  </div>
                  <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2.5">
                    <div class="bg-[#2563EB] dark:bg-[#3B82F6] h-2.5 rounded-full transition-all duration-300" style="width: {progress}%"></div>
                  </div>
                  
                  {#if eta !== ''}
                    <p class="text-[#2563EB] dark:text-[#3B82F6] font-medium text-sm text-right">Prêt dans {eta} secondes</p>
                  {:else}
                    <p class="text-[#2563EB] dark:text-[#3B82F6] font-medium text-sm text-right">Upload en cours...</p>
                  {/if}
                </div>
              {/if}

              {#if isDownloadable}
                <button
                  onclick={handleDownloadVideo}
                  class="mt-4 inline-block w-full px-6 py-3 bg-[#2563EB] dark:bg-[#3B82F6] text-white rounded-xl hover:bg-[#2563EB]/80 dark:hover:bg-[#3B82F6]/80 transition text-center cursor-pointer"
                  transition:fade
                >
                  <Icon icon="lucide:download" class="inline mr-2" /> Télécharger
                </button>
              {/if}
            {/if}
            </div>
        </div>

        {#if responseMessage}
          <div class="p-4 bg-white dark:bg-gray-800 rounded-2xl border border-[#2563EB]/20 dark:border-[#3B82F6]/20 relative flex gap-4 items-center" in:fly={{ x: 20, duration: 800 }}>
            <Icon icon="lucide:alert-triangle" class="text-[#2563EB] dark:text-[#3B82F6] text-2xl" />
            <p class="text-center text-lg text-[#2563EB] dark:text-[#3B82F6]" transition:fade>{responseMessage}</p>
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