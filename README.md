# Practical JavaScript Compiler

## Todo
- runtime for lists
- function expressions and statements
- boolean conversion using unary !
- truthy and falsy values
- Symbol table implementation
- 3 address code
- List

## Meetings
### First Meeting
- All lists are of a fixed size.
- No need of an input, a main will do the initializations.
- new can be handled using sbreak.
- anonymous function can be handled by giving out unique names.
- eval is left for the end: Done using the runtime
- Handling exceptions using a runtime object.
- overloading is left for the end: 
- The concept of an event loop as in Node?
- A runtime library for lists, hasmaps and inheritance.

## Technical Specifications
- Version                              : EC5.1
- Target                               : SPIM
- Lexer Generator                      : PLY
- Parser Generator                     : PLY
- Implementation                       : Python

## Idiosyncracies of JavaScript 
- Only one number type
- function language
- function scope
- JavaScript allows for arbitary comparisons between different types of data
    - Note, we use the python comparison results over here which may be a bit off
      as compared to JS results.

## Features not implemented
- Data types:
    - Only one number type: Integers
- Language Constructs
    - Ternary Operator
    - with
    - do while
    - switch case
    - RegEx
- OOP features of ES5.1
    - new
    - this
    - instanceof
    - delete
- Bitwise Operations and operators
```
    - & | ^ ~ >> << >>>
    - &= |= ^= >>= <<= >>>=
```
- Unused keywords
    - class
    - const
    - extends
    - field
    - final
    - import
    - package
    - private
    - protected
    - public
    - super
- Library routines are not implemented.
    - OOP features are not implemented because it is a library feature.

## Warts of the language
- eval
- Semicolon insertion
- comma at the end of arrays and objects
- '==' and '===' mean the same thing, strict checking
- '!=' and '!==' mean the same thing, strict checking
- '++' and '--' are not supported

# Usage
- run python lexer.py -y <testFileName>

## Tests
- All the test files need to added under the tests folder

## Dependencies
- Python 2.7 and higher
- [ply](https://github.com/dabeaz/ply)

