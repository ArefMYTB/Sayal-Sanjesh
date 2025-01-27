import Card from "components/card";
import { MdAdd, MdDelete } from "react-icons/md";
import { useDisclosure } from "@chakra-ui/hooks";
import CustomModal from "components/modals";
import CustomButton from "components/button";
import { useQuery } from "@tanstack/react-query";
import { reqFunction } from "utils/API";
import SimpleTable from "components/tables/SimpleTable";
import { toPersianDate } from "utils/TimeUtiles";
import UserForm from "components/forms/UserForm";
import { useState } from "react";
import { renderToast } from "utils/globalUtils";
import DeleteForm from "components/forms/DeleteForm";

export type UserObject = {
  admin: {
    admin_name: string;
    admin_lastname: string;
    admin_phone: string;
  };
  user_id: string;
  user_name: string;
  user_lastname: string;
  user_phone: string;
  user_create_date: Date;
  All_water_meter_with_this_user_id: number;
  all_users: number;
};
type UserTableData = Array<{
  userName: string;
  userPhone: string;
  userDevicesCount: string;
  userCreateDate: string;
  userCreator: string;
  creatorPhone: string;
  userAction: JSX.Element;
}>;
const UsersTable = () => {
  const AdminPermissions: string[] = JSON.parse(
    window.localStorage.getItem("permissions")
  );
  const [userName, setUserName] = useState<string>("");
  const [userLastName, setUserLastName] = useState<string>("");
  const [userPhoneNumber, setUserPhoneNumber] = useState<string>("");
  const [userInfo, setUserInfo] = useState<UserObject>(null);
  const {
    data: usersData,
    isLoading: usersIsLoading,
    status: usersStatus,
    refetch: usersRefetch,
  } = useQuery({
    queryFn: () =>
      reqFunction("users/admin/getAllUsers", {
        page: 1,
        count: 100,
        user_name: "",
        user_lastname: "",
        user_phone: "",
      }),
    queryKey: ["usersList"],
  });
  const newUsersData = usersData?.data ?? [];
  const {
    isOpen: isUserOpen,
    onOpen: onUsersOpen,
    onClose: onUserClose,
  } = useDisclosure();
  const {
    isOpen: isDeleteConfirmOpen,
    onOpen: onDeleteConfirmOpen,
    onClose: onDeletConfirmClose,
  } = useDisclosure();
  const deleteUserClick = async (id: string) => {
    //console.log(id);
    let user: UserObject[] = newUsersData.filter(
      (userData: UserObject) => userData.user_id === id
    );
    setUserInfo(user.length > 0 ? user[0] : null);
    onDeleteConfirmOpen();
  };
  const deleteUser = async (id: string) => {
    // console.log(id);
    const response = await reqFunction("users/admin/delete", {
      user_id: id,
    });
    if (response.code === 200) {
      renderToast("بهره بردار با موفقیت حذف شد.", "success");
      onDeletConfirmClose();
      usersRefetch();
    } else {
      renderToast(
        response?.farsi_message
          ? response.farsi_message
          : "در حذف بهره بردار مشکلی رخ داده",
        "err"
      );
    }
  };
  const renderUserActions = (userId: string) => {
    return (
      <div className=" flex items-center justify-center">
        {AdminPermissions.includes("UserDelete") ? (
          <CustomButton
            onClick={() => deleteUserClick(userId)}
            icon={<MdDelete />}
            color="red"
            extra="!p-2"
          />
        ) : (
          <></>
        )}
      </div>
    );
  };
  const usersTableHeader = [
    { title: "نام بهره بردار", headerKey: "userName" },
    { title: "شماره تماس", headerKey: "userPhone" },
    { title: "مالکیت دستگاه", headerKey: "userDevicesCount" },
    { title: "تاریخ ثبت نام", headerKey: "userCreateDate" },
    { title: "ثبت کننده", headerKey: "userCreator" },
    { title: "شماره ثبت کننده", headerKey: "creatorPhone" },
    { title: "عملیات", headerKey: "userAction" },
  ];
  const tableData = () => {
    let projectTableData: UserTableData = [];
    if (!usersIsLoading && usersStatus !== "pending" && newUsersData) {
      // //console.log(newUsersData);
      newUsersData.forEach((obj: UserObject) =>
        projectTableData.push({
          userName: `${obj.user_name} ${obj.user_lastname}`,
          userPhone: obj.user_phone,
          userDevicesCount: `${obj.All_water_meter_with_this_user_id} عدد`,
          userCreateDate: toPersianDate(obj.user_create_date),
          userCreator: `${obj.admin.admin_name} ${obj.admin.admin_lastname}`,
          creatorPhone: obj.admin.admin_phone,
          userAction: renderUserActions(obj.user_id),
        })
      );
    }
    return projectTableData;
  };
  return (
    <div className=" users-table-container">
      <CustomModal
        isOpen={isDeleteConfirmOpen}
        onClose={onDeletConfirmClose}
        title={""}
        modalType="form"
        information={null}
        modalForm={
          <DeleteForm
            deleteType="user"
            userDeleted={userInfo}
            onClose={onDeletConfirmClose}
            deleteFunction={deleteUser}
          />
        }
      />
      <CustomModal
        isOpen={isUserOpen}
        onClose={onUserClose}
        title={"بهره بردار"}
        modalType="form"
        information={null}
        modalForm={
          <UserForm
            userName={userName}
            setUserName={setUserName}
            userLastname={userLastName}
            setUserLastname={setUserLastName}
            userPhoneNumber={userPhoneNumber}
            setUserPhoneNumber={setUserPhoneNumber}
            onClose={onUserClose}
            updateTable={usersRefetch}
          />
        }
      />
      <Card extra="border-none h-max">
        <div className="relative flex items-center justify-between p-4">
          <div className="text-xl font-bold text-navy-700 dark:text-white">
            {`بهره برداران (${
              usersIsLoading
                ? "loading..."
                : newUsersData
                ? newUsersData.length
                : 0
            })`}
          </div>
          <div className=" moldal-btns flex items-center justify-end">
            {AdminPermissions.includes("UserCreate") ? (
              <CustomButton
                text="ایجاد بهره بردار"
                onClick={onUsersOpen}
                icon={<MdAdd />}
                color="green"
                extra="ml-4"
              />
            ) : (
              <></>
            )}
          </div>
        </div>
        <SimpleTable
          header={usersTableHeader}
          data={tableData()}
          hasIndex={true}
          extra="!h-[65vh]"
        />
      </Card>
      {/* <div className="pagination my-4 py-4"></div> */}
    </div>
  );
};
export default UsersTable;
