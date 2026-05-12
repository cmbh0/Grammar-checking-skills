# 代码语法验证与自动修复技能

## 概述

这是一个强大的代码语法验证与自动修复工具，能够智能检测代码错误、自动修复常见问题，并维护一个错误库来学习和避免重复犯错。

## 功能特性

- ✅ **多语言支持**：支持 JavaScript、TypeScript、Python、Java、Go、Rust、C、C++、C#、Ruby、PHP、Dart、Kotlin、Swift、R、Scala、Haskell、Lua、Perl、Shell 等多种编程语言
- ✅ **智能语法检查**：自动检测代码中的语法错误和常见问题
- ✅ **自动修复**：能够自动修复常见的代码问题
- ✅ **错误库学习**：记录所有错误，自动学习修复模式
- ✅ **相似错误识别**：基于历史数据提供智能修复建议
- ✅ **迭代修复**：支持多轮验证和修复，直到代码无错误

## 目录结构

```
/workspace/.solo/skills/code-validator/
├── skill.json              # 技能配置文件
├── code_validator.py       # Python 主程序（推荐使用）
├── code_validator.sh       # Bash 备用脚本
├── error_library.json      # 错误库（自动生成）
├── validator_config.json   # 验证配置（自动生成）
└── README.md               # 本文档
```

## 快速开始

### 方式一：使用 Python 版本（推荐）

```bash
cd /workspace/.solo/skills/code-validator
python3 code_validator.py validate [项目目录]
```

### 方式二：使用 Bash 版本

```bash
cd /workspace/.solo/skills/code-validator
./code_validator.sh validate [项目目录]
```

## 使用命令

### 1. 验证整个项目

验证当前目录或指定目录下的所有代码文件：

```bash
python3 code_validator.py validate
python3 code_validator.py validate ./my-project
```

**工作流程：**
1. 自动检测项目语言类型
2. 收集所有源文件
3. 进行多轮语法检查
4. 发现错误后尝试自动修复
5. 将错误记录到错误库
6. 重复直到所有错误修复或达到最大迭代次数

### 2. 检查单个文件

检查指定文件的语法：

```bash
python3 code_validator.py check src/app.js
python3 code_validator.py check tests/test_module.py
```

### 3. 查看错误库状态

查看已记录的错误和修复历史：

```bash
python3 code_validator.py library
```

**输出示例：**
```
📊 错误库统计
==================================================
总错误数: 42
最后更新: 2026-05-12T10:30:00Z

按分类统计:
  • syntax: 25 个
  • semantic: 12 个
  • style: 5 个

按错误类型统计:
  • syntax_error: 20 次
  • undefined_reference: 12 次
  • indentation_error: 5 次

最近修复记录:
  ✅ src/utils.js - 2026-05-12T10:25:00Z
  ✅ src/components/App.tsx - 2026-05-12T10:20:00Z
```

### 4. 清空错误库

如果需要重新开始，可以清空错误库：

```bash
python3 code_validator.py clear-library
```

## 错误库机制

### 工作原理

1. **自动记录**：每次发现错误时，自动添加到错误库
2. **智能分类**：错误按类型分类（syntax、style、semantic、logical）
3. **修复建议**：每种错误都有对应的修复建议
4. **学习能力**：记录修复历史，逐渐学习最佳的修复方式

### 错误库数据结构

```json
{
  "version": "1.0.0",
  "created_at": "2026-05-12T08:00:00Z",
  "last_updated": "2026-05-12T10:30:00Z",
  "total_errors": 42,
  "categories": {
    "syntax": [...],
    "style": [...],
    "semantic": [...],
    "logical": [...]
  },
  "recent_fixes": [...],
  "statistics": {
    "by_language": {},
    "by_error_type": {}
  }
}
```

### 错误条目

每个错误记录包含：
- **id**：唯一标识符
- **file**：发生错误的文件
- **error_type**：错误类型（syntax_error、undefined_reference 等）
- **error_message**：原始错误信息
- **fix_suggestion**：修复建议
- **category**：错误分类
- **timestamp**：发现时间
- **fix_count**：修复次数
- **success_rate**：修复成功率

## 自动修复能力

### JavaScript/TypeScript
- 去除末尾空白字符
- 修复双分号问题
- 修复对象/数组末尾多余逗号
- 统一引号格式

### Python
- Tab 缩进转换为空格
- 去除末尾空白字符
- 修复常见的 PEP8 风格问题

### Dart
- 去除末尾空白字符
- 修复双分号问题

### Kotlin
- 去除末尾空白字符
- 修复双分号问题

### Swift
- 去除末尾空白字符

### Lua
- 去除末尾空白字符

### Perl
- 去除末尾空白字符

### Shell
- 去除末尾空白字符
- Tab 缩进转换为空格

### C/C++
- 去除末尾空白字符

### C#
- 去除末尾空白字符

### Ruby
- 去除末尾空白字符

### PHP
- 去除末尾空白字符

### Go
- 基本的语法检查和格式化

### Rust
- 编译时错误检测

## 配置选项

配置文件 `validator_config.json` 包含以下选项：

```json
{
  "auto_fix": true,              // 是否自动修复
  "max_iterations": 5,           // 最大迭代次数
  "severity_threshold": "warning",
  "exclude_patterns": [
    "node_modules/*",
    "dist/*",
    "build/*"
  ],
  "language_settings": {
    "javascript": {
      "linter": "eslint",
      "auto_fix_rules": true
    },
    "python": {
      "linter": "pylint",
      "auto_fix_rules": false
    }
  }
}
```

## 使用示例

### 示例 1：验证新项目

```bash
# 创建示例项目
mkdir my-project && cd my-project

# 创建测试文件
cat > app.js << 'EOF'
function greet(name {
    console.log(`Hello, ${name}`);
}

const data = [1, 2, 3, ];
module.exports = { greet, data };
EOF

# 运行验证
python3 ../code_validator.py validate

# 输出示例
[INFO] 开始验证项目: /workspace/my-project
[INFO] 检测到语言: javascript
[INFO] 找到 1 个源文件
[INFO] === 第 1 轮验证 ===
[ERROR] /workspace/my-project/app.js: 语法错误
[SUCCESS] 已自动修复: /workspace/my-project/app.js (3 处)
[INFO] === 第 2 轮验证 ===
[SUCCESS] 语法检查通过: /workspace/my-project/app.js
[SUCCESS] 所有文件验证通过！
```

### 示例 2：检查特定文件

```bash
python3 code_validator.py check src/components/Button.tsx
```

### 示例 3：集成到开发流程

可以将验证集成到项目中：

**package.json 脚本：**
```json
{
  "scripts": {
    "validate": "python3 ../.solo/skills/code-validator/code_validator.py validate",
    "check": "python3 ../.solo/skills/code-validator/code_validator.py check"
  }
}
```

**Git Hooks (pre-commit)：**
```bash
#!/bin/bash
# .git/hooks/pre-commit
python3 ../.solo/skills/code-validator/code_validator.py validate || exit 1
```

## 高级用法

### 1. 自定义验证配置

创建 `validator_config.json` 来自定义验证行为：

```json
{
  "auto_fix": true,
  "max_iterations": 10,
  "exclude_patterns": [
    "node_modules/*",
    "*.test.js",
    "dist/*"
  ]
}
```

### 2. 批量验证多个项目

```bash
#!/bin/bash
# 批量验证脚本
for project in project1 project2 project3; do
    echo "验证 $project..."
    python3 code_validator.py validate ./$project
done
```

### 3. CI/CD 集成

**GitHub Actions 示例：**
```yaml
name: Code Validation
on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.x'
      - name: Run validation
        run: |
          python3 .solo/skills/code-validator/code_validator.py validate
```

## 常见问题

### Q: 如何处理不支持的语言？

A: 当前版本支持主流编程语言。对于不支持的语言，会给出提示。可以根据错误信息手动修复。

### Q: 错误库会无限增长吗？

A: 可以配置最大条目数（默认1000条），超出后会清理旧的记录。也可以随时使用 `clear-library` 命令清空。

### Q: 自动修复会破坏代码吗？

A: 自动修复只针对安全的、确定的问题（如空白字符、末尾逗号等）。对于可能导致问题的修改，只会提供建议而不自动修改。

### Q: 如何查看具体的修复历史？

A: 使用 `library` 命令可以查看最近的修复记录。详细的修复历史存储在 `error_library.json` 文件中。

## 技术细节

### 依赖要求

- Python 3.6+
- Node.js（用于 JavaScript/TypeScript 验证，可选）
- 标准 Unix 工具（grep、sed 等，Bash 版本需要）

### 性能考虑

- 大型项目建议使用 Python 版本
- 可以通过调整 `max_iterations` 控制验证深度
- 使用 `exclude_patterns` 排除不需要验证的文件

### 错误库存储位置

- 默认位置：`/workspace/.solo/skills/code-validator/error_library.json`
- 可以通过修改脚本调整存储位置

## 贡献指南

欢迎贡献代码！请确保：

1. 添加新语言支持时更新 `skill.json`
2. 保持代码风格一致
3. 添加相应的测试
4. 更新文档
