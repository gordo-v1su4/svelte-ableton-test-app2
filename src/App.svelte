<script>
  import { onMount } from 'svelte';
  import SessionInfo from './components/SessionInfo.svelte';
  import TransientList from './components/TransientList.svelte';
  import WaveformViewer from './components/WaveformViewer.svelte';
  import { fetchAbletonData, getAudioFilePath, getTransientsForClip } from './lib/data';

  let data = null;
  let audioSrc = '';
  let transients = [];

  onMount(async () => {
      const fetchedData = await fetchAbletonData();
      if (fetchedData) {
        data = fetchedData;
        audioSrc = getAudioFilePath(data);
        // Assume first audio clip for transients (modify as needed)
        const audioClip = data.clips.find(clip => clip.is_audio);
        if (audioClip) {
          transients = getTransientsForClip(data, audioClip.name);
        }
      }
    });
</script>

<div class="container">
  <h1>Ableton Data Visualizer</h1>
  {#if data}
    <SessionInfo session={data.session} />
    <TransientList transients={transients} tempo={data.session.tempo} />
    <WaveformViewer {audioSrc} {transients} tempo={data.session.tempo} />
  {:else}
    <p>Loading data...</p>
  {/if}
</div>