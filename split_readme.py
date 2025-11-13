#!/usr/bin/env python3
"""
Split README.md into separate chapter files
"""
import re
import os

def split_readme():
    with open('README.md', 'r', encoding='utf-8') as f:
        content = f.read()

    # 각 Part와 Chapter의 시작 위치 찾기
    parts = []
    chapters = []
    appendices = []

    # Part 패턴
    part_pattern = r'^## 📘|^## 📗|^## 📙|^## 📕|^## 📒|^## 📓|^## 📔|^## 📖'
    # Chapter 패턴
    chapter_pattern = r'^### Chapter \d+:'
    # Appendix 패턴
    appendix_pattern = r'^### Appendix [A-Z]:'

    lines = content.split('\n')
    current_part = None
    current_chapter = None
    chapter_content = []

    part_mapping = {
        '📘': 'part1',
        '📗': 'part2',
        '📙': 'part3',
        '📕': 'part4',
        '📒': 'part5',
        '📓': 'part6',
        '📔': 'part7',
        '📖': 'appendix'
    }

    i = 0
    while i < len(lines):
        line = lines[i]

        # Part 시작 확인
        if re.match(part_pattern, line):
            # 이전 chapter 저장
            if current_chapter and chapter_content:
                save_chapter(current_part, current_chapter, '\n'.join(chapter_content))

            # Part 추출
            for emoji, dirname in part_mapping.items():
                if emoji in line:
                    current_part = dirname
                    break
            chapter_content = []
            current_chapter = None

        # Chapter 시작 확인
        elif re.match(chapter_pattern, line):
            # 이전 chapter 저장
            if current_chapter and chapter_content:
                save_chapter(current_part, current_chapter, '\n'.join(chapter_content))

            # Chapter 번호 추출
            match = re.search(r'Chapter (\d+):', line)
            if match:
                current_chapter = f"chapter{match.group(1).zfill(2)}"
                chapter_content = [line]

        # Appendix 시작 확인
        elif re.match(appendix_pattern, line):
            # 이전 chapter 저장
            if current_chapter and chapter_content:
                save_chapter(current_part, current_chapter, '\n'.join(chapter_content))

            # Appendix 추출
            match = re.search(r'Appendix ([A-Z]):', line)
            if match:
                current_part = 'appendix'
                current_chapter = f"appendix-{match.group(1).lower()}"
                chapter_content = [line]

        # Part나 다른 Chapter가 아니면 현재 chapter에 추가
        elif current_chapter:
            chapter_content.append(line)

        i += 1

    # 마지막 chapter 저장
    if current_chapter and chapter_content:
        save_chapter(current_part, current_chapter, '\n'.join(chapter_content))

def save_chapter(part, chapter_name, content):
    """Save chapter content to file"""
    if not part or not chapter_name:
        return

    filepath = f"docs/{part}/{chapter_name}.md"
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Saved: {filepath}")

if __name__ == '__main__':
    split_readme()
