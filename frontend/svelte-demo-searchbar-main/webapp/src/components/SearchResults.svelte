<script>
      import { searchResultsStore } from "/src/stores/searchResultsStore.js";

      function parsePosition(str){
        return Math.min(...str.replaceAll(' ', '').replaceAll('[', '').replaceAll(']', '').split(',').map(function(str) { return parseInt(str); }));
      }

      function computeOpacity(position){
        return Math.floor(position / 2);
      }

</script>
<div class="flex flex-col w-1/5 gap-y-4">
    {#each $searchResultsStore as result}
        {@const position = parsePosition(result.position)}
        {@const opacity = computeOpacity(position)}
        <div class="flex flex-col justify-start items-start w-full px-2 relative">
            <div class="text-gray-700 flex">{result.name}</div>
            <div class="text-gray-500 text-sm">{result.artists.replaceAll('"', '').replaceAll('\'', '').replaceAll('[', '').replaceAll(']', '')}</div>
            <div class="text-gray-500 text-sm absolute top-0 right-2 font-semibold" style="opacity:{opacity}%">#{position}</div>
            <div class="text-red-500 text-sm absolute top-0 right-2 font-semibold" style="opacity:{100-opacity}%">#{position}</div>
        </div>
    {/each}
</div>