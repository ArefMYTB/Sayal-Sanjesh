import { reqFunction } from "utils/API";
import ConsumptionChartFilter from "./ConsumptionChartFilter";
import { useQuery } from "@tanstack/react-query";
import MixChart from "components/charts/MixChart";
import { useParams } from "react-router-dom";
import { OneDeviceObj } from ".";
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
          project_id: deviceInfo[0].water_meter_project_info?.project_id
            ? deviceInfo[0].water_meter_project_info.project_id
            : null,
          user_id: null,
          water_meters: deviceSerial,
          type_id: null,
          tag_id: deviceInfo[0].water_meter_tag_info.water_meter_tag_id,
          start_time: fromDate.format("YYYY-M-D"),
          end_time: tillDate.format("YYYY-M-D"),
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
        {!consumptionsDatesIsLoading &&
        consumptionsDatesStatus === "success" ? (
          <div className="chart-container mx-auto h-[500px] w-full min-w-[95%]">
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
              chartTag={{
                label: deviceInfo[0].water_meter_tag_info.water_meter_tag_name,
                value: deviceInfo[0].water_meter_tag_info.water_meter_tag_id,
              }}
            />
          </div>
        ) : (
          <div>chart is loading</div>
        )}
      </div>
    </>
  );
};
export default CounterConsumptionChart;
