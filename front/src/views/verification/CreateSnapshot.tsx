import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { reqFunction } from "utils/API";
import SnapshotSelectFilter from "./SnapshotSelectFilter";
import SimpleTable from "components/tables/SimpleTable";
import { DynamicOption } from "components/fields/SelectInput";
import { DeviceObj } from "views/counters";
import { ProjectObject } from "views/projects";

type CreateSnapshotTableData = Array<{
  counterName: string;
  counterSerial: string;
  counterProject?: string;
  owner: string;
}>;

const CreateSnapshotView = () => {
  const [project, setProject] = useState<DynamicOption>(null);
  const [counter, setCounter] = useState<DynamicOption>(null);
  const [selectedCounters, setSelectedCounters] = useState<string[]>([]);
  const [serialSearch, setSerialSearch] = useState<string>("");


  // Fetch project list 
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

  // Fetch device list 
  const {
    data: projectDeviceData,
    isLoading: projectDeviceIsLoading,
    status: projectDeviceStatus,
  } = useQuery({
    queryFn: () =>
      reqFunction("watermeters/v2/admin/getAll", {
        page: 1,
        count: 100,
        user_id: null,
        project_id: project ? project.value : null,
        water_meter_serial: serialSearch || null,
      }),
    queryKey: ["projectDevice", project?.value, serialSearch],
    enabled: !!project || !!serialSearch?.trim(),
  });
  
  

  const renderProjectSelectData = () => {
    let selectData: DynamicOption[] = [];
    projectsData?.data?.forEach((project: ProjectObject) =>
      selectData.push({
        label: project.water_meter_project_name,
        value: project.water_meter_project_id,
      })
    );
    return selectData;
  };

  const renderCounterSelectData = () => {
    let selectData: DynamicOption[] = [];
    if (
      projectDeviceStatus === "success" &&
      projectDeviceData?.data?.length > 0
    ) {
      projectDeviceData.data.forEach((device: DeviceObj) => {
        selectData.push({
          label: device.water_meter_name,
          value: device.water_meter_serial,
        });
      });
    }
    return selectData;
  };

  // table data
  const createSnapshotTableHeader = [
    { title: "نام کنتور", headerKey: "counterName" },
    { title: "شماره سریال", headerKey: "counterSerial" },
    { title: "مالک کنتور", headerKey: "owner" },
  ];

  const tableData = () => {
    let createSnapshotTableData: CreateSnapshotTableData = [];
    if (!projectDeviceIsLoading && projectDeviceStatus === "success") {
      const devicesToDisplay = counter
        ? projectDeviceData.data.filter(
            (device: DeviceObj) => device.water_meter_serial === counter.value
          )
        : projectDeviceData.data;
  
      devicesToDisplay.forEach((device: DeviceObj) => {
        createSnapshotTableData.push({
          counterName: device.water_meter_name,
          counterSerial: device.water_meter_serial,
          owner: `${device.water_meter_user__user_name ?? "_"} ${
            device.water_meter_user__user_lastname ?? "_"
          }`,
        });
      });
    }
    return createSnapshotTableData;
  };
  

  return (
    <div className="py-4">
      <SnapshotSelectFilter
        filterPage="createSnapshot"
        projectSelect={renderProjectSelectData()}
        counterSelect={renderCounterSelectData()}
        project={project}
        setProject={setProject}
        counter={counter}
        setCounter={setCounter}
        serialSearch={serialSearch}
        setSerialSearch={setSerialSearch}
      />


      <div className="relative flex items-center justify-between p-4">
        <div className="py-2 text-xl font-bold text-navy-700 dark:text-white">
          {` دستگاه ها ${
            counter && projectDeviceStatus === "success" ? "(1 عدد)" : ""
          }`}
        </div>
      </div>

      {(counter || serialSearch) && !projectDeviceIsLoading && projectDeviceStatus === "success" ? (

        <SimpleTable
          header={createSnapshotTableHeader}
          data={tableData()}
          isCheckTable={true}
          selectedItems={selectedCounters}
          setSelectedItems={setSelectedCounters}
          hasIndex={true}
          extra="h-[53vh]"
        />
      ) : (
        <div className="py-2 text-navy-700 dark:text-white">
          پروژه و دستگاه را انتخاب کنید !!!
        </div>
      )}
    </div>
  );
};

export default CreateSnapshotView;
