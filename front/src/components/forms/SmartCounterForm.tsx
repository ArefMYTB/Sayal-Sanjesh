import React, { useState } from "react";
import CustomButton from "../button";
// import InputField from "../fields/InputField";
import SelectInput, { DynamicOption } from "../fields/SelectInput";
import { reqFunction } from "../../utils/API";
import { renderToast } from "../../utils/globalUtils";
import { DeviceObj } from "views/counters";
import { ModuleObject } from "views/warehouse/ModuleStorage";
import { renderSelectData } from "utils/CommonFunctions";

interface SmartCounterFormProps {
  simpleCountersData: DeviceObj[];
  counterlessModules: ModuleObject[];
  onClose: Function;
  updateTable: any;
  updateSelectsDatas: any;
}
const SmartCounterForm = (props: SmartCounterFormProps) => {
  const {
    simpleCountersData,
    counterlessModules,
    onClose,
    updateTable,
    updateSelectsDatas,
  } = props;
  const [simpleCounterSelect, setSimpleCounterSelect] =
    useState<DynamicOption>(null);
  const [counterlessModuleSelect, setcounterlessModuleSelect] =
    useState<DynamicOption>(null);

  const createSmartCounter = async () => {
    if (simpleCounterSelect && counterlessModuleSelect) {
      let module = counterlessModules.filter(
          (module) =>
            module.water_meter_module_id === counterlessModuleSelect.value
        )[0],
        counter = simpleCountersData.filter(
          (device) => device.water_meter_serial === simpleCounterSelect.value
        )[0];
      const data = {
        water_meter_user_id: counter.water_meter_user__user_id,
        water_meter_name: counter.water_meter_name,
        water_meter_serial: counter.water_meter_serial,
        water_meter_location:
          typeof counter.water_meter_location === "string"
            ? { lat: "", lng: "" }
            : counter.water_meter_location,
        other_information: counter.other_information,
        water_meter_validation: counter.water_meter_validation,
        water_meter_activation: counter.water_meter_activation,
        water_meter_condition: counter.water_meter_condition,
        water_meter_type: counter.water_meter_type__water_meter_type_id,
        water_meter_project_id:
          counter.water_meter_project__water_meter_project_id,
        water_meter_module_id: module.water_meter_module_id,
        water_meter_manual_number: counter.water_meter_manual_number,
        water_meter_order_mode: counter.water_meter_order_mode,
        call_publisher: true,
      };
      let response = await reqFunction("watermeters/admin/edit", data);
      if (response.code === 200) {
        renderToast("ایجاد دستگاه با موفقیت انجام شد", "success");
        updateTable();
        onClose();
        updateSelectsDatas();
      } else {
        renderToast(
          response?.farsi_message
            ? response.farsi_message
            : "در ایجاد دستگاه خطایی رخ داده",
          "err"
        );
      }
    } else {
      renderToast("تمامی موارد را وارد کنید", "warn");
    }
  };
  return (
    <div className=" flex flex-col space-y-4">
      {/* <InputField
        id="simple-counter-name"
        label="نام کنتور هوشمند"
        placeholder="نام کنتور هوشمند را وارد کنید"
        type="text"
        state={counterName}
        setState={setCounterName}
      /> */}
      <SelectInput
        label="کنتور مکانیکی"
        placeholder="کنتور مکانیکی مورد نظر را انتخاب کنید"
        dynamicOptions={renderSelectData(simpleCountersData, "counter")}
        state={simpleCounterSelect}
        setState={setSimpleCounterSelect}
      />
      <SelectInput
        label="ماژول"
        placeholder="ماژول مورد نظر را انتخاب کنید"
        dynamicOptions={renderSelectData(counterlessModules, "module")}
        state={counterlessModuleSelect}
        setState={setcounterlessModuleSelect}
      />
      {/* <InputField
        id="simple-counter-serial"
        label="سریال بدنه"
        placeholder="سریال بدنه کنتور را وارد کنید"
        type="text"
        state={deviceTypeName}
        setState={setDeviceTypeName}
      /> */}
      <div className="form-actions flex flex-row items-center justify-end ">
        <CustomButton onClick={onClose} text="بستن" color="red" />
        <CustomButton
          onClick={() => createSmartCounter()}
          text={`ایجاد کنتور هوشمند`}
          color="green"
          extra="!ml-0"
        />
      </div>
    </div>
  );
};
export default SmartCounterForm;
