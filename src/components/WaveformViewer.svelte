<script>
import { onMount, onDestroy } from 'svelte';
import { beatsToSeconds } from '../lib/time';
export let audioSrc = '';
export let transients = [];
export let tempo = 120;

let peaksInstance = null;

onMount(() => {
  // @ts-ignore
  if (typeof window.Peaks === 'undefined') {
    console.error('Peaks.js not loaded');
    return;
  }

  const options = {
    containers: {
      zoomview: document.getElementById('waveform-container')
    },
    mediaElement: document.getElementById('audio-player'),
    pointMarkerColor: '#ff0000',
    pointLabelText: (point) => point.label
  };

  // @ts-ignore
  window.Peaks.init(options, (err, peaks) => {
    if (err) {
      console.error('Peaks.js error:', err);
      return;
    }
    peaksInstance = peaks;

    // Add transient markers as points
    transients.forEach((t) => {
      const time = beatsToSeconds(t.beat_time, tempo);
      peaks.points.add({
        time,
        label: `${t.clip_name} (Beat ${t.beat_time})`,
        color: '#ff0000'
      });
    });
  });

  return () => {
    if (peaksInstance) {
      peaksInstance.destroy();
    }
  };
});

onDestroy(() => {
  if (peaksInstance) {
    peaksInstance.destroy();
  }
});
</script>

<div class="section">
  <h2>Waveform</h2>
  <div id="waveform-container"></div>
  <audio id="audio-player" controls>
    <source src={audioSrc} type="audio/wav" />
    Your browser does not support the audio element.
  </audio>
</div>