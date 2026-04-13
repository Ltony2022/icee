from threading import RLock

from src.core.logger import get_logger
from src.function.ApplicationBlock import ApplicationBlock
from src.helpers.FileClassification import FileClassification
from src.helpers.FileHandle import FileHandler
from src.helpers.ProcessWatcher import ProcessWatcher

logger = get_logger("application_block")


class WindowsApplicationBlock(ApplicationBlock):
    def __init__(self, output_file="Output.txt", poll_interval_seconds=1):
        logger.info("Initializing WindowsApplicationBlock")
        self._block_state: dict[str, bool] = {}
        self._lock = RLock()
        self._output_file = output_file
        self._poll_interval_seconds = poll_interval_seconds

        self._watcher: ProcessWatcher | None = None
        self._file_handler = FileHandler()
        self._file_classifier = FileClassification()

    def _snapshot(self):
        return [
            {"name": app, "blocked": state}
            for app, state in sorted(self._block_state.items())
        ]

    def _blocked_set(self):
        return {name for name, blocked in self._block_state.items() if blocked}

    def _restart_watcher(self):
        logger.debug("_restart_watcher called")
        if self._watcher is not None:
            self._watcher.stop()
            self._watcher = None

        blocked = self._blocked_set()
        if not blocked:
            logger.debug("No blocked processes, skipping watcher start")
            return

        logger.info("Starting ProcessWatcher with blocked=%s", blocked)
        self._watcher = ProcessWatcher(
            blocked_processes=blocked,
            output_file=self._output_file,
            poll_interval_seconds=self._poll_interval_seconds,
        )
        self._watcher.start()

    def add_block_application(self, application_name):
        logger.info("add_block_application called with: %s", application_name)
        application_name = (application_name or "").strip()
        if not application_name:
            raise ValueError("application name is required")

        key = application_name.lower()
        with self._lock:
            was_added = key not in self._block_state
            self._block_state[key] = False
        logger.info("Application '%s' %s", key, "added" if was_added else "already existed")
        return was_added, self._snapshot()

    def remove_block_application(self, application_name):
        logger.info("remove_block_application called with: %s", application_name)
        application_name = (application_name or "").strip()
        if not application_name:
            raise ValueError("application name is required")

        key = application_name.lower()
        with self._lock:
            if key not in self._block_state:
                logger.warning("Application '%s' not found in block list", key)
                raise KeyError(key)
            del self._block_state[key]
            self._restart_watcher()
        logger.info("Application '%s' removed", key)
        return self._snapshot()

    def list_blocked_application(self):
        logger.debug("list_blocked_application called")
        with self._lock:
            return self._snapshot()

    def enforce_block(self):
        logger.info("enforce_block called")
        with self._lock:
            for key in self._block_state:
                self._block_state[key] = True
            self._restart_watcher()
            return self._snapshot()

    def disable_block(self):
        logger.info("disable_block called")
        with self._lock:
            for key in self._block_state:
                self._block_state[key] = False
            if self._watcher is not None:
                self._watcher.stop()
                self._watcher = None
            return self._snapshot()

    def list_installed_applications(self):
        logger.info("list_installed_applications called")
        shortcuts = self._file_handler.ShortcutList()
        logger.debug("Found %d shortcuts", len(shortcuts))
        results = []
        for shortcut in shortcuts:
            display_name = shortcut.stem
            try:
                resolved = self._file_handler.FileResolve(shortcut)
                if not resolved.is_file():
                    continue
                classification = self._file_classifier.classify(
                    name=display_name,
                    path=resolved,
                    source=shortcut,
                )
                if classification.is_windows_builtin or classification.is_uninstall_or_update:
                    continue
                executable_name = self._file_handler.FileName(resolved)
                results.append(
                    {
                        "display_name": display_name,
                        "executable": executable_name,
                    }
                )
            except Exception as error:
                logger.error("Failed to resolve %s: %s", shortcut, error)
                continue
        results.sort(key=lambda app: app["display_name"].lower())
        logger.info("Resolved %d installed applications", len(results))
        return results

    def stop(self):
        logger.info("stop called")
        with self._lock:
            if self._watcher is not None:
                self._watcher.stop()
                self._watcher = None
