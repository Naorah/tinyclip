<script>
  let { children } = $props();
  import "../app.css";
  import NavBar from "$lib/components/NavBar.svelte";
</script> 

<NavBar />

{@render children()}