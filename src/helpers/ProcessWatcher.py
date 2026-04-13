import os
import signal
from threading import Event, Thread

import pythoncom
import wmi


class ProcessWatcher:
    def __init__(
        self,
        blocked_processes=None,
        output_file="Output.txt",
        poll_interval_seconds=1,
    ):
        self.blocked_processes = {
            proc.lower() for proc in (blocked_processes or [])
        }
        self.output_file = output_file
        self.poll_interval_seconds = poll_interval_seconds

        self._stop_event = Event()
        self._thread = None

        self._terminate_existing_blocked_processes()

    def start(self):
        if self._thread and self._thread.is_alive():
            return

        self._stop_event.clear()
        self._thread = Thread(target=self._listen_process_creation, daemon=True)
        self._thread.start()

    def stop(self):
        self._stop_event.set()
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=self.poll_interval_seconds + 1)

    def _listen_process_creation(self):
        pythoncom.CoInitialize()
        try:
            watcher = self._create_process_watcher()
            print("Listening for application launches...")

            while not self._stop_event.is_set():
                try:
                    event = watcher(timeout_ms=int(self.poll_interval_seconds * 1000))
                except wmi.x_wmi_timed_out:
                    continue

                process = getattr(event, "TargetInstance", event)
                self._handle_new_process(process)
        finally:
            pythoncom.CoUninitialize()

    @staticmethod
    def _create_process_watcher():
        conn = wmi.WMI()
        raw_wql = (
            "SELECT * FROM __InstanceCreationEvent WITHIN 1 "
            "WHERE TargetInstance ISA 'Win32_Process'"
        )
        return conn.watch_for(raw_wql=raw_wql)

    def _handle_new_process(self, process):
        process_name = getattr(process, "Caption", "Unknown")
        process_path = getattr(process, "ExecutablePath", "Unknown")
        process_id = getattr(process, "ProcessId", None)

        with open(self.output_file, "a", encoding="utf-8") as file:
            file.write(f"Application Name: {process_name}\n")
            file.write(f"Application Source: {process_path}\n")
            file.write(f"PID: {process_id}\n\n")
            file.write(f"Additional Information\n{process}\n")
            file.write("-" * 100 + "\n")

        print(f"Application Launched: {process_name} (PID: {process_id})")

        if process_id is not None and self._is_blocked_process(process_name):
            self._terminate_process(process_id)

    def _terminate_existing_blocked_processes(self):
        if not self.blocked_processes:
            return

        pythoncom.CoInitialize()
        try:
            conn = wmi.WMI()
            for process in conn.Win32_Process():
                process_name = getattr(process, "Caption", "")
                process_id = getattr(process, "ProcessId", None)

                if process_id is None or not self._is_blocked_process(process_name):
                    continue

                print(
                    "Terminating existing blocked process: "
                    f"{process_name} (PID: {process_id})"
                )
                self._terminate_process(process_id)
        finally:
            pythoncom.CoUninitialize()

    def _is_blocked_process(self, process_name):
        return bool(process_name) and process_name.lower() in self.blocked_processes

    @staticmethod
    def _terminate_process(process_id):
        try:
            os.kill(process_id, signal.SIGTERM)
        except OSError as error:
            print(f"Error terminating process {process_id}: {error}")
