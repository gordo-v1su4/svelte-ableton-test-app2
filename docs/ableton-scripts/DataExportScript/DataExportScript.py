import Live
import json
import os
from pathlib import Path

def detect_key_from_midi(midi_patterns):
    """Simple key detection based on note frequency analysis"""
    note_counts = {}
    note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    
    # Count note occurrences
    for pattern in midi_patterns:
        for note in pattern["notes"]:
            pitch_class = note["pitch"] % 12
            note_counts[pitch_class] = note_counts.get(pitch_class, 0) + 1
    
    if not note_counts:
        return "unknown"
    
    # Find most common note (simplified key detection)
    most_common_note = max(note_counts, key=note_counts.get)
    return f"{note_names[most_common_note]} Major"  # Simplified - assumes major

def extract_ableton_data(song):
    """Extract comprehensive data from Ableton Live song"""
    try:
        data = {
            "bpm": float(song.tempo),
            "time_signature": {
                "numerator": song.signature_numerator,
                "denominator": song.signature_denominator
            },
            "key": "unknown",
            "trigger_markers": [],
            "midi_patterns": [],
            "transient_markers": [],
            "audio_files": [],
            "track_info": [],
            "song_length": song.song_length
        }
        
        # Extract cue points
        for cue in song.cue_points:
            data["trigger_markers"].append({
                "name": cue.name or "Unnamed",
                "time": float(cue.time)
            })
        
        # Extract track and clip data
        for track_idx, track in enumerate(song.tracks):
            track_info = {
                "index": track_idx,
                "name": track.name,
                "is_foldable": track.is_foldable,
                "muted": track.mute,
                "solo": track.solo,
                "arm": track.arm if hasattr(track, 'arm') else False,
                "volume": float(track.mixer_device.volume.value) if hasattr(track, 'mixer_device') else 1.0,
                "panning": float(track.mixer_device.panning.value) if hasattr(track, 'mixer_device') else 0.0,
                "clips": []
            }
            
            # Live 12 API: use clip_slots instead of clips
            for clip_idx, clip_slot in enumerate(track.clip_slots):
                if clip_slot.clip is None:
                    continue
                
                clip = clip_slot.clip
                clip_data = {
                    "index": clip_idx,
                    "name": clip.name or "Unnamed",
                    "start_time": float(clip.start_time),
                    "end_time": float(clip.end_time),
                    "loop_start": float(clip.loop_start),
                    "loop_end": float(clip.loop_end),
                    "looping": clip.looping,
                    "muted": clip.muted,
                    "color": clip.color if hasattr(clip, 'color') else None,
                    "is_midi": clip.is_midi_clip,
                    "is_audio": clip.is_audio_clip
                }
                
                # Extract MIDI data
                if clip.is_midi_clip and clip.has_notes:
                    try:
                        notes = []
                        for note in clip.get_notes(0, 0, clip.length, 128):
                            notes.append({
                                "pitch": int(note[0]),
                                "start_time": float(note[1]),
                                "duration": float(note[2]),
                                "velocity": int(note[3])
                            })
                        
                        if notes:  # Only add if we have notes
                            data["midi_patterns"].append({
                                "track": track.name,
                                "track_index": track_idx,
                                "clip": clip.name or "Unnamed",
                                "clip_index": clip_idx,
                                "notes": notes
                            })
                            clip_data["note_count"] = len(notes)
                    except Exception as e:
                        print(f"Error extracting MIDI from {track.name}: {str(e)}")
                
                # Extract audio warp markers
                if clip.is_audio_clip:
                    try:
                        if hasattr(clip, 'file_path') and clip.file_path:
                            data["audio_files"].append({
                                "track": track.name,
                                "track_index": track_idx,
                                "clip": clip.name or "Unnamed",
                                "clip_index": clip_idx,
                                "file_path": str(clip.file_path)
                            })
                        
                        if hasattr(clip, 'warp_markers') and clip.warp_markers:
                            transients = []
                            for marker in clip.warp_markers:
                                transients.append({
                                    "time": float(marker.beat_time),
                                    "sample_time": float(marker.sample_time) if hasattr(marker, 'sample_time') else None
                                })
                            
                            if transients:
                                data["transient_markers"].append({
                                    "track": track.name,
                                    "track_index": track_idx,
                                    "clip": clip.name or "Unnamed",
                                    "clip_index": clip_idx,
                                    "transients": transients
                                })
                                clip_data["warp_marker_count"] = len(transients)
                    except Exception as e:
                        print(f"Error extracting audio data from {track.name}: {str(e)}")
                
                track_info["clips"].append(clip_data)
            
            data["track_info"].append(track_info)
        
        # Detect key from MIDI data
        data["key"] = detect_key_from_midi(data["midi_patterns"])
        
        # Create output directory
        output_dir = Path.home() / "Documents" / "Github" / "ableton-scripts" / "exports"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate filename with timestamp
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = output_dir / f"ableton_data_export_{timestamp}.json"
        
        # Export data
        with open(output_path, "w", encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        
        print(f"✓ Data exported successfully to {output_path}")
        print(f"  - BPM: {data['bpm']}")
        print(f"  - Key: {data['key']}")
        print(f"  - Tracks: {len(data['track_info'])}")
        print(f"  - MIDI Patterns: {len(data['midi_patterns'])}")
        print(f"  - Audio Files: {len(data['audio_files'])}")
        print(f"  - Cue Points: {len(data['trigger_markers'])}")
        
        return True
        
    except Exception as e:
        print(f"✗ Export failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def create_instance(c_instance):
    """Entry point for Ableton Live"""
    return DataExportScript(c_instance)

class DataExportScript:
    """Main script class for Ableton Live integration"""
    
    def __init__(self, c_instance):
        self.c_instance = c_instance
        self.song = c_instance.song()
        
        print("=== Ableton Data Export Script Loaded ===")
        
        # Automatically extract data when script loads
        success = extract_ableton_data(self.song)
        
        if success:
            print("=== Export Complete ===")
        else:
            print("=== Export Failed - Check console for errors ===")
    
    def update_display(self):
        """Required method for Ableton Control Surface - called periodically"""
        pass
    
    def refresh_state(self):
        """Required method for Ableton Control Surface"""
        pass
    
    def build_midi_map(self, midi_map_handle):
        """Required method for Ableton Control Surface"""
        pass
    
    def receive_midi(self, midi_bytes):
        """Required method for Ableton Control Surface"""
        pass
    
    def can_lock_to_device(self, device):
        """Required method for Ableton Control Surface"""
        return False
    
    def can_lock_to_devices(self, devices):
        """Required method for Ableton Control Surface (plural version)"""
        return False
    
    def connect_script_instances(self, instanciated_scripts):
        """Required method for Ableton Control Surface"""
        pass
    
    def suggest_input_port(self):
        """Required method for Ableton Control Surface"""
        return ""
    
    def suggest_output_port(self):
        """Required method for Ableton Control Surface"""
        return ""
        
    def disconnect(self):
        """Called when script is unloaded"""
        print("Data Export Script disconnected")
        pass