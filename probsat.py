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
                avg = 0
                unsat = 0
                sat = 0
                # Run solver and store output
                for i in range(0,loop):
                    setup = '''
import subprocess

file = open("probsat_results/{file_name}.tmp.{num}", "w")
sys.stdout = file
'''.format(file_name=name,num=i)
       
                    file = open("probsat_results/{file_name}.tmp.{num}".format(file_name=name, num=i), "w")
                    t0 = time.time()
                    sp = subprocess.Popen(["probsat/probSAT/probSAT", "{file_name}".format(file_name=file_name)], stdout=file)
                    sp.communicate()
                    t1 = time.time()
                    avg += (t1-t0)
                    file.close()
                # Open stored output to see if solver successfully detected satisfiable and unsatisfiable SAT problem
                for i in range(0, loop):
                    path = "probsat_results/{file_name}.tmp.{num}".format(file_name=name, num=i)
                    with open(path, "r") as f:
                        seen_results = False
                        for line in f:
                            try:
                                if line.strip().split()[1] == "UNSATISFIABLE":
                                    unsat += 1
                                    seen_results = True
                                    break
                                elif line.strip().split()[1] == "SATISFIABLE":
                                    sat += 1
                                    seen_results = True
                                    break
                            except:
                                continue
                        if seen_results:
                            os.remove(path)
                r = name + " " + str(avg/loop) + " sat:" + str(sat) + " unsat:" + str(unsat) + "\n"
                results += r
                count += 1
    # Store output in single file
    with open("probsat_results/{tests}".format(tests=tests), "w") as o:
        o.write(results)

#Code starts here
benchmarks = [["uf20-91", 100], ["uf100-430", 100], ["UF125.538.100", 100]]
for bm in benchmarks:
    run_test(bm[0], bm[1])