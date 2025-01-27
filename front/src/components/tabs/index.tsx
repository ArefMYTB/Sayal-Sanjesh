import { Tabs, TabList, TabPanels, Tab, TabPanel } from "@chakra-ui/react";
import { useState } from "react";
export type TabData = {
  label: string;
  labelIcon?: JSX.Element;
  content: JSX.Element;
};
interface TabsDataProps {
  tabsData: TabData[];
  index?: number;
}
const CustomTabs = (props: TabsDataProps) => {
  const { tabsData, index } = props;
  const [tabIndex, setTabIndex] = useState(index ? index : 0);
  return (
    <Tabs
      isFitted
      isLazy
      variant="soft-rounded"
      colorScheme="blue"
      className="p-4"
      index={tabIndex}
      onChange={(index) => setTabIndex(index)}
    >
      <TabList className="overflow-x-scroll border-b py-2">
        {tabsData.map((tab: TabData, index) => (
          <Tab className=" border-b-blue-400" key={index}>
            {tab.label}
          </Tab>
        ))}
      </TabList>
      <TabPanels className="custom-tab-panel !h-[400px]">
        {tabsData.map((tab: TabData, index) => (
          <TabPanel p={4} key={index}>
            {tab.content}
          </TabPanel>
        ))}
      </TabPanels>
    </Tabs>
  );
};
export default CustomTabs;
