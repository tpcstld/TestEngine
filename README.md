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
  tester.testcase("0", "NUM 0", name="zero number")
  tester.testcase("htht", ["This","Is an", "Example"])
  
  tester.print_summary()
```

Options
-------

Below are the options that all testers support.

You can set an option by writing `{tester_variable}.{option} = {new_value}

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
