<script>
  export let session = {};
</script>

<div class="section">
  <h2>Session Info</h2>
  <p><strong>Tempo:</strong> {session.tempo || 'N/A'} BPM</p>
  <p><strong>Time Signature:</strong> {session.time_signature?.numerator || 'N/A'}/{session.time_signature?.denominator || 'N/A'}</p>
  <p><strong>Key Signature:</strong> {session.key_signature || 'N/A'}</p>
</div>