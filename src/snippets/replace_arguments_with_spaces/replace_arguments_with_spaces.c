void ReplaceArgumentsWithSpaces(const char *original, char *modified) {
    const char *firstSpace = strchr(original, ' ');
    if (firstSpace != NULL) {
        size_t length = firstSpace - original + 1;
        strncpy(modified, original, length);
        memset(modified + length, ' ', strlen(original) - length);
        modified[strlen(original)] = '\0';
    } else {
        strcpy(modified, original);
    }
}
