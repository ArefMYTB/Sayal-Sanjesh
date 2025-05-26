import { Checkbox } from "@chakra-ui/react";
import { useQuery } from "@tanstack/react-query";
import CustomButton from "components/button";
import InputField from "components/fields/InputField";
import SelectInput, { DynamicOption } from "components/fields/SelectInput";
import { useState } from "react";
import { reqFunction } from "utils/API";
import { isPhoneValid, renderToast } from "utils/globalUtils";
// import { PermissionObj } from "views/settings/Permissions";
import { PermissionObject } from "views/settings/PermissionsCategory";

interface AdminFormProps {
  adminName: null | string;
  setAdminName: React.Dispatch<any>;
  adminLastname: null | string;
  setAdminLastname: React.Dispatch<any>;
  adminPhoneNumber: null | string;
  setAdminPhoneNumber: React.Dispatch<any>;
  adminPassword: null | string;
  setAdminPassword: React.Dispatch<any>;
  adminPermissions: string[];
  setAdminPermissions: React.Dispatch<any>;
  selectedPermissions: string[];
  setSelectedPermissions: React.Dispatch<any>;
  adminId: null | string;
  setAdminId: React.Dispatch<any>;
  roleOptions: DynamicOption[];
  role: DynamicOption;
  setRole: React.Dispatch<any>;
  defaultPermissions: string[];
  isEditForm: boolean;
  clearForm: Function;
  setIsEditForm: React.Dispatch<any>;
  onClose: Function;
  updateTable: any;
}
export type AdminObject = {
  admin_name: null | string;
  admin_phone?: null | string;
  admin_lastname: null | string;
  admin_password?: null | string;
  admin_permissions: string[];
  other_information: {};
  other_admin_id?: string;
};
const AdminForm = (props: AdminFormProps) => {
  const [phoneBorder, setPhoneBorder] = useState<
    "err" | "success" | "dis" | "normal"
  >("normal");
  const {
    adminName,
    setAdminName,
    adminLastname,
    setAdminLastname,
    adminPhoneNumber,
    setAdminPhoneNumber,
    adminPassword,
    setAdminPassword,
    // adminPermissions,
    // setAdminPermissions,
    roleOptions,
    role,
    setRole,
    selectedPermissions,
    setSelectedPermissions,
    clearForm,
    adminId,
    // setAdminId,
    isEditForm,
    // setIsEditForm,
    defaultPermissions,
    onClose,
    updateTable,
  } = props;
  const {
    data: rolesData,
    isLoading: rolesIsLoading,
    status: rolesStatus,
    // refetch: rolesRefetch,
  } = useQuery({
    queryFn: () =>
      reqFunction("PermissionCategory/admin/getAll", {
        page: 1,
        count: 10,
        permission_category_english_name: role.value,
      }),
    queryKey: ["rolePermissionList", role],
  });
  const ADMINPERMISSIONS: string[] = JSON.parse(
    window.localStorage.getItem("permissions")
  );
  const createAdmin = async () => {
    if (
      adminName &&
      adminLastname &&
      adminPhoneNumber &&
      adminPassword &&
      role
    ) {
      let aPermissions = [
        ...selectedPermissions,
        ...defaultPermissions,
        role.value === "Admin" ? "Admin" : "ProjectManager",
      ];
      let uniqPermissions = aPermissions.filter(
        (value, index) => aPermissions.indexOf(value) === index
      );
      if (isPhoneValid(adminPhoneNumber)) {
        const json: AdminObject = {
          admin_name: adminName,
          admin_phone: adminPhoneNumber,
          admin_lastname: adminLastname,
          admin_password: adminPassword,
          admin_permissions: uniqPermissions,
          other_information: {},
        };
        const data = new FormData();
        data.append("data", JSON.stringify(json));
        let response = await reqFunction("admins/admin/add", data);
        if (response.code === 200) {
          renderToast("ایجاد مدیر با موفقیت انجام شد", "success");
          updateTable();
          onClose();
          clearForm();
        } else {
          renderToast(
            response?.farsi_message
              ? response.farsi_message
              : "در ایجاد مدیر خطایی رخ داده",
            "err"
          );
        }
      } else {
        renderToast("شماره تماس 11 رقم بوده و با 0 شروع میگردد", "warn");
        setPhoneBorder("err");
      }
    } else {
      renderToast("تمامی موارد را وارد کنید", "warn");
    }
  };
  const editAdmin = async () => {
    let aPermissions = [
      ...selectedPermissions,
      ...defaultPermissions,
      role.value === "Admin" ? "Admin" : "ProjectManager",
    ];
    let uniqPermissions = aPermissions.filter(
      (value, index) => aPermissions.indexOf(value) === index
    );
    if (adminName && adminLastname && adminPhoneNumber) {
      if (isPhoneValid(adminPhoneNumber)) {
        const json: AdminObject = {
          other_admin_id: adminId,
          admin_name: adminName,
          admin_lastname: adminLastname,
          admin_permissions: uniqPermissions,
          other_information: {},
        };
        const data = new FormData();
        data.append("data", JSON.stringify(json));
        let response = await reqFunction("admins/admin/edit", data);
        if (response.code === 200) {
          renderToast("تغییر مدیر با موفقیت انجام شد", "success");
          updateTable();
          onClose();
          clearForm();
        } else {
          renderToast(
            response?.farsi_message
              ? response.farsi_message
              : "در تغییر مدیر خطایی رخ داده",
            "err"
          );
        }
      } else {
        renderToast("شماره تماس 11 رقم بوده و با 0 شروع میگردد", "warn");
        setPhoneBorder("err");
      }
    } else {
      renderToast("تمامی موارد را وارد کنید", "warn");
    }
  };
  const pClicked = (permissionEngName: string) => {
    let selected = [...selectedPermissions];
    selected.includes(permissionEngName)
      ? setSelectedPermissions(selected.filter((d) => d !== permissionEngName))
      : setSelectedPermissions([...selected, permissionEngName]);
  };
  const renderRolePermissions = () => {
    let rolePermissions: PermissionObject[] =
      Array.isArray(rolesData?.data) && rolesData.data.length > 0
        ? rolesData.data[0].permissions_with_this_category
        : [];
    let modifiedPermissions: PermissionObject[] = [];
    if (rolePermissions) {
      rolePermissions.forEach((p) => {
        if (ADMINPERMISSIONS.includes(p.permission_english_name)) {
          modifiedPermissions.push(p);
        }
      });
    }
    return (
      <div className=" grid grid-cols-4 gap-2">
        {rolePermissions
          ? modifiedPermissions
              .filter(
                (permissions) =>
                  permissions.permission_english_name !== "Admin" &&
                  permissions.permission_english_name !== "ProjectManager" &&
                  !defaultPermissions.includes(
                    permissions.permission_english_name
                  )
              )
              .map((p) => (
                <Checkbox
                  key={p.permission_id}
                  isChecked={selectedPermissions.includes(
                    p.permission_english_name
                  )}
                  onChange={(e) => pClicked(p.permission_english_name)}
                >
                  {p.permission_persian_name
                    ? p.permission_persian_name
                    : p.permission_english_name}
                </Checkbox>
              ))
          : ""}
      </div>
    );
  };
  return (
    <div className=" flex flex-col space-y-4">
      <InputField
        id="admin-name"
        label="نام کاربر"
        placeholder="نام مدیر را وارد کنید"
        type="text"
        state={adminName}
        setState={setAdminName}
      />
      <InputField
        id="admin-last-name"
        label="نام خانوادگی مدیر"
        placeholder="نام خانوادگی مدیر را وارد کنید"
        type="text"
        state={adminLastname}
        setState={setAdminLastname}
      />
      <InputField
        id="admin-mobile"
        label="شماره موبایل"
        placeholder="شماره موبایل را وارد کنید"
        type="text"
        disabled={isEditForm}
        state={adminPhoneNumber}
        setState={setAdminPhoneNumber}
        border={phoneBorder}
      />
      <InputField
        id="admin-mobile"
        label="رمز عبور"
        placeholder="رمز عبور را وارد کنید"
        type="text"
        state={adminPassword}
        setState={setAdminPassword}
        extra={`${isEditForm ? "hidden" : null}`}
        // border={phoneBorder}
      />
      <SelectInput
        label="نقش مدیر"
        dynamicOptions={roleOptions}
        state={role}
        placeholder="نقش را انتخاب کنید"
        setState={setRole}
        isMandatory={true}
      />
      {!rolesIsLoading && rolesStatus === "success" && role ? (
        renderRolePermissions()
      ) : (
        <></>
      )}
      <div className="form-actions flex flex-row items-center justify-end ">
        <CustomButton onClick={onClose} text="بستن" color="red" />
        <CustomButton
          onClick={() => (isEditForm ? editAdmin() : createAdmin())}
          text={`${isEditForm ? "تغییر" : "ایجاد"}`}
          color="green"
          extra="!ml-0"
        />
      </div>
    </div>
  );
};
export default AdminForm;
