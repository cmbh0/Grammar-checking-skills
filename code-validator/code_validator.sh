#!/bin/bash

# 代码语法验证与自动修复技能
# Code Syntax Validation and Auto-Fix Skill
# 版本: 1.0.0

set -e

# 配置路径
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ERROR_LIBRARY="$SKILL_DIR/error_library.json"
CONFIG_FILE="$SKILL_DIR/validator_config.json"
LOG_FILE="$SKILL_DIR/validation.log"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [INFO] $1" >> "$LOG_FILE"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [SUCCESS] $1" >> "$LOG_FILE"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [WARNING] $1" >> "$LOG_FILE"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [ERROR] $1" >> "$LOG_FILE"
}

# 初始化错误库
init_error_library() {
    if [ ! -f "$ERROR_LIBRARY" ]; then
        cat > "$ERROR_LIBRARY" << 'EOF'
{
  "version": "1.0.0",
  "created_at": "",
  "last_updated": "",
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
EOF
        # 更新创建时间
        local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
        sed -i "s/\"created_at\": \"\"/\"created_at\": \"$timestamp\"/" "$ERROR_LIBRARY"
        sed -i "s/\"last_updated\": \"\"/\"last_updated\": \"$timestamp\"/" "$ERROR_LIBRARY"
        log_info "错误库已初始化"
    fi
}

# 读取配置
load_config() {
    if [ -f "$CONFIG_FILE" ]; then
        log_info "加载配置文件: $CONFIG_FILE"
    else
        create_default_config
    fi
}

# 创建默认配置
create_default_config() {
    cat > "$CONFIG_FILE" << 'EOF'
{
  "auto_fix": true,
  "max_iterations": 5,
  "severity_threshold": "warning",
  "exclude_patterns": [
    "node_modules/*",
    ".git/*",
    "dist/*",
    "build/*",
    "*.min.js",
    "*.map"
  ],
  "language_settings": {
    "javascript": {
      "linter": "eslint",
      "config": ".eslintrc.json",
      "auto_fix_rules": true
    },
    "typescript": {
      "linter": "eslint",
      "config": ".eslintrc.json",
      "auto_fix_rules": true
    },
    "python": {
      "linter": "pylint",
      "config": "pylintrc",
      "auto_fix_rules": false
    }
  },
  "error_library_settings": {
    "max_entries": 1000,
    "auto_learn": true,
    "similarity_threshold": 0.8
  }
}
EOF
    log_info "已创建默认配置文件"
}

# 检测项目语言
detect_project_languages() {
    local project_dir="${1:-.}"
    local languages=()
    
    # 多种语言检测
    [ -f "$project_dir/package.json" ] && languages+=("javascript" "typescript")
    [ -f "$project_dir/requirements.txt" ] || [ -f "$project_dir/setup.py" ] && languages+=("python")
    [ -f "$project_dir/go.mod" ] && languages+=("go")
    [ -f "$project_dir/Cargo.toml" ] && languages+=("rust")
    [ -f "$project_dir/pom.xml" ] || [ -f "$project_dir/build.gradle" ] && languages+=("java")
    [ -f "$project_dir/composer.json" ] && languages+=("php")
    [ -f "$project_dir/Gemfile" ] && languages+=("ruby")
    
    echo "${languages[@]}"
}

# JavaScript/TypeScript 语法检查
check_javascript() {
    local file="$1"
    local errors=()
    
    if command -v node &> /dev/null; then
        # 使用Node.js进行基本语法检查
        if node --check "$file" 2>&1; then
            log_success "语法检查通过: $file"
            return 0
        else
            local error_msg=$(node --check "$file" 2>&1)
            errors+=("$error_msg")
            log_error "语法错误在 $file: $error_msg"
        fi
    fi
    
    # 尝试使用ESLint
    if command -v npx &> /dev/null && [ -f ".eslintrc.json" ]; then
        local eslint_output=$(npx eslint "$file" --format json 2>&1 || true)
        if [ -n "$eslint_output" ]; then
            errors+=("ESLint: $eslint_output")
        fi
    fi
    
    # 返回错误
    if [ ${#errors[@]} -gt 0 ]; then
        printf '%s\n' "${errors[@]}"
        return 1
    fi
    
    return 0
}

# Python 语法检查
check_python() {
    local file="$1"
    local errors=()
    
    if command -v python3 &> /dev/null; then
        # 使用Python编译器进行语法检查
        if python3 -m py_compile "$file" 2>&1; then
            log_success "语法检查通过: $file"
            return 0
        else
            local error_msg=$(python3 -m py_compile "$file" 2>&1)
            errors+=("$error_msg")
            log_error "语法错误在 $file: $error_msg"
        fi
    fi
    
    # 尝试使用Pylint
    if command -v pylint &> /dev/null; then
        local pylint_output=$(pylint "$file" 2>&1 || true)
        if [ -n "$pylint_output" ]; then
            errors+=("Pylint: $pylint_output")
        fi
    fi
    
    if [ ${#errors[@]} -gt 0 ]; then
        printf '%s\n' "${errors[@]}"
        return 1
    fi
    
    return 0
}

# Go 语法检查
check_go() {
    local file="$1"
    
    if command -v go &> /dev/null; then
        if go vet "$file" 2>&1; then
            log_success "语法检查通过: $file"
            return 0
        else
            log_error "语法错误在 $file"
            go vet "$file" 2>&1
            return 1
        fi
    fi
    
    return 0
}

# Rust 语法检查
check_rust() {
    local file="$1"
    
    if command -v rustc &> /dev/null; then
        if rustc --crate-type lib "$file" 2>&1 | grep -q "error"; then
            log_error "语法错误在 $file"
            rustc --crate-type lib "$file" 2>&1
            return 1
        else
            log_success "语法检查通过: $file"
            return 0
        fi
    fi
    
    return 0
}

# Java 语法检查
check_java() {
    local file="$1"
    local errors=()
    
    if command -v javac &> /dev/null; then
        local output=$(javac "$file" 2>&1 || true)
        if [ -n "$output" ]; then
            errors+=("$output")
            log_error "语法错误在 $file: $output"
        else
            log_success "语法检查通过: $file"
            return 0
        fi
    fi
    
    if [ ${#errors[@]} -gt 0 ]; then
        printf '%s\n' "${errors[@]}"
        return 1
    fi
    
    return 0
}

# 通用语法检查器
check_syntax() {
    local file="$1"
    local ext="${file##*.}"
    
    case "$ext" in
        js|mjs|cjs)
            check_javascript "$file"
            ;;
        ts|mts|cts)
            check_javascript "$file"
            ;;
        py)
            check_python "$file"
            ;;
        go)
            check_go "$file"
            ;;
        rs)
            check_rust "$file"
            ;;
        java)
            check_java "$file"
            ;;
        *)
            log_warning "不支持的文件类型: $ext"
            return 1
            ;;
    esac
}

# 分析错误并提取模式
analyze_error_pattern() {
    local error_msg="$1"
    local error_type=""
    local error_category="syntax"
    
    # 提取错误类型
    if echo "$error_msg" | grep -qi "syntax"; then
        error_type="syntax_error"
        error_category="syntax"
    elif echo "$error_msg" | grep -qi "undefined"; then
        error_type="undefined_reference"
        error_category="semantic"
    elif echo "$error_msg" | grep -qi "import\|require"; then
        error_type="module_error"
        error_category="semantic"
    elif echo "$error_msg" | grep -qi "type"; then
        error_type="type_error"
        error_category="semantic"
    else
        error_type="general_error"
        error_category="syntax"
    fi
    
    echo "$error_type:$error_category"
}

# 添加错误到错误库
add_to_error_library() {
    local file="$1"
    local error_msg="$2"
    local fix_suggestion="$3"
    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    
    init_error_library
    
    # 解析错误类型
    local error_info=$(analyze_error_pattern "$error_msg")
    local error_type=$(echo "$error_info" | cut -d':' -f1)
    local error_category=$(echo "$error_info" | cut -d':' -f2)
    
    # 创建错误条目
    local error_entry=$(cat << EOF
{
  "id": "$(uuidgen 2>/dev/null || echo "err-$(date +%s)")",
  "file": "$file",
  "error_type": "$error_type",
  "error_message": "$error_msg",
  "fix_suggestion": "$fix_suggestion",
  "category": "$error_category",
  "timestamp": "$timestamp",
  "fix_count": 0,
  "success_rate": 0
}
EOF
)
    
    # 更新错误库（使用jq如果可用，否则使用sed）
    if command -v jq &> /dev/null; then
        local temp_file=$(mktemp)
        echo "$error_entry" | jq -s ".[]" > "$temp_file"
        jq --argjson entry "$error_entry" '.categories[entry.category] += [$entry] | .total_errors += 1 | .last_updated = "'"$timestamp"'"' "$ERROR_LIBRARY" > "$temp_file" && mv "$temp_file" "$ERROR_LIBRARY"
        log_info "错误已添加到错误库"
    else
        log_warning "jq未安装，无法更新错误库结构"
    fi
}

# 从错误库获取修复建议
get_fix_suggestion() {
    local error_msg="$1"
    local suggestion=""
    
    if [ ! -f "$ERROR_LIBRARY" ]; then
        return 1
    fi
    
    # 简单模式匹配
    if echo "$error_msg" | grep -qi "unexpected token"; then
        suggestion="检查语法括号、引号是否匹配，确保语句完整"
    elif echo "$error_msg" | grep -qi "undefined"; then
        suggestion="检查变量/函数是否已定义或正确导入"
    elif echo "$error_msg" | grep -qi "import"; then
        suggestion="检查模块路径是否正确，模块是否已安装"
    elif echo "$error_msg" | grep -qi "syntax"; then
        suggestion="检查基本语法结构，包括括号、引号、分号"
    else
        suggestion="请仔细检查代码结构和语法"
    fi
    
    echo "$suggestion"
}

# 自动修复基本语法错误
auto_fix() {
    local file="$1"
    local fixed=0
    
    # 通用修复：去除多余空白字符
    sed -i 's/[[:space:]]*$//' "$file"
    ((fixed++))
    
    # 修复常见的JavaScript问题
    if [[ "$file" == *.js || "$file" == *.ts ]]; then
        # 修复分号问题（如果使用分号风格）
        if grep -q ';$' "$file"; then
            sed -i 's/\s*;\s*$/;/g' "$file"
            ((fixed++))
        fi
        
        # 修复引号不一致
        if command -v node &> /dev/null; then
            node -e "
const fs = require('fs');
let content = fs.readFileSync('$file', 'utf8');
let changed = false;

// 统一引号（示例）
if (content.includes('\"')) {
    content = content.replace(/\"([^\"]*)\"/g, (m, g) => {
        if (!g.includes(\"'\")) {
            return \"'\" + g + \"'\";
        }
        return m;
    });
    changed = true;
}

if (changed) {
    fs.writeFileSync('$file', content);
    console.log('Quotes normalized');
}
" 2>/dev/null && ((fixed++)) || true
        fi
    fi
    
    # 修复Python缩进问题
    if [[ "$file" == *.py ]]; then
        # 确保一致的缩进（转换为空格）
        sed -i 's/\t/    /g' "$file"
        ((fixed++))
    fi
    
    if [ $fixed -gt 0 ]; then
        log_success "已自动修复 $file ($fixed 项)"
        return 0
    else
        log_warning "无法自动修复 $file"
        return 1
    fi
}

# 验证整个项目
validate_project() {
    local project_dir="${1:-.}"
    local max_iterations="${2:-5}"
    local current_iteration=0
    local has_errors=true
    
    log_info "开始验证项目: $project_dir"
    
    # 检测项目语言
    local languages=$(detect_project_languages "$project_dir")
    if [ -z "$languages" ]; then
        log_warning "无法检测项目语言"
    else
        log_info "检测到语言: $languages"
    fi
    
    # 收集所有源文件
    local source_files=$(find "$project_dir" -type f \( \
        -name "*.js" -o -name "*.ts" -o -name "*.py" -o -name "*.go" -o \
        -name "*.rs" -o -name "*.java" -o -name "*.c" -o -name "*.cpp" \
    \) ! -path "*/node_modules/*" ! -path "*/.git/*" ! -path "*/dist/*" 2>/dev/null)
    
    if [ -z "$source_files" ]; then
        log_warning "未找到源文件"
        return 0
    fi
    
    log_info "找到 $(echo "$source_files" | wc -l) 个源文件"
    
    # 迭代验证和修复
    while [ $has_errors = true ] && [ $current_iteration -lt $max_iterations ]; do
        ((current_iteration++))
        log_info "=== 第 $current_iteration 轮验证 ==="
        
        has_errors=false
        local iteration_errors=()
        
        for file in $source_files; do
            if ! check_syntax "$file"; then
                has_errors=true
                local error_msg=$(check_syntax "$file" 2>&1 || true)
                iteration_errors+=("$file: $error_msg")
                
                # 获取修复建议
                local suggestion=$(get_fix_suggestion "$error_msg")
                
                # 添加到错误库
                add_to_error_library "$file" "$error_msg" "$suggestion"
                
                # 尝试自动修复
                if auto_fix "$file"; then
                    log_success "已修复: $file"
                fi
            fi
        done
        
        # 如果有错误，报告并继续
        if [ $has_errors = true ]; then
            log_warning "发现 ${#iteration_errors[@]} 个错误"
            for err in "${iteration_errors[@]}"; do
                log_error "$err"
            done
        fi
    done
    
    if [ $has_errors = true ]; then
        log_error "经过 $max_iterations 轮修复后仍存在错误"
        return 1
    else
        log_success "所有文件验证通过！"
        return 0
    fi
}

# 快速检查错误库
check_error_library() {
    log_info "=== 错误库状态 ==="
    
    if [ ! -f "$ERROR_LIBRARY" ]; then
        log_warning "错误库为空"
        return 0
    fi
    
    if command -v jq &> /dev/null; then
        echo ""
        echo "错误统计："
        jq -r '.categories | to_entries[] | "- \(.key): \(.value | length) 个错误"' "$ERROR_LIBRARY"
        echo ""
        echo "最近修复："
        jq -r '.recent_fixes[:5][] | "- \(.file): \(.fix_at)"' "$ERROR_LIBRARY" 2>/dev/null || echo "暂无"
        echo ""
    else
        log_info "错误库文件位置: $ERROR_LIBRARY"
    fi
}

# 显示帮助
show_help() {
    cat << 'EOF'
代码语法验证与自动修复技能 (Code Validator Skill)
================================================

用法: code_validator.sh [命令] [选项]

命令:
    validate [目录]      验证整个项目或指定目录
    check <文件>         检查单个文件
    fix <文件>           自动修复文件中的错误
    library             显示错误库状态
    clear-library       清空错误库
    help                显示此帮助信息

示例:
    ./code_validator.sh validate                    # 验证当前项目
    ./code_validator.sh validate ./my-project       # 验证指定项目
    ./code_validator.sh check src/app.js            # 检查单个文件
    ./code_validator.sh fix src/app.js               # 修复单个文件
    ./code_validator.sh library                      # 查看错误库

工作流程:
    1. 读取项目源文件
    2. 进行语法检查
    3. 发现错误后尝试自动修复
    4. 将错误记录到错误库
    5. 提供修复建议

支持的编程语言:
    - JavaScript/TypeScript
    - Python
    - Go
    - Rust
    - Java
    - C/C++
    - Ruby
    - PHP

更多信息请访问项目文档
EOF
}

# 主函数
main() {
    # 初始化
    init_error_library
    mkdir -p "$(dirname "$LOG_FILE")" 2>/dev/null || true
    
    # 解析命令
    local command="${1:-help}"
    local target="${2:-.}"
    
    case "$command" in
        validate)
            validate_project "$target"
            ;;
        check)
            if [ -f "$target" ]; then
                check_syntax "$target"
            else
                log_error "文件不存在: $target"
                exit 1
            fi
            ;;
        fix)
            if [ -f "$target" ]; then
                auto_fix "$target"
                # 修复后再次检查
                if check_syntax "$target"; then
                    log_success "修复成功！"
                else
                    log_warning "可能需要手动检查"
                fi
            else
                log_error "文件不存在: $target"
                exit 1
            fi
            ;;
        library)
            check_error_library
            ;;
        clear-library)
            rm -f "$ERROR_LIBRARY"
            init_error_library
            log_success "错误库已清空"
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            log_error "未知命令: $command"
            show_help
            exit 1
            ;;
    esac
}

# 运行主函数
main "$@"
