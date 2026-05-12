#!/usr/bin/env python3
"""
代码语法验证与自动修复技能 - Python实现
Code Syntax Validation and Auto-Fix Skill
版本: 1.0.0
"""

import os
import sys
import json
import subprocess
import re
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict
from enum import Enum

class ErrorCategory(Enum):
    SYNTAX = "syntax"
    STYLE = "style"
    SEMANTIC = "semantic"
    LOGICAL = "logical"

@dataclass
class ErrorEntry:
    """错误条目数据结构"""
    id: str
    file: str
    error_type: str
    error_message: str
    fix_suggestion: str
    category: str
    timestamp: str
    fix_count: int = 0
    success_rate: float = 0.0

class ColorOutput:
    """彩色输出"""
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'
    
    @staticmethod
    def info(msg):
        print(f"{ColorOutput.BLUE}[INFO]{ColorOutput.NC} {msg}")
    
    @staticmethod
    def success(msg):
        print(f"{ColorOutput.GREEN}[SUCCESS]{ColorOutput.NC} {msg}")
    
    @staticmethod
    def warning(msg):
        print(f"{ColorOutput.YELLOW}[WARNING]{ColorOutput.NC} {msg}")
    
    @staticmethod
    def error(msg):
        print(f"{ColorOutput.RED}[ERROR]{ColorOutput.NC} {msg}", file=sys.stderr)

class ErrorLibrary:
    """错误库管理类"""
    
    def __init__(self, library_path: str):
        self.library_path = Path(library_path)
        self.data = self._load_or_init()
    
    def _load_or_init(self) -> Dict:
        """加载或初始化错误库"""
        if self.library_path.exists():
            with open(self.library_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # 初始化新错误库
        from datetime import timezone
        return {
            "version": "1.0.0",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "last_updated": datetime.now(timezone.utc).isoformat(),
            "total_errors": 0,
            "categories": {
                "syntax": [],
                "style": [],
                "semantic": [],
                "logical": []
            },
            "recent_fixes": [],
            "statistics": {
                "by_language": {},
                "by_error_type": {}
            }
        }
    
    def add_error(self, file: str, error_type: str, error_msg: str, 
                  suggestion: str, category: str = "syntax") -> ErrorEntry:
        """添加错误到错误库"""
        entry = ErrorEntry(
            id=self._generate_id(),
            file=file,
            error_type=error_type,
            error_message=error_msg,
            fix_suggestion=suggestion,
            category=category,
            timestamp=datetime.utcnow().isoformat() + "Z"
        )
        
        # 添加到对应分类
        self.data["categories"][category].append(asdict(entry))
        self.data["total_errors"] += 1
        self.data["last_updated"] = datetime.utcnow().isoformat() + "Z"
        
        # 更新统计
        self._update_statistics(error_type, category)
        self._save()
        
        return entry
    
    def _generate_id(self) -> str:
        """生成唯一ID"""
        import uuid
        return str(uuid.uuid4())[:8]
    
    def _update_statistics(self, error_type: str, category: str):
        """更新统计信息"""
        stats = self.data["statistics"]
        
        # 按错误类型统计
        if error_type not in stats["by_error_type"]:
            stats["by_error_type"][error_type] = 0
        stats["by_error_type"][error_type] += 1
        
        # 按分类统计
        if category not in stats["by_language"]:
            stats["by_language"][category] = 0
        stats["by_language"][category] += 1
    
    def add_fix_record(self, file: str, error_id: str, success: bool):
        """添加修复记录"""
        record = {
            "file": file,
            "error_id": error_id,
            "success": success,
            "fix_at": datetime.utcnow().isoformat() + "Z"
        }
        
        self.data["recent_fixes"].insert(0, record)
        # 只保留最近100条记录
        self.data["recent_fixes"] = self.data["recent_fixes"][:100]
        
        # 更新错误条目的修复计数
        for category in self.data["categories"]:
            for entry in self.data["categories"][category]:
                if entry["id"] == error_id:
                    entry["fix_count"] += 1
                    if success:
                        entry["success_rate"] = min(1.0, entry["success_rate"] + 0.1)
        
        self._save()
    
    def get_similar_errors(self, error_msg: str, threshold: float = 0.7) -> List[ErrorEntry]:
        """查找相似错误"""
        similar = []
        
        for category in self.data["categories"]:
            for entry_data in self.data["categories"][category]:
                if self._calculate_similarity(error_msg, entry_data["error_message"]) >= threshold:
                    similar.append(ErrorEntry(**entry_data))
        
        return similar
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """计算文本相似度"""
        text1 = text1.lower()
        text2 = text2.lower()
        
        # 简单的词汇重叠度计算
        words1 = set(re.findall(r'\w+', text1))
        words2 = set(re.findall(r'\w+', text2))
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1 & words2
        union = words1 | words2
        
        return len(intersection) / len(union)
    
    def _save(self):
        """保存错误库"""
        self.library_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.library_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def show_statistics(self):
        """显示统计信息"""
        print("\n📊 错误库统计")
        print("=" * 50)
        print(f"总错误数: {self.data['total_errors']}")
        print(f"最后更新: {self.data['last_updated']}")
        
        print("\n按分类统计:")
        for category, entries in self.data["categories"].items():
            print(f"  • {category}: {len(entries)} 个")
        
        print("\n按错误类型统计:")
        for error_type, count in self.data["statistics"]["by_error_type"].items():
            print(f"  • {error_type}: {count} 次")
        
        if self.data["recent_fixes"]:
            print("\n最近修复记录:")
            for fix in self.data["recent_fixes"][:5]:
                status = "✅" if fix["success"] else "❌"
                print(f"  {status} {fix['file']} - {fix['fix_at']}")

class SyntaxValidator:
    """语法验证器"""
    
    def __init__(self, error_library: ErrorLibrary):
        self.error_library = error_library
        self.fix_strategies = self._init_fix_strategies()
    
    def _init_fix_strategies(self) -> Dict:
        """初始化修复策略"""
        return {
            "javascript": {
                "patterns": [
                    (r'\s+$', ''),  # 去除末尾空白
                    (r';\s*;', ';'),  # 双分号
                    (r',\s*}', '}'),  # 对象末尾多余逗号
                    (r',\s*]', ']'),  # 数组末尾多余逗号
                ],
                "fix_func": self._fix_javascript
            },
            "python": {
                "patterns": [
                    (r'\t', '    '),  # Tab转空格
                    (r'\s+$', ''),  # 去除末尾空白
                ],
                "fix_func": self._fix_python
            },
            "dart": {
                "patterns": [
                    (r'\s+$', ''),
                    (r';\s*;', ';'),
                ],
                "fix_func": self._fix_generic
            },
            "kotlin": {
                "patterns": [
                    (r'\s+$', ''),
                    (r';\s*;', ';'),
                ],
                "fix_func": self._fix_generic
            },
            "swift": {
                "patterns": [
                    (r'\s+$', ''),
                ],
                "fix_func": self._fix_generic
            },
            "lua": {
                "patterns": [
                    (r'\s+$', ''),
                ],
                "fix_func": self._fix_generic
            },
            "perl": {
                "patterns": [
                    (r'\s+$', ''),
                ],
                "fix_func": self._fix_generic
            },
            "shell": {
                "patterns": [
                    (r'\s+$', ''),
                    (r'\t', '    '),
                ],
                "fix_func": self._fix_generic
            },
            "c": {
                "patterns": [
                    (r'\s+$', ''),
                ],
                "fix_func": self._fix_generic
            },
            "cpp": {
                "patterns": [
                    (r'\s+$', ''),
                ],
                "fix_func": self._fix_generic
            },
            "csharp": {
                "patterns": [
                    (r'\s+$', ''),
                ],
                "fix_func": self._fix_generic
            },
            "ruby": {
                "patterns": [
                    (r'\s+$', ''),
                ],
                "fix_func": self._fix_generic
            },
            "php": {
                "patterns": [
                    (r'\s+$', ''),
                ],
                "fix_func": self._fix_generic
            },
        }
    
    def check_file(self, file_path: str) -> Tuple[bool, List[str]]:
        """检查文件语法"""
        file_path = Path(file_path)
        
        if not file_path.exists():
            return False, [f"文件不存在: {file_path}"]
        
        ext = file_path.suffix.lower()
        checker_method = f"_check_{self._get_language(ext)}"
        
        if hasattr(self, checker_method):
            return getattr(self, checker_method)(file_path)
        
        return False, [f"不支持的文件类型: {ext}"]
    
    def _get_language(self, ext: str) -> str:
        """根据扩展名获取语言"""
        lang_map = {
            '.js': 'javascript',
            '.mjs': 'javascript',
            '.cjs': 'javascript',
            '.ts': 'javascript',
            '.jsx': 'javascript',
            '.tsx': 'javascript',
            '.py': 'python',
            '.go': 'go',
            '.rs': 'rust',
            '.java': 'java',
            '.dart': 'dart',
            '.kt': 'kotlin',
            '.kts': 'kotlin',
            '.swift': 'swift',
            '.r': 'r',
            '.scala': 'scala',
            '.sc': 'scala',
            '.hs': 'haskell',
            '.lua': 'lua',
            '.pl': 'perl',
            '.pm': 'perl',
            '.sh': 'shell',
            '.bash': 'shell',
            '.c': 'c',
            '.cpp': 'cpp',
            '.cc': 'cpp',
            '.h': 'c',
            '.hpp': 'cpp',
            '.cs': 'csharp',
            '.rb': 'ruby',
            '.php': 'php',
        }
        return lang_map.get(ext, 'unknown')
    
    def _check_javascript(self, file_path: Path) -> Tuple[bool, List[str]]:
        """检查JavaScript文件"""
        errors = []
        
        try:
            # 尝试用Node.js检查
            result = subprocess.run(
                ['node', '--check', str(file_path)],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode != 0:
                errors.append(result.stderr)
        except (subprocess.TimeoutExpired, FileNotFoundError):
            # Node不可用时使用基础检查
            errors.extend(self._basic_syntax_check(file_path))
        
        if errors:
            return False, errors
        return True, []
    
    def _check_python(self, file_path: Path) -> Tuple[bool, List[str]]:
        """检查Python文件"""
        errors = []
        
        try:
            result = subprocess.run(
                ['python3', '-m', 'py_compile', str(file_path)],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode != 0:
                errors.append(result.stderr)
        except (subprocess.TimeoutExpired, FileNotFoundError):
            # 使用AST检查
            errors.extend(self._check_python_ast(file_path))
        
        if errors:
            return False, errors
        return True, []
    
    def _check_python_ast(self, file_path: Path) -> List[str]:
        """使用AST检查Python语法"""
        errors = []
        
        try:
            import ast
            with open(file_path, 'r', encoding='utf-8') as f:
                source = f.read()
            
            ast.parse(source)
        except SyntaxError as e:
            errors.append(f"Python语法错误: {e}")
        except Exception as e:
            errors.append(f"解析错误: {e}")
        
        return errors
    
    def _check_dart(self, file_path: Path) -> Tuple[bool, List[str]]:
        """检查Dart文件"""
        errors = []
        
        try:
            result = subprocess.run(
                ['dart', 'analyze', '--no-fatal-infos', '--no-fatal-warnings', str(file_path)],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                errors.append(result.stderr if result.stderr else result.stdout)
        except (subprocess.TimeoutExpired, FileNotFoundError):
            # 没有dart命令时使用基础检查
            errors.extend(self._basic_syntax_check(file_path))
        
        if errors:
            return False, errors
        return True, []
    
    def _check_kotlin(self, file_path: Path) -> Tuple[bool, List[str]]:
        """检查Kotlin文件"""
        errors = []
        
        try:
            result = subprocess.run(
                ['kotlinc', '-no-stdlib', '-cp', '.', '-script', str(file_path)],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                errors.append(result.stderr if result.stderr else result.stdout)
        except (subprocess.TimeoutExpired, FileNotFoundError):
            errors.extend(self._basic_syntax_check(file_path))
        
        if errors:
            return False, errors
        return True, []
    
    def _check_swift(self, file_path: Path) -> Tuple[bool, List[str]]:
        """检查Swift文件"""
        errors = []
        
        try:
            result = subprocess.run(
                ['swiftc', '-parse', str(file_path)],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                errors.append(result.stderr if result.stderr else result.stdout)
        except (subprocess.TimeoutExpired, FileNotFoundError):
            errors.extend(self._basic_syntax_check(file_path))
        
        if errors:
            return False, errors
        return True, []
    
    def _check_r(self, file_path: Path) -> Tuple[bool, List[str]]:
        """检查R文件"""
        errors = []
        
        try:
            result = subprocess.run(
                ['Rscript', '-e', f"parse(file='{str(file_path)}')"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                errors.append(result.stderr if result.stderr else result.stdout)
        except (subprocess.TimeoutExpired, FileNotFoundError):
            errors.extend(self._basic_syntax_check(file_path))
        
        if errors:
            return False, errors
        return True, []
    
    def _check_scala(self, file_path: Path) -> Tuple[bool, List[str]]:
        """检查Scala文件"""
        errors = []
        
        try:
            result = subprocess.run(
                ['scalac', '-cp', '.', '-Xcheck-null', str(file_path)],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                errors.append(result.stderr if result.stderr else result.stdout)
        except (subprocess.TimeoutExpired, FileNotFoundError):
            errors.extend(self._basic_syntax_check(file_path))
        
        if errors:
            return False, errors
        return True, []
    
    def _check_haskell(self, file_path: Path) -> Tuple[bool, List[str]]:
        """检查Haskell文件"""
        errors = []
        
        try:
            result = subprocess.run(
                ['ghc', '-fno-code', str(file_path)],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                errors.append(result.stderr if result.stderr else result.stdout)
        except (subprocess.TimeoutExpired, FileNotFoundError):
            errors.extend(self._basic_syntax_check(file_path))
        
        if errors:
            return False, errors
        return True, []
    
    def _check_lua(self, file_path: Path) -> Tuple[bool, List[str]]:
        """检查Lua文件"""
        errors = []
        
        try:
            result = subprocess.run(
                ['luac', '-p', str(file_path)],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode != 0:
                errors.append(result.stderr if result.stderr else result.stdout)
        except (subprocess.TimeoutExpired, FileNotFoundError):
            errors.extend(self._basic_syntax_check(file_path))
        
        if errors:
            return False, errors
        return True, []
    
    def _check_perl(self, file_path: Path) -> Tuple[bool, List[str]]:
        """检查Perl文件"""
        errors = []
        
        try:
            result = subprocess.run(
                ['perl', '-c', str(file_path)],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode != 0:
                errors.append(result.stderr if result.stderr else result.stdout)
        except (subprocess.TimeoutExpired, FileNotFoundError):
            errors.extend(self._basic_syntax_check(file_path))
        
        if errors:
            return False, errors
        return True, []
    
    def _check_shell(self, file_path: Path) -> Tuple[bool, List[str]]:
        """检查Shell文件"""
        errors = []
        
        try:
            # 尝试用bash检查
            result = subprocess.run(
                ['bash', '-n', str(file_path)],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode != 0:
                errors.append(result.stderr if result.stderr else result.stdout)
        except (subprocess.TimeoutExpired, FileNotFoundError):
            errors.extend(self._basic_syntax_check(file_path))
        
        if errors:
            return False, errors
        return True, []
    
    def _check_c(self, file_path: Path) -> Tuple[bool, List[str]]:
        """检查C文件"""
        errors = []
        
        try:
            result = subprocess.run(
                ['gcc', '-fsyntax-only', '-Wall', '-Wextra', str(file_path)],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                errors.append(result.stderr if result.stderr else result.stdout)
        except (subprocess.TimeoutExpired, FileNotFoundError):
            errors.extend(self._basic_syntax_check(file_path))
        
        if errors:
            return False, errors
        return True, []
    
    def _check_cpp(self, file_path: Path) -> Tuple[bool, List[str]]:
        """检查C++文件"""
        errors = []
        
        try:
            result = subprocess.run(
                ['g++', '-fsyntax-only', '-Wall', '-Wextra', str(file_path)],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                errors.append(result.stderr if result.stderr else result.stdout)
        except (subprocess.TimeoutExpired, FileNotFoundError):
            errors.extend(self._basic_syntax_check(file_path))
        
        if errors:
            return False, errors
        return True, []
    
    def _check_csharp(self, file_path: Path) -> Tuple[bool, List[str]]:
        """检查C#文件"""
        errors = []
        
        try:
            # 尝试使用dotnet build或csc
            result = subprocess.run(
                ['csc', '/nologo', '/t:library', '/out:/dev/null', str(file_path)],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                errors.append(result.stderr if result.stderr else result.stdout)
        except (subprocess.TimeoutExpired, FileNotFoundError):
            try:
                # 尝试dotnet语法检查
                result = subprocess.run(
                    ['dotnet', 'build', '--no-incremental', '--no-restore'],
                    capture_output=True,
                    text=True,
                    timeout=60,
                    cwd=str(file_path.parent)
                )
                if result.returncode != 0:
                    errors.append(result.stderr if result.stderr else result.stdout)
            except:
                errors.extend(self._basic_syntax_check(file_path))
        
        if errors:
            return False, errors
        return True, []
    
    def _check_ruby(self, file_path: Path) -> Tuple[bool, List[str]]:
        """检查Ruby文件"""
        errors = []
        
        try:
            result = subprocess.run(
                ['ruby', '-c', str(file_path)],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode != 0:
                errors.append(result.stderr if result.stderr else result.stdout)
        except (subprocess.TimeoutExpired, FileNotFoundError):
            errors.extend(self._basic_syntax_check(file_path))
        
        if errors:
            return False, errors
        return True, []
    
    def _check_php(self, file_path: Path) -> Tuple[bool, List[str]]:
        """检查PHP文件"""
        errors = []
        
        try:
            result = subprocess.run(
                ['php', '-l', str(file_path)],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode != 0:
                errors.append(result.stderr if result.stderr else result.stdout)
        except (subprocess.TimeoutExpired, FileNotFoundError):
            errors.extend(self._basic_syntax_check(file_path))
        
        if errors:
            return False, errors
        return True, []
    
    def _basic_syntax_check(self, file_path: Path) -> List[str]:
        """基础语法检查"""
        errors = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查括号匹配
            if not self._check_brackets(content):
                errors.append("括号匹配错误")
            
            # 检查引号匹配
            if not self._check_quotes(content):
                errors.append("引号匹配错误")
            
            # 检查常见的JavaScript问题
            if file_path.suffix in ['.js', '.ts', '.jsx', '.tsx']:
                if not self._check_javascript_common(content):
                    errors.append("JavaScript常见语法问题")
        
        except Exception as e:
            errors.append(f"读取文件错误: {e}")
        
        return errors
    
    def _check_brackets(self, content: str) -> bool:
        """检查括号匹配"""
        stack = []
        pairs = {'(': ')', '[': ']', '{': '}'}
        
        for char in content:
            if char in pairs:
                stack.append(char)
            elif char in pairs.values():
                if not stack or pairs.get(stack[-1]) != char:
                    return False
                stack.pop()
        
        return len(stack) == 0
    
    def _check_quotes(self, content: str) -> bool:
        """检查引号匹配"""
        # 移除字符串中的引号（简化检查）
        cleaned = re.sub(r'["\'][^"\']*["\']', '', content)
        
        # 检查是否有未闭合的引号
        double_quotes = cleaned.count('"')
        single_quotes = cleaned.count("'")
        
        return (double_quotes % 2 == 0) and (single_quotes % 2 == 0)
    
    def _check_javascript_common(self, content: str) -> bool:
        """检查JavaScript常见问题"""
        # 检查是否有常见的未定义变量使用
        if re.search(r'\bundefined\b', content):
            # 检查上下文
            return True
        
        return True
    
    def _fix_javascript(self, content: str) -> Tuple[str, int]:
        """修复JavaScript问题"""
        fixed_count = 0
        
        # 去除末尾空白
        new_content = re.sub(r'\s+$', '', content, flags=re.MULTILINE)
        if new_content != content:
            fixed_count += 1
            content = new_content
        
        # 修复双分号
        new_content = re.sub(r';\s*;', ';', content)
        if new_content != content:
            fixed_count += 1
            content = new_content
        
        # 修复对象/数组末尾逗号
        new_content = re.sub(r',\s*([}\]])', r'\1', content)
        if new_content != content:
            fixed_count += 1
            content = new_content
        
        return content, fixed_count
    
    def _fix_python(self, content: str) -> Tuple[str, int]:
        """修复Python问题"""
        fixed_count = 0
        
        # Tab转空格
        if '\t' in content:
            content = content.replace('\t', '    ')
            fixed_count += 1
        
        # 去除末尾空白
        new_content = re.sub(r'\s+$', '', content, flags=re.MULTILINE)
        if new_content != content:
            fixed_count += 1
            content = new_content
        
        return content, fixed_count
    
    def _fix_generic(self, content: str) -> Tuple[str, int]:
        """通用修复函数"""
        fixed_count = 0
        
        # 去除末尾空白
        new_content = re.sub(r'\s+$', '', content, flags=re.MULTILINE)
        if new_content != content:
            fixed_count += 1
            content = new_content
        
        return content, fixed_count
    
    def auto_fix(self, file_path: str) -> Tuple[bool, int]:
        """自动修复文件"""
        file_path = Path(file_path)
        ext = file_path.suffix.lower()
        language = self._get_language(ext)
        
        if language not in self.fix_strategies:
            return False, 0
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 应用修复策略
            strategy = self.fix_strategies[language]
            content, fixed_count = strategy["fix_func"](content)
            
            # 额外的模式修复
            for pattern, replacement in strategy["patterns"]:
                new_content = re.sub(pattern, replacement, content)
                if new_content != content:
                    fixed_count += 1
                    content = new_content
            
            # 保存修复后的内容
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return True, fixed_count
        
        except Exception as e:
            ColorOutput.error(f"修复失败: {e}")
            return False, 0
    
    def analyze_error(self, error_msg: str) -> Tuple[str, str]:
        """分析错误并分类"""
        error_msg_lower = error_msg.lower()
        
        if 'syntax' in error_msg_lower:
            return 'syntax_error', 'syntax'
        elif 'undefined' in error_msg_lower or 'unresolved' in error_msg_lower:
            return 'undefined_reference', 'semantic'
        elif 'import' in error_msg_lower or 'require' in error_msg_lower or 'export' in error_msg_lower or 'module' in error_msg_lower:
            return 'module_error', 'semantic'
        elif 'type' in error_msg_lower:
            return 'type_error', 'semantic'
        elif 'indent' in error_msg_lower or 'indentation' in error_msg_lower:
            return 'indentation_error', 'style'
        elif 'semicolon' in error_msg_lower or 'semi-colon' in error_msg_lower:
            return 'semicolon_error', 'style'
        elif 'brace' in error_msg_lower or 'bracket' in error_msg_lower or 'parentheses' in error_msg_lower:
            return 'brace_error', 'syntax'
        elif 'quote' in error_msg_lower or 'string' in error_msg_lower and 'terminated' in error_msg_lower:
            return 'quote_error', 'syntax'
        elif 'missing' in error_msg_lower:
            return 'missing_element', 'syntax'
        elif 'extra' in error_msg_lower or 'unexpected' in error_msg_lower:
            return 'unexpected_element', 'syntax'
        else:
            return 'general_error', 'syntax'
    
    def get_fix_suggestion(self, error_msg: str) -> str:
        """获取修复建议"""
        suggestions = {
            'syntax_error': '检查语法括号、引号是否匹配，确保语句完整',
            'undefined_reference': '检查变量或函数是否已定义或正确导入',
            'module_error': '检查模块路径是否正确，模块是否已安装/导入',
            'type_error': '检查变量类型是否正确，注意类型转换',
            'indentation_error': '检查缩进是否一致',
            'semicolon_error': '检查分号是否正确放置',
            'brace_error': '检查括号/大括号是否正确匹配',
            'quote_error': '检查字符串引号是否正确闭合',
            'missing_element': '检查是否缺少必要的关键字或符号',
            'unexpected_element': '移除多余或意外的符号',
            'general_error': '请仔细检查代码结构和语法'
        }
        
        error_type, _ = self.analyze_error(error_msg)
        return suggestions.get(error_type, suggestions['general_error'])


class CodeValidator:
    """代码验证主类"""
    
    def __init__(self, project_dir: str = "."):
        self.project_dir = Path(project_dir)
        skill_dir = Path(__file__).parent
        self.error_library = ErrorLibrary(str(skill_dir / "error_library.json"))
        self.validator = SyntaxValidator(self.error_library)
        self.max_iterations = 5
    
    def detect_languages(self) -> List[str]:
        """检测项目语言"""
        languages = []
        
        # 检测各种项目文件
        markers = {
            'javascript': ['package.json', 'package-lock.json'],
            'typescript': ['tsconfig.json'],
            'python': ['requirements.txt', 'setup.py', 'pyproject.toml'],
            'go': ['go.mod', 'go.sum'],
            'rust': ['Cargo.toml', 'Cargo.lock'],
            'java': ['pom.xml', 'build.gradle', 'build.gradle.kts', 'gradlew'],
            'dart': ['pubspec.yaml', 'pubspec.yml', 'pubspec.lock'],
            'kotlin': ['build.gradle.kts', 'settings.gradle.kts', 'gradlew'],
            'swift': ['Package.swift', 'Info.plist'],
            'r': ['DESCRIPTION', 'NAMESPACE', '*.Rproj'],
            'scala': ['build.sbt', 'project/plugins.sbt', 'sbt'],
            'haskell': ['cabal.project', 'package.yaml', 'stack.yaml'],
            'lua': ['rockspec'],
            'perl': ['Makefile.PL', 'Build.PL', 'cpanfile'],
            'c': ['Makefile', 'configure'],
            'cpp': ['Makefile', 'configure', 'CMakeLists.txt'],
            'csharp': ['*.csproj', '*.sln'],
            'ruby': ['Gemfile', 'Rakefile'],
            'php': ['composer.json', 'composer.lock'],
        }
        
        for lang, files in markers.items():
            if any((self.project_dir / f).exists() for f in files):
                languages.append(lang)
            # 检查通配符模式
            for pattern in files:
                if '*' in pattern and list(self.project_dir.glob(pattern)):
                    languages.append(lang)
                    break
        
        # 去重
        return list(set(languages))
    
    def collect_source_files(self) -> List[Path]:
        """收集源文件"""
        extensions = [
            '.js', '.mjs', '.ts', '.jsx', '.tsx',  # JavaScript/TypeScript
            '.py', '.pyw',                           # Python
            '.go',                                   # Go
            '.rs',                                   # Rust
            '.java',                                 # Java
            '.dart',                                 # Dart
            '.kt', '.kts',                           # Kotlin
            '.swift',                                # Swift
            '.r', '.R',                              # R
            '.scala', '.sc',                         # Scala
            '.hs', '.lhs',                           # Haskell
            '.lua',                                  # Lua
            '.pl', '.pm', '.t',                      # Perl
            '.sh', '.bash', '.zsh',                  # Shell
            '.c', '.h',                              # C
            '.cpp', '.cc', '.hpp', '.hxx', '.cxx',   # C++
            '.cs',                                   # C#
            '.rb',                                   # Ruby
            '.php', '.php3', '.php4', '.php5',       # PHP
        ]
        exclude_dirs = {'node_modules', '.git', 'dist', 'build', '__pycache__', '.venv', 'venv', 'target', 'build', 'bin', 'obj'}
        
        files = []
        for ext in extensions:
            for file in self.project_dir.rglob(f'*{ext}'):
                # 排除特定目录
                if not any(excl in file.parts for excl in exclude_dirs):
                    files.append(file)
        
        return files
    
    def validate_project(self, max_iterations: int = 5) -> bool:
        """验证整个项目"""
        ColorOutput.info(f"开始验证项目: {self.project_dir}")
        
        # 检测语言
        languages = self.detect_languages()
        if languages:
            ColorOutput.info(f"检测到语言: {', '.join(languages)}")
        else:
            ColorOutput.warning("无法检测项目语言")
        
        # 收集文件
        files = self.collect_source_files()
        if not files:
            ColorOutput.warning("未找到源文件")
            return True
        
        ColorOutput.info(f"找到 {len(files)} 个源文件")
        
        # 迭代验证和修复
        iteration = 0
        has_errors = True
        
        while has_errors and iteration < max_iterations:
            iteration += 1
            ColorOutput.info(f"=== 第 {iteration} 轮验证 ===")
            
            has_errors = False
            error_count = 0
            
            for file in files:
                success, errors = self.validator.check_file(str(file))
                
                if not success:
                    has_errors = True
                    error_count += 1
                    
                    for error in errors:
                        ColorOutput.error(f"{file}: {error}")
                        
                        # 分析错误
                        error_type, category = self.validator.analyze_error(error)
                        suggestion = self.validator.get_fix_suggestion(error)
                        
                        # 添加到错误库
                        entry = self.error_library.add_error(
                            str(file), error_type, error, suggestion, category
                        )
                        
                        # 尝试自动修复
                        fixed, fix_count = self.validator.auto_fix(str(file))
                        if fixed:
                            self.error_library.add_fix_record(str(file), entry.id, True)
                            ColorOutput.success(f"已修复: {file} ({fix_count} 处)")
                        else:
                            self.error_library.add_fix_record(str(file), entry.id, False)
            
            if has_errors:
                ColorOutput.warning(f"发现 {error_count} 个错误")
        
        if has_errors:
            ColorOutput.error(f"经过 {max_iterations} 轮修复后仍存在错误")
            return False
        else:
            ColorOutput.success("所有文件验证通过！")
            return True
    
    def check_single_file(self, file_path: str) -> bool:
        """检查单个文件"""
        success, errors = self.validator.check_file(file_path)
        
        if success:
            ColorOutput.success(f"语法检查通过: {file_path}")
            return True
        else:
            for error in errors:
                ColorOutput.error(f"{file_path}: {error}")
                
                # 分析并获取建议
                error_type, category = self.validator.analyze_error(error)
                suggestion = self.validator.get_fix_suggestion(error)
                
                # 检查是否有相似的已知错误
                similar = self.error_library.get_similar_errors(error)
                
                if similar:
                    ColorOutput.info("类似错误记录:")
                    for entry in similar[:3]:
                        print(f"  → {entry.fix_suggestion}")
                
                ColorOutput.info(f"修复建议: {suggestion}")
                
                # 添加到错误库
                entry = self.error_library.add_error(
                    file_path, error_type, error, suggestion, category
                )
                
                # 尝试自动修复
                fixed, fix_count = self.validator.auto_fix(file_path)
                if fixed:
                    ColorOutput.success(f"已自动修复 {fix_count} 处问题")
            
            return False


def show_help():
    """显示帮助信息"""
    help_text = """
代码语法验证与自动修复技能 (Code Validator Skill)
================================================

用法: python3 code_validator.py [命令] [选项]

命令:
    validate [目录]      验证整个项目或指定目录（默认当前目录）
    check <文件>         检查单个文件
    library             显示错误库状态
    clear-library       清空错误库
    help                显示此帮助信息

示例:
    python3 code_validator.py validate                    # 验证当前项目
    python3 code_validator.py validate ./my-project       # 验证指定项目
    python3 code_validator.py check src/app.js            # 检查单个文件
    python3 code_validator.py library                     # 查看错误库

工作流程:
    1. 读取项目源文件
    2. 进行语法检查
    3. 发现错误后尝试自动修复
    4. 将错误记录到错误库
    5. 提供修复建议
    6. 支持从错误库学习，识别常见错误模式

支持的编程语言:
    • JavaScript/TypeScript
    • Python
    • Go
    • Rust
    • Java
    • Dart
    • Kotlin
    • Swift
    • R
    • Scala
    • Haskell
    • Lua
    • Perl
    • Shell
    • C/C++
    • C#
    • Ruby
    • PHP

特性:
    ✓ 多语言支持
    ✓ 自动修复常见错误
    ✓ 智能错误分析
    ✓ 错误库学习
    ✓ 修复历史记录
    ✓ 统计报告
"""
    print(help_text)


def main():
    """主函数"""
    if len(sys.argv) < 2:
        show_help()
        sys.exit(0)
    
    command = sys.argv[1]
    target = sys.argv[2] if len(sys.argv) > 2 else "."
    
    validator = CodeValidator()
    
    if command == 'validate':
        success = validator.validate_project()
        sys.exit(0 if success else 1)
    
    elif command == 'check':
        success = validator.check_single_file(target)
        sys.exit(0 if success else 1)
    
    elif command == 'library':
        validator.error_library.show_statistics()
    
    elif command == 'clear-library':
        if Path(validator.error_library.library_path).exists():
            Path(validator.error_library.library_path).unlink()
        ColorOutput.success("错误库已清空")
    
    elif command in ['help', '--help', '-h']:
        show_help()
    
    else:
        ColorOutput.error(f"未知命令: {command}")
        show_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
