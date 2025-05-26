import Card from "components/card";
import CustomTabs from "components/tabs";
import MqttLogs from "./MqttLogs";
import SystemLogs from "./SystemLogs";
const LogsView = () => {
  const AdminPermissions: string[] = JSON.parse(
    window.localStorage.getItem("permissions")
  );
  const tabsData = AdminPermissions.includes("LogSystem")
    ? [
        { label: "ارسال داده", content: <MqttLogs /> },
        { label: "تغییرات سیستم", content: <SystemLogs /> },
      ]
    : [{ label: "ارسال داده", content: <MqttLogs /> }];
  return (
    <div className="">
      <Card>
        <CustomTabs tabsData={tabsData} />
      </Card>
    </div>
  );
};
export default LogsView;
