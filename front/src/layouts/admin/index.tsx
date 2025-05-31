import { Navigate, Route, Routes, useLocation } from "react-router-dom";

import Navbar from "components/navbar/RTL";
import React, { useEffect, useState } from "react";
import Sidebar from "components/sidebar/RTL";
// import Footer from "components/footer/Footer";
import routes from "routes";

export default function RTL() {
  const location = useLocation();
  const [open, setOpen] = React.useState(true);
  const [currentRoute, setCurrentRoute] = React.useState("داشبورد");

  const [showChangePassAlert, setShowChangePassAlert] = useState(false);

  useEffect(() => {
    const ChangePass = JSON.parse(
      localStorage.getItem("ChangedPass") || "false"
    );
    if (ChangePass === false) {
      setShowChangePassAlert(true);
    }
  }, []);

  useEffect(() => {
    window.addEventListener("resize", () =>
      window.innerWidth < 1200 ? setOpen(false) : setOpen(true)
    );
  }, []);
  useEffect(() => {
    getActiveRoute(routes);
  }, [location.pathname]);

  const getActiveRoute = (routes: RoutesType[]): string | boolean => {
    let activeRoute = "RTL";
    for (let i = 0; i < routes.length; i++) {
      if (
        window.location.href.indexOf(
          routes[i].layout + "/" + routes[i].path
        ) !== -1
      ) {
        setCurrentRoute(routes[i].name);
      }
    }
    return activeRoute;
  };
  const getActiveNavbar = (routes: RoutesType[]): string | boolean => {
    let activeNavbar = false;
    for (let i = 0; i < routes.length; i++) {
      if (
        window.location.href.indexOf(routes[i].layout + routes[i].path) !== -1
      ) {
        return routes[i].secondary;
      }
    }
    return activeNavbar;
  };
  const getRoutes = (routes: RoutesType[]): any => {
    return routes.map((prop, key) => {
      if (prop.layout === "/admin") {
        return (
          <Route path={`/${prop.path}`} element={prop.component} key={key} />
        );
      } else {
        return null;
      }
    });
  };
  document.documentElement.dir = "rtl";
  return (
    <div className="flex h-full w-full">
      {showChangePassAlert && (
        <div className="bg-black fixed inset-0 z-[9999] flex items-start justify-center bg-opacity-50 pt-24">
          <div className="mx-4 w-full max-w-md rounded-xl bg-white p-6 shadow-2xl">
            <h2 className="mb-4 text-center text-xl font-semibold text-red-600">
              لطفا رمز خود را تغییر دهید.
            </h2>
            <div className="flex justify-center">
              <button
                onClick={() => setShowChangePassAlert(false)}
                className="rounded bg-blue-600 px-6 py-2 text-white hover:bg-blue-700"
              >
                باشه
              </button>
            </div>
          </div>
        </div>
      )}

      <Sidebar
        open={open}
        onClose={() => (open ? setOpen(false) : setOpen(true))}
      />
      {/* Navbar & Main Content */}
      <div
        className={`h-full min-h-screen w-full overflow-x-hidden bg-lightPrimary dark:!bg-navy-900 `}
      >
        {/* Main Content */}
        <main
          className={`mx-[12px] h-full flex-none transition-all md:pe-2 xl:${
            open ? "mr-0 lg:mr-[313px]" : "mr-0"
          }`}
        >
          {/* Routes */}
          <div className="h-full">
            <Navbar
              onOpenSidenav={() => (open ? setOpen(false) : setOpen(true))}
              brandText={currentRoute}
              secondary={getActiveNavbar(routes)}
            />
            <div className="pt-5s mx-auto mb-auto h-full min-h-[84vh] p-2 md:pr-2">
              <Routes>
                {getRoutes(routes)}
                <Route
                  path="/"
                  element={<Navigate to="/admin/dashboard" replace />}
                />
              </Routes>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
