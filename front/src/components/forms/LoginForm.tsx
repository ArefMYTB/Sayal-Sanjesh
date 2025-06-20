import { useQueryClient } from "@tanstack/react-query";
import InputField from "components/fields/InputField";
import { useState, useEffect } from "react";
import { reqFunction } from "utils/API";
import { isPhoneValid, renderToast } from "utils/globalUtils";
interface LoginFormProps {
  phone: string;
  setPhone: React.Dispatch<any>;
  password: string;
  setPassword: React.Dispatch<any>;
}
const LoginForm = (props: LoginFormProps) => {
  const { phone, setPhone, password, setPassword } = props;
  const [lockoutTime, setLockoutTime] = useState<number | null>(null);

  const queryClient = useQueryClient();
  let adminPath = `/admin/dashboard`;
  let userPath = `/user/dashboard`;
  const [phoneBorder, setPhoneBorder] = useState<
    "err" | "success" | "dis" | "normal"
  >("normal");

  const userLogin = async () => {
    if (phone && password) {
      if (isPhoneValid(phone)) {
        const json = { admin_phone: phone, admin_password: password };
        let response = await reqFunction("admins/admin/login", json);

        if (response.code === 200) {
          renderToast("ورود مدیر با موفقیت انجام شد", "info");
          localStorage.setItem("token", JSON.stringify(response.data.token));
          localStorage.setItem(
            "permissions",
            JSON.stringify(response.data.permissions)
          );
          localStorage.setItem(
            "ChangedPass",
            JSON.stringify(response.data.ChangedPass)
          );
          // Save login history in localstorage if available
          if (response.data.last_successful_login) {
            const lastSuccess = new Date(
              response.data.last_successful_login
            ).toLocaleString("fa-IR");
            localStorage.setItem("lastSuccess", lastSuccess);
          }
          if (response.data?.last_failed_attempt) {
            const lastFail = new Date(
              response.data?.last_failed_attempt
            ).toLocaleString("fa-IR");
            localStorage.setItem("lastFail", lastFail);
          }

          queryClient.removeQueries();
          window.location.href = adminPath;
        } else {
          const resData = response?.data;
          if (resData?.locked_out) {
            console.log("Locked out");
            const seconds = resData?.lockout_seconds || 30;
            setLockoutTime(seconds);
            renderToast(
              `دسترسی مسدود شد. لطفاً ${seconds} ثانیه صبر کنید`,
              "err"
            );
          } else {
            renderToast(
              response?.farsi_message || "رمز یا شماره اشتباه است",
              "err"
            );
          }
        }
      } else {
        renderToast("شماره تماس 11 رقم بوده و با 0 شروع میگردد", "warn");
        setPhoneBorder("err");
      }
    } else {
      renderToast("تمامی موارد را وارد کنید", "warn");
    }
  };

  const endUserLogin = async () => {
    if (phone && password) {
      if (isPhoneValid(phone)) {
        const json: {
          user_phone: string;
          user_password: string;
        } = {
          user_phone: phone,
          user_password: password,
        };
        let response = await reqFunction("users/user/login", json);
        if (response.code === 200) {
          renderToast("ورود بهره بردار با موفقیت انجام شد", "info");
          // window.localStorage.setItem(
          //   "token",
          //   JSON.stringify(response.data.token)
          // );
          // window.localStorage.setItem(
          //   "permissions",
          //   JSON.stringify(response.data.permissions)
          // );
          // window.localStorage.setItem(
          //   "ChangedPass",
          //   JSON.stringify(response.data.ChangedPass)
          // );

          // queryClient.removeQueries();
          // window.location.href = userPath;
        } else {
          renderToast(response?.farsi_message, "err");
        }
      } else {
        renderToast("شماره تماس 11 رقم بوده و با 0 شروع میگردد", "warn");
        setPhoneBorder("err");
      }
    } else {
      renderToast("تمامی موارد را وارد کنید", "warn");
    }
  };

  useEffect(() => {
    if (lockoutTime && lockoutTime > 0) {
      const timer = setInterval(() => {
        setLockoutTime((prev) => (prev ? prev - 1 : null));
      }, 1000);
      return () => clearInterval(timer);
    }
  }, [lockoutTime]);

  return (
    <div className="mt-[10vh] w-full max-w-full flex-col items-center md:pl-4 lg:pl-0 xl:max-w-[420px]">
      <h4 className="mb-2.5 text-4xl font-bold text-navy-700 dark:text-white">
        ورود
      </h4>
      <p className="mb-9 ml-1 text-base text-gray-600">
        نام کاربری و رمز عبور را وارد کنید
      </p>
      <InputField
        id="admin-mobile"
        label="شماره موبایل"
        placeholder="شماره موبایل را وارد کنید"
        type="text"
        state={phone}
        setState={setPhone}
        border={phoneBorder}
      />

      {/* Password */}
      <InputField
        variant="auth"
        extra="mb-3"
        label="رمز عبور"
        placeholder="ترکیبی از عدد و حروف کوچک و بزرگ"
        id="password"
        type="password"
        state={password}
        setState={setPassword}
      />
      <div className="flex gap-2">
        <button
          onClick={userLogin}
          disabled={!!lockoutTime}
          className={`linear mt-2 w-full rounded-xl py-[12px] text-base font-medium transition duration-200
    ${
      lockoutTime
        ? "cursor-not-allowed bg-gray-400"
        : "bg-brand-500 text-white hover:bg-brand-600 active:bg-brand-700 dark:bg-brand-400 dark:text-white dark:hover:bg-brand-300 dark:active:bg-brand-200"
    }
  `}
        >
          {lockoutTime ? `صبر کنید (${lockoutTime} ثانیه)` : "ورود مدیر"}
        </button>

        {/* <button
          onClick={endUserLogin}
          className="linear mt-2 w-full rounded-xl bg-brand-500 py-[12px] text-base font-medium text-white transition duration-200 hover:bg-brand-600 active:bg-brand-700 dark:bg-brand-400 dark:text-white dark:hover:bg-brand-300 dark:active:bg-brand-200"
        >
          ورود بهره بردار
        </button> */}
      </div>
      <div className="mt-4">
        <span className=" text-sm font-medium text-navy-700 dark:text-gray-600">
          رمز خود را فراموش کرده اید؟
        </span>
        <a
          href=" "
          className="ml-1 text-sm font-medium text-brand-500 hover:text-brand-600 dark:text-white"
        >
          بازنشانی رمز عبور
        </a>
      </div>
    </div>
  );
};
export default LoginForm;
