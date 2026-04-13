import { atom } from "recoil";

const MINUTE = 60; // a minute = 60 seconds
const POMODORO = 25 * MINUTE; // a pomodoro = 25 minutes

interface FocusTimer {
    timer: number;
    round: number;
    mode: "pomodoro" | "break";
    isRunning: boolean;
}

const defaultFocusTimer: FocusTimer = {
  timer: POMODORO,
  round: 1,
  mode: "pomodoro",
  isRunning: false,
};

export const focusTimerAtom = atom<FocusTimer>({
  key: "focusTimer",
  default: defaultFocusTimer,
});