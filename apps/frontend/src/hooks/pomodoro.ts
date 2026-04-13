import { focusTimerAtom } from "@/atoms/focusTimer";
import { useCallback, useEffect, useRef } from "react";
import toast from "react-hot-toast";
import { useRecoilState } from "recoil";

const usePomodoro = () => {
  // some default values
  const MINUTE = 60; // a minute = 60 seconds
  const POMODORO = 25 * MINUTE; // a pomodoro = 25 minutes
  const SHORT_BREAK = 5 * MINUTE; // a short break = 5 minutes
  const LONG_BREAK = 15 * MINUTE; // a long break = 15 minutes

  // let's have a state that tracks the timer
  const [focusTimer, setFocusTimer] = useRecoilState(focusTimerAtom);

  // state related to pomodoro
  // TODO: navigate to recoil
  // const [isRunning, setIsRunning] = useState(false);  
  // const [timer, setTimer] = useState(POMODORO);
  // const [round, setRound] = useState(1);
  // const [mode, setMode] = useState("pomodoro");

  // a variable that tracks the time of the current mode
  const currentModeTime =
    focusTimer.mode === "pomodoro"
      ? POMODORO
      : focusTimer.round % 4 === 0
        ? LONG_BREAK
        : SHORT_BREAK;

  // function that play complete sound
  const playCompleteSound = () => {
    const audio = new Audio("/sounds/pomodoroComplete.wav");
    audio.play();
  }

  const intervalRef = useRef<NodeJS.Timeout | null>(null);

  const handleModeSwitch = useCallback(() => {
    setFocusTimer((prevState) => {
      let newRound = prevState.round;
      const newFocusTimer = { ...prevState }; // Create a new state object

      if (prevState.mode === "break") {
        newRound += 1;
        newFocusTimer.mode = "pomodoro";
        newFocusTimer.timer = POMODORO;
        newFocusTimer.isRunning = false; // Pause the timer
        if (intervalRef.current) {
          clearInterval(intervalRef.current);
        }

        // display the notification bubble
        toast("Break complete! You can now start a new pomodoro.");
      } else if (prevState.mode === "pomodoro") {
        newFocusTimer.mode = "break";
        newFocusTimer.timer = newRound % 4 === 0 ? LONG_BREAK : SHORT_BREAK;
      }

      return { ...newFocusTimer, round: newRound }; // Return the new state
    });
  }, [LONG_BREAK, POMODORO, SHORT_BREAK, setFocusTimer]);

  // useEffect to track the change of variables and start/stop the timer
  useEffect(() => {
    if (focusTimer.isRunning && focusTimer.timer > 0) {
      intervalRef.current = setInterval(() => {
        setFocusTimer((prevState) => ({
          ...prevState,
          timer: prevState.timer - 1,
        }));
      }, 1000);
    } else if (focusTimer.timer === 0) {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
      playCompleteSound(); // play the sound

      // display the notification bubble
      toast("Pomodoro complete! You can now take a break.");
      handleModeSwitch();
    }

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, [focusTimer.isRunning, focusTimer.timer, handleModeSwitch, setFocusTimer]);

  // if user leaves the page, still running the timer

  const stopTimer = () => {
    setFocusTimer((prevState) => ({
      ...prevState,
      isRunning: false,
    }));
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
    }
  };

  // debug function that set timer to 3 seconds
  function debug() {
    setFocusTimer((prevState) => ({
      ...prevState,
      timer: 3,
    }));
  }

  return {
    countdown: () => setFocusTimer((prevState) => ({
      ...prevState,
      isRunning: true,
    })),
    stopTimer,
    timer: focusTimer.timer,
    round: focusTimer.round,
    isRunning: focusTimer.isRunning,
    debug,
    currentModeTime,
    mode: focusTimer.mode,
  };
};

export default usePomodoro;
