"""
Classical Cipher Utils - 使用示例

展示各种古典密码的使用方法。
"""

from mod import (
    CaesarCipher, ROT13, AtbashCipher, VigenereCipher,
    AffineCipher, PlayfairCipher, RailFenceCipher,
    ColumnarTranspositionCipher, SimpleSubstitutionCipher,
    PolybiusSquareCipher,
    caesar_encrypt, caesar_decrypt, rot13, atbash,
    vigenere_encrypt, vigenere_decrypt,
    affine_encrypt, affine_decrypt,
    rail_fence_encrypt, rail_fence_decrypt,
    playfair_encrypt, playfair_decrypt
)


def print_section(title):
    """打印分节标题"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)


def demo_caesar():
    """凯撒密码演示"""
    print_section("凯撒密码 (Caesar Cipher)")
    
    text = "HELLO WORLD"
    shift = 3
    
    print(f"原文: {text}")
    print(f"位移: {shift}")
    
    encrypted = CaesarCipher.encrypt(text, shift)
    print(f"加密: {encrypted}")
    
    decrypted = CaesarCipher.decrypt(encrypted, shift)
    print(f"解密: {decrypted}")
    
    # 暴力破解
    print("\n暴力破解演示（前5个结果）:")
    results = CaesarCipher.brute_force(encrypted)
    for shift, decrypted in results[:5]:
        print(f"  位移 {shift:2d}: {decrypted}")
    
    # 便捷函数
    print(f"\n便捷函数: caesar_encrypt('ABC', 3) = {caesar_encrypt('ABC', 3)}")


def demo_rot13():
    """ROT13演示"""
    print_section("ROT13")
    
    text = "Python Programming"
    print(f"原文: {text}")
    
    transformed = ROT13.transform(text)
    print(f"变换: {transformed}")
    
    back = ROT13.transform(transformed)
    print(f"还原: {back}")
    
    print(f"\n便捷函数: rot13('HELLO') = {rot13('HELLO')}")


def demo_atbash():
    """埃特巴什密码演示"""
    print_section("埃特巴什密码 (Atbash Cipher)")
    
    text = "HELLO WORLD"
    print(f"原文: {text}")
    
    encrypted = AtbashCipher.encrypt(text)
    print(f"加密: {encrypted}")
    
    # 加密即解密
    decrypted = AtbashCipher.decrypt(encrypted)
    print(f"解密: {decrypted}")
    
    print(f"\n便捷函数: atbash('ABC') = {atbash('ABC')}")


def demo_vigenere():
    """维吉尼亚密码演示"""
    print_section("维吉尼亚密码 (Vigenère Cipher)")
    
    text = "ATTACKATDAWN"
    key = "LEMON"
    
    print(f"原文: {text}")
    print(f"密钥: {key}")
    
    encrypted = VigenereCipher.encrypt(text, key)
    print(f"加密: {encrypted}")
    
    decrypted = VigenereCipher.decrypt(encrypted, key)
    print(f"解密: {decrypted}")
    
    # 长密钥演示
    print("\n长密钥演示:")
    text2 = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"
    key2 = "SUPERSECRETKEY"
    encrypted2 = VigenereCipher.encrypt(text2, key2)
    print(f"  原文: {text2}")
    print(f"  密文: {encrypted2}")


def demo_affine():
    """仿射密码演示"""
    print_section("仿射密码 (Affine Cipher)")
    
    text = "AFFINE CIPHER"
    a, b = 5, 8  # a必须与26互质
    
    print(f"原文: {text}")
    print(f"参数: a={a}, b={b} (E(x) = ({a}x + {b}) mod 26)")
    print(f"有效的a值: {AffineCipher.VALID_A_VALUES}")
    
    encrypted = AffineCipher.encrypt(text, a, b)
    print(f"加密: {encrypted}")
    
    decrypted = AffineCipher.decrypt(encrypted, a, b)
    print(f"解密: {decrypted}")


def demo_playfair():
    """普莱费尔密码演示"""
    print_section("普莱费尔密码 (Playfair Cipher)")
    
    text = "HELLO WORLD"
    key = "PLAYFAIR"
    
    print(f"原文: {text}")
    print(f"密钥: {key}")
    
    encrypted = PlayfairCipher.encrypt(text, key)
    print(f"加密: {encrypted}")
    
    decrypted = PlayfairCipher.decrypt(encrypted, key)
    print(f"解密: {decrypted}")
    
    # 显示密钥矩阵
    print("\n密钥矩阵:")
    matrix = PlayfairCipher._create_matrix(key)
    for row in matrix:
        print(f"  {' '.join(row)}")


def demo_rail_fence():
    """栅栏密码演示"""
    print_section("栅栏密码 (Rail Fence Cipher)")
    
    text = "WE ARE DISCOVERED FLEE AT ONCE"
    
    for rails in [2, 3, 4]:
        encrypted = RailFenceCipher.encrypt(text, rails)
        decrypted = RailFenceCipher.decrypt(encrypted, rails)
        print(f"{rails}栏:")
        print(f"  原文: {text}")
        print(f"  密文: {encrypted}")
        print(f"  解密: {decrypted}")


def demo_columnar_transposition():
    """列置换密码演示"""
    print_section("列置换密码 (Columnar Transposition Cipher)")
    
    text = "WEAREDISCOVEREDFLEEATONCE"
    key = "ZEBRAS"
    
    print(f"原文: {text}")
    print(f"密钥: {key}")
    print(f"密钥排序: Z(6) E(2) B(1) R(4) A(3) S(5)")
    
    encrypted = ColumnarTranspositionCipher.encrypt(text, key)
    print(f"加密: {encrypted}")
    
    decrypted = ColumnarTranspositionCipher.decrypt(encrypted, key)
    print(f"解密: {decrypted}")


def demo_simple_substitution():
    """简单替换密码演示"""
    print_section("简单替换密码 (Simple Substitution Cipher)")
    
    text = "HELLO WORLD"
    key = "QWERTYUIOPASDFGHJKLZXCVBNM"
    
    print(f"原文: {text}")
    print(f"密钥: {key}")
    
    encrypted = SimpleSubstitutionCipher.encrypt(text, key)
    print(f"加密: {encrypted}")
    
    decrypted = SimpleSubstitutionCipher.decrypt(encrypted, key)
    print(f"解密: {decrypted}")


def demo_polybius():
    """波利比乌斯方阵密码演示"""
    print_section("波利比乌斯方阵密码 (Polybius Square Cipher)")
    
    text = "HELLO WORLD"
    
    print(f"原文: {text}")
    print(f"\n标准方阵 (I/J合并):")
    for i, row in enumerate(PolybiusSquareCipher.STANDARD_SQUARE):
        print(f"  {i+1}: {' '.join(row)}")
    print("    1 2 3 4 5")
    
    encrypted = PolybiusSquareCipher.encrypt(text)
    print(f"\n加密: {encrypted}")
    
    decrypted = PolybiusSquareCipher.decrypt(encrypted)
    print(f"解密: {decrypted}")


def demo_multi_layer():
    """多重加密演示"""
    print_section("多重加密演示")
    
    original = "TOP SECRET MESSAGE"
    print(f"原始消息: {original}")
    
    # 第一层：维吉尼亚
    key1 = "KEY"
    step1 = VigenereCipher.encrypt(original, key1)
    print(f"维吉尼亚加密 (key=KEY): {step1}")
    
    # 第二层：栅栏
    step2 = RailFenceCipher.encrypt(step1, 3)
    print(f"栅栏加密 (3栏): {step2}")
    
    # 第三层：凯撒
    step3 = CaesarCipher.encrypt(step2, 7)
    print(f"凯撒加密 (shift=7): {step3}")
    
    # 解密（反向）
    dec_step1 = CaesarCipher.decrypt(step3, 7)
    dec_step2 = RailFenceCipher.decrypt(dec_step1, 3)
    dec_step3 = VigenereCipher.decrypt(dec_step2, key1)
    
    print(f"\n解密结果: {dec_step3}")
    print(f"验证: {'成功' if dec_step3 == original else '失败'}")


def demo_custom_polybius():
    """自定义波利比乌斯方阵演示"""
    print_section("自定义波利比乌斯方阵")
    
    # 使用自定义关键词的方阵
    custom_square = [
        ['P', 'L', 'A', 'Y', 'F'],
        ['I', 'R', 'E', 'X', 'M'],  # J -> I
        ['B', 'C', 'D', 'G', 'H'],
        ['K', 'N', 'O', 'Q', 'S'],
        ['T', 'U', 'V', 'W', 'Z']
    ]
    
    text = "SECRET"
    print(f"原文: {text}")
    print(f"自定义方阵:")
    for i, row in enumerate(custom_square):
        print(f"  {i+1}: {' '.join(row)}")
    
    encrypted = PolybiusSquareCipher.encrypt(text, custom_square)
    print(f"\n加密: {encrypted}")
    
    decrypted = PolybiusSquareCipher.decrypt(encrypted, custom_square)
    print(f"解密: {decrypted}")


def main():
    """主函数"""
    print("\n" + "="*60)
    print("  Classical Cipher Utils - 古典密码工具使用示例")
    print("="*60)
    
    demo_caesar()
    demo_rot13()
    demo_atbash()
    demo_vigenere()
    demo_affine()
    demo_playfair()
    demo_rail_fence()
    demo_columnar_transposition()
    demo_simple_substitution()
    demo_polybius()
    demo_multi_layer()
    demo_custom_polybius()
    
    print("\n" + "="*60)
    print("  演示完成！")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()