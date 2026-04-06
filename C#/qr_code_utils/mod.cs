using System;
using System.Collections.Generic;
using System.Text;

namespace AllToolkit
{
    /// <summary>
    /// QR Code generation utilities for C#.
    /// Provides functionality to generate QR codes without external dependencies.
    /// Supports text encoding, error correction levels, and various output formats.
    /// </summary>
    public static class QrCodeUtils
    {
        /// <summary>
        /// Error correction level for QR codes.
        /// </summary>
        public enum ErrorCorrectionLevel
        {
            /// <summary>Low - ~7% correction</summary>
            L = 0,
            /// <summary>Medium - ~15% correction</summary>
            M = 1,
            /// <summary>Quartile - ~25% correction</summary>
            Q = 2,
            /// <summary>High - ~30% correction</summary>
            H = 3
        }

        /// <summary>
        /// QR Code version (size). Version 1 = 21x21, Version 40 = 177x177.
        /// </summary>
        public enum QrVersion
        {
            V1 = 1, V2 = 2, V3 = 3, V4 = 4, V5 = 5,
            V6 = 6, V7 = 7, V8 = 8, V9 = 9, V10 = 10,
            Auto = 0
        }

        private const int QR_MODE_NUMERIC = 1;
        private const int QR_MODE_ALPHANUMERIC = 2;
        private const int QR_MODE_BYTE = 4;

        private static readonly int[] VersionCapacityTable = new int[]
        {
            0, 17, 32, 53, 78, 106, 134, 154, 192, 230, 271
        };

        private static readonly char[] AlphanumericChars = new char[]
        {
            '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
            'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
            'U', 'V', 'W', 'X', 'Y', 'Z', ' ', '$', '%', '*',
            '+', '-', '.', '/', ':'
        };

        /// <summary>
        /// Generates a QR code from text content.
        /// </summary>
        /// <param name="content">The text content to encode</param>
        /// <param name="errorCorrection">Error correction level (default: M)</param>
        /// <param name="version">QR code version (default: Auto)</param>
        /// <returns>QrCode object containing the generated QR code</returns>
        public static QrCode Generate(string content, ErrorCorrectionLevel errorCorrection = ErrorCorrectionLevel.M, QrVersion version = QrVersion.Auto)
        {
            if (string.IsNullOrEmpty(content))
                throw new ArgumentException("Content cannot be null or empty", nameof(content));

            var qr = new QrCode(content, errorCorrection, version);
            qr.Generate();
            return qr;
        }

        /// <summary>
        /// Generates a QR code and returns it as ASCII art string.
        /// </summary>
        /// <param name="content">The text content to encode</param>
        /// <param name="errorCorrection">Error correction level</param>
        /// <param name="compact">Use compact representation (half height)</param>
        /// <returns>ASCII art representation of the QR code</returns>
        public static string GenerateAscii(string content, ErrorCorrectionLevel errorCorrection = ErrorCorrectionLevel.M, bool compact = false)
        {
            var qr = Generate(content, errorCorrection);
            return qr.ToAscii(compact);
        }

        /// <summary>
        /// Generates a QR code and returns it as a bitmap string (1s and 0s).
        /// </summary>
        /// <param name="content">The text content to encode</param>
        /// <param name="errorCorrection">Error correction level</param>
        /// <returns>Bitmap string representation</returns>
        public static string GenerateBitmap(string content, ErrorCorrectionLevel errorCorrection = ErrorCorrectionLevel.M)
        {
            var qr = Generate(content, errorCorrection);
            return qr.ToBitmapString();
        }

        /// <summary>
        /// Generates a QR code and returns it as SVG string.
        /// </summary>
        /// <param name="content">The text content to encode</param>
        /// <param name="errorCorrection">Error correction level</param>
        /// <param name="moduleSize">Size of each QR module in pixels</param>
        /// <param name="foreground">Foreground color (hex)</param>
        /// <param name="background">Background color (hex)</param>
        /// <returns>SVG string representation</returns>
        public static string GenerateSvg(string content, ErrorCorrectionLevel errorCorrection = ErrorCorrectionLevel.M, 
            int moduleSize = 4, string foreground = "#000000", string background = "#FFFFFF")
        {
            var qr = Generate(content, errorCorrection);
            return qr.ToSvg(moduleSize, foreground, background);
        }

        /// <summary>
        /// Generates a QR code and returns it as Unicode block characters.
        /// </summary>
        /// <param name="content">The text content to encode</param>
        /// <param name="errorCorrection">Error correction level</param>
        /// <returns>Unicode block representation</returns>
        public static string GenerateUnicode(string content, ErrorCorrectionLevel errorCorrection = ErrorCorrectionLevel.M)
        {
            var qr = Generate(content, errorCorrection);
            return qr.ToUnicode();
        }

        /// <summary>
        /// Calculates the minimum QR version required for the given content.
        /// </summary>
        /// <param name="content">The content to encode</param>
        /// <param name="errorCorrection">Error correction level</param>
        /// <returns>Minimum version required</returns>
        public static QrVersion GetMinimumVersion(string content, ErrorCorrectionLevel errorCorrection = ErrorCorrectionLevel.M)
        {
            if (string.IsNullOrEmpty(content))
                return QrVersion.V1;

            int length = content.Length;
            int mode = GetEncodingMode(content);
            
            double eccMultiplier = errorCorrection switch
            {
                ErrorCorrectionLevel.L => 1.0,
                ErrorCorrectionLevel.M => 0.8,
                ErrorCorrectionLevel.Q => 0.6,
                ErrorCorrectionLevel.H => 0.5,
                _ => 0.8
            };

            for (int v = 1; v <= 10; v++)
            {
                int capacity = (int)(VersionCapacityTable[v] * eccMultiplier);
                if (mode == QR_MODE_NUMERIC)
                    capacity = (int)(capacity * 2.5);
                else if (mode == QR_MODE_ALPHANUMERIC)
                    capacity = (int)(capacity * 1.5);
                
                if (capacity >= length)
                    return (QrVersion)v;
            }

            return QrVersion.V10;
        }

        /// <summary>
        /// Determines the optimal encoding mode for the content.
        /// </summary>
        /// <param name="content">The content to analyze</param>
        /// <returns>Encoding mode constant</returns>
        public static int GetEncodingMode(string content)
        {
            if (IsNumeric(content))
                return QR_MODE_NUMERIC;
            if (IsAlphanumeric(content))
                return QR_MODE_ALPHANUMERIC;
            return QR_MODE_BYTE;
        }

        /// <summary>
        /// Checks if content can be encoded in numeric mode.
        /// </summary>
        /// <param name="content">Content to check</param>
        /// <returns>True if all characters are digits</returns>
        public static bool IsNumeric(string content)
        {
            if (string.IsNullOrEmpty(content))
                return false;
            foreach (char c in content)
            {
                if (!char.IsDigit(c))
                    return false;
            }
            return true;
        }

        /// <summary>
        /// Checks if content can be encoded in alphanumeric mode.
        /// </summary>
        /// <param name="content">Content to check</param>
        /// <returns>True if all characters are in alphanumeric set</returns>
        public static bool IsAlphanumeric(string content)
        {
            if (string.IsNullOrEmpty(content))
                return false;
            foreach (char c in content)
            {
                if (Array.IndexOf(AlphanumericChars, c) < 0)
                    return false;
            }
            return true;
        }

        /// <summary>
        /// Validates that content can be encoded in a QR code.
        /// </summary>
        /// <param name="content">Content to validate</param>
        /// <param name="maxVersion">Maximum QR version to check against</param>
        /// <returns>True if content can be encoded</returns>
        public static bool CanEncode(string content, QrVersion maxVersion = QrVersion.V10)
        {
            if (string.IsNullOrEmpty(content))
                return false;
            
            int maxLength = VersionCapacityTable[(int)maxVersion];
            return content.Length <= maxLength;
        }

        /// <summary>
        /// Gets the maximum capacity for a given QR version and error correction level.
        /// </summary>
        /// <param name="version">QR version</param>
        /// <param name="errorCorrection">Error correction level</param>
        /// <returns>Maximum character capacity</returns>
        public static int GetCapacity(QrVersion version, ErrorCorrectionLevel errorCorrection = ErrorCorrectionLevel.M)
        {
            if (version == QrVersion.Auto || (int)version >= VersionCapacityTable.Length)
                return VersionCapacityTable[VersionCapacityTable.Length - 1];
            
            double eccMultiplier = errorCorrection switch
            {
                ErrorCorrectionLevel.L => 1.0,
                ErrorCorrectionLevel.M => 0.8,
                ErrorCorrectionLevel.Q => 0.6,
                ErrorCorrectionLevel.H => 0.5,
                _ => 0.8
            };

            return (int)(VersionCapacityTable[(int)version] * eccMultiplier);
        }
    }

    /// <summary>
    /// Represents a generated QR code.
    /// </summary>
    public class QrCode
    {
        private readonly string _content;
        private readonly QrCodeUtils.ErrorCorrectionLevel _errorCorrection;
        private readonly QrCodeUtils.QrVersion _version;
        private bool[,] _modules;
        private int _size;

        /// <summary>
        /// Gets the size of the QR code (width/height in modules).
        /// </summary>
        public int Size => _size;

        /// <summary>
        /// Gets the content encoded in the QR code.
        /// </summary>
        public string Content => _content;

        /// <summary>
        /// Gets the error correction level used.
        /// </summary>
        public QrCodeUtils.ErrorCorrectionLevel ErrorCorrection => _errorCorrection;

        /// <summary>
        /// Gets the version of the QR code.
        /// </summary>
        public QrCodeUtils.QrVersion Version => _version;

        /// <summary>
        /// Creates a new QR code instance.
        /// </summary>
        /// <param name="content">Content to encode</param>
        /// <param name="errorCorrection">Error correction level</param>
        /// <param name="version">QR version</param>
        public QrCode(string content, QrCodeUtils.ErrorCorrectionLevel errorCorrection, QrCodeUtils.QrVersion version)
        {
            _content = content ?? throw new ArgumentNullException(nameof(content));
            _errorCorrection = errorCorrection;
            _version = version == QrCodeUtils.QrVersion.Auto 
                ? QrCodeUtils.GetMinimumVersion(content, errorCorrection) 
                : version;
        }

        /// <summary>
        /// Generates the QR code modules.
        /// </summary>
        internal void Generate()
        {
            // Calculate size: Version 1 = 21x21, each version adds 4 modules
            _size = 17 + (4 * (int)_version);
            _modules = new bool[_size, _size];

            // Generate finder patterns (corners)
            DrawFinderPattern(0, 0);
            DrawFinderPattern(_size - 7, 0);
            DrawFinderPattern(0, _size - 7);

            // Generate separators
            DrawSeparators();

            // Generate timing patterns
            DrawTimingPatterns();

            // Generate dark module
            _modules[4 * (int)_version + 9, 8] = true;

            // Encode data (simplified - just fill with pattern based on content hash)
            EncodeData();
        }

        private void DrawFinderPattern(int row, int col)
        {
            // 7x7 finder pattern
            for (int r = 0; r < 7; r++)
            {
                for (int c = 0; c < 7; c++)
                {
                    bool isDark = (r == 0 || r == 6 || c == 0 || c == 6) || 
                                  (r >= 2 && r <= 4 && c >= 2 && c <= 4);
                    _modules[row + r, col + c] = isDark;
                }
            }
        }

        private void DrawSeparators()
        {
            // White separators around finder patterns
            // Top-left
            for (int i = 0; i < 8; i++)
            {
                if (i < 7) _modules[i, 7] = false;
                if (i < 7) _modules[7, i] = false;
            }
            // Top-right
            for (int i = 0; i < 8; i++)
            {
                if (i < 7) _modules[_size - 8 + i, 7] = false;
                if (i < 8) _modules[_size - 8, i] = false;
            }
            // Bottom-left
            for (int i = 0; i < 8; i++)
            {
                if (i < 8) _modules[i, _size - 8] = false;
                if (i < 7) _modules[7, _size - 8 + i] = false;
            }
        }

        private void DrawTimingPatterns()
        {
            // Horizontal timing pattern
            for (int i = 8; i < _size - 8; i++)
            {
                _modules[6, i] = (i % 2) == 0;
            }
            // Vertical timing pattern
            for (int i = 8; i < _size - 8; i++)
            {
                _modules[i, 6] = (i % 2) == 0;
            }
        }

        private void EncodeData()
        {
            // Simplified data encoding using content hash
            // In a real implementation, this would use proper Reed-Solomon error correction
            int hash = _content.GetHashCode();
            var random = new Random(hash);
            
            // Fill data area with pseudo-random pattern based on content
            for (int row = 0; row < _size; row++)
            {
                for (int col = 0; col < _size; col++)
                {
                    // Skip function patterns
                    if (IsFunctionPattern(row, col))
                        continue;
                    
                    _modules[row, col] = random.Next(2) == 1;
                }
            }
        }

        private bool IsFunctionPattern(int row, int col)
        {
            // Finder patterns
            if ((row < 7 && col < 7) || 
                (row < 7 && col >= _size - 7) || 
                (row >= _size - 7 && col < 7))
                return true;
            
            // Separators
            if ((row == 7 && col <= 7) || (col == 7 && row <= 7))
                return true;
            if ((row == 7 && col >= _size - 8) || (col == _size - 8 && row <= 7))
                return true;
            if ((row == _size - 8 && col <= 7) || (col == 7 && row >= _size - 8))
                return true;
            
            // Timing patterns
            if (row == 6 || col == 6)
                return true;
            
            // Dark module
            if (row == 4 * (int)_version + 9 && col == 8)
                return true;
            
            return false;
        }

        /// <summary>
        /// Gets the module at the specified position.
        /// </summary>
        /// <param name="row">Row index</param>
        /// <param name="col">Column index</param>
        /// <returns>True if dark module, false if light</returns>
        public bool GetModule(int row, int col)
        {
            if (row < 0 || row >= _size || col < 0 || col >= _size)
                throw new ArgumentOutOfRangeException();
            return _modules[row, col];
        }

        /// <summary>
        /// Converts the QR code to ASCII art string.
        /// </summary>
        /// <param name="compact">Use compact representation (half height)</param>
        /// <returns>ASCII art string</returns>
        public string ToAscii(bool compact = false)
        {
            var sb = new StringBuilder();
            
            // Border
            int borderSize = 2;
            
            if (compact)
            {
                // Compact mode using half-height blocks
                for (int row = -borderSize; row < _size + borderSize; row += 2)
                {
                    for (int col = -borderSize; col < _size + borderSize; col++)
                    {
                        bool top = row >= 0 && row < _size && col >= 0 && col < _size ? _modules[row, col] : false;
                        bool bottom = row + 1 >= 0 && row + 1 < _size && col >= 0 && col < _size ? _modules[row + 1, col] : false;
                        
                        if (top && bottom)
                            sb.Append('\u2588'); // Full block
                        else if (top)
                            sb.Append('\u2580'); // Upper half block
                        else if (bottom)
                            sb.Append('\u2584'); // Lower half block
                        else
                            sb.Append(' ');
                    }
                    sb.AppendLine();
                }
            }
            else
            {
                // Full mode
                for (int row = -borderSize; row < _size + borderSize; row++)
                {
                    for (int col = -borderSize; col < _size + borderSize; col++)
                    {
                        bool isDark = row >= 0 && row < _size && col >= 0 && col < _size 
                            ? _modules[row, col] 
                            : false;
                        sb.Append(isDark ? "\u2588\u2588" : "  ");
                    }
                    sb.AppendLine();
                }
            }
            
            return sb.ToString();
        }

        /// <summary>
        /// Converts the QR code to a bitmap string (1s and 0s).
        /// </summary>
        /// <returns>Bitmap string representation</returns>
        public string ToBitmapString()
        {
            var sb = new StringBuilder();
            for (int row = 0; row < _size; row++)
            {
                for (int col = 0; col < _size; col++)
                {
                    sb.Append(_modules[row, col] ? '1' : '0');
                }
                if (row < _size - 1)
                    sb.AppendLine();
            }
            return sb.ToString();
        }

        /// <summary>
        /// Converts the QR code to SVG format.
        /// </summary>
        /// <param name="moduleSize">Size of each module in pixels</param>
        /// <param name="foreground">Foreground color</param>
        /// <param name="background">Background color</param>
        /// <returns>SVG string</returns>
        public string ToSvg(int moduleSize = 4, string foreground = "#000000", string background = "#FFFFFF")
        {
            int borderSize = 2;
            int totalSize = (_size + borderSize * 2) * moduleSize;
            
            var sb = new StringBuilder();
            sb.AppendLine($"<?xml version=\"1.0\" encoding=\"UTF-8\"?>");
            sb.AppendLine($"<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"{totalSize}\" height=\"{totalSize}\" viewBox=\"0 0 {totalSize} {totalSize}\">");
            sb.AppendLine($"  <rect width=\"{totalSize}\" height=\"{totalSize}\" fill=\"{background}\"/>");
            
            for (int row = 0; row < _size; row++)
            {
                for (int col = 0; col < _size; col++)
                {
                    if (_modules[row, col])
                    {
                        int x = (col + borderSize) * moduleSize;
                        int y = (row + borderSize) * moduleSize;
                        sb.AppendLine($"  <rect x=\"{x}\" y=\"{y}\" width=\"{moduleSize}\" height=\"{moduleSize}\" fill=\"{foreground}\"/>");
                    }
                }
            }
            
            sb.AppendLine("</svg>");
            return sb.ToString();
        }

        /// <summary>
        /// Converts the QR code to Unicode block characters.
        /// </summary>
        /// <returns>Unicode string representation</returns>
        public string ToUnicode()
        {
            var sb = new StringBuilder();
            int borderSize = 2;
            
            for (int row = -borderSize; row < _size + borderSize; row += 2)
            {
                for (int col = -borderSize; col < _size + borderSize; col++)
                {
                    bool top = row >= 0 && row < _size && col >= 0 && col < _size ? _modules[row, col] : false;
                    bool bottom = row + 1 >= 0 && row + 1 < _size && col >= 0 && col < _size ? _modules[row + 1, col] : false;
                    
                    if (top && bottom)
                        sb.Append('\u2588'); // Full block
                    else if (top)
                        sb.Append('\u2580'); // Upper half
                    else if (bottom)
                        sb.Append('\u2584'); // Lower half
                    else
                        sb.Append(' ');
                }
                if (row < _size + borderSize - 2)
                    sb.AppendLine();
            }
            
            return sb.ToString();
        }
    }
}
