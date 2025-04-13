import React, { useState } from "react";
import ReactDOM from "react-dom";
import ReactApexChart from "react-apexcharts";
import ApexCharts from "apexcharts";

interface ChartState {
  series: ApexAxisChartSeries;
  options: ApexCharts.ApexOptions;
  selection: string;
}

const parseDate = (dateStr: string): number => {
  return new Date(dateStr).getTime(); // "YYYY-MM-DD HH:MM:SS" works here
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
  };
};

const ApexChart: React.FC = () => {
  const [state, setState] = useState<ChartState>({
    series: [
      {
        data: [
          [parseDate("2024-08-28 06:00:00"), 30.95],
          [parseDate("2024-09-29 06:00:00"), 31.34],
          [parseDate("2024-11-30 06:00:00"), 31.18],
          [parseDate("2025-01-28 06:00:00"), 30.95],
          [parseDate("2025-01-29 06:00:00"), 31.34],
          [parseDate("2025-01-30 06:00:00"), 31.18],
          [parseDate("2025-01-31 06:00:00"), 31.05],
          [parseDate("2025-02-01 06:00:00"), 31.0],
          [parseDate("2025-02-28 06:00:00"), 30.95],
          [parseDate("2025-03-29 06:00:00"), 31.34],
          [parseDate("2025-03-30 06:00:00"), 31.18],
          [parseDate("2025-03-31 06:00:00"), 31.05],
          [parseDate("2025-04-01 06:00:00"), 31.0],
          [parseDate("2025-04-08 06:00:00"), 38.0],
          [parseDate("2025-04-12 06:00:00"), 31.0],
          [parseDate("2025-04-13 05:00:00"), 31.0],
          [parseDate("2025-04-13 08:00:00"), 38.0],
          [parseDate("2025-04-13 12:00:00"), 31.0],
        ],
      },
    ],
    options: {
      chart: {
        id: "area-datetime",
        type: "area",
        height: 350,
        zoom: {
          autoScaleYaxis: true,
        },
        offsetX: -10,
        offsetY: 10,
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
      //       x: parseDate("2025-04-11 05:00:00"), // to put a vertical line in the chart
      //       borderColor: "#999",
      //       label: {
      //         text: "شکستگی",
      //         style: {
      //           color: "#fff",
      //           background: "#775DD0",
      //         },
      //       },
      //     },
      //   ],
      // },
      dataLabels: {
        enabled: true, // False = Hiding Data
      },
      markers: {
        size: 0,
        shape: "circle",
      },
      xaxis: {
        type: "datetime",
        min: new Date(new Date().setDate(new Date().getDate() - 7)).getTime(),
        max: new Date().getTime(),
      },
      tooltip: {
        x: {
          format: "yyyy-MM-dd HH:mm:ss", // format of our time data in database
        },
      },
      fill: {
        // play with gradient colors
        type: "gradient",
        gradient: {
          shadeIntensity: 1,
          opacityFrom: 0.7,
          opacityTo: 0.9,
          stops: [0, 100],
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

    ApexCharts.exec("area-datetime", "zoomX", range.start, range.end);
  };

  return (
    <div>
      <div id="chart">
        <div className="toolbar mt-4 flex justify-end space-x-2">
          <button
            id="one_day"
            onClick={() => updateData("one_day")}
            className={`ml-2 rounded-md px-4 py-2 text-white ${
              state.selection === "one_day"
                ? "bg-blue-500"
                : "bg-gray-300 hover:bg-blue-200"
            } transition duration-300`}
          >
            1D
          </button>

          <button
            id="one_week"
            onClick={() => updateData("one_week")}
            className={`ml-2 rounded-md px-4 py-2 text-white ${
              state.selection === "one_week"
                ? "bg-blue-500"
                : "bg-gray-300 hover:bg-blue-200"
            } transition duration-300`}
          >
            1W
          </button>
          <button
            id="one_month"
            onClick={() => updateData("one_month")}
            className={`ml-2 rounded-md px-4 py-2 text-white ${
              state.selection === "one_month"
                ? "bg-blue-500"
                : "bg-gray-300 hover:bg-blue-200"
            } transition duration-300`}
          >
            1M
          </button>
          <button
            id="six_months"
            onClick={() => updateData("six_months")}
            className={`rounded-md px-4 py-2 text-white ${
              state.selection === "six_months"
                ? "bg-blue-500"
                : "bg-gray-300 hover:bg-blue-200"
            } transition duration-300`}
          >
            6M
          </button>
          <button
            id="one_year"
            onClick={() => updateData("one_year")}
            className={`rounded-md px-4 py-2 text-white ${
              state.selection === "one_year"
                ? "bg-blue-500"
                : "bg-gray-300 hover:bg-blue-200"
            } transition duration-300`}
          >
            1Y
          </button>
        </div>

        <div id="chart-timeline">
          <ReactApexChart
            options={state.options}
            series={state.series}
            type="area"
            height={350}
          />
        </div>
      </div>
      <div id="html-dist"></div>
    </div>
  );
};

export default ApexChart;
