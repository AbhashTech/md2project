
# MD2PROJECT

With advantment of AI and different platform, there are people who can not afford premium plan but have generated great lines of code. Thinking about them(And obviously by ourself),we've created a **universal Markdown to Project Structure utility** that automatically extracts file paths and code blocks from markdown documentation and creates the corresponding folders and files.

## What Was Created

**1. md2project.py** - The main utility script that:

- Extracts files from markdown using multiple pattern formats (bold filenames, headers, backticks)
- Supports 15+ file types (.ts, .tsx, .js, .jsx, .json, .css, .html, .md, .py, .go, .sh, .yaml, .yml, .toml, .txt, .env, .gitignore)
- Intelligently filters out command blocks (npm install, cd commands, etc.)
- Creates complete directory structures automatically
- Provides dry-run mode to preview before creating files

**2. README.md** - Complete documentation with examples and troubleshooting

## How to Use

### Basic Usage

```bash
# Single markdown file
python md2project.py documentation.md

# Multiple markdown files (like yours)
python md2project.py Create-react-frontend-using-react19-vite-tailwin.md provide-rest-of-the-code-as-well.md -o billing-frontend

# Preview without creating
python md2project.py docs.md --dry-run

# Custom output directory
python md2project.py docs.md -o my-project-name
```


### For Your Specific Files

```bash
python md2project.py \
  Create-react-frontend-using-react19-vite-tailwin.md \
  provide-rest-of-the-code-as-well.md \
  -o billing-frontend

cd billing-frontend
npm install
npm run dev
```


## Features

The utility successfully detected **38 files** from your markdown files, including all the React components, API files, pages, hooks, utilities, and configuration files organized across **10 directories** (src/api, src/components/common, src/components/customers, src/components/products, src/hooks, src/pages, src/store, src/types, src/utils).

## Supported Markdown Formats

- `**filename.ts**` followed by code block
- `**filename.ts**[1]` with references
- `### filename.ts` as headers
- ```filename.ts``` with backticks

The utility is completely standalone, requires only Python 3.6+, no external dependencies, and works universally with any markdown file containing code blocks with file paths.

