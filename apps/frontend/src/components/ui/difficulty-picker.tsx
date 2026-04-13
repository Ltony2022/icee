import {
  DropdownMenu,
  DropdownMenuCheckboxItem,
  DropdownMenuContent,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Button } from "./button";

const DifficultyPicker = () => {
  return (
    <div>
      {" "}
      <div className="flex justify-center items-center">
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="outline">Select difficulty</Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent className="w-56">
            <DropdownMenuLabel>
              <p>Difficulty</p>
            </DropdownMenuLabel>
            <DropdownMenuSeparator />
            <DropdownMenuCheckboxItem checked={true}>
              Easy
            </DropdownMenuCheckboxItem>
            <DropdownMenuCheckboxItem disabled>
              Medium (Coming soon)
            </DropdownMenuCheckboxItem>
            <DropdownMenuCheckboxItem disabled>
              Hard (Coming soon)
            </DropdownMenuCheckboxItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>
    </div>
  );
};

export default DifficultyPicker;
