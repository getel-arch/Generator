void GetSystemTimeFormatted() {
    SYSTEMTIME st;
    GetSystemTime(&st);
    printf("Current system time (UTC): %02d-%02d-%04d %02d:%02d:%02d\n",
           st.wDay, st.wMonth, st.wYear, st.wHour, st.wMinute, st.wSecond);
}
