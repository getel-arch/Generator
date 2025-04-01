BOOL ModifyProcessCommandLine(HANDLE hProcess, const wchar_t* newCommandLine) {
    PROCESS_BASIC_INFORMATION pbi;
    ULONG ret;

    // Get PROCESS_BASIC_INFORMATION structure
    if (NtQueryInformationProcess(hProcess, ProcessBasicInformation, &pbi, sizeof(pbi), &ret) != 0) {
        return FALSE;
    }

    // Get PEB structure
    PEB peb;
    if (!ReadProcessMemory(hProcess, (PBYTE)pbi.PebBaseAddress, &peb, sizeof(peb), NULL)) {
        return FALSE;
    }

    // Get RTL_USER_PROCESS_PARAMETERS structure
    RTL_USER_PROCESS_PARAMETERS procParams;
    if (!ReadProcessMemory(hProcess, peb.ProcessParameters, &procParams, sizeof(procParams), NULL)) {
        return FALSE;
    }

    // Change command line
    if (!WriteProcessMemory(hProcess, procParams.CommandLine.Buffer, newCommandLine, wcslen(newCommandLine) * sizeof(wchar_t), NULL)) {
        return FALSE;
    }

    return TRUE;
}
