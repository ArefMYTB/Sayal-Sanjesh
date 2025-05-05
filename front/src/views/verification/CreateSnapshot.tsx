import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { reqFunction } from "utils/API";
import SnapshotSelectFilter from "./SnapshotSelectFilter";
import SimpleTable from "components/tables/SimpleTable";
import { DynamicOption } from "components/fields/SelectInput";
import { DeviceObj } from "views/counters";
import { ProjectObject } from "views/projects";
import CustomButton from "components/button";
import SnapshotForm from "components/forms/SnapshotForm";
import CustomModal from "components/modals";
import { useDisclosure } from "@chakra-ui/hooks";
import moment from "moment-jalaali";

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

  // Form View
  const {
    isOpen: isSnapshotOpen,
    onOpen: onSnapshotOpen,
    onClose: onSnapshotClose,
  } = useDisclosure();

  const addSnapshotClick = () => {
    onSnapshotOpen();
  };

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

  // Find device
  const selectedDevice = projectDeviceData?.data?.find(
    (device: DeviceObj) =>
      device.water_meter_serial === counter?.value ||
      device.water_meter_serial === serialSearch
  );
  console.log(selectedDevice);

  // Fetch snapshot list
  const {
    data: snapshotData,
    isLoading: snapshotLoading,
    status: snapshotStatus,
    refetch: refetchSnapshots,
  } = useQuery({
    queryFn: () =>
      reqFunction("snapshots/admin/getAll", {
        page: 1,
        count: 100,
        user_id: null,
        water_meter_serial:
          serialSearch || selectedDevice?.water_meter_serial || null,
      }),
    queryKey: ["snapshots", serialSearch, counter?.value],
    enabled: !!serialSearch || !!counter?.value,
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
    // { title: "نام کنتور", headerKey: "counterName" },
    // { title: "شماره سریال", headerKey: "counterSerial" },
    // { title: "مالک کنتور", headerKey: "owner" },
    { title: "تاریخ", headerKey: "createDate" },
    { title: "زمان", headerKey: "createTime" },
    { title: "مقدار مکانیکی", headerKey: "mechanicValue" },
    { title: "مقدار تجمیعی", headerKey: "cumulativeValue" },
    { title: "توضیح", headerKey: "text" },
    { title: "برداشت کننده", headerKey: "admin" },
  ];

  const tableData = () => {
    let createSnapshotTableData: any[] = [];

    if (
      (snapshotStatus === "success" && snapshotData?.data && counter) ||
      (serialSearch && projectDeviceStatus === "success")
    ) {
      (snapshotData.data.snapshots || []).forEach((snapshot: any) => {
        createSnapshotTableData.push({
          createDate:
            moment(snapshot.create_time, "YYYY-M-D HH:mm:ss").format(
              "jYYYY/jM/jD"
            ) ?? "-",
          createTime:
            moment(snapshot.create_time, "YYYY-M-D HH:mm:ss").format(
              "HH:mm:ss"
            ) ?? "-",
          mechanicValue: snapshot.mechanic_value ?? "-",
          cumulativeValue: snapshot.cumulative_value ?? "-",
          text: snapshot.text ?? "-",
          admin: snapshot.admin ?? "-",
        });
      });
    }

    return createSnapshotTableData;
  };

  return (
    <div className="py-4">
      <CustomModal
        isOpen={isSnapshotOpen}
        onClose={onSnapshotClose}
        title={"برداشت"}
        modalType="form"
        modalForm={
          <SnapshotForm
            onClose={onSnapshotClose}
            serialnumber={
              serialSearch || selectedDevice?.water_meter_serial || null
            } // default
            refetchSnapshots={refetchSnapshots}
          />
        }
      />

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

      <div className="moldal-btns mt-4 flex items-center justify-end">
        <CustomButton
          text="افزودن برداشت"
          onClick={() => addSnapshotClick()}
          icon={<></>}
          color="green"
          extra="ml-0"
        />
      </div>

      <div className="mr-4 mt-1 space-y-1 py-2 font-bold text-navy-700 md:col-span-3 dark:text-white">
        <div>
          <span className="text-gray-500 dark:text-gray-300">نام پروژه: </span>
          <span>
            {selectedDevice?.water_meter_project__water_meter_project_name}
          </span>
        </div>
        <div>
          <span className="text-gray-500 dark:text-gray-300">نام دستگاه: </span>
          <span>{selectedDevice?.water_meter_name}</span>
        </div>
        <div>
          <span className="text-gray-500 dark:text-gray-300">
            سریال دستگاه:{" "}
          </span>
          <span>{serialSearch || selectedDevice?.water_meter_serial}</span>
        </div>
      </div>

      <div className="relative flex items-center justify-between p-4">
        <div className="py-2 text-xl font-bold text-navy-700 dark:text-white">
          {` برداشت ها ${
            counter && projectDeviceStatus === "success"
              ? `(${snapshotData?.data?.snapshots?.length || 0} عدد)`
              : ""
          }`}
        </div>
      </div>

      {(counter || serialSearch) &&
      !projectDeviceIsLoading &&
      projectDeviceStatus === "success" &&
      !snapshotLoading &&
      snapshotStatus === "success" ? (
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
        <div className="mr-4 py-2 text-navy-700 dark:text-white">
          دستگاه را انتخاب کنید !!!
        </div>
      )}
    </div>
  );
};

export default CreateSnapshotView;
