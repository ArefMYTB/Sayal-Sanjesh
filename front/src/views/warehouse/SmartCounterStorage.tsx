import { useDisclosure } from "@chakra-ui/hooks";
import { useQuery } from "@tanstack/react-query";
import CustomButton from "components/button";
import SmartCounterForm from "components/forms/SmartCounterForm";
import CustomModal from "components/modals";
import CustomPagination from "components/pagination";
import SimpleTable from "components/tables/SimpleTable";
import { useState } from "react";
import { reqFunction } from "utils/API";
import { CountOption, countSelect } from "variables";
// import { ModuleObject } from "./ModuleStorage";
import { DeviceObj } from "views/counters";
import Loading from "components/loading";
import { MdDelete, MdEdit } from "react-icons/md";
import {
  renderModuleAttr,
  renderToast,
  //  renderToast
} from "utils/globalUtils";
import DeleteForm from "components/forms/DeleteForm";
import { renderTags } from "utils/CommonFunctions";
type SmartStorageTable = {
  counterName: string;
  bodySerial: string;
  counterTag: JSX.Element;
  counterType: string;
  moduleType: string;
  moduleCode: string;
  moduleProperties: JSX.Element;
  counterActions: JSX.Element;
};
const SmartCounterStorage = () => {
  const AdminPermissions: string[] = JSON.parse(
    window.localStorage.getItem("permissions")
  );
  const [page, setPage] = useState<number>(1);
  const [count, setCount] = useState<CountOption>(countSelect[0]);
  // const [isEdit, setIsEdit] = useState<boolean>(false);
  const [selectedCounter, setSelectedCounter] = useState<DeviceObj | null>(
    null
  );
  // const [modulesWithoutMeter, setModulesWithoutMeter] = useState<
  //   null | ModuleObject[]
  // >(null);
  // const [simpleCounters, setSimpleCounters] = useState<null | DeviceObj[]>(
  //   null
  // );
  const {
    data: simpleCounterData,
    // isLoading: simpleCounterIsLoading,
    // status: simpleCounterStatus,
    refetch: simpleCounterRefetch,
  } = useQuery({
    queryFn: () =>
      reqFunction("watermeters/v2/admin/getAll", {
        page: 1,
        count: 100,
        user_id: null,
        project_id: null,
        water_meter_serial: null,
        water_meter_type_id: null,
        has_module: false,
      }),
    queryKey: ["simpleCounterList"],
  });
  const {
    data: counterlessModulesData,
    // isLoading: counterlessModulesIsLoading,
    // status: counterlessModulesStatus,
    refetch: counterlessModuleRefetch,
  } = useQuery({
    queryFn: () =>
      reqFunction("WaterMeterModules/admin/getAll", {
        page: 1,
        count: 100,
        water_meter_module_name: "",
        water_meter_module_create_date: "",
        mood: "modules_without_meter",
      }),
    queryKey: ["counterlessModulesList"],
  });
  const {
    data: smartCounterData,
    isLoading: smartCounterIsLoading,
    status: smartCounterStatus,
    refetch: smartCounterRefetch,
  } = useQuery({
    queryFn: () =>
      reqFunction("watermeters/v2/admin/getAll", {
        page: page,
        count: count.value,
        user_id: null,
        project_id: null,
        water_meter_serial: null,
        water_meter_type_id: null,
        has_module: true,
        has_user: false,
      }),
    queryKey: ["smartCounterList", page, count],
  });
  const {
    isOpen: isAddSmartCounterOpen,
    onOpen: onAddSmartCounterOpen,
    onClose: onAddSmartCounterClose,
  } = useDisclosure();
  const {
    isOpen: isDeleteConfirmOpen,
    onOpen: onDeleteConfirmOpen,
    onClose: onDeletConfirmClose,
  } = useDisclosure();
  const tableHeader = [
    { title: "نام کنتور", headerKey: "counterName" },
    { title: "سریال بدنه", headerKey: "bodySerial" },
    { title: "دسته بندی", headerKey: "counterTag" },
    { title: "نوع کنتور", headerKey: "counterType" },
    { title: "نوع ماژول", headerKey: "moduleType" },
    { title: "کد ماژول", headerKey: "moduleCode" },
    { title: "ویژگی های ماژول", headerKey: "moduleProperties" },
    { title: "عملیات", headerKey: "counterActions" },
  ];
  // const editDeviceClick = (counterInfo: DeviceObj) => {
  //   let tagOption = counterTagSelect.filter(
  //     (tag) =>
  //       tag.value ===
  //       counterInfo.water_meter_type__water_meter_tag__water_meter_tag_id
  //   )[0];
  //   setTag(tagOption);
  //   let typeSelects = renderTypeOptions();
  //   let typeOption = typeSelects.filter(
  //     (type) =>
  //       type.label === counterInfo.water_meter_type__water_meter_type_name
  //   )[0];
  //   let modelOption = counterModels.filter(
  //     (model) => model.value === counterInfo.water_meter_model
  //   )[0];
  //   let sizeOption = counterSizes.filter(
  //     (counter) => counter.value === counterInfo.water_meter_size
  //   )[0];
  //   setSelectedCounter(counterInfo);
  //   setCounterName(counterInfo.water_meter_name);
  //   setType(typeOption ? typeOption : null);
  //   setCounterModel(modelOption ? modelOption : null);
  //   setCounterSize(sizeOption ? sizeOption : null);
  //   setCounterSerial(counterInfo.water_meter_serial);
  //   setCounterManufacturer(
  //     counterInfo.other_information?.manufacturere
  //       ? counterInfo.other_information.manufacturere
  //       : ""
  //   );
  //   setManualNumber(
  //     counterInfo.water_meter_manual_number
  //       ? counterInfo.water_meter_manual_number
  //       : 0
  //   );

  //   setIsEdit(true);
  //   onAddSmartCounterOpen();
  // };
  const deleteSimpleCounterClicked = (counterInfo: DeviceObj) => {
    setSelectedCounter(counterInfo);
    onDeleteConfirmOpen();
  };
  const deleteSimpleCounter = async (serial: string) => {
    const response = await reqFunction("watermeters/admin/smartRemove", {
      water_meter_serial: serial,
    });
    if (response.code === 200) {
      renderToast("کنتور هوشمند با موفقیت حذف شد.", "success");
      onDeletConfirmClose();
      smartCounterRefetch();
      // clearForm();
    } else {
      renderToast(
        response?.farsi_message
          ? response.farsi_message
          : "در حذف کنتور هوشمند مشکلی رخ داده",
        "err"
      );
    }
  };
  const renderDeviceActions = (deviceInfo: DeviceObj) => {
    return (
      <>
        <div className=" flex items-center justify-center">
          {/* {AdminPermissions.includes("MeterEdit") ? (
          <CustomButton
            onClick={() => editDeviceClick(deviceInfo)}
            icon={<MdEdit />}
            color="orange"
            extra="!p-2"
          />
        ) : (
          // <></>
          <></>
        )} */}
          {AdminPermissions.includes("MeterDelete") ? (
            <CustomButton
              onClick={() => deleteSimpleCounterClicked(deviceInfo)}
              icon={<MdDelete />}
              color="red"
              extra="!p-2"
            />
          ) : (
            // <></>
            <></>
          )}
        </div>
      </>
    );
  };
  const updateSelectsDatas = () => {
    simpleCounterRefetch();
    counterlessModuleRefetch();
  };
  const tableData = () => {
    let deviceTableData: SmartStorageTable[] = [];
    smartCounterData.data?.forEach((device: DeviceObj) => {
      deviceTableData.push({
        counterName: device.water_meter_name,
        bodySerial: device.water_meter_serial,
        counterTag: renderTags(
          device.water_meter_type__water_meter_tag__water_meter_tag_name
        ),
        counterType: device.water_meter_type__water_meter_type_name,
        moduleCode: device.water_meter_module__water_meter_module_code,
        moduleType:
          device.water_meter_module__module_type__module_type_name ?? "__",
        moduleProperties:
          device?.water_meter_module__water_meter_module_property ? (
            renderModuleAttr(
              device.water_meter_module__water_meter_module_property,
              device.water_meter_module__water_meter_module_code
            )
          ) : (
            <></>
          ),
        counterActions: renderDeviceActions(device),
      });
    });

    return deviceTableData;
  };
  return (
    <>
      <CustomModal
        isOpen={isDeleteConfirmOpen}
        onClose={onDeletConfirmClose}
        title={""}
        modalType="form"
        information={null}
        modalForm={
          <DeleteForm
            deleteType="simpleCounter"
            simpleCounterDeleted={selectedCounter}
            onClose={onDeletConfirmClose}
            deleteFunction={deleteSimpleCounter}
          />
        }
      />
      <CustomModal
        title="کنتور هوشمند"
        isOpen={isAddSmartCounterOpen}
        onClose={onAddSmartCounterClose}
        modalType="form"
        modalForm={
          <SmartCounterForm
            simpleCountersData={simpleCounterData?.data}
            counterlessModules={counterlessModulesData?.data}
            onClose={onAddSmartCounterClose}
            updateTable={smartCounterRefetch}
            updateSelectsDatas={updateSelectsDatas}
          />
        }
      />
      <div className="relative flex items-center justify-between p-4">
        <div className="text-xl font-bold text-navy-700 dark:text-white">
          {`کنتورهای هوشمند (${
            smartCounterIsLoading
              ? "loading..."
              : smartCounterData?.data[0]?.all_water_meters
              ? smartCounterData?.data[0]?.all_water_meters
              : 0
          })`}
        </div>
        <div className=" moldal-btns flex items-center justify-end">
          <CustomButton
            text="افزودن کنتور هوشمند"
            onClick={() => onAddSmartCounterOpen()}
            icon={<></>}
            color="green"
            extra="ml-0"
          />
        </div>
      </div>
      {!smartCounterIsLoading && smartCounterStatus === "success" ? (
        <SimpleTable
          header={tableHeader}
          data={tableData()}
          extra="h-[56vh] "
          hasIndex={true}
        />
      ) : (
        <Loading />
      )}
      <div className="pagination ">
        <CustomPagination
          page={page}
          pageSize={count}
          totalData={
            smartCounterData?.data.length > 0
              ? smartCounterData.data[0].all_water_meters
              : 100
          }
          changePageFunc={setPage}
          changeCount={setCount}
        />
      </div>
    </>
  );
};
export default SmartCounterStorage;
