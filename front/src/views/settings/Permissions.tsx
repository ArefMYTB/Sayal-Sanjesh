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
import PermissionForm from "components/forms/PermissionFrom";
import { renderToast } from "utils/globalUtils";

type PermissionTableData = Array<{
  permissionName: string;
  permissionEnglishName: string;
  rolesWithPermission: number;
  permissionCreateDate: string;
  permissionActions: JSX.Element;
}>;
type PCObj = {
  permission_category_id: string;
  permission_category_english_name: string;
  permission_category_persian_name: string;
};
export type PermissionObj = {
  admin: {
    admin_id: string;
    admin_name: string;
    admin_lastname: string;
    admin_phone: string;
  };
  permission_id: string;
  permission_persian_name: string;
  permission_english_name: string;
  permission_description: string;
  permission_create_date: string;
  category_with_this_permission: PCObj[];
  category_numbers_with_this_category: number;
  all_permissions_number: number;
};
const Permissions = () => {
  const [permissionEngName, setPermissionEngName] = useState<string>("");
  const [permissionFarsiName, setPermissionFarsiName] = useState<string>("");
  const [permissionId, setPermissionId] = useState<string>("");
  const [isEdit, setIsEdit] = useState<boolean>(false);
  const {
    data: permissionsData,
    isLoading: permissionsIsLoading,
    status: permissionsStatus,
    refetch: permissionsRefetch,
  } = useQuery({
    queryFn: () =>
      reqFunction("Permissions/admin/getAll", {
        page: 1,
        count: 100,
        permission_english_name: "",
      }),
    queryKey: ["permissionsList"],
  });

  const {
    isOpen: isPermissionOpen,
    onOpen: onPermissionOpen,
    onClose: onPermissionClose,
  } = useDisclosure();
  const clearForm = () => {
    setPermissionEngName("");
    setPermissionFarsiName("");
    setPermissionId("");
    setIsEdit(false);
  };
  const addPermissionClick = () => {
    clearForm();
    onPermissionOpen();
  };
  const editPermissionClick = (permission: PermissionObj) => {
    setIsEdit(true);
    setPermissionEngName(permission.permission_english_name);
    setPermissionFarsiName(permission.permission_persian_name);
    setPermissionId(permission.permission_id);
    onPermissionOpen();
  };
  const deletePermissionClick = async (permission: PermissionObj) => {
    //console.log(permission);
    const response = await reqFunction("Permissions/admin/delete", {
      permission_id: permission.permission_id,
    });
    if (response.code === 200) {
      renderToast("دسترسی با موفقیت حذف شد.", "success");
      permissionsRefetch();
    } else {
      renderToast(
        response?.farsi_message
          ? response.farsi_message
          : "در حذف دسترسی مشکلی رخ داده",
        "err"
      );
    }
  };
  const renderPermissionActions = (permission: PermissionObj) => {
    return (
      <div className=" flex items-center justify-center">
        <CustomButton
          onClick={() => editPermissionClick(permission)}
          icon={<MdEdit />}
          color="orange"
          extra="!p-2"
        />
        <CustomButton
          onClick={() => {
            if (window.confirm("آیا از حذف این نوع دسترسی اطمینان دارید؟")) {
              deletePermissionClick(permission)
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
    { title: "نام فارسی دسترسی", headerKey: "permissionName" },
    { title: "نام انگلیسی", headerKey: "permissionEnglishName" },
    { title: "نقش ها با این دسترسی", headerKey: "rolesWithPermission" },
    { title: "تاریخ ایجاد", headerKey: "permissionCreateDate" },
    { title: "عملیات", headerKey: "permissionActions" },
  ];
  const tableData = () => {
    let permissionTableData: PermissionTableData = [];
    if (!permissionsIsLoading && permissionsStatus === "success") {
      permissionsData.data.forEach((obj: PermissionObj) =>
        permissionTableData.push({
          permissionName: obj.permission_persian_name,
          permissionEnglishName: obj.permission_english_name,
          rolesWithPermission: obj.category_numbers_with_this_category,
          permissionCreateDate: toPersianDate(obj.permission_create_date),
          permissionActions: renderPermissionActions(obj),
        })
      );
    }
    return permissionTableData;
  };
  return (
    <div className=" users-table-container">
      <CustomModal
        isOpen={isPermissionOpen}
        onClose={onPermissionClose}
        title={"دسترسی"}
        modalType="form"
        information={null}
        modalForm={
          <PermissionForm
            englishName={permissionEngName}
            setEnglishName={setPermissionEngName}
            farsiName={permissionFarsiName}
            setFarsiName={setPermissionFarsiName}
            onClose={onPermissionClose}
            updateTable={permissionsRefetch}
            permissionId={permissionId}
            clearForm={clearForm}
            isEdit={isEdit}
          />
        }
      />
      <Card extra="border-none h-max">
        <div className="relative flex items-center justify-between p-4">
          <div className="text-xl font-bold text-navy-700 dark:text-white">
            {`دسترسی ها (${
              permissionsIsLoading ? "loading..." : permissionsData?.data.length
            })`}
          </div>
          <div className=" moldal-btns flex items-center justify-end">
            <CustomButton
              text="ایجاد دسترسی"
              onClick={() => addPermissionClick()}
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
export default Permissions;
