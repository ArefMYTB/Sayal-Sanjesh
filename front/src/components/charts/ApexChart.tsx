import React, { useState, useEffect } from "react";
import ReactApexChart from "react-apexcharts";
import ApexCharts from "apexcharts";
import { useQuery } from "@tanstack/react-query";
import { reqFunction } from "utils/API";

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
  date.setMinutes(date.getMinutes() + 210); // add 3.5 hours = 210 minutes bc of time difference
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
    startFormatted: start.toISOString().split("T")[0] + " 00:00:00",
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
        enabled: false, // False = Hiding Data
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
      yaxis: {
        labels: {
          formatter: (value: number) =>
            (Math.round(value / 10) * 10).toString(), // round y-axis to 10
        },
      },
      tooltip: {
        x: {
          format: "yyyy-MM-dd HH:mm:ss", // format of our time data in database
        },
      },
      // fill: {
      //   // play with gradient colors
      //   type: "gradient",
      //   gradient: {
      //     shadeIntensity: 1,
      //     opacityFrom: 0.7,
      //     opacityTo: 0.9,
      //     stops: [0, 100],
      //   },
      // },
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

    setTimeRange(range); // ← triggers refetch
    ApexCharts.exec("area-datetime", "zoomX", range.start, range.end);
  };

  const {
    data: consumptionsDatesData,
    isLoading: consumptionsDatesIsLoading,
    status: consumptionsDatesStatus,
  } = useQuery({
    queryFn: () =>
      reqFunction(
        "watermeters/admin/getAll/consumption/chart",
        {
          page: 1,
          count: 1000,
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
          {[
            ["one_day", "1D"],
            ["one_week", "1W"],
            ["one_month", "1M"],
            ["six_months", "6M"],
            ["one_year", "1Y"],
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

        <div id="chart-timeline">
          <ReactApexChart
            options={state.options}
            series={state.series}
            type={chart_type}
            height={350}
          />
        </div>
      </div>
      <div id="html-dist"></div>
    </div>
  );
};

export default ApexChart;
