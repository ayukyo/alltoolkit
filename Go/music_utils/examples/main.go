// Example usage of music_utils package
package main

import (
	"fmt"
	"math"

	music "github.com/ayukyo/alltoolkit/Go/music_utils"
)

func main() {
	fmt.Println("=== Music Utils Examples ===")
	fmt.Println()

	// 1. Note Frequency
	fmt.Println("1. Note Frequencies:")
	notes := []music.Note{
		{Name: music.C, Octave: 4},
		{Name: music.A, Octave: 4},
		{Name: music.G, Octave: 4},
	}
	for _, note := range notes {
		fmt.Printf("   %s: %.2f Hz (MIDI: %d)\n", note.String(), note.Frequency(), note.MIDI())
	}
	fmt.Println()

	// 2. Parse Note from string
	fmt.Println("2. Parsing Notes:")
	for _, str := range []string{"C4", "A#5", "Db3", "G#2"} {
		note, err := music.ParseNote(str)
		if err != nil {
			fmt.Printf("   %s: Error - %v\n", str, err)
		} else {
			fmt.Printf("   %s -> %s (%.2f Hz)\n", str, note.StringFlat(), note.Frequency())
		}
	}
	fmt.Println()

	// 3. Frequency to Note
	fmt.Println("3. Frequency to Note:")
	for _, freq := range []float64{440.0, 261.63, 880.0, 523.25} {
		note := music.FrequencyToNote(freq)
		cents := music.CentsDeviation(freq)
		fmt.Printf("   %.2f Hz -> %s (cents deviation: %d)\n", freq, note.String(), cents)
	}
	fmt.Println()

	// 4. Scales
	fmt.Println("4. Scales:")
	scales := []music.Scale{
		music.NewScale(music.C, music.MajorScale),
		music.NewScale(music.A, music.MinorScale),
		music.NewScale(music.E, music.PentatonicMinor),
		music.NewScale(music.C, music.BluesScale),
	}
	for _, scale := range scales {
		fmt.Printf("   %s: %v\n", scale.String(), scale.Notes())
	}
	fmt.Println()

	// 5. Scale Frequencies (C Major starting from C4)
	fmt.Println("5. C Major Scale Frequencies (C4):")
	cMajor := music.NewScale(music.C, music.MajorScale)
	freqs := cMajor.Frequencies(4, 1)
	noteNames := cMajor.Notes()
	for i, freq := range freqs {
		fmt.Printf("   %s%d: %.2f Hz\n", noteNames[i].String(), 4, freq)
	}
	fmt.Println()

	// 6. Chords
	fmt.Println("6. Chords:")
	chords := []music.Chord{
		music.NewChord(music.C, music.Major),
		music.NewChord(music.A, music.Minor),
		music.NewChord(music.G, music.DominantSeventh),
		music.NewChord(music.C, music.MajorSeventh),
		music.NewChord(music.D, music.Power),
	}
	for _, chord := range chords {
		fmt.Printf("   %s (%s): %v\n", chord.String(), chord.FullName(), chord.Notes())
	}
	fmt.Println()

	// 7. Chord Frequencies
	fmt.Println("7. C Major Chord Frequencies (C4):")
	cMajorChord := music.NewChord(music.C, music.Major)
	chordFreqs := cMajorChord.Frequencies(4)
	chordNotes := cMajorChord.Notes()
	for i, freq := range chordFreqs {
		fmt.Printf("   %s: %.2f Hz\n", chordNotes[i].String(), freq)
	}
	fmt.Println()

	// 8. Intervals
	fmt.Println("8. Intervals:")
	c4 := music.Note{Name: music.C, Octave: 4}
	intervals := []music.Note{
		{Name: music.D, Octave: 4},
		{Name: music.E, Octave: 4},
		{Name: music.G, Octave: 4},
		{Name: music.C, Octave: 5},
	}
	for _, target := range intervals {
		interval := music.GetInterval(c4, target)
		fmt.Printf("   C4 to %s: %s (%d semitones)\n", target.String(), interval.String(), interval.Semitones())
	}
	fmt.Println()

	// 9. Transposition
	fmt.Println("9. Transposition:")
	transpositions := []int{12, -12, 7, 5}
	for _, semitones := range transpositions {
		transposed := c4.Transpose(semitones)
		fmt.Printf("   C4 transposed by %d semitones: %s (%.2f Hz)\n", semitones, transposed.String(), transposed.Frequency())
	}
	fmt.Println()

	// 10. Circle of Fifths
	fmt.Println("10. Circle of Fifths:")
	cof := music.CircleOfFifths()
	fmt.Printf("   %v\n", cof)
	fmt.Println()

	// 11. Relative Keys
	fmt.Println("11. Relative Keys:")
	fmt.Printf("   Relative minor of C Major: %s\n", music.RelativeMinor(music.C).String())
	fmt.Printf("   Relative major of A Minor: %s\n", music.RelativeMajor(music.A).String())
	fmt.Println()

	// 12. BPM Calculations
	fmt.Println("12. BPM Calculations:")
	bpms := []int{60, 120, 140, 200}
	for _, bpm := range bpms {
		ms := music.BPMtoMilliseconds(bpm)
		sec := music.BPMtoSeconds(bpm)
		fmt.Printf("   %d BPM: %.2f ms/beat, %.3f sec/beat\n", bpm, ms, sec)
	}
	fmt.Println()

	// 13. Note Values
	fmt.Println("13. Note Values at 120 BPM:")
	noteValues := []music.NoteValue{
		music.WholeNote,
		music.HalfNote,
		music.QuarterNote,
		music.EighthNote,
		music.SixteenthNote,
	}
	for _, value := range noteValues {
		ms := value.DurationMs(120)
		fmt.Printf("   %v: %.2f ms (%.2f beats)\n", value, ms, value.Duration())
	}
	fmt.Println()

	// 14. Dotted Notes
	fmt.Println("14. Dotted Notes at 120 BPM:")
	fmt.Printf("   Quarter note: %.2f ms\n", music.QuarterNote.DurationMs(120))
	fmt.Printf("   Dotted quarter (1 dot): %.2f ms\n", music.QuarterNote.DurationWithDots(1)*500)
	fmt.Printf("   Double dotted quarter (2 dots): %.2f ms\n", music.QuarterNote.DurationWithDots(2)*500)
	fmt.Println()

	// 15. Chord Identification
	fmt.Println("15. Chord Identification:")
	chordInputs := [][]music.NoteName{
		{music.C, music.E, music.G},
		{music.A, music.C, music.E},
		{music.G, music.B, music.D},
	}
	for _, notes := range chordInputs {
		chord, err := music.IdentifyChord(notes)
		if err != nil {
			fmt.Printf("   %v: Could not identify\n", notes)
		} else {
			fmt.Printf("   %v -> %s (%s)\n", notes, chord.String(), chord.FullName())
		}
	}
	fmt.Println()

	// 16. Harmonic Series
	fmt.Println("16. Harmonic Series (A3 = 220 Hz, first 8 harmonics):")
	harmonics := music.HarmonicSeries(220.0, 8)
	for i, freq := range harmonics {
		note := music.FrequencyToNote(freq)
		fmt.Printf("   Harmonic %d: %.2f Hz (~%s)\n", i+1, freq, note.String())
	}
	fmt.Println()

	// 17. Beat Frequency
	fmt.Println("17. Beat Frequency:")
	fmt.Printf("   440 Hz + 442 Hz: %.2f Hz beat frequency\n", music.BeatFrequency(440.0, 442.0))
	fmt.Println()

	// 18. Just Intonation
	fmt.Println("18. Just Intonation (from A4 = 440 Hz):")
	for name, interval := range music.JustIntervals {
		freq := interval.Frequency(440.0)
		equalFreq := 440.0 * math.Pow(2, float64(interval.Semitones())/12.0)
		diff := freq - equalFreq
		fmt.Printf("   %s (%d/%d): %.2f Hz (equal temperament: %.2f Hz, diff: %.2f Hz)\n",
			name, interval.Numerator, interval.Denominator, freq, equalFreq, diff)
	}
	fmt.Println()

	// 19. Equal Temperament
	fmt.Println("19. Equal Temperament Frequencies (from A4):")
	for _, semitones := range []int{-12, -9, -5, -3, 0, 3, 5, 7, 12} {
		freq := music.EqualTemperamentFrequency(semitones)
		note := music.Note{Name: music.A, Octave: 4}.Transpose(semitones)
		fmt.Printf("   %+d semitones: %.2f Hz (%s)\n", semitones, freq, note.String())
	}
	fmt.Println()

	// 20. Scale Types
	fmt.Println("20. Available Scale Types:")
	scaleTypes := []music.ScaleType{
		music.MajorScale,
		music.MinorScale,
		music.HarmonicMinor,
		music.Dorian,
		music.Phrygian,
		music.Lydian,
		music.Mixolydian,
		music.Locrian,
		music.PentatonicMajor,
		music.PentatonicMinor,
		music.BluesScale,
		music.Chromatic,
		music.WholeTone,
	}
	for _, st := range scaleTypes {
		fmt.Printf("   %s\n", st.String())
	}
	fmt.Println()

	// 21. Modes (from C Major scale degrees)
	fmt.Println("21. Modes of C Major:")
	modes := []music.Scale{
		music.NewScale(music.C, music.MajorScale),    // Ionian (I)
		music.NewScale(music.D, music.Dorian),        // Dorian (II)
		music.NewScale(music.E, music.Phrygian),      // Phrygian (III)
		music.NewScale(music.F, music.Lydian),        // Lydian (IV)
		music.NewScale(music.G, music.Mixolydian),    // Mixolydian (V)
		music.NewScale(music.A, music.MinorScale),    // Aeolian (VI)
		music.NewScale(music.B, music.Locrian),       // Locrian (VII)
	}
	for _, mode := range modes {
		fmt.Printf("   %s: %v\n", mode.String(), mode.Notes())
	}
	fmt.Println()

	// 22. Chord Types
	fmt.Println("22. Available Chord Types:")
	chordTypes := []music.ChordType{
		music.Major,
		music.Minor,
		music.Diminished,
		music.Augmented,
		music.MajorSeventh,
		music.MinorSeventh,
		music.DominantSeventh,
		music.Power,
	}
	for _, ct := range chordTypes {
		chord := music.NewChord(music.C, ct)
		fmt.Printf("   %s (%s): %v\n", ct.Symbol(), ct.String(), chord.Notes())
	}
	fmt.Println()

	fmt.Println("=== End of Examples ===")
}