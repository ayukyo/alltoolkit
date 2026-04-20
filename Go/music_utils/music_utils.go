// Package music_utils provides music theory utilities.
// Zero external dependencies - pure Go standard library implementation.
//
// Features:
//   - Note frequency calculations (A4 = 440Hz standard)
//   - Scale generation (major, minor, modes, pentatonic, blues)
//   - Chord generation and identification
//   - MIDI note conversions
//   - Interval calculations
//   - Key signature helpers
//
// Author: AllToolkit
// Date: 2026-04-20
package music_utils

import (
	"errors"
	"fmt"
	"math"
	"sort"
	"strings"
)

// Note names
type NoteName int

const (
	C NoteName = iota
	CSharp
	D
	DSharp
	E
	F
	FSharp
	G
	GSharp
	A
	ASharp
	B
)

// Note name strings for display
var noteNames = map[NoteName]string{
	C:     "C",
	CSharp: "C#",
	D:     "D",
	DSharp: "D#",
	E:     "E",
	F:     "F",
	FSharp: "F#",
	G:     "G",
	GSharp: "G#",
	A:     "A",
	ASharp: "A#",
	B:     "B",
}

// Alternate names (flats)
var noteNamesFlat = map[NoteName]string{
	C:     "C",
	CSharp: "Db",
	D:     "D",
	DSharp: "Eb",
	E:     "E",
	F:     "F",
	FSharp: "Gb",
	G:     "G",
	GSharp: "Ab",
	A:     "A",
	ASharp: "Bb",
	B:     "B",
}

// String returns the note name as a string (using sharps by default)
func (n NoteName) String() string {
	if name, ok := noteNames[n]; ok {
		return name
	}
	return "Unknown"
}

// StringFlat returns the note name using flat notation
func (n NoteName) StringFlat() string {
	if name, ok := noteNamesFlat[n]; ok {
		return name
	}
	return "Unknown"
}

// Note represents a musical note with octave
type Note struct {
	Name   NoteName
	Octave int
}

// String returns the note as a string (e.g., "C4", "A#5")
func (n Note) String() string {
	return fmt.Sprintf("%s%d", n.Name.String(), n.Octave)
}

// StringFlat returns the note using flat notation
func (n Note) StringFlat() string {
	return fmt.Sprintf("%s%d", n.Name.StringFlat(), n.Octave)
}

// Frequency calculates the frequency of the note in Hz
// Using equal temperament: f = 440 * 2^((n-69)/12) where n is MIDI note number
func (n Note) Frequency() float64 {
	midi := n.MIDI()
	return 440.0 * math.Pow(2, float64(midi-69)/12.0)
}

// MIDI returns the MIDI note number (C4 = 60, A4 = 69)
func (n Note) MIDI() int {
	return n.Octave*12 + int(n.Name) + 12
}

// SemitonesFrom returns the number of semitones from another note
func (n Note) SemitonesFrom(other Note) int {
	return n.MIDI() - other.MIDI()
}

// Transpose transposes the note by a number of semitones
func (n Note) Transpose(semitones int) Note {
	newMIDI := n.MIDI() + semitones
	return MIDItoNote(newMIDI)
}

// MIDItoNote converts a MIDI note number to a Note
func MIDItoNote(midi int) Note {
	octave := (midi - 12) / 12
	name := NoteName((midi-12)%12 + 1)
	if name < 0 {
		name += 12
	}
	// Adjust for correct calculation
	name = NoteName((midi - 12) % 12)
	return Note{Name: name, Octave: octave}
}

// FrequencyToNote converts a frequency to the nearest Note
func FrequencyToNote(freq float64) Note {
	if freq <= 0 {
		return Note{Name: A, Octave: 4}
	}
	// f = 440 * 2^((n-69)/12)
	// n = 69 + 12 * log2(f/440)
	midi := 69 + 12*math.Log2(freq/440.0)
	return MIDItoNote(int(math.Round(midi)))
}

// CentsDeviation returns how many cents the frequency deviates from the nearest note
func CentsDeviation(freq float64) int {
	if freq <= 0 {
		return 0
	}
	midiExact := 69 + 12*math.Log2(freq/440.0)
	midiNearest := math.Round(midiExact)
	cents := int(math.Round((midiExact - midiNearest) * 100))
	return cents
}

// Interval types
type Interval int

const (
	Unison Interval = iota
	MinorSecond
	MajorSecond
	MinorThird
	MajorThird
	PerfectFourth
	AugmentedFourth
	PerfectFifth
	MinorSixth
	MajorSixth
	MinorSeventh
	MajorSeventh
	Octave
	MinorNinth
	MajorNinth
	MinorTenth
	MajorTenth
	PerfectEleventh
	AugmentedEleventh
	PerfectTwelfth
	MinorThirteenth
	MajorThirteenth
)

// Interval names
var intervalNames = map[Interval]string{
	Unison:           "Unison",
	MinorSecond:      "Minor Second",
	MajorSecond:      "Major Second",
	MinorThird:       "Minor Third",
	MajorThird:       "Major Third",
	PerfectFourth:    "Perfect Fourth",
	AugmentedFourth:  "Augmented Fourth",
	PerfectFifth:     "Perfect Fifth",
	MinorSixth:       "Minor Sixth",
	MajorSixth:       "Major Sixth",
	MinorSeventh:     "Minor Seventh",
	MajorSeventh:     "Major Seventh",
	Octave:           "Octave",
	MinorNinth:       "Minor Ninth",
	MajorNinth:       "Major Ninth",
	MinorTenth:       "Minor Tenth",
	MajorTenth:       "Major Tenth",
	PerfectEleventh:  "Perfect Eleventh",
	AugmentedEleventh: "Augmented Eleventh",
	PerfectTwelfth:   "Perfect Twelfth",
	MinorThirteenth:  "Minor Thirteenth",
	MajorThirteenth:  "Major Thirteenth",
}

// Semitones returns the number of semitones in the interval
func (i Interval) Semitones() int {
	return int(i)
}

// String returns the interval name
func (i Interval) String() string {
	if name, ok := intervalNames[i]; ok {
		return name
	}
	return "Unknown Interval"
}

// GetInterval returns the interval between two notes
func GetInterval(from, to Note) Interval {
	semitones := to.SemitonesFrom(from)
	if semitones < 0 {
		semitones = -semitones
	}
	if semitones > 24 {
		semitones = semitones % 12 + 12
	}
	switch semitones {
	case 0:
		return Unison
	case 1:
		return MinorSecond
	case 2:
		return MajorSecond
	case 3:
		return MinorThird
	case 4:
		return MajorThird
	case 5:
		return PerfectFourth
	case 6:
		return AugmentedFourth
	case 7:
		return PerfectFifth
	case 8:
		return MinorSixth
	case 9:
		return MajorSixth
	case 10:
		return MinorSeventh
	case 11:
		return MajorSeventh
	case 12:
		return Octave
	case 13:
		return MinorNinth
	case 14:
		return MajorNinth
	case 15:
		return MinorTenth
	case 16:
		return MajorTenth
	case 17:
		return PerfectEleventh
	case 18:
		return AugmentedEleventh
	case 19:
		return PerfectTwelfth
	case 20:
		return MinorThirteenth
	case 21:
		return MajorThirteenth
	default:
		return Unison
	}
}

// Scale types
type ScaleType int

const (
	MajorScale ScaleType = iota
	MinorScale
	HarmonicMinor
	MelodicMinor
	Dorian
	Phrygian
	Lydian
	Mixolydian
	Locrian
	PentatonicMajor
	PentatonicMinor
	BluesScale
	Chromatic
	WholeTone
)

// Scale patterns (semitones from root)
var scalePatterns = map[ScaleType][]int{
	MajorScale:       {0, 2, 4, 5, 7, 9, 11},
	MinorScale:       {0, 2, 3, 5, 7, 8, 10},
	HarmonicMinor:    {0, 2, 3, 5, 7, 8, 11},
	MelodicMinor:     {0, 2, 3, 5, 7, 9, 11},
	Dorian:           {0, 2, 3, 5, 7, 9, 10},
	Phrygian:         {0, 1, 3, 5, 7, 8, 10},
	Lydian:           {0, 2, 4, 6, 7, 9, 11},
	Mixolydian:       {0, 2, 4, 5, 7, 9, 10},
	Locrian:          {0, 1, 3, 5, 6, 8, 10},
	PentatonicMajor:  {0, 2, 4, 7, 9},
	PentatonicMinor:  {0, 3, 5, 7, 10},
	BluesScale:       {0, 3, 5, 6, 7, 10},
	Chromatic:        {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11},
	WholeTone:        {0, 2, 4, 6, 8, 10},
}

// Scale type names
var scaleTypeNames = map[ScaleType]string{
	MajorScale:      "Major",
	MinorScale:      "Natural Minor",
	HarmonicMinor:   "Harmonic Minor",
	MelodicMinor:    "Melodic Minor",
	Dorian:          "Dorian",
	Phrygian:        "Phrygian",
	Lydian:          "Lydian",
	Mixolydian:      "Mixolydian",
	Locrian:         "Locrian",
	PentatonicMajor: "Major Pentatonic",
	PentatonicMinor: "Minor Pentatonic",
	BluesScale:      "Blues",
	Chromatic:       "Chromatic",
	WholeTone:       "Whole Tone",
}

// String returns the scale type name
func (s ScaleType) String() string {
	if name, ok := scaleTypeNames[s]; ok {
		return name
	}
	return "Unknown Scale"
}

// Scale represents a musical scale
type Scale struct {
	Root NoteName
	Type ScaleType
}

// String returns the scale name
func (s Scale) String() string {
	return fmt.Sprintf("%s %s", s.Root.String(), s.Type.String())
}

// Notes returns all notes in the scale within one octave
func (s Scale) Notes() []NoteName {
	pattern := scalePatterns[s.Type]
	notes := make([]NoteName, len(pattern))
	for i, semitone := range pattern {
		notes[i] = NoteName((int(s.Root) + semitone) % 12)
	}
	return notes
}

// NotesWithOctave returns all notes in the scale across multiple octaves
func (s Scale) NotesWithOctave(startOctave, octaves int) []Note {
	pattern := scalePatterns[s.Type]
	totalNotes := len(pattern) * octaves
	notes := make([]Note, 0, totalNotes)
	
	for oct := 0; oct < octaves; oct++ {
		for _, semitone := range pattern {
			noteName := NoteName((int(s.Root) + semitone) % 12)
			octave := startOctave + oct + (int(s.Root)+semitone)/12
			notes = append(notes, Note{Name: noteName, Octave: octave})
		}
	}
	return notes
}

// Frequencies returns all frequencies in the scale
func (s Scale) Frequencies(startOctave, octaves int) []float64 {
	notes := s.NotesWithOctave(startOctave, octaves)
	freqs := make([]float64, len(notes))
	for i, note := range notes {
		freqs[i] = note.Frequency()
	}
	return freqs
}

// ContainsNote checks if a note is in the scale
func (s Scale) ContainsNote(note NoteName) bool {
	for _, n := range s.Notes() {
		if n == note {
			return true
		}
	}
	return false
}

// NewScale creates a new scale
func NewScale(root NoteName, scaleType ScaleType) Scale {
	return Scale{Root: root, Type: scaleType}
}

// ParseNote parses a note string (e.g., "C4", "A#5", "Db3")
func ParseNote(s string) (Note, error) {
	s = strings.TrimSpace(s)
	if len(s) < 2 {
		return Note{}, errors.New("invalid note format")
	}
	
	// Extract note name
	var name NoteName
	var rest string
	
	// Check for sharp
	if strings.Contains(s, "#") {
		rest = strings.TrimPrefix(s, s[:strings.Index(s, "#")+1])
		switch s[:strings.Index(s, "#")+1] {
		case "C#":
			name = CSharp
		case "D#":
			name = DSharp
		case "F#":
			name = FSharp
		case "G#":
			name = GSharp
		case "A#":
			name = ASharp
		default:
			return Note{}, fmt.Errorf("unknown note: %s", s)
		}
	} else if strings.Contains(s, "b") {
		// Check for flat
		rest = strings.TrimPrefix(s, s[:strings.Index(s, "b")+1])
		switch s[:strings.Index(s, "b")+1] {
		case "Db":
			name = CSharp
		case "Eb":
			name = DSharp
		case "Gb":
			name = FSharp
		case "Ab":
			name = GSharp
		case "Bb":
			name = ASharp
		default:
			return Note{}, fmt.Errorf("unknown note: %s", s)
		}
	} else {
		rest = s[1:]
		switch s[0] {
		case 'C':
			name = C
		case 'D':
			name = D
		case 'E':
			name = E
		case 'F':
			name = F
		case 'G':
			name = G
		case 'A':
			name = A
		case 'B':
			name = B
		default:
			return Note{}, fmt.Errorf("unknown note: %s", s)
		}
	}
	
	// Parse octave
	var octave int
	_, err := fmt.Sscanf(rest, "%d", &octave)
	if err != nil {
		return Note{}, fmt.Errorf("invalid octave: %s", rest)
	}
	
	return Note{Name: name, Octave: octave}, nil
}

// Chord types
type ChordType int

const (
	Major ChordType = iota
	Minor
	Diminished
	Augmented
	MajorSeventh
	MinorSeventh
	DominantSeventh
	DiminishedSeventh
	HalfDiminished
	SuspendedSecond
	SuspendedFourth
	MajorSixth
	MinorSixth
	MinorMajorSeventh
	AugmentedMajorSeventh
	AugmentedSeventh
	Ninth
	MinorNinth
	MajorNinth
	Eleventh
	MinorEleventh
	MajorEleventh
	Thirteenth
	MinorThirteenth
	MajorThirteenth
	AddNine
	MinorAddNine
	Power
)

// Chord patterns (semitones from root)
var chordPatterns = map[ChordType][]int{
	Major:                {0, 4, 7},
	Minor:                {0, 3, 7},
	Diminished:           {0, 3, 6},
	Augmented:            {0, 4, 8},
	MajorSeventh:         {0, 4, 7, 11},
	MinorSeventh:         {0, 3, 7, 10},
	DominantSeventh:      {0, 4, 7, 10},
	DiminishedSeventh:    {0, 3, 6, 9},
	HalfDiminished:       {0, 3, 6, 10},
	SuspendedSecond:      {0, 2, 7},
	SuspendedFourth:      {0, 5, 7},
	MajorSixth:           {0, 4, 7, 9},
	MinorSixth:           {0, 3, 7, 9},
	MinorMajorSeventh:    {0, 3, 7, 11},
	AugmentedMajorSeventh: {0, 4, 8, 11},
	AugmentedSeventh:     {0, 4, 8, 10},
	Ninth:                {0, 4, 7, 10, 14},
	MinorNinth:           {0, 3, 7, 10, 14},
	MajorNinth:           {0, 4, 7, 11, 14},
	Eleventh:             {0, 4, 7, 10, 14, 17},
	MinorEleventh:        {0, 3, 7, 10, 14, 17},
	MajorEleventh:        {0, 4, 7, 11, 14, 17},
	Thirteenth:           {0, 4, 7, 10, 14, 17, 21},
	MinorThirteenth:      {0, 3, 7, 10, 14, 17, 21},
	MajorThirteenth:      {0, 4, 7, 11, 14, 17, 21},
	AddNine:              {0, 4, 7, 14},
	MinorAddNine:         {0, 3, 7, 14},
	Power:                {0, 7},
}

// Chord type names and symbols
var chordTypeNames = map[ChordType]string{
	Major:                "Major",
	Minor:                "Minor",
	Diminished:           "Diminished",
	Augmented:            "Augmented",
	MajorSeventh:         "Major 7th",
	MinorSeventh:         "Minor 7th",
	DominantSeventh:      "Dominant 7th",
	DiminishedSeventh:    "Diminished 7th",
	HalfDiminished:       "Half Diminished",
	SuspendedSecond:      "Suspended 2nd",
	SuspendedFourth:      "Suspended 4th",
	MajorSixth:           "Major 6th",
	MinorSixth:           "Minor 6th",
	MinorMajorSeventh:    "Minor-Major 7th",
	AugmentedMajorSeventh: "Augmented Major 7th",
	AugmentedSeventh:     "Augmented 7th",
	Ninth:                "9th",
	MinorNinth:           "Minor 9th",
	MajorNinth:           "Major 9th",
	Eleventh:             "11th",
	MinorEleventh:        "Minor 11th",
	MajorEleventh:        "Major 11th",
	Thirteenth:           "13th",
	MinorThirteenth:      "Minor 13th",
	MajorThirteenth:      "Major 13th",
	AddNine:              "Add9",
	MinorAddNine:         "Minor Add9",
	Power:                "Power",
}

var chordTypeSymbols = map[ChordType]string{
	Major:                "",
	Minor:                "m",
	Diminished:           "dim",
	Augmented:            "aug",
	MajorSeventh:         "maj7",
	MinorSeventh:         "m7",
	DominantSeventh:      "7",
	DiminishedSeventh:    "dim7",
	HalfDiminished:       "m7b5",
	SuspendedSecond:      "sus2",
	SuspendedFourth:      "sus4",
	MajorSixth:           "6",
	MinorSixth:           "m6",
	MinorMajorSeventh:    "mmaj7",
	AugmentedMajorSeventh: "augmaj7",
	AugmentedSeventh:     "aug7",
	Ninth:                "9",
	MinorNinth:           "m9",
	MajorNinth:           "maj9",
	Eleventh:             "11",
	MinorEleventh:        "m11",
	MajorEleventh:        "maj11",
	Thirteenth:           "13",
	MinorThirteenth:      "m13",
	MajorThirteenth:      "maj13",
	AddNine:              "add9",
	MinorAddNine:         "madd9",
	Power:                "5",
}

// String returns the chord type name
func (c ChordType) String() string {
	if name, ok := chordTypeNames[c]; ok {
		return name
	}
	return "Unknown Chord"
}

// Symbol returns the chord type symbol
func (c ChordType) Symbol() string {
	if symbol, ok := chordTypeSymbols[c]; ok {
		return symbol
	}
	return "?"
}

// Chord represents a musical chord
type Chord struct {
	Root NoteName
	Type ChordType
}

// String returns the chord name
func (c Chord) String() string {
	return fmt.Sprintf("%s%s", c.Root.String(), c.Type.Symbol())
}

// FullName returns the full chord name
func (c Chord) FullName() string {
	return fmt.Sprintf("%s %s", c.Root.String(), c.Type.String())
}

// Notes returns the notes in the chord
func (c Chord) Notes() []NoteName {
	pattern := chordPatterns[c.Type]
	notes := make([]NoteName, len(pattern))
	for i, semitone := range pattern {
		notes[i] = NoteName((int(c.Root) + semitone%12) % 12)
	}
	return notes
}

// NotesWithOctave returns the notes with octave
func (c Chord) NotesWithOctave(octave int) []Note {
	pattern := chordPatterns[c.Type]
	notes := make([]Note, len(pattern))
	for i, semitone := range pattern {
		totalSemitones := int(c.Root) + semitone
		noteName := NoteName(totalSemitones % 12)
		noteOctave := octave + totalSemitones/12
		notes[i] = Note{Name: noteName, Octave: noteOctave}
	}
	return notes
}

// Frequencies returns the frequencies of the chord notes
func (c Chord) Frequencies(octave int) []float64 {
	notes := c.NotesWithOctave(octave)
	freqs := make([]float64, len(notes))
	for i, note := range notes {
		freqs[i] = note.Frequency()
	}
	return freqs
}

// NewChord creates a new chord
func NewChord(root NoteName, chordType ChordType) Chord {
	return Chord{Root: root, Type: chordType}
}

// IdentifyChord attempts to identify a chord from a set of notes
func IdentifyChord(notes []NoteName) (Chord, error) {
	if len(notes) < 2 {
		return Chord{}, errors.New("need at least 2 notes to identify a chord")
	}
	
	// Normalize notes (remove duplicates, sort)
	noteSet := make(map[NoteName]bool)
	for _, n := range notes {
		noteSet[n] = true
	}
	uniqueNotes := make([]int, 0, len(noteSet))
	for n := range noteSet {
		uniqueNotes = append(uniqueNotes, int(n))
	}
	sort.Ints(uniqueNotes)
	
	// Try each root note
	for i, root := range uniqueNotes {
		// Calculate intervals from root
		intervals := make([]int, len(uniqueNotes))
		for j, note := range uniqueNotes {
			interval := note - root
			if interval < 0 {
				interval += 12
			}
			intervals[j] = interval
		}
		
		// Check against chord patterns
		for chordType, pattern := range chordPatterns {
			// Normalize pattern
			normalizedPattern := make([]int, len(pattern))
			for k, p := range pattern {
				normalizedPattern[k] = p % 12
			}
			sort.Ints(normalizedPattern)
			
			// Compare intervals
			if matchIntervals(intervals, normalizedPattern) {
				return Chord{Root: NoteName(root), Type: chordType}, nil
			}
		}
		
		_ = i // unused
	}
	
	return Chord{}, errors.New("could not identify chord")
}

// matchIntervals checks if two interval sets match
func matchIntervals(a, b []int) bool {
	if len(a) != len(b) {
		return false
	}
	for i := range a {
		if a[i] != b[i] {
			return false
		}
	}
	return true
}

// CircleOfFifths returns notes in the circle of fifths
func CircleOfFifths() []NoteName {
	return []NoteName{C, G, D, A, E, B, FSharp, CSharp, GSharp, DSharp, ASharp, F}
}

// CircleOfFourths returns notes in the circle of fourths
func CircleOfFourths() []NoteName {
	return []NoteName{C, F, ASharp, DSharp, GSharp, CSharp, FSharp, B, E, A, D, G}
}

// RelativeMinor returns the relative minor of a major key
func RelativeMinor(majorKey NoteName) NoteName {
	return NoteName((int(majorKey) + 9) % 12)
}

// RelativeMajor returns the relative major of a minor key
func RelativeMajor(minorKey NoteName) NoteName {
	return NoteName((int(minorKey) + 3) % 12)
}

// KeySignature represents a key signature
type KeySignature struct {
	Key         NoteName
	IsMajor     bool
	Accidentals []NoteName // Sharps or flats
}

// GetKeySignature returns the key signature for a given key
func GetKeySignature(key NoteName, isMajor bool) KeySignature {
	accidentals := make([]NoteName, 0)
	
	// Order of sharps: F#, C#, G#, D#, A#, E#, B#
	sharpsOrder := []NoteName{FSharp, CSharp, GSharp, DSharp, ASharp, F, C}
	// Order of flats: Bb, Eb, Ab, Db, Gb, Cb, Fb
	flatsOrder := []NoteName{ASharp, DSharp, GSharp, CSharp, FSharp, B, E}
	
	// Major keys with sharps: G, D, A, E, B, F#, C#
	// Major keys with flats: F, Bb, Eb, Ab, Db, Gb, Cb
	sharpKeys := []NoteName{G, D, A, E, B, FSharp, CSharp}
	flatKeys := []NoteName{F, ASharp, DSharp, GSharp, CSharp, FSharp, B}
	
	if isMajor {
		for i, k := range sharpKeys {
			if k == key {
				for j := 0; j <= i; j++ {
					accidentals = append(accidentals, sharpsOrder[j])
				}
				return KeySignature{Key: key, IsMajor: true, Accidentals: accidentals}
			}
		}
		for i, k := range flatKeys {
			if k == key {
				for j := 0; j <= i; j++ {
					accidentals = append(accidentals, flatsOrder[j])
				}
				return KeySignature{Key: key, IsMajor: true, Accidentals: accidentals}
			}
		}
	} else {
		// Minor keys
		relativeMajor := RelativeMajor(key)
		sig := GetKeySignature(relativeMajor, true)
		sig.Key = key
		sig.IsMajor = false
		return sig
	}
	
	return KeySignature{Key: key, IsMajor: isMajor, Accidentals: accidentals}
}

// Tempo marking constants
const (
	Larghissimo   = 24 // Very, very slow
	Grave         = 35 // Slow and solemn
	Largo         = 50 // Broad
	Lento         = 53 // Slow
	Adagio        = 71 // Slow and stately
	Andante       = 92 // Walking pace
	Moderato      = 114 // Moderate
	Allegretto    = 120 // Moderately fast
	Allegro       = 144 // Fast
	Vivace        = 168 // Lively
	Presto        = 200 // Very fast
	Prestissimo   = 208 // Extremely fast
)

// BPMtoMilliseconds converts beats per minute to milliseconds per beat
func BPMtoMilliseconds(bpm int) float64 {
	if bpm <= 0 {
		return 0
	}
	return 60000.0 / float64(bpm)
}

// BPMtoSeconds converts beats per minute to seconds per beat
func BPMtoSeconds(bpm int) float64 {
	if bpm <= 0 {
		return 0
	}
	return 60.0 / float64(bpm)
}

// MillisecondsToBPM converts milliseconds per beat to BPM
func MillisecondsToBPM(ms float64) int {
	if ms <= 0 {
		return 0
	}
	return int(math.Round(60000.0 / ms))
}

// SecondsToBPM converts seconds per beat to BPM
func SecondsToBPM(seconds float64) int {
	if seconds <= 0 {
		return 0
	}
	return int(math.Round(60.0 / seconds))
}

// NoteValue represents a note duration type
type NoteValue int

const (
	DoubleWholeNote NoteValue = iota
	WholeNote
	HalfNote
	QuarterNote
	EighthNote
	SixteenthNote
	ThirtySecondNote
	SixtyFourthNote
)

// Note value names
var noteValueNames = map[NoteValue]string{
	DoubleWholeNote:    "Double Whole Note",
	WholeNote:          "Whole Note",
	HalfNote:           "Half Note",
	QuarterNote:        "Quarter Note",
	EighthNote:         "Eighth Note",
	SixteenthNote:      "Sixteenth Note",
	ThirtySecondNote:   "Thirty-Second Note",
	SixtyFourthNote:    "Sixty-Fourth Note",
}

// String returns the note value name
func (n NoteValue) String() string {
	if name, ok := noteValueNames[n]; ok {
		return name
	}
	return "Unknown Note Value"
}

// Duration returns the duration of a note value in beats
func (n NoteValue) Duration() float64 {
	return math.Pow(2, float64(DoubleWholeNote-n))
}

// DurationMs returns the duration in milliseconds at a given BPM
func (n NoteValue) DurationMs(bpm int) float64 {
	quarterNoteMs := BPMtoMilliseconds(bpm)
	return quarterNoteMs * n.Duration() / QuarterNote.Duration()
}

// Note values with dots
func (n NoteValue) DurationWithDots(dots int) float64 {
	duration := n.Duration()
	for i := 0; i < dots; i++ {
		duration += duration / math.Pow(2, float64(i+1))
	}
	return duration
}

// TransposeByInterval transposes a note by a named interval
func TransposeByInterval(note Note, interval Interval) Note {
	return note.Transpose(interval.Semitones())
}

// HarmonicSeries returns the harmonic series for a fundamental frequency
func HarmonicSeries(fundamental float64, harmonics int) []float64 {
	series := make([]float64, harmonics)
	for i := 0; i < harmonics; i++ {
		series[i] = fundamental * float64(i+1)
	}
	return series
}

// EqualTemperamentFrequency returns the frequency of a note in equal temperament
// semitonesFromA4 is the number of semitones above or below A4 (440Hz)
func EqualTemperamentFrequency(semitonesFromA4 int) float64 {
	return 440.0 * math.Pow(2, float64(semitonesFromA4)/12.0)
}

// JustIntonationRatio represents a just intonation interval
type JustIntonationRatio struct {
	Numerator   int
	Denominator int
	Name        string
}

// Common just intonation ratios
var JustIntervals = map[string]JustIntonationRatio{
	"unison":      {1, 1, "Unison"},
	"minorSecond": {16, 15, "Minor Second"},
	"majorSecond": {9, 8, "Major Second"},
	"minorThird":  {6, 5, "Minor Third"},
	"majorThird":  {5, 4, "Major Third"},
	"fourth":      {4, 3, "Perfect Fourth"},
	"tritone":     {7, 5, "Tritone"},
	"fifth":       {3, 2, "Perfect Fifth"},
	"minorSixth":  {8, 5, "Minor Sixth"},
	"majorSixth":  {5, 3, "Major Sixth"},
	"minorSeventh": {7, 4, "Minor Seventh"},
	"majorSeventh": {15, 8, "Major Seventh"},
	"octave":      {2, 1, "Octave"},
}

// Frequency returns the frequency for a just intonation interval
func (j JustIntonationRatio) Frequency(fundamental float64) float64 {
	return fundamental * float64(j.Numerator) / float64(j.Denominator)
}

// Semitones returns the approximate semitone count (for comparison with equal temperament)
func (j JustIntonationRatio) Semitones() int {
	// Calculate approximate semitones: log2(ratio) * 12
	semitones := math.Log2(float64(j.Numerator)/float64(j.Denominator)) * 12
	return int(math.Round(semitones))
}

// Cents returns the cents deviation from equal temperament
func (j JustIntonationRatio) Cents() float64 {
	equalSemitones := math.Log2(float64(j.Numerator)/float64(j.Denominator)) * 12
	justSemitones := math.Log2(float64(j.Numerator)/float64(j.Denominator)) * 12
	return (justSemitones - equalSemitones) * 100
}

// BeatFrequency returns the beat frequency when two frequencies are played together
func BeatFrequency(freq1, freq2 float64) float64 {
	return math.Abs(freq1 - freq2)
}

// ResonantFrequency calculates resonant frequencies for a given length and wave speed
func ResonantFrequency(length, waveSpeed float64, mode int) float64 {
	return float64(mode) * waveSpeed / (2 * length)
}