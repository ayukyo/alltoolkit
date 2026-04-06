' =============================================================================
' AllToolkit - JSON Utilities for VB.NET
' =============================================================================
' A comprehensive JSON parsing and generation utility module for VB.NET with
' zero dependencies. Supports parsing JSON strings to .NET objects, generating
' JSON from objects, and safe navigation with default values.
'
' Features:
' - Zero dependencies, uses only .NET standard library
' - Complete JSON support: null, boolean, number, string, array, object
' - Type-safe access with default values
' - Pretty printing with customizable indentation
' - Safe parsing with error handling
' - Full Unicode and escape sequence support
'
' Author: AllToolkit Contributors
' License: MIT
' =============================================================================

Imports System
Imports System.Collections.Generic
Imports System.Text
Imports System.Globalization

Namespace AllToolkit

    ''' <summary>
    ''' Enumeration of JSON value types
    ''' </summary>
    Public Enum JsonType
        Null
        Boolean
        Number
        String
        Array
        Object
    End Enum

    ''' <summary>
    ''' Represents a JSON value with type information
    ''' </summary>
    Public Class JsonValue
        Public Property Type As JsonType = JsonType.Null
        Public Property RawValue As Object = Nothing

        ' Cached values for performance
        Private _stringValue As String = Nothing
        Private _numberValue As Double = 0
        Private _boolValue As Boolean = False
        Private _arrayValue As List(Of JsonValue) = Nothing
        Private _objectValue As Dictionary(Of String, JsonValue) = Nothing

        ''' <summary>
        ''' Creates a null JSON value
        ''' </summary>
        Public Sub New()
            Type = JsonType.Null
        End Sub

        ''' <summary>
        ''' Creates a JSON value from a string
        ''' </summary>
        Public Sub New(value As String)
            Type = JsonType.String
            _stringValue = value
            RawValue = value
        End Sub

        ''' <summary>
        ''' Creates a JSON value from a number
        ''' </summary>
        Public Sub New(value As Double)
            Type = JsonType.Number
            _numberValue = value
            RawValue = value
        End Sub

        ''' <summary>
        ''' Creates a JSON value from a boolean
        ''' </summary>
        Public Sub New(value As Boolean)
            Type = JsonType.Boolean
            _boolValue = value
            RawValue = value
        End Sub

        ''' <summary>
        ''' Creates a JSON array value
        ''' </summary>
        Public Sub New(value As List(Of JsonValue))
            Type = JsonType.Array
            _arrayValue = value
            RawValue = value
        End Sub

        ''' <summary>
        ''' Creates a JSON object value
        ''' </summary>
        Public Sub New(value As Dictionary(Of String, JsonValue))
            Type = JsonType.Object
            _objectValue = value
            RawValue = value
        End Sub

        ''' <summary>
        ''' Gets the string value, returns default if not a string
        ''' </summary>
        Public Function AsString(Optional defaultValue As String = "") As String
            If Type = JsonType.String Then
                Return _stringValue
            End If
            Return defaultValue
        End Function

        ''' <summary>
        ''' Gets the number value, returns default if not a number
        ''' </summary>
        Public Function AsNumber(Optional defaultValue As Double = 0) As Double
            If Type = JsonType.Number Then
                Return _numberValue
            End If
            Return defaultValue
        End Function

        ''' <summary>
        ''' Gets the integer value, returns default if not a number
        ''' </summary>
        Public Function AsInteger(Optional defaultValue As Integer = 0) As Integer
            If Type = JsonType.Number Then
                Return CInt(_numberValue)
            End If
            Return defaultValue
        End Function

        ''' <summary>
        ''' Gets the boolean value, returns default if not a boolean
        ''' </summary>
        Public Function AsBoolean(Optional defaultValue As Boolean = False) As Boolean
            If Type = JsonType.Boolean Then
                Return _boolValue
            End If
            Return defaultValue
        End Function

        ''' <summary>
        ''' Gets the array value, returns empty list if not an array
        ''' </summary>
        Public Function AsArray() As List(Of JsonValue)
            If Type = JsonType.Array AndAlso _arrayValue IsNot Nothing Then
                Return _arrayValue
            End If
            Return New List(Of JsonValue)()
        End Function

        ''' <summary>
        ''' Gets the object value, returns empty dictionary if not an object
        ''' </summary>
        Public Function AsObject() As Dictionary(Of String, JsonValue)
            If Type = JsonType.Object AndAlso _objectValue IsNot Nothing Then
                Return _objectValue
            End If
            Return New Dictionary(Of String, JsonValue)()
        End Function

        ''' <summary>
        ''' Gets a value from object by key, returns null if not found or not an object
        ''' </summary>
        Public Function GetValue(key As String) As JsonValue
            If Type = JsonType.Object AndAlso _objectValue IsNot Nothing Then
                If _objectValue.ContainsKey(key) Then
                    Return _objectValue(key)
                End If
            End If
            Return New JsonValue()
        End Function

        ''' <summary>
        ''' Gets a value from array by index, returns null if out of bounds or not an array
        ''' </summary>
        Public Function GetValue(index As Integer) As JsonValue
            If Type = JsonType.Array AndAlso _arrayValue IsNot Nothing Then
                If index >= 0 AndAlso index < _arrayValue.Count Then
                    Return _arrayValue(index)
                End If
            End If
            Return New JsonValue()
        End Function

        ''' <summary>
        ''' Checks if this value is null
        ''' </summary>
        Public Function IsNull() As Boolean
            Return Type = JsonType.Null
        End Function

        ''' <summary>
        ''' Checks if this value is an object with the specified key
        ''' </summary>
        Public Function HasKey(key As String) As Boolean
            Return Type = JsonType.Object AndAlso _objectValue IsNot Nothing AndAlso _objectValue.ContainsKey(key)
        End Function

        ''' <summary>
        ''' Gets the count of elements (for arrays) or keys (for objects)
        ''' </summary>
        Public Function Count() As Integer
            If Type = JsonType.Array AndAlso _arrayValue IsNot Nothing Then
                Return _arrayValue.Count
            ElseIf Type = JsonType.Object AndAlso _objectValue IsNot Nothing Then
                Return _objectValue.Count
            End If
            Return 0
        End Function

        ''' <summary>
        ''' Converts this JSON value to a JSON string
        ''' </summary>
        Public Function ToJson() As String
            Return JsonUtils.Serialize(Me)
        End Function

        ''' <summary>
        ''' Converts this JSON value to a pretty-printed JSON string
        ''' </summary>
        Public Function ToPrettyJson(Optional indent As String = "  ") As String
            Return JsonUtils.SerializePretty(Me, indent)
        End Function

        ''' <summary>
        ''' Returns a string representation of this JSON