class InvalidArchivePathException(Exception):

    def __str__(self):
        return "Invalid archive path provided."


class ArchivePathNotFoundException(Exception):
    def __str__(self):
        return "Archive path does not exist."


class UnsupportedArchiveFormatException(Exception):
    def __str__(self):
        return "Unsupported archive format."


class UnZipFileException(Exception):
    def __str__(self):
        return "Failed to unzip the archive."
