import Card from "components/card";
import { MdAdd, MdAddCircleOutline, MdDelete, MdEdit } from "react-icons/md";
import { RiUserForbidFill } from "react-icons/ri";
import { useDisclosure } from "@chakra-ui/hooks";
import CustomModal from "components/modals";
import CustomButton from "components/button";
import { useQuery } from "@tanstack/react-query";
import { reqFunction } from "utils/API";
import SimpleTable from "components/tables/SimpleTable";
import { toPersianDate } from "utils/TimeUtiles";
import AdminForm from "components/forms/AdminForm";
import SuspendAdminForm from "components/forms/AdminSuspendForm";
import { useState } from "react";
import { DynamicOption } from "components/fields/SelectInput";
import { PermissionCategory } from "views/settings/PermissionsCategory";
import AssignProjectForm, {
  ProjectManagers,
} from "components/forms/AssignProjectForm";
import { ProjectObject } from "views/projects";
import { renderToast } from "utils/globalUtils";
import DeleteForm from "components/forms/DeleteForm";

export type AdminsObject = {
  admin_id: string;
  admin_name: string;
  admin_lastname: string;
  admin_phone: string;
  admin_create_date: Date;
  admin_permissions: string[];
  lockout_until: string;
};
type AdminTableData = Array<{
  adminName: string;
  adminPhone: string;
  adminCreateDate: string;
  adminPermissions: string;
  assignProject: JSX.Element;
  adminAction: JSX.Element;
}>;
const AdminsTable = () => {
  const ADMINPERMISSIONS: string[] = JSON.parse(
    window.localStorage.getItem("permissions")
  );
  const [adminName, setAdminName] = useState<string>("");
  const [adminLastname, setAdminLastname] = useState<string>("");
  const [adminPhoneNumber, setAdminPhoneNumber] = useState<string>("");
  const [adminPermissions, setAdminPermissions] = useState<string[]>([]);
  const [selectedPermissions, setSelectedPermissions] = useState<string[]>([]);
  const [adminPassword, setAdminPassword] = useState<string>("");
  const [role, setRole] = useState<DynamicOption>(null);
  const [adminId, setAdminId] = useState<string>("");
  const [isEditForm, setIsEditForm] = useState<boolean>(false);
  const [middleProjectIds, setMiddleProjectIds] = useState<string[]>([]);
  const [adminInfo, setAdminInfo] = useState<AdminsObject>(null);
  const [lockoutUntil, setLockoutUntil] = useState<string | null>(null);

  const {
    data: adminsData,
    isLoading: adminsIsLoading,
    status: adminsStatus,
    refetch: adminsRefetch,
  } = useQuery({
    queryFn: () =>
      reqFunction("admins/admin/getAll", {
        admin_name: "",
        admin_phone: "",
        admin_lastname: "",
      }),
    queryKey: ["adminsList"],
  });
  const {
    data: middlesProject,
    isLoading: middlesProjectIsLoading,
    status: middlesProjectStatus,
    refetch: middlesProjectRefetch,
  } = useQuery({
    queryFn: () => reqFunction("middle/admin/getAll", {}, "get"),
    queryKey: ["middlesProjectList"],
  });
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
        permission_category_english_name: "",
      }),
    queryKey: ["permissionsCategoryList"],
  });
  const {
    data: projectsData,
    isLoading: projectsIsLoading,
    status: projectStatus,
  } = useQuery({
    queryFn: () =>
      reqFunction("WaterMeterProjectsURL/admin/getAll", {
        page: 1,
        count: 100,
        water_meter_project_name: null,
        water_meter_project_create_date: null,
        user_id: null,
      }),
    queryKey: ["projectList"],
  });
  // Edit
  const {
    isOpen: isAdminOpen,
    onOpen: onAdminOpen,
    onClose: onAdminClose,
  } = useDisclosure();
  const {
    isOpen: isAdminSuspendOpen,
    onOpen: onAdminSuspendOpen,
    onClose: onAdminSuspendClose,
  } = useDisclosure();
  const {
    isOpen: isAssignProjectOpen,
    onOpen: onAssignProjectOpen,
    onClose: onAssignProjectClose,
  } = useDisclosure();
  const {
    isOpen: isDeleteConfirmOpen,
    onOpen: onDeleteConfirmOpen,
    onClose: onDeletConfirmClose,
  } = useDisclosure();
  const clearData = () => {
    setAdminName("");
    setAdminLastname("");
    setAdminPhoneNumber("");
    setAdminPermissions([]);
    setSelectedPermissions([]);
    setRole(null);
    setAdminPassword("");
    setAdminId("");
    setIsEditForm(false);
  };
  const addAdminClicked = (data: PermissionCategory[]) => {
    onAdminOpen();
    clearData();
  };
  const renderOptions = (data: PermissionCategory[]) => {
    let options: DynamicOption[] = [];

    data?.forEach((d) => {
      const isDefault =
        d.permission_category_english_name === "DefaultPermissions";
      const isAdminExcluded =
        d.permission_category_english_name === "Admin" &&
        ADMINPERMISSIONS.includes("ProjectManager");

      if (!isDefault && !isAdminExcluded) {
        options.push({
          label: d.permission_category_persian_name,
          value: d.permission_category_english_name,
        });
      }
    });

    return options;
  };

  const editAdminClick = (id: string) => {
    let selectedAdmin: AdminsObject[] = adminsData.data.filter(
      (admin: AdminsObject) => id === admin.admin_id
    );
    setIsEditForm(true);
    setAdminId(selectedAdmin[0].admin_id);
    setAdminName(selectedAdmin[0].admin_name);
    setAdminLastname(selectedAdmin[0].admin_lastname);
    setAdminPhoneNumber(selectedAdmin[0].admin_phone);
    selectedAdmin[0].admin_permissions.includes("Admin")
      ? setRole({
          label: "مدیر سیستم",
          value: "Admin",
        })
      : setRole({
          label: "مدیر پروژه",
          value: "ProjectManager",
        });
    setSelectedPermissions(selectedAdmin[0].admin_permissions);
    onAdminOpen();
  };
  const suspendAdminClick = (id: string) => {
    let selectedAdmin: AdminsObject[] = adminsData.data.filter(
      (admin: AdminsObject) => id === admin.admin_id
    );
    setAdminId(selectedAdmin[0].admin_id);
    setAdminName(selectedAdmin[0].admin_name);
    setAdminLastname(selectedAdmin[0].admin_lastname);
    setAdminPhoneNumber(selectedAdmin[0].admin_phone);
    setLockoutUntil(selectedAdmin[0].lockout_until);
    onAdminSuspendOpen();
  };
  const deleteAdminClick = (id: string) => {
    let admin: AdminsObject[] = adminsData.data.filter(
      (adminData: AdminsObject) => adminData.admin_id === id
    );
    setAdminInfo(admin.length > 0 ? admin[0] : null);
    onDeleteConfirmOpen();
  };
  const deleteAdmin = async (id: string) => {
    // console.log(id);
    const response = await reqFunction("admins/admin/remove", {
      other_admin_id: id,
    });
    if (response.code === 200) {
      renderToast("کاربر سیستم با موفقیت حذف شد.", "success");
      onDeletConfirmClose();
      adminsRefetch();
    } else {
      renderToast(
        response?.farsi_message
          ? response.farsi_message
          : "در حذف کاربر سیستم مشکلی رخ داده",
        "err"
      );
    }
  };
  const renderAdminActions = (admin: AdminsObject) => {
    const isSuspended = admin.lockout_until !== null;
    return (
      <div className=" flex items-center justify-center">
        {ADMINPERMISSIONS.includes("CRUDAdmin") ||
        ADMINPERMISSIONS.includes("CRUDManager") ? (
          <div className="flex">
            <CustomButton
              onClick={() => editAdminClick(admin.admin_id)}
              icon={<MdEdit />}
              color="orange"
              extra="!p-2"
            />
            <CustomButton
              onClick={() => suspendAdminClick(admin.admin_id)}
              icon={<RiUserForbidFill />}
              color={isSuspended ? "blue" : "yellow"}
              extra="!p-2"
            />
            <CustomButton
              onClick={() => {
                deleteAdminClick(admin.admin_id);
              }}
              icon={<MdDelete />}
              color="red"
              extra="!p-2"
            />
          </div>
        ) : (
          <></>
        )}
      </div>
    );
  };
  const assignProjectClicked = (obj: AdminsObject) => {
    setAdminId(obj.admin_id);
    let projects = middlesProject?.data ? middlesProject.data : [];
    let selectedMiddle = projects.filter(
      (admin: ProjectManagers) => admin.admin_id === obj.admin_id
    );
    let ProjectManagerProjectIds: string[] = [];
    if (selectedMiddle.length > 0) {
      selectedMiddle[0].middel_admin_projects.forEach((p: ProjectObject) =>
        ProjectManagerProjectIds.push(p.water_meter_project_id)
      );
    }
    setMiddleProjectIds(ProjectManagerProjectIds);
    onAssignProjectOpen();
  };
  const renderAssignBtn = (obj: AdminsObject) => {
    return (
      <div className=" flex items-center justify-center">
        <CustomButton
          onClick={() => assignProjectClicked(obj)}
          icon={<MdAddCircleOutline />}
          color="green"
          extra="!p-2"
          isDisabled={obj.admin_permissions.includes("Admin")}
        />
      </div>
    );
  };
  const adminsTableHeader =
    ADMINPERMISSIONS.includes("CRUDManager") ||
    ADMINPERMISSIONS.includes("CRUDAdmin")
      ? [
          { title: "نام کاربر سیستم", headerKey: "adminName" },
          { title: "شماره تماس", headerKey: "adminPhone" },
          { title: "تاریخ عضویت", headerKey: "adminCreateDate" },
          { title: "نقش کاربر سیستم", headerKey: "adminPermissions" },
          { title: "افزودن پروژه", headerKey: "assignProject" },
          { title: "عملیات", headerKey: "adminAction" },
        ]
      : [
          { title: "نام کاربر سیستم", headerKey: "adminName" },
          { title: "شماره تماس", headerKey: "adminPhone" },
          { title: "تاریخ عضویت", headerKey: "adminCreateDate" },
          { title: "نقش کاربر سیستم", headerKey: "adminPermissions" },
          { title: "عملیات", headerKey: "adminAction" },
        ];
  const renderProjectSelect = (data: ProjectObject[]) => {
    let projectOptions: DynamicOption[] = [];
    data?.forEach((project) =>
      projectOptions.push({
        label: project.water_meter_project_name,
        value: project.water_meter_project_id,
      })
    );
    return projectOptions;
  };
  const tableData = () => {
    let projectTableData: AdminTableData = [];
    if (!adminsIsLoading && adminsStatus !== "pending") {
      adminsData.data?.forEach((obj: AdminsObject) =>
        projectTableData.push({
          adminName: `${obj.admin_name} ${obj.admin_lastname}`,
          adminPhone: obj.admin_phone,
          adminCreateDate: toPersianDate(obj.admin_create_date),
          adminPermissions: obj.admin_permissions.includes("Admin")
            ? "مدیر سیستم"
            : "مدیر پروژه",
          assignProject: renderAssignBtn(obj),
          adminAction: renderAdminActions(obj),
        })
      );
    }
    return projectTableData;
  };
  const renderDefault = (categories: PermissionCategory[] | undefined) => {
    if (!categories) return [];

    const defaultCategory = categories.find(
      (c) => c.permission_category_english_name === "DefaultPermissions"
    );

    return (
      defaultCategory?.permissions_with_this_category?.map(
        (p) => p.permission_english_name
      ) ?? []
    );
  };

  return (
    <>
      {!rolesIsLoading &&
      rolesStatus === "success" &&
      !projectsIsLoading &&
      projectStatus === "success" &&
      !middlesProjectIsLoading &&
      middlesProjectStatus === "success" ? (
        <div className=" users-table-container">
          <CustomModal
            isOpen={isDeleteConfirmOpen}
            onClose={onDeletConfirmClose}
            title={""}
            modalType="form"
            information={null}
            modalForm={
              <DeleteForm
                deleteType="admin"
                adminDeleted={adminInfo}
                onClose={onDeletConfirmClose}
                deleteFunction={deleteAdmin}
              />
            }
          />
          <CustomModal
            isOpen={isAssignProjectOpen}
            onClose={onAssignProjectClose}
            title={"دسترسی پروژه"}
            modalType="form"
            information={null}
            modalForm={
              <AssignProjectForm
                onClose={onAssignProjectClose}
                projectSelectData={renderProjectSelect(projectsData.data)}
                middleId={adminId}
                ProjectManagers={middlesProject?.data}
                middleProjectRefetch={middlesProjectRefetch}
                middleProjectIds={middleProjectIds}
              />
            }
          />
          {/* Edit Admin */}
          <CustomModal
            isOpen={isAdminOpen}
            onClose={onAdminClose}
            title={"کاربر سیستم"}
            modalType="form"
            information={null}
            modalForm={
              <AdminForm
                adminName={adminName}
                setAdminName={setAdminName}
                adminLastname={adminLastname}
                setAdminLastname={setAdminLastname}
                adminPhoneNumber={adminPhoneNumber}
                setAdminPhoneNumber={setAdminPhoneNumber}
                adminPassword={adminPassword}
                setAdminPassword={setAdminPassword}
                adminPermissions={adminPermissions}
                setAdminPermissions={setAdminPermissions}
                adminId={adminId}
                setAdminId={setAdminId}
                isEditForm={isEditForm}
                roleOptions={
                  !rolesIsLoading && rolesStatus === "success"
                    ? renderOptions(rolesData?.data)
                    : []
                }
                role={role}
                setRole={setRole}
                defaultPermissions={
                  rolesData?.data ? renderDefault(rolesData.data) : []
                }
                selectedPermissions={selectedPermissions}
                setSelectedPermissions={setSelectedPermissions}
                setIsEditForm={setIsEditForm}
                onClose={onAdminClose}
                clearForm={clearData}
                updateTable={adminsRefetch}
              />
            }
          />
          {/* Suspend Admin */}
          <CustomModal
            isOpen={isAdminSuspendOpen}
            onClose={onAdminSuspendClose}
            title={"کاربر سیستم"}
            modalType="form"
            information={null}
            modalForm={
              <SuspendAdminForm
                adminName={adminName}
                adminLastname={adminLastname}
                adminPhoneNumber={adminPhoneNumber}
                adminId={adminId}
                setAdminId={setAdminId}
                lockoutUntil={lockoutUntil}
                onClose={onAdminSuspendClose}
                clearForm={clearData}
                updateTable={adminsRefetch}
              />
            }
          />
          <Card extra="border-none h-max">
            <div className="relative flex items-center justify-between p-4">
              <div className="text-xl font-bold text-navy-700 dark:text-white">
                {`کاربران سیستم (${
                  adminsIsLoading ? "loading..." : adminsData?.data?.length
                })`}
              </div>
              <div className=" moldal-btns flex items-center justify-end">
                {(!rolesIsLoading &&
                  rolesStatus === "success" &&
                  ADMINPERMISSIONS.includes("CRUDAdmin")) ||
                ADMINPERMISSIONS.includes("CRUDManager") ? (
                  <CustomButton
                    text="ایجاد کاربر سیستم"
                    onClick={() => addAdminClicked(rolesData.data)}
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
              header={adminsTableHeader}
              data={tableData()}
              hasIndex={true}
              extra="!h-[65vh]"
            />
          </Card>
        </div>
      ) : (
        <></>
      )}
    </>
  );
};
export default AdminsTable;
