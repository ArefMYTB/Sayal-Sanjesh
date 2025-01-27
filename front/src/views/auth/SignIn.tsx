import LoginForm from "components/forms/LoginForm";
import { useState } from "react";
// import { FcGoogle } from "react-icons/fc";
// import Checkbox from "components/checkbox";

export default function SignIn() {
  window.localStorage.removeItem("token");
  window.localStorage.removeItem("permissions");
  window.localStorage.removeItem("userInfo");
  const [phone, setPhone] = useState<string>("");
  const [password, setPassword] = useState<string>("");

  return (
    <div className="mb-16 mt-16 flex h-full w-full items-center justify-center px-2 md:mx-0 md:px-0 lg:mb-10  lg:items-center lg:justify-start">
      {/* Sign in section */}
      <LoginForm
        phone={phone}
        setPhone={setPhone}
        password={password}
        setPassword={setPassword}
      />
    </div>
  );
}
