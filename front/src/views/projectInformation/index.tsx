import {
  useQuery,
  // , useQueryClient
} from "@tanstack/react-query";
import Card from "components/card";
import CustomTabs from "components/tabs";
import { useParams } from "react-router-dom";
import { reqFunction } from "utils/API";
import ProjectAbstract from "./ProjectAbstract";
import ProjectInformation from "./ProjectInformation";
import OtherDevices from "./OtherDevices";
import ProjectBuyers from "./ProjectBuyers";
import ProjectCounters from "./ProjectCounters";
import ProjectConsumptionChart from "./ProjectConsumptionChart";
import { DynamicOption } from "components/fields/SelectInput";

import {
  CountOption,
  countSelect,
  counterTagSelect,
  reversedSelect,
  sortValueSelect,
} from "variables";
import { useState } from "react";
import DeleteAllData from "./DeleteAllData";
// import MqttClient from "components/MQTT";

const ProjectDetailsView = () => {
  const { projectId } = useParams();
  const [tag, setTag] = useState<DynamicOption>(counterTagSelect[0]);
  const [sortValue, setSortValue] = useState<DynamicOption>(sortValueSelect[0]);
  const [reversed, setReversed] = useState<DynamicOption>(reversedSelect[0]);
  const [page, setPage] = useState<number>(1);
  const [count, setCount] = useState<CountOption>(countSelect[0]);
  // const queryClient = useQueryClient();
  // const queryKey = [{
  //   active: true,
  //   exact: true,
  //   stale: true,
  //   filters: [
  //     { queryKey: ["projectCounterConsumptionList"] },
  //     { queryKey: projectId },
  //     { queryKey: tag.value },
  //     { queryKey: sortValue.value },
  //     { queryKey: reversed.value },
  //   ],
  // }];

  // const handleRefetch = () => {
  //   queryClient.refetchQueries({
  //     queryKey: [
  //       "projectCounterConsumptionList",
  //       count,
  //       projectId,
  //       tag,
  //       sortValue,
  //       reversed,
  //     ],
  //     exact: true,
  //   });
  //   // //console.log("refetch function");
  // };
  const {
    data: projectData,
    isLoading: projectIsLoading,
    status: projectStatus,
    refetch: projectRefetch,
  } = useQuery({
    queryFn: () =>
      reqFunction("WaterMeterProjectsURL/admin/getOne", {
        water_meter_project_id: projectId,
      }),
    queryKey: ["projectDetail", projectId],
  });
  //project devices
  const {
    data: projectDeviceData,
    isLoading: projectDeviceIsLoading,
    status: projectDeviceStatus,
  } = useQuery({
    queryFn: () =>
      reqFunction("watermeters/v2/admin/getAll", {
        page: 1,
        count: 1000,
        user_id: null,
        project_id: projectId,
        water_meter_serial: null,
      }),
    queryKey: ["projectDevice", projectId],
  });
  const tabsData = [
    {
      label: "داشبورد",
      content: (
        <ProjectAbstract
          projectDevices={projectDeviceData?.data}
          projectData={projectData?.data}
          updateInfo={projectRefetch}
        />
      ),
    },
    {
      label: "نمودار مصرف",
      content: <ProjectConsumptionChart projectData={projectData?.data} />,
    },
    {
      label: "جزئیات",
      content: <ProjectInformation projectData={projectData?.data} />,
    },
    {
      label: "کنتورها",
      content: (
        <ProjectCounters
          projectId={projectId}
          projectDevices={projectDeviceData?.data}
          tag={tag}
          setTag={setTag}
          reversed={reversed}
          setReversed={setReversed}
          sortValue={sortValue}
          setSortValue={setSortValue}
          page={page}
          setPage={setPage}
          count={count}
          setCount={setCount}
        />
      ),
    },
    {
      label: "سایر دستگاه ها",
      content: <OtherDevices projectDevices={projectDeviceData?.data} />,
    },
    {
      label: "بهره برداران",
      content: <ProjectBuyers projectDevices={projectDeviceData?.data} />,
    },
  ];
  if (projectId === "1f0dba9e-1ecd-48a0-b0b4-fa880f7985f1") {
    tabsData.push({
      label: "پاک کردن",
      content: (
        <DeleteAllData
          projectId={projectId}
          projectDevices={projectDeviceData?.data}
        />
      ),
    });
  }

  return (
    <div className="">
      <Card extra="h-[88vh]">
        {!projectIsLoading &&
        projectStatus === "success" &&
        !projectDeviceIsLoading &&
        projectDeviceStatus === "success" ? (
          <>
            <CustomTabs tabsData={tabsData} />
            {/* <MqttClient projectId={projectId} update={handleRefetch} /> */}
          </>
        ) : (
          <div>essential page data loading</div>
        )}
      </Card>
    </div>
  );
};
export default ProjectDetailsView;
