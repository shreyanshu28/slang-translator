<script>
    import { onMount, onDestroy } from 'svelte';
    
    export let text = "NoLogo";

    let element;

    let color = '#FFFFFF';
    let colors = [
        "#3B3561",
        "#F5B700",
        "#DC0073",
        "#008BF8"
    ];

    function setRandomColor(){
        let oldColor = `${color}`;
        while (color === oldColor) {
            console.log('new color');
            color = colors[Math.floor(Math.random() * colors.length)];
        }
    }

    onMount(() => {
        setRandomColor();
    });

</script>

<h1 class="text-6xl font-extrabold select-none text-white text-[{color}] transition-colors duration-1000 cursor-pointer" bind:this={element} on:click={()=> 
setRandomColor()}>{text}</h1>