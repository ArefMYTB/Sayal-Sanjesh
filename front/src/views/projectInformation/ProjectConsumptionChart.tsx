import { useState } from "react";
import { reqFunction } from "utils/API";
import ConsumptionChartFilter from "./ConsumptionChartFilter";
import { DynamicOption } from "components/fields/SelectInput";
import { counterTagSelect } from "variables";
import { ProjectObject } from "views/projects";
import { getToday } from "utils/TimeUtiles";
import { useQuery } from "@tanstack/react-query";
import MixChart from "components/charts/MixChart";
import { useParams } from "react-router-dom";
import {
  renderComplexChartData,
  renderComplexChartOptions,
} from "utils/globalUtils";
interface ProjectConsumptionChartProps {
  projectData: [ProjectObject];
}
const ProjectConsumptionChart = (props: ProjectConsumptionChartProps) => {
  // const id = useId();
  const { projectId } = useParams();
  // const {
  //    projectData
  //    } = props;
  const [tag, setTag] = useState<DynamicOption>(counterTagSelect[0]);
  const [fromDate, setFromDate] = useState(getToday().subtract(20, "day"));
  const [tillDate, setTillDate] = useState(getToday().add(1, "day"));
  // const [total, setTotal] = useState<number>(0);
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
          project_id: projectId,
          user_id: null,
          water_meters: null,
          type_id: null,
          tag_id: tag.value,
          start_time: fromDate.format("YYYY-M-D"),
          end_time: tillDate.format("YYYY-M-D"),
        },
        "post"
      ),
    queryKey: ["consumptionsDates", projectId, tag],
  });
  return (
    <>
      <div className="projects-overview pt-4">
        {/* <div className="mt-2 py-4 text-xl font-bold text-navy-700 dark:text-white">
          نمودار مصرف
        </div> */}
        <div className="chart-statistics py-2">
          <ConsumptionChartFilter
            tagSelect={counterTagSelect}
            tag={tag}
            setTag={setTag}
            fromDate={fromDate}
            setFromDate={setFromDate}
            tillDate={tillDate}
            setTillDate={setTillDate}
            update={consumptionDatesRefetch}
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
          <div className="chart-container mx-auto h-[450px] w-full min-w-[95%]">
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
          <div>chart is loading</div>
        )}
      </div>
    </>
  );
};
export default ProjectConsumptionChart;
