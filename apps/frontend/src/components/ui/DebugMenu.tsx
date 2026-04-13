import toast from "react-hot-toast";
import { Modal, ModalBody, ModalTrigger } from "./animated-modals";
import { Button } from "./button";

const FocusFeatureDebugMenu = ({ debug }: { debug: () => void }) => {
  return (
    <div>
      <Modal>
        <ModalTrigger>
          <p className="border-2 p-2 rounded-md">🐞 Open modal</p>
        </ModalTrigger>
        <ModalBody>
          <p className="p-4 text-xl font-bold">Debug menu</p>
          <p className="ml-4">Timer</p>
          {/* debug the timer to skip to 3 seconds */}
          <Button
            className="ml-4 mt-4 w-48"
            onClick={() => {
              debug();
              // notify user that the timer has been set to 3 seconds
              toast.success("Set timer to 3 seconds");
            }}
          >
            Set timer to 3 sec
          </Button>
          {/* other feature  */}
          <div>
            <p className="pl-4 mt-4">Other features</p>

            {/* reset timer */}
            <Button
              className="ml-4 mt-4 w-48"
              onClick={() => {
                // do something
                console.log("Reset timer");
                // notify user that the timer has been reset
                toast.success("Reset timer");
              }}
            >
              Reset timer
            </Button>
          </div>
        </ModalBody>
      </Modal>
    </div>
  );
};

export default FocusFeatureDebugMenu;
