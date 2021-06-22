# Markdown Guidelines

<!-- mdformat-toc start --slug=github --maxlevel=6 --minlevel=2 -->

- [Markdown Styling](#markdown-styling)
- [Suggested tooling](#suggested-tooling)
  - [Formatting](#formatting)
  - [Table of Contents (ToC)](#table-of-contents-toc)

<!-- mdformat-toc end -->

## Markdown Styling<a name="markdown-styling"></a>

1. 100% [CommonMark](https://spec.commonmark.org/current/) compliance

2. Continuous numbered ordered list markers (use `1.`, `2.`, `3.`... instead of `1.`,
   `1.`, `1.`... for ordered lists)

3. Wrap lines at 100 characters

4. Loose lists, i.e each list item is preceded and followed by an empty line

5. Table of contents is the start of every file

6. HTML based heading links. eg. `## Markdown Styling<a name="markdown-styling"></a>`

## Suggested tooling<a name="suggested-tooling"></a>

### Formatting<a name="formatting"></a>

Use `mdformat-gfm`, a plugin for `mdformat` built for github flavoured markdown

- `$ pip install mdformat-gfm`

- To check compliance: `$ mdformat --check --number --wrap 90 ./source_folder`

- To make required changes: `$ mdformat --number --wrap 90 ./source_folder`

- __NOTE:__ `mdformat` wraps words beyond the 100 character mark to the next line, if a
  word starts at the 99th character, it remains on the same line making the total line
  length 100+, it is for this reason that the `--wrap` is passed a line length of __90__
  instead of __100__

### Table of Contents (ToC)<a name="table-of-contents-toc"></a>

Use `mdformat-toc`, a plugin for `mdformat` built to auto-generate ToC's

- `$ pip install mdformat-toc`

- Add `<!-- mdformat-toc start --slug=github --minlevel=2 -->` to the start of every
  markdown file

- Run `mdformat` to construct the ToC
