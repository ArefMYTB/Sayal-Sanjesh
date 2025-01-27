import { useState } from "react";
import CustomButton from "../button";
import InputField from "../fields/InputField";
import SelectInput, { DynamicOption } from "../fields/SelectInput";
import CheckInput from "components/fields/CheckInput";
import { moduleAttributes, simOprators } from "variables";
import { renderToast } from "utils/globalUtils";
import { reqFunction } from "utils/API";
import { ModuleObject } from "views/warehouse/ModuleStorage";

interface ModuleFormProps {
  moduleInfo: ModuleObject | null;
  setModuleInfo: React.Dispatch<ModuleObject | null>;
  isEdit: boolean;
  setIsEdit: React.Dispatch<boolean>;
  moduleTypeSelectData: DynamicOption[] | null;
  onClose: Function;
  updateTable: any;
}
const ModuleForm = (props: ModuleFormProps) => {
  const {
    moduleInfo,
    setModuleInfo,
    isEdit,
    setIsEdit,
    moduleTypeSelectData,
    onClose,
    updateTable,
  } = props;
  const [moduleName, setModuleName] = useState<string>(
    isEdit && moduleInfo?.water_meter_module_name
      ? moduleInfo.water_meter_module_name
      : ""
  );
  const [moduleType, setModuleType] = useState<DynamicOption | null>(
    isEdit && moduleInfo.module_type_info?.module_type_id
      ? {
          label: moduleInfo.module_type_info.module_type_name,
          value: moduleInfo.module_type_info.module_type_id,
        }
      : null
  );
  const [moduleCode, setModuleCode] = useState<string>(
    isEdit && moduleInfo?.water_meter_module_code
      ? moduleInfo.water_meter_module_code
      : ""
  );
  const [moduleAttr, setModuleAttr] = useState<string[]>(
    isEdit && moduleInfo?.water_meter_module_property
      ? moduleInfo.water_meter_module_property
      : []
  );
  const [moduleOprator, setModuleOprator] = useState<DynamicOption | null>(
    isEdit && moduleInfo?.water_meter_module_sim_operator
      ? simOprators.filter(
          (oprator) =>
            oprator.value === moduleInfo.water_meter_module_sim_operator
        )[0]
      : null
  );
  const [moduleSim, setModuleSim] = useState<string>(
    isEdit && moduleInfo?.water_meter_module_sim
      ? moduleInfo.water_meter_module_sim
      : ""
  );
  const createModule = async () => {
    if (moduleName && moduleType && moduleCode) {
      const data = {
        water_meter_module_name: moduleName,
        water_meter_module_code: moduleCode,
        module_type_id: moduleType.value,
        water_meter_module_sim: moduleSim,
        water_meter_module_sim_operator: moduleOprator
          ? moduleOprator.value
          : null,
        water_meter_module_property: moduleAttr,
        water_meter_module_other_information: {},
      };
      let response = await reqFunction("WaterMeterModules/admin/add", data);
      if (response.code === 200) {
        renderToast("ایجاد ماژول با موفقیت انجام شد", "success");
        updateTable();
        setIsEdit(false);
        setModuleInfo(null);
        onClose();
      } else {
        renderToast(
          response?.farsi_message
            ? response.farsi_message
            : "در ایجاد ماژول خطایی رخ داده",
          "err"
        );
      }
    } else {
      renderToast("تمامی موارد را وارد کنید", "warn");
    }
  };
  const editModule = async () => {
    if (moduleName && moduleType && moduleCode) {
      const data = {
        water_meter_module_id: moduleInfo.water_meter_module_id,
        water_meter_module_name: moduleName,
        water_meter_module_code: moduleCode,
        module_type_id: moduleType.value,
        water_meter_module_sim: moduleSim,
        water_meter_module_sim_operator: moduleOprator
          ? moduleOprator.value
          : null,
        water_meter_module_property: moduleAttr,
        water_meter_module_other_information: {},
      };
      let response = await reqFunction("WaterMeterModules/admin/edit", data);
      if (response.code === 200) {
        renderToast("تغییر ماژول با موفقیت انجام شد", "success");
        updateTable();
        setIsEdit(false);
        setModuleInfo(null);
        onClose();
      } else {
        renderToast(
          response?.farsi_message
            ? response.farsi_message
            : "در تغییر ماژول خطایی رخ داده",
          "err"
        );
      }
    } else {
      renderToast("تمامی موارد را وارد کنید", "warn");
    }
  };
  return (
    <div className=" flex flex-col space-y-4">
      <InputField
        id="module-name"
        label="نام ماژول"
        placeholder="نام ماژول را وارد کنید"
        type="text"
        state={moduleName}
        setState={setModuleName}
      />
      <SelectInput
        label="نوع ماژول"
        placeholder="نوع ماژول مورد نظر را انتخاب کنید"
        dynamicOptions={moduleTypeSelectData}
        state={moduleType}
        setState={setModuleType}
      />
      <InputField
        id="module-serial"
        label="کد ماژول"
        placeholder="کد ماژول کنتور را وارد کنید"
        type="text"
        state={moduleCode}
        setState={setModuleCode}
        disabled={isEdit ? true : false}
      />
      <CheckInput
        checkTitle="ویژگی های ماژول"
        inputsData={moduleAttributes}
        checkedData={moduleAttr}
        setCheckedData={setModuleAttr}
      />
      <SelectInput
        label="نوع سیمکارت"
        placeholder="نوع سیمکارت مورد نظر را انتخاب کنید"
        dynamicOptions={simOprators}
        state={moduleOprator}
        setState={setModuleOprator}
      />
      <InputField
        id="simple-counter-name"
        label="شماره سیمکارت"
        placeholder="شماره سیمکارت کنتور را وارد کنید"
        type="number"
        state={moduleSim}
        setState={setModuleSim}
      />
      <div className="form-actions flex flex-row items-center justify-end ">
        <CustomButton onClick={onClose} text="بستن" color="red" />
        <CustomButton
          onClick={() => (isEdit ? editModule() : createModule())}
          text={isEdit ? "تغییر ماژول" : "ایجاد ماژول"}
          color="green"
          extra="!ml-0"
        />
      </div>
    </div>
  );
};
export default ModuleForm;
