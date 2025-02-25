import { useQuery } from "@tanstack/react-query";
import CustomButton from "components/button";
import DonutChart from "components/charts/DonutChart";
import PieChart from "components/charts/PieChart";
import SelectInput, { DynamicOption } from "components/fields/SelectInput";
import SimpleTable from "components/tables/SimpleTable";
import { useMemo, useState } from "react";
import { MdAdd } from "react-icons/md";
import { reqFunction } from "utils/API";
import { renderToast } from "utils/globalUtils";
import { DeviceObj } from "views/counters";
import { ProjectObject } from "views/projects";
import { TypeObject } from "views/settings/DeviceTypesTable";
import { ChartOptions } from "views/systemReports/ProjecsReport";

interface ProjectAbstractProps {
  projectData: [ProjectObject];
  projectDevices: DeviceObj[];
  updateInfo: any;
}
type ProjectTypeTable = {
  deviceType: string;
  deviceTag: string;
};
const ProjectAbstract = (props: ProjectAbstractProps) => {
  const { projectData, projectDevices, updateInfo } = props;
  let projectInfo = projectData[0];
  const [deviceTypes, setDeviceTypes] = useState(null);

  const {
    data: typesData,
    isLoading: typesIsLoading,
    status: typesStatus,
    // refetch: typesRefetch,
  } = useQuery({
    queryFn: () =>
      reqFunction("WaterMeterTypes/admin/getAll", {
        page: 1,
        count: 20,
        water_meter_type_name: "",
        water_meter_type_create_date: "",
      }),
    queryKey: ["typesList"],
  });
  const renderTagsChartData = (data: ProjectObject) => {
    let containTagsId: string[] = [];
    const chartData: number[] = [];
    data.types.forEach((type: TypeObject) => {
      if (!containTagsId.includes(type.water_meter_tag.water_meter_tag_id)) {
        containTagsId.push(type.water_meter_tag.water_meter_tag_id);
      }
    });
    containTagsId.forEach((tag: string) => {
      chartData.push(
        projectDevices.filter(
          (device: DeviceObj) =>
            device.water_meter_type__water_meter_tag__water_meter_tag_id === tag
        ).length
      );
    });
    return chartData;
  };
  const renderTagsChartOptions = (data: ProjectObject) => {
    let containTags: string[] = [];
    const chartOptions: ChartOptions = { labels: [] };
    data.types.forEach((type: TypeObject) => {
      if (!containTags.includes(type.water_meter_tag.water_meter_tag_name)) {
        containTags.push(type.water_meter_tag.water_meter_tag_name);
      }
    });
    chartOptions.labels = containTags;
    return chartOptions;
  };

  const renderTypesChartData = (data: ProjectObject) => {
    let containTypes: string[] = [];
    const chartData: number[] = [];
    data.types.forEach((type: TypeObject) => {
      containTypes.push(type.water_meter_type_name);
    });
    containTypes.forEach((type: string) => {
      chartData.push(
        projectDevices.filter(
          (device: DeviceObj) =>
            device.water_meter_type__water_meter_type_name === type
        ).length
      );
    });
    return chartData;
  };
  const renderTypesChartOptions = (data: ProjectObject) => {
    const chartOptions: ChartOptions = { labels: [] };
    data.types.forEach((type: TypeObject) => {
      chartOptions.labels.push(type.water_meter_type_name);
    });
    return chartOptions;
  };
  const renderTypesOptions = () => {
    let allTypes: TypeObject[] = typesData.data;
    let options: DynamicOption[] = [];
    let projectTypes = projectInfo.types;
    let projectTypesName: string[] = [];
    projectTypes.forEach((type) =>
      projectTypesName.push(type.water_meter_type_name)
    );
    allTypes.forEach((type) =>
      options.push({
        label: type.water_meter_type_name,
        value: type.water_meter_type_id,
        disabled: projectTypesName.includes(type.water_meter_type_name),
      })
    );
    return options;
  };
  const tagChartData = useMemo(
    () => renderTagsChartData(projectInfo),
    [projectInfo]
  );
  const tagChartOptions = useMemo(
    () => renderTagsChartOptions(projectInfo),
    [projectInfo]
  );
  const typeChartData = useMemo(
    () => renderTypesChartData(projectInfo),
    [projectInfo]
  );
  const typeChartOptions = useMemo(
    () => renderTypesChartOptions(projectInfo),
    [projectInfo]
  );
  const addType = async () => {
    // //console.log(deviceTypes);
    let typesIds: string[] = [];
    deviceTypes.forEach((type: any) => typesIds.push(type.value));
    const response = await reqFunction("WaterMeterProjectsURL/admin/addType", {
      water_meter_project_id: projectInfo.water_meter_project_id,
      water_meter_type_id: typesIds,
    });
    if (response.code === 200) {
      renderToast("نوع دستگاه با موفقیت به پروژه اضافه شد.", "success");
      updateInfo();
      setDeviceTypes(null);
      // renderTagsChartData(projectInfo);
      // renderTagsChartOptions(projectInfo);
      // renderTypesChartData(projectInfo);
      // renderTypesChartOptions(projectInfo);
    } else {
      renderToast(
        response?.farsi_message
          ? response.farsi_message
          : "در افزودن نوع دستگاه به پروژه رخ داده",
        "err"
      );
    }
  };
  const projectTypeTableHeader = [
    { title: "نوع دستگاه", headerKey: "deviceType" },
    { title: "دسته بندی", headerKey: "deviceTag" },
  ];
  const renderTableData = () => {
    let projectTypeTableData: ProjectTypeTable[] = [];

    projectInfo.types.forEach((type) =>
      projectTypeTableData.push({
        deviceType: type.water_meter_type_name,
        deviceTag: type.water_meter_tag.water_meter_tag_name,
      })
    );

    return projectTypeTableData;
  };
  return (
    <>
      {projectInfo.water_meters_with_this_id.All_water_meter_with_this_id !==
      "1000" ? (
        <div className="projects-abstract pt-4">
          <div className=" py-4 text-center text-xl font-bold text-navy-700 dark:text-white">
            {projectInfo.water_meter_project_name}
          </div>
          <div className=" grid grid-cols-1 gap-5 md:grid-cols-2">
            <div className="chart-statistics flex flex-col items-center justify-center py-2">
              <div className=" py-4 text-center text-xl font-bold text-navy-700 dark:text-white">
                {`تعداد کل دستگاه ها : ${projectInfo.water_meters_with_this_id.All_water_meter_with_this_id} عدد`}
              </div>
              <div className="chart-container h-[180px] w-full">
                <PieChart
                  // chartOptions={renderTagsChartOptions(projectInfo)}
                  chartOptions={tagChartOptions}
                  // chartData={renderTagsChartData(projectInfo)}
                  chartData={tagChartData}
                />
              </div>
            </div>

            <div className="chart-statistics flex flex-col items-center justify-center py-2 ">
              <div className="mt-2 py-4 text-center text-xl font-bold text-navy-700 dark:text-white">
                {`انواع دستگاه در این پروژه `}
              </div>
              <div className="chart-container h-[180px] w-full ">
                <DonutChart
                  // chartOptions={renderTypesChartOptions(projectInfo)}
                  chartOptions={typeChartOptions}
                  // chartData={renderTypesChartData(projectInfo)}
                  chartData={typeChartData}
                />
              </div>
            </div>
          </div>
        </div>
      ) : (
        <div>دستگاهی در این پروژه موجود نیست</div>
      )}
      {!typesIsLoading && typesStatus === "success" ? (
        <div className="">
          <div className="py-2 text-start text-xl font-bold text-navy-700 dark:text-white">
            انواع دستگاه پروژه
            {`(${projectInfo?.types ? projectInfo.types.length : 0} نوع)`}
          </div>
          <div className="grid grid-cols-1 gap-4 lg:grid-cols-6  ">
            <SelectInput
              label="نوع دستگاه"
              placeholder="نوع دستگاه ها را انتخاب کنید"
              dynamicOptions={renderTypesOptions()}
              state={deviceTypes}
              setState={setDeviceTypes}
              isMulti={true}
              extra="lg:col-span-5"
            />
            <CustomButton
              text="افزودن نوع به پروژه"
              onClick={() => addType()}
              icon={<MdAdd />}
              color="green"
              isDisabled={!deviceTypes}
              extra=" h-[50px]  self-end w-max !ml-0"
            />
          </div>
          <SimpleTable
            data={renderTableData()}
            header={projectTypeTableHeader}
            hasIndex={true}
            extra="h-[27vh]"
          />
        </div>
      ) : (
        <div>type is loading</div>
      )}
    </>
  );
};
export default ProjectAbstract;
