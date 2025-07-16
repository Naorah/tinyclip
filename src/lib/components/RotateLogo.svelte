<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import * as THREE from 'three';
  import { SVGLoader } from 'three/examples/jsm/loaders/SVGLoader.js';
  import themeMode from "$lib/rune/ThemeMode.svelte";

  let { src } = $props();

  let container: HTMLDivElement;
  let renderer: THREE.WebGLRenderer;
  let camera: THREE.PerspectiveCamera;
  let scene: THREE.Scene;
  let animationId: number;
  let svgGroup: THREE.Group;
  let pivot: THREE.Group;
  let bounceOffset = 0;
  const bounceSpeed = 0.005;
  const bounceAmplitude = 5;
  const front_color = "#AF3300";
  let back_color = $state();

  $effect(() => {
    if (themeMode.isDark) {
      updateBackground("#111827");
    }
  });
  
  $effect(() => {
    if (!themeMode.isDark) {
      updateBackground("#F8FAFC");
    }
  });
  
  function updateBackground(color:string) {
    if (scene) {
      scene.background = new THREE.Color(color);
    }
  }

  // Gestion du redimensionnement
  function handleResize() {
    if (container && renderer && camera) {
      const width = container.clientWidth;
      const height = container.clientHeight;

      camera.aspect = width / height;
      camera.updateProjectionMatrix();
      renderer.setSize(width, height);
    }
  }

  onMount(() => {
    const saved = localStorage.getItem('theme');
    if (saved === 'light') {
      back_color = "#F8FAFC";
    } else {
      back_color = "#111827";
    }
    // Base
    scene = new THREE.Scene();
    scene.background = new THREE.Color(back_color);
    camera = new THREE.PerspectiveCamera(70, container.clientWidth / container.clientHeight, 0.1, 1000);
    camera.position.z = 300;

    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(container.clientWidth, container.clientHeight);
    container.appendChild(renderer.domElement);

    // Ajout de l'écouteur de redimensionnement
    window.addEventListener('resize', handleResize);

    // Lumière
    const light = new THREE.DirectionalLight(0xffffff, 1);
    light.position.set(0, 0, 300);
    scene.add(light);

    // Groupe pour contenir tout le SVG
    svgGroup = new THREE.Group();
    scene.add(svgGroup);

    // Point pivot pour la rotation
    pivot = new THREE.Group();
    scene.add(pivot);
    pivot.position.y = 38.5;
    // Charger SVG
    const loader = new SVGLoader();
    loader.load(src, (data: any) => {
      const material = new THREE.MeshPhongMaterial({ 
        color: front_color,
        side: THREE.DoubleSide,
        emissive: 0xff3300,
        emissiveIntensity: 0.2
      });

      data.paths.forEach((path: any) => {
        const shapes = SVGLoader.createShapes(path);
        shapes.forEach((shape: any) => {
          const geometry = new THREE.ExtrudeGeometry(shape, {
            depth: 10,
            bevelEnabled: true,
            bevelThickness: 2,
            bevelSize: 1,
            bevelSegments: 3
          });
          const mesh = new THREE.Mesh(geometry, material);
          svgGroup.add(mesh);
        });
      });

      // Centre le groupe entier
      const box = new THREE.Box3().setFromObject(svgGroup);
      const center = box.getCenter(new THREE.Vector3());
      
      // Déplace le groupe pour que son centre soit à l'origine
      svgGroup.position.sub(center);
      
      // Ajuste l'échelle
      const size = box.getSize(new THREE.Vector3());
      const maxDim = Math.max(size.x, size.y);
      const scale = 100 / maxDim;
      svgGroup.scale.multiplyScalar(scale);

      // Ajoute le groupe au pivot après l'avoir centré
      pivot.add(svgGroup);

      // Ajustement initial de la taille
      handleResize();
    });

    // Animation
    function animate() {
      animationId = requestAnimationFrame(animate);
      
      if (pivot) {
        pivot.rotation.y += 0.003;
        
        // Effet de rebond
        bounceOffset += bounceSpeed;
        const bounceY = Math.sin(bounceOffset) * bounceAmplitude;
        svgGroup.position.y = bounceY;
      }

      renderer.render(scene, camera);
    }

    animate();

    // Nettoyage
    onDestroy(() => {
      cancelAnimationFrame(animationId);
      window.removeEventListener('resize', handleResize);
      renderer.dispose();
      container.removeChild(renderer.domElement);
    });
  });
</script>

<div class="w-full h-full" bind:this={container}></div>