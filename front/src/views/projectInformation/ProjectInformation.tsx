import { toPersianDate } from "utils/TimeUtiles";
import { ProjectObject } from "views/projects";
import Widget from "views/rtl/default/components/Widget";

interface ProjectInformationProps {
  projectData: [ProjectObject];
}
const ProjectInformation = (props: ProjectInformationProps) => {
  const { projectData } = props;
  const info = projectData[0];
  return (
    <div className="projects-overview pt-4">
      <div className="pb-4 text-xl font-bold text-navy-700 dark:text-white">
        جزئیات پروژه
      </div>
      <div className=" mt-3 grid grid-cols-1 gap-5 md:grid-cols-2 lg:grid-cols-3">
        <Widget title={"نام پروژه "} subtitle={info.water_meter_project_name} />
        <Widget
          title={"تاریخ شروع پروژه"}
          subtitle={toPersianDate(info.water_meter_project_start_date)}
        />
        <Widget
          title={"محل انجام پروژه"}
          subtitle={`شهر ${info.water_meter_project_title}`}
        />
        <Widget
          title={"شماره قرارداد "}
          subtitle={info.water_meter_project_contract_number}
        />
        <Widget
          title={"نام کارفرما"}
          subtitle={`${info.water_meter_project_employer_description.name} ${info.water_meter_project_employer_description.lastName}`}
        />
        <Widget
          title={"تلفن کارفرما"}
          subtitle={info.water_meter_project_employer_description.phoneNumber}
        />

        <Widget
          title={"تعداد دستگاه در پروژه"}
          subtitle={`${info.water_meters_with_this_id.All_water_meter_with_this_id} عدد`}
        />
      </div>
    </div>
  );
};
export default ProjectInformation;
