import { useDisclosure } from "@chakra-ui/hooks";
import { useQuery } from "@tanstack/react-query";
import CustomButton from "components/button";
import { DynamicOption } from "components/fields/SelectInput";
import DeleteForm from "components/forms/DeleteForm";
import SimpleCounterForm from "components/forms/SimpleCounterForm";
import Loading from "components/loading";
import CustomModal from "components/modals";
import CustomPagination from "components/pagination";
import SimpleTable from "components/tables/SimpleTable";
import { useState } from "react";
import { MdDelete, MdEdit } from "react-icons/md";
import { reqFunction } from "utils/API";
import { renderTags } from "utils/CommonFunctions";
import { renderToast } from "utils/globalUtils";
import {
  CountOption,
  countSelect,
  counterModels,
  counterSizes,
  counterTagSelect,
} from "variables";
import { DeviceObj } from "views/counters";
import { TypeObject } from "views/settings/DeviceTypesTable";
type SimpleCounterTableData = {
  counterName: string;
  bodySerial: string;
  counterTag: JSX.Element;
  counterType: string;
  counterModel: string;
  counterSize: string;
  manufacture: string;
  counterActions: JSX.Element;
};
const SimpleCounterStorage = () => {
  const AdminPermissions: string[] = JSON.parse(
    window.localStorage.getItem("permissions")
  );
  const [counterName, setCounterName] = useState<string>("");
  const [tag, setTag] = useState<DynamicOption>(null);
  const [type, setType] = useState<DynamicOption>(null);
  const [counterModel, setCounterModel] = useState<DynamicOption>(null);
  const [counterSize, setCounterSize] = useState<CountOption>(null);
  const [counterSerial, setCounterSerial] = useState<string>("");
  const [counterManufacturer, setCounterManufacturer] = useState<string>("");
  const [manualNumber, setManualNumber] = useState<number>(0);
  const [isEdit, setIsEdit] = useState<boolean>(false);
  const [selectedCounter, setSelectedCounter] = useState<DeviceObj | null>(
    null
  );
  const [page, setPage] = useState<number>(1);
  const [count, setCount] = useState<CountOption>(countSelect[0]);
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
    data: simpleCounterData,
    isLoading: simpleCounterIsLoading,
    status: simpleCounterStatus,
    refetch: simpleCounterRefetch,
  } = useQuery({
    queryFn: () =>
      reqFunction("watermeters/v2/admin/getAll", {
        page: page,
        count: count.value,
        user_id: null,
        project_id: null,
        water_meter_serial: null,
        water_meter_type_id: null,
        has_module: false,
      }),
    queryKey: ["simpleCounterList", page, count],
  });
  const {
    isOpen: isAddCounterOpen,
    onOpen: onAddCounterOpen,
    onClose: onAddCounterClose,
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
    { title: "مدل کنتور", headerKey: "counterModel" },
    { title: "سایز کنتور", headerKey: "counterSize" },
    { title: "تولید کننده", headerKey: "manufacture" },
    { title: "عملیات", headerKey: "counterActions" },
  ];

  const editDeviceClick = (counterInfo: DeviceObj) => {
    let tagOption = counterTagSelect.filter(
      (tag) =>
        tag.value ===
        counterInfo.water_meter_type__water_meter_tag__water_meter_tag_id
    )[0];
    setTag(tagOption);
    let typeSelects = renderTypeOptions();
    let typeOption = typeSelects.filter(
      (type) =>
        type.label === counterInfo.water_meter_type__water_meter_type_name
    )[0];
    let modelOption = counterModels.filter(
      (model) => model.value === counterInfo.water_meter_model
    )[0];
    let sizeOption = counterSizes.filter(
      (counter) => counter.value === counterInfo.water_meter_size
    )[0];
    setSelectedCounter(counterInfo);
    setCounterName(counterInfo.water_meter_name);
    setType(typeOption ? typeOption : null);
    setCounterModel(modelOption ? modelOption : null);
    setCounterSize(sizeOption ? sizeOption : null);
    setCounterSerial(counterInfo.water_meter_serial);
    setCounterManufacturer(
      counterInfo.other_information?.manufacturere
        ? counterInfo.other_information.manufacturere
        : ""
    );
    setManualNumber(
      counterInfo.water_meter_manual_number
        ? counterInfo.water_meter_manual_number
        : 0
    );
    setIsEdit(true);
    onAddCounterOpen();
  };
  const deleteSimpleCounterClicked = (counterInfo: DeviceObj) => {
    setSelectedCounter(counterInfo);
    onDeleteConfirmOpen();
  };
  const deleteSimpleCounter = async (serial: string) => {
    const response = await reqFunction("watermeters/admin/remove", {
      water_meter_serial: serial,
    });
    if (response.code === 200) {
      renderToast("کنتور مکانیکی با موفقیت حذف شد.", "success");
      onDeletConfirmClose();
      simpleCounterRefetch();
      clearForm();
    } else {
      renderToast(
        response?.farsi_message
          ? response.farsi_message
          : "در حذف کنتور مکانیکی مشکلی رخ داده",
        "err"
      );
    }
  };
  const renderDeviceActions = (deviceInfo: DeviceObj) => {
    return (
      <div className=" flex items-center justify-center">
        {AdminPermissions.includes("Store") ? (
          <CustomButton
            onClick={() => editDeviceClick(deviceInfo)}
            icon={<MdEdit />}
            color="orange"
            extra="!p-2"
          />
        ) : (
          <></>
        )}
        {AdminPermissions.includes("Store") ? (
          <CustomButton
            onClick={() => {
              deleteSimpleCounterClicked(deviceInfo);
            }}
            icon={<MdDelete />}
            color="red"
            extra="!p-2"
          />
        ) : (
          <></>
        )}
      </div>
    );
  };
  const renderTypeOptions = () => {
    let allTypes: TypeObject[] = typesData?.data ? typesData.data : [];
    let typeSelectData: DynamicOption[] = [];
    if (tag) {
      allTypes.forEach((type) => {
        typeSelectData.push({
          label: type.water_meter_type_name,
          value: type.water_meter_type_id,
          disabled: tag.value !== type.water_meter_tag.water_meter_tag_id,
        });
      });
    } else {
      allTypes.forEach((type) => {
        typeSelectData.push({
          label: type.water_meter_type_name,
          value: type.water_meter_type_id,
        });
      });
    }
    return typeSelectData;
  };
  const renderDeviceModel = (model: string) => {
    if (model) {
      return counterModels.filter((counter) => counter.value === model)[0]
        .label;
    } else {
      return "__";
    }
  };
  const renderDeviceSize = (size: number) => {
    if (size) {
      return counterSizes.filter((counter) => counter.value === size)[0].label;
    } else {
      return "__";
    }
  };
  const tableData = () => {
    let deviceTableData: SimpleCounterTableData[] = [];
    simpleCounterData?.data?.forEach((device: DeviceObj) => {
      deviceTableData.push({
        counterName: device.water_meter_name,
        bodySerial: device.water_meter_serial,
        counterTag: renderTags(
          device.water_meter_type__water_meter_tag__water_meter_tag_name
        ),
        counterType: device.water_meter_type__water_meter_type_name,
        counterModel: renderDeviceModel(device.water_meter_model),
        counterSize: renderDeviceSize(device.water_meter_size),
        manufacture: device.other_information?.manufacturere
          ? device.other_information.manufacturere
          : "__",
        counterActions: renderDeviceActions(device),
      });
    });

    return deviceTableData;
  };
  const clearForm = () => {
    setCounterName("");
    setTag(null);
    setType(null);
    setCounterModel(null);
    setCounterSize(null);
    setCounterSerial("");
    setCounterManufacturer("");
    setManualNumber(0);
    setIsEdit(false);
    setSelectedCounter(null);
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
        title="کنتور غیر هوشمند"
        isOpen={isAddCounterOpen}
        onClose={onAddCounterClose}
        modalType="form"
        modalForm={
          <SimpleCounterForm
            counterInformation={selectedCounter}
            counterName={counterName}
            setCounterName={setCounterName}
            tag={tag}
            setTag={setTag}
            typeOptions={renderTypeOptions()}
            type={type}
            setType={setType}
            counterModel={counterModel}
            setCounterModel={setCounterModel}
            counterSize={counterSize}
            setCounterSize={setCounterSize}
            counterSerial={counterSerial}
            setCounterSerial={setCounterSerial}
            counterManufacturer={counterManufacturer}
            setCounterManufacturer={setCounterManufacturer}
            manualNumber={manualNumber}
            setManualNumber={setManualNumber}
            onClose={onAddCounterClose}
            updateTable={simpleCounterRefetch}
            clearForm={clearForm}
            isEditForm={isEdit}
          />
        }
      />
      <div className="relative flex items-center justify-between p-4">
        <div className="text-xl font-bold text-navy-700 dark:text-white">
          {`کنتورهای مکانیکی (${
            simpleCounterIsLoading
              ? "loading..."
              : Array.isArray(simpleCounterData?.data) &&
                simpleCounterData.data.length > 0
              ? simpleCounterData.data[0].all_water_meters
              : 0
          })`}
        </div>
        <div className=" moldal-btns flex items-center justify-end">
          <CustomButton
            text="افزودن کنتور مکانیکی"
            onClick={() => {
              clearForm();
              onAddCounterOpen();
            }}
            icon={<></>}
            color="green"
            extra="ml-0"
          />
        </div>
      </div>
      {!typesIsLoading &&
      typesStatus === "success" &&
      !simpleCounterIsLoading &&
      simpleCounterStatus === "success" ? (
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
            simpleCounterData?.data?.length > 0
              ? simpleCounterData.data[0].all_water_meters
              : 100
          }
          changePageFunc={setPage}
          changeCount={setCount}
        />
      </div>
    </>
  );
};
export default SimpleCounterStorage;
