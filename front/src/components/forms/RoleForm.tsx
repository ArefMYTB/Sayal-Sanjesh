import { Checkbox } from "@chakra-ui/react";
import { useQuery } from "@tanstack/react-query";
// import { setSelectionRange } from "@testing-library/user-event/dist/utils";
import CustomButton from "components/button";
import InputField from "components/fields/InputField";
import { reqFunction } from "utils/API";
import { renderToast } from "utils/globalUtils";
import { PermissionObj } from "views/settings/Permissions";
import { PermissionObject } from "views/settings/PermissionsCategory";

interface RoleFormProps {
  englishName: null | string;
  setEnglishName: React.Dispatch<any>;
  farsiName: null | string;
  setFarsiName: React.Dispatch<any>;
  onClose: Function;
  updateTable: any;
  roleId: null | string;
  clearForm: Function;
  selectedPermissions: string[];
  setSelectedPermission: React.Dispatch<any>;
  // allPermissions: PermissionObject[];
  isEdit: boolean;
}
const RoleForm = (props: RoleFormProps) => {
  const {
    englishName,
    setEnglishName,
    farsiName,
    setFarsiName,
    onClose,
    updateTable,
    clearForm,
    roleId,
    selectedPermissions,
    setSelectedPermission,
    isEdit,
  } = props;
  const {
    data: permissionsData,
    isLoading: permissionsIsLoading,
    status: permissionsStatus,
  } = useQuery({
    queryFn: () =>
      reqFunction("Permissions/admin/getAll", {
        page: 1,
        count: 100,
        permission_english_name: "",
      }),
    queryKey: ["permissionsList"],
  });
  const editRole = async () => {
    if (englishName) {
      const json = {
        permission_category_id: roleId,
        permission_category_description: "",
        permission_category_english_name: englishName,
        permission_category_persian_name: farsiName,
        permissions: selectedPermissions,
      };
      let response = await reqFunction("PermissionCategory/admin/edit", json);
      if (response.code === 200) {
        renderToast("تغییر نقش با موفقیت انجام شد", "success");
        updateTable();
        onClose();
        clearForm();
      } else {
        renderToast(
          response?.farsi_message
            ? response.farsi_message
            : "در اعمال تغییر نقش خطایی رخ داده",
          "err"
        );
      }
    } else {
      renderToast("نام انگلیسی بدون فاصله را وارد کنید", "warn");
    }
  };
  const createRole = async () => {
    if (englishName) {
      const json = {
        permission_category_description: "",
        permission_category_english_name: englishName,
        permission_category_persian_name: farsiName,
        permissions: selectedPermissions,
      };
      let response = await reqFunction("PermissionCategory/admin/create", json);
      if (response.code === 200) {
        renderToast("ایجاد نقش با موفقیت انجام شد", "success");
        updateTable();
        onClose();
        clearForm();
      } else {
        renderToast(
          response?.farsi_message
            ? response.farsi_message
            : "در ایجاد نقش خطایی رخ داده",
          "err"
        );
      }
    } else {
      renderToast("نام انگلیسی بدون فاصله را وارد کنید", "warn");
    }
  };
  const pClicked = (permissionId: string) => {
    let selected = [...selectedPermissions];
    selected.includes(permissionId)
      ? setSelectedPermission(selected.filter((d) => d !== permissionId))
      : setSelectedPermission([...selected, permissionId]);
  };
  const renderCheckOptions = (data: PermissionObj[]) => {
    let permissions: PermissionObject[] = [];
    data.forEach((permission: PermissionObj) => {
      permissions.push({
        permission_english_name: permission.permission_english_name,
        permission_persian_name: permission.permission_persian_name,
        permission_id: permission.permission_id,
      });
    });
    return (
      <div className=" grid grid-cols-4 gap-2">
        {permissions.map((p) => (
          <Checkbox
            key={p.permission_id}
            isChecked={selectedPermissions.includes(p.permission_id)}
            onChange={(e) => pClicked(p.permission_id)}
          >
            {p.permission_persian_name
              ? p.permission_persian_name
              : p.permission_english_name}
          </Checkbox>
        ))}
      </div>
    );
  };
  return (
    <div className=" flex flex-col space-y-4">
      <InputField
        id="tag-name"
        label="نام فارسی نقش"
        placeholder="نام فارسی نقش را وارد کنید"
        type="text"
        state={farsiName}
        setState={setFarsiName}
      />
      <InputField
        id="tag-name"
        label="نام انگلیسی نقش"
        placeholder="نام انگلیسی نقش را وارد کنید"
        type="text"
        // disabled={isEdit}
        state={englishName}
        setState={setEnglishName}
      />
      {!permissionsIsLoading && permissionsStatus === "success" ? (
        <>{renderCheckOptions(permissionsData?.data)}</>
      ) : (
        <div> در حال دریافت دسترسی ها !!!</div>
      )}
      <div className="form-actions flex flex-row items-center justify-end ">
        <CustomButton onClick={onClose} text="بستن" color="red" />
        <CustomButton
          onClick={() => (isEdit ? editRole() : createRole())}
          text={isEdit ? "تغییر" : "ایجاد"}
          color="green"
          extra="!ml-0"
        />
      </div>
    </div>
  );
};
export default RoleForm;
