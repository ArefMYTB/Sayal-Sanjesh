import { useQuery } from "@tanstack/react-query";
import { DynamicOption } from "components/fields/SelectInput";
import { useState } from "react";
import { reqFunction } from "utils/API";
import { getDatesBetween, getToday } from "utils/TimeUtiles";
import { counterTagSelect } from "variables";
import ComparisonFilter from "./ComparisonFilters";
import { ProjectObject } from "views/projects";
import Loading from "components/loading";
import { DeviceObj } from "views/counters";
import { renderComplexChartOptions, renderToast } from "utils/globalUtils";
import MixChart from "components/charts/MixChart";

const ConsumptionComparison = () => {
  const [fromDate, setFromDate] = useState(getToday().jDate(1));
  const [tillDate, setTillDate] = useState(getToday().add(1, "day"));
  const [project, setProject] = useState<DynamicOption>(null);
  const [tag, setTag] = useState<DynamicOption>(counterTagSelect[0]);
  const [counter, setCounter] = useState<DynamicOption>(null);
  const [otherCounters, setOtherCounters] = useState<DynamicOption[]>([]);
  const [chartLoading, setChartloading] = useState<boolean>(false);
  const [comparisonData, setComparisonData] = useState<any>({});
  //projects
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
  const renderProjectSelect = (projectList: ProjectObject[]) => {
    let projectSelect: DynamicOption[] = [];
    projectList.forEach((project) => {
      projectSelect.push({
        value: project.water_meter_project_id,
        label: project.water_meter_project_name,
      });
    });
    return projectSelect;
  };
  //counters
  const {
    data: devicesData,
    isLoading: devicesIsLoading,
    status: devicesStatus,
    // refetch: deviceRefetch,
  } = useQuery({
    queryFn: () =>
      reqFunction("watermeters/v2/admin/getAll", {
        page: 1,
        count: 1000,
        user_id: null,
        project_id: project ? project.value : null,
        water_meter_serial: null,
      }),
    queryKey: ["deviceList", project],
  });
  const renderCounterSelectData = () => {
    let selectData: DynamicOption[] = [];
    if (!devicesIsLoading && devicesStatus === "success" && project) {
      let filteredCounter = devicesData.data.filter(
        (device: DeviceObj) =>
          device.water_meter_type__water_meter_tag__water_meter_tag_id ===
          tag.value
      );
      filteredCounter.length > 0
        ? filteredCounter.forEach((counter: DeviceObj) => {
            selectData.push({
              label: counter.water_meter_name,
              value: counter.water_meter_serial,
            });
          })
        : (selectData = []);
    }
    return selectData;
  };
  const renderOtherCounterSelectData = () => {
    let selectData: DynamicOption[] = [];
    if (!devicesIsLoading && devicesStatus === "success" && counter) {
      let filteredCounter = devicesData.data.filter(
        (device: DeviceObj) =>
          device.water_meter_type__water_meter_tag__water_meter_tag_id ===
          tag.value
      );
      filteredCounter.length > 0
        ? filteredCounter
            .filter(
              (device: DeviceObj) => device.water_meter_serial !== counter.value
            )
            .forEach((device: DeviceObj) => {
              selectData.push({
                label: device.water_meter_name,
                value: device.water_meter_serial,
              });
            })
        : (selectData = []);
    }
    return selectData;
  };
  const getCountersSerial = () => {
    let serials: string[] | any = [];
    serials.push(counter.value);
    otherCounters.forEach((c) => serials.push(c.value));
    return serials;
  };
  const getName = (serial: string) => {
    let countersSelect: DynamicOption[] = renderCounterSelectData();
    return countersSelect.filter((device) => device.value === serial)[0].label;
  };
  const renderChartData = () => {
    let new_data = { ...comparisonData };
    let chartData: { name: string; type: string; data: number[] }[] = [];
    let serials: string[] =
      counter && otherCounters.length > 0 ? getCountersSerial() : [];
    let datesBetween = getDatesBetween(
      fromDate.format("YYYY-MM-DD"),
      tillDate.format("YYYY-MM-DD")
    );
    serials.reverse();
    serials.forEach((serial, index) => {
      let consumptions: number[] = [];
      let data = new_data[serial] ?? {};
      datesBetween.forEach((date) => {
        data[date]
          ? consumptions.push(Math.round(data[date]))
          : consumptions.push(0);
      });
      chartData.push({
        name: getName(serial),
        type: index === serials.length - 1 ? "line" : "bar",
        data: consumptions,
      });
    });

    return chartData.reverse();
    // return chartData;
  };
  const compaireCounters = async () => {
    setChartloading(true);
    const response = await reqFunction(
      "watermeters/admin/getAll/consumption/date/meter",
      {
        water_meters_list: getCountersSerial(),
        start_time: fromDate.format("YYYY-MM-DD"),
        end_time: tillDate.format("YYYY-MM-DD"),
      }
    );
    if (response.code === 200) {
      setComparisonData(response.data);
      setChartloading(false);
    } else {
      setChartloading(false);
      renderToast(
        response?.farsi_message
          ? response.farsi_message
          : "در دریافت اطلاعات خطایی رخ داده",
        "err"
      );
    }
  };
  return (
    <div className="">
      {!projectsIsLoading && projectsStatus === "success" ? (
        <ComparisonFilter
          tag={tag}
          setTag={setTag}
          tagSelect={counterTagSelect}
          project={project}
          setProject={setProject}
          projectSelect={renderProjectSelect(projectsData.data)}
          fromDate={fromDate}
          setFromDate={setFromDate}
          tillDate={tillDate}
          setTillDate={setTillDate}
          counterSelect={renderCounterSelectData()}
          counter={counter}
          setCounter={setCounter}
          otherCountersSelect={renderOtherCounterSelectData()}
          otherCounters={otherCounters}
          setOtherCounters={setOtherCounters}
          compaire={compaireCounters}
        />
      ) : (
        <Loading />
      )}
      {Object.keys(comparisonData).length === 0 ? (
        <></>
      ) : chartLoading ? (
        <Loading />
      ) : (
        <>
          <div className="chart-container mx-auto h-[500px] w-full min-w-[95%]">
            <MixChart
              chartData={renderChartData()}
              chartOptions={renderComplexChartOptions(fromDate, tillDate)}
              chartTag={tag}
              isComparison={true}
            />
          </div>
        </>
      )}
    </div>
  );
};
export default ConsumptionComparison;
