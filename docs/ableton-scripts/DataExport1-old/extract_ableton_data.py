import Live
import json
from os.path import join

def extract_ableton_data(song):
    data = {
        "bpm": song.tempo,
        "key": "unknown",
        "trigger_markers": [],
        "midi_patterns": [],
        "transient_markers": [],
        "audio_files": []
    }
    for cue in song.cue_points:
        data["trigger_markers"].append({"name": cue.name or "Unnamed", "time": cue.time})
    for track in song.tracks:
        for clip in track.clips:
            if clip.is_midi_clip:
                notes = [{"pitch": n[0], "start_time": n[1], "duration": n[2], "velocity": n[3]} for n in clip.get_notes(0, 0, clip.length, 128) if clip.has_notes]
                data["midi_patterns"].append({"track": track.name, "clip": clip.name or "Unnamed", "notes": notes})
            if clip.is_audio_clip and clip.warp_markers:
                transients = [{"time": m.time} for m in clip.warp_markers]
                data["transient_markers"].append({"track": track.name, "clip": clip.name or "Unnamed", "transients": transients})
            if clip.is_audio_clip:
                data["audio_files"].append({"track": track.name, "clip": clip.name or "Unnamed", "file_path": clip.file_path})
    output_path = join("C:/Users/Gordo/Documents/Github/ableton-scripts/exports", "ableton_data_export.json")  # Update username
    with open(output_path, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Data exported to {output_path}")

def create_instance(c_instance):
    return DataExportScript(c_instance)

class DataExportScript:
    def __init__(self, c_instance):
        self.c_instance = c_instance
        extract_ableton_data(c_instance.song())