import Card from "components/card";
import CustomTabs from "components/tabs";
import ProjectsReport from "./ProjecsReport";
import DeviceTypesReport from "./DeviceTypesReport";
import DevicesReport from "./DeviceReports";
import ConsumptionReport from "./ConsumptionReports";
import ConsumptionComparison from "./ConsumptionComparison";
const SystemReportsView = () => {
  const tabsData = [
    { label: "پروژه ها", content: <ProjectsReport /> },
    { label: "نوع دستگاه", content: <DeviceTypesReport /> },
    { label: "دستگاه ها", content: <DevicesReport /> },
    { label: "مصرف", content: <ConsumptionReport /> },
    { label: "مقایسه مصرف", content: <ConsumptionComparison /> },
  ];
  return (
    <div className=" ">
      <Card extra="!h-[95vh]">
        <CustomTabs tabsData={tabsData} />
      </Card>
    </div>
  );
};
export default SystemReportsView;
