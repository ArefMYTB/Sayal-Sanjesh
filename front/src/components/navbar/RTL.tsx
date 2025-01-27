import Dropdown from "components/dropdown";
import { FiAlignJustify } from "react-icons/fi";
import { useLocation, useNavigate } from "react-router-dom";
import { FiSearch } from "react-icons/fi";
import { RiMoonFill, RiSunFill } from "react-icons/ri";
import avatar from "assets/img/avatars/avatar4.png";
import { useContext, useEffect, useState } from "react";
import { reqFunction } from "utils/API";
import { useDisclosure } from "@chakra-ui/hooks";
import CustomModal from "components/modals";
import ProfileForm from "components/forms/ProfileForm";
import ChangePassForm from "components/forms/ChangePassForm";
import { renderToast } from "utils/globalUtils";
import { MdArrowCircleLeft } from "react-icons/md";
import { ThemeContext } from "ThemeProvider";

const Navbar = (props: {
  onOpenSidenav: () => void;
  brandText: string;
  secondary?: boolean | string;
}) => {
  let path = `/auth/login`;
  let navigate = useNavigate();
  let location = useLocation();
  const {
    onOpenSidenav,
    brandText,
    //  secondary
  } = props;
  const { isDark, setIsDark } = useContext(ThemeContext);
  // console.log(isDark);
  const [userName, setUsername] = useState<string>("");
  const [userLastName, setUserLastName] = useState<string>("");
  const [userPic, setUserPic] = useState<string>("");
  // const [userId, setUserId] = useState<string>("");
  const [userPhone, setUserPhone] = useState<string>("");

  const {
    isOpen: isProfileOpen,
    onOpen: onProfileOpen,
    onClose: onProfileClose,
  } = useDisclosure();
  const {
    isOpen: isPasswordOpen,
    onOpen: onPasswordOpen,
    onClose: onPasswordClose,
  } = useDisclosure();
  useEffect(() => {
    getProfile();
  }, []);
  const getProfile = async () => {
    let profileData = await reqFunction("admins/admin/getProfile", {});
    if (profileData.code === 200) {
      let profile = profileData.data[0];
      setUsername(profile.admin_name);
      setUserLastName(profile.admin_lastname);
      // setUserPassword(profile.admin_password);
      setUserPic(profile.admin_images[0]);
      // setUserId(profile.admin_id);
      setUserPhone(profile.admin_phone);
      window.localStorage.setItem(
        "permissions",
        JSON.stringify(profile.admin_permissions)
      );
    } else if (profileData.code !== 200) {
      renderToast(
        profileData?.farsi_message
          ? profileData.farsi_message
          : "در ورود خطایی رخ داده.دوباره تلاش کنید",
        "err"
      );
      navigate(path);
    }
  };
  const logOutFunc = async () => {
    let logout = await reqFunction("admins/admin/logout", {});
    if (logout.code === 200) {
      renderToast("خروج با موفقیت انجام شد", "success");
      navigate(path);
    } else {
    }
  };
  const renderNavigationLinks = () => {
    let pathArray = location.pathname.split("/");
    return (
      <>
        <div
          className="cursor-pointer text-sm font-normal text-navy-700 hover:underline dark:text-white dark:hover:text-white"
          // href="/"
          onClick={
            pathArray.length < 4
              ? null
              : () => {
                  pathArray[2] === "projects"
                    ? navigate("/admin/projects")
                    : pathArray[2] === "counters"
                    ? navigate("/admin/counters")
                    : navigate("/admin/bills");
                }
          }
        >
          {brandText === "داشبورد" ? "" : brandText}
          {pathArray.length < 4 ? (
            <></>
          ) : (
            <span className="mx-1 text-sm text-navy-700 hover:text-navy-700 dark:text-white">
              {" "}
              {"> "}
            </span>
          )}
        </div>
        {pathArray.length > 3 ? (
          <span className=" text-sm font-normal text-navy-700  dark:text-white dark:hover:text-white">
            {pathArray[2] === "projects"
              ? "جزئیات پروژه"
              : pathArray[2] === "counters"
              ? "جزئیات کنتور"
              : "جزئیات قبض"}
          </span>
        ) : (
          <></>
        )}
      </>
    );
  };
  return (
    <nav className="sticky top-0   z-[1000] flex flex-row flex-wrap items-center justify-between rounded-xl bg-white/10 p-2 backdrop-blur-xl dark:bg-[#0b14374d]">
      <CustomModal
        isOpen={isProfileOpen}
        onClose={onProfileClose}
        title={"پروفایل"}
        modalType="form"
        information={null}
        modalForm={
          <ProfileForm
            adminName={userName}
            setAdminName={setUsername}
            adminLastname={userLastName}
            setAdminLastname={setUserLastName}
            adminPhoneNumber={userPhone}
            update={getProfile}
            profilePreview={userPic}
            setProfilePreview={setUserPic}
            onClose={onProfileClose}
          />
        }
      />
      <CustomModal
        isOpen={isPasswordOpen}
        onClose={onPasswordClose}
        title={"تغییر رمز"}
        modalType="form"
        information={null}
        modalForm={
          <ChangePassForm onClose={onPasswordClose} update={getProfile} />
        }
      />
      <div className="ms-[6px]">
        <div className="flex h-6 w-[224px] items-center justify-start pt-1">
          <div
            className="cursor-pointer text-sm font-normal text-navy-700 hover:underline dark:text-white dark:hover:text-white"
            // href="/"
            onClick={() => navigate("/admin/dashboard")}
          >
            داشبورد{" "}
            <span className="mx-1 text-sm text-navy-700 hover:text-navy-700 dark:text-white">
              {" "}
              {"> "}
            </span>
          </div>
          {renderNavigationLinks()}
        </div>
      </div>

      <div className="relative mt-[3px] flex h-[61px] w-[355px] flex-grow items-center justify-around gap-2 rounded-full bg-white px-2 py-2 shadow-xl shadow-shadow-500 md:w-[365px] md:flex-grow-0 md:gap-1 xl:w-[365px] xl:gap-2 dark:!bg-navy-800 dark:shadow-none">
        {/* <div className="flex h-full items-center rounded-full bg-lightPrimary text-navy-700 xl:w-[225px] dark:bg-navy-900 dark:text-white">
          <p className="pe-2 ps-3 text-xl">
            <FiSearch className="h-4 w-4 text-gray-400 dark:text-white" />
          </p>
          <input
            type="text"
            placeholder="جستجو..."
            className="block h-full w-full rounded-full bg-lightPrimary text-sm font-medium text-navy-700 outline-none placeholder:!text-gray-400 sm:w-fit dark:bg-navy-900 dark:text-white dark:placeholder:!text-white"
          />
        </div> */}
        {/* Profile & Dropdown */}
        <Dropdown
          button={
            <img
              className="h-10 w-10 rounded-full"
              src={
                userPic
                  ? `${process.env.REACT_APP_SAYAL_API_ENDPOINT_MAIN}${userPic}`
                  : avatar
              }
              alt="admin_pic"
            />
          }
          children={
            <div className="flex h-48 w-56 flex-col justify-start rounded-[20px] bg-white bg-cover bg-no-repeat shadow-xl shadow-shadow-500 dark:!bg-navy-700 dark:text-white dark:shadow-none">
              <div className="ms-4 mt-3">
                <div className="flex items-center gap-2">
                  <p className="text-sm font-bold text-navy-700 dark:text-white">
                    {`👋 ${userName} ${userLastName}, خوش آمدی`}
                  </p>{" "}
                </div>
              </div>
              <div className="mt-3 h-px w-full bg-gray-200 dark:bg-white/20 " />

              <div className="my-3 ms-4 mt-3 flex flex-col">
                <div
                  onClick={onProfileOpen}
                  className="my-2 cursor-pointer text-sm text-gray-800 dark:text-white hover:dark:text-white"
                >
                  پروفایل کاربر{" "}
                </div>
                <div
                  onClick={onPasswordOpen}
                  className="my-2 mt-3 cursor-pointer text-sm text-gray-800 dark:text-white hover:dark:text-white"
                >
                  تغییر رمز عبور
                </div>
                <div
                  onClick={() => {
                    logOutFunc();
                  }}
                  className="mt-3 cursor-pointer text-sm font-medium text-red-500 hover:text-red-500"
                >
                  خروج
                </div>
              </div>
            </div>
          }
          classNames={"py-2 top-8 -start-[180px] w-max"}
        />
        <span
          className="flex cursor-pointer text-2xl text-gray-600  dark:text-white"
          onClick={onOpenSidenav}
        >
          <FiAlignJustify className="h-full w-full" />
        </span>

        <div
          className="cursor-pointer text-2xl text-gray-600"
          onClick={() => {
            if (isDark) {
              document.body.classList.remove("dark");
              // setDarkmode(false);
              setIsDark(false);
            } else {
              document.body.classList.add("dark");
              // setDarkmode(true);
              setIsDark(true);
            }
          }}
        >
          {isDark ? (
            <RiSunFill className="h-full w-full text-gray-600 dark:text-white" />
          ) : (
            <RiMoonFill className="h-full w-full text-gray-600 dark:text-white" />
          )}
        </div>
        <span
          className="flex cursor-pointer text-3xl text-gray-600  dark:text-white"
          onClick={() => navigate(-1)}
        >
          <MdArrowCircleLeft className="h-full w-full" />
        </span>
      </div>
    </nav>
  );
};

export default Navbar;
