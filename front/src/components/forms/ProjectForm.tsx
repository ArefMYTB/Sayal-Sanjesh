import { useState } from "react";
import CustomButton from "components/button";
import DateInput from "components/fields/DateInput";
import InputField from "components/fields/InputField";
import { getToday } from "utils/TimeUtiles";
import SelectInput, { DynamicOption } from "components/fields/SelectInput";
import { cities } from "variables";
// import FileUploader from "components/fields/ImageUpload";
// import { get } from "http";
import { ProjectObject } from "views/projects";
import { reqFunction } from "utils/API";
import { renderToast } from "utils/globalUtils";
import FileUploader from "components/fields/ImageUpload";
// type ProjectData = {
//   water_meter_project_name: string;
//   water_meter_project_title: string;
//   water_meter_project_other_information: { description?: string };
//   water_meter_project_start_date: null | string;
//   water_meter_project_employer_description: { discription: string };
//   water_meter_project_contract_number: string;
//   water_meter_project_images: Array<string>;
//   water_meter_project_urls: {
//     logo: string;
//     gallery: Array<string>;
//   };
// };
interface ProjectFormProps {
  projectData: ProjectObject;
  onClose: Function;
  isEditForm: boolean;
  setEditForm: React.Dispatch<boolean>;
  updateTable: any;
}
const ProjectForm = (props: ProjectFormProps) => {
  const { onClose, projectData, isEditForm, updateTable, setEditForm } = props;
  const [projectName, setProjectName] = useState<string>(
    isEditForm ? projectData?.water_meter_project_name : ""
  );
  const [date, setDate] = useState(
    isEditForm
      ? getToday(projectData?.water_meter_project_start_date)
      : getToday()
  );
  const [projectCity, setProjectCity] = useState<DynamicOption>(
    isEditForm
      ? cities.filter(
          (city) => city.label === projectData?.water_meter_project_title
        )[0]
      : null
  );
  const [contractNumber, setContractNumber] = useState<string>(
    isEditForm ? projectData?.water_meter_project_contract_number : ""
  );
  const [projectDescription, setProjectDescription] = useState<string>(
    isEditForm &&
      projectData?.water_meter_project_other_information?.description
      ? projectData?.water_meter_project_other_information?.description
      : ""
  );
  const [previewUrl, setPreviewUrl] = useState<string | null>(
    isEditForm && projectData?.water_meter_project_urls?.logo
      ? projectData?.water_meter_project_urls?.logo
      : null
  );
  const [pmName, setPmName] = useState<string>(
    isEditForm
      ? projectData?.water_meter_project_employer_description?.name
      : ""
  );
  const [pmLastName, setPmLastName] = useState<string>(
    isEditForm
      ? projectData?.water_meter_project_employer_description?.lastName
      : ""
  );
  const [pmPhone, setPmPhone] = useState<string>(
    isEditForm
      ? projectData?.water_meter_project_employer_description?.phoneNumber
      : ""
  );
  const editProject = async () => {
    let json: ProjectObject = {
      water_meter_project_name: projectName,
      water_meter_project_title: projectCity.label,
      water_meter_project_other_information: {
        description: projectDescription,
      },
      water_meter_project_start_date: date,
      water_meter_project_employer_description: {
        name: pmName,
        lastName: pmLastName,
        phoneNumber: pmPhone,
      },
      water_meter_project_contract_number: contractNumber,
      water_meter_project_images: projectData?.water_meter_project_images,
      water_meter_project_urls: {
        logo: previewUrl ? previewUrl : "",
        gallery: projectData?.water_meter_project_urls?.gallery
          ? projectData.water_meter_project_urls.gallery
          : [],
      },
      water_meter_project_id: projectData?.water_meter_project_id,
    };
    let response = await reqFunction("WaterMeterProjectsURL/admin/edit", json);
    if (response.code === 200) {
      renderToast("تغییر پروژه با موفقیت انجام شد", "success");
      updateTable();
      onClose();
      // clearForm();
      setEditForm(false);
    } else {
      renderToast(
        response?.farsi_message
          ? response.farsi_message
          : "در تغییر پروژه خطایی رخ داده",
        "err"
      );
    }
  };
  const addProject = async () => {
    let json: ProjectObject = {
      water_meter_project_name: projectName,
      water_meter_project_title: projectCity.label,
      water_meter_project_other_information: {
        description: projectDescription,
      },
      water_meter_project_start_date: date,
      water_meter_project_employer_description: {
        name: pmName,
        lastName: pmLastName,
        phoneNumber: pmPhone,
      },
      water_meter_project_contract_number: contractNumber,
      water_meter_project_images: [],
      water_meter_project_urls: {
        logo: previewUrl ? previewUrl : "",
        gallery: [],
      },
    };
    let response = await reqFunction("WaterMeterProjectsURL/admin/add", json);
    if (response.code === 200) {
      renderToast("افزودن پروژه با موفقیت انجام شد", "success");
      updateTable();
      onClose();
      // clearForm();
      setEditForm(false);
    } else {
      renderToast(
        response?.farsi_message
          ? response.farsi_message
          : "در افزودن پروژه خطایی رخ داده",
        "err"
      );
    }
  };
  return (
    <div className=" flex flex-col space-y-2">
      <FileUploader
        preview={previewUrl}
        setPreview={setPreviewUrl}
        uploaderType="projectImage"
        uploadEndpoint="Updload/admin"
      />
      <InputField
        id="project-name"
        label="نام پروژه"
        placeholder="نام پروژه را وارد کنید"
        type="text"
        state={projectName}
        setState={setProjectName}
      />
      <DateInput label="تاریخ شروع پروژه" value={date} onChange={setDate} />
      <SelectInput
        label="شهر پروژه"
        placeholder="شهر پروژه را انتخاب کنید"
        dynamicOptions={cities}
        state={projectCity}
        setState={setProjectCity}
      />

      <InputField
        id="contract-number"
        label="شماره قرارداد"
        placeholder="شماره قرارداد را وارد کنید"
        type="text"
        state={contractNumber}
        setState={setContractNumber}
      />
      <InputField
        id="project-description"
        label="توضیحات پروژه"
        placeholder="توضیحات پروژه را وارد کنید"
        type="text-aria"
        state={projectDescription}
        setState={setProjectDescription}
      />
      <div className=" py-1 text-lg font-bold">مشخصات کارفرما</div>
      <InputField
        id="project-manager-name"
        label="نام"
        placeholder="نام کارفرما را وارد کنید"
        type="text"
        state={pmName}
        setState={setPmName}
      />

      <InputField
        id="project-manager-lastName"
        label="نام خانوادگی"
        placeholder="نام خانوادگی کارفرما را وارد کنید"
        type="text"
        state={pmLastName}
        setState={setPmLastName}
      />
      <InputField
        id="project-manager-phone"
        label="شماره کارفرما"
        placeholder="شماره تماس کارفرما را وارد کنید"
        type="text"
        state={pmPhone}
        setState={setPmPhone}
      />
      <div className="form-actions flex flex-row items-center justify-end ">
        <CustomButton onClick={onClose} text="بستن" color="red" />
        <CustomButton
          onClick={() => (isEditForm ? editProject() : addProject())}
          text={`${isEditForm ? "تغییر" : "افزودن"}`}
          color="green"
          extra="!ml-0"
        />
      </div>
    </div>
  );
};
export default ProjectForm;
