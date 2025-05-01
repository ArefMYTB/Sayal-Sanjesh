import { useState } from "react";
import { reqFunction } from "utils/API";
import ConsumptionChartFilter from "./ConsumptionChartFilter";
import DateInput from "components/fields/DateInput";
import { useQuery } from "@tanstack/react-query";
import MixChart from "components/charts/MixChart";
import { useParams } from "react-router-dom";
import { OneDeviceObj } from ".";
import ApexChart from "components/charts/ApexChart";
// import CustomButton from "components/button";
import { getToday } from "utils/TimeUtiles";
import {
  renderComplexChartData,
  renderComplexChartOptions,
} from "utils/globalUtils";

interface CounterConsumptionChartProps {
  deviceInfo: [OneDeviceObj];
  fromDate: any;
  setFromDate: React.Dispatch<any>;
  tillDate: any;
  setTillDate: React.Dispatch<any>;
}

const CounterConsumptionChart = (props: CounterConsumptionChartProps) => {
  const { deviceSerial } = useParams();
  const { deviceInfo, fromDate, setFromDate, tillDate, setTillDate } = props;

  const [chartType, setChartType] = useState<"daily" | "range">("daily"); // default: daily
  const [apexSelection, setApexSelection] = useState<"one_day" | "one_week">("one_week");
  const [apexChartType, setApexChartType] = useState<"bar" | "line">("bar");
  // Start & End Dates for ApexChart
  const [endDate, setEndDate] = useState(getToday());
  const [startDate, setStartDate] = useState(endDate);

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
          project_id:
            deviceInfo[0].water_meter_project_info?.project_id ?? null,
          user_id: null,
          water_meters: deviceSerial,
          type_id: null,
          tag_id: deviceInfo[0].water_meter_tag_info.water_meter_tag_id,
          start_time: fromDate.format("YYYY-M-D"),
          end_time: tillDate.format("YYYY-MM-DD 23:59:59"),
        },
        "post"
      ),
    queryKey: ["consumptionsDates", deviceSerial],
  });  

  return (
    <>
      <div className="projects-overview pt-2">
        <div className="mt-2 py-4 text-xl font-bold text-navy-700 dark:text-white">
          {`نمودار مصرف ${deviceInfo[0].water_meter_name}`}
        </div>

        {/* Chart Type Toggle Buttons */}
        <div className="flex justify-end gap-4 pb-4">
          <button
            className={`rounded-lg px-4 py-2 ${
              chartType === "daily"
                ? "bg-navy-700 text-white"
                : "bg-gray-200 text-gray-800"
            }`}
            onClick={() => setChartType("daily")}
          >
            نمودار مصرف روزانه
          </button>
          <button
            className={`rounded-lg px-4 py-2 ${
              chartType === "range"
                ? "bg-navy-700 text-white"
                : "bg-gray-200 text-gray-800"
            }`}
            onClick={() => setChartType("range")}
          >
            نمودار مصرف در بازه
          </button>
        </div>

        {chartType === "daily" ? (
          <div className="chart-statistics py-2">
            <ConsumptionChartFilter
              fromDate={fromDate}
              setFromDate={setFromDate}
              tillDate={tillDate}
              setTillDate={setTillDate}
              update={consumptionDatesRefetch}
              chartTag={{
                label: deviceInfo[0].water_meter_tag_info.water_meter_tag_name,
                value: deviceInfo[0].water_meter_tag_info.water_meter_tag_id,
              }}
              total={
                consumptionsDatesData?.data
                  ? consumptionsDatesData?.data?.total
                  : 0
              }
              tab="chart"
            />
          </div>
        ) : null}

        {/* Chart Types and Start Time for ApexChart */}
        {chartType === "range" && (
          <div className="flex items-center justify-between gap-4 pb-4">
            <div className="flex gap-2">
              <DateInput
                label="تاریخ شروع"
                value={startDate}
                onChange={() => {}}
                disabled={true}
              />

              <DateInput
                label="تاریخ پایان"
                value={endDate}
                onChange={setEndDate}
              />
            </div>
            <div className="flex gap-2">
              <button
                className={`rounded-lg px-4 py-2 ${
                  apexChartType === "bar"
                    ? "bg-navy-600 text-white"
                    : "bg-gray-100 text-gray-800"
                }`}
                onClick={() => setApexChartType("bar")}
              >
                bar
              </button>
              <button
                className={`rounded-lg px-4 py-2 ${
                  apexChartType === "line"
                    ? "bg-navy-600 text-white"
                    : "bg-gray-100 text-gray-800"
                }`}
                onClick={() => setApexChartType("line")}
              >
                line
              </button>
            </div>
          </div>
        )}

        {!consumptionsDatesIsLoading &&
        consumptionsDatesStatus === "success" ? (
          <div className="chart-container mx-auto h-[500px] w-full min-w-[95%]">
            {chartType === "daily" ? (
              <MixChart
                chartData={renderComplexChartData(
                  consumptionsDatesData.data,
                  fromDate,
                  tillDate
                )}
                chartOptions={renderComplexChartOptions(fromDate, tillDate)}
                chartTag={{
                  label:
                    deviceInfo[0].water_meter_tag_info.water_meter_tag_name,
                  value: deviceInfo[0].water_meter_tag_info.water_meter_tag_id,
                }}
              />
            ) : null}

            {chartType === "range" ? (
              <ApexChart
                key={`${apexChartType}-${endDate.format("YYYY-MM-DD")}`}
                project_id={
                  deviceInfo[0].water_meter_project_info?.project_id ?? null
                }
                user_id={null}
                water_meters={deviceSerial!}
                type_id={null}
                chart_type={apexChartType}
                tag_id={deviceInfo[0].water_meter_tag_info.water_meter_tag_id}
                endDate={endDate}
                setStartDate={setStartDate}
                apexSelection={apexSelection}
                setApexSelection={setApexSelection}
              />
            ) : null}
          </div>
        ) : (
          <div>chart is loading</div>
        )}
      </div>
    </>
  );
};

export default CounterConsumptionChart;
