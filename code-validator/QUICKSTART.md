# 代码语法验证技能 - 快速入门指南

## 🎯 技能简介

这是一个智能代码语法验证工具，可以：
- ✅ 自动检测并修复代码语法错误
- ✅ 维护错误库，学习常见错误模式
- ✅ 支持 20+ 种编程语言：JavaScript、TypeScript、Python、Java、Go、Rust、C、C++、C#、Ruby、PHP、Dart、Kotlin、Swift、R、Scala、Haskell、Lua、Perl、Shell
- ✅ 自动修复常见问题
- ✅ 提供修复建议

## 🚀 快速开始

### 第一步：进入技能目录

```bash
cd /workspace/.solo/skills/code-validator
```

### 第二步：运行验证

**验证整个项目：**
```bash
python3 code_validator.py validate
```

**验证指定目录：**
```bash
python3 code_validator.py validate ./你的项目目录
```

**检查单个文件：**
```bash
python3 code_validator.py check path/to/your/file.js
```

## 📖 常用命令

### 1. validate - 验证项目

```bash
# 验证当前目录
python3 code_validator.py validate

# 验证指定目录
python3 code_validator.py validate /path/to/project

# 验证并显示详细信息
python3 code_validator.py validate -v
```

**工作流程：**
1. 🔍 自动检测项目语言
2. 📁 收集所有源文件
3. 🔎 进行语法检查
4. 🔧 自动修复错误
5. 📚 记录到错误库
6. 🔄 重复直到无错误

### 2. check - 检查文件

```bash
# 检查单个文件
python3 code_validator.py check src/app.js

# 检查多个文件
python3 code_validator.py check file1.py file2.js
```

### 3. library - 查看错误库

```bash
# 查看错误统计
python3 code_validator.py library

# 查看最近的修复记录
python3 code_validator.py library --recent
```

**输出示例：**
```
📊 错误库统计
==================================================
总错误数: 15
最后更新: 2024-01-15T10:30:00

按分类统计:
  • syntax: 10 个
  • style: 3 个
  • semantic: 2 个

按错误类型统计:
  • syntax_error: 8 次
  • indentation_error: 4 次
  • undefined_reference: 3 次
```

### 4. fix - 修复文件

```bash
# 自动修复文件中的常见错误
python3 code_validator.py fix src/app.js
```

## 💡 实际使用示例

### 示例 1：验证 JavaScript 项目

```bash
# 创建测试文件
mkdir -p /workspace/test-project
cat > /workspace/test-project/app.js << 'EOF'
const greeting = "Hello"

function sayHello(name {
    console.log(`${greeting}, ${name}!`)
}

const items = [1, 2, 3, ];
module.exports = { sayHello, items };
EOF

# 运行验证
cd /workspace/.solo/skills/code-validator
python3 code_validator.py validate /workspace/test-project
```

**输出：**
```
[INFO] 开始验证项目: /workspace/test-project
[INFO] 检测到语言: javascript
[INFO] 找到 1 个源文件
[INFO] === 第 1 轮验证 ===
[ERROR] /workspace/test-project/app.js: 语法错误
[SUCCESS] 已自动修复: /workspace/test-project/app.js (3 处)
[INFO] === 第 2 轮验证 ===
[SUCCESS] 语法检查通过: /workspace/test-project/app.js
[SUCCESS] 所有文件验证通过！
```

### 示例 2：检查 Python 文件

```bash
cat > /workspace/test.py << 'EOF'
def calculate_sum(a,b):
    result = a + b
    return result

numbers = [1,2, 3, 4, ]
print(calculate_sum(10,20))
EOF

cd /workspace/.solo/skills/code-validator
python3 code_validator.py check /workspace/test.py
```

### 示例 3：检查 Dart 文件

```bash
cat > /workspace/test.dart << 'EOF'
void main() {
  String greeting = "Hello, World!";
  print(greeting);
  
  List<int> numbers = [1, 2, 3, ];
  for (var number in numbers) {
    print(number);
  }
}
EOF

cd /workspace/.solo/skills/code-validator
python3 code_validator.py check /workspace/test.dart
```

## 🔧 自动修复能力

### JavaScript/TypeScript
- ✅ 去除末尾空白字符
- ✅ 修复双分号
- ✅ 修复对象/数组末尾多余逗号
- ✅ 统一引号格式

### Python
- ✅ Tab 缩进转空格
- ✅ 去除末尾空白
- ✅ 修复常见 PEP8 问题

### Dart
- ✅ 去除末尾空白字符
- ✅ 修复双分号

### Kotlin
- ✅ 去除末尾空白字符
- ✅ 修复双分号

### Swift
- ✅ 去除末尾空白字符

### Lua
- ✅ 去除末尾空白字符

### Perl
- ✅ 去除末尾空白字符

### Shell
- ✅ 去除末尾空白字符
- ✅ Tab 缩进转空格

### C/C++
- ✅ 去除末尾空白字符

### C#
- ✅ 去除末尾空白字符

### Ruby
- ✅ 去除末尾空白字符

### PHP
- ✅ 去除末尾空白字符

## 📚 错误库功能

### 工作原理

1. **记录错误**：每次发现错误，自动记录到错误库
2. **智能分析**：分析错误类型和模式
3. **提供建议**：给出修复建议
4. **学习改进**：根据修复历史优化建议

### 查看错误库

```bash
# 查看完整统计
python3 code_validator.py library

# 查看错误库文件
cat error_library.json
```

### 错误库结构

```json
{
  "version": "1.0.0",
  "total_errors": 42,
  "categories": {
    "syntax": [...],    // 语法错误
    "style": [...],     // 风格问题
    "semantic": [...],  // 语义错误
    "logical": [...]    // 逻辑错误
  },
  "recent_fixes": [...],  // 最近修复记录
  "statistics": {...}     // 统计信息
}
```

## ⚙️ 配置选项

创建 `validator_config.json` 来自定义行为：

```json
{
  "auto_fix": true,              // 开启自动修复
  "max_iterations": 5,           // 最大修复轮次
  "exclude_patterns": [           // 排除的文件
    "node_modules/*",
    "dist/*",
    "*.test.js"
  ]
}
```

## 🎨 工作流程图

```
┌─────────────────────────────────────────┐
│  1. 输入项目路径                         │
│     python3 code_validator.py validate  │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  2. 检测项目语言                         │
│     (JS/TS/Python/Go/Rust/Java)        │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  3. 收集源文件                           │
│     (排除 node_modules 等)               │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  4. 进行语法检查                         │
│     • JavaScript → Node.js              │
│     • Python → py_compile / AST         │
│     • Go → go vet                      │
│     • 通用 → 括号/引号匹配检查           │
└──────────────┬──────────────────────────┘
               │
               ▼
        ┌──────────────┐
        │ 发现错误？    │
        └──────┬───────┘
               │
        是    │    否
        ┌─────┴─────┐
        ▼           ▼
┌───────────────┐  ┌─────────────────┐
│ 记录到错误库   │  │ ✅ 验证通过！    │
│ 提供修复建议  │  └─────────────────┘
│ 尝试自动修复  │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│ 修复后重新检查 │
│ (最多5轮)     │
└───────┬───────┘
        │
        └──────→ 重复直到无错误
```

## 🔍 常见问题

### Q1: 如何处理不支持的语言？

**A:** 当前版本支持：
- ✅ JavaScript/TypeScript
- ✅ Python
- ✅ Go
- ✅ Rust
- ✅ Java
- ✅ C/C++

对于不支持的语言，会给出提示。

### Q2: 错误库会无限增长吗？

**A:** 不会。错误库配置了最大条目数（1000条），超出后会自动清理旧记录。

### Q3: 自动修复安全吗？

**A:** 是的。自动修复只针对安全的、确定的问题：
- 空白字符
- 末尾逗号
- 括号匹配
- 缩进格式

不会修改业务逻辑代码。

### Q4: 如何重置错误库？

```bash
# 方法1：使用命令
python3 code_validator.py clear-library

# 方法2：删除文件
rm error_library.json
```

## 💻 集成到开发流程

### Git Hooks (pre-commit)

创建 `.git/hooks/pre-commit`:

```bash
#!/bin/bash
python3 /workspace/.solo/skills/code-validator/code_validator.py validate || exit 1
```

### package.json 脚本

```json
{
  "scripts": {
    "lint:code": "python3 /workspace/.solo/skills/code-validator/code_validator.py validate",
    "check": "python3 /workspace/.solo/skills/code-validator/code_validator.py check"
  }
}
```

## 📝 输出说明

### 颜色编码

- 🔵 **[INFO]** - 信息提示
- 🟢 **[SUCCESS]** - 成功消息
- 🟡 **[WARNING]** - 警告信息
- 🔴 **[ERROR]** - 错误信息

### 退出码

- `0` - 验证通过，无错误
- `1` - 存在错误或验证失败

## 🎓 高级技巧

### 1. 批量验证多个项目

```bash
#!/bin/bash
projects=("project1" "project2" "project3")

for project in "${projects[@]}"; do
    echo "验证 $project..."
    python3 code_validator.py validate ./$project
done
```

### 2. 只检查不修复

如果只想检查，不想自动修复，可以先备份错误库：

```bash
cp error_library.json error_library.json.bak
python3 code_validator.py validate
# 检查后恢复
mv error_library.json.bak error_library.json
```

### 3. 查看详细错误信息

```bash
# 使用 Python 调试模式
python3 -u code_validator.py validate -v
```

## 📞 技术支持

### 文件位置

- **主程序**: `code_validator.py`
- **配置文件**: `validator_config.json`
- **错误库**: `error_library.json`
- **日志文件**: `validation.log`

### 调试

查看日志文件获取详细信息：

```bash
tail -f validation.log
```

## 🎯 下一步

1. ✅ 尝试运行验证
2. 📚 查看错误库状态
3. 🔧 自定义配置
4. 🔗 集成到项目

---

**版本**: 1.0.0
**最后更新**: 2024-01-15
**维护者**: AI Assistant
