import Card from "components/card";
import {
  MdAdd,
  MdDelete,
  MdEdit,
  // MdFilterAlt,
  MdRemoveRedEye,
} from "react-icons/md";
import { useDisclosure } from "@chakra-ui/hooks";

import CustomModal from "components/modals";
import CustomButton from "components/button";
import { useQuery } from "@tanstack/react-query";
import { reqFunction } from "utils/API";
import SimpleTable from "components/tables/SimpleTable";
import { toPersianDate } from "utils/TimeUtiles";
import ProjectForm from "components/forms/ProjectForm";
import { TypeObject } from "views/settings/DeviceTypesTable";
import { Image } from "@chakra-ui/react";
import NoImage from "../../assets/img/avatars/no-image-icon.png";
import { TagObject } from "views/counters";
import { renderToast } from "utils/globalUtils";
import { useState } from "react";
import DeleteForm from "components/forms/DeleteForm";
import CustomPagination from "components/pagination";
import { CountOption, countSelect } from "variables";
import { Link } from "react-router-dom";
import { decryptData } from "utils/Decryption";
// import RabbitMqComponent from "components/rabbitMq";
// import RabbitMQSubscriber from "components/rabbitMq/RabbitMQSubscriber";

export type ProjectObject = {
  all_project_numbers?: number;
  water_meter_project_name?: string;
  water_meter_project_title?: string;
  water_meter_project_start_date?: Date;
  water_meter_project_employer_description?: {
    name: string;
    lastName: string;
    phoneNumber: string;
  };
  water_meter_project_images?: string[];
  project_meters_per_tag?: TagObject[];
  water_meter_project_other_information?: { description?: string };
  water_meter_project_contract_number?: string;
  types?: TypeObject[];
  water_meter_project_urls?: {
    gallery: string[];
    logo: string;
  };
  water_meters_with_this_id?: { All_water_meter_with_this_id: string };
  water_meter_project_id?: string;
};
type ProjectTableData = Array<{
  projectLogo: JSX.Element;
  projectName: JSX.Element;
  projectCity: string;
  projectStartDate: string;
  projectManager: string;
  projectDevices: string;
  projectActions: JSX.Element;
}>;
const ProjectsView = () => {
  const AdminPermissions: string[] = JSON.parse(
    window.localStorage.getItem("permissions")
  );
  const [isEditForm, setEditForm] = useState<boolean>(false);
  const [projectInfo, setProjectinfo] = useState({});
  const [page, setPage] = useState<number>(1);
  const [count, setCount] = useState<CountOption>(countSelect[0]);
  const { data, isLoading, status, refetch } = useQuery({
    queryFn: () =>
      reqFunction("WaterMeterProjectsURL/admin/getAll", {
        page: page,
        count: count.value,
        water_meter_project_name: null,
        water_meter_project_create_date: null,
        user_id: null,
      }),
    queryKey: ["projectList", page, count],
  });
  // console.log("initial data not encoded : ", data?.data);
  // console.log("coded data :", data?.test_data);
  // console.log(
  //   "data after decode :",
  //   decryptData(data.test_data, "f675e6d9e84f419ba71b87a1fb57dfd5")
  // );
  const projectData = data?.data ?? [];
  const {
    isOpen: isProjectOpen,
    onOpen: onProjectOpen,
    onClose: onProjectClose,
  } = useDisclosure();
  const {
    isOpen: isDeleteConfirmOpen,
    onOpen: onDeleteConfirmOpen,
    onClose: onDeletConfirmClose,
  } = useDisclosure();
  const addProjectClick = () => {
    setEditForm(false);
    setProjectinfo({});
    onProjectOpen();
  };
  const editProjectClick = (id: string) => {
    setEditForm(true);
    let project = projectData.filter(
      (project: ProjectObject) => project.water_meter_project_id === id
    );
    setProjectinfo(project[0]);
    onProjectOpen();
  };
  const deleteProjectClicked = (id: string) => {
    let project = projectData.filter(
      (project: ProjectObject) => project.water_meter_project_id === id
    );
    setProjectinfo(project[0]);
    onDeleteConfirmOpen();
  };
  const deleteProject = async (id: string) => {
    const response = await reqFunction("WaterMeterProjectsURL/admin/delete", {
      water_meter_project_id: id,
    });
    if (response.code === 200) {
      renderToast("پروژه با موفقیت حذف شد.", "success");
      onDeletConfirmClose();
      refetch();
    } else {
      renderToast(
        response?.farsi_message
          ? response.farsi_message
          : "در حذف پروژه مشکلی رخ داده",
        "err"
      );
    }
  };
  const renderProjectName = (name: string, projectId: string) => {
    return (
      <>
        {AdminPermissions.includes("ViewProject") ? (
          <Link to={`/admin/projects/${projectId}`} rel="noopener noreferrer">
            <span>{name}</span>
          </Link>
        ) : (
          <span>{name}</span>
        )}
      </>
    );
  };
  const renderProjectLogo = (logo: string, projectId: string) => {
    return (
      <>
        {AdminPermissions.includes("ViewProject") ? (
          <Link to={`/admin/projects/${projectId}`} rel="noopener noreferrer">
            <div className="mr-9 flex h-16 w-16 items-center justify-center overflow-hidden rounded-full bg-white">
              <Image
                src={
                  !logo
                    ? NoImage
                    : `${process.env.REACT_APP_SAYAL_API_ENDPOINT_MAIN}${logo}`
                }
                // borderRadius=""
                boxSize="70px"
                alt="here"
              />
            </div>
          </Link>
        ) : (
          <div className="mr-9 flex h-16 w-16 items-center justify-center overflow-hidden rounded-full bg-white">
            <Image
              src={
                !logo
                  ? NoImage
                  : `${process.env.REACT_APP_SAYAL_API_ENDPOINT_MAIN}${logo}`
              }
              // borderRadius=""
              boxSize="70px"
              alt="here"
            />
          </div>
        )}
      </>
    );
  };
  const renderProjectActions = (projectId: string) => {
    return (
      <div className=" flex items-center justify-center">
        {AdminPermissions.includes("ViewProject") ? (
          <Link to={`/admin/projects/${projectId}`} rel="noopener noreferrer">
            <CustomButton
              // onClick={() => routeChange(projectId)}
              onClick={null}
              icon={<MdRemoveRedEye />}
              color="blue"
              extra="!p-2"
            />
          </Link>
        ) : (
          <></>
        )}
        {AdminPermissions.includes("Admin") ? (
          <CustomButton
            onClick={() => editProjectClick(projectId)}
            icon={<MdEdit />}
            color="orange"
            extra="!p-2"
          />
        ) : (
          <></>
        )}
        {AdminPermissions.includes("Admin") ? (
          <CustomButton
            onClick={() => {
              deleteProjectClicked(projectId);
            }}
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
  const projectTableHeader = AdminPermissions.includes("ViewProject")
    ? [
        { title: "تصویر پروژه", headerKey: "projectLogo" },
        { title: "نام پروژه", headerKey: "projectName" },
        { title: "شهر محل انجام", headerKey: "projectCity" },
        { title: "تاریخ شروع پروژه", headerKey: "projectStartDate" },
        { title: "مدیر پروژه", headerKey: "projectManager" },
        { title: "تعداد دستگاه پروژه", headerKey: "projectDevices" },
        { title: "عملیات", headerKey: "projectActions" },
      ]
    : [
        { title: "تصویر پروژه", headerKey: "projectLogo" },
        { title: "نام پروژه", headerKey: "projectName" },
        { title: "شهر محل انجام", headerKey: "projectCity" },
        { title: "تاریخ شروع پروژه", headerKey: "projectStartDate" },
        { title: "مدیر پروژه", headerKey: "projectManager" },
        { title: "تعداد دستگاه پروژه", headerKey: "projectDevices" },
      ];
  const tableData = () => {
    let projectTableData: ProjectTableData = [];
    if (!isLoading && status !== "pending") {
      projectData.forEach((obj: ProjectObject) =>
        projectTableData.push({
          projectLogo: renderProjectLogo(
            obj.water_meter_project_urls.logo,
            obj.water_meter_project_id
          ),
          projectName: renderProjectName(
            obj.water_meter_project_name,
            obj.water_meter_project_id
          ),
          projectCity: obj.water_meter_project_title,
          projectStartDate: toPersianDate(obj.water_meter_project_start_date),
          projectManager:
            obj.water_meter_project_employer_description?.lastName ?? "",
          projectDevices:
            obj.water_meters_with_this_id?.All_water_meter_with_this_id,
          projectActions: renderProjectActions(obj.water_meter_project_id),
        })
      );
    }
    return projectTableData;
  };

  return (
    <div className="">
      <CustomModal
        isOpen={isDeleteConfirmOpen}
        onClose={onDeletConfirmClose}
        title={""}
        modalType="form"
        information={null}
        modalForm={
          <DeleteForm
            deleteType="project"
            projectDeleted={projectInfo}
            onClose={onDeletConfirmClose}
            deleteFunction={deleteProject}
          />
        }
      />
      <CustomModal
        isOpen={isProjectOpen}
        onClose={onProjectClose}
        title={"پروژه"}
        modalType="form"
        modalForm={
          <ProjectForm
            projectData={projectInfo}
            onClose={onProjectClose}
            isEditForm={isEditForm}
            setEditForm={setEditForm}
            updateTable={refetch}
          />
        }
      />
      <Card>
        <div className="relative flex items-center justify-between p-4">
          <div className="text-xl font-bold text-navy-700 dark:text-white">
            {`پروژه ها (${
              isLoading && projectData.length < 0
                ? "loading"
                : projectData[0]?.all_project_numbers
            })`}
          </div>
          <div className=" moldal-btns flex items-center justify-end">
            {AdminPermissions.includes("Admin") ? (
              <CustomButton
                text="افزودن پروژه"
                onClick={() => addProjectClick()}
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
          header={projectTableHeader}
          data={tableData()}
          extra="h-[60vh]"
          // hasIndex={true}
        />
        <div className="pagination ">
          <CustomPagination
            page={page}
            pageSize={count}
            totalData={
              projectData.length > 0 ? projectData[0].all_project_numbers : 0
            }
            changePageFunc={setPage}
            changeCount={setCount}
          />
        </div>
      </Card>
      {/* <AMQPComponent /> */}
      {/* <RabbitMqComponent /> */}
      {/* <RabbitMQSubscriber /> */}
    </div>
  );
};
export default ProjectsView;
