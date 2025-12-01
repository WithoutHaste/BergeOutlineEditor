# Berge Outline Editor

Small app to keep writing organized from outline to final version. 

## Quick Start

Python:
- Navigate to `python` folder
- Run `python3 app_berge_outline_editor.py`.

## Keyboard Commands

### When inside a section (textbox):

Alt+Enter will insert a new section sibling after the current one.

Alt+Plus will insert the first child of the current section.
- ditto for Alt+Equal (because this keyboard doesn't have a keypad)
- ditto for Alt+m ("m" for "more", to offer a name-based key mapping)

Alt+Down will move focus to the next section downward

Alt+Up will move focus to the previous section upward
- built-in Shift+Tab also works

Alt+Left will move focus to the parent of the current section

Alt+Right will move focus to the first child of the current section

Control+s will save the file under the current filename

## Local Settings

App saves a local `berge.ini` file with your settings:
- Last-used filename is saved, and is automatically opened when the app is started again.

## Architecture

Python3

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
  - a lower level marked whose text starts with `(final)\n` is part of the final draft of the document
- when Berge saves, it appends a duplicate section at the end of the document
  - this section is just the `(final)` pieces all put together, so the final draft can be read
  - do not edit this section yourself, it will be overwritten when Berge saves again - any differences between this duplicate section and the upper sections will be ignored
  
See `test_files` directory for examples of the file format.

## Warnings

Berge is built entirely for my own use, so feature development will end as soon as it works well enough for my projects.  The gui is built for my screen and viewing habits.
- I'm hopping between Berge and Notepad++ depending on which one is easier to do the current editing in.  Berge for managing the sections (outline linked to final text), and Notepad++ for rearranging big pieces of the file.

Berge is built for small projects.  It loads the entire text of the document at once, so a large document could cause it to run out of memory.
