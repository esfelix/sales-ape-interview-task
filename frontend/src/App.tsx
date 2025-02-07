import { useEffect, useState } from "react";
import { LoginCard } from "./components/LoginCard";
import { CustomChat } from "./components/CustomChat";

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    document.cookie =
      "session_id=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";

    (async () => {
      try {
        const res = await fetch("http://localhost:8000/auth/spotify/me", {
          credentials: "include",
        });
        if (res.ok) {
          const data = await res.json();
          if (data.logged_in) setIsLoggedIn(true);
        }
      } catch {}
    })();
  }, []);

  const handleConnectSpotify = () => {
    window.location.href = "http://localhost:8000/auth/spotify/connect";
  };

  return (
    <>
      {isLoggedIn ? (
        <CustomChat />
      ) : (
        <LoginCard onConnectSpotify={handleConnectSpotify} />
      )}
    </>
  );
}

export default App;
