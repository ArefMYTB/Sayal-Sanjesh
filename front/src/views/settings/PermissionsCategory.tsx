import Card from "components/card";
import { MdAdd, MdDelete, MdEdit } from "react-icons/md";
import { useDisclosure } from "@chakra-ui/hooks";
import CustomModal from "components/modals";
import CustomButton from "components/button";
import { useQuery } from "@tanstack/react-query";
import { reqFunction } from "utils/API";
import SimpleTable from "components/tables/SimpleTable";
import { toPersianDate } from "utils/TimeUtiles";
import { useState } from "react";

import RoleForm from "components/forms/RoleForm";
import { renderToast } from "utils/globalUtils";

type PermissionCategoryTableData = Array<{
  roleFarsiName: string;
  roleEnglishName: string;
  rolePermissionsNumber: number;
  roleCreateDate: string;
  roleActions: JSX.Element;
}>;
export type PermissionObject = {
  permission_id: string;
  permission_english_name: string;
  permission_persian_name: string;
};
export type PermissionCategory = {
  admin: {
    admin_id: string;
    admin_name: string;
    admin_lastname: string;
    admin_phone: string;
  };
  permission_category_id: string;
  permission_category_persian_name: string;
  permission_category_english_name: string;
  permission_category_description: string;
  permission_category_create_date: string;
  permissions_with_this_category: PermissionObject[];
  permission_numbers_with_this_category: number;
  all_permission_category_numbers: number;
};
const PermissionsCategory = () => {
  const [roleEngName, setRoleEngName] = useState<string>("");
  const [roleFaName, setRoleFaName] = useState<string>("");
  const [roleId, setRoleId] = useState<string>("");
  const [isEdit, setIsEdit] = useState<boolean>(false);
  const [selectedPermissions, setSelectedPermissions] = useState<string[]>([]);
  // const [allPermissions, setAllPermissions] = useState<PermissionObject[]>([]);
  const {
    data: rolesData,
    isLoading: rolesIsLoading,
    status: rolesStatus,
    refetch: rolesRefetch,
  } = useQuery({
    queryFn: () =>
      reqFunction("PermissionCategory/admin/getAll", {
        page: 1,
        count: 10,
        permission_category_english_name: "",
      }),
    queryKey: ["permissionsCategoryList"],
  });

  const {
    isOpen: isRoleOpen,
    onOpen: onRoleOpen,
    onClose: onRoleClose,
  } = useDisclosure();
  const clearForm = () => {
    setRoleEngName("");
    setRoleFaName("");
    setRoleId("");
    setSelectedPermissions([]);
    setIsEdit(false);
  };
  const editRoleClicked = (obj: PermissionCategory) => {
    // //console.log(obj);
    let permisions: string[] = [];
    obj.permissions_with_this_category.forEach((p) =>
      permisions.push(p.permission_id)
    );
    setRoleEngName(obj.permission_category_english_name);
    setRoleFaName(obj.permission_category_persian_name);
    setSelectedPermissions(permisions);
    setRoleId(obj.permission_category_id);
    setIsEdit(true);
    onRoleOpen();
  };
  const addRoleClicked = () => {
    clearForm();
    onRoleOpen();
  };
  const deleteRole = async (roleId: string) => {
    // //console.log(roleId);
    const response = await reqFunction("PermissionCategory/admin/delete", {
      permission_category_id: roleId,
    });
    if (response.code === 200) {
      renderToast("نقش با موفقیت حذف شد.", "success");
      // onDeletConfirmClose();
      rolesRefetch();
    } else {
      renderToast(
        response?.farsi_message
          ? response.farsi_message
          : "در حذف نقش مشکلی رخ داده",
        "err"
      );
    }
  };
  const renderpermissionCategoryActions = (obj: PermissionCategory) => {
    return (
      <div className=" flex items-center justify-center">
        <CustomButton
          onClick={() => editRoleClicked(obj)}
          icon={<MdEdit />}
          color="orange"
          extra="!p-2"
        />
        <CustomButton
          onClick={() => {
            // need to render delete confimation form
            if (window.confirm("آیا از حذف این نقش اطمینان دارید؟")) {
              deleteRole(obj.permission_category_id);
            }
          }}
          icon={<MdDelete />}
          color="red"
          extra="!p-2"
        />
      </div>
    );
  };
  const eventTypeTableHeader = [
    { title: "نام نقش", headerKey: "roleFarsiName" },
    { title: "نام انگلیسی نقش", headerKey: "roleEnglishName" },
    { title: "تعداد دسترسی", headerKey: "rolePermissionsNumber" },
    { title: "تاریخ ایجاد", headerKey: "roleCreateDate" },
    { title: "عملیات", headerKey: "roleActions" },
  ];
  const tableData = () => {
    let permissionCategoryTableData: PermissionCategoryTableData = [];
    if (!rolesIsLoading && rolesStatus === "success") {
      rolesData?.data?.forEach((obj: PermissionCategory) =>
        permissionCategoryTableData.push({
          roleEnglishName: obj.permission_category_english_name,
          roleFarsiName: obj.permission_category_persian_name,
          rolePermissionsNumber: obj.permission_numbers_with_this_category,
          roleCreateDate: toPersianDate(obj.permission_category_create_date),
          roleActions: renderpermissionCategoryActions(obj),
        })
      );
    }
    return permissionCategoryTableData;
  };

  return (
    <div className=" users-table-container">
      <CustomModal
        isOpen={isRoleOpen}
        onClose={onRoleClose}
        title={"نقش دسترسی"}
        modalType="form"
        information={null}
        modalForm={
          <RoleForm
            englishName={roleEngName}
            setEnglishName={setRoleEngName}
            farsiName={roleFaName}
            setFarsiName={setRoleFaName}
            onClose={onRoleClose}
            updateTable={rolesRefetch}
            roleId={roleId}
            selectedPermissions={selectedPermissions}
            setSelectedPermission={setSelectedPermissions}
            // allPermissions={allPermissions}
            isEdit={isEdit}
            clearForm={clearForm}
          />
        }
      />
      <Card extra="border-none h-max">
        <div className="relative flex items-center justify-between p-4">
          <div className="text-xl font-bold text-navy-700 dark:text-white">
            {`نقش های سیستم (${
              rolesIsLoading ? "loading..." : rolesData?.data?.length
            })`}
          </div>
          <div className=" moldal-btns flex items-center justify-end">
            <CustomButton
              text="ایجاد نقش"
              onClick={() => {
                addRoleClicked();
              }}
              icon={<MdAdd />}
              color="green"
              extra="ml-4"
            />
          </div>
        </div>
        <SimpleTable
          header={eventTypeTableHeader}
          data={tableData()}
          hasIndex={true}
          extra="!h-[65vh]"
        />
      </Card>
    </div>
  );
};
export default PermissionsCategory;
