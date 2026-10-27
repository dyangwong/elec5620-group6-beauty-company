"""Read Windows memory/version/CPU instruction support without requiring WMI."""
import ctypes
import json
import platform


class Memory(ctypes.Structure):
    _fields_ = [("length", ctypes.c_ulong), ("load", ctypes.c_ulong)] + [
        (name, ctypes.c_ulonglong) for name in ("total", "available", "totalPage", "availablePage",
                                               "totalVirtual", "availableVirtual", "extended")]


def main():
    report = {"platform": platform.platform(), "python": platform.python_version()}
    if platform.system() == "Windows":
        memory = Memory()
        memory.length = ctypes.sizeof(Memory)
        if not ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(memory)):
            raise ctypes.WinError()
        report.update(totalPhysicalBytes=memory.total, availablePhysicalBytes=memory.available,
                      avx2=bool(ctypes.windll.kernel32.IsProcessorFeaturePresent(40)))
        length = ctypes.c_ulong(0)
        kernel = ctypes.windll.kernel32
        kernel.GetLogicalProcessorInformationEx(0, None, ctypes.byref(length))
        buffer = ctypes.create_string_buffer(length.value)
        if not kernel.GetLogicalProcessorInformationEx(0, buffer, ctypes.byref(length)):
            raise ctypes.WinError()
        offset, cores = 0, 0
        while offset < length.value:
            relation = ctypes.c_ulong.from_buffer(buffer, offset).value
            size = ctypes.c_ulong.from_buffer(buffer, offset + 4).value
            if size < 8 or offset + size > length.value:
                raise ValueError("Invalid Windows processor topology")
            if relation == 0:
                cores += 1
            offset += size
        report["physicalCores"] = cores
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
