from memory_profiler import profile
from line_profiler import LineProfiler

import controller
import model
import view1

global file_name = "data_profiling.json"

class library_profiler:
    def __init__(self):
        global file_name
        model.file_path = file_name
        with open(file_name, mode='a'):
            pass

    @profile
    def io_cpu_profile():
        lprofiler = LineProfiler()
        lprofiler.add_function(model.open_file)
        lprofiler.add_function(model.save_file)

        def run():
            view1.start_process()
            

        lp_wrapper = lprofiler(run)
        lp_wrapper()
        lprofiler.print_stats()



if __name__ == "__main__":
    profiler = library_profiler()
