' =============================================================================
' AllToolkit - File Utilities for VB.NET
' =============================================================================
' A comprehensive file manipulation utility library for VB.NET applications.
' Zero dependencies - uses only .NET standard library.
' 
' Features:
' - File reading/writing with encoding support
' - File information and metadata retrieval
' - Directory operations (create, delete, enumerate)
' - Path manipulation and validation
' - File copying, moving, and deletion with safety checks
' - File search and filtering
' - File size formatting
' =============================================================================

Imports System
Imports System.IO
Imports System.Text
Imports System.Linq
Imports System.Collections.Generic

Namespace AllToolkit

    ''' <summary>
    ''' File operation result containing success status and optional error message.
    ''' </summary>
    Public Class FileResult
        ''' <summary>Indicates whether the operation was successful.</summary>
        Public Property Success As Boolean
        
        ''' <summary>Error message if operation failed.</summary>
        Public Property ErrorMessage As String
        
        ''' <summary>Full path of the affected file/directory.</summary>
        Public Property Path As String

        Public Sub New(success As Boolean, Optional path As String = "", Optional errorMessage As String = "")
            Me.Success = success
            Me.Path = path
            Me.ErrorMessage = errorMessage
        End Sub
    End Class

    ''' <summary>
    ''' File information wrapper with additional utility properties.
    ''' </summary>
    Public Class FileInfoWrapper
        ''' <summary>Original FileInfo object.</summary>
        Public ReadOnly Property Info As FileInfo
        
        ''' <summary>File name with extension.</summary>
        Public ReadOnly Property Name As String
            Get
                Return Info.Name
            End Get
        End Property
        
        ''' <summary>File name without extension.</summary>
        Public ReadOnly Property NameWithoutExtension As String
            Get
                Return Path.GetFileNameWithoutExtension(Info.Name)
            End Get
        End Property
        
        ''' <summary>File extension (lowercase, without dot).</summary>
        Public ReadOnly Property Extension As String
            Get
                Return Info.Extension.TrimStart("."c).ToLower()
            End Get
        End Property
        
        ''' <summary>Full path of the file.</summary>
        Public ReadOnly Property FullPath As String
            Get
                Return Info.FullName
            End Get
        End Property
        
        ''' <summary>Directory containing the file.</summary>
        Public ReadOnly Property Directory As String
            Get
                Return Info.DirectoryName
            End Get
        End Property
        
        ''' <summary>File size in bytes.</summary>
        Public ReadOnly Property SizeBytes As Long
            Get
                Return Info.Length
            End Get
        End Property
        
        ''' <summary>File size as human-readable string.</summary>
        Public ReadOnly Property SizeFormatted As String
            Get
                Return FileUtils.FormatFileSize(Info.Length)
            End Get
        End Property
        
        ''' <summary>Creation timestamp.</summary>
        Public ReadOnly Property Created As DateTime
            Get
                Return Info.CreationTime
            End Get
        End Property
        
        ''' <summary>Last modification timestamp.</summary>
        Public ReadOnly Property Modified As DateTime
            Get
                Return Info.LastWriteTime
            End Get
        End Property
        
        ''' <summary>Last access timestamp.</summary>
        Public ReadOnly Property Accessed As DateTime
            Get
                Return Info.LastAccessTime
            End Get
        End Property
        
        ''' <summary>True if file is read-only.</summary>
        Public ReadOnly Property IsReadOnly As Boolean
            Get
                Return Info.IsReadOnly
            End Get
        End Property
        
        ''' <summary>True if file is hidden.</summary>
        Public ReadOnly Property IsHidden As Boolean
            Get
                Return (Info.Attributes And FileAttributes.Hidden) = FileAttributes.Hidden
            End Get
        End Property
        
        ''' <summary>File attributes.</summary>
        Public ReadOnly Property Attributes As FileAttributes
            Get
                Return Info.Attributes
            End Get
        End Property

        Public Sub New(fileInfo As FileInfo)
            Me.Info = fileInfo
        End Sub
    End Class

    ''' <summary>
    ''' Search options for file enumeration.
    ''' </summary>
    Public Class FileSearchOptions
        ''' <summary>Search pattern (e.g., "*.txt").</summary>
        Public Property Pattern As String = "*"
        
        ''' <summary>Search in subdirectories.</summary>
        Public Property Recursive As Boolean = False
        
        ''' <summary>Include hidden files.</summary>
        Public Property IncludeHidden As Boolean = False
        
        ''' <summary>Minimum file size in bytes (0 = no limit).</summary>
        Public Property MinSize As Long = 0
        
        ''' <summary>Maximum file size in bytes (0 = no limit).</summary>
        Public Property MaxSize As Long = 0
        
        ''' <summary>Modified after this date (Nothing = no limit).</summary>
        Public Property ModifiedAfter As DateTime? = Nothing
        
        ''' <summary>Modified before this date (Nothing = no limit).</summary>
        Public Property ModifiedBefore As DateTime? = Nothing
    End Class

    ''' <summary>
    ''' Comprehensive file utilities for VB.NET.
    ''' </summary>
    Public Module FileUtils

        ' =========================================================================
        ' Constants
        ' =========================================================================
        
        ''' <summary>Default encoding for file operations.</summary>
        Public ReadOnly DefaultEncoding As Encoding = Encoding.UTF8
        
        ''' <summary>Buffer size for file operations (64KB).</summary>
        Public Const BufferSize As Integer = 65536

        ' =========================================================================
        ' File Reading Operations
        ' =========================================================================

        ''' <summary>
        ''' Reads all text from a file.
        ''' </summary>
        ''' <param name="filePath">Path to the file.</param>
        ''' <param name="encoding">Text encoding (default: UTF-8).</param>
        ''' <returns>File contents as string, or empty string if file doesn't exist.</returns>
        Public Function ReadAllText(filePath As String, Optional encoding As Encoding = Nothing) As String
            If String.IsNullOrEmpty(filePath) Then Return String.Empty
            If Not File.Exists(filePath) Then Return String.Empty
            
            Try
                Dim enc As Encoding = If(encoding, DefaultEncoding)
                Return File.ReadAllText(filePath, enc)
            Catch
                Return String.Empty
            End Try
        End Function

        ''' <summary>
        ''' Reads all lines from a file.
        ''' </summary>
        ''' <param name="filePath">Path to the file.</param>
        ''' <param name="encoding">Text encoding (default: UTF-8).</param>
        ''' <returns>Array of lines,