import { Button } from "@/components/ui/button";
import { useNavigate } from "react-router-dom";

const NotFound = () => {
  // use navigate to redirect to home page
  const changeToPage = useNavigate();

  return (
    <div>
      <h1 className="text-3xl font-bold">404 Not Found</h1>
      <p className="text-gray-400">
        The page you are looking for does not exist.
      </p>
      <Button
        onClick={() => {
          changeToPage("/");
        }}
        className="mt-4"
      >
        Go to Homepage
      </Button>
    </div>
  );
};

export default NotFound;
