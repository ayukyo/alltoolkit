/**
 * ISBN Utils - 国际标准书号 (ISBN) 工具集
 * 
 * 功能：
 * - ISBN-10 和 ISBN-13 验证
 * - ISBN-10 与 ISBN-13 互相转换
 * - 从 ISBN 提取信息（前缀、注册组、出版者、校验位）
 * - 格式化显示
 * - 生成有效 ISBN
 * 
 * 无外部依赖，纯 Kotlin 标准库实现
 * 
 * @author AllToolkit
 * @date 2026-05-13
 */

package isbn_utils

/**
 * ISBN 类型枚举
 */
enum class ISBNType {
    ISBN_10,
    ISBN_13,
    INVALID
}

/**
 * ISBN 解析结果
 */
data class ISBNInfo(
    val type: ISBNType,
    val original: String,
    val formatted: String,
    val isValid: Boolean,
    val prefix: String?,           // ISBN-13 的 GS1 前缀 (978 或 979)
    val registrationGroup: String?, // 注册组代码（国家/地区）
    val registrant: String?,        // 出版者代码
    val publication: String?,       // 出版物代码
    val checkDigit: Char?,          // 校验位
    val isbn10: String?,            // ISBN-10 格式
    val isbn13: String?             // ISBN-13 格式
)

/**
 * ISBN 工具类
 * 提供完整的 ISBN 验证、解析、转换功能
 */
object ISBNUtils {
    
    // ISBN-13 前缀
    private const val ISBN_13_PREFIX_BOOKLAND = "978"
    private const val ISBN_13_PREFIX_OTHER = "979"
    
    // 已知的注册组前缀（部分常用）
    // 格式：前缀 -> (国家/地区名, 最小长度, 最大长度)
    private val registrationGroups = mapOf(
        // 978 前缀下的注册组
        "0" to Triple("英语区", 1, 5),
        "1" to Triple("英语区", 2, 5),
        "2" to Triple("法语区", 2, 5),
        "3" to Triple("德语区", 2, 5),
        "4" to Triple("日本", 2, 5),
        "5" to Triple("俄语区", 2, 5),
        "7" to Triple("中国", 2, 4),
        "80" to Triple("捷克/斯洛伐克", 2, 4),
        "81" to Triple("印度", 2, 4),
        "82" to Triple("挪威", 2, 4),
        "83" to Triple("波兰", 2, 4),
        "84" to Triple("西班牙", 2, 4),
        "85" to Triple("巴西", 2, 4),
        "86" to Triple("塞尔维亚", 2, 4),
        "87" to Triple("丹麦", 2, 4),
        "88" to Triple("意大利", 2, 4),
        "89" to Triple("韩国", 2, 4),
        "90" to Triple("荷兰/比利时", 2, 4),
        "91" to Triple("瑞典", 2, 4),
        "92" to Triple("国际组织", 1, 4),
        "93" to Triple("印度", 2, 4),
        "94" to Triple("荷兰", 2, 4),
        "952" to Triple("芬兰", 2, 4),
        "953" to Triple("克罗地亚", 2, 4),
        "954" to Triple("保加利亚", 2, 4),
        "955" to Triple("斯里兰卡", 2, 4),
        "956" to Triple("智利", 2, 4),
        "957" to Triple("台湾", 2, 4),
        "958" to Triple("哥伦比亚", 2, 4),
        "959" to Triple("东南亚", 2, 4),
        "960" to Triple("希腊", 2, 4),
        "961" to Triple("斯洛文尼亚", 2, 4),
        "962" to Triple("香港", 2, 4),
        "963" to Triple("匈牙利", 2, 4),
        "964" to Triple("伊朗", 2, 4),
        "965" to Triple("以色列", 2, 4),
        "966" to Triple("乌克兰", 2, 4),
        "967" to Triple("马来西亚", 2, 4),
        "968" to Triple("墨西哥", 2, 4),
        "969" to Triple("巴基斯坦", 2, 4),
        "970" to Triple("墨西哥", 2, 4),
        "971" to Triple("菲律宾", 2, 4),
        "972" to Triple("葡萄牙", 2, 4),
        "973" to Triple("罗马尼亚", 2, 4),
        "974" to Triple("泰国", 2, 4),
        "975" to Triple("土耳其", 2, 4),
        "976" to Triple("加勒比", 2, 4),
        "977" to Triple("埃及", 2, 4),
        "978" to Triple("尼日利亚", 2, 4),
        "979" to Triple("印度尼西亚", 2, 4),
        "980" to Triple("委内瑞拉", 2, 4),
        "981" to Triple("新加坡", 2, 4),
        "982" to Triple("太平洋地区", 2, 4),
        "983" to Triple("马来西亚", 2, 4),
        "984" to Triple("孟加拉国", 2, 4),
        "985" to Triple("白俄罗斯", 2, 4),
        "986" to Triple("台湾", 2, 4),
        "987" to Triple("阿根廷", 2, 4),
        "988" to Triple("香港", 2, 4),
        "989" to Triple("葡萄牙", 2, 4),
        "9940" to Triple("土耳其", 2, 4),
        "9941" to Triple("格鲁吉亚", 2, 4),
        "9942" to Triple("格鲁吉亚", 2, 4),
        "9943" to Triple("亚美尼亚", 2, 4),
        "9944" to Triple("亚美尼亚", 2, 4),
        "9945" to Triple("朝鲜", 2, 4),
        "9946" to Triple("朝鲜", 2, 4),
        "9947" to Triple("朝鲜", 2, 4),
        "9948" to Triple("哈萨克斯坦", 2, 4),
        "9949" to Triple("爱沙尼亚", 2, 4),
        "9950" to Triple("巴勒斯坦", 2, 4),
        "9951" to Triple("科索沃", 2, 4),
        "9952" to Triple("科索沃", 2, 4),
        "9953" to Triple("阿尔及利亚", 2, 4),
        "9954" to Triple("阿尔及利亚", 2, 4),
        "9955" to Triple("立陶宛", 2, 4),
        "9956" to Triple("立陶宛", 2, 4),
        "9957" to Triple("约旦", 2, 4),
        "9958" to Triple("约旦", 2, 4),
        "9959" to Triple("约旦", 2, 4),
        "9960" to Triple("沙特阿拉伯", 2, 4),
        "9961" to Triple("沙特阿拉伯", 2, 4),
        "9962" to Triple("沙特阿拉伯", 2, 4),
        "9963" to Triple("叙利亚", 2, 4),
        "9964" to Triple("叙利亚", 2, 4),
        "9965" to Triple("乌兹别克斯坦", 2, 4),
        "9966" to Triple("乌兹别克斯坦", 2, 4),
        "9967" to Triple("吉尔吉斯斯坦", 2, 4),
        "9968" to Triple("吉尔吉斯斯坦", 2, 4),
        "9969" to Triple("蒙古", 2, 4),
        "9970" to Triple("蒙古", 2, 4),
        "9971" to Triple("蒙古", 2, 4),
        "9972" to Triple("蒙古", 2, 4),
        "9973" to Triple("阿尔巴尼亚", 2, 4),
        "9974" to Triple("阿尔巴尼亚", 2, 4),
        "9975" to Triple("摩尔多瓦", 2, 4),
        "9976" to Triple("摩尔多瓦", 2, 4),
        "9977" to Triple("塔吉克斯坦", 2, 4),
        "9978" to Triple("塔吉克斯坦", 2, 4),
        "9979" to Triple("冰岛", 2, 4),
        "9980" to Triple("冰岛", 2, 4),
        "9981" to Triple("冰岛", 2, 4),
        "9982" to Triple("冰岛", 2, 4),
        "9983" to Triple("土库曼斯坦", 2, 4),
        "9984" to Triple("土库曼斯坦", 2, 4),
        "9985" to Triple("拉脱维亚", 2, 4),
        "9986" to Triple("拉脱维亚", 2, 4),
        "9987" to Triple("拉脱维亚", 2, 4),
        "9988" to Triple("阿塞拜疆", 2, 4),
        "9989" to Triple("阿塞拜疆", 2, 4),
        "99901" to Triple("巴林", 1, 3),
        "99902" to Triple("巴林", 1, 3),
        "99903" to Triple("巴林", 1, 3),
        "99904" to Triple("卡塔尔", 1, 3),
        "99905" to Triple("卡塔尔", 1, 3),
        "99906" to Triple("卡塔尔", 1, 3),
        "99907" to Triple("科威特", 1, 3),
        "99908" to Triple("科威特", 1, 3),
        "99909" to Triple("科威特", 1, 3),
        "99910" to Triple("阿联酋", 1, 3),
        "99911" to Triple("阿联酋", 1, 3),
        "99912" to Triple("阿联酋", 1, 3),
        "99913" to Triple("阿曼", 1, 3),
        "99914" to Triple("阿曼", 1, 3),
        "99915" to Triple("阿曼", 1, 3),
        "99916" to Triple("也门", 1, 3),
        "99917" to Triple("也门", 1, 3),
        "99918" to Triple("也门", 1, 3),
        "99919" to Triple("伊拉克", 1, 3),
        "99920" to Triple("伊拉克", 1, 3),
        "99921" to Triple("伊拉克", 1, 3),
        "99922" to Triple("黎巴嫩", 1, 3),
        "99923" to Triple("黎巴嫩", 1, 3),
        "99924" to Triple("黎巴嫩", 1, 3),
        "99925" to Triple("巴勒斯坦", 1, 3),
        "99926" to Triple("巴勒斯坦", 1, 3),
        "99927" to Triple("阿富汗", 1, 3),
        "99928" to Triple("阿富汗", 1, 3),
        "99929" to Triple("阿富汗", 1, 3),
        "99930" to Triple("阿富汗", 1, 3)
    )
    
    /**
     * 清理 ISBN 字符串，移除所有非数字字符（保留 X）
     */
    fun cleanISBN(isbn: String): String {
        return isbn.uppercase().filter { it.isDigit() || it == 'X' }
    }
    
    /**
     * 检测 ISBN 类型
     */
    fun detectType(isbn: String): ISBNType {
        val cleaned = cleanISBN(isbn)
        return when (cleaned.length) {
            10 -> ISBNType.ISBN_10
            13 -> ISBNType.ISBN_13
            else -> ISBNType.INVALID
        }
    }
    
    /**
     * 验证 ISBN-10 校验位
     * 校验位计算：sum(digit[i] * (10-i)) mod 11
     * 最后一位可以是 0-9 或 X（表示 10）
     */
    fun validateISBN10(isbn: String): Boolean {
        val cleaned = cleanISBN(isbn)
        if (cleaned.length != 10) return false
        
        // 检查前9位是否都是数字
        if (!cleaned.take(9).all { it.isDigit() }) return false
        
        // 检查最后一位
        val lastChar = cleaned[9]
        if (!lastChar.isDigit() && lastChar != 'X') return false
        
        // 计算校验位
        var sum = 0
        for (i in 0 until 9) {
            sum += (cleaned[i] - '0') * (10 - i)
        }
        
        val checkDigit = if (lastChar == 'X') 10 else (lastChar - '0')
        sum += checkDigit
        
        return sum % 11 == 0
    }
    
    /**
     * 验证 ISBN-13 校验位
     * 校验位计算：sum = sum(digit[i] * (1 if i is even else 3))
     * checkDigit = (10 - (sum % 10)) % 10
     */
    fun validateISBN13(isbn: String): Boolean {
        val cleaned = cleanISBN(isbn)
        if (cleaned.length != 13) return false
        
        // 检查是否都是数字
        if (!cleaned.all { it.isDigit() }) return false
        
        // 检查前缀是否有效
        val prefix = cleaned.take(3)
        if (prefix != ISBN_13_PREFIX_BOOKLAND && prefix != ISBN_13_PREFIX_OTHER) {
            return false
        }
        
        // 计算校验位
        var sum = 0
        for (i in 0 until 12) {
            val digit = cleaned[i] - '0'
            sum += digit * if (i % 2 == 0) 1 else 3
        }
        
        val checkDigit = (10 - (sum % 10)) % 10
        return cleaned[12] - '0' == checkDigit
    }
    
    /**
     * 验证 ISBN（自动检测类型）
     */
    fun validate(isbn: String): Boolean {
        val type = detectType(isbn)
        return when (type) {
            ISBNType.ISBN_10 -> validateISBN10(isbn)
            ISBNType.ISBN_13 -> validateISBN13(isbn)
            ISBNType.INVALID -> false
        }
    }
    
    /**
     * 计算 ISBN-10 校验位
     */
    fun calculateISBN10CheckDigit(isbn9: String): Char {
        val cleaned = cleanISBN(isbn9)
        require(cleaned.length == 9) { "需要 9 位数字" }
        
        var sum = 0
        for (i in cleaned.indices) {
            sum += (cleaned[i] - '0') * (10 - i)
        }
        
        val checkDigit = (11 - (sum % 11)) % 11
        return if (checkDigit == 10) 'X' else ('0' + checkDigit)
    }
    
    /**
     * 计算 ISBN-13 校验位
     */
    fun calculateISBN13CheckDigit(isbn12: String): Char {
        val cleaned = cleanISBN(isbn12)
        require(cleaned.length == 12) { "需要 12 位数字" }
        require(cleaned.all { it.isDigit() }) { "只能包含数字" }
        
        var sum = 0
        for (i in cleaned.indices) {
            val digit = cleaned[i] - '0'
            sum += digit * if (i % 2 == 0) 1 else 3
        }
        
        val checkDigit = (10 - (sum % 10)) % 10
        return '0' + checkDigit
    }
    
    /**
     * ISBN-10 转换为 ISBN-13
     */
    fun convertToISBN13(isbn10: String): String? {
        if (!validateISBN10(isbn10)) return null
        
        val cleaned = cleanISBN(isbn10)
        val isbn12 = ISBN_13_PREFIX_BOOKLAND + cleaned.take(9)
        val checkDigit = calculateISBN13CheckDigit(isbn12)
        
        return isbn12 + checkDigit
    }
    
    /**
     * ISBN-13 转换为 ISBN-10
     * 注意：只有以 978 开头的 ISBN-13 才能转换为 ISBN-10
     */
    fun convertToISBN10(isbn13: String): String? {
        if (!validateISBN13(isbn13)) return null
        
        val cleaned = cleanISBN(isbn13)
        
        // 只有 978 前缀的可以转换
        if (!cleaned.startsWith(ISBN_13_PREFIX_BOOKLAND)) {
            return null
        }
        
        val isbn9 = cleaned.substring(3, 12)
        val checkDigit = calculateISBN10CheckDigit(isbn9)
        
        return isbn9 + checkDigit
    }
    
    /**
     * 格式化 ISBN-10
     * 格式：X-XXXXX-XXX-X
     */
    fun formatISBN10(isbn: String): String {
        val cleaned = cleanISBN(isbn)
        if (cleaned.length != 10) return isbn
        
        // 标准 ISBN-10 格式：组号-出版者号-书名号-校验位
        // 这里使用常见的简化格式
        return "${cleaned[0]}-${cleaned.substring(1, 6)}-${cleaned.substring(6, 9)}-${cleaned[9]}"
    }
    
    /**
     * 格式化 ISBN-13
     * 格式：XXX-X-XXXXX-XXX-X
     */
    fun formatISBN13(isbn: String): String {
        val cleaned = cleanISBN(isbn)
        if (cleaned.length != 13) return isbn
        
        // 标准 ISBN-13 格式：前缀-组号-出版者号-书名号-校验位
        return "${cleaned.substring(0, 3)}-${cleaned[3]}-${cleaned.substring(4, 9)}-${cleaned.substring(9, 12)}-${cleaned[12]}"
    }
    
    /**
     * 格式化 ISBN（自动检测类型）
     */
    fun format(isbn: String): String {
        val type = detectType(isbn)
        return when (type) {
            ISBNType.ISBN_10 -> formatISBN10(isbn)
            ISBNType.ISBN_13 -> formatISBN13(isbn)
            ISBNType.INVALID -> isbn
        }
    }
    
    /**
     * 尝试识别注册组
     */
    private fun identifyRegistrationGroup(isbnWithoutPrefix: String): Pair<String, String?>? {
        // 尝试匹配注册组（从长到短）
        for (len in 5 downTo 1) {
            if (len > isbnWithoutPrefix.length) continue
            val prefix = isbnWithoutPrefix.take(len)
            registrationGroups[prefix]?.let { (name, _, _) ->
                return Pair(prefix, name)
            }
        }
        return null
    }
    
    /**
     * 解析 ISBN 并提取详细信息
     */
    fun parse(isbn: String): ISBNInfo {
        val cleaned = cleanISBN(isbn)
        val type = detectType(isbn)
        val isValid = validate(isbn)
        
        if (!isValid || type == ISBNType.INVALID) {
            return ISBNInfo(
                type = type,
                original = isbn,
                formatted = format(isbn),
                isValid = false,
                prefix = null,
                registrationGroup = null,
                registrant = null,
                publication = null,
                checkDigit = null,
                isbn10 = null,
                isbn13 = null
            )
        }
        
        return when (type) {
            ISBNType.ISBN_10 -> {
                val checkDigit = cleaned[9]
                val groupInfo = identifyRegistrationGroup(cleaned)
                
                ISBNInfo(
                    type = type,
                    original = isbn,
                    formatted = formatISBN10(cleaned),
                    isValid = true,
                    prefix = null,
                    registrationGroup = groupInfo?.first,
                    registrant = cleaned.substring(groupInfo?.first?.length ?: 1, 9).take(4),
                    publication = cleaned.substring((groupInfo?.first?.length ?: 1) + 4, 9),
                    checkDigit = checkDigit,
                    isbn10 = cleaned,
                    isbn13 = convertToISBN13(cleaned)
                )
            }
            ISBNType.ISBN_13 -> {
                val prefix = cleaned.take(3)
                val checkDigit = cleaned[12]
                val withoutPrefix = cleaned.substring(3, 12)
                val groupInfo = identifyRegistrationGroup(withoutPrefix)
                
                ISBNInfo(
                    type = type,
                    original = isbn,
                    formatted = formatISBN13(cleaned),
                    isValid = true,
                    prefix = prefix,
                    registrationGroup = groupInfo?.first,
                    registrant = withoutPrefix.substring(groupInfo?.first?.length ?: 1).take(4),
                    publication = withoutPrefix.substring((groupInfo?.first?.length ?: 1) + 4),
                    checkDigit = checkDigit,
                    isbn10 = if (prefix == ISBN_13_PREFIX_BOOKLAND) convertToISBN10(cleaned) else null,
                    isbn13 = cleaned
                )
            }
            ISBNType.INVALID -> {
                ISBNInfo(
                    type = type,
                    original = isbn,
                    formatted = isbn,
                    isValid = false,
                    prefix = null,
                    registrationGroup = null,
                    registrant = null,
                    publication = null,
                    checkDigit = null,
                    isbn10 = null,
                    isbn13 = null
                )
            }
        }
    }
    
    /**
     * 生成随机 ISBN-10
     */
    fun generateRandomISBN10(): String {
        val digits = (1..9).map { (0..9).random() }
        val isbn9 = digits.joinToString("")
        val checkDigit = calculateISBN10CheckDigit(isbn9)
        return isbn9 + checkDigit
    }
    
    /**
     * 生成随机 ISBN-13
     */
    fun generateRandomISBN13(): String {
        val prefix = listOf(ISBN_13_PREFIX_BOOKLAND, ISBN_13_PREFIX_OTHER).random()
        val digits = (1..9).map { (0..9).random() }
        val isbn12 = prefix + digits.joinToString("")
        val checkDigit = calculateISBN13CheckDigit(isbn12)
        return isbn12 + checkDigit
    }
    
    /**
     * 批量验证 ISBN 列表
     */
    fun validateBatch(isbns: List<String>): Map<String, Boolean> {
        return isbns.associateWith { validate(it) }
    }
    
    /**
     * 从文本中提取所有 ISBN
     */
    fun extractFromText(text: String): List<String> {
        // 匹配 ISBN-10 和 ISBN-13 的正则表达式
        val isbn10Regex = Regex("""\b(?:ISBN[-\s]?)?(\d{1,5}[-\s]?\d{1,7}[-\s]?\d{1,7}[-\s]?[\dX])\b""", RegexOption.IGNORE_CASE)
        val isbn13Regex = Regex("""\b(?:ISBN[-\s]?)?(\d{3}[-\s]?\d{1,5}[-\s]?\d{1,7}[-\s]?\d{1,7}[-\s]?\d)\b""", RegexOption.IGNORE_CASE)
        
        val results = mutableListOf<String>()
        
        // 提取并验证 ISBN-13
        isbn13Regex.findAll(text).forEach { match ->
            val cleaned = cleanISBN(match.groupValues[1])
            if (cleaned.length == 13 && validateISBN13(cleaned)) {
                results.add(cleaned)
            }
        }
        
        // 提取并验证 ISBN-10
        isbn10Regex.findAll(text).forEach { match ->
            val cleaned = cleanISBN(match.groupValues[1])
            if (cleaned.length == 10 && validateISBN10(cleaned)) {
                results.add(cleaned)
            }
        }
        
        return results.distinct()
    }
    
    /**
     * 比较两个 ISBN 是否相同（忽略格式差异）
     */
    fun areEquivalent(isbn1: String, isbn2: String): Boolean {
        val type1 = detectType(isbn1)
        val type2 = detectType(isbn2)
        
        if (type1 == ISBNType.INVALID || type2 == ISBNType.INVALID) return false
        
        // 统一转换为 ISBN-13 进行比较
        val isbn13_1 = if (type1 == ISBNType.ISBN_10) convertToISBN13(isbn1) else cleanISBN(isbn1)
        val isbn13_2 = if (type2 == ISBNType.ISBN_10) convertToISBN13(isbn2) else cleanISBN(isbn2)
        
        return isbn13_1 == isbn13_2
    }
    
    /**
     * 获取 ISBN 信息摘要（用于显示）
     */
    fun getSummary(isbn: String): String {
        val info = parse(isbn)
        
        if (!info.isValid) {
            return "无效的 ISBN: ${info.original}"
        }
        
        val sb = StringBuilder()
        sb.appendLine("ISBN 信息:")
        sb.appendLine("  类型: ${if (info.type == ISBNType.ISBN_10) "ISBN-10" else "ISBN-13"}")
        sb.appendLine("  原始: ${info.original}")
        sb.appendLine("  格式化: ${info.formatted}")
        
        info.prefix?.let {
            sb.appendLine("  GS1 前缀: $it")
        }
        
        info.registrationGroup?.let { group ->
            val regionName = identifyRegistrationGroup(
                if (info.type == ISBNType.ISBN_13) {
                    cleanISBN(isbn).substring(3)
                } else {
                    cleanISBN(isbn)
                }
            )?.second ?: "未知"
            sb.appendLine("  注册组: $group ($regionName)")
        }
        
        info.registrant?.let {
            sb.appendLine("  出版者代码: $it")
        }
        
        info.publication?.let {
            sb.appendLine("  出版物代码: $it")
        }
        
        info.checkDigit?.let {
            sb.appendLine("  校验位: $it")
        }
        
        info.isbn10?.let {
            sb.appendLine("  ISBN-10: $it")
        }
        
        info.isbn13?.let {
            sb.appendLine("  ISBN-13: $it")
        }
        
        return sb.toString().trimEnd()
    }
}

/**
 * 扩展函数：快速验证 ISBN
 */
fun String.isValidISBN(): Boolean = ISBNUtils.validate(this)

/**
 * 扩展函数：快速格式化 ISBN
 */
fun String.formatISBN(): String = ISBNUtils.format(this)

/**
 * 扩展函数：快速解析 ISBN
 */
fun String.parseISBN(): ISBNInfo = ISBNUtils.parse(this)