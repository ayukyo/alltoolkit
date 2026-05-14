# DNA Utils 🧬

DNA/RNA 序列工具库 - 提供完整的生物序列操作功能。

## 功能特性

- **序列验证** - DNA/RNA 序列合法性检查
- **转录翻译** - DNA → RNA → 蛋白质
- **互补链生成** - 正向互补、反向互补
- **GC 含量** - GC 比例计算
- **密码子查询** - 遗传密码表查询
- **序列统计** - 碱基频率、序列长度等
- **突变操作** - 点突变、插入、删除
- **序列比对** - 基础比对功能

## 快速开始

```python
from dna_utils.mod import DNASequence, RNASequence, validate_dna

# 验证 DNA 序列
is_valid = validate_dna("ATCGATCG")
print(is_valid)  # True

# 创建 DNA 序列对象
dna = DNASequence("ATCGATCGATCG")

# 获取基本信息
print(f"长度: {dna.length}")
print(f"GC含量: {dna.gc_content:.2%}")

# 转录为 RNA
rna = dna.transcribe()
print(rna.sequence)  # "AUCGAUCGAUCG"

# 翻译为蛋白质
protein = rna.translate()
print(protein.sequence)  # 氨基酸序列
```

## 核心类

### DNASequence

```python
from dna_utils.mod import DNASequence

dna = DNASequence("ATCGATCG")

# 互补链
complement = dna.complement()  # "TAGCTAGC"

# 反向互补
reverse_complement = dna.reverse_complement()  # "CGATCGAT"

# GC 含量
gc = dna.gc_content  # 0.5 (50%)

# 转录
rna = dna.transcribe()
```

### RNASequence

```python
from dna_utils.mod import RNASequence

rna = RNASequence("AUCGAUCG")

# 翻译为蛋白质
protein = rna.translate()

# 获取密码子
codons = rna.get_codons()  # ["AUC", "GAU", "CG"]
```

## 主要函数

| 函数 | 说明 |
|------|------|
| `validate_dna(seq)` | 验证 DNA 序列 |
| `validate_rna(seq)` | 验证 RNA 序列 |
| `transcribe(dna)` | DNA 转录为 RNA |
| `translate(rna)` | RNA 翻译为蛋白质 |
| `complement(seq)` | 生成互补链 |
| `reverse_complement(seq)` | 生成反向互补链 |
| `gc_content(seq)` | 计算 GC 含量 |
| `codon_to_amino(codon)` | 密码子转氨基酸 |
| `amino_to_codons(amino)` | 氨基酸转密码子列表 |

## 遗传密码表

使用标准遗传密码表（Standard Genetic Code）：

```python
from dna_utils.mod import CODON_TABLE, get_amino_acid

# 查询密码子对应的氨基酸
amino = get_amino_acid("UUU")  # "F" (苯丙氨酸)
amino = get_amino_acid("AUG")  # "M" (甲硫氨酸，起始密码子)

# 终止密码子
stop_codons = ["UAA", "UAG", "UGA"]
```

## 突变操作

```python
from dna_utils.mod import mutate_point, mutate_insert, mutate_delete

# 点突变
mutated = mutate_point("ATCGATCG", position=3, new_base="G")

# 插入
mutated = mutate_insert("ATCGATCG", position=4, insert_seq="TT")

# 删除
mutated = mutate_delete("ATCGATCG", position=2, length=3)
```

## 序列统计

```python
from dna_utils.mod import SequenceStats

dna = DNASequence("ATCGATCGATCGAAATTT")
stats = SequenceStats(dna)

print(stats.base_frequency)
# {'A': 6, 'T': 5, 'C': 3, 'G': 4}

print(stats.dinucleotide_frequency)
# {'AT': 3, 'TC': 2, 'CG': 3, ...}
```

## IUPAC 模糊碱基

支持 IUPAC 编码的模糊碱基：

| 码 | 含义 | 可能碱基 |
|----|------|----------|
| R | 嘌呤 | A, G |
| Y | 嘧啶 | C, T |
| N | 任意 | A, C, G, T |
| S | 强碱基 | G, C |
| W | 弱碱基 | A, T |

## 测试

```bash
python Python/dna_utils/dna_utils_test.py
```

## 许可证

MIT License