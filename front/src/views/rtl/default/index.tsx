import {
  MdCategory,
  MdGasMeter,
  MdPeopleAlt,
  MdViewList,
} from "react-icons/md";
import Widget from "views/rtl/default/components/Widget";
import { useQuery } from "@tanstack/react-query";
import { reqFunction } from "utils/API";
import { ChartOptions } from "views/systemReports/ProjecsReport";
import PieChart from "components/charts/PieChart";
import DonutChart from "components/charts/DonutChart";
import MultiColumnsChart from "components/charts/MultiColumnsChart";
import { DynamicOption } from "components/fields/SelectInput";
import { useState } from "react";
import { getToday } from "utils/TimeUtiles";
import { counterTagSelect } from "variables";
import { ProjectObject } from "views/projects";
import { UserObject } from "views/users/UsersTable";
import { TypeObject } from "views/settings/DeviceTypesTable";
import MixChart from "components/charts/MixChart";
import ConsumptionChartFilter from "views/systemReports/ConsumptionChartFilter";
import CustomMap from "components/map";
import Loading from "components/loading";
import {
  renderComplexChartData,
  renderComplexChartOptions,
} from "utils/globalUtils";
import { renderSelectData } from "utils/CommonFunctions";

const Dashboard = () => {
  const [tag, setTag] = useState<DynamicOption>(counterTagSelect[0]);
  const [user, setUser] = useState<DynamicOption>(null);
  const [project, setProject] = useState<DynamicOption>(null);
  const [type, setType] = useState<DynamicOption>(null);
  const fromDate = getToday().jDate(1);
  const tillDate = getToday().add(1, "day");
  let permissions: string[] = JSON.parse(
    window.localStorage.getItem("permissions")
  );
  const {
    data: dashboardData,
    isLoading: dashboardDataIsLoading,
    status: dashboardDataStatus,
  } = useQuery({
    queryFn: () =>
      reqFunction("watermeters/admin/countAll", {
        type: null,
        project: null,
        water_meter_activation: null,
        water_meter_validation: null,
      }),
    queryKey: ["dashboardStatistics"],
  });
  const {
    data: citiesData,
    isLoading: citiesIsLoading,
    status: citiesStatus,
  } = useQuery({
    queryFn: () =>
      reqFunction("WaterMeterProjectsURL/admin/getAll/city/count", {}, "get"),
    queryKey: ["citiesStatistics"],
  });
  const {
    data: devicesData,
    isLoading: devicesIsLoading,
    status: devicesStatus,
  } = useQuery({
    queryFn: () =>
      reqFunction("WaterMeterTags/admin/total/statistcs", {}, "get"),
    queryKey: ["devicesStatistics"],
  });
  const {
    data: typesConditionData,
    isLoading: typesConditionIsLoading,
    status: typesConditionStatus,
  } = useQuery({
    queryFn: () => reqFunction("WaterMeterTypes/admin/getAllValues", {}, "get"),
    queryKey: ["devicesTypeConditions"],
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
    // refetch: consumptionDatesRefetch,
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
  const renderDonutData = (data: any) => {
    const chartData: string[] = [];
    delete data?.all_water_meters_count;
    for (const property in data) {
      chartData.push(data[property]);
    }
    return chartData;
  };
  const renderDonutOptions = (data: any) => {
    const chartOptions: ChartOptions = { labels: [] };
    delete data?.all_water_meters_count;
    for (const property in data) {
      chartOptions.labels.push(property);
    }
    return chartOptions;
  };
  const renderChartData = (data: any) => {
    const chartData: string[] = [];
    for (const property in data) {
      chartData.push(data[property]);
    }
    return chartData;
  };
  const renderChartOptions = (data: any) => {
    const chartOptions: ChartOptions = { labels: [] };
    for (const property in data) {
      chartOptions.labels.push(property);
    }
    return chartOptions;
  };
  const renderSaleCharData = (data: any) => {
    let chartData: { name: string; data: number[] }[] = [];
    const saleData: number[] = [];
    const availableData: number[] = [];
    for (const property in data) {
      saleData.push(data[property].activation);
      availableData.push(data[property].all_water_meter);
    }
    chartData = [
      { name: "فروش رفته", data: saleData },
      { name: "موجودی کل", data: availableData },
    ];
    return chartData;
  };
  const renderSaleChartOptions = (data: any) => {
    const SaleChartOptions: string[] = [];
    for (const property in typesConditionData.data) {
      SaleChartOptions.push(property);
    }
    return SaleChartOptions;
  };
  const renderTypeSelect = (typeList: TypeObject[]) => {
    let typeSelect: DynamicOption[] = [];
    let typeInProject: string[] = [];
    if (project) {
      let fP: ProjectObject[] = projectsData.data.filter(
        (p: ProjectObject) => p.water_meter_project_id === project.value
      );
      fP[0].types.forEach((type) =>
        typeInProject.push(type.water_meter_type_id)
      );
    }
    typeList
      .filter((types) => types.water_meter_tag.water_meter_tag_id === tag.value)
      .forEach((type) => {
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
    <div>
      <div className="xl:grid-col-4 mt-3 grid grid-cols-1 gap-5 md:grid-cols-2 lg:grid-cols-3 2xl:grid-cols-4 3xl:grid-cols-6">
        {!dashboardDataIsLoading && dashboardDataStatus === "success" ? (
          <>
            <Widget
              icon={<MdViewList className="h-7 w-7" />}
              title={"پروژه ها"}
              subtitle={`${dashboardData?.data?.water_meter_project} عدد`}
              link={"/admin/projects"}
            />
            <Widget
              icon={<MdGasMeter className="h-6 w-6" />}
              title={"دستگاه ها"}
              subtitle={`${dashboardData?.data?.all_water_meter} عدد`}
              link={"/admin/counters"}
            />
            <Widget
              icon={<MdPeopleAlt className="h-7 w-7" />}
              title={"بهره برداران"}
              subtitle={`${dashboardData?.data?.all_users} نفر`}
              link={"/admin/users"}
            />
            <Widget
              icon={<MdCategory className="h-7 w-7" />}
              title={"انواع دستگاه ها"}
              subtitle={`${dashboardData?.data?.water_meter_type} نوع`}
              link={null}
            />
            <Widget
              icon={<MdCategory className="h-7 w-7" />}
              title={"تعداد دستگاه فعال"}
              subtitle={`${dashboardData?.data?.water_meter_activation} عدد`}
              link={null}
            />
          </>
        ) : (
          <Loading />
        )}
      </div>
      {!citiesIsLoading &&
      citiesStatus &&
      !devicesIsLoading &&
      devicesStatus === "success" ? (
        <>
          <div className=" grid grid-cols-1 gap-4 py-4 xl:grid-cols-6">
            <div className=" map-wrapper xl:col-span-4">
              <CustomMap />
            </div>
            <div className="round-charts grid grid-cols-1 gap-2 xl:col-span-2 ">
              <div className="donat h-[29vh]">
                <div className=" text-lg font-semibold dark:text-white">
                  تفکیک دستگاه ها
                </div>
                <DonutChart
                  chartOptions={renderDonutOptions(devicesData?.data)}
                  chartData={renderDonutData(devicesData?.data)}
                />
              </div>
              <div className="pie h-[29vh]">
                <div className="text-lg font-semibold dark:text-white">
                  پروژه به تفکیک شهر
                </div>
                <PieChart
                  chartOptions={renderChartOptions(citiesData?.data)}
                  chartData={renderChartData(citiesData?.data)}
                />
              </div>
            </div>
          </div>
        </>
      ) : (
        <Loading />
      )}
      <div className="mt-2 py-4 text-xl font-bold text-navy-700 dark:text-white">
        مصرف ماه اخیر
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
            userSelect={renderSelectData(usersData.data, "user")}
            user={user}
            setUser={setUser}
            projectSelect={renderSelectData(projectsData.data, "project")}
            project={project}
            setProject={setProject}
            typeSelect={renderTypeSelect(typesData.data)}
            type={type}
            setType={setType}
            // fromDate={fromDate}
            // setFromDate={setFromDate}
            // tillDate={tillDate}
            // setTillDate={setTillDate}
            // update={consumptionDatesRefetch}
          />
        </div>
      ) : (
        <Loading />
      )}
      {!consumptionsDatesIsLoading && consumptionsDatesStatus === "success" ? (
        <div className="chart-container mx-auto h-[60vh] w-full min-w-[95%]">
          <MixChart
            chartData={renderComplexChartData(
              consumptionsDatesData?.data,
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
      {permissions.includes("Admin") ? (
        <>
          {!typesConditionIsLoading && typesConditionStatus === "success" ? (
            <>
              <div className="mt-5 grid !grid-cols-1 gap-5 lg:!grid-cols-6">
                <div className="chart-container sales-chart-wrapper col-span-1 h-[500px] w-full min-w-[60%] lg:col-span-4">
                  <MultiColumnsChart
                    chartOptions={renderSaleChartOptions(
                      typesConditionData.data
                    )}
                    chartData={renderSaleCharData(typesConditionData.data)}
                  />
                </div>
              </div>
            </>
          ) : (
            <Loading />
          )}
        </>
      ) : (
        <></>
      )}
    </div>
  );
};

export default Dashboard;
