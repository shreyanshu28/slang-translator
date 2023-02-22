<script>
    import axios from 'axios';
    import { searchResultsStore } from "/src/stores/searchResultsStore.js";

    let searchText = '';
    let timeout;

    function keyPressed(){
        if (timeout) clearTimeout(timeout);
        timeout = setTimeout(() => {
            fetchSearchResults();
        }, 300);
    }

    async function fetchSearchResults(){
        try {
            let { data, status } = await axios.post('http://localhost:2999/search', {
                text: searchText
            });

            if (status != 200){
                alert('Error fetching search results!');
                return;
            }
        searchResultsStore.set(data.results);
        } catch (error){
            alert('Error fetching search results! Probably the API is not ready yet.');
            return;
        }
    }
</script>
<div class="w-1/5">
    <div class="input-group relative flex w-full">
    <input bind:value={searchText} on:keydown={()=> keyPressed()} type="text" class="form-control relative flex-auto block w-full px-3 py-3 text-base font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-gray-400 focus:outline-none" placeholder="query">
    <button on:click={()=> fetchSearchResults()} class="absolute top-2 right-2 btn flex p-2 text-gray-700 font-medium text-xs leading-tight uppercase rounded focus:outline-none focus:ring-0 transition duration-150 ease-in-out items-center" type="button">
        <svg aria-hidden="true" focusable="false" data-prefix="fas" data-icon="search" class="w-4" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
        <path fill="currentColor" d="M505 442.7L405.3 343c-4.5-4.5-10.6-7-17-7H372c27.6-35.3 44-79.7 44-128C416 93.1 322.9 0 208 0S0 93.1 0 208s93.1 208 208 208c48.3 0 92.7-16.4 128-44v16.3c0 6.4 2.5 12.5 7 17l99.7 99.7c9.4 9.4 24.6 9.4 33.9 0l28.3-28.3c9.4-9.4 9.4-24.6.1-34zM208 336c-70.7 0-128-57.2-128-128 0-70.7 57.2-128 128-128 70.7 0 128 57.2 128 128 0 70.7-57.2 128-128 128z"></path>
        </svg>
    </button>
    </div>
</div>