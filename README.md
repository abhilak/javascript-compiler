# Practical JavaScript Compiler

# Todo
- Lists
    - Runtime
    - Normal implementation
    - Thinking of making it a C type array with only one type of element
- Parameters as an array ' arguments array'
- A variable cache for variables loaded in from another scope
- Error productions:
    - Declaration statments without a semicolon
    - Empty statements
- Replace 'place' with the function name, this will maintain consistency
in the way 'place' is handled all across
- Register Allocation:
    - Remove redundancy as both caller and callee are flushing registers.
    - Make use of dirty bit
    - Update flushtemporary and flsuh registers to make used of function name
    and dirty bit
    - Use nextReg heuristic

# Issues

# Language Specification
## Unique Stuff
- Breaks and continues don't signal errors, but they are silently removed
- The idea of callbacks:
    - Callbacks are the pascal equivalent of procedures.
    - They don't return values and hence cannot be used in expressions.
    - Callbacks can be passed to functions.
    - Callbacks can be returned from functions.
- Typing
    - Strongly typed.
    - Parameters are not type checked.
- Functions
    - Not hoisted, you have to define them before using them.
    - No closures
    - The number of parameters is not checked
    - Type Hinting: The types of function parameters needs to be hinted
- Strings defined using double quotes are constants
- Blocks must have curly braces
- Scoping
    - Lexical Scoping
    - Function is the fundamental unit of scope

## Features not implemented
- Data types:
    - Only one number type: Integers
    - Objects
    - No NaN, INFINITY and NULL
- Language Constructs
    - Ternary Operator
    - with
    - do while
    - switch case
    - RegEx
    - try, catch, finally and throw
    - for 
    - SIAF
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
- Type coercion
    - '+' does not change type to string
    - '!' does not change type to string, it can be only used on boolean operators
    - expression are not automatically converted to boolean in case of logical expressions

## Warts of the language
- eval
- Semicolon insertion
- comma at the end of arrays and objects
- '==' and '===' mean the same thing, strict checking
- '!=' and '!==' mean the same thing, strict checking
- '++' and '--' are not supported

## Meetings
### First Meeting
- All lists are of a fixed size.
- ~~No need of an input, a main will do the initializations~~
- ~~anonymous function can be handled by giving out unique names~~
- new can be handled using sbreak.
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

## Dependencies
- Python 2.7 and higher
- [ply](https://github.com/dabeaz/ply)

# Flow
- JSlexer defines a debug instance and a lexer instance.
- parser defines a ST, TAC and parser instance.
- runTime define a RTC which uses all of the above.

# Usage
- run make
- ./runTime.py <testFileName>

