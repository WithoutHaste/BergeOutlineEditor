# Berge Outline Editor

Small app to keep writing organized from outline to final version. 

## Architecture

Python3

## File Format

Goals:
- format is legible as-is
- format is simple enough that a user could write/edit it directly
- text-based files can be edited by other tools (non-proprietary)

File Format: Text/Markdown

Inner Format:
- top-level headers indicate the "outline" units
  - each lower level under that indicates a greater level of detail being added
  - a lower level marked with "(scene)" is part of the final draft of the document
- when Berge saves, it appends a duplicate section at the end of the document
  - this section is just the "(scene)" pieces all put together, so the final draft can be read
  - do not edit this section yourself, it will be overwritten when Berge saves again - any differences between this duplicate section and the upper sections will be ignored
  
See `test_files` directory for examples of the file format.

## Features

TODO