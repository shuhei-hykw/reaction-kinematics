# Coding Rules

## Language
- Always respond in Japanese

## Style
- Indentation: 2 spaces (never tabs)
- In-code comments: English only
- Place a 79-character separator comment above every function and class
  definition (matching the def/class indentation):
  module-level: `#______________________________________________________________________________`
  (i.e., `#` followed by 78 underscores; the line totals 79 characters).
  For class methods at 2-space indent, use `  #` followed by 76 underscores
  so the line still totals 79 characters.

## Error handling
- Include essential error guards, but keep code concise and minimal

## Formatting
- Line length: 79 characters max
- Avoid magic numbers; always assign named constants

## Git
- Never include "Co-Authored-By: Claude" in commit messages

## Documentation
- Always update CHANGELOG.md and README.md in English
- CHANGELOG.md lives at the repository root (git-managed)
- CHANGELOG.md lists changes in **reverse chronological order** (newest at top)
- Each entry goes under `## YYYY-MM-DD HH:MM — <title>`
- Record what changed and why; include relevant physics context
