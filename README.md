TestEngine
==========

TestEngine is my personal unit-tester for commandline programs.

Example
-------

The following example tests a C++ program complied from `wlp4scan.cc`.

```
from Testers import CPPTester

tester = CPPTester( "./{{ binary_name }}", "wlp4scan.cc", __name__="__main__" )

tester.testcase("00", "ERROR", name="invalid two-zeros")

tester.out_stream = tester.STD_OUT
tester.testcase("0", "NUM 0", name="zero number")
tester.testcase("htht", ["This","Is an", "Example"])

tester.print_summary()
```

Usage
-----

To set up the unit-tester, import and construct the testing class you want.

There are currently 3 different classes:

```
CompileTester( command, compile_command )
    A blanket tester for all compiled programs
            command: command-line command you would invoke to test your program
    compile_command: command-line command to compile your program.

AsmTester( javaCommand, filename )
    A tester for cs241's .mips files
        javaCommand: command-line command you would invoke to test your program
           filename: the filename of your .mips source file

CPPTester( command, filename, [create=True] )
    A tester for C++ programs
            command: command-line command you would invoke to test your program
           filename: the filename[s] of your c++ source file[s], space delimited
             create: (optional) if false, does not compile source.
```

To write a test case, invoke the `testcase` method

```
{tester}.testcase( startup, asserts, [name=None] )
    Creates a test case.
            startup: what to feed in STDIN to your program
            asserts: what parts of the output should match
               name: (optiona) name of the test case
```

`asserts` may be either a string or a list (for multiple matches)

To conclude the test suite, invoke the `print_summary` method

```
{tester}.print_summary()
    Prints a summary of the results and performs cleanup.
```

Options
-------

Below are the options that all testers support.

You can set an option by writing `{tester_variable}.{option} = {new_value}`

```
TEMP_BINARY_NAME:           type: string
                            The binary file created when compiling the program.
                            Replaces {{ binary_name }} in the execute command
                            default: "tempbinary"

out_stream:                 type: STD_OUT or STD_ERR
                            The stream that the test will check.
                            default: STD_ERR
                        
always_print_output:        type: boolean
                            T: Always print the testcase's output
                            F: Only print the output if there's an error.
                            default: False

only_show_checked_output:   type: boolean
                            T: Only print the output specified by out_stream
                            F: Print only STD_OUT and STD_ERR output
                            default: False


exact_match_only:           type: boolean
                            T: out_stream must match expected result exactly
                            F: out_stream only needs to contain expected result
                            default: False

cleanup_binary:             type: boolean
                            T: Deletes the binary after testing has finished
                            F: Does not delete the temporary binary
                            default: True

```
