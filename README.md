# Todo
- relational expressions
- function expressions and statements
- types and variables
- find NaN, null in python
    - NaN is not equalt to NaN and is toxic
- assignment shorthands
- string to number conversion using unary +
- boolean conversion using unary !
- truthy and falsy values
- taking input

# Practical JavaScript Compiler

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
- RegEx
- Ternary Operator

## Warts of the language
- with
- eval
- Semicolon insertion
- comma at the end of arrays and objects
- '+' is not overloaded for strings and numbers
- '==' and '===' mean the same thing
- '!=' and '!==' mean the same thing
- '++' and '--' are not supported

## Features Implemented till now
- Declaration of variables
    - Objects and arrays are supported
- Assignment of values to variables
- Addition, Subtratction, Multiplication, Division of numbers
- String concatenation

# Usage
- run python lexer.py <testFileName>

# Build Instruction
- lexer.py contains the token definitions
    - the variable **lexer** stores the lexer
    - to start lexing, we need to give **lexer** a string and call **lexer.token** for a token

## Dependencies
- Python 2.7 and higher
- [ply](https://github.com/dabeaz/ply)

## Compiling and Building
- The builds are only for a Linux compliant machine (preferably Ubuntu)
- Use the makefile provided (instructions will be added as and when new components will be added)

## Tests
- All the test files need to added under the tests folder

