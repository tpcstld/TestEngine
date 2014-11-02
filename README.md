TestEngine
==========

TestEngine is my personal unit-tester for commandline programs.

Example
-------

The following example tests a C++ program complied from `wlp4scan.cc`.

```
  from Testers import CPPTester

  tester = CPPTester( "/{{ binary_name }}", "wlp4scan.cc", __name__="__main__" )

  tester.testcase("00", "ERROR", name="invalid two-zeros")
  tester.testcase("0", "NUM 0", name="zero number")
  tester.testcase("htht", ["This","Is an", "Example"])
  
  tester.print_summary()
```
