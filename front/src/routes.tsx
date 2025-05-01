import Dashboard from "views/rtl/default";
import CountersView from "views/counters";
import ProjectsView from "views/projects";
import UsersView from "./views/users";
import BillsView from "views/bills";
import OrdersView from "views/orders";
import SettingsView from "views/settings";
import VerificationView from "views/verification"
import SystemReportsView from "views/systemReports";
// Auth Imports
import SignIn from "views/auth/SignIn";
// Icon Imports
import {
  MdBarChart,
  MdDashboard,
  MdGasMeter,
  MdOutlineFeed,
  MdOutlineLogout,
  MdOutlineSettings,
  MdOutlineWifiTethering,
  MdPeopleAlt,
  MdReceiptLong,
  MdViewList,
  MdWarehouse,
  MdVerified,
} from "react-icons/md";
import ProjectDetailsView from "views/projectInformation";
import DeviceDetailsView from "views/deviceInformation";
import LogsView from "views/logs";
// import TestComponent from "views/testPage";
import Warehouse from "views/warehouse";
// import BillDetailsView from "views/billInformation";

const routes = [
  {
    name: "داشبورد",
    layout: "/admin",
    path: "dashboard",
    icon: <MdDashboard className="h-6 w-6" />,
    component: <Dashboard />,
    // role: "SuperAdmin",
    role: "Admin",
  },
  {
    name: "پروژه ها",
    layout: "/admin",
    path: "projects",
    icon: <MdViewList className="h-6 w-6" />,
    component: <ProjectsView />,
    role: "ProjectMenu",
  },
  {
    name: "مدیریت کاربران",
    layout: "/admin",
    path: "users",
    icon: <MdPeopleAlt className="h-6 w-6" />,
    component: <UsersView />,
    role: "UserMenu",
  },
  {
    name: "انبار",
    layout: "/admin",
    path: "warehouse",
    icon: <MdWarehouse className="h-6 w-6" />,
    component: <Warehouse />,
    role: "SuperAdmin",
  },
  {
    name: "کنتورها",
    layout: "/admin",
    path: "counters",
    icon: <MdGasMeter className="h-6 w-6" />,
    component: <CountersView />,
    role: "MeterMenu",
  },
  {
    name: "مدیریت قبوض",
    layout: "/admin",
    path: "bills",
    icon: <MdReceiptLong className="h-6 w-6" />,
    component: <BillsView />,
    role: "Bills",
  },
  {
    name: "گزارشات سیستم",
    layout: "/admin",
    path: "reports",
    icon: <MdBarChart className="h-6 w-6" />,
    component: <SystemReportsView />,
    role: "Reports",
  },
  {
    name: "لاگ سیستم",
    layout: "/admin",
    path: "logs",
    icon: <MdOutlineFeed className="h-6 w-6" />,
    component: <LogsView />,
    role: "LogDetail",
  },
  {
    name: "مدیریت دستورات",
    layout: "/admin",
    path: "orders",
    icon: <MdOutlineWifiTethering className="h-6 w-6" />,
    component: <OrdersView />,
    role: "SuperAdmin",
  },
  {
    name: "تنظیمات سیستم",
    layout: "/admin",
    path: "settings",
    icon: <MdOutlineSettings className="h-6 w-6" />,
    component: <SettingsView />,
    role: "SuperAdmin",
  },
  {
    name: "صحت سنجی",
    layout: "/admin",
    path: "verification",
    icon: <MdVerified className="h-6 w-6" />,
    component: <VerificationView />,
    role: "SuperAdmin",
  },

  {
    name: "خروج",
    layout: "/auth",
    path: "login",
    icon: <MdOutlineLogout className="h-6 w-6" />,
    component: <SignIn />,
    role: "Admin",
  },
  {
    name: "جزئیات پروژه",
    layout: "/admin",
    path: "projects/:projectId",
    icon: null,
    component: <ProjectDetailsView />,
    role: "Admin",
  },
  {
    name: "جزئیات دستگاه",
    layout: "/admin",
    path: "counters/:deviceSerial",
    icon: null,
    component: <DeviceDetailsView />,
    role: "Admin",
  },
  // {
  //   name: "تست کنتور",
  //   layout: "/admin",
  //   path: "test",
  //   icon: null,
  //   // icon: <MdGasMeter className="h-6 w-6" />,
  //   component: <TestComponent />,
  //   role: "Admin",
  // },
];
export default routes;
