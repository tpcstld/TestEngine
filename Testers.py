#1/usr/bin/python
import subprocess

"""
Options:
    TEMP_BINARY_NAME (string): 
        Rename the temporary binary file created
        Replaces {{ binary_name }} in the compile string
        default: "tempbinary"
    out_stream (STD_OUT|STD_ERR): 
        Choose which stream the test will read it's output from
        default: STD_ERR
    always_print_output (bool): 
        True: Print the binary's output, even if there's no error
        False: Only print the binary's output if there's an error
        default: False
    only_show_checked_output (bool): 
        True: When printing output, only show the stream specified by out_stream
        False: When printing output, show's both STD_OUT and STD_ERR output
        default: False
    debug_tester (bool): 
        True: Show the shell commands that the tester is executing
        False: Do not log show the shell commands
        default: False
    exact_match_only (bool):
        True: Output from out_stream must match exactly
        False: Output from out_stream 
        default: False
    cleanup_binary (bool):
        True: Deletes the temporary binary after testing has finished
        False: Does not delete the temporary binary
        default: True

Example:

    import sys
    sys.path.append("../testing")
    from Testers import CPPTester

    tester = CPPTester( ".//{{ binary_name }}", "wlp4scan.cc", __name__=="__main__")
    tester.always_print_output = True

    tester.testcase("00", "ERROR", name="invalid twozeros")
    tester.testcase("0", "NUM 0", name="zero number")
    tester.testcase("htht", ["This","Is an", "Example"])
    
    tester.print_summary()
"""

class BaseTester:
    TEMP_BINARY_NAME = "tempbinary"
    STD_OUT = 0
    STD_ERR = 1
    test_counter = 1
    out_stream = STD_ERR
    execute_program_command = None
    always_print_output = False
    only_show_checked_output = False
    debug_tester = False
    exact_match_only = False
    cleanup_binary = True
    failed_tests = []

    def compile_binary(self, command):
        p = self.execute_process(command)
        p.communicate()

    def execute_process(self, command, outputs=None):
        if (self.debug_tester):
            print "Executing command: " + command
        return subprocess.Popen(command, shell=True, stdin=outputs, stdout=outputs, stderr=outputs)

    def cleanup_tempbinary(self):
        p = self.execute_process("rm " + self.TEMP_BINARY_NAME)
        p.communicate()

    def print_summary(self):
        print ""
        print "### SUMMARY ###"
        print "Tests ran:", self.test_counter - 1

        num_failed = len(self.failed_tests)
        if num_failed > 0:
            failed_string = "\033[91m" + str(num_failed) + "\033[0m"
        else:
            failed_string = "\033[92m" + str(num_failed) + "\033[0m"

        print "Tests failed:", failed_string
        if self.cleanup_binary:
            self.cleanup_tempbinary()

    def testcase(self, startup, asserts, name=None):
        command = self.execute_program_command.replace("{{ binary_name }}", self.TEMP_BINARY_NAME)
        p = self.execute_process(command, subprocess.PIPE)

        output = p.communicate(input=startup)
        success = True
        failed_testcase = None
        if isinstance(asserts, list):
            for case in asserts:
                try:
                    if self.exact_match_only:
                        assert case == output[self.out_stream]
                    else:
                        assert case in output[self.out_stream]
                except:
                    success = False
                    failed_testcase = case
                    break
        else:
            try:
                if self.exact_match_only:
                    assert asserts == output[self.out_stream]
                else:
                    assert asserts in output[self.out_stream]
            except:
                success = False
                failed_testcase = asserts

        test_name = "\033[36m"                    
        if name is None:
            test_name += str(self.test_counter)
        else:
            test_name += name
        test_name += "\033[0m"

        if success:
            print "Test " + test_name  + "\033[92m" + " passed!" + "\033[0m"
        else:
            print "Test " + test_name  + "\033[91m" +  " FAILED!" + "\033[0m"

            exact_match_string = ""
            if self.exact_match_only:
                exact_match_string = "\033[95m" + "(Exact Match)" + "\033[0m" 

            print "Failing testcase: " + "\033[93m" + failed_testcase + "\033[0m", exact_match_string
            self.failed_tests = self.failed_tests + [test_name]

        if not success or self.always_print_output:
            if self.only_show_checked_output:
                print output[self.outStream]
            else:
                print output
        self.test_counter = self.test_counter + 1

class CompileTester(BaseTester):
    def __init__(self, command, compile_command):
        self.execute_program_command = command;
        self.compile_binary(compile_command)

class AsmTester(BaseTester):
    def __init__(self, javaCommand, filename):
        self.execute_program_command = javaCommand
        command = "java cs241.binasm < " + filename + " > " + self.TEMP_BINARY_NAME
        self.compile_binary(command)

class CPPTester(BaseTester):
    def __init__(self, run_command, filename, create=True):
        self.execute_program_command = run_command
        if create:
            command = "g++ " + filename + " -o " + self.TEMP_BINARY_NAME
            self.compile_binary(command)
