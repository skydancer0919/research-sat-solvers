import os
import io
import sys
import time
import subprocess
from timeit import timeit

def run_test(tests, loop=10):
    results = ""
    count = 1
    for root, dirs, files in os.walk(tests):
        for name in files:
            if name.endswith((".cnf")):
                file_name = os.path.abspath(os.path.join(root,name))
                #format_tests(file_name)
                avg = 0
                unsat = 0
                sat = 0
                # Run solver and store output
                for i in range(0,loop):
                    setup = '''
import subprocess

file = open("minisat_2005_results/{file_name}.tmp.{num}", "w")
sys.stdout = file
'''.format(file_name=name,num=i)
       
                    file = open("minisat_2005_results/{file_name}.tmp.{num}".format(file_name=name, num=i), "w")
                    t0 = time.time()
                    sp = subprocess.Popen(["minisat/core/minisat_static", "{file_name}".format(file_name=file_name)], stdout=file)
                    sp.communicate()
                    t1 = time.time()
                    avg += (t1-t0)
                    file.close()
                # Open stored output to see if solver successfully detected satisfiable and unsatisfiable SAT problem
                for i in range(0, loop):
                    path = "minisat_2005_results/{file_name}.tmp.{num}".format(file_name=name, num=i)
                    with open(path, "r") as f:
                        seen_results = False
                        for line in f:
                            if line.strip() == "UNSATISFIABLE":
                                unsat += 1
                                seen_results = True
                                break
                            elif line.strip() == "SATISFIABLE":
                                sat += 1
                                seen_results = True
                                break
                        if seen_results:
                            os.remove(path)
                r = name + " " + str(avg/loop) + " sat:" + str(sat) + " unsat:" + str(unsat) + "\n"
                print(r)
                print("Finished test {num}".format(num=count))
                results += r
                count += 1
    # Store output in single file
    with open("minisat_2005_results/{tests}".format(tests=tests), "w") as o:
        o.write(results)

#Code starts here
#benchmarks = [["uf20-91", 100]]
benchmarks = [["uf20-91", 100], ["uf100-430", 100], ["UUF100.430.1000", 100], ["UF125.538.100", 100],["UUF125.538.100", 100]]
#benchmarks = ["uf20-91", "uf100-430", "UUF100.430.1000", "UF125.538.100","UUF125.538.100", "UF250.1065.100", "UUF250.1065.100"]
for bm in benchmarks:
    run_test(bm[0], bm[1])