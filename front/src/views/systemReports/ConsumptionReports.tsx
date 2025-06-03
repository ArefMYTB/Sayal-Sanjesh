import { useId, useState } from "react";
import { reqFunction } from "utils/API";
import Widget from "views/rtl/default/components/Widget";
import ConsumptionChartFilter from "./ConsumptionChartFilter";
import { DynamicOption } from "components/fields/SelectInput";
import { counterTagSelect } from "variables";
import { UserObject } from "views/users/UsersTable";
import { ProjectObject } from "views/projects";
import { TypeObject } from "views/settings/DeviceTypesTable";
import { getDatesBetween, getToday, toPersianDate } from "utils/TimeUtiles";
import { useQuery } from "@tanstack/react-query";
import MixChart from "components/charts/MixChart";
import Loading from "components/loading";
import {
  renderComplexChartData,
  renderComplexChartOptions,
} from "utils/globalUtils";
import { renderUnit } from "utils/CommonFunctions";

const ConsumptionReport = () => {
  const id = useId();
  const [fromDate, setFromDate] = useState(getToday().jDate(1));
  const [tillDate, setTillDate] = useState(getToday().add(1, "day"));
  const [project, setProject] = useState<DynamicOption>(null);
  const [tag, setTag] = useState<DynamicOption>(counterTagSelect[0]);
  const [user, setUser] = useState<DynamicOption>(null);
  const [type, setType] = useState<DynamicOption>(null);
  // //console.log(1 + id + 1);
  //consumptions statistics data
  const {
    data: consumptionsData,
    isLoading: consumptionsIsLoading,
    status: consumptionsStatus,
  } = useQuery({
    queryFn: () =>
      reqFunction("watermeters/admin/consumption/total/statistics", {}, "post"),
    queryKey: ["consumptionStatistics"],
  });
  //users data
  const {
    data: usersData,
    isLoading: usersIsLoading,
    status: usersStatus,
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
  //project data
  const {
    data: projectsData,
    isLoading: projectsIsLoading,
    status: projectsStatus,
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
  //types data
  const {
    data: typesData,
    isLoading: typesIsLoading,
    status: typesStatus,
  } = useQuery({
    queryFn: () =>
      reqFunction("WaterMeterTypes/admin/getAll", {
        page: 1,
        count: 10,
        water_meter_type_name: "",
        water_meter_type_create_date: "",
      }),
    queryKey: ["typesList"],
  });
  //consumptions main request data by date
  const {
    data: consumptionsDatesData,
    isLoading: consumptionsDatesIsLoading,
    status: consumptionsDatesStatus,
    refetch: consumptionDatesRefetch,
  } = useQuery({
    queryFn: () =>
      reqFunction(
        "watermeters/admin/getAll/consumption/date",
        {
          page: 1,
          count: 1000,
          project_id: project ? project.value : null,
          user_id: user ? user.value : null,
          water_meters: null,
          type_id: type ? type.value : null,
          tag_id: tag.value,
          start_time: fromDate.format("YYYY-M-D"),
          end_time: tillDate.format("YYYY-M-D"),
        },
        "post"
      ),
    queryKey: ["consumptionsDates", project, user, tag, type],
  });
  //statistic render
  const renderWidgets = (data: any) => {
    let v: any[] = [];
    let new_data = { ...data };
    delete new_data.all_consumptions;
    for (const property in new_data) {
      if (property !== "سایر") {
        v.push({ ...data[property], name: property });
      }
    }
    return (
      <>
        {v.map(
          (
            obj: {
              sum_of_all_tag_consumption: number;
              name: string;
              tag_count: number;
            },
            index: number
          ) => (
            <>
              {/* {console.log(`${id}-${index}`)} */}
              <Widget
                // key={index + id + index}
                key={`${id}-${index}`}
                title={`میزان مصرف ${obj.name}`}
                subtitle={`${Math.round(
                  obj.sum_of_all_tag_consumption
                ).toLocaleString()} ${renderUnit(obj.name, false)}`}
              />
            </>
          )
        )}
      </>
    );
  };
  const renderUserSelect = (userList: UserObject[]) => {
    let usersSelect: DynamicOption[] = [];
    userList?.forEach((user) => {
      usersSelect.push({
        value: user.user_id,
        label: `${user.user_name} ${user.user_lastname}`,
      });
    });
    return usersSelect;
  };
  const renderProjectSelect = (projectList: ProjectObject[]) => {
    let projectSelect: DynamicOption[] = [];
    projectList?.forEach((project) => {
      projectSelect.push({
        value: project.water_meter_project_id,
        label: project.water_meter_project_name,
      });
    });
    return projectSelect;
  };
  const renderTypeSelect = (typeList: TypeObject[]) => {
    let typeSelect: DynamicOption[] = [];
    let typeInProject: string[] = [];
    if (project) {
      let fP: ProjectObject[] = projectsData.data?.filter(
        (p: ProjectObject) => p.water_meter_project_id === project.value
      );
      fP[0].types?.forEach((type) =>
        typeInProject.push(type.water_meter_type_id)
      );
    }
    typeList
      ?.filter(
        (types) => types.water_meter_tag.water_meter_tag_id === tag.value
      )
      ?.forEach((type) => {
        typeSelect.push({
          value: type.water_meter_type_id,
          label: type.water_meter_type_name,
          disabled: !project
            ? false
            : typeInProject.includes(type.water_meter_type_id)
            ? false
            : true,
        });
      });
    return typeSelect;
  };
  return (
    <>
      <div className="projects-overview h-max pt-4">
        <div className="pb-4 text-xl font-bold text-navy-700 dark:text-white">
          آمار کلی
        </div>

        {!consumptionsIsLoading && consumptionsStatus === "success" ? (
          <div className=" mt-3 grid grid-cols-1 gap-5 md:grid-cols-2 lg:grid-cols-3">
            {renderWidgets(consumptionsData.data)}
          </div>
        ) : (
          // <div>statistics loading</div>
          <Loading />
        )}

        <div className="mt-2 py-4 text-xl font-bold text-navy-700 dark:text-white">
          نمودار مصرف
        </div>
        {!usersIsLoading &&
        usersStatus === "success" &&
        !projectsIsLoading &&
        projectsStatus === "success" &&
        !typesIsLoading &&
        typesStatus === "success" ? (
          <div className="chart-statistics py-2">
            <ConsumptionChartFilter
              tagSelect={counterTagSelect}
              tag={tag}
              setTag={setTag}
              userSelect={renderUserSelect(usersData.data)}
              user={user}
              setUser={setUser}
              projectSelect={renderProjectSelect(projectsData.data)}
              project={project}
              setProject={setProject}
              typeSelect={renderTypeSelect(typesData.data)}
              type={type}
              setType={setType}
              fromDate={fromDate}
              setFromDate={setFromDate}
              tillDate={tillDate}
              setTillDate={setTillDate}
              update={consumptionDatesRefetch}
            />
          </div>
        ) : (
          // <div>consumption date essential loading</div>
          <Loading />
        )}
        {!consumptionsDatesIsLoading &&
        consumptionsDatesStatus === "success" ? (
          <div className="chart-container mx-auto h-[400px] w-full min-w-[95%]">
            <MixChart
              chartData={renderComplexChartData(
                consumptionsDatesData.data,
                fromDate,
                tillDate
              )}
              chartOptions={renderComplexChartOptions(
                // consumptionsDatesData.data,
                fromDate,
                tillDate
              )}
              chartTag={tag}
            />
          </div>
        ) : (
          // <div>chart is loading</div>
          <Loading />
        )}
      </div>
    </>
  );
};
export default ConsumptionReport;
