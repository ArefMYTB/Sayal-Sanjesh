import Card from "components/card";
import { MdEdit, MdRemoveRedEye } from "react-icons/md";
import { useDisclosure } from "@chakra-ui/hooks";

import CustomModal from "components/modals";
import CustomButton from "components/button";
import { useQuery } from "@tanstack/react-query";
import { reqFunction } from "utils/API";
import SimpleTable from "components/tables/SimpleTable";
import { DynamicOption } from "components/fields/SelectInput";
import { useState } from "react";
import DeviceForm from "components/forms/DeviceForm";
import {
  CountOption,
  countSelect,
  deviceOrderModesSelectData,
} from "variables";
import CustomPagination from "components/pagination";
import { Link } from "react-router-dom";

export type DeviceObj = {
  water_meter_name: string;
  water_meter_user__user_name: string;
  water_meter_user__user_lastname: string;
  water_meter_user__user_id: string;
  water_meter_user__user_phone: string;
  water_meter_project__water_meter_project_name: string | null;
  water_meter_module__water_meter_module_id: string | null;
  water_meter_project__water_meter_project_id: string | null;
  water_meter_serial: string;
  water_meter_location: string | { lat: number; lng: number } | null;
  water_meter_module__water_meter_module_code: string | null;
  water_meter_module__water_meter_module_name: string | null;
  water_meter_type__water_meter_tag__water_meter_tag_id: string;
  water_meter_type__water_meter_tag__water_meter_tag_name: string;
  water_meter_model: string;
  water_meter_size: number;
  water_meter_type__water_meter_type_name: string;
  water_meter_type__water_meter_type_id: string;
  water_meter_validation: number;
  water_meter_manual_number: null | number;
  water_meter_order_mode: null | "" | "R" | "P";
  water_meter_activation: null | number;
  water_meter_condition: null | number;
  all_water_meters: number;
  water_meter_module__module_type__module_type_name: string;
  water_meter_module__water_meter_module_property: string[];
  other_information: { manufacturere?: string };
};
export type TagObject = {
  water_meter_tag_id: string;
  water_meter_tag_name: string;
  water_meter_tag_create_date: Date;
  meter_number_per_tag: number;
};
type DeviceTableData = Array<{
  deviceName: JSX.Element;
  deviceSerial: string;
  deviceProject: string;
  deviceValidation: JSX.Element;
  deviceActivation: JSX.Element;
  deviceTag: JSX.Element;
  deviceType: string;
  deviceOwner: string;
  deviceModuleName: string;
  deviceActions: JSX.Element;
}>;
const CountersView = () => {
  const AdminPermissions: string[] = JSON.parse(
    window.localStorage.getItem("permissions")
  );
  const [deviceName, setDeviceName] = useState<string>("");
  const [deviceSerial, setDeviceSerial] = useState<string>("");
  const [deviceType, setDeviceType] = useState<DynamicOption>(null);
  const [deviceUser, setDeviceUser] = useState<DynamicOption>(null);
  const [deviceProject, setDeviceProject] = useState<DynamicOption>(null);
  const [deviceModule, setDeviceModule] = useState<DynamicOption>(null);
  const [deviceOrderMode, setDeviceOrderMode] = useState<DynamicOption>(null);
  const [deviceManualNumber, setDeviceManualNumber] = useState<number>(0);
  const [selectedCounter, setSelectedCounter] = useState<DeviceObj>(null);
  const [isEditForm, setIsEditForm] = useState<boolean>(false);
  const [page, setPage] = useState<number>(1);
  const [count, setCount] = useState<CountOption>(countSelect[0]);
  const {
    data: devicesData,
    isLoading: devicesIsLoading,
    status: devicesStatus,
    refetch: deviceRefetch,
  } = useQuery({
    queryFn: () =>
      reqFunction("watermeters/v2/admin/getAll", {
        page: page,
        count: count.value,
        has_module: null,
        user_id: null,
        project_id: null,
        water_meter_serial: null,
        has_user: null,
      }),
    queryKey: ["deviceList", page, count],
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
  const {
    data: typesData,
    isLoading: typesIsLoading,
    status: typesStatus,
  } = useQuery({
    queryFn: () =>
      reqFunction("WaterMeterTypes/admin/getAll", {
        page: 1,
        count: 10,
        water_meter_type_name: "",
        water_meter_type_create_date: "",
      }),
    queryKey: ["typesList"],
  });
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
    data: modulesData,
    isLoading: modulesIsLoading,
    status: modulesStatus,
  } = useQuery({
    queryFn: () =>
      reqFunction("WaterMeterModules/admin/getAll", {
        page: 1,
        count: 100,
        water_meter_module_name: "",
        water_meter_module_create_date: "",
      }),
    queryKey: ["modulesList"],
  });
  const {
    data: usersData,
    isLoading: usersIsLoading,
    status: usersStatus,
  } = useQuery({
    queryFn: () =>
      reqFunction("users/admin/getAllUsers", {
        page: 1,
        count: 100,
        user_name: "",
        user_lastname: "",
        user_phone: "",
      }),
    queryKey: ["usersList"],
  });
  const {
    isOpen: isDeviceOpen,
    onOpen: onDeviceOpen,
    onClose: onDeviceClose,
  } = useDisclosure();
  const devicesTableHeader =
    AdminPermissions.includes("MeterEdit") ||
    AdminPermissions.includes("MeterDelete") ||
    AdminPermissions.includes("MeterDetail")
      ? [
          { title: "نام دستگاه", headerKey: "deviceName" },
          { title: "سریال دستگاه", headerKey: "deviceSerial" },
          { title: "نام پروژه", headerKey: "deviceProject" },
          { title: "دسته بندی", headerKey: "deviceTag" },
          { title: "نوع دستگاه", headerKey: "deviceType" },
          { title: "وضعیت تایید(ماژول)", headerKey: "deviceValidation" },
          { title: "فعال سازی(کاربر)", headerKey: "deviceActivation" },
          { title: "بهره بردار", headerKey: "deviceOwner" },
          { title: "ماژول دستگاه", headerKey: "deviceModuleName" },
          { title: "عملیات", headerKey: "deviceActions" },
        ]
      : [
          { title: "نام دستگاه", headerKey: "deviceName" },
          { title: "سریال دستگاه", headerKey: "deviceSerial" },
          { title: "نام پروژه", headerKey: "deviceProject" },
          { title: "دسته بندی", headerKey: "deviceTag" },
          { title: "نوع دستگاه", headerKey: "deviceType" },
          { title: "وضعیت تایید(ماژول)", headerKey: "deviceValidation" },
          { title: "فعال سازی(کاربر)", headerKey: "deviceActivation" },
          { title: "بهره بردار", headerKey: "deviceOwner" },
          { title: "ماژول دستگاه", headerKey: "deviceModuleName" },
        ];
  const renderTags = (renderType: "select" | "show", tagId: string) => {
    if (!tagsIsLoading && tagsStatus !== "pending") {
      const renderTag = (id: string) => {
        let tag: TagObject = tagsData.data.filter(
          (tags: TagObject) => tags.water_meter_tag_id === id
        )[0];
        return tag.water_meter_tag_name;
      };
      switch (renderType) {
        case "show":
          return (
            <span
              className={`${
                renderTag(tagId) === "آب"
                  ? " bg-blue-500"
                  : renderTag(tagId) === "برق"
                  ? " bg-red-500"
                  : renderTag(tagId) === "گاز"
                  ? "bg-orange-500"
                  : " bg-yellow-600"
              } rounded px-2 text-sm text-white`}
            >
              {renderTag(tagId)}
            </span>
          );
        case "select":
          return;
        default:
          return <span>__</span>;
      }
    }
  };

  const renderModulesSelectData = () => {
    let selectedData: DynamicOption[] = [];
    if (!modulesIsLoading && modulesStatus !== "pending") {
      modulesData.data?.forEach(
        (module: {
          water_meter_module_name: string;
          water_meter_module_id: string;
        }) => {
          selectedData.push({
            label: module.water_meter_module_name,
            value: module.water_meter_module_id,
          });
        }
      );
    }

    return selectedData;
  };
  const renderTypesSelectData = () => {
    let selectedData: DynamicOption[] = [];
    if (!typesIsLoading && typesStatus !== "pending") {
      typesData.data.forEach(
        (type: {
          water_meter_type_name: string;
          water_meter_type_id: string;
        }) => {
          selectedData.push({
            label: type.water_meter_type_name,
            value: type.water_meter_type_id,
          });
        }
      );
    }

    return selectedData;
  };
  const renderProjectSelectData = () => {
    let selectedData: DynamicOption[] = [];
    if (!projectsIsLoading && projectsStatus !== "pending") {
      projectsData.data.forEach(
        (project: {
          water_meter_project_name: string;
          water_meter_project_id: string;
        }) => {
          selectedData.push({
            label: project.water_meter_project_name,
            value: project.water_meter_project_id,
          });
        }
      );
    }

    return selectedData;
  };
  const renderUserSelectData = () => {
    let selectedData: DynamicOption[] = [];
    if (!usersIsLoading && usersStatus !== "pending" && usersData?.data) {
      usersData.data.forEach(
        (user: {
          user_name: string;
          user_lastname: string;
          user_id: string;
        }) => {
          selectedData.push({
            label: `${user.user_name} ${user.user_lastname}`,
            value: user.user_id,
          });
        }
      );
    }

    return selectedData;
  };
  // const openAddModal = () => {
  //   renderModulesSelectData();
  //   renderTypesSelectData();
  //   renderProjectSelectData();
  //   renderUserSelectData();
  //   setIsEditForm(false);
  //   onDeviceOpen();
  // };
  const editDeviceClick = (serial: string) => {
    //  const [deviceManualNumber, setDeviceManualNumber] = useState<number>(0);
    let selectedDevice: DeviceObj = devicesData.data.filter(
      (device: DeviceObj) => device.water_meter_serial === serial
    )[0];
    setSelectedCounter(selectedDevice);
    let types = renderTypesSelectData();
    let users = renderUserSelectData();
    let projects = renderProjectSelectData();
    let modules = renderModulesSelectData();
    setIsEditForm(true);
    setDeviceName(selectedDevice.water_meter_name);
    setDeviceSerial(selectedDevice.water_meter_serial);
    setDeviceType(
      types.filter(
        (type: DynamicOption) =>
          type.label === selectedDevice.water_meter_type__water_meter_type_name
      )[0] ?? null
    );
    setDeviceUser(
      users.filter(
        (user: DynamicOption) =>
          user.value === selectedDevice.water_meter_user__user_id
      )[0] ?? null
    );
    setDeviceProject(
      projects.filter(
        (project: DynamicOption) =>
          project.label ===
          selectedDevice.water_meter_project__water_meter_project_name
      )[0]
    );
    setDeviceModule(
      modules.filter(
        (module: DynamicOption) =>
          module.label ===
          selectedDevice.water_meter_module__water_meter_module_name
      )[0] ?? null
    );
    setDeviceOrderMode(
      selectedDevice.water_meter_order_mode
        ? deviceOrderModesSelectData.filter(
            (data: DynamicOption) =>
              data.value === selectedDevice.water_meter_order_mode
          )[0]
        : null
    );
    setDeviceManualNumber(selectedDevice.water_meter_manual_number);
    onDeviceOpen();
  };
  const renderDeviceName = (name: string, serial: string) => {
    return (
      <>
        {AdminPermissions.includes("MeterDetail") ? (
          <Link to={`/admin/counters/${serial}`} rel="noopener noreferrer">
            <span>{name}</span>
          </Link>
        ) : (
          <span>{name}</span>
        )}
      </>
    );
  };
  const renderDeviceActions = (deviceSerial: string) => {
    return (
      <div className=" flex items-center justify-center">
        {AdminPermissions.includes("MeterDetail") ? (
          <Link
            to={`/admin/counters/${deviceSerial}`}
            rel="noopener noreferrer"
          >
            <CustomButton
              // onClick={() => routeChange(counterSerial)}
              onClick={null}
              icon={<MdRemoveRedEye />}
              color="blue"
              extra="!p-2 "
            />
          </Link>
        ) : (
          <></>
        )}
        {AdminPermissions.includes("MeterEdit") ? (
          <CustomButton
            onClick={() => editDeviceClick(deviceSerial)}
            icon={<MdEdit />}
            color="orange"
            extra="!p-2"
          />
        ) : (
          <></>
        )}
        {/* {AdminPermissions.includes("MeterDelete") ? (
          <CustomButton
            onClick={() => deleteCounter(deviceSerial)}
            icon={<MdDelete />}
            color="red"
            extra="!p-2"
          />
        ) : (
          <></>
        )} */}
      </div>
    );
  };
  const tableData = () => {
    let deviceTableData: DeviceTableData = [];
    if (!devicesIsLoading && devicesStatus !== "pending") {
      devicesData.data.forEach((device: DeviceObj) => {
        deviceTableData.push({
          deviceName: renderDeviceName(
            device.water_meter_name,
            device.water_meter_serial
          ),
          deviceSerial: device.water_meter_serial,
          deviceProject: device.water_meter_project__water_meter_project_name,
          deviceValidation:
            device.water_meter_validation === 1 ? (
              <span className=" rounded bg-green-600 px-1 text-sm text-white">
                تایید شده
              </span>
            ) : (
              <span className=" rounded bg-red-600 px-1 text-sm text-white">
                تایید نشده
              </span>
            ),
          deviceActivation:
            device.water_meter_activation === 1 ? (
              <span className=" rounded bg-green-600 px-1 text-sm text-white">
                فعال شده
              </span>
            ) : device.water_meter_activation === 0 ? (
              <span className=" rounded bg-red-600 px-1 text-sm text-white">
                فعال نشده
              </span>
            ) : (
              <span className=" rounded bg-red-600 px-1 text-sm text-white">
                فعال نشده
              </span>
            ),
          deviceTag: renderTags(
            "show",
            device.water_meter_type__water_meter_tag__water_meter_tag_id
          ),
          deviceType: device.water_meter_type__water_meter_type_name,
          deviceOwner: `${device.water_meter_user__user_name ?? "_"} ${
            device.water_meter_user__user_lastname ?? "_"
          }`,
          deviceModuleName:
            device.water_meter_module__water_meter_module_name ?? "__",
          deviceActions: renderDeviceActions(device.water_meter_serial),
        });
      });
    }
    return deviceTableData;
  };
  return (
    <div className="">
      <CustomModal
        isOpen={isDeviceOpen}
        onClose={onDeviceClose}
        title={"کنتور"}
        modalType="form"
        information={null}
        modalForm={
          <DeviceForm
            deviceName={deviceName}
            setDeviceName={setDeviceName}
            deviceSerial={deviceSerial}
            setDeviceSerial={setDeviceSerial}
            deviceType={deviceType}
            setDeviceType={setDeviceType}
            deviceModule={deviceModule}
            setDeviceModule={setDeviceModule}
            deviceProject={deviceProject}
            setDeviceProject={setDeviceProject}
            deviceUser={deviceUser}
            setDeviceUser={setDeviceUser}
            deviceManualNumber={deviceManualNumber}
            setDeviceManualNumber={setDeviceManualNumber}
            deviceOrderMode={deviceOrderMode}
            setDeviceOrderMode={setDeviceOrderMode}
            deviceModuleOptions={renderModulesSelectData()}
            deviceProjectOptions={renderProjectSelectData()}
            deviceTypesOptions={renderTypesSelectData()}
            deviceUserOptions={renderUserSelectData()}
            isEditForm={isEditForm}
            setEditForm={setIsEditForm}
            onClose={onDeviceClose}
            updateTable={deviceRefetch}
            selectedDevice={selectedCounter}
          />
        }
      />
      <Card extra="h-[80vh]">
        <div className="relative flex items-center justify-between p-4">
          <div className="text-xl font-bold text-navy-700 dark:text-white">
            {`دستگاه ها (${
              devicesIsLoading
                ? "loading..."
                : devicesData?.data[0]?.all_water_meters
                ? devicesData?.data[0]?.all_water_meters
                : 0
            })`}
          </div>
          {/* <div className=" moldal-btns flex items-center justify-end">
            {AdminPermissions.includes("MeterCreate") ? (
              <CustomButton
                text="افزودن کنتور"
                onClick={() => {
                  openAddModal();
                }}
                icon={<MdAdd />}
                color="green"
              />
            ) : (
              <></>
            )}
          </div> */}
        </div>
        <div className="table-container mx-auto  w-full ">
          <SimpleTable
            header={devicesTableHeader}
            data={tableData()}
            hasIndex={true}
            extra="h-[55vh]"
            page={page}
            count={count.value}
          />
        </div>
        <div className="pagination ">
          <CustomPagination
            page={page}
            pageSize={count}
            totalData={
              devicesData?.data.length > 0
                ? devicesData.data[0].all_water_meters
                : 0
            }
            changePageFunc={setPage}
            changeCount={setCount}
          />
        </div>
      </Card>
    </div>
  );
};
export default CountersView;
