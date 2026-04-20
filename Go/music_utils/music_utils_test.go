package music_utils

import (
	"math"
	"testing"
)

// TestNoteNameString tests note name string conversion
func TestNoteNameString(t *testing.T) {
	tests := []struct {
		name     NoteName
		expected string
	}{
		{C, "C"},
		{CSharp, "C#"},
		{D, "D"},
		{DSharp, "D#"},
		{E, "E"},
		{F, "F"},
		{FSharp, "F#"},
		{G, "G"},
		{GSharp, "G#"},
		{A, "A"},
		{ASharp, "A#"},
		{B, "B"},
	}

	for _, tt := range tests {
		t.Run(tt.expected, func(t *testing.T) {
			if got := tt.name.String(); got != tt.expected {
				t.Errorf("NoteName.String() = %v, want %v", got, tt.expected)
			}
		})
	}
}

// TestNoteNameStringFlat tests note name flat notation
func TestNoteNameStringFlat(t *testing.T) {
	tests := []struct {
		name     NoteName
		expected string
	}{
		{C, "C"},
		{CSharp, "Db"},
		{D, "D"},
		{DSharp, "Eb"},
		{E, "E"},
		{F, "F"},
		{FSharp, "Gb"},
		{G, "G"},
		{GSharp, "Ab"},
		{A, "A"},
		{ASharp, "Bb"},
		{B, "B"},
	}

	for _, tt := range tests {
		t.Run(tt.expected, func(t *testing.T) {
			if got := tt.name.StringFlat(); got != tt.expected {
				t.Errorf("NoteName.StringFlat() = %v, want %v", got, tt.expected)
			}
		})
	}
}

// TestNoteString tests note string conversion
func TestNoteString(t *testing.T) {
	tests := []struct {
		note     Note
		expected string
	}{
		{Note{C, 4}, "C4"},
		{Note{A, 4}, "A4"},
		{Note{CSharp, 5}, "C#5"},
		{Note{DSharp, 3}, "D#3"},
	}

	for _, tt := range tests {
		t.Run(tt.expected, func(t *testing.T) {
			if got := tt.note.String(); got != tt.expected {
				t.Errorf("Note.String() = %v, want %v", got, tt.expected)
			}
		})
	}
}

// TestNoteFrequency tests frequency calculation
func TestNoteFrequency(t *testing.T) {
	// A4 should be 440 Hz
	a4 := Note{Name: A, Octave: 4}
	if freq := a4.Frequency(); math.Abs(freq-440.0) > 0.01 {
		t.Errorf("A4 frequency = %v, want 440", freq)
	}

	// C4 should be approximately 261.63 Hz
	c4 := Note{Name: C, Octave: 4}
	expectedC4 := 261.63
	if freq := c4.Frequency(); math.Abs(freq-expectedC4) > 0.01 {
		t.Errorf("C4 frequency = %v, want %v", freq, expectedC4)
	}

	// A5 should be 880 Hz (one octave above A4)
	a5 := Note{Name: A, Octave: 5}
	if freq := a5.Frequency(); math.Abs(freq-880.0) > 0.01 {
		t.Errorf("A5 frequency = %v, want 880", freq)
	}
}

// TestNoteMIDI tests MIDI note number conversion
func TestNoteMIDI(t *testing.T) {
	tests := []struct {
		note     Note
		expected int
	}{
		{Note{C, 0}, 12},   // C0 = MIDI 12
		{Note{C, 4}, 60},    // C4 = MIDI 60
		{Note{A, 4}, 69},    // A4 = MIDI 69
		{Note{C, 5}, 72},    // C5 = MIDI 72
		{Note{G, 9}, 127},   // G9 = MIDI 127 (highest)
	}

	for _, tt := range tests {
		t.Run(tt.note.String(), func(t *testing.T) {
			if got := tt.note.MIDI(); got != tt.expected {
				t.Errorf("Note.MIDI() = %v, want %v", got, tt.expected)
			}
		})
	}
}

// TestMIDItoNote tests MIDI to note conversion
func TestMIDItoNote(t *testing.T) {
	tests := []struct {
		midi        int
		expected    Note
	}{
		{60, Note{C, 4}},
		{69, Note{A, 4}},
		{72, Note{C, 5}},
	}

	for _, tt := range tests {
		t.Run("", func(t *testing.T) {
			got := MIDItoNote(tt.midi)
			if got.Name != tt.expected.Name || got.Octave != tt.expected.Octave {
				t.Errorf("MIDItoNote(%v) = %v, want %v", tt.midi, got, tt.expected)
			}
		})
	}
}

// TestFrequencyToNote tests frequency to note conversion
func TestFrequencyToNote(t *testing.T) {
	// 440 Hz should be A4
	note := FrequencyToNote(440.0)
	if note.Name != A || note.Octave != 4 {
		t.Errorf("FrequencyToNote(440) = %v, want A4", note)
	}

	// 261.63 Hz should be approximately C4
	note = FrequencyToNote(261.63)
	if note.Name != C || note.Octave != 4 {
		t.Errorf("FrequencyToNote(261.63) = %v, want C4", note)
	}

	// 880 Hz should be A5
	note = FrequencyToNote(880.0)
	if note.Name != A || note.Octave != 5 {
		t.Errorf("FrequencyToNote(880) = %v, want A5", note)
	}
}

// TestNoteTranspose tests note transposition
func TestNoteTranspose(t *testing.T) {
	tests := []struct {
		note      Note
		semitones int
		expected  Note
	}{
		{Note{C, 4}, 12, Note{C, 5}},   // Octave up
		{Note{C, 4}, -12, Note{C, 3}},  // Octave down
		{Note{C, 4}, 7, Note{G, 4}},    // Perfect fifth up
		{Note{C, 4}, -7, Note{F, 3}},   // Perfect fifth down
		{Note{A, 4}, 3, Note{C, 5}},    // Minor third up (crossing octave)
	}

	for _, tt := range tests {
		t.Run("", func(t *testing.T) {
			got := tt.note.Transpose(tt.semitones)
			if got.Name != tt.expected.Name || got.Octave != tt.expected.Octave {
				t.Errorf("Note.Transpose(%v) = %v, want %v", tt.semitones, got, tt.expected)
			}
		})
	}
}

// TestParseNote tests note parsing
func TestParseNote(t *testing.T) {
	tests := []struct {
		input    string
		expected Note
		hasError bool
	}{
		{"C4", Note{C, 4}, false},
		{"A4", Note{A, 4}, false},
		{"C#5", Note{CSharp, 5}, false},
		{"Db3", Note{CSharp, 3}, false}, // Db = C#
		{"G#2", Note{GSharp, 2}, false},
		{"Ab2", Note{GSharp, 2}, false}, // Ab = G#
		{"invalid", Note{}, true},
		{"", Note{}, true},
	}

	for _, tt := range tests {
		t.Run(tt.input, func(t *testing.T) {
			got, err := ParseNote(tt.input)
			if tt.hasError {
				if err == nil {
					t.Errorf("ParseNote(%v) expected error, got %v", tt.input, got)
				}
			} else {
				if err != nil {
					t.Errorf("ParseNote(%v) unexpected error: %v", tt.input, err)
				} else if got.Name != tt.expected.Name || got.Octave != tt.expected.Octave {
					t.Errorf("ParseNote(%v) = %v, want %v", tt.input, got, tt.expected)
				}
			}
		})
	}
}

// TestScaleNotes tests scale note generation
func TestScaleNotes(t *testing.T) {
	// C major scale
	cMajor := NewScale(C, MajorScale)
	notes := cMajor.Notes()
	expected := []NoteName{C, D, E, F, G, A, B}
	if len(notes) != len(expected) {
		t.Errorf("C major scale has %v notes, want %v", len(notes), len(expected))
	}
	for i, n := range notes {
		if n != expected[i] {
			t.Errorf("C major scale note %d = %v, want %v", i, n, expected[i])
		}
	}

	// A minor scale
	aMinor := NewScale(A, MinorScale)
	notes = aMinor.Notes()
	expected = []NoteName{A, B, C, D, E, F, G}
	for i, n := range notes {
		if n != expected[i] {
			t.Errorf("A minor scale note %d = %v, want %v", i, n, expected[i])
		}
	}
}

// TestScaleContainsNote tests scale note membership
func TestScaleContainsNote(t *testing.T) {
	cMajor := NewScale(C, MajorScale)

	tests := []struct {
		note     NoteName
		expected bool
	}{
		{C, true},
		{D, true},
		{E, true},
		{F, true},
		{G, true},
		{A, true},
		{B, true},
		{CSharp, false}, // Not in C major
		{GSharp, false}, // Not in C major
	}

	for _, tt := range tests {
		t.Run(tt.note.String(), func(t *testing.T) {
			if got := cMajor.ContainsNote(tt.note); got != tt.expected {
				t.Errorf("Scale.ContainsNote(%v) = %v, want %v", tt.note, got, tt.expected)
			}
		})
	}
}

// TestScaleFrequencies tests scale frequency generation
func TestScaleFrequencies(t *testing.T) {
	cMajor := NewScale(C, MajorScale)
	freqs := cMajor.Frequencies(4, 1)

	if len(freqs) != 7 {
		t.Errorf("C major scale frequencies count = %v, want 7", len(freqs))
	}

	// First note (C4) should be approximately 261.63 Hz
	if math.Abs(freqs[0]-261.63) > 0.1 {
		t.Errorf("C4 frequency = %v, want approximately 261.63", freqs[0])
	}
}

// TestChordNotes tests chord note generation
func TestChordNotes(t *testing.T) {
	tests := []struct {
		name     string
		chord    Chord
		expected []NoteName
	}{
		{"C Major", NewChord(C, Major), []NoteName{C, E, G}},
		{"C Minor", NewChord(C, Minor), []NoteName{C, DSharp, G}},
		{"C Diminished", NewChord(C, Diminished), []NoteName{C, DSharp, FSharp}},
		{"C Augmented", NewChord(C, Augmented), []NoteName{C, E, GSharp}},
		{"C7", NewChord(C, DominantSeventh), []NoteName{C, E, G, ASharp}},
		{"Cmaj7", NewChord(C, MajorSeventh), []NoteName{C, E, G, B}},
		{"Cm7", NewChord(C, MinorSeventh), []NoteName{C, DSharp, G, ASharp}},
		{"C Power", NewChord(C, Power), []NoteName{C, G}},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			notes := tt.chord.Notes()
			if len(notes) != len(tt.expected) {
				t.Errorf("%v chord has %v notes, want %v", tt.name, len(notes), len(tt.expected))
				return
			}
			for i, n := range notes {
				if n != tt.expected[i] {
					t.Errorf("%v chord note %d = %v, want %v", tt.name, i, n, tt.expected[i])
				}
			}
		})
	}
}

// TestChordString tests chord string representation
func TestChordString(t *testing.T) {
	tests := []struct {
		chord    Chord
		expected string
	}{
		{NewChord(C, Major), "C"},
		{NewChord(A, Minor), "Am"},
		{NewChord(G, DominantSeventh), "G7"},
		{NewChord(F, MajorSeventh), "Fmaj7"},
		{NewChord(D, Power), "D5"},
	}

	for _, tt := range tests {
		t.Run(tt.expected, func(t *testing.T) {
			if got := tt.chord.String(); got != tt.expected {
				t.Errorf("Chord.String() = %v, want %v", got, tt.expected)
			}
		})
	}
}

// TestIdentifyChord tests chord identification
func TestIdentifyChord(t *testing.T) {
	tests := []struct {
		name     string
		notes    []NoteName
		expected ChordType
	}{
		{"C Major", []NoteName{C, E, G}, Major},
		{"A Minor", []NoteName{A, C, E}, Minor},
		{"G Power", []NoteName{G, D}, Power},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			chord, err := IdentifyChord(tt.notes)
			if err != nil {
				t.Errorf("IdentifyChord(%v) error: %v", tt.notes, err)
				return
			}
			if chord.Type != tt.expected {
				t.Errorf("IdentifyChord(%v) type = %v, want %v", tt.notes, chord.Type, tt.expected)
			}
		})
	}
}

// TestIdentifyChordErrors tests chord identification errors
func TestIdentifyChordErrors(t *testing.T) {
	_, err := IdentifyChord([]NoteName{C})
	if err == nil {
		t.Error("IdentifyChord with single note should return error")
	}

	_, err = IdentifyChord([]NoteName{})
	if err == nil {
		t.Error("IdentifyChord with empty notes should return error")
	}
}

// TestIntervalSemitones tests interval semitone counts
func TestIntervalSemitones(t *testing.T) {
	tests := []struct {
		interval   Interval
		semitones  int
	}{
		{Unison, 0},
		{MinorSecond, 1},
		{MajorSecond, 2},
		{MinorThird, 3},
		{MajorThird, 4},
		{PerfectFourth, 5},
		{AugmentedFourth, 6},
		{PerfectFifth, 7},
		{MinorSixth, 8},
		{MajorSixth, 9},
		{MinorSeventh, 10},
		{MajorSeventh, 11},
		{Octave, 12},
	}

	for _, tt := range tests {
		t.Run(tt.interval.String(), func(t *testing.T) {
			if got := tt.interval.Semitones(); got != tt.semitones {
				t.Errorf("Interval.Semitones() = %v, want %v", got, tt.semitones)
			}
		})
	}
}

// TestGetInterval tests interval detection between notes
func TestGetInterval(t *testing.T) {
	tests := []struct {
		from     Note
		to       Note
		expected Interval
	}{
		{Note{C, 4}, Note{C, 4}, Unison},
		{Note{C, 4}, Note{D, 4}, MajorSecond},
		{Note{C, 4}, Note{E, 4}, MajorThird},
		{Note{C, 4}, Note{G, 4}, PerfectFifth},
		{Note{C, 4}, Note{C, 5}, Octave},
		{Note{A, 4}, Note{C, 5}, MinorThird}, // A to C
	}

	for _, tt := range tests {
		t.Run("", func(t *testing.T) {
			if got := GetInterval(tt.from, tt.to); got != tt.expected {
				t.Errorf("GetInterval(%v, %v) = %v, want %v", tt.from, tt.to, got, tt.expected)
			}
		})
	}
}

// TestCircleOfFifths tests circle of fifths
func TestCircleOfFifths(t *testing.T) {
	cof := CircleOfFifths()
	expected := []NoteName{C, G, D, A, E, B, FSharp, CSharp, GSharp, DSharp, ASharp, F}

	if len(cof) != len(expected) {
		t.Errorf("Circle of fifths length = %v, want %v", len(cof), len(expected))
		return
	}

	for i, n := range cof {
		if n != expected[i] {
			t.Errorf("Circle of fifths[%d] = %v, want %v", i, n, expected[i])
		}
	}
}

// TestRelativeMinor tests relative minor key
func TestRelativeMinor(t *testing.T) {
	tests := []struct {
		major    NoteName
		minor    NoteName
	}{
		{C, A},
		{G, E},
		{D, B},
		{A, FSharp},
		{E, CSharp},
	}

	for _, tt := range tests {
		t.Run("", func(t *testing.T) {
			if got := RelativeMinor(tt.major); got != tt.minor {
				t.Errorf("RelativeMinor(%v) = %v, want %v", tt.major, got, tt.minor)
			}
		})
	}
}

// TestRelativeMajor tests relative major key
func TestRelativeMajor(t *testing.T) {
	tests := []struct {
		minor    NoteName
		major    NoteName
	}{
		{A, C},
		{E, G},
		{B, D},
		{FSharp, A},
		{CSharp, E},
	}

	for _, tt := range tests {
		t.Run("", func(t *testing.T) {
			if got := RelativeMajor(tt.minor); got != tt.major {
				t.Errorf("RelativeMajor(%v) = %v, want %v", tt.minor, got, tt.major)
			}
		})
	}
}

// TestBPMConversions tests BPM to milliseconds conversions
func TestBPMConversions(t *testing.T) {
	// 60 BPM = 1000ms per beat
	ms := BPMtoMilliseconds(60)
	if math.Abs(ms-1000.0) > 0.01 {
		t.Errorf("BPMtoMilliseconds(60) = %v, want 1000", ms)
	}

	// 120 BPM = 500ms per beat
	ms = BPMtoMilliseconds(120)
	if math.Abs(ms-500.0) > 0.01 {
		t.Errorf("BPMtoMilliseconds(120) = %v, want 500", ms)
	}

	// Test reverse conversion
	bpm := MillisecondsToBPM(1000)
	if bpm != 60 {
		t.Errorf("MillisecondsToBPM(1000) = %v, want 60", bpm)
	}

	bpm = MillisecondsToBPM(500)
	if bpm != 120 {
		t.Errorf("MillisecondsToBPM(500) = %v, want 120", bpm)
	}
}

// TestBPMtoSeconds tests BPM to seconds conversions
func TestBPMtoSeconds(t *testing.T) {
	// 60 BPM = 1 second per beat
	sec := BPMtoSeconds(60)
	if math.Abs(sec-1.0) > 0.0001 {
		t.Errorf("BPMtoSeconds(60) = %v, want 1", sec)
	}

	// 120 BPM = 0.5 seconds per beat
	sec = BPMtoSeconds(120)
	if math.Abs(sec-0.5) > 0.0001 {
		t.Errorf("BPMtoSeconds(120) = %v, want 0.5", sec)
	}
}

// TestNoteValueDuration tests note value durations
func TestNoteValueDuration(t *testing.T) {
	tests := []struct {
		value    NoteValue
		expected float64
	}{
		{WholeNote, 4.0},
		{HalfNote, 2.0},
		{QuarterNote, 1.0},
		{EighthNote, 0.5},
		{SixteenthNote, 0.25},
	}

	for _, tt := range tests {
		t.Run("", func(t *testing.T) {
			if got := tt.value.Duration(); got != tt.expected {
				t.Errorf("NoteValue.Duration() = %v, want %v", got, tt.expected)
			}
		})
	}
}

// TestNoteValueDurationMs tests note value duration in milliseconds
func TestNoteValueDurationMs(t *testing.T) {
	// Quarter note at 60 BPM = 1000ms
	quarterMs := QuarterNote.DurationMs(60)
	if math.Abs(quarterMs-1000.0) > 0.01 {
		t.Errorf("QuarterNote.DurationMs(60) = %v, want 1000", quarterMs)
	}

	// Whole note at 60 BPM = 4000ms
	wholeMs := WholeNote.DurationMs(60)
	if math.Abs(wholeMs-4000.0) > 0.01 {
		t.Errorf("WholeNote.DurationMs(60) = %v, want 4000", wholeMs)
	}
}

// TestNoteValueDurationWithDots tests dotted note durations
func TestNoteValueDurationWithDots(t *testing.T) {
	// Quarter note with one dot = 1 + 0.5 = 1.5 beats
	dottedQuarter := QuarterNote.DurationWithDots(1)
	if math.Abs(dottedQuarter-1.5) > 0.0001 {
		t.Errorf("QuarterNote.DurationWithDots(1) = %v, want 1.5", dottedQuarter)
	}

	// Quarter note with two dots = 1 + 0.5 + 0.25 = 1.75 beats
	doubleDottedQuarter := QuarterNote.DurationWithDots(2)
	if math.Abs(doubleDottedQuarter-1.75) > 0.0001 {
		t.Errorf("QuarterNote.DurationWithDots(2) = %v, want 1.75", doubleDottedQuarter)
	}
}

// TestEqualTemperamentFrequency tests equal temperament frequency calculation
func TestEqualTemperamentFrequency(t *testing.T) {
	// A4 = 440 Hz (0 semitones from A4)
	freq := EqualTemperamentFrequency(0)
	if math.Abs(freq-440.0) > 0.01 {
		t.Errorf("EqualTemperamentFrequency(0) = %v, want 440", freq)
	}

	// A5 = 880 Hz (12 semitones from A4)
	freq = EqualTemperamentFrequency(12)
	if math.Abs(freq-880.0) > 0.01 {
		t.Errorf("EqualTemperamentFrequency(12) = %v, want 880", freq)
	}

	// A3 = 220 Hz (-12 semitones from A4)
	freq = EqualTemperamentFrequency(-12)
	if math.Abs(freq-220.0) > 0.01 {
		t.Errorf("EqualTemperamentFrequency(-12) = %v, want 220", freq)
	}
}

// TestHarmonicSeries tests harmonic series generation
func TestHarmonicSeries(t *testing.T) {
	series := HarmonicSeries(100.0, 5)
	expected := []float64{100.0, 200.0, 300.0, 400.0, 500.0}

	if len(series) != len(expected) {
		t.Errorf("HarmonicSeries length = %v, want %v", len(series), len(expected))
		return
	}

	for i, f := range series {
		if math.Abs(f-expected[i]) > 0.01 {
			t.Errorf("HarmonicSeries[%d] = %v, want %v", i, f, expected[i])
		}
	}
}

// TestBeatFrequency tests beat frequency calculation
func TestBeatFrequency(t *testing.T) {
	// 440 Hz and 442 Hz should produce 2 Hz beats
	beat := BeatFrequency(440.0, 442.0)
	if math.Abs(beat-2.0) > 0.01 {
		t.Errorf("BeatFrequency(440, 442) = %v, want 2", beat)
	}

	// Order shouldn't matter
	beat = BeatFrequency(442.0, 440.0)
	if math.Abs(beat-2.0) > 0.01 {
		t.Errorf("BeatFrequency(442, 440) = %v, want 2", beat)
	}
}

// TestJustIntonation tests just intonation ratios
func TestJustIntonation(t *testing.T) {
	// Perfect fifth (3:2) of 440 Hz should be 660 Hz
	fifth := JustIntervals["fifth"]
	freq := fifth.Frequency(440.0)
	if math.Abs(freq-660.0) > 0.01 {
		t.Errorf("Just fifth of 440 Hz = %v, want 660", freq)
	}

	// Octave (2:1) of 440 Hz should be 880 Hz
	octave := JustIntervals["octave"]
	freq = octave.Frequency(440.0)
	if math.Abs(freq-880.0) > 0.01 {
		t.Errorf("Just octave of 440 Hz = %v, want 880", freq)
	}
}

// TestScaleTypeString tests scale type string representation
func TestScaleTypeString(t *testing.T) {
	tests := []struct {
		scaleType ScaleType
		expected  string
	}{
		{MajorScale, "Major"},
		{MinorScale, "Natural Minor"},
		{HarmonicMinor, "Harmonic Minor"},
		{Dorian, "Dorian"},
		{PentatonicMajor, "Major Pentatonic"},
		{BluesScale, "Blues"},
	}

	for _, tt := range tests {
		t.Run(tt.expected, func(t *testing.T) {
			if got := tt.scaleType.String(); got != tt.expected {
				t.Errorf("ScaleType.String() = %v, want %v", got, tt.expected)
			}
		})
	}
}

// TestChordTypeString tests chord type string representation
func TestChordTypeString(t *testing.T) {
	tests := []struct {
		chordType ChordType
		expected  string
	}{
		{Major, "Major"},
		{Minor, "Minor"},
		{MajorSeventh, "Major 7th"},
		{DominantSeventh, "Dominant 7th"},
		{Power, "Power"},
	}

	for _, tt := range tests {
		t.Run(tt.expected, func(t *testing.T) {
			if got := tt.chordType.String(); got != tt.expected {
				t.Errorf("ChordType.String() = %v, want %v", got, tt.expected)
			}
		})
	}
}

// TestChordTypeSymbol tests chord type symbol representation
func TestChordTypeSymbol(t *testing.T) {
	tests := []struct {
		chordType ChordType
		expected  string
	}{
		{Major, ""},
		{Minor, "m"},
		{MajorSeventh, "maj7"},
		{DominantSeventh, "7"},
		{Power, "5"},
	}

	for _, tt := range tests {
		t.Run(tt.expected, func(t *testing.T) {
			if got := tt.chordType.Symbol(); got != tt.expected {
				t.Errorf("ChordType.Symbol() = %v, want %v", got, tt.expected)
			}
		})
	}
}

// TestChordFrequencies tests chord frequency generation
func TestChordFrequencies(t *testing.T) {
	cMajor := NewChord(C, Major)
	freqs := cMajor.Frequencies(4)

	if len(freqs) != 3 {
		t.Errorf("C major chord should have 3 frequencies, got %v", len(freqs))
		return
	}

	// C4 should be approximately 261.63 Hz
	if math.Abs(freqs[0]-261.63) > 0.1 {
		t.Errorf("C4 in chord = %v Hz, want approximately 261.63", freqs[0])
	}

	// E4 should be approximately 329.63 Hz
	if math.Abs(freqs[1]-329.63) > 0.1 {
		t.Errorf("E4 in chord = %v Hz, want approximately 329.63", freqs[1])
	}

	// G4 should be approximately 392.00 Hz
	if math.Abs(freqs[2]-392.00) > 0.1 {
		t.Errorf("G4 in chord = %v Hz, want approximately 392.00", freqs[2])
	}
}

// TestScaleNotesWithOctave tests scale generation across octaves
func TestScaleNotesWithOctave(t *testing.T) {
	cMajor := NewScale(C, MajorScale)
	notes := cMajor.NotesWithOctave(4, 2) // Two octaves starting from C4

	if len(notes) != 14 { // 7 notes * 2 octaves
		t.Errorf("Two octaves of C major should have 14 notes, got %v", len(notes))
	}

	// First note should be C4
	if notes[0].Name != C || notes[0].Octave != 4 {
		t.Errorf("First note should be C4, got %v", notes[0])
	}

	// Last note should be B5
	if notes[13].Name != B || notes[13].Octave != 5 {
		t.Errorf("Last note should be B5, got %v", notes[13])
	}
}

// TestChordNotesWithOctave tests chord generation with octave
func TestChordNotesWithOctave(t *testing.T) {
	cMajor := NewChord(C, Major)
	notes := cMajor.NotesWithOctave(4)

	if len(notes) != 3 {
		t.Errorf("C major chord should have 3 notes, got %v", len(notes))
	}

	// C4, E4, G4
	if notes[0].Name != C || notes[0].Octave != 4 {
		t.Errorf("First note should be C4, got %v", notes[0])
	}
	if notes[1].Name != E || notes[1].Octave != 4 {
		t.Errorf("Second note should be E4, got %v", notes[1])
	}
	if notes[2].Name != G || notes[2].Octave != 4 {
		t.Errorf("Third note should be G4, got %v", notes[2])
	}
}

// TestSemitonesFrom tests semitone distance calculation
func TestSemitonesFrom(t *testing.T) {
	tests := []struct {
		from     Note
		to       Note
		expected int
	}{
		{Note{C, 4}, Note{D, 4}, 2},
		{Note{C, 4}, Note{C, 5}, 12},
		{Note{A, 4}, Note{C, 5}, 3},
		{Note{C, 5}, Note{C, 4}, -12},
	}

	for _, tt := range tests {
		t.Run("", func(t *testing.T) {
			if got := tt.to.SemitonesFrom(tt.from); got != tt.expected {
				t.Errorf("Note.SemitonesFrom() = %v, want %v", got, tt.expected)
			}
		})
	}
}

// TestTransposeByInterval tests interval-based transposition
func TestTransposeByInterval(t *testing.T) {
	c4 := Note{C, 4}

	tests := []struct {
		interval Interval
		expected Note
	}{
		{Unison, Note{C, 4}},
		{MajorThird, Note{E, 4}},
		{PerfectFifth, Note{G, 4}},
		{Octave, Note{C, 5}},
		{MajorSeventh, Note{B, 4}},
	}

	for _, tt := range tests {
		t.Run(tt.interval.String(), func(t *testing.T) {
			got := TransposeByInterval(c4, tt.interval)
			if got.Name != tt.expected.Name || got.Octave != tt.expected.Octave {
				t.Errorf("TransposeByInterval(C4, %v) = %v, want %v", tt.interval, got, tt.expected)
			}
		})
	}
}

// TestResonantFrequency tests resonant frequency calculation
func TestResonantFrequency(t *testing.T) {
	// First mode (fundamental) for 1 meter at 343 m/s (speed of sound)
	freq := ResonantFrequency(1.0, 343.0, 1)
	if math.Abs(freq-171.5) > 0.01 {
		t.Errorf("ResonantFrequency(1, 343, 1) = %v, want 171.5", freq)
	}

	// Second mode (first harmonic)
	freq = ResonantFrequency(1.0, 343.0, 2)
	if math.Abs(freq-343.0) > 0.01 {
		t.Errorf("ResonantFrequency(1, 343, 2) = %v, want 343", freq)
	}
}

// TestCentsDeviation tests cents deviation calculation
func TestCentsDeviation(t *testing.T) {
	// Exactly A4 (440 Hz) should have 0 cents deviation
	cents := CentsDeviation(440.0)
	if cents != 0 {
		t.Errorf("CentsDeviation(440) = %v, want 0", cents)
	}

	// Slightly sharp A4 should have positive cents
	cents = CentsDeviation(441.0)
	if cents <= 0 {
		t.Errorf("CentsDeviation(441) should be positive, got %v", cents)
	}

	// Slightly flat A4 should have negative cents
	cents = CentsDeviation(439.0)
	if cents >= 0 {
		t.Errorf("CentsDeviation(439) should be negative, got %v", cents)
	}
}

// TestChordFullName tests chord full name
func TestChordFullName(t *testing.T) {
	tests := []struct {
		chord    Chord
		expected string
	}{
		{NewChord(C, Major), "C Major"},
		{NewChord(A, Minor), "A Minor"},
		{NewChord(G, DominantSeventh), "G Dominant 7th"},
	}

	for _, tt := range tests {
		t.Run(tt.expected, func(t *testing.T) {
			if got := tt.chord.FullName(); got != tt.expected {
				t.Errorf("Chord.FullName() = %v, want %v", got, tt.expected)
			}
		})
	}
}

// TestCircleOfFourths tests circle of fourths
func TestCircleOfFourths(t *testing.T) {
	cof := CircleOfFourths()
	expected := []NoteName{C, F, ASharp, DSharp, GSharp, CSharp, FSharp, B, E, A, D, G}

	if len(cof) != len(expected) {
		t.Errorf("Circle of fourths length = %v, want %v", len(cof), len(expected))
		return
	}

	for i, n := range cof {
		if n != expected[i] {
			t.Errorf("Circle of fourths[%d] = %v, want %v", i, n, expected[i])
		}
	}
}