package json_utils

/**
 * JSON Utilities for Kotlin - A zero-dependency JSON library
 * Uses only Kotlin standard library
 *
 * @author AllToolkit
 * @version 1.0.0
 */

/** JSON value sealed class hierarchy */
sealed class JsonValue {
    fun isNull(): Boolean = this is JsonNull
    fun isBoolean(): Boolean = this is JsonBoolean
    fun isNumber(): Boolean = this is JsonNumber
    fun isString(): Boolean = this is JsonString
    fun isArray(): Boolean = this is JsonArray
    fun isObject(): Boolean = this is JsonObject

    fun asBoolean(default: Boolean = false): Boolean = when (this) {
        is JsonBoolean -> value
        else -> default
    }

    fun asDouble(default: Double = 0.0): Double = when (this) {
        is JsonNumber -> value
        is JsonString -> value.toDoubleOrNull() ?: default
        else -> default
    }

    fun asInt(default: Int = 0): Int = asDouble(default.toDouble()).toInt()
    fun asLong(default: Long = 0L): Long = asDouble(default.toDouble()).toLong()

    fun asString(default: String = ""): String = when (this) {
        is JsonString -> value
        is JsonNumber -> value.toString()
        is JsonBoolean -> value.toString()
        is JsonNull -> "null"
        else -> default
    }

    fun asArray(): JsonArray = when (this) {
        is JsonArray -> this
        else -> JsonArray(emptyList())
    }

    fun asObject(): JsonObject = when (this) {
        is JsonObject -> this
        else -> JsonObject(emptyMap())
    }

    fun size(): Int = when (this) {
        is JsonArray -> values.size
        is JsonObject -> properties.size
        else -> 0
    }

    abstract fun toJsonString(): String
    abstract fun toPrettyString(indent: String = "  ", level: Int = 0): String
}

object JsonNull : JsonValue() {
    override fun toJsonString(): String = "null"
    override fun toPrettyString(indent: String, level: Int): String = "null"
    override fun toString(): String = "null"
}

data class JsonBoolean(val value: Boolean) : JsonValue() {
    override fun toJsonString(): String = value.toString()
    override fun toPrettyString(indent: String, level: Int): String = value.toString()
    override fun toString(): String = value.toString()
}

data class JsonNumber(val value: Double) : JsonValue() {
    constructor(value: Int) : this(value.toDouble())
    constructor(value: Long) : this(value.toDouble())
    constructor(value: Float) : this(value.toDouble())

    override fun toJsonString(): String = when {
        value.isNaN() -> "null"
        value.isInfinite() -> "null"
        value == value.toLong().toDouble() -> value.toLong().toString()
        else -> value.toString()
    }
    override fun toPrettyString(indent: String, level: Int): String = toJsonString()
    override fun toString(): String = toJsonString()
}

data class JsonString(val value: String) : JsonValue() {
    override fun toJsonString(): String = escapeJsonString(value)
    override fun toPrettyString(indent: String, level: Int): String = escapeJsonString(value)
    override fun toString(): String = value
}

data class JsonArray(val values: List<JsonValue>) : JsonValue(), Iterable<JsonValue> by values {
    constructor(vararg values: JsonValue) : this(values.toList())

    operator fun get(index: Int): JsonValue = if (index in values.indices) values[index] else JsonNull
    fun getString(index: Int, default: String = ""): String = get(index).asString(default)
    fun getInt(index: Int, default: Int = 0): Int = get(index).asInt(default)
    fun getDouble(index: Int, default: Double = 0.0): Double = get(index).asDouble(default)
    fun getBoolean(index: Int, default: Boolean = false): Boolean = get(index).asBoolean(default)
    fun getObject(index: Int): JsonObject = get(index).asObject()
    fun getArray(index: Int): JsonArray = get(index).asArray()

    override fun toJsonString(): String = values.joinToString(",", "[", "]") { it.toJsonString() }
    override fun toPrettyString(indent: String, level: Int): String {
        if (values.isEmpty()) return "[]"
        val prefix = indent.repeat(level)
        val innerPrefix = indent.repeat(level + 1)
        val lines = values.joinToString(",\n") { "$innerPrefix${it.toPrettyString(indent, level + 1)}" }
        return "[\n$lines\n$prefix]"
    }
    override fun toString(): String = toJsonString()
}

data class JsonObject(val properties: Map<String, JsonValue>) : JsonValue() {
    constructor(vararg pairs: Pair<String, JsonValue>) : this(mapOf(*pairs))

    operator fun get(key: String): JsonValue = properties[key] ?: JsonNull
    fun has(key: String): Boolean = properties.containsKey(key)
    fun getString(key: String, default: String = ""): String = get(key).asString(default)
    fun getInt(key: String, default: Int = 0): Int = get(key).asInt(default)
    fun getDouble(key: String, default: Double = 0.0): Double = get(key).asDouble(default)
    fun getBoolean(key: String, default: Boolean = false): Boolean = get(key).asBoolean(default)
    fun getObject(key: String): JsonObject = get(key).asObject()
    fun getArray(key: String): JsonArray = get(key).asArray()
    fun keys(): Set<String> = properties.keys
    fun values(): Collection<JsonValue> = properties.values
    fun entries(): Set<Map.Entry<String, JsonValue>> = properties.entries

    operator fun plus(other: JsonObject): JsonObject = JsonObject(properties + other.properties)

    override fun toJsonString(): String {
        if (properties.isEmpty()) return "{}"
        val entries = properties.entries.joinToString(",") { "${escapeJsonString(it.key)}:${it.value.toJsonString()}" }
        return "{$entries}"
    }

    override fun toPrettyString(indent: String, level: Int): String {
        if (properties.isEmpty()) return "{}"
        val prefix = indent.repeat(level)
        val innerPrefix = indent.repeat(level + 1)
        val lines = properties.entries.joinToString(",\n") {
            "$innerPrefix${escapeJsonString(it.key)}: ${it.value.toPrettyString(indent, level + 1)}"
        }
        return "{\n$lines\n$prefix}"
    }

    override fun toString(): String = toJsonString()
}

/** Escapes a string for JSON output */
fun escapeJsonString(str: String): String {
    val sb = StringBuilder(str.length + 10)
    sb.append('"')
    for (c in str) {
        when (c) {
            '"' -> sb.append("\\\"")
            '\\' -> sb.append("\\\\")
            '\b' -> sb.append("\\b")
            '\n' -> sb.append("\\n")
            '\r' -> sb.append("\\r")
            '\t' -> sb.append("\\t")
            else -> if (c.code < 0x20) {
                sb.append(String.format("\\u%04x", c.code))
            } else {
                sb.append(c)
            }
        }
    }
    sb.append('"')
    return sb.toString()
}

/** JSON Parser class */
class JsonParser(private val json: String) {
    private var pos = 0

    fun parse(): JsonValue {
        skipWhitespace()
        return when (peek()) {
            'n' -> parseNull()
            't', 'f' -> parseBoolean()
            '"' -> parseString()
            '[' -> parseArray()
            '{' -> parseObject()
            '-', in '0'..'9' -> parseNumber()
            else -> throw JsonParseException("Unexpected character '${peek()}' at position $pos")
        }
    }

    private fun peek(): Char = if (pos < json.length) json[pos] else '\u0000'
    private fun advance(): Char = json[pos++]
    private fun skipWhitespace() { while (pos < json.length && json[pos].isWhitespace()) pos++ }

    private fun parseNull(): JsonNull {
        if (json.substring(pos, pos + 4) == "null") { pos += 4; return JsonNull }
        throw JsonParseException("Expected 'null' at position $pos")
    }

    private fun parseBoolean(): JsonBoolean {
        return when {
            json.substring(pos, kotlin.math.min(pos + 4, json.length)) == "true" -> {
                pos += 4
                JsonBoolean(true)
            }
            json.substring(pos, kotlin.math.min(pos + 5, json.length)) == "false" -> {
                pos += 5
                JsonBoolean(false)
            }
            else -> throw JsonParseException("Expected 'true' or 'false' at position $pos")
        }
    }

    private fun parseString(): JsonString {
        if (advance() != '"') throw JsonParseException("Expected opening quote at position ${pos - 1}")
        val sb = StringBuilder()
        while (pos < json.length) {
            when (val c = advance()) {
                '"' -> return JsonString(sb.toString())
                '\\' -> {
                    when (val esc = advance()) {
                        '"' -> sb.append('"')
                        '\\' -> sb.append('\\')
                        '/' -> sb.append('/')
                        'b' -> sb.append('\b')
                        'f' -> sb.append('\u000C')
                        'n' -> sb.append('\n')
                        'r' -> sb.append('\r')
                        't' -> sb.append('\t')
                        'u' -> {
                            if (pos + 4 > json.length) throw JsonParseException("Incomplete unicode escape at position $pos")
                            val hex = json.substring(pos, pos + 4)
                            pos += 4
                            sb.append(hex.toInt(16).toChar())
                        }
                        else -> sb.append(esc)
                    }
                }
                else -> sb.append(c)
            }
        }
        throw JsonParseException("Unterminated string at position $pos")
    }

    private fun parseNumber(): JsonNumber {
        val start = pos
        if (peek() == '-') advance()
        while (peek().isDigit()) advance()
        if (peek() == '.') {
            advance()
            while (peek().isDigit()) advance()
        }
        if (peek() == 'e' || peek() == 'E') {
            advance()
            if (peek() == '+' || peek() == '-') advance()
            while (peek().isDigit()) advance()
        }
        val numStr = json.substring(start, pos)
        return JsonNumber(numStr.toDouble())
    }

    private fun parseArray(): JsonArray {
        if (advance() != '[') throw JsonParseException("Expected '[' at position ${pos - 1}")
        skipWhitespace()
        if (peek() == ']') {
            advance()
            return JsonArray(emptyList())
        }
        val values = mutableListOf<JsonValue>()
        while (true) {
            skipWhitespace()
            values.add(parse())
            skipWhitespace()
            when (advance()) {
                ',' -> continue
                ']' -> return JsonArray(values)
                else -> throw JsonParseException("Expected ',' or ']' at position ${pos - 1}")
            }
        }
    }

    private fun parseObject(): JsonObject {
        if (advance() != '{') throw JsonParseException("Expected '{' at position ${pos - 1}")
        skipWhitespace()
        if (peek() == '}') {
            advance()
            return JsonObject(emptyMap())
        }
        val props = mutableMapOf<String, JsonValue>()
        while (true) {
            skipWhitespace()
            val key = parseString().value
            skipWhitespace()
            if (advance() != ':') throw JsonParseException("Expected ':' at position ${pos - 1}")
            skipWhitespace()
            props[key] = parse()
            skipWhitespace()
            when (advance()) {
                ',' -> continue
                '}' -> return JsonObject(props)
                else -> throw JsonParseException("Expected ',' or '}' at position ${pos - 1}")
            }
        }
    }
}

/** Exception thrown when JSON parsing fails */
class JsonParseException(message: String) : Exception(message)

/** JSON Utilities object with convenience functions */
object JsonUtils {
    /** Parse a JSON string into a JsonValue */
    @JvmStatic
    fun parse(json: String): JsonValue = JsonParser(json).parse()

    /** Parse a JSON string safely, returning null on error */
    @JvmStatic
    fun parseOrNull(json: String): JsonValue? = try {
        parse(json)
    } catch (e: JsonParseException) {
        null
    }

    /** Check if a string is valid JSON */
    @JvmStatic
    fun isValid(json: String): Boolean = try {
        parse(json)
        true
    } catch (e: JsonParseException) {
        false
    }

    /** Create a JsonObject from pairs */
    @JvmStatic
    fun obj(vararg pairs: Pair<String, Any?>): JsonObject = JsonObject(
        pairs.map { it.first to toJsonValue(it.second) }.toMap()
    )

    /** Create a JsonArray from values */
    @JvmStatic
    fun arr(vararg values: Any?): JsonArray = JsonArray(
        values.map { toJsonValue(it) }
    )

    /** Convert any value to JsonValue */
    @JvmStatic
    fun toJsonValue(value: Any?): JsonValue = when (value) {
        null -> JsonNull
        is JsonValue -> value
        is Boolean -> JsonBoolean(value)
        is Int -> JsonNumber(value)
        is Long -> JsonNumber(value)
        is Float -> JsonNumber(value)
        is Double -> JsonNumber(value)
        is String -> JsonString(value)
        is List<*> -> JsonArray(value.map { toJsonValue(it) })
        is Map<*, *> -> JsonObject(
            value.mapNotNull { (k, v) ->
                (k as? String)?.let { it to toJsonValue(v) }
            }.toMap()
        )
        else -> JsonString(value.toString())
    }

    /** Pretty print a JSON string */
    @JvmStatic
    fun prettyPrint(json: String, indent: String = "  "): String =
        parse(json).toPrettyString(indent)

    /** Minify a JSON string */
    @JvmStatic
    fun minify(json: String): String = parse(json).toJsonString()

    /** Merge two JSON objects */
    @JvmStatic
    fun merge(obj1: JsonObject, obj2: JsonObject): JsonObject = obj1 + obj2

    /** Convert Kotlin map to JSON string */
    @JvmStatic
    fun toJson(map: Map<String, Any?>): String = JsonObject(
        map.mapValues { toJsonValue(it.value) }
    ).toJsonString()

    /** Convert Kotlin list to JSON string */
    @JvmStatic
    fun toJson(list: List<Any?>): String = JsonArray(
        list.map { toJsonValue(it) }
    ).toJsonString()
}
