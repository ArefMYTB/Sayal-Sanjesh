import Card from "components/card";
import CustomTabs, { TabData } from "components/tabs";
import SimpleCounterStorage from "./SimpleCounterStorage";
import ModuleStorage from "./ModuleStorage";
import SmartCounterStorage from "./SmartCounterStorage";

const Warehouse = () => {
  const tabsData: TabData[] = [
    { label: "کنتور مکانیکی", content: <SimpleCounterStorage /> },
    { label: "ماژول", content: <ModuleStorage /> },
    { label: "کنتور هوشمند", content: <SmartCounterStorage /> },
  ];
  return (
    <Card>
      <CustomTabs tabsData={tabsData} />
    </Card>
  );
};
export default Warehouse;
