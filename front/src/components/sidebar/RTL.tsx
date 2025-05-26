/* eslint-disable */

// import { HiX } from "react-icons/hi";
import Links from "./components/Links";
import SayalLogo from "../../assets/img/avatars/222.png";
// import SidebarCard from "components/sidebar/components/SidebarCard";
import routes from "routes";
import { HiX } from "react-icons/hi";

const Sidebar = (props: {
  open: boolean;
  onClose: React.MouseEventHandler<HTMLSpanElement>;
}) => {
  const permissions: string[] = JSON.parse(
    window.localStorage.getItem("permissions")
  );
  const decidePermission = () => {
    let r: RoutesType[] = [];
    routes.forEach((route: RoutesType) =>
      permissions.includes(route.role) ? r.push(route) : null
    );
    return r;
  };
  let decidedRoutes = permissions.includes("Admin")
    ? routes
    : decidePermission();
  const { open, onClose } = props;
  return (
    <div
      className={`sm:none duration-175 linear  fixed !z-top flex min-h-full min-w-[300px] flex-col bg-white pb-10 shadow-2xl shadow-white/5 transition-all   dark:!bg-navy-800 dark:text-white ${
        open ? "translate-x-0" : "translate-x-96"
      }`}
    >
      <span
        className="absolute end-4 top-4 block cursor-pointer xl:hidden"
        onClick={onClose}
      >
        <HiX />
      </span>
      <div className={`mx-[56px] mt-[50px] flex items-center`}>
        <div className="ms-1 mt-1 flex h-2.5 items-center justify-start font-poppins text-[26px] font-bold uppercase text-navy-700 dark:text-white">
          <img
            src={SayalLogo}
            className=" ml-4  h-10 w-10 rounded-full dark:bg-white"
          />
          <span>سیال سنجش</span>
        </div>
      </div>
      <div className="mb-3 mt-[38px] h-px bg-gray-300 dark:bg-white/30" />
      {/* Nav item */}

      <ul className="mb-auto pt-1">
        <Links routes={decidedRoutes} />
      </ul>

      {/* Free Horizon Card */}
      {/* <div className="flex justify-center">
        <SidebarCard />
      </div> */}

      {/* Nav item end */}
    </div>
  );
};

export default Sidebar;
