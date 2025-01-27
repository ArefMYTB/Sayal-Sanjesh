import CustomButton from "components/button";
import SelectInput, { DynamicOption } from "components/fields/SelectInput";
import { useState } from "react";
import { MdDelete } from "react-icons/md";
import { reqFunction } from "utils/API";
import { renderToast } from "utils/globalUtils";
import { ProjectObject } from "views/projects";

export type MiddleAdmins = {
  admin_id: string;
  admin_name: string;
  admin_lastname: string;
  admin_phone: string;
  middel_admin_projects: ProjectObject[];
};
interface AssignProjectFormProps {
  projectSelectData?: DynamicOption[] | null;
  onClose: Function;
  middleId: string;
  middleAdmins: MiddleAdmins[];
  middleProjectRefetch: Function;
  middleProjectIds: string[];
  // updateTable: any;
}
const AssignProjectForm = (props: AssignProjectFormProps) => {
  const [project, setProject] = useState<DynamicOption>(null);

  const {
    projectSelectData,
    onClose,
    middleId,
    middleAdmins,
    middleProjectRefetch,
    middleProjectIds,
    // updateTable,
  } = props;
  // //console.log(middleAdmins);
  const deleteMiddleProject = async (
    pid: string,
    middleProjects: ProjectObject[]
  ) => {
    //console.log(pid);
    let newProjectList = middleProjects.filter(
      (project) => project.water_meter_project_id !== pid
    );
    let middleNewProjectIds: string[] = [];
    newProjectList.forEach((project) =>
      middleNewProjectIds.push(project.water_meter_project_id)
    );
    let response = await reqFunction("middle/admin/edit/data", {
      middle_admin_id: middleId,
      project_ids: middleNewProjectIds,
      water_meter_ids: [],
    });
    if (response.code === 200) {
      renderToast("تغییرات در تخصیص پروژه با موفقیت انجام شد", "success");
      // updateTable();
      middleProjectRefetch();
      // onClose();
      setProject(null);
      // setOrderType(null);
    } else {
      renderToast(
        response?.farsi_message
          ? response.farsi_message
          : "در تخصیص پروژه خطایی رخ داده",
        "err"
      );
    }
  };
  const renderMiddleInfo = () => {
    let selectedMiddle = middleAdmins.filter(
      (admin) => admin.admin_id === middleId
    );

    return (
      <>
        {selectedMiddle.length > 0 ? (
          selectedMiddle[0].middel_admin_projects.map((p, i) => (
            <div
              key={p.water_meter_project_id}
              className="flex items-center justify-between border-b py-2"
            >
              <span className="">{p.water_meter_project_name}</span>{" "}
              <span className="">
                <CustomButton
                  onClick={() =>
                    deleteMiddleProject(
                      p.water_meter_project_id,
                      selectedMiddle[0].middel_admin_projects
                    )
                  }
                  icon={<MdDelete />}
                  color="red"
                  extra="!p-2"
                />
              </span>
            </div>
          ))
        ) : (
          <div className="py-2  text-navy-700  dark:text-white">
            پروژه ای به این کاربر تخصیص داده نشده است !!!
          </div>
        )}
      </>
    );
  };
  const assignProject = async () => {
    if (project) {
      let newProjectList = [...middleProjectIds, project.value];
      let response = await reqFunction("middle/admin/add/data", {
        middle_admin_id: middleId,
        project_ids: newProjectList,
        water_meter_ids: [],
      });
      if (response.code === 200) {
        renderToast("تخصیص پروژه با موفقیت انجام شد", "success");
        // updateTable();
        middleProjectRefetch();
        // onClose();
        setProject(null);
        // setOrderType(null);
      } else {
        renderToast(
          response?.farsi_message
            ? response.farsi_message
            : "در تخصیص پروژه خطایی رخ داده",
          "err"
        );
      }
    } else {
      renderToast("تمامی موارد را انتخاب کنید", "warn");
    }
  };
  return (
    <>
      <div className=" py-2">
        <div className="text-md font-bold text-navy-700 dark:text-white">
          پروژه های مدیر
        </div>
        <div className="">{renderMiddleInfo()}</div>
      </div>
      <div className=" flex flex-col space-y-4">
        <SelectInput
          label="نام پروژه"
          placeholder="پروژه مورد نظر را انتخاب کنید"
          dynamicOptions={projectSelectData}
          state={project}
          setState={setProject}
        />
        <div className="form-actions flex flex-row items-center justify-end ">
          <CustomButton onClick={onClose} text="بستن" color="red" />
          <CustomButton
            onClick={() => assignProject()}
            text={`ارسال`}
            color="green"
            extra="!ml-0"
          />
        </div>
      </div>
    </>
  );
};
export default AssignProjectForm;
