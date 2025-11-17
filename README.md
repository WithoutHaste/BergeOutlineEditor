# Berge Outline Editor

Small app to keep writing organized from outline to final version. 

## Quick Start

Python:
- Navigate to `python` folder > Run `python3 app_berge_outline_editor.py`.

## Keyboard Commands

### When inside a section (textbox):

Alt+Enter will insert a new section sibling after the current one.

Alt+Down will move focus to the next section downward

Alt+Up will move focus to the previous section upward
- built-in Shift+Tab also works

Alt+Left will move focus to the parent of the current section

Alt+Right will move focus to the first child of the current section

## Architecture

Jumping between Python and C++, depending on which seems easier.

## File Format

Goals:
- format is legible as-is
- format is simple enough that a user could write/edit it directly
- text-based files can be edited by other tools (non-proprietary)

File Format: Text/Markdown

Inner Format:
- section headers don't actually matter, except for the "Duplicate" one
  - section headers will be re-written by Berge on each save, so don't put important info into them
- top-level headers indicate the "outline" units
  - each lower level under that indicates a greater level of detail being added
  - a lower level marked with "(final)" is part of the final draft of the document
- when Berge saves, it appends a duplicate section at the end of the document
  - this section is just the "(final)" pieces all put together, so the final draft can be read
  - do not edit this section yourself, it will be overwritten when Berge saves again - any differences between this duplicate section and the upper sections will be ignored
  
See `test_files` directory for examples of the file format.

## Warnings

Berge is built entirely for my own use, so feature development will end as soon as it works well enough for my projects.  The gui is built for my screen and viewing habits.

Berge is built for small projects.  It loads the entire text of the document at once, so a large document could cause it to run out of memory.
