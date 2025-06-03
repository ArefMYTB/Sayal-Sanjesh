import { ProjectObject } from "views/projects";
import BillSelectFilter from "./BillSelectFilter";
import { DeviceObj, TagObject } from "views/counters";
import { DynamicOption } from "components/fields/SelectInput";
import { useState } from "react";
import { reqFunction } from "utils/API";
import { useQuery } from "@tanstack/react-query";
import SimpleTable from "components/tables/SimpleTable";
import CustomButton from "components/button";
import { useDisclosure } from "@chakra-ui/hooks";
import CustomModal from "components/modals";
// import { getToday } from "utils/TimeUtiles";
import CreateBillForm from "components/forms/CreateBillForm";
interface CreateBillProps {
  projects: ProjectObject[];
  tags: TagObject[];
}
type CreateBillTableData = Array<{
  counterName: string;
  counterSerial: string;
  counterProject?: string;
  owner: string;
}>;
const CreateBillView = (props: CreateBillProps) => {
  const { projects, tags } = props;
  const [project, setProject] = useState<DynamicOption>(null);
  const [tag, setTag] = useState<DynamicOption>(null);
  const [selectedCounters, setSelectedCounters] = useState<string[]>([]);
  const [payDescription, setPayDescription] = useState<string>("");
  const [billDescription, setBillDescription] = useState<string>("");
  const {
    data: projectDeviceData,
    isLoading: projectDeviceIsLoading,
    status: projectDeviceStatus,
    // refetch: projectDeviceRefetch,
  } = useQuery({
    queryFn: () =>
      reqFunction("watermeters/v2/admin/getAll", {
        page: 1,
        count: 100,
        user_id: null,
        project_id: project ? project.value : null,
        water_meter_serial: null,
      }),
    queryKey: ["projectDevice", project],
  });
  const {
    isOpen: createBillIsOpen,
    onOpen: onCreateBillOpen,
    onClose: onCreateBillClose,
  } = useDisclosure();
  const renderProjectSelectData = () => {
    let selectData: DynamicOption[] = [];
    projects && projects.length > 0
      ? projects.forEach((project) =>
          selectData.push({
            label: project.water_meter_project_name,
            value: project.water_meter_project_id,
          })
        )
      : (selectData = []);
    return selectData;
  };
  const renderTagSelectData = () => {
    let selectData: DynamicOption[] = [];
    tags?.length > 0
      ? tags?.forEach((tag) =>
          selectData.push({
            label: tag.water_meter_tag_name,
            value: tag.water_meter_tag_id,
          })
        )
      : (selectData = []);
    return selectData;
  };
  const createBillTableHeader = [
    { title: "نام کنتور", headerKey: "counterName" },
    { title: "شماره سریال", headerKey: "counterSerial" },
    // { title: "ثبت آخرین مصرف در", headerKey: "lstCunsTime" },
    { title: "مالک کنتور", headerKey: "owner" },
  ];
  const tableData = () => {
    let createBillTableData: CreateBillTableData = [];
    if (!projectDeviceIsLoading && projectDeviceStatus === "success") {
      let filteredTag = projectDeviceData?.data?.filter(
        (device: DeviceObj) =>
          device.water_meter_type__water_meter_tag__water_meter_tag_id ===
          tag.value
      );
      filteredTag?.forEach((device: DeviceObj) => {
        createBillTableData.push({
          counterName: device.water_meter_name,
          counterSerial: device.water_meter_serial,
          //  counterProject: device.water_meter_project__water_meter_project_name,
          owner: `${device.water_meter_user__user_name ?? "_"} ${
            device.water_meter_user__user_lastname ?? "_"
          }`,
        });
      });
    }
    return createBillTableData;
  };
  return (
    <div className="py-4">
      <CustomModal
        isOpen={createBillIsOpen}
        onClose={onCreateBillClose}
        title={"صدور قبض"}
        modalType="form"
        information={null}
        modalForm={
          <CreateBillForm
            project={project}
            tag={tag}
            payDescription={payDescription}
            setPayDescription={setPayDescription}
            billDescription={billDescription}
            setBillDescription={setBillDescription}
            selectedDevices={selectedCounters}
            onClose={onCreateBillClose}
          />
        }
      />
      <BillSelectFilter
        filterPage="createBill"
        projectSelect={renderProjectSelectData()}
        tagSelect={renderTagSelectData()}
        project={project}
        setProject={setProject}
        tag={tag}
        setTag={setTag}
      />
      <div className="relative flex items-center justify-between p-4">
        <div className="py-2 text-xl font-bold text-navy-700 dark:text-white">
          {` دستگاه ها ${
            tag && !projectDeviceIsLoading && projectDeviceStatus === "success"
              ? `(${
                  projectDeviceData?.data?.filter(
                    (device: DeviceObj) =>
                      device.water_meter_type__water_meter_tag__water_meter_tag_id ===
                      tag.value
                  ).length
                } عدد)`
              : ""
          }`}
        </div>
        <div className=" moldal-btns flex items-center justify-end">
          <CustomButton
            isDisabled={selectedCounters.length > 0 ? false : true}
            text="صدور قبض"
            onClick={onCreateBillOpen}
            color="green"
          />
        </div>
      </div>
      {tag && !projectDeviceIsLoading && projectDeviceStatus === "success" ? (
        <SimpleTable
          header={createBillTableHeader}
          data={tableData()}
          isCheckTable={true}
          selectedItems={selectedCounters}
          setSelectedItems={setSelectedCounters}
          hasIndex={true}
          extra="h-[53vh]"
        />
      ) : (
        <div className="py-2  text-navy-700  dark:text-white">
          دسته بندی را انتخاب کنید !!!
        </div>
      )}
    </div>
  );
};
export default CreateBillView;
