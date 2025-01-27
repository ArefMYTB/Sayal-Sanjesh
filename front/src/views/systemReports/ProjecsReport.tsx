import { useQuery } from "@tanstack/react-query";
import PieChart from "components/charts/PieChart";
import Loading from "components/loading";
import { reqFunction } from "utils/API";
import Widget from "views/rtl/default/components/Widget";
export type ChartOptions = {
  labels?: string[];
};
const ProjectsReport = () => {
  const {
    data: projectsData,
    isLoading: projectIsLoading,
    status: projectStatus,
  } = useQuery({
    queryFn: () =>
      reqFunction("WaterMeterProjectsURL/admin/total/statistics", {}, "get"),
    queryKey: ["projectStatistics"],
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
  return (
    <>
      {!projectIsLoading &&
      projectStatus === "success" &&
      !citiesIsLoading &&
      citiesStatus === "success" ? (
        <div className="projects-overview pt-4">
          <div className="pb-4 text-xl font-bold text-navy-700 dark:text-white">
            آمار کلی
          </div>
          <div className=" mt-3 grid grid-cols-1 gap-5 md:grid-cols-2 lg:grid-cols-3">
            <Widget
              title={"تعداد پروژه ها"}
              subtitle={`${projectsData.data.all_projects} عدد`}
            />
            <Widget
              title={"شهرهای پروژه"}
              subtitle={`${projectsData.data.all_cities} شهر`}
            />
            <Widget
              title={"شهر با بیشترین پروژه"}
              subtitle={`${projectsData.data.city_with_max_projects[0][0]} با ${projectsData.data.city_with_max_projects[0][1]} پروژه`}
            />

            <Widget
              title={"پروژه با بیشترین دستگاه"}
              subtitle={`${projectsData.data.project_with_max_counters[0].water_meter_project_name} با ${projectsData.data.project_with_max_counters[0].number_of_counter} پروژه`}
            />
          </div>
          <div className="mt-2 py-4 text-xl font-bold text-navy-700 dark:text-white">
            آمار پروژه ها به تفکیک شهرها
          </div>
          <div className="chart-statistics flex flex-col items-center justify-center py-2 md:flex-row md:justify-between ">
            <div className="chart-container h-[300px] min-w-[45%]">
              <PieChart
                chartOptions={renderChartOptions(citiesData.data)}
                chartData={renderChartData(citiesData.data)}
              />
            </div>
          </div>
        </div>
      ) : (
        // <div>loading or err</div>
        <Loading />
      )}
    </>
  );
};
export default ProjectsReport;
