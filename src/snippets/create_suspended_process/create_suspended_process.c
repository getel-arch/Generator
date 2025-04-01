BOOL CreateSuspendedProcess(LPCSTR commandLine, PROCESS_INFORMATION* pi) {
    STARTUPINFOA si = { sizeof(si) };
    return CreateProcessA(
        NULL, 
        (LPSTR)commandLine, 
        NULL, 
        NULL, 
        FALSE, 
        CREATE_SUSPENDED, 
        NULL, 
        NULL, 
        &si, 
        pi
    );
}
