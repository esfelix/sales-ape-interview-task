import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";

interface LoginCardProps {
  onConnectSpotify: () => void;
}

export function LoginCard({ onConnectSpotify }: LoginCardProps) {
  return (
    <div className="flex h-screen w-full items-center justify-center bg-gray-50">
      <Card className="w-[350px]">
        <CardHeader>
          <CardTitle>Welcome</CardTitle>
        </CardHeader>
        <CardContent />
        <CardFooter className="flex justify-between">
          <Button onClick={onConnectSpotify}>Connect with Spotify</Button>
        </CardFooter>
      </Card>
    </div>
  );
}
