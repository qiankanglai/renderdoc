import renderdoc as rd
import os
import time
import rdtest


class VK_Large_Descriptor_Sets(rdtest.TestCase):
    demos_test_name = 'VK_Large_Descriptor_Sets'

    def run(self):
        self.capture_filename = self.get_capture()

        self.check(os.path.exists(self.capture_filename), "Didn't generate capture in make_capture")

        rdtest.log.print("Loading capture")

        memory_before: int = rd.GetCurrentProcessMemoryUsage()
        start_time = time.time()

        self.controller = rdtest.open_capture(self.capture_filename, opts=self.get_replay_options())

        duration = time.time() - start_time
        memory_after: int = rd.GetCurrentProcessMemoryUsage()

        memory_increase = memory_after - memory_before

        rdtest.log.print("Loaded capture in {:02} seconds, consuming {} bytes of memory".format(duration, memory_increase))

        if memory_increase > 1200*1000*1000:
            raise rdtest.TestFailureException("Memory usage is too high".format(duration))
        else:
            rdtest.log.success("Memory usage is OK")

        if rd.IsReleaseBuild():
            if duration >= 2.5:
                raise rdtest.TestFailureException("Time to load is too high")
            rdtest.log.success("Time to load is OK")
        else:
            rdtest.log.print("Not checking time to load in non-release build")

        if self.controller is not None:
            self.controller.Shutdown()