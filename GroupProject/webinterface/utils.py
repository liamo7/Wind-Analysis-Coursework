from GroupProject import settings


def printAllFilesInDirectory():
    import os
    for r, d, f in os.walk(settings.BASE_DIR):
        for file in f:
            print(os.path.join(settings.BASE_DIR, file))