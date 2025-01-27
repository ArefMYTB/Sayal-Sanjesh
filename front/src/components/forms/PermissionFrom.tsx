import CustomButton from "components/button";
import InputField from "components/fields/InputField";
import { reqFunction } from "utils/API";
import { renderToast } from "utils/globalUtils";

interface PermissionFromProps {
  englishName: null | string;
  setEnglishName: React.Dispatch<any>;
  farsiName: null | string;
  setFarsiName: React.Dispatch<any>;
  onClose: Function;
  updateTable: any;
  permissionId: null | string;
  isEdit: boolean;
  clearForm: Function;
}
const PermissionForm = (props: PermissionFromProps) => {
  const {
    englishName,
    setEnglishName,
    farsiName,
    setFarsiName,
    onClose,
    updateTable,
    clearForm,
    permissionId,
    isEdit,
  } = props;
  const addPermission = async () => {
    if (englishName) {
      const json = {
        permission_english_name: englishName,
        permission_persian_name: farsiName,
        permission_description: "",
      };
      let response = await reqFunction("Permissions/admin/create", json);
      if (response.code === 200) {
        renderToast("ایجاد دسترسی با موفقیت انجام شد", "success");
        updateTable();
        onClose();
        clearForm();
      } else {
        renderToast(
          response?.farsi_message
            ? response.farsi_message
            : "در ایجاد دسترسی خطایی رخ داده!",
          "err"
        );
      }
    } else {
      renderToast("نام انگلیسی بدون فاصله را وارد کنید", "warn");
    }
  };
  const editPermission = async () => {
    if (englishName) {
      const json = {
        permission_id: permissionId,
        permission_english_name: englishName,
        permission_persian_name: farsiName,
        permission_description: "",
      };
      let response = await reqFunction("Permissions/admin/edit", json);
      if (response.code === 200) {
        renderToast("تغییر دسترسی با موفقیت انجام شد", "success");
        updateTable();
        onClose();
        clearForm();
      } else {
        renderToast(
          response?.farsi_message
            ? response.farsi_message
            : "در اعمال تغییر دسترسی خطایی رخ داده",
          "err"
        );
      }
    } else {
      renderToast("نام انگلیسی بدون فاصله را وارد کنید", "warn");
    }
  };
  return (
    <div className=" flex flex-col space-y-4">
      <InputField
        id="tag-name"
        label="نام فارسی دسترسی"
        placeholder="نام فارسی دسترسی را وارد کنید"
        type="text"
        state={farsiName}
        setState={setFarsiName}
      />
      <InputField
        id="tag-name"
        label="نام انگلیسی دسترسی"
        placeholder="نام انگلیسی دسترسی را وارد کنید"
        type="text"
        // disabled={true}
        state={englishName}
        setState={setEnglishName}
      />
      <div className="form-actions flex flex-row items-center justify-end ">
        <CustomButton onClick={onClose} text="بستن" color="red" />
        <CustomButton
          onClick={() => (isEdit ? editPermission() : addPermission())}
          text={isEdit ? "تغییر" : "ایجاد"}
          color="green"
          extra="!ml-0"
        />
      </div>
    </div>
  );
};
export default PermissionForm;
