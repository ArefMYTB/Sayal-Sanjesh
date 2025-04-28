import CustomButton from "components/button";
import InputField from "components/fields/InputField";
import SelectInput, { DynamicOption } from "components/fields/SelectInput";
// import GetLocationMap from "components/map/GetLocationMap";
import { useState } from "react";
import { reqFunction } from "utils/API";
import { renderToast } from "utils/globalUtils";
import { deviceOrderModesSelectData } from "variables";
import "leaflet/dist/leaflet.css";
import CheckInput from "components/fields/CheckInput";
import GetLocationMap from "components/map/GetLocationMap";
import { DeviceObj } from "views/counters";
import { renderUnit } from "utils/CommonFunctions";
export type DeviceFormObject = {
  water_meter_name: null | string;
  water_meter_serial: null | string;
  water_meter_project: null | string;
  water_meter_user_id: null | string;
  water_meter_validation: number;
  water_meter_activation: number;
  water_meter_condition: number;
  water_meter_type: null | string;
  water_meter_module: null | string;
  water_meter_manual_number: null | number;
  water_meter_order_mode: "P " | "R" | "";
  water_meter_location: any;
  call_publisher: any;
  other_information: {};
};
interface DeviceFormProps {
  deviceName: null | string;
  setDeviceName: React.Dispatch<any>;
  deviceSerial: null | string;
  setDeviceSerial: React.Dispatch<any>;
  deviceProjectOptions: DynamicOption[];
  deviceProject: null | DynamicOption;
  setDeviceProject: React.Dispatch<any>;
  deviceUserOptions: DynamicOption[];
  deviceUser: null | DynamicOption;
  setDeviceUser: React.Dispatch<any>;
  deviceModuleOptions: DynamicOption[];
  deviceModule: null | DynamicOption;
  setDeviceModule: React.Dispatch<any>;
  deviceTypesOptions: DynamicOption[];
  deviceType: null | DynamicOption;
  setDeviceType: React.Dispatch<any>;
  deviceManualNumber: null | number;
  setDeviceManualNumber: React.Dispatch<any>;
  deviceOrderMode: null | DynamicOption;
  setDeviceOrderMode: React.Dispatch<any>;
  onClose: Function;
  isEditForm: boolean;
  setEditForm: React.Dispatch<any>;
  updateTable: any;
  selectedDevice: DeviceObj;
}
const DeviceForm = (props: DeviceFormProps) => {
  const {
    deviceName,
    setDeviceName,
    deviceSerial,
    setDeviceSerial,
    deviceProject,
    setDeviceProject,
    deviceUser,
    setDeviceUser,
    deviceType,
    setDeviceType,
    deviceModule,
    setDeviceModule,
    deviceManualNumber,
    setDeviceManualNumber,
    deviceOrderMode,
    setDeviceOrderMode,
    deviceProjectOptions,
    deviceModuleOptions,
    deviceTypesOptions,
    deviceUserOptions,
    isEditForm,
    setEditForm,
    updateTable,
    selectedDevice,
    onClose,
  } = props;
  const [nameBorder, setNameBorder] = useState<
    "err" | "success" | "dis" | "normal"
  >("normal");
  const [serialBorder, setSerialBorder] = useState<
    "err" | "success" | "dis" | "normal"
  >("normal");
  const [hasManualLocation, setHasManualLocation] = useState<string[]>(
    isEditForm &&
      typeof selectedDevice?.water_meter_location !== "string" &&
      selectedDevice?.water_meter_location?.lat
      ? ["manual-location"]
      : []
  );
  const [lat, setLat] = useState<number | null>(
    isEditForm &&
      typeof selectedDevice?.water_meter_location !== "string" &&
      selectedDevice?.water_meter_location?.lat
      ? selectedDevice.water_meter_location.lat
      : 35.724096
  );
  const [lng, setLng] = useState<number | null>(
    isEditForm &&
      typeof selectedDevice?.water_meter_location !== "string" &&
      selectedDevice?.water_meter_location?.lng
      ? selectedDevice.water_meter_location.lng
      : 51.430389
  );
  // const [typeBorder, setTypeBorder] = useState<
  //   "err" | "success" | "dis" | "normal"
  // >("normal");
  // const [moduleBorder, setModuleBorder] = useState<
  //   "err" | "success" | "dis" | "normal"
  // >("normal");
  const clearForm = () => {
    setDeviceName("");
    setDeviceSerial("");
    setDeviceProject(null);
    setDeviceType(null);
    setDeviceManualNumber(null);
    setDeviceModule(null);
    setDeviceOrderMode(null);
    setDeviceUser(null);
  };
  const createDevice = async () => {
    if (
      deviceName &&
      deviceSerial &&
      deviceType
      // && deviceModule
    ) {
      const data = {
        water_meter_user_id: deviceUser ? deviceUser.value : null,
        water_meter_name: deviceName,
        water_meter_serial: deviceSerial,
        water_meter_location: {
          lat: lat ? Number(lat) : 0,
          lng: lng ? Number(lng) : 0,
        },
        other_information: {},
        water_meter_validation: 0,
        water_meter_activation: 0,
        water_meter_condition: 0,
        water_meter_type: deviceType ? deviceType.value : null,
        water_meter_project: deviceProject ? deviceProject.value : null,
        water_meter_module: deviceModule ? deviceModule.value : null,
        water_meter_manual_number: deviceManualNumber,
        water_meter_order_mode: deviceOrderMode ? deviceOrderMode.value : "",
      };
      let response = await reqFunction("watermeters/admin/create", data);
      if (response.code === 200) {
        renderToast("ایجاد دستگاه با موفقیت انجام شد", "success");
        updateTable();
        onClose();
        clearForm();
      } else {
        renderToast(
          response?.farsi_message
            ? response.farsi_message
            : "در ایجاد دستگاه خطایی رخ داده",
          "err"
        );
      }
    } else {
      deviceName ? setNameBorder("normal") : setNameBorder("err");
      deviceSerial ? setSerialBorder("normal") : setSerialBorder("err");
      // deviceType ? setTypeBorder("normal") : setTypeBorder("err");
      // deviceModule ? setModuleBorder("normal") : setModuleBorder("err");
      renderToast("تمامی موارد را وارد کنید", "warn");
    }
  };
  const editDevice = async () => {
    console.log("edit");
    if (
      deviceName &&
      deviceSerial &&
      deviceType
      // && deviceModule
    ) {
      const data = {
        water_meter_user_id: deviceUser ? deviceUser.value : null,
        water_meter_name: deviceName,
        water_meter_serial: deviceSerial,
        water_meter_location: {
          lat: lat ? Number(lat) : 0,
          lng: lng ? Number(lng) : 0,
        },
        other_information: {},
        water_meter_validation: selectedDevice.water_meter_validation,
        water_meter_activation: selectedDevice.water_meter_activation,
        water_meter_condition: selectedDevice.water_meter_condition,
        water_meter_type: deviceType ? deviceType.value : null,
        water_meter_project_id: deviceProject ? deviceProject.value : null,
        water_meter_module_id: deviceModule ? deviceModule.value : null,
        water_meter_manual_number: deviceManualNumber,
        water_meter_order_mode: deviceOrderMode ? deviceOrderMode.value : "",
        call_publisher: true,
      };

      let response = await reqFunction("watermeters/admin/edit", data);
      if (response.code === 200) {
        renderToast("تغییر دستگاه با موفقیت انجام شد", "success");
        updateTable();
        onClose();
        clearForm();
        setEditForm(false);
      } else {
        renderToast(
          response?.farsi_message
            ? response.farsi_message
            : "در تغییر دستگاه خطایی رخ داده",
          "err"
        );
      }
    } else {
      deviceName ? setNameBorder("normal") : setNameBorder("err");
      deviceSerial ? setSerialBorder("normal") : setSerialBorder("err");
      // deviceType ? setTypeBorder("normal") : setTypeBorder("err");
      // deviceModule ? setModuleBorder("normal") : setModuleBorder("err");
      renderToast("تمامی موارد را وارد کنید", "warn");
    }
  };
  return (
    <div className="flex flex-col lg:flex-row lg:gap-12 p-4">
      <div className="flex-1 flex flex-col gap-4">
        <InputField
          id="device-type-name"
          label="نام دستگاه"
          placeholder="نام نوع دستگاه را وارد کنید"
          type="text"
          state={deviceName}
          setState={setDeviceName}
          border={nameBorder}
        />
        {/* {isEditForm ? (
          
        ) : (
          <></>
        )} */}
        <InputField
          id="device-type-name"
          label="سریال دستگاه"
          placeholder="سریال دستگاه را وارد کنید"
          type="text"
          disabled={isEditForm}
          state={deviceSerial}
          setState={setDeviceSerial}
          border={serialBorder}
        />
        <SelectInput
          label=" نوع دستگاه"
          placeholder="نوع دستگاه مورد نظر را انتخاب کنید"
          dynamicOptions={deviceTypesOptions}
          state={deviceType}
          setState={setDeviceType}
          disabled={isEditForm}
        />
        <SelectInput
          label=" ماژول دستگاه"
          placeholder="ماژول مورد نظر را انتخاب کنید"
          dynamicOptions={deviceModuleOptions}
          state={deviceModule}
          setState={setDeviceModule}
          // disabled={isEditForm}
        />
        <SelectInput
          label=" پروژه دستگاه"
          placeholder="پروژه مورد نظر را انتخاب کنید"
          dynamicOptions={deviceProjectOptions}
          state={deviceProject}
          setState={setDeviceProject}
        />
        <SelectInput
          label=" مالک دستگاه"
          placeholder="مالک دستگاه مورد نظر را انتخاب کنید"
          dynamicOptions={deviceUserOptions}
          state={deviceUser}
          setState={setDeviceUser}
        />
        {/* <SelectInput
          label=" قابلیت دستور"
          placeholder="قابلیت دستور پذیری دستگاه مورد نظر را انتخاب کنید"
          dynamicOptions={deviceOrderModesSelectData}
          state={deviceOrderMode}
          setState={setDeviceOrderMode}
        /> */}
        <InputField
          id="device-type-name"
          label={`عدد مکانیکی (${renderUnit(
            selectedDevice.water_meter_type__water_meter_tag__water_meter_tag_name,
            false
          )})`}
          placeholder="عدد مکانیکی دستگاه را وارد کنید"
          type="number"
          state={deviceManualNumber}
          setState={setDeviceManualNumber}
          // border={serialBorder}
        />
      </div>
      <div className="flex-1 flex flex-col gap-4">
        <CheckInput
          inputsData={[
            { id: "manual-location", name: "ایجاد موقعیت مکانی" },
          ]}
          checkedData={hasManualLocation}
          setCheckedData={setHasManualLocation}
        />
        {hasManualLocation.length > 0 ? (
          <GetLocationMap lat={lat} setLat={setLat} lng={lng} setLng={setLng} />
        ) : (
          <></>
        )}
        <div
          className={`form-actions !mt-2 flex flex-row items-center justify-end `}
        >
          <CustomButton onClick={onClose} text="بستن" color="red" />
          <CustomButton
            onClick={() => (isEditForm ? editDevice() : createDevice())}
            text={`${isEditForm ? "تغییر" : "ایجاد"}`}
            color="green"
            extra="!ml-0"
          />
        </div>
      </div>
    </div>
  );
};
export default DeviceForm;
