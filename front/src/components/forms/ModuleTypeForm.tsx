import CustomButton from "components/button";
import InputField from "components/fields/InputField";
import { reqFunction } from "utils/API";
import { renderToast } from "utils/globalUtils";

interface ModuleTypeFormProps {
  moduleTypeName: string;
  setModuleTypeName: React.Dispatch<string>;
  onClose: Function;
  updateTable: any;
  isEditForm: boolean;
  moduleId: string;
  clearForm: Function;
}
const ModuleTypeForm = (props: ModuleTypeFormProps) => {
  const {
    moduleTypeName,
    setModuleTypeName,
    onClose,
    updateTable,
    moduleId,
    isEditForm,
    clearForm,
  } = props;
  const createModuleType = async () => {
    if (moduleTypeName) {
      const json = {
        module_type_name: moduleTypeName,
        module_other_information: {},
      };
      let response = await reqFunction("ModuleType/admin/add", json);
      if (response.code === 200) {
        renderToast("ایجاد نوع ماژول با موفقیت انجام شد", "success");
        updateTable();
        onClose();
        clearForm();
      } else {
        renderToast(
          response?.farsi_message
            ? response.farsi_message
            : "در ایجاد نوع ماژول خطایی رخ داده",
          "err"
        );
      }
    } else {
      renderToast("تمامی موارد را وارد کنید", "warn");
    }
  };
  const editModuleType = async () => {
    if (moduleTypeName) {
      const json = {
        module_type_id: moduleId,
        module_type_name: moduleTypeName,
        module_other_information: {},
      };
      let response = await reqFunction("ModuleType/admin/edit", json);
      if (response.code === 200) {
        renderToast("تغییر نوع ماژول با موفقیت انجام شد", "success");
        updateTable();
        onClose();
        clearForm();
      } else {
        renderToast(
          response?.farsi_message
            ? response.farsi_message
            : "در تغییر نوع ماژول خطایی رخ داده",
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
        id="tag-name"
        label="نام نوع ماژول"
        placeholder="نام نوع ماژول را وارد کنید"
        type="text"
        state={moduleTypeName}
        setState={setModuleTypeName}
      />

      <div className="form-actions flex flex-row items-center justify-end ">
        <CustomButton onClick={onClose} text="بستن" color="red" />
        <CustomButton
          onClick={() => (isEditForm ? editModuleType() : createModuleType())}
          text={isEditForm ? "تغییر" : "ایجاد"}
          color="green"
          extra="!ml-0"
        />
      </div>
    </div>
  );
};
export default ModuleTypeForm;
