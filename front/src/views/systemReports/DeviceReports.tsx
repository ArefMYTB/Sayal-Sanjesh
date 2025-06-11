import { useQuery } from "@tanstack/react-query";
import DonutChart from "components/charts/DonutChart";
import { useId } from "react";
import { reqFunction } from "utils/API";
import Widget from "views/rtl/default/components/Widget";
import { ChartOptions } from "./ProjecsReport";
import MultiColumnsChart from "components/charts/MultiColumnsChart";
import Loading from "components/loading";

const DevicesReport = () => {
  let permissions: string[] = JSON.parse(
    window.localStorage.getItem("permissions")
  );

  const id = useId();
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
  const renderWidgets = (data: {}) => {
    let keys = [];
    for (const property in data) {
      keys.push(property);
    }
    return keys.map((key: string, index: number) => (
      <Widget
        key={id + index}
        title={
          key.includes("_") ? "تعداد کل دستگاه ها" : `تعداد کنتور های ${key}`
        }
        subtitle={`${devicesData.data[key]} عدد`}
      />
    ));
  };
  return (
    <>
      {!devicesIsLoading &&
      devicesStatus === "success" &&
      !typesConditionIsLoading &&
      typesConditionStatus === "success" ? (
        <div className="projects-overview pt-4">
          <div className="pb-4 text-xl font-bold text-navy-700 dark:text-white">
            آمار کلی
          </div>
          <div className=" mt-3 grid grid-cols-1 gap-5 md:grid-cols-2 lg:grid-cols-3">
            {renderWidgets(devicesData.data)}
          </div>
          {permissions.includes("Store") ? (
            <>
              <div className="mt-2 py-4 text-xl font-bold text-navy-700 dark:text-white">
                آمار دستگاه ها به تفکیک دسته و فروش
              </div>
              <div className="chart-statistics flex flex-col items-center justify-center py-2 md:flex-row md:justify-between ">
                <div className="chart-container h-[400px] w-full min-w-[60%]">
                  <MultiColumnsChart
                    chartOptions={renderSaleChartOptions(
                      typesConditionData.data
                    )}
                    chartData={renderSaleCharData(typesConditionData.data)}
                  />
                </div>
                <div className="chart-container h-[400px] min-w-[35%]">
                  <DonutChart
                    chartOptions={renderDonutOptions(devicesData.data)}
                    chartData={renderDonutData(devicesData.data)}
                  />
                </div>
              </div>
            </>
          ) : (
            <></>
          )}
        </div>
      ) : (
        // <div>loading or err</div>
        <Loading />
      )}
    </>
  );
};
export default DevicesReport;
