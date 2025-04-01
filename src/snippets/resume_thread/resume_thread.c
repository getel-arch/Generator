DWORD ResumeThreadByHandle(HANDLE threadHandle) {
    DWORD resumeCount = ResumeThread(threadHandle);
    if (resumeCount == (DWORD)-1) {
        printf("Error: Unable to resume thread (error code: %lu)\n", GetLastError());
    }
    return resumeCount;
}
