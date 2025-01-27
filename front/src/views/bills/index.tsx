import Card from "components/card";
import CustomTabs from "components/tabs";
import CreateBillView from "./CreateBill";
import ShowBillView from "./ShowBills";
import { useQuery } from "@tanstack/react-query";
import { reqFunction } from "utils/API";
import ProjectSettings from "views/projectInformation/ProjectSettings";
// import ProjectSettings from "./ProjectSettings";
const BillsView = () => {
  const {
    data: projectsData,
    isLoading: projectsIsLoading,
    status: projectsStatus,
  } = useQuery({
    queryFn: () =>
      reqFunction("WaterMeterProjectsURL/admin/getAll", {
        page: 1,
        count: 100,
        water_meter_project_name: null,
        water_meter_project_create_date: null,
        user_id: null,
      }),
    queryKey: ["projectList"],
  });
  const {
    data: tagsData,
    isLoading: tagsIsLoading,
    status: tagsStatus,
  } = useQuery({
    queryFn: () =>
      reqFunction("WaterMeterTags/admin/getAll", {
        page: 1,
        count: 10,
        water_meter_tag_name: "",
        water_meter_type_create_date: "",
      }),
    queryKey: ["tagsList"],
  });
  const tabsData = [
    {
      label: "صدور قبض",
      content: (
        <CreateBillView projects={projectsData?.data} tags={tagsData?.data} />
      ),
    },
    {
      label: "مشاهده قبض",
      content: (
        <ShowBillView projects={projectsData?.data} tags={tagsData?.data} />
      ),
    },
    {
      label: "تنظیمات مصرف",
      content: <ProjectSettings />,
    },
  ];
  return (
    <div className=" ">
      <Card>
        {!projectsIsLoading &&
        projectsStatus === "success" &&
        !tagsIsLoading &&
        tagsStatus === "success" ? (
          <CustomTabs tabsData={tabsData} />
        ) : (
          <div>Essential Data is Loading </div>
        )}
      </Card>
    </div>
  );
};
export default BillsView;
