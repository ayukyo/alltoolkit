"""
MIDI Utilities - Zero-dependency MIDI file processing

Usage:
    from midi_utils import read_midi, write_midi, extract_notes, create_simple_melody
    
    # Read MIDI file
    midi = read_midi("song.mid")
    
    # Extract notes
    notes = extract_notes("song.mid")
    
    # Create melody
    melody = [("C4", 1.0), ("D4", 1.0), ("E4", 1.0)]
    midi = create_simple_melody(melody, bpm=120)
    write_midi(midi, "output.mid")
"""

from .mod import (
    # Data classes
    MIDIEvent,
    NoteEvent,
    MIDITrack,
    MIDIFile,
    MIDIInfo,
    
    # Exceptions
    MIDIUtilsError,
    InvalidMIDIFileError,
    UnsupportedMIDIFormatError,
    
    # Enums
    MIDIMessageType,
    MetaEventType,
    
    # Read functions
    parse_midi_file,
    read_midi,
    get_midi_info,
    extract_notes,
    
    # Write functions
    write_midi_file,
    write_midi,
    
    # Create functions
    create_midi_event,
    create_note_on_event,
    create_note_off_event,
    create_tempo_event,
    create_track_name_event,
    create_end_of_track_event,
    create_simple_melody,
    create_scale,
    create_chord,
    
    # Helper functions
    midi_note_to_name,
    name_to_midi_note,
    ticks_to_seconds,
    seconds_to_ticks,
    get_instrument_name,
    transpose_notes,
    notes_to_text,
)

__all__ = [
    'MIDIEvent',
    'NoteEvent',
    'MIDITrack',
    'MIDIFile',
    'MIDIInfo',
    'MIDIUtilsError',
    'InvalidMIDIFileError',
    'UnsupportedMIDIFormatError',
    'MIDIMessageType',
    'MetaEventType',
    'parse_midi_file',
    'read_midi',
    'get_midi_info',
    'extract_notes',
    'write_midi_file',
    'write_midi',
    'create_midi_event',
    'create_note_on_event',
    'create_note_off_event',
    'create_tempo_event',
    'create_track_name_event',
    'create_end_of_track_event',
    'create_simple_melody',
    'create_scale',
    'create_chord',
    'midi_note_to_name',
    'name_to_midi_note',
    'ticks_to_seconds',
    'seconds_to_ticks',
    'get_instrument_name',
    'transpose_notes',
    'notes_to_text',
]

__version__ = '1.0.0'
__author__ = 'AllToolkit'