# 📝 Blog Processing Scripts

These scripts help you convert your markdown blog files into the JSON format needed for the RAG system.

## 🚀 Quick Start

### Option 1: Use Your Existing Markdown Files

If you already have markdown blog files:

```bash
cd ai-coach-bot/scripts

# Convert your markdown files to JSON
python convert_md_to_json.py /path/to/your/blog/files -r -o ../data/processed_blogs.json
```

### Option 2: Create Sample Content for Testing

If you want to test the system first with sample content:

```bash
cd ai-coach-bot/scripts

# Create sample blog files
python setup_sample_blogs.py

# Convert them to JSON
python convert_md_to_json.py sample_blogs -r -o ../data/processed_blogs.json
```

## 📋 Script Details

### `convert_md_to_json.py`

Converts markdown files to JSON format for the RAG system.

**Features:**
- Extracts YAML frontmatter (title, category, tags, date)
- Cleans markdown syntax for better RAG processing
- Handles nested directories
- Creates comprehensive metadata

**Usage:**
```bash
python convert_md_to_json.py <input_directory> [options]

Options:
  -r, --recursive     Search subdirectories
  -o, --output FILE   Output JSON file (default: ../data/processed_blogs.json)
```

**Expected markdown format:**
```markdown
---
title: "Your Blog Title"
category: "BMX Techniques"
tags: "bmx, tricks, tutorial"
date: "2024-01-15"
---

# Your Blog Title

Your blog content here...
```

### `setup_sample_blogs.py`

Creates sample blog content for testing.

**Creates 4 sample blogs:**
- BMX tricks for beginners
- Cardio training for BMX
- Choosing the right BMX bike
- BMX bike maintenance guide

**Usage:**
```bash
python setup_sample_blogs.py
```

## 📊 Output Format

The scripts create a JSON file with this structure:

```json
{
  "blogs": [
    {
      "title": "Blog Title",
      "content": "Cleaned blog content...",
      "category": "Category Name",
      "tags": ["tag1", "tag2"],
      "date": "2024-01-15",
      "source_file": "/path/to/file.md",
      "word_count": 500,
      "char_count": 3000
    }
  ],
  "metadata": {
    "total_count": 4,
    "last_updated": "2024-01-15T10:30:00",
    "categories": ["BMX Techniques", "Fitness"],
    "source_directory": "/path/to/blogs"
  }
}
```

## 🔧 Customization

### Adding Your Own Content

1. **Organize your markdown files** in a directory structure
2. **Add frontmatter** to each file (optional but recommended):
   ```yaml
   ---
   title: "Your Title"
   category: "Your Category"
   tags: "tag1, tag2, tag3"
   date: "2024-01-15"
   ---
   ```
3. **Run the conversion script**
4. **Test with the RAG system**

### Supported Frontmatter Fields

- `title`: Blog post title
- `category` or `categories`: Content category
- `tags` or `tag`: Comma-separated tags
- `date` or `published`: Publication date

### Content Processing

The script automatically:
- Removes markdown syntax (headers, bold, italic, links)
- Preserves paragraph structure
- Extracts title from frontmatter or first header
- Counts words and characters
- Handles UTF-8 encoding

## 🧪 Testing Your Content

After processing your blogs:

```bash
cd ../hackathon_aws_version
python test_rag.py
```

This will verify:
- Knowledge base loads correctly
- Embeddings are computed
- RAG retrieval works
- API endpoints respond

## 💡 Tips

1. **Use descriptive titles** - they're weighted heavily in retrieval
2. **Add relevant tags** - helps with categorization
3. **Keep content focused** - each blog should cover a specific topic
4. **Include practical advice** - the RAG system works best with actionable content
5. **Test regularly** - run the test script after adding new content

## 🚨 Troubleshooting

**"No markdown files found"**
- Check your directory path
- Use `-r` flag for recursive search
- Ensure files have `.md` or `.markdown` extension

**"Empty processed_blogs.json"**
- Check for errors in markdown processing
- Verify frontmatter format
- Look for encoding issues

**"RAG system not finding content"**
- Ensure JSON file is in correct location (`ai-coach-bot/data/processed_blogs.json`)
- Check file permissions
- Verify JSON format is valid