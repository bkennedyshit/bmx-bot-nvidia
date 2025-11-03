#!/usr/bin/env python3
"""
Convert markdown blog files to JSON format for RAG system
"""

import os
import json
import re
from datetime import datetime
from pathlib import Path
import argparse

def extract_frontmatter(content):
    """Extract YAML frontmatter from markdown content."""
    frontmatter = {}
    
    # Check for YAML frontmatter
    if content.startswith('---'):
        try:
            end_idx = content.find('---', 3)
            if end_idx != -1:
                frontmatter_text = content[3:end_idx].strip()
                content = content[end_idx + 3:].strip()
                
                # Simple YAML parsing for common fields
                for line in frontmatter_text.split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        key = key.strip()
                        value = value.strip().strip('"\'')
                        frontmatter[key] = value
        except:
            pass
    
    return frontmatter, content

def clean_markdown_content(content):
    """Clean markdown content for better RAG processing."""
    # Remove markdown syntax but keep structure
    content = re.sub(r'^#{1,6}\s+', '', content, flags=re.MULTILINE)  # Headers
    content = re.sub(r'\*\*(.*?)\*\*', r'\1', content)  # Bold
    content = re.sub(r'\*(.*?)\*', r'\1', content)  # Italic
    content = re.sub(r'`(.*?)`', r'\1', content)  # Inline code
    content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)  # Code blocks
    content = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', content)  # Links
    content = re.sub(r'!\[([^\]]*)\]\([^\)]+\)', r'\1', content)  # Images
    content = re.sub(r'\n\s*\n', '\n\n', content)  # Multiple newlines
    
    return content.strip()

def process_markdown_file(file_path):
    """Process a single markdown file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract frontmatter
        frontmatter, main_content = extract_frontmatter(content)
        
        # Clean content
        cleaned_content = clean_markdown_content(main_content)
        
        # Extract title (from frontmatter or first header)
        title = frontmatter.get('title', '')
        if not title:
            # Try to extract from first header
            title_match = re.search(r'^#\s+(.+)', content, re.MULTILINE)
            if title_match:
                title = title_match.group(1).strip()
            else:
                title = Path(file_path).stem.replace('-', ' ').replace('_', ' ').title()
        
        # Extract other metadata
        category = frontmatter.get('category', frontmatter.get('categories', 'General'))
        tags = frontmatter.get('tags', frontmatter.get('tag', ''))
        if isinstance(tags, str):
            tags = [tag.strip() for tag in tags.split(',') if tag.strip()]
        
        date = frontmatter.get('date', frontmatter.get('published', ''))
        
        # Create blog entry
        blog_entry = {
            "title": title,
            "content": cleaned_content,
            "category": category,
            "tags": tags if isinstance(tags, list) else [],
            "date": date,
            "source_file": str(file_path),
            "word_count": len(cleaned_content.split()),
            "char_count": len(cleaned_content)
        }
        
        return blog_entry
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

def find_markdown_files(directory):
    """Find all markdown files in directory and subdirectories."""
    md_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.md', '.markdown')) and not file.lower().startswith('readme'):
                md_files.append(os.path.join(root, file))
    return md_files

def main():
    parser = argparse.ArgumentParser(description='Convert markdown blog files to JSON for RAG system')
    parser.add_argument('input_dir', help='Directory containing markdown files')
    parser.add_argument('--output', '-o', default='../data/processed_blogs.json', 
                       help='Output JSON file path')
    parser.add_argument('--recursive', '-r', action='store_true', 
                       help='Search subdirectories recursively')
    
    args = parser.parse_args()
    
    # Find markdown files
    if args.recursive:
        md_files = find_markdown_files(args.input_dir)
    else:
        md_files = [os.path.join(args.input_dir, f) for f in os.listdir(args.input_dir) 
                   if f.lower().endswith(('.md', '.markdown')) and not f.lower().startswith('readme')]
    
    print(f"Found {len(md_files)} markdown files")
    
    # Process files
    blogs = []
    categories = set()
    
    for file_path in md_files:
        print(f"Processing: {file_path}")
        blog_entry = process_markdown_file(file_path)
        
        if blog_entry:
            blogs.append(blog_entry)
            if blog_entry['category']:
                categories.add(blog_entry['category'])
    
    # Create output structure
    output_data = {
        "blogs": blogs,
        "metadata": {
            "total_count": len(blogs),
            "last_updated": datetime.now().isoformat(),
            "categories": list(categories),
            "source_directory": args.input_dir,
            "processing_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    }
    
    # Ensure output directory exists
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write JSON file
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Successfully processed {len(blogs)} blog posts")
    print(f"📁 Output saved to: {output_path}")
    print(f"📊 Categories found: {', '.join(categories)}")
    print(f"📝 Total words: {sum(blog['word_count'] for blog in blogs):,}")

if __name__ == "__main__":
    main()