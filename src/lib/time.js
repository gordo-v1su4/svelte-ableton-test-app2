export function beatsToSeconds(beatTime, tempo) {
  if (!tempo) return 0;
  return beatTime * (60 / tempo); // Convert beats to seconds
}