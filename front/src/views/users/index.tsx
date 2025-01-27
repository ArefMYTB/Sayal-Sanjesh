import UsersTable from "./UsersTable";
import AdminsTable from "./AdminsTable";
import Card from "components/card";
import CustomTabs from "components/tabs";
// import CustomMap from "components/map";
const UsersView = () => {
  const AdminPermissions: string[] = JSON.parse(
    window.localStorage.getItem("permissions")
  );
  const tabsData =
    AdminPermissions.includes("SuperAdmin") ||
    AdminPermissions.includes("CreateMiddleAdmin")
      ? [
          { label: "بهره بردار", content: <UsersTable /> },
          { label: "کاربر سیستم", content: <AdminsTable /> },
        ]
      : [{ label: "بهره بردار", content: <UsersTable /> }];
  return (
    <div className="">
      <Card>
        <CustomTabs tabsData={tabsData} />
      </Card>
    </div>
  );
};
export default UsersView;
