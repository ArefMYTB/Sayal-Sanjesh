import React from "react";
import CustomButton from "../button";
import InputField from "../fields/InputField";
import SelectInput, { DynamicOption } from "../fields/SelectInput";
import { reqFunction } from "../../utils/API";
import { renderToast } from "../../utils/globalUtils";
import {
  CountOption,
  counterModels,
  counterSizes,
  counterTagSelect,
} from "variables";
import { DeviceObj } from "views/counters";

interface SimpleCounterFormProps {
  counterInformation: DeviceObj | null;
  counterName: string;
  setCounterName: React.Dispatch<string>;
  tag: DynamicOption | null;
  setTag: React.Dispatch<DynamicOption | null>;
  type: DynamicOption | null;
  setType: React.Dispatch<DynamicOption | null>;
  typeOptions: DynamicOption[];
  counterModel: DynamicOption | null;
  setCounterModel: React.Dispatch<DynamicOption | null>;
  counterSize: CountOption | null;
  setCounterSize: React.Dispatch<CountOption | null>;
  counterSerial: string;
  setCounterSerial: React.Dispatch<string>;
  counterManufacturer: string;
  setCounterManufacturer: React.Dispatch<string>;
  manualNumber: number;
  setManualNumber: React.Dispatch<number>;
  onClose: Function;
  updateTable: any;
  isEditForm: boolean;
  clearForm: Function;
}
const SimpleCounterForm = (props: SimpleCounterFormProps) => {
  const {
    counterInformation,
    counterName,
    setCounterName,
    tag,
    setTag,
    type,
    setType,
    typeOptions,
    counterModel,
    setCounterModel,
    counterSize,
    setCounterSize,
    counterSerial,
    setCounterSerial,
    counterManufacturer,
    setCounterManufacturer,
    manualNumber,
    setManualNumber,
    clearForm,
    onClose,
    updateTable,
    isEditForm,
  } = props;
  const createSimpleCounter = async () => {
    const simpleCounterData: any = {
      water_meter_user_id: null,
      water_meter_name: counterName,
      water_meter_serial: counterSerial,
      water_meter_location: { lat: "", lng: "" },
      other_information: { manufacturere: counterManufacturer },
      water_meter_validation: 0,
      water_meter_activation: 0,
      water_meter_condition: 0,
      water_meter_type: type.value,
      water_meter_project: null,
      water_meter_module: null,
      water_meter_manual_number: manualNumber,
      water_meter_order_mode: "",
      water_meter_model: counterModel.value,
      water_meter_size: counterSize.value,
    };
    let response = await reqFunction(
      "watermeters/admin/create",
      simpleCounterData
    );
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
  };
  const editSimpleCounter = async () => {
    const simpleCounterData: any = {
      water_meter_user_id: counterInformation.water_meter_user__user_id,
      water_meter_name: counterName,
      water_meter_serial: counterSerial,
      water_meter_location: { lat: "", lng: "" },
      other_information: { manufacturere: counterManufacturer },
      water_meter_validation: counterInformation.water_meter_validation,
      water_meter_activation: counterInformation.water_meter_activation,
      water_meter_condition: counterInformation.water_meter_condition,
      water_meter_type: type.value,
      water_meter_project_id:
        counterInformation.water_meter_project__water_meter_project_id,
      water_meter_module_id:
        counterInformation.water_meter_module__water_meter_module_id,
      water_meter_manual_number: manualNumber,
      water_meter_order_mode: "",
      water_meter_model: counterModel.value,
      water_meter_size: counterSize.value,
    };
    let response = await reqFunction(
      "watermeters/admin/edit",
      simpleCounterData
    );
    if (response.code === 200) {
      renderToast("تغییر دستگاه با موفقیت انجام شد", "success");
      updateTable();
      onClose();
      clearForm();
    } else {
      renderToast(
        response?.farsi_message
          ? response.farsi_message
          : "در تغییر دستگاه خطایی رخ داده",
        "err"
      );
    }
  };
  return (
    <div className=" flex flex-col space-y-4">
      <InputField
        id="simple-counter-name"
        label="نام کنتور"
        placeholder="نام کنتور مکانیکی را وارد کنید"
        type="text"
        state={counterName}
        setState={setCounterName}
      />
      <InputField
        id="simple-counter-serial"
        label="سریال کنتور"
        placeholder="سریال بدنه یا مکانیزم کنتور را وارد کنید"
        type="text"
        state={counterSerial}
        setState={setCounterSerial}
        disabled={isEditForm}
      />
      <SelectInput
        label="دسته بندی"
        placeholder="دسته بندی مورد نظر را انتخاب کنید"
        dynamicOptions={counterTagSelect}
        state={tag}
        setState={setTag}
      />
      <SelectInput
        label="نوع کنتور"
        placeholder="نوع کنتور مورد نظر را انتخاب کنید"
        dynamicOptions={typeOptions}
        state={type}
        setState={setType}
      />
      <SelectInput
        label="مدل کنتور"
        placeholder="مدل کنتور مورد نظر را انتخاب کنید"
        dynamicOptions={counterModels}
        state={counterModel}
        setState={setCounterModel}
      />
      <SelectInput
        label="سایز کنتور"
        placeholder="سایز کنتور مورد نظر را انتخاب کنید"
        dynamicOptions={counterSizes}
        state={counterSize}
        setState={setCounterSize}
      />
      <InputField
        id="simple-counter-mechanichal-number"
        label="عدد مکانیکی"
        placeholder="عدد مکانیکی کنتور را وارد کنید"
        type="number"
        state={manualNumber}
        setState={setManualNumber}
      />
      <InputField
        id="simple-counter-manufacturer"
        label="تولید کننده"
        placeholder="نام تولید کننده کنتور را وارد کنید"
        type="text"
        state={counterManufacturer}
        setState={setCounterManufacturer}
      />

      <div className="form-actions flex flex-row items-center justify-end ">
        <CustomButton onClick={onClose} text="بستن" color="red" />
        <CustomButton
          onClick={() =>
            isEditForm ? editSimpleCounter() : createSimpleCounter()
          }
          text={isEditForm ? "تغییر کنتور مکانیکی" : `ایجاد کنتور مکانیکی`}
          color="green"
          extra="!ml-0"
        />
      </div>
    </div>
  );
};
export default SimpleCounterForm;
