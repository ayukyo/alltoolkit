// Package huffman_utils provides comprehensive Huffman encoding and decoding utilities.
// Zero external dependencies - uses only Go standard library.
package huffman_utils

import (
	"bufio"
	"container/heap"
	"fmt"
	"io"
	"os"
	"sort"
	"strings"
)

// ==================== Core Types ====================

// HuffmanNode represents a node in the Huffman tree
type HuffmanNode struct {
	Char      byte         // Character (0 for internal nodes)
	Frequency int          // Frequency count
	Left      *HuffmanNode // Left child
	Right     *HuffmanNode // Right child
	Parent    *HuffmanNode // Parent node (for adaptive Huffman)
}

// IsLeaf returns true if the node is a leaf node
func (n *HuffmanNode) IsLeaf() bool {
	return n.Left == nil && n.Right == nil
}

// HuffmanTree represents a Huffman tree with encoding/decoding capabilities
type HuffmanTree struct {
	Root       *HuffmanNode
	CodeTable  map[byte]string // Character to code mapping
	CharTable  map[string]byte // Code to character mapping
	Frequencies map[byte]int   // Character frequencies
}

// HuffmanResult contains the result of Huffman encoding
type HuffmanResult struct {
	EncodedData  []byte         // Bit-packed encoded data
	OriginalSize int            // Original size in bytes
	EncodedSize  int            // Encoded size in bits
	CompressionRatio float64    // Compression ratio (original/encoded)
	CodeTable    map[byte]string // Huffman codes
	Frequencies  map[byte]int   // Character frequencies
	BitLength    int            // Total number of bits
}

// DecodeResult contains the result of Huffman decoding
type DecodeResult struct {
	Data         []byte         // Decoded data
	BitLength    int            // Number of bits decoded
	Success      bool           // Whether decoding was successful
}

// CanonicalHuffmanCode represents a canonical Huffman code entry
type CanonicalHuffmanCode struct {
	Char  byte
	Bits  int    // Number of bits
	Code  string // Canonical code
}

// BitWriter helps write individual bits to a byte slice
type BitWriter struct {
	data   []byte
	offset int // Current bit offset
}

// NewBitWriter creates a new BitWriter
func NewBitWriter() *BitWriter {
	return &BitWriter{
		data:   make([]byte, 0),
		offset: 0,
	}
}

// WriteBit writes a single bit
func (bw *BitWriter) WriteBit(bit byte) error {
	if bit > 1 {
		return fmt.Errorf("bit must be 0 or 1")
	}

	byteIndex := bw.offset / 8
	bitIndex := bw.offset % 8

	if byteIndex >= len(bw.data) {
		bw.data = append(bw.data, 0)
	}

	if bit == 1 {
		bw.data[byteIndex] |= (1 << (7 - bitIndex))
	}

	bw.offset++
	return nil
}

// WriteBits writes multiple bits from a string
func (bw *BitWriter) WriteBits(bits string) error {
	for _, bit := range bits {
		if bit == '0' {
			if err := bw.WriteBit(0); err != nil {
				return err
			}
		} else if bit == '1' {
			if err := bw.WriteBit(1); err != nil {
				return err
			}
		} else {
			return fmt.Errorf("invalid bit character: %c", bit)
		}
	}
	return nil
}

// Bytes returns the written bytes
func (bw *BitWriter) Bytes() []byte {
	return bw.data
}

// BitCount returns the total number of bits written
func (bw *BitWriter) BitCount() int {
	return bw.offset
}

// BitReader helps read individual bits from a byte slice
type BitReader struct {
	data   []byte
	offset int // Current bit offset
}

// NewBitReader creates a new BitReader
func NewBitReader(data []byte) *BitReader {
	return &BitReader{
		data:   data,
		offset: 0,
	}
}

// ReadBit reads a single bit
func (br *BitReader) ReadBit() (byte, error) {
	if br.offset >= len(br.data)*8 {
		return 0, io.EOF
	}

	byteIndex := br.offset / 8
	bitIndex := br.offset % 8

	bit := (br.data[byteIndex] >> (7 - bitIndex)) & 1
	br.offset++

	return bit, nil
}

// ReadBits reads n bits and returns as string
func (br *BitReader) ReadBits(n int) (string, error) {
	var result strings.Builder
	for i := 0; i < n; i++ {
		bit, err := br.ReadBit()
		if err != nil {
			return result.String(), err
		}
		result.WriteByte('0' + bit)
	}
	return result.String(), nil
}

// HasMore returns true if there are more bits to read
func (br *BitReader) HasMore() bool {
	return br.offset < len(br.data)*8
}

// BitCount returns the total number of bits read
func (br *BitReader) BitCount() int {
	return br.offset
}

// ==================== Frequency Analysis ====================

// CountFrequencies counts the frequency of each byte in the data
func CountFrequencies(data []byte) map[byte]int {
	freq := make(map[byte]int)
	for _, b := range data {
		freq[b]++
	}
	return freq
}

// CountFrequenciesFromString counts frequency of each character in a string
func CountFrequenciesFromString(s string) map[byte]int {
	return CountFrequencies([]byte(s))
}

// CountRuneFrequencies counts frequency of each rune (for UTF-8 strings)
func CountRuneFrequencies(s string) map[rune]int {
	freq := make(map[rune]int)
	for _, r := range s {
		freq[r]++
	}
	return freq
}

// GetTopFrequencies returns the top n most frequent bytes
func GetTopFrequencies(freq map[byte]int, n int) []struct {
	Char  byte
	Count int
} {
	type charCount struct {
		Char  byte
		Count int
	}

	var list []charCount
	for c, count := range freq {
		list = append(list, charCount{c, count})
	}

	sort.Slice(list, func(i, j int) bool {
		return list[i].Count > list[j].Count
	})

	if n > len(list) {
		n = len(list)
	}

	result := make([]struct {
		Char  byte
		Count int
	}, n)
	for i := 0; i < n; i++ {
		result[i].Char = list[i].Char
		result[i].Count = list[i].Count
	}

	return result
}

// ==================== Huffman Tree Building ====================

// NodeHeap implements heap.Interface for Huffman nodes
type NodeHeap []*HuffmanNode

func (h NodeHeap) Len() int { return len(h) }
func (h NodeHeap) Less(i, j int) bool {
	// First compare by frequency
	if h[i].Frequency != h[j].Frequency {
		return h[i].Frequency < h[j].Frequency
	}
	// If frequencies are equal, compare by character value for consistency
	// Internal nodes have Char = 0, leaf nodes have non-zero Char
	// Prefer leaf nodes before internal nodes (leaf has non-zero char)
	if h[i].Char != h[j].Char {
		return h[i].Char < h[j].Char
	}
	// If both are internal nodes, use depth or position as tiebreaker
	// This ensures consistent ordering
	return i < j
}
func (h NodeHeap) Swap(i, j int) { h[i], h[j] = h[j], h[i] }

func (h *NodeHeap) Push(x interface{}) {
	*h = append(*h, x.(*HuffmanNode))
}

func (h *NodeHeap) Pop() interface{} {
	old := *h
	n := len(old)
	x := old[n-1]
	*h = old[0 : n-1]
	return x
}

// BuildTree builds a Huffman tree from frequency data
func BuildTree(frequencies map[byte]int) *HuffmanTree {
	if len(frequencies) == 0 {
		return &HuffmanTree{
			Root:       nil,
			CodeTable:  make(map[byte]string),
			CharTable:  make(map[string]byte),
			Frequencies: make(map[byte]int),
		}
	}

	// Handle single character case
	if len(frequencies) == 1 {
		for char, freq := range frequencies {
			return &HuffmanTree{
				Root: &HuffmanNode{
					Char:      char,
					Frequency: freq,
				},
				CodeTable:  map[byte]string{char: "0"},
				CharTable:  map[string]byte{"0": char},
				Frequencies: frequencies,
			}
		}
	}

	// Create heap
	h := &NodeHeap{}
	heap.Init(h)

	for char, freq := range frequencies {
		heap.Push(h, &HuffmanNode{
			Char:      char,
			Frequency: freq,
		})
	}

	// Build tree
	for h.Len() > 1 {
		left := heap.Pop(h).(*HuffmanNode)
		right := heap.Pop(h).(*HuffmanNode)

		parent := &HuffmanNode{
			Frequency: left.Frequency + right.Frequency,
			Left:      left,
			Right:     right,
		}
		left.Parent = parent
		right.Parent = parent

		heap.Push(h, parent)
	}

	root := heap.Pop(h).(*HuffmanNode)

	// Build code tables
	codeTable := make(map[byte]string)
	charTable := make(map[string]byte)
	buildCodeTable(root, "", codeTable, charTable)

	return &HuffmanTree{
		Root:       root,
		CodeTable:  codeTable,
		CharTable:  charTable,
		Frequencies: frequencies,
	}
}

// buildCodeTable recursively builds the code table
func buildCodeTable(node *HuffmanNode, code string, codeTable map[byte]string, charTable map[string]byte) {
	if node == nil {
		return
	}

	if node.IsLeaf() {
		if code == "" {
			code = "0" // Single node case
		}
		codeTable[node.Char] = code
		charTable[code] = node.Char
		return
	}

	buildCodeTable(node.Left, code+"0", codeTable, charTable)
	buildCodeTable(node.Right, code+"1", codeTable, charTable)
}

// BuildTreeFromData builds a Huffman tree directly from data
func BuildTreeFromData(data []byte) *HuffmanTree {
	freq := CountFrequencies(data)
	return BuildTree(freq)
}

// ==================== Encoding ====================

// Encode encodes data using Huffman coding
func Encode(data []byte) *HuffmanResult {
	if len(data) == 0 {
		return &HuffmanResult{
			EncodedData:    []byte{},
			OriginalSize:   0,
			EncodedSize:    0,
			CompressionRatio: 0,
			CodeTable:      make(map[byte]string),
			Frequencies:    make(map[byte]int),
			BitLength:      0,
		}
	}

	freq := CountFrequencies(data)
	tree := BuildTree(freq)

	bw := NewBitWriter()
	for _, b := range data {
		code := tree.CodeTable[b]
		if err := bw.WriteBits(code); err != nil {
			return nil
		}
	}

	encodedData := bw.Bytes()
	bitLength := bw.BitCount()
	encodedSize := len(encodedData)

	var compressionRatio float64
	if encodedSize > 0 {
		compressionRatio = float64(len(data)) / float64(encodedSize)
	}

	return &HuffmanResult{
		EncodedData:    encodedData,
		OriginalSize:   len(data),
		EncodedSize:    encodedSize,
		CompressionRatio: compressionRatio,
		CodeTable:      tree.CodeTable,
		Frequencies:    freq,
		BitLength:      bitLength,
	}
}

// EncodeString encodes a string using Huffman coding
func EncodeString(s string) *HuffmanResult {
	return Encode([]byte(s))
}

// EncodeWithTree encodes data using an existing Huffman tree
func EncodeWithTree(data []byte, tree *HuffmanTree) *HuffmanResult {
	if len(data) == 0 || tree == nil {
		return &HuffmanResult{
			EncodedData:    []byte{},
			OriginalSize:   0,
			EncodedSize:    0,
			CompressionRatio: 0,
			CodeTable:      tree.CodeTable,
			Frequencies:    tree.Frequencies,
			BitLength:      0,
		}
	}

	bw := NewBitWriter()
	for _, b := range data {
		code := tree.CodeTable[b]
		if code == "" {
			return nil // Character not in tree
		}
		if err := bw.WriteBits(code); err != nil {
			return nil
		}
	}

	encodedData := bw.Bytes()
	bitLength := bw.BitCount()
	encodedSize := len(encodedData)

	var compressionRatio float64
	if encodedSize > 0 {
		compressionRatio = float64(len(data)) / float64(encodedSize)
	}

	return &HuffmanResult{
		EncodedData:    encodedData,
		OriginalSize:   len(data),
		EncodedSize:    encodedSize,
		CompressionRatio: compressionRatio,
		CodeTable:      tree.CodeTable,
		Frequencies:    tree.Frequencies,
		BitLength:      bitLength,
	}
}

// ==================== Decoding ====================

// Decode decodes Huffman encoded data
func Decode(encodedData []byte, tree *HuffmanTree, bitLength int) *DecodeResult {
	if tree == nil || tree.Root == nil {
		return &DecodeResult{
			Data:      []byte{},
			BitLength: 0,
			Success:   len(encodedData) == 0,
		}
	}

	br := NewBitReader(encodedData)
	var result []byte

	current := tree.Root

	for i := 0; i < bitLength; i++ {
		bit, err := br.ReadBit()
		if err != nil {
			return &DecodeResult{
				Data:      result,
				BitLength: i,
				Success:   false,
			}
		}

		if bit == 0 {
			current = current.Left
		} else {
			current = current.Right
		}

		if current == nil {
			return &DecodeResult{
				Data:      result,
				BitLength: i,
				Success:   false,
			}
		}

		if current.IsLeaf() {
			result = append(result, current.Char)
			current = tree.Root
		}
	}

	return &DecodeResult{
		Data:      result,
		BitLength: bitLength,
		Success:   true,
	}
}

// DecodeString decodes Huffman encoded data to string
func DecodeString(encodedData []byte, tree *HuffmanTree, bitLength int) (string, bool) {
	result := Decode(encodedData, tree, bitLength)
	return string(result.Data), result.Success
}

// DecodeWithTable decodes using code-to-char table
func DecodeWithTable(encodedData []byte, charTable map[string]byte, bitLength int) *DecodeResult {
	if len(charTable) == 0 {
		return &DecodeResult{
			Data:      []byte{},
			BitLength: 0,
			Success:   len(encodedData) == 0,
		}
	}

	br := NewBitReader(encodedData)
	var result []byte
	var currentCode strings.Builder

	for i := 0; i < bitLength; i++ {
		bit, err := br.ReadBit()
		if err != nil {
			return &DecodeResult{
				Data:      result,
				BitLength: i,
				Success:   false,
			}
		}

		currentCode.WriteByte('0' + bit)
		code := currentCode.String()

		if char, exists := charTable[code]; exists {
			result = append(result, char)
			currentCode.Reset()
		}
	}

	return &DecodeResult{
		Data:      result,
		BitLength: bitLength,
		Success:   true,
	}
}

// ==================== Canonical Huffman ====================

// BuildCanonicalCodes builds canonical Huffman codes from code lengths
func BuildCanonicalCodes(charLengths map[byte]int) map[byte]string {
	if len(charLengths) == 0 {
		return make(map[byte]string)
	}

	// Create list of (char, length) pairs
	type charLen struct {
		char   byte
		length int
	}

	var list []charLen
	for c, l := range charLengths {
		list = append(list, charLen{c, l})
	}

	// Sort by length, then by character value
	sort.Slice(list, func(i, j int) bool {
		if list[i].length != list[j].length {
			return list[i].length < list[j].length
		}
		return list[i].char < list[j].char
	})

	// Generate canonical codes
	codes := make(map[byte]string)
	code := 0
	prevLength := 0

	for _, cl := range list {
		code <<= (cl.length - prevLength)
		codes[cl.char] = padLeft(fmt.Sprintf("%b", code), cl.length)
		code++
		prevLength = cl.length
	}

	return codes
}

// padLeft pads a binary string with leading zeros
func padLeft(s string, length int) string {
	for len(s) < length {
		s = "0" + s
	}
	return s
}

// GetCodeLengths returns code lengths for each character
func GetCodeLengths(tree *HuffmanTree) map[byte]int {
	lengths := make(map[byte]int)
	for char, code := range tree.CodeTable {
		lengths[char] = len(code)
	}
	return lengths
}

// BuildCanonicalTree builds a Huffman tree using canonical codes
func BuildCanonicalTree(codeLengths map[byte]int) *HuffmanTree {
	codes := BuildCanonicalCodes(codeLengths)

	root := &HuffmanNode{}
	charTable := make(map[string]byte)

	for char, code := range codes {
		current := root
		for i, bit := range code {
			if bit == '0' {
				if current.Left == nil {
					current.Left = &HuffmanNode{Parent: current}
				}
				current = current.Left
			} else {
				if current.Right == nil {
					current.Right = &HuffmanNode{Parent: current}
				}
				current = current.Right
			}

			if i == len(code)-1 {
				current.Char = char
			}
		}
		charTable[code] = char
	}

	return &HuffmanTree{
		Root:       root,
		CodeTable:  codes,
		CharTable:  charTable,
		Frequencies: make(map[byte]int),
	}
}

// ==================== Utility Functions ====================

// CalculateEntropy calculates the Shannon entropy of the data
func CalculateEntropy(frequencies map[byte]int, total int) float64 {
	if total == 0 {
		return 0
	}

	var entropy float64
	for _, count := range frequencies {
		if count > 0 {
			p := float64(count) / float64(total)
			entropy -= p * log2(p)
		}
	}
	return entropy
}

// CalculateExpectedCodeLength calculates the expected code length
func CalculateExpectedCodeLength(tree *HuffmanTree, frequencies map[byte]int) float64 {
	if tree == nil || len(frequencies) == 0 {
		return 0
	}

	total := 0
	for _, count := range frequencies {
		total += count
	}

	var expected float64
	for char, code := range tree.CodeTable {
		expected += float64(frequencies[char]) / float64(total) * float64(len(code))
	}

	return expected
}

// CalculateEfficiency calculates the encoding efficiency (entropy / expected length)
func CalculateEfficiency(tree *HuffmanTree, frequencies map[byte]int) float64 {
	if tree == nil || len(frequencies) == 0 {
		return 0
	}

	total := 0
	for _, count := range frequencies {
		total += count
	}

	entropy := CalculateEntropy(frequencies, total)
	expected := CalculateExpectedCodeLength(tree, frequencies)

	if expected == 0 {
		return 0
	}

	return entropy / expected
}

// GetAverageCodeLength returns the average code length
func GetAverageCodeLength(tree *HuffmanTree) float64 {
	if tree == nil || len(tree.CodeTable) == 0 {
		return 0
	}

	var total float64
	var count float64
	for _, code := range tree.CodeTable {
		total += float64(len(code))
		count++
	}

	if count == 0 {
		return 0
	}
	return total / count
}

// GetMaxCodeLength returns the maximum code length
func GetMaxCodeLength(tree *HuffmanTree) int {
	if tree == nil {
		return 0
	}

	maxLen := 0
	for _, code := range tree.CodeTable {
		if len(code) > maxLen {
			maxLen = len(code)
		}
	}
	return maxLen
}

// GetMinCodeLength returns the minimum code length
func GetMinCodeLength(tree *HuffmanTree) int {
	if tree == nil || len(tree.CodeTable) == 0 {
		return 0
	}

	minLen := int(^uint(0) >> 31) // Max int
	for _, code := range tree.CodeTable {
		if len(code) < minLen {
			minLen = len(code)
		}
	}
	return minLen
}

// CountDistinctCharacters returns the number of distinct characters
func CountDistinctCharacters(data []byte) int {
	seen := make(map[byte]bool)
	for _, b := range data {
		seen[b] = true
	}
	return len(seen)
}

// ==================== Serialization ====================

// SerializeTree serializes a Huffman tree to bytes
func SerializeTree(tree *HuffmanTree) []byte {
	if tree == nil {
		return []byte{}
	}

	// Format: [num_chars:2][char:1][code_len:1][code:N]...
	var result []byte

	// Write number of characters
	numChars := len(tree.CodeTable)
	result = append(result, byte(numChars>>8), byte(numChars))

	// Write each character and its code
	for char, code := range tree.CodeTable {
		result = append(result, char)
		result = append(result, byte(len(code)))
		result = append(result, []byte(code)...)
	}

	return result
}

// DeserializeTree deserializes a Huffman tree from bytes
func DeserializeTree(data []byte) (*HuffmanTree, error) {
	if len(data) < 2 {
		return nil, fmt.Errorf("invalid tree data: too short")
	}

	numChars := int(data[0])<<8 | int(data[1])
	offset := 2

	codeTable := make(map[byte]string)
	charTable := make(map[string]byte)

	for i := 0; i < numChars; i++ {
		if offset >= len(data) {
			return nil, fmt.Errorf("invalid tree data: unexpected end")
		}

		char := data[offset]
		offset++

		if offset >= len(data) {
			return nil, fmt.Errorf("invalid tree data: missing code length")
		}

		codeLen := int(data[offset])
		offset++

		if offset+codeLen > len(data) {
			return nil, fmt.Errorf("invalid tree data: code data too short")
		}

		code := string(data[offset : offset+codeLen])
		offset += codeLen

		codeTable[char] = code
		charTable[code] = char
	}

	// Rebuild tree from code table
	root := &HuffmanNode{}
	for char, code := range codeTable {
		current := root
		for i, bit := range code {
			if bit == '0' {
				if current.Left == nil {
					current.Left = &HuffmanNode{Parent: current}
				}
				current = current.Left
			} else {
				if current.Right == nil {
					current.Right = &HuffmanNode{Parent: current}
				}
				current = current.Right
			}

			if i == len(code)-1 {
				current.Char = char
			}
		}
	}

	return &HuffmanTree{
		Root:       root,
		CodeTable:  codeTable,
		CharTable:  charTable,
		Frequencies: make(map[byte]int),
	}, nil
}

// SerializeEncodedData serializes encoded data with tree
func SerializeEncodedData(result *HuffmanResult) []byte {
	if result == nil {
		return []byte{}
	}

	treeData := SerializeTree(&HuffmanTree{CodeTable: result.CodeTable})

	// Format: [tree_len:4][tree_data][bit_length:4][encoded_data]
	var data []byte

	// Tree length (4 bytes)
	treeLen := len(treeData)
	data = append(data, byte(treeLen>>24), byte(treeLen>>16), byte(treeLen>>8), byte(treeLen))

	// Tree data
	data = append(data, treeData...)

	// Bit length (4 bytes)
	bitLen := result.BitLength
	data = append(data, byte(bitLen>>24), byte(bitLen>>16), byte(bitLen>>8), byte(bitLen))

	// Encoded data
	data = append(data, result.EncodedData...)

	return data
}

// DeserializeEncodedData deserializes encoded data with tree
func DeserializeEncodedData(data []byte) (*HuffmanResult, error) {
	if len(data) < 8 {
		return nil, fmt.Errorf("invalid data: too short")
	}

	// Read tree length
	treeLen := int(data[0])<<24 | int(data[1])<<16 | int(data[2])<<8 | int(data[3])
	offset := 4

	if offset+treeLen > len(data) {
		return nil, fmt.Errorf("invalid data: tree data too short")
	}

	// Read tree data
	treeData := data[offset : offset+treeLen]
	offset += treeLen

	tree, err := DeserializeTree(treeData)
	if err != nil {
		return nil, err
	}

	// Read bit length
	if offset+4 > len(data) {
		return nil, fmt.Errorf("invalid data: missing bit length")
	}
	bitLen := int(data[offset])<<24 | int(data[offset+1])<<16 | int(data[offset+2])<<8 | int(data[offset+3])
	offset += 4

	// Read encoded data
	encodedData := data[offset:]

	return &HuffmanResult{
		EncodedData:    encodedData,
		OriginalSize:   0, // Unknown without decoding
		EncodedSize:    len(encodedData),
		CompressionRatio: 0,
		CodeTable:      tree.CodeTable,
		Frequencies:    tree.Frequencies,
		BitLength:      bitLen,
	}, nil
}

// ==================== File Operations ====================

// EncodeFile encodes a file using Huffman coding
func EncodeFile(inputPath, outputPath string) (*HuffmanResult, error) {
	data, err := os.ReadFile(inputPath)
	if err != nil {
		return nil, err
	}

	result := Encode(data)
	if result == nil {
		return nil, fmt.Errorf("encoding failed")
	}

	serialized := SerializeEncodedData(result)
	err = os.WriteFile(outputPath, serialized, 0644)
	if err != nil {
		return nil, err
	}

	return result, nil
}

// DecodeFile decodes a Huffman encoded file
func DecodeFile(inputPath, outputPath string) (*DecodeResult, error) {
	data, err := os.ReadFile(inputPath)
	if err != nil {
		return nil, err
	}

	result, err := DeserializeEncodedData(data)
	if err != nil {
		return nil, err
	}

	tree := &HuffmanTree{
		CodeTable: result.CodeTable,
		CharTable: make(map[string]byte),
	}
	for char, code := range result.CodeTable {
		tree.CharTable[code] = char
	}

	decodeResult := Decode(result.EncodedData, tree, result.BitLength)
	if !decodeResult.Success {
		return nil, fmt.Errorf("decoding failed")
	}

	err = os.WriteFile(outputPath, decodeResult.Data, 0644)
	if err != nil {
		return nil, err
	}

	return decodeResult, nil
}

// ==================== Streaming ====================

// HuffmanEncoder provides streaming encoding
type HuffmanEncoder struct {
	tree   *HuffmanTree
	writer *BitWriter
}

// NewEncoder creates a new streaming encoder
func NewEncoder(frequencies map[byte]int) *HuffmanEncoder {
	tree := BuildTree(frequencies)
	return &HuffmanEncoder{
		tree:   tree,
		writer: NewBitWriter(),
	}
}

// Write encodes and writes a byte
func (e *HuffmanEncoder) Write(b byte) error {
	code := e.tree.CodeTable[b]
	if code == "" {
		return fmt.Errorf("character not in tree: %d", b)
	}
	return e.writer.WriteBits(code)
}

// WriteBytes encodes and writes multiple bytes
func (e *HuffmanEncoder) WriteBytes(data []byte) error {
	for _, b := range data {
		if err := e.Write(b); err != nil {
			return err
		}
	}
	return nil
}

// GetResult returns the encoding result
func (e *HuffmanEncoder) GetResult() *HuffmanResult {
	return &HuffmanResult{
		EncodedData:  e.writer.Bytes(),
		EncodedSize:  len(e.writer.Bytes()),
		CodeTable:    e.tree.CodeTable,
		Frequencies:  e.tree.Frequencies,
		BitLength:    e.writer.BitCount(),
	}
}

// GetTree returns the Huffman tree
func (e *HuffmanEncoder) GetTree() *HuffmanTree {
	return e.tree
}

// HuffmanDecoder provides streaming decoding
type HuffmanDecoder struct {
	tree    *HuffmanTree
	reader  *BitReader
	current *HuffmanNode
	maxBits int    // Maximum bits to read (optional)
}

// NewDecoder creates a new streaming decoder
func NewDecoder(tree *HuffmanTree, data []byte) *HuffmanDecoder {
	return &HuffmanDecoder{
		tree:    tree,
		reader:  NewBitReader(data),
		current: tree.Root,
		maxBits: len(data) * 8, // Default to all bits
	}
}

// NewDecoderWithBitLimit creates a decoder with a specific bit limit
func NewDecoderWithBitLimit(tree *HuffmanTree, data []byte, bitLength int) *HuffmanDecoder {
	return &HuffmanDecoder{
		tree:    tree,
		reader:  NewBitReader(data),
		current: tree.Root,
		maxBits: bitLength,
	}
}

// Read decodes and reads a byte
func (d *HuffmanDecoder) Read() (byte, error) {
	for {
		if d.reader.BitCount() >= d.maxBits {
			return 0, io.EOF
		}

		bit, err := d.reader.ReadBit()
		if err != nil {
			return 0, err
		}

		if bit == 0 {
			d.current = d.current.Left
		} else {
			d.current = d.current.Right
		}

		if d.current == nil {
			return 0, fmt.Errorf("invalid bit sequence")
		}

		if d.current.IsLeaf() {
			char := d.current.Char
			d.current = d.tree.Root
			return char, nil
		}
	}
}

// ReadAll decodes and reads all bytes
func (d *HuffmanDecoder) ReadAll() ([]byte, error) {
	var result []byte
	for d.reader.BitCount() < d.maxBits {
		b, err := d.Read()
		if err != nil {
			if err == io.EOF {
				break
			}
			return result, err
		}
		result = append(result, b)
	}
	return result, nil
}

// ==================== Additional Utilities ====================

// CompareHuffmanCodes compares two Huffman code tables
func CompareHuffmanCodes(t1, t2 *HuffmanTree) bool {
	if len(t1.CodeTable) != len(t2.CodeTable) {
		return false
	}
	for char, code := range t1.CodeTable {
		if t2.CodeTable[char] != code {
			return false
		}
	}
	return true
}

// MergeFrequencyTables merges multiple frequency tables
func MergeFrequencyTables(tables ...map[byte]int) map[byte]int {
	result := make(map[byte]int)
	for _, table := range tables {
		for char, count := range table {
			result[char] += count
		}
	}
	return result
}

// GetCodeTableStats returns statistics about a code table
func GetCodeTableStats(codeTable map[byte]string) struct {
	MinLength   int
	MaxLength   int
	AvgLength   float64
	TotalCodes  int
	LengthCount map[int]int
} {
	stats := struct {
		MinLength   int
		MaxLength   int
		AvgLength   float64
		TotalCodes  int
		LengthCount map[int]int
	}{
		MinLength:   int(^uint(0) >> 31),
		MaxLength:   0,
		TotalCodes:  len(codeTable),
		LengthCount: make(map[int]int),
	}

	var totalLen float64
	for _, code := range codeTable {
		len := len(code)
		totalLen += float64(len)

		if len < stats.MinLength {
			stats.MinLength = len
		}
		if len > stats.MaxLength {
			stats.MaxLength = len
		}
		stats.LengthCount[len]++
	}

	if stats.TotalCodes > 0 {
		stats.AvgLength = totalLen / float64(stats.TotalCodes)
	} else {
		stats.MinLength = 0
	}

	return stats
}

// PrintTree prints the Huffman tree structure
func PrintTree(node *HuffmanNode, indent string, isLeft bool) string {
	if node == nil {
		return ""
	}

	var result string
	result += indent

	if isLeft {
		result += "├── "
	} else {
		result += "└── "
	}

	if node.IsLeaf() {
		result += fmt.Sprintf("'%c' (%d)\n", node.Char, node.Frequency)
	} else {
		result += fmt.Sprintf("* (%d)\n", node.Frequency)
	}

	if node.Left != nil {
		result += PrintTree(node.Left, indent+func() string {
			if isLeft {
				return "│   "
			}
			return "    "
		}(), true)
	}
	if node.Right != nil {
		result += PrintTree(node.Right, indent+func() string {
			if isLeft {
				return "│   "
			}
			return "    "
		}(), false)
	}

	return result
}

// ValidateTree validates a Huffman tree structure
func ValidateTree(node *HuffmanNode) error {
	if node == nil {
		return nil
	}

	// Check: leaf nodes have characters, internal nodes don't
	if node.IsLeaf() {
		if node.Left != nil || node.Right != nil {
			return fmt.Errorf("leaf node should not have children")
		}
	} else {
		if node.Left == nil || node.Right == nil {
			return fmt.Errorf("internal node must have both children")
		}
		if node.Char != 0 {
			return fmt.Errorf("internal node should not have a character")
		}
	}

	// Check: frequency is sum of children
	if !node.IsLeaf() {
		expectedFreq := node.Left.Frequency + node.Right.Frequency
		if node.Frequency != expectedFreq {
			return fmt.Errorf("frequency mismatch: got %d, expected %d", node.Frequency, expectedFreq)
		}
	}

	// Recursively validate children
	if err := ValidateTree(node.Left); err != nil {
		return err
	}
	if err := ValidateTree(node.Right); err != nil {
		return err
	}

	return nil
}

// Helper function
func log2(x float64) float64 {
	if x <= 0 {
		return 0
	}
	const ln2 = 0.693147180559945309417
	return float64(float64(internalLog(x)) / ln2)
}

func internalLog(x float64) float64 {
	if x <= 0 {
		return 0
	}
	// Using math.Log equivalent
	var result float64 = 0
	for x > 2 {
		x /= 2
		result += ln2
	}
	for x < 1 {
		x *= 2
		result -= ln2
	}

	// Taylor series for ln(1+x)
	x -= 1
	for i := 1; i <= 20; i++ {
		term := x
		for j := 1; j < i; j++ {
			term *= x
		}
		if i%2 == 1 {
			result += term / float64(i)
		} else {
			result -= term / float64(i)
		}
	}

	return result
}

const ln2 = 0.693147180559945309417

// ==================== Adaptive Huffman (FGK Algorithm) ====================

// AdaptiveHuffmanEncoder implements adaptive Huffman coding (FGK algorithm)
type AdaptiveHuffmanEncoder struct {
	root    *HuffmanNode
	nodes   map[byte]*HuffmanNode
	nytNode *HuffmanNode // Not Yet Transmitted node
	counter int           // Node numbering for sibling property
}

// NewAdaptiveEncoder creates a new adaptive Huffman encoder
func NewAdaptiveEncoder() *AdaptiveHuffmanEncoder {
	nyt := &HuffmanNode{
		Char:      0,
		Frequency: 0,
	}
	return &AdaptiveHuffmanEncoder{
		root:    nyt,
		nytNode: nyt,
		nodes:   make(map[byte]*HuffmanNode),
		counter: 1,
	}
}

// EncodeByte encodes a single byte adaptively
func (a *AdaptiveHuffmanEncoder) EncodeByte(b byte) (string, bool) {
	// Check if character has been seen before
	if node, exists := a.nodes[b]; exists {
		// Get code before updating
		code := a.getNodeCode(node)
		// Update tree
		a.updateTree(node)
		return code, false // Not first occurrence
	}

	// First occurrence - emit NYT code + character
	nytCode := a.getNodeCode(a.nytNode)

	// Create new node for this character
	newNode := &HuffmanNode{
		Char:      b,
		Frequency: 1,
	}

	// Create new internal node
	newInternal := &HuffmanNode{
		Frequency: 1,
		Left:      a.nytNode,
		Right:     newNode,
	}

	// Update parent relationships
	if a.nytNode.Parent != nil {
		if a.nytNode.Parent.Left == a.nytNode {
			a.nytNode.Parent.Left = newInternal
		} else {
			a.nytNode.Parent.Right = newInternal
		}
		newInternal.Parent = a.nytNode.Parent
	} else {
		a.root = newInternal
	}

	a.nytNode.Parent = newInternal
	newNode.Parent = newInternal

	// Record the new character node
	a.nodes[b] = newNode

	// Update frequencies up the tree
	a.updateFrequencies(newInternal.Parent)

	return nytCode + fmt.Sprintf("%08b", b), true // First occurrence
}

// getNodeCode gets the code for a node
func (a *AdaptiveHuffmanEncoder) getNodeCode(node *HuffmanNode) string {
	var code string
	current := node
	for current.Parent != nil {
		if current.Parent.Left == current {
			code = "0" + code
		} else {
			code = "1" + code
		}
		current = current.Parent
	}
	return code
}

// updateTree updates the tree after incrementing frequency
func (a *AdaptiveHuffmanEncoder) updateTree(node *HuffmanNode) {
	for node != nil {
		node.Frequency++
		node = node.Parent
	}
}

// updateFrequencies updates frequencies up the tree
func (a *AdaptiveHuffmanEncoder) updateFrequencies(node *HuffmanNode) {
	for node != nil {
		node.Frequency = node.Left.Frequency + node.Right.Frequency
		node = node.Parent
	}
}

// ==================== Convenience Functions ====================

// QuickEncode provides a simple way to encode data
func QuickEncode(data []byte) ([]byte, map[byte]string) {
	result := Encode(data)
	return result.EncodedData, result.CodeTable
}

// QuickDecode provides a simple way to decode data
func QuickDecode(encodedData []byte, codeTable map[byte]string, bitLength int) ([]byte, bool) {
	charTable := make(map[string]byte)
	for char, code := range codeTable {
		charTable[code] = char
	}
	result := DecodeWithTable(encodedData, charTable, bitLength)
	return result.Data, result.Success
}

// GetCompressionStats returns compression statistics
func GetCompressionStats(original, encoded []byte, bitLength int) struct {
	OriginalSize    int
	EncodedSize     int
	BitLength       int
	CompressionRatio float64
	SpaceSaved      float64
} {
	originalSize := len(original)
	encodedSize := len(encoded)

	var compressionRatio, spaceSaved float64
	if encodedSize > 0 {
		compressionRatio = float64(originalSize) / float64(encodedSize)
	}
	if originalSize > 0 {
		spaceSaved = float64(originalSize*8-bitLength) / float64(originalSize*8) * 100
	}

	return struct {
		OriginalSize    int
		EncodedSize     int
		BitLength       int
		CompressionRatio float64
		SpaceSaved      float64
	}{
		OriginalSize:    originalSize,
		EncodedSize:     encodedSize,
		BitLength:       bitLength,
		CompressionRatio: compressionRatio,
		SpaceSaved:      spaceSaved,
	}
}

// WriteEncodedFile writes encoded data to file with header
func WriteEncodedFile(path string, result *HuffmanResult) error {
	data := SerializeEncodedData(result)
	return os.WriteFile(path, data, 0644)
}

// ReadEncodedFile reads encoded data from file
func ReadEncodedFile(path string) (*HuffmanResult, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return nil, err
	}
	return DeserializeEncodedData(data)
}

// BufferedReader provides buffered reading for encoding
type BufferedReader struct {
	reader *bufio.Reader
}

// NewBufferedReader creates a new buffered reader
func NewBufferedReader(r io.Reader) *BufferedReader {
	return &BufferedReader{
		reader: bufio.NewReader(r),
	}
}

// ReadByte reads a single byte
func (r *BufferedReader) ReadByte() (byte, error) {
	return r.reader.ReadByte()
}

// ReadAll reads all remaining bytes
func (r *BufferedReader) ReadAll() ([]byte, error) {
	return io.ReadAll(r.reader)
}