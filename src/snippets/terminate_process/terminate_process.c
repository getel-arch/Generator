BOOL TerminateProcessById(DWORD pid) {
    HANDLE hProcess = OpenProcess(PROCESS_TERMINATE, FALSE, pid);
    if (!hProcess) {
        printf("Failed to open process with PID %lu\n", pid);
        return FALSE;
    }

    BOOL result = TerminateProcess(hProcess, 0);
    CloseHandle(hProcess);
    return result;
}
