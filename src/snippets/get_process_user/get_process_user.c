char* GetProcessUser(HANDLE process) {
    HANDLE token = NULL;
    if (!OpenProcessToken(process, TOKEN_QUERY, &token)) {
        return NULL;
    }

    DWORD size = 0;
    GetTokenInformation(token, TokenUser, NULL, 0, &size);
    if (GetLastError() != ERROR_INSUFFICIENT_BUFFER) {
        CloseHandle(token);
        return NULL;
    }

    PTOKEN_USER tokenUser = (PTOKEN_USER)malloc(size);
    if (!GetTokenInformation(token, TokenUser, tokenUser, size, &size)) {
        free(tokenUser);
        CloseHandle(token);
        return NULL;
    }

    SID_NAME_USE sidType;
    char domain[MAX_PATH];
    DWORD domainSize = MAX_PATH;
    char username[MAX_PATH];
    DWORD usernameSize = MAX_PATH;

    if (!LookupAccountSid(NULL, tokenUser->User.Sid, username, &usernameSize, domain, &domainSize, &sidType)) {
        free(tokenUser);
        CloseHandle(token);
        return NULL;
    }

    free(tokenUser);
    CloseHandle(token);

    // Allocate and return the username
    return strdup(username);
}
