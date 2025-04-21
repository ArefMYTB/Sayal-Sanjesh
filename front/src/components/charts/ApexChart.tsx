import React, { useState, useEffect } from "react";
import ReactApexChart from "react-apexcharts";
import ApexCharts from "apexcharts";
import { useQuery } from "@tanstack/react-query";
import { reqFunction } from "utils/API";
import moment from "moment-jalaali";

interface ChartState {
  series: ApexAxisChartSeries;
  options: ApexCharts.ApexOptions;
  selection: string;
}

interface ApexChartProps {
  project_id: string | null;
  user_id?: number | null;
  water_meters: string;
  type_id?: number | null;
  chart_type?: "line" | "bar";
  tag_id: string;
}

const parseDate = (dateStr: string): number => {
  // "YYYY-MM-DD HH:MM:SS" works here
  const date = new Date(dateStr);
  return date.getTime();
};

// Time Range for Chart Data
const getTimeRange = (range: "1D" | "1W" | "1M" | "6M" | "1Y") => {
  const now = new Date();
  const end = now.getTime();

  const start = new Date(now);
  if (range === "1D") start.setDate(now.getDate() - 1);
  if (range === "1W") start.setDate(now.getDate() - 7);
  if (range === "1M") start.setMonth(now.getMonth() - 1);
  if (range === "6M") start.setMonth(now.getMonth() - 6);
  if (range === "1Y") start.setFullYear(now.getFullYear() - 1);

  return {
    start: start.getTime(),
    end,
    startFormatted: start.toISOString().split("T")[0] + " 20:30:00",
    endFormatted: now.toISOString().split("T")[0] + " 20:29:00",
  };
};

const ApexChart: React.FC<ApexChartProps> = ({
  project_id,
  user_id = null,
  water_meters,
  type_id = null,
  chart_type,
  tag_id,
}) => {
  const [timeRange, setTimeRange] = useState(getTimeRange("1W")); // default to 1 week
  const [isZoomedIn, setIsZoomedIn] = useState(false);
  const [state, setState] = useState<ChartState>({
    series: [
      {
        data: [],
      },
    ],
    options: {
      chart: {
        id: "area-datetime",
        type: chart_type, // line or bar
        height: 350,
        zoom: {
          autoScaleYaxis: true,
        },
        events: {
          zoomed: function (chartContext, { xaxis }) {
            const zoomDuration = xaxis.max - xaxis.min;

            // If zoom range is less than 1 day → show time
            setIsZoomedIn(zoomDuration < 24 * 60 * 60 * 1000);
          },
          beforeResetZoom: () => {
            setIsZoomedIn(false);
          },
        },
        offsetX: -10,
        offsetY: 10,
        toolbar: {
          show: true,
          tools: {
            download: true,
          },
          export: {
            csv: {
              dateFormatter(timestamp: number) {
                return moment(timestamp).format("jYYYY/jMM/jDD HH:mm:ss");
              },
            },
            // png: {
            //   filename: "chart",
            // },
          },
        },
      },
      // annotations: {
      //   yaxis: [
      //     {
      //       y: 30,
      //       borderColor: "#999",
      //       label: {
      //         text: "Support",
      //         style: {
      //           color: "#fff",
      //           background: "#00E396",
      //         },
      //       },
      //     },
      //   ],
      //   xaxis: [
      //     {
      //       x: parseDate("2025-04-21 05:00:00"), // to put a vertical line in the chart
      //       borderColor: "#999",
      //       label: {
      //         text: "شکستگی",
      //         style: {
      //           color: "#fff",
      //           background: "#775DD0",
      //           fontSize: "18",
      //         },
      //       },
      //     },
      //   ],
      // },
      dataLabels: {
        enabled: false, // False = Hiding Data
      },
      markers: {
        size: 0,
        shape: "circle",
      },
      xaxis: {
        type: "datetime",
        labels: {
          formatter: function (val: string) {
            return moment(val).format("jMM/jDD HH:mm:SS");
          },
        },
        min: timeRange.start,
        max: timeRange.end,
      },
      yaxis: {
        labels: {
          formatter: (value: number) =>
            (Math.round(value / 10) * 10).toString(), // round y-axis to 10
        },
      },
      tooltip: {
        x: {
          formatter: (timestamp: number) => {
            return moment(timestamp).format("jYYYY/jMM/jDD HH:mm");
          },
        },
      },
      grid: {
        padding: {
          left: 50, // creates spacing between y-axis and chart area
          right: 10,
        },
      },
    },
    selection: "one_week", // default
  });

  useEffect(() => {
    // Trigger chart update when zoom level changes
    ApexCharts.exec("area-datetime", "updateOptions", {
      xaxis: {
        labels: {
          formatter: function (val: string) {
            return isZoomedIn
              ? moment(+val).format("HH:mm") // Just show time when zoomed in
              : moment(+val).format("jMM/jDD HH:mm"); // Show date in Jalali format when zoomed out
          },
        },
      },
    });
  }, [isZoomedIn]);

  const updateData = (timeline: string) => {
    setState((prev) => ({
      ...prev,
      selection: timeline,
    }));

    let range;
    switch (timeline) {
      case "one_day":
        range = getTimeRange("1D");
        break;
      case "one_week":
        range = getTimeRange("1W");
        break;
      case "one_month":
        range = getTimeRange("1M");
        break;
      case "six_months":
        range = getTimeRange("6M");
        break;
      case "one_year":
        range = getTimeRange("1Y");
        break;
      default:
        return;
    }

    setTimeRange(range); // ← triggers refetch
    ApexCharts.exec("area-datetime", "zoomX", range.start, range.end);
  };

  const {
    data: consumptionsDatesData,
    // isLoading: consumptionsDatesIsLoading,
    // status: consumptionsDatesStatus,
  } = useQuery({
    queryFn: () =>
      reqFunction(
        "watermeters/admin/getAll/consumption/chart",
        {
          project_id: project_id,
          user_id: null,
          water_meters: water_meters,
          type_id: null,
          tag_id: tag_id,
          start_time: timeRange.startFormatted,
          end_time: timeRange.endFormatted,
        },
        "post"
      ),
    queryKey: [
      "consumptionsDates",
      water_meters,
      tag_id,
      timeRange.startFormatted,
      timeRange.endFormatted,
    ],
  });

  useEffect(() => {
    if (consumptionsDatesData && Array.isArray(consumptionsDatesData.data)) {
      const formattedData = consumptionsDatesData.data.map((item: any) => [
        parseDate(item.create_time),
        item.value,
      ]);

      setState((prev) => ({
        ...prev,
        series: [{ data: formattedData }],
      }));
    }
  }, [consumptionsDatesData]);

  useEffect(() => {
    setState((prev) => ({
      ...prev,
      options: {
        ...prev.options,
        chart: {
          ...prev.options.chart,
          type: chart_type, // dynamically update chart type
        },
      },
    }));
  }, [chart_type]);

  return (
    <div>
      <div id="chart">
        <div className="toolbar mt-4 flex justify-end space-x-2">
          <div>
            {[
              ["one_day", "1D"],
              ["one_week", "1W"],
              // ["one_month", "1M"],
              // ["six_months", "6M"],
              // ["one_year", "1Y"],
            ].map(([key, label]) => (
              <button
                key={key}
                onClick={() => updateData(key)}
                className={`ml-2 rounded-md px-4 py-2 text-white ${
                  state.selection === key
                    ? "bg-blue-500"
                    : "bg-gray-300 hover:bg-blue-200"
                } transition duration-300`}
              >
                {label}
              </button>
            ))}
          </div>
        </div>

        <div id="chart-timeline">
          <ReactApexChart
            options={state.options}
            series={state.series}
            type={chart_type}
            height={550}
          />
        </div>
      </div>
      <div id="html-dist"></div>
    </div>
  );
};

export default ApexChart;

// generate annotations:

// const generateDayStartAnnotations = (start: number, end: number) => {
//   const dayMs = 24 * 60 * 60 * 1000;
//   let annotations = [];

//   let current = moment(start).startOf("day");
//   while (current.valueOf() < end) {
//     annotations.push({
//       x: current.valueOf(),
//       borderColor: "#e0e0e0",
//       label: {
//         text: current.format("jMM/jDD"),
//         style: {
//           fontSize: "10px",
//         },
//       },
//     });
//     current = current.add(1, "day");
//   }

//   return annotations;
// };
// in options
// annotations: {
//   xaxis: [...generateDayStartAnnotations(timeRange.start, timeRange.end)],
// },
