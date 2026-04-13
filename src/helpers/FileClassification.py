from __future__ import annotations
import re
from dataclasses import dataclass
from pathlib import Path
import os


@dataclass(frozen=True)
class ClassificationResult:
    is_exe: bool
    is_windows_builtin: bool
    is_uninstall_or_update: bool

    @property
    def keep(self) -> bool:
        return self.is_exe and not (
            self.is_windows_builtin or self.is_uninstall_or_update
        )


class FileClassification:
    def __init__(self):
        pass

    UNINSTALL_PATTERNS = (
        r"\buninstall\b",
        r"\bunin\b",
        r"\bremove\b",
        r"\bmaintenance\b",
        r"\bupdater?\b",
        r"\bupdate\b",
        r"\brepair\b",
        r"\bmodify\b",
    )

    BUILTIN_NAME_KEYWORDS = {
        "windows security",
        "windows tools",
        "control panel",
        "command prompt",
        "powershell",
        "registry editor",
        "task manager",
        "disk cleanup",
        "system configuration",
        "defragment and optimize drives",
        "remote desktop connection",
    }

    WINDOWS_DIR_PREFIXES = (
        r"c:\windows",
        r"c:\program files\windowsapps",
    )

    def classify(
        self, *, name: str, path: Path | None = None, source: Path | None = None
    ) -> ClassificationResult:
        name = name.casefold().strip()
        target_text = str(path).casefold() if path else ""
        folder_text = str(source).casefold() if source else ""

        is_exe = bool(path and path.suffix.casefold() == ".exe")

        is_uninstall_or_update = False
        if any(re.search(pat, name) for pat in self.UNINSTALL_PATTERNS):
            is_uninstall_or_update = True
        elif target_text and (
            "unins" in target_text
            or "uninstall" in target_text
            or "update.exe" in target_text
            or "\\updater\\" in target_text
        ):
            is_uninstall_or_update = True

        is_windows_builtin = False
        if name in self.BUILTIN_NAME_KEYWORDS:
            is_windows_builtin = True
        elif "\\windows\\start menu\\programs\\system tools" in folder_text:
            is_windows_builtin = True
        elif target_text and any(
            target_text.startswith(p) for p in self.WINDOWS_DIR_PREFIXES
        ):
            is_windows_builtin = True

        return ClassificationResult(
            is_exe=is_exe,
            is_windows_builtin=is_windows_builtin,
            is_uninstall_or_update=is_uninstall_or_update,
        )
