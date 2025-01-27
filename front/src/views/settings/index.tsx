import Card from "components/card";
import CustomTabs from "components/tabs";
import TagsTable from "./TagsTable";
import DeviceTypesTable from "./DeviceTypesTable";
import OrderTypesTable from "./OrderTypesTable";
import EventTypesTable from "./EventTypesTable";
import PermissionsCategory from "./PermissionsCategory";
import Permissions from "./Permissions";
import Moduletypes from "./ModuleTypesTable";
const SettingsView = () => {
  const tabsData = [
    { label: "دسته بندی", content: <TagsTable /> },
    { label: "نوع دستگاه", content: <DeviceTypesTable /> },
    { label: "نوع ماژول", content: <Moduletypes /> },
    { label: "نوع دستور", content: <OrderTypesTable /> },
    { label: "نوع رخداد", content: <EventTypesTable /> },
    { label: "دسترسی ها", content: <Permissions /> },
    { label: "نقش ها", content: <PermissionsCategory /> },
  ];
  return (
    <div className=" ">
      <Card>
        <CustomTabs tabsData={tabsData} />
      </Card>
    </div>
  );
};
export default SettingsView;
