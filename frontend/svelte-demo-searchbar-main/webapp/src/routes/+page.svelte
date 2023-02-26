<script>
  import Logo from "/src/components/Logo.svelte";
  import SearchBar from "/src/components/SearchBar.svelte";
  import SearchResults from "/src/components/SearchResults.svelte";
</script>

<div class="flex flex-col justify-center items-center h-screen w-screen gap-y-4">
  <Logo text="Slang Translator"/>
  <SearchBar />
  <SearchResults />

</div>