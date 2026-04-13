from argparse import FileType
from plistlib import InvalidFileException
import pythoncom
import win32com.client
import os
from pathlib import Path
from src.helpers.FileClassification import FileClassification
from src.core.logger import get_logger
# from icoextract import IconExtractor
# from PIL import Image
# from io import BytesIO

logger = get_logger("file_handle")


class FileHandler:
    def __init__(self, local: bool = True):
        logger.info("Initializing FileHandler")
        try:
            self.shell = win32com.client.Dispatch("WScript.Shell")
            self.ProgramFilesPath = os.path.join(
                os.environ["APPDATA"], "Microsoft", "Windows", "Start Menu", "Programs"
            )
            self.ProgramDataFilesPath = os.path.join(
                os.environ["ProgramData"],
                "Microsoft",
                "Windows",
                "Start Menu",
                "Programs",
            )
            logger.debug("ProgramFilesPath: %s", self.ProgramFilesPath)
            logger.debug("ProgramDataFilesPath: %s", self.ProgramDataFilesPath)
        except Exception as error:
            logger.error("Failed to initialize FileHandler: %s", error)

    def ShortcutList(self):
        logger.info("ShortcutList called")
        SKIP_DIRS = ["system tools", "system"]
        results = []
        FileClassifer = FileClassification()
        for root in [self.ProgramFilesPath, self.ProgramDataFilesPath]:
            root = Path(root)
            if not root.exists():
                logger.warning("Directory does not exist: %s", root)
                continue
            logger.debug("Scanning directory: %s", root)
            for dirpath, dirnames, filenames in os.walk(root):
                dirnames[:] = [d for d in dirnames if d.casefold() not in SKIP_DIRS]
                for f in filenames:
                    p = Path(dirpath) / f
                    if p.suffix.casefold() != ".lnk":
                        continue
                    result = FileClassifer.classify(name=f, source=p)
                    if not result.is_windows_builtin and not result.is_uninstall_or_update:
                        results.append(p)
        logger.info("ShortcutList found %d shortcuts", len(results))
        return results

    def FileName(self, filepath: str | Path):
        logger.debug("FileName called with: %s", filepath)
        filepath = Path(filepath)
        if filepath.exists():
            logger.debug("FileName result: %s", filepath.name)
            return filepath.name
        else:
            logger.error("File does not exist: %s", filepath)
            raise InvalidFileException(f"File does not exist: {filepath}")

    def ExtractFileIcon(self, path: str | Path, output_path: str | Path | None = None):
        # Implement later
        pass

    def ExtractListIcon(
        self, paths: list[str] | list[Path], output_path: str | Path | None = None
    ):
        # Implement later
        pass

    def FileResolve(self, path: str | Path):
        logger.debug("FileResolve called with: %s", path)
        try:
            FilePath = Path(path)
        except Exception as error:
            logger.error("Invalid path: %s — %s", path, error)
            raise InvalidFileException(f"Invalid path: {path}") from error

        logger.debug("FilePath suffix: '%s', repr: %r", FilePath.suffix, FilePath.suffix)
        if FilePath.suffix.casefold() == ".lnk":
            pythoncom.CoInitialize()
            try:
                shell = win32com.client.Dispatch("WScript.Shell")
                shortcut = shell.CreateShortcut(str(FilePath))
                target = shortcut.TargetPath
                logger.debug("Shortcut TargetPath: '%s'", target)
                resolved = Path(target)
                logger.debug("FileResolve resolved: %s -> %s", path, resolved)
                return resolved
            finally:
                pythoncom.CoUninitialize()

        if FilePath.is_symlink():
            resolved = FilePath.resolve()
            logger.debug("FileResolve resolved symlink: %s -> %s", path, resolved)
            return resolved

        logger.error("Unsupported file type: %s", FilePath)
        raise InvalidFileException(f"Unsupported file type: {FilePath.suffix}")

    def ExecutableList(self, shortcuts: list[str] | list[Path] | None = None):
        logger.info("ExecutableList called")
        if shortcuts is None:
            shortcuts = self.ShortcutList()
        resolved_count = 0
        for shortcut in shortcuts:
            try:
                resolved_path = self.FileResolve(shortcut)
                if resolved_path.is_file():
                    resolved_count += 1
                    yield resolved_path
            except InvalidFileException as error:
                logger.debug("Skipping shortcut %s: %s", shortcut, error)
                continue
        logger.info("ExecutableList resolved %d executables", resolved_count)

    def ListFileNames(
        self,
        shortcuts: list[str] | list[Path] | None = None,
        executables: list[str] | list[Path] | None = None,
    ):
        logger.info("ListFileNames called (shortcuts=%s, executables=%s)",
                    len(shortcuts) if shortcuts else None,
                    len(executables) if executables else None)
        if shortcuts is None and executables is None:
            raise ValueError("No shortcuts or executables provided")
        elif shortcuts:
            return [self.FileName(shortcut) for shortcut in shortcuts]
        elif executables:
            return [self.FileName(executable) for executable in executables]
