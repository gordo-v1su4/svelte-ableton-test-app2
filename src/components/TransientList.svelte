<script>
  export let transients = [];
  export let tempo = 120;
</script>

<div class="section">
  <h2>Transients</h2>
  {#if transients.length > 0}
    <ul>
      {#each transients as t}
        <li>
          <strong>{t.clip_name}</strong> - Beat: {t.beat_time}, Time: {Math.round((t.beat_time * (60 / tempo)) * 1000) / 1000}s
        </li>
      {/each}
    </ul>
  {:else}
    <p>No transients found.</p>
  {/if}
</div>