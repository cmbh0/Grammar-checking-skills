# Grammar-checking-skills

## 项目介绍

`Grammar-checking-skills` 当前收录的是 `code-validator` 技能：一个面向代码项目的语法验证与自动修复工具。它可以扫描项目中的源代码文件，识别常见语法错误、格式问题和可安全自动修复的问题，并将错误记录到错误库中，用于后续复盘与改进。

## 核心能力

- **多语言代码检查**：支持 JavaScript、TypeScript、Python、Java、Go、Rust、C、C++、C#、Ruby、PHP、Dart、Kotlin、Swift、R、Scala、Haskell、Lua、Perl、Shell 等语言。
- **语法验证**：对项目或单个文件执行语法检查，尽早暴露代码错误。
- **自动修复**：针对安全、确定的常见问题执行自动修复，例如末尾空白、缩进、重复分号、部分多余逗号等。
- **错误库机制**：自动记录错误类型、错误信息、修复建议和修复历史，帮助形成可复用的错误经验库。
- **项目级工作流**：支持对整个项目进行多轮验证与修复，直到通过或达到最大迭代次数。

## 仓库结构

```text
.
├── README.md
└── code-validator/
    ├── skill.json
    ├── README.md
    ├── QUICKSTART.md
    ├── code_validator.py
    └── code_validator.sh
```

## 快速开始

进入技能目录：

```bash
cd code-validator
```

验证整个项目：

```bash
python3 code_validator.py validate /path/to/project
```

检查单个文件：

```bash
python3 code_validator.py check path/to/file.py
```

查看错误库统计：

```bash
python3 code_validator.py library
```

更多说明请查看：

- [`code-validator/README.md`](code-validator/README.md)
- [`code-validator/QUICKSTART.md`](code-validator/QUICKSTART.md)

## 适用场景

- 在提交代码前进行本地语法检查。
- 对 AI 生成代码进行二次验证。
- 为项目建立基础质量门禁。
- 记录常见错误并形成可复用修复经验。

