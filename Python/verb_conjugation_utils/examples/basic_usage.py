"""
Verb Conjugation Utils - 使用示例
"""

import sys
sys.path.insert(0, '..')
from mod import (
    Language, Tense, Person, Mood,
    get_verb_info, conjugate, conjugate_all_forms,
    is_irregular_verb, list_irregular_verbs,
    get_participle_forms, get_past_forms,
    generate_verb_table, detect_verb_type,
    create_sentence, suggest_spelling, compare_verbs,
)

print("\n========== Verb Conjugation Utils Examples ==========\n")

# ==================== 基本变位示例 ====================

print("--- 1. Basic Conjugation Examples ---\n")

# 现在简单时
print("Present Simple:")
print(f"  I walk: {conjugate('walk', Tense.PRESENT_SIMPLE, Person.FIRST_SINGULAR).conjugated}")
print(f"  He walks: {conjugate('walk', Tense.PRESENT_SIMPLE, Person.THIRD_SINGULAR).conjugated}")
print(f"  They go: {conjugate('go', Tense.PRESENT_SIMPLE, Person.THIRD_PLURAL).conjugated}")
print(f"  She tries: {conjugate('try', Tense.PRESENT_SIMPLE, Person.THIRD_SINGULAR).conjugated}")
print()

# 过去简单时
print("Past Simple:")
print(f"  I walked: {conjugate('walk', Tense.PAST_SIMPLE, Person.FIRST_SINGULAR).conjugated}")
print(f"  I went: {conjugate('go', Tense.PAST_SIMPLE, Person.FIRST_SINGULAR).conjugated}")
print(f"  I was: {conjugate('be', Tense.PAST_SIMPLE, Person.FIRST_SINGULAR).conjugated}")
print(f"  They were: {conjugate('be', Tense.PAST_SIMPLE, Person.THIRD_PLURAL).conjugated}")
print()

# 现在进行时
print("Present Continuous:")
print(f"  I am walking: {conjugate('walk', Tense.PRESENT_CONTINUOUS, Person.FIRST_SINGULAR).conjugated}")
print(f"  She is working: {conjugate('work', Tense.PRESENT_CONTINUOUS, Person.THIRD_SINGULAR).conjugated}")
print(f"  They are reading: {conjugate('read', Tense.PRESENT_CONTINUOUS, Person.THIRD_PLURAL).conjugated}")
print()

# 现在完成时
print("Present Perfect:")
print(f"  I have walked: {conjugate('walk', Tense.PRESENT_PERFECT, Person.FIRST_SINGULAR).conjugated}")
print(f"  She has gone: {conjugate('go', Tense.PRESENT_PERFECT, Person.THIRD_SINGULAR).conjugated}")
print(f"  He has written: {conjugate('write', Tense.PRESENT_PERFECT, Person.THIRD_SINGULAR).conjugated}")
print()

# 将来时
print("Future Simple & Continuous:")
print(f"  I will walk: {conjugate('walk', Tense.FUTURE_SIMPLE, Person.FIRST_SINGULAR).conjugated}")
print(f"  I will be walking: {conjugate('walk', Tense.FUTURE_CONTINUOUS, Person.FIRST_SINGULAR).conjugated}")
print(f"  I will have walked: {conjugate('walk', Tense.FUTURE_PERFECT, Person.FIRST_SINGULAR).conjugated}")
print()

# ==================== 否定和疑问形式 ====================

print("--- 2. Negative and Interrogative Forms ---\n")

# 否定形式
print("Negative Forms:")
result = conjugate("walk", Tense.PRESENT_SIMPLE, Person.FIRST_SINGULAR, negative=True)
print(f"  I do not walk: {result.negative}")

result = conjugate("walk", Tense.PRESENT_SIMPLE, Person.THIRD_SINGULAR, negative=True)
print(f"  She does not walk: {result.negative}")

result = conjugate("walk", Tense.PAST_SIMPLE, Person.FIRST_SINGULAR, negative=True)
print(f"  I did not walk: {result.negative}")

result = conjugate("walk", Tense.PRESENT_PERFECT, Person.FIRST_SINGULAR, negative=True)
print(f"  I have not walked: {result.negative}")

result = conjugate("walk", Tense.FUTURE_SIMPLE, Person.FIRST_SINGULAR, negative=True)
print(f"  I will not walk: {result.negative}")
print()

# 疑问形式
print("Interrogative Forms:")
result = conjugate("walk", Tense.PRESENT_SIMPLE, Person.FIRST_SINGULAR, interrogative=True)
print(f"  Do I walk?: {result.interrogative}")

result = conjugate("walk", Tense.PRESENT_SIMPLE, Person.THIRD_SINGULAR, interrogative=True)
print(f"  Does she walk?: {result.interrogative}")

result = conjugate("walk", Tense.PAST_SIMPLE, Person.FIRST_SINGULAR, interrogative=True)
print(f"  Did I walk?: {result.interrogative}")

result = conjugate("walk", Tense.PRESENT_PERFECT, Person.FIRST_SINGULAR, interrogative=True)
print(f"  Have I walked?: {result.interrogative}")
print()

# ==================== 动词信息 ====================

print("--- 3. Verb Information ---\n")

# 不规则动词
print("Irregular Verb 'go':")
info = get_verb_info("go")
print(f"  Infinitive: {info.infinitive}")
print(f"  Past Simple: {info.past_simple}")
print(f"  Past Participle: {info.past_participle}")
print(f"  Present Participle: {info.present_participle}")
print(f"  Third Person Singular: {info.third_person_singular}")
print(f"  Is Irregular: {info.is_irregular}")
print()

# 规则动词
print("Regular Verb 'create':")
info = get_verb_info("create")
print(f"  Infinitive: {info.infinitive}")
print(f"  Past Simple: {info.past_simple}")
print(f"  Past Participle: {info.past_participle}")
print(f"  Present Participle: {info.present_participle}")
print(f"  Third Person Singular: {info.third_person_singular}")
print(f"  Is Regular: {info.is_regular}")
print()

# ==================== 所有变位形式 ====================

print("--- 4. All Conjugation Forms ---\n")

forms = conjugate_all_forms("write")
print("Verb 'write' - Selected forms:")
print(f"  Present Simple (I): {forms['present_simple']['first_singular']['conjugated']}")
print(f"  Present Simple (She): {forms['present_simple']['third_singular']['conjugated']}")
print(f"  Past Simple (I): {forms['past_simple']['first_singular']['conjugated']}")
print(f"  Present Continuous (I): {forms['present_continuous']['first_singular']['conjugated']}")
print(f"  Present Perfect (I): {forms['present_perfect']['first_singular']['conjugated']}")
print(f"  Future Simple (I): {forms['future_simple']['first_singular']['conjugated']}")
print(f"  Conditional (I): {forms['conditional']['first_singular']['conjugated']}")
print()

# ==================== 不规则动词列表 ====================

print("--- 5. Irregular Verbs List ---\n")

verbs = list_irregular_verbs()
print(f"Total irregular verbs in database: {len(verbs)}")
print("\nFirst 15 irregular verbs:")
for i, v in enumerate(verbs[:15], 1):
    print(f"  {i}. {v.infinitive}: {v.past_simple} / {v.past_participle}")
print()

# ==================== 句子创建 ====================

print("--- 6. Sentence Creation ---\n")

print("Simple sentences:")
print(f"  {create_sentence('write', Tense.PRESENT_SIMPLE, Person.FIRST_SINGULAR)}")
print(f"  {create_sentence('write', Tense.PRESENT_SIMPLE, Person.THIRD_SINGULAR)}")
print(f"  {create_sentence('write', Tense.PAST_SIMPLE, Person.FIRST_SINGULAR)}")
print()

print("With custom subject:")
print(f"  {create_sentence('write', Tense.PRESENT_SIMPLE, Person.FIRST_SINGULAR, subject='John')}")
print(f"  {create_sentence('write', Tense.PAST_SIMPLE, Person.THIRD_SINGULAR, subject='Mary')}")
print()

print("With object:")
print(f"  {create_sentence('write', Tense.PRESENT_SIMPLE, Person.FIRST_SINGULAR, object='a letter')}")
print(f"  {create_sentence('read', Tense.PAST_SIMPLE, Person.THIRD_SINGULAR, subject='She', object='the book')}")
print()

print("Negative sentences:")
print(f"  {create_sentence('write', Tense.PRESENT_SIMPLE, Person.FIRST_SINGULAR, negative=True)}")
print(f"  {create_sentence('write', Tense.PRESENT_SIMPLE, Person.THIRD_SINGULAR, subject='She', object='emails', negative=True)}")
print()

print("Interrogative sentences:")
print(f"  {create_sentence('write', Tense.PRESENT_SIMPLE, Person.FIRST_SINGULAR, interrogative=True)}")
print(f"  {create_sentence('write', Tense.PRESENT_PERFECT, Person.THIRD_SINGULAR, object='the report', interrogative=True)}")
print()

# ==================== 动词类型检测 ====================

print("--- 7. Verb Type Detection ---\n")

verbs_to_check = ["work", "go", "be", "can", "stop"]
for verb in verbs_to_check:
    type_info = detect_verb_type(verb)
    print(f"Verb '{verb}':")
    print(f"  Is Auxiliary: {type_info['is_auxiliary']}")
    print(f"  Is Irregular: {type_info['is_irregular']}")
    print(f"  Is Regular: {type_info['is_regular']}")
    print(f"  Is Transitive: {type_info['is_transitive']}")
    print(f"  Ends with E: {type_info['ending']['ends_with_e']}")
    print(f"  Is CVC Pattern: {type_info['ending']['is_cvc_pattern']}")
    print()

# ==================== 拼写建议 ====================

print("--- 8. Spelling Suggestions ---\n")

test_inputs = ["ga", "hav", "wrk", "b", "go"]
for input_word in test_inputs:
    suggestions = suggest_spelling(input_word)
    print(f"Input '{input_word}': Suggestions = {suggestions}")
print()

# ==================== 动词比较 ====================

print("--- 9. Verb Comparison ---\n")

comparison = compare_verbs("go", "walk")
print(f"Compare 'go' and 'walk':")
print(f"  Both irregular: {comparison['same_irregularity']}")
print(f"  Same past form: {comparison['same_past_form']}")
print(f"  Same participle: {comparison['same_participle']}")
print()

comparison = compare_verbs("have", "make")
print(f"Compare 'have' and 'make':")
print(f"  Both irregular: {comparison['same_irregularity']}")
print(f"  Same past form: {comparison['same_past_form']}")
print(f"  Same participle: {comparison['same_participle']}")
print()

# ==================== 变位表格 ====================

print("--- 10. Verb Conjugation Table ---\n")

# 生成一个简化版的表格（只显示部分）
print(generate_verb_table("be")[:500] + "...")
print()

print("\n========== Examples Complete ==========\n")