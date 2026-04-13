import { Card, CardContent, CardHeader } from "@/components/ui/card";
import type { colPage as colPageType } from "@/constant/homeModule.tsx";
import { colPage } from "@/constant/homeModule.tsx";
import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button.tsx";

export default function ListOfCards({ type = "default" }) {
  console.log("Type of data: " + type);
  return (
    <div className="p-12 flex items-center justify-between gap-2">
      {colPage.map((data: colPageType) => {
        return (
          <Card className="w-full h-full transition-all duration-300 hover:shadow-lg border border-amber-400/50 hover:border-amber-400 rounded-xl overflow-hidden hover:-translate-y-1">
            <CardHeader className="text-xl font-semibold text-gray-800">
              {data.title}
            </CardHeader>
            <CardContent className="text-gray-600 px-6">
              {data.content}
            </CardContent>
            <Button
              className="m-6 bg-amber-500 hover:bg-amber-600 text-white rounded-lg px-6 py-2 transition-colors duration-200"
              asChild
            >
              <Link to={data.link}>Explore</Link>
            </Button>
          </Card>
        );
      })}
    </div>
  );
}
