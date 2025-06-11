const ABLETON_DATA_PATH = '/ableton-data.json';

export async function fetchAbletonData() {
  try {
    const response = await fetch(ABLETON_DATA_PATH);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error("Error fetching Ableton data:", error);
    return null;
  }
}

export function getAudioFilePath(data) {
  if (!data || !data.session || !data.session.audio_file) {
    return '';
  }
  return `/audio/${data.session.audio_file}`;
}

export function getTransientsForClip(data, clipName) {
  if (!data || !data.clips) {
    return [];
  }
  const clip = data.clips.find(c => c.name === clipName);
  return clip ? clip.transients : [];
}