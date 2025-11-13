#!/usr/bin/env python3
"""
Extract and validate C# code examples from markdown files
"""
import re
import os
import glob

def extract_csharp_blocks(filepath):
    """Extract all C# code blocks from a markdown file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all csharp code blocks
    pattern = r'```csharp\n(.*?)```'
    blocks = re.findall(pattern, content, re.DOTALL)

    return blocks

def check_code_block(code, filepath, block_num):
    """Check a code block for common issues"""
    issues = []

    # Check for incomplete class definitions
    if '{' in code and '}' in code:
        # Has braces, likely complete
        pass
    elif 'var ' in code or 'IObservable' in code:
        # Variable declarations without context
        issues.append("Code snippet without class/method context")

    # Check for undefined types (common in examples)
    undefined_types = []
    common_example_types = ['User', 'StockPrice', 'Order', 'Alert', 'OrderEvent']
    for type_name in common_example_types:
        if type_name in code and f'class {type_name}' not in code and f'record {type_name}' not in code:
            undefined_types.append(type_name)

    if undefined_types:
        issues.append(f"Uses undefined types: {', '.join(undefined_types)} (expected for examples)")

    # Check for undefined methods (common in examples)
    undefined_methods = []
    common_example_methods = [
        'GetUserAsync', 'SearchAsync', 'FetchDataAsync',
        'UpdateUI', 'ProcessData', 'CalculateExpensiveOperation',
        'ParseStockPrice', 'SlowConsumer', 'ProcessBatch'
    ]
    for method_name in common_example_methods:
        if method_name in code and f'async.*{method_name}' not in code and f'void {method_name}' not in code:
            undefined_methods.append(method_name)

    if undefined_methods:
        issues.append(f"Uses undefined methods: {', '.join(undefined_methods[:3])}... (expected for examples)")

    # Check for basic syntax errors
    if code.count('{') != code.count('}'):
        issues.append("⚠️ SYNTAX ERROR: Mismatched braces")

    if code.count('(') != code.count(')'):
        issues.append("⚠️ SYNTAX ERROR: Mismatched parentheses")

    # Check for common typos
    if 'Obsevable' in code:  # common typo
        issues.append("⚠️ TYPO: 'Obsevable' should be 'Observable'")

    return issues

def main():
    """Main function"""
    print("=" * 80)
    print("Checking C# Code Examples in Documentation")
    print("=" * 80)

    total_blocks = 0
    total_issues = 0
    critical_issues = 0

    # Get all markdown files
    md_files = glob.glob('docs/**/*.md', recursive=True)

    for filepath in sorted(md_files):
        blocks = extract_csharp_blocks(filepath)

        if not blocks:
            continue

        print(f"\n📄 {filepath}")
        print(f"   Found {len(blocks)} code blocks")

        for i, block in enumerate(blocks, 1):
            total_blocks += 1
            issues = check_code_block(block, filepath, i)

            if issues:
                total_issues += len(issues)
                print(f"\n   Block #{i}:")
                for issue in issues:
                    if '⚠️' in issue:
                        critical_issues += 1
                        print(f"      {issue}")
                    # else:
                    #     print(f"      ℹ️  {issue}")

    print("\n" + "=" * 80)
    print("Summary")
    print("=" * 80)
    print(f"Total code blocks checked: {total_blocks}")
    print(f"Total issues found: {total_issues}")
    print(f"Critical issues (syntax errors/typos): {critical_issues}")

    if critical_issues == 0:
        print("\n✅ No critical syntax errors found!")
        print("ℹ️  Note: Examples use placeholder types/methods by design")
    else:
        print(f"\n⚠️  {critical_issues} critical issues need to be fixed!")

    return critical_issues

if __name__ == '__main__':
    exit_code = main()
    exit(0 if exit_code == 0 else 1)
