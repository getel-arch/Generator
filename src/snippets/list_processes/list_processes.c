// Function to list processes and return an array of ProcessInfo
int ListProcesses(ProcessInfo* processes, int maxProcesses) {
    HANDLE snapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
    if (snapshot == INVALID_HANDLE_VALUE) {
        printf("Failed to create snapshot\n");
        return -1;
    }

    PROCESSENTRY32 pe32;
    pe32.dwSize = sizeof(PROCESSENTRY32);

    if (!Process32First(snapshot, &pe32)) {
        printf("Failed to retrieve process information\n");
        CloseHandle(snapshot);
        return -1;
    }

    int processCount = 0;
    do {
        if (processCount >= maxProcesses) {
            break;
        }

        HANDLE process = OpenProcess(PROCESS_QUERY_INFORMATION, FALSE, pe32.th32ProcessID);
        if (process) {
            strncpy(processes[processCount].name, pe32.szExeFile, MAX_PATH);
            processes[processCount].pid = pe32.th32ProcessID;

            char* username = GetProcessUser(process);
            if (username) {
                strncpy(processes[processCount].user, username, MAX_PATH);
                free(username);
            } else {
                strncpy(processes[processCount].user, "Unknown", MAX_PATH);
            }

            CloseHandle(process);
        } else {
            strncpy(processes[processCount].name, pe32.szExeFile, MAX_PATH);
            processes[processCount].pid = pe32.th32ProcessID;
            strncpy(processes[processCount].user, "Unknown", MAX_PATH);
        }

        processCount++;
    } while (Process32Next(snapshot, &pe32));

    CloseHandle(snapshot);
    return processCount;
}
