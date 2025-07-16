<script lang="ts">
  import Icon from "@iconify/svelte";
</script>

<!-- Footer -->
<footer class="py-8 px-4 border-t border-gray-100 dark:border-gray-800 bg-[#F9FAFB] dark:bg-[#0F172A]">
  <div class="max-w-4xl mx-auto flex flex-col md:flex-row justify-between items-center gap-4">
    <div class="flex items-center gap-3">
      <img src="/favicon.svg" alt="TinyClip" class="w-8 h-8" />
      <span class="font-medium text-[#2563EB] dark:text-[#3B82F6]">TinyClip</span>
    </div>
    <div class="flex items-center gap-6">
      <a href="https://github.com/Naorah/tinyclip" target="_blank" class="text-[#111827] dark:text-[#F1F5F9] hover:text-[#2563EB] dark:hover:text-[#3B82F6] transition">
        <Icon icon="lucide:github" class="w-6 h-6" />
      </a>
    </div>
  </div>
</footer>