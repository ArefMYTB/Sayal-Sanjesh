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
  endDate: any;
  setStartDate: (value: any) => void;
  apexSelection: "one_day" | "one_week";
  setApexSelection: React.Dispatch<React.SetStateAction<"one_day" | "one_week">>;
}

const parseDate = (dateStr: string): number => {
  // "YYYY-MM-DD HH:MM:SS" works here
  const date = new Date(dateStr);
  return date.getTime();
};

// Time Range for Chart Data
const getTimeRange = (range: "1D" | "1W" | "1M" | "6M" | "1Y", baseDate: Date) => {
  const now = new Date(baseDate);
  const end = now.getTime();

  const start = new Date(now);
  if (range === "1D") start.setDate(now.getDate() - 1);
  if (range === "1W") start.setDate(now.getDate() - 7);
  // if (range === "1M") start.setMonth(now.getMonth() - 1);
  // if (range === "6M") start.setMonth(now.getMonth() - 6);
  // if (range === "1Y") start.setFullYear(now.getFullYear() - 1);

  return {
    start: start.getTime(),
    end,
    startFormatted: start.toISOString().split("T")[0] + " 20:30:00", // from 00:00:00
    endFormatted: now.toISOString().split("T")[0] + " 20:29:59", // till 23:59:59
  };
};

const ApexChart: React.FC<ApexChartProps> = ({
  project_id,
  user_id = null,
  water_meters,
  type_id = null,
  chart_type,
  tag_id,
  endDate,
  setStartDate,
  apexSelection, 
  setApexSelection,
}) => {
  const [timeRange, setTimeRange] = useState(getTimeRange(apexSelection === "one_day" ? "1D" : "1W", endDate));
  const [isZoomedIn, setIsZoomedIn] = useState(false);
  // Yaxis annotations for separating dates
  const generateDayStartAnnotations = (start: number, end: number) => {
    const dayMs = 24 * 60 * 60 * 1000;
    let annotations = [];
    let current = moment(start).startOf("day");
    while (current.valueOf() < end) {
      annotations.push({
        x: current.valueOf(),
        borderColor: "#e0e0e0",
        label: {
          text: current.format("jMM/jDD"),
          style: {
            fontSize: "12px",
          },
        },
      });
      current = current.add(1, "day");
    }
    return annotations;
  };

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
            setIsZoomedIn(zoomDuration < 72 * 60 * 60 * 1000);
          },
          beforeResetZoom: () => {
            setIsZoomedIn(false);
          },
        },
        // offsetX: -10,
        // offsetY: 10,
        // Tools: Download + Zoom in&out + Hand
        toolbar: {
          show: true,
          tools: {
            pan: false,
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
      annotations: {
        xaxis: [...generateDayStartAnnotations(timeRange.start, timeRange.end)],
      },

      dataLabels: {
        enabled: false, // False = Hiding Data
      },
      markers: {
        size: 0,
        shape: "circle",
      },
      xaxis: {
        type: "datetime",
        // labels: {
        //   formatter: function (val: string) {
        //     return moment(val).format("jMM/jDD HH:mm:SS");
        //   },
        // },
        min: timeRange.start,
        max: timeRange.end,
        
        tickAmount: 24,
          
      },
      yaxis: {
        labels: {
          formatter: (value: number) =>
            (Math.round(value / 10) * 10).toString(), // round y-axis to 10
        },
      },
      // on hover
      tooltip: {
        x: {
          formatter: (timestamp: number) => {
            return moment(timestamp).format("jYYYY/jMM/jDD HH:mm");
          },
        },
        y: {
          formatter: function (value: number) {
            return `${value} لیتر`;
          },
          title: {
            formatter: () => "",
          },
        },
        marker: {
          show: false,
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

  // Trigger chart update when zoom level changes
  useEffect(() => {
    ApexCharts.exec("area-datetime", "updateOptions", {
      xaxis: {
        labels: {
          formatter: function (val: string) {
            const date = moment(+val);
  
            if (isZoomedIn) {
              // Round to the nearest 30 minutes
              const minutes = date.minutes();
              const rounded = minutes < 15
                ? date.minutes(0)
                : minutes < 45
                ? date.minutes(30)
                : date.add(1, "hour").minutes(0);
  
              return rounded.format("HH:mm");
            } else {
              return ""; // or return date.format("jMM/jDD") if you want to show dates when zoomed out
            }
          },
        },
      },
    });
  }, [isZoomedIn]);

  // Data per Time Range
  const updateData = (timeline: "one_day" | "one_week") => {
    setApexSelection(timeline);
    setState((prev) => ({
      ...prev,
      selection: timeline,
    }));

    let range;
    switch (timeline) {
      case "one_day":
        range = getTimeRange("1D", endDate);
        break;
      case "one_week":
        range = getTimeRange("1W", endDate);
        break;
      // case "one_month":
      //   range = getTimeRange("1M", endDate);
      //   break;
      // case "six_months":
      //   range = getTimeRange("6M");
      //   break;
      // case "one_year":
      //   range = getTimeRange("1Y");
      //   break;
      default:
        return;
    }

    setTimeRange(range); // ← triggers refetch
    setStartDate(moment(range.start).add(1, "day"));
    ApexCharts.exec("area-datetime", "zoomX", range.start, range.end);
  };

  // remember my choice
  // useEffect(() => {
  //   const range = getTimeRange(apexSelection === "one_day" ? "1D" : "1W", endDate);
  //   setTimeRange(range);
  // }, [endDate, apexSelection]);  
  useEffect(() => {
    // ensure correct time range is applied when endDate changes
    updateData(apexSelection); 
  }, [endDate]);
  

  // Get data
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

  // Get Time (in Sec) and Value for consumption data
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
  
  // dynamically update chart type
  useEffect(() => {
    setState((prev) => ({
      ...prev,
      options: {
        ...prev.options,
        chart: {
          ...prev.options.chart,
          type: chart_type,
        },
      },
    }));
  }, [chart_type]);

  // make sure all data in xaxix and yaxix are shown
  useEffect(() => {
    if (consumptionsDatesData && Array.isArray(consumptionsDatesData.data)) {
      const formattedData = consumptionsDatesData.data.map((item: any) => [
        parseDate(item.create_time),
        item.value,
      ]);
  
      if (formattedData.length === 0) return;
  
      // Find min and max for x and y axis
      const allX = formattedData.map((item: any) => item[0]);
      const allY = formattedData.map((item: any) => item[1]);
      const minX = Math.min(...allX);
      const maxX = Math.max(...allX);
      const minY = Math.min(...allY);
      const maxY = Math.max(...allY);
  
      setState((prev) => ({
        ...prev,
        series: [{ data: formattedData }],
        options: {
          ...prev.options,
          // xaxis: {
          //   ...prev.options.xaxis,
          //   min: Math.min(timeRange.start, minX) - 1000 * 60, // add small padding (1 min)
          //   max: Math.max(timeRange.end, maxX) + 1000 * 60,   // add small padding (1 min)
          // },
          xaxis: {
            ...prev.options.xaxis,
            min: minX,
            max: maxX,
          },
          yaxis: {
            ...prev.options.yaxis,
            min: Math.floor(minY * 0.9),  // 10% margin at bottom
            max: Math.ceil(maxY * 1.1),   // 10% margin at top
            forceNiceScale: true,
          },
        },
      }));
    }
  }, [consumptionsDatesData]);

  // re-render annotations
  useEffect(() => {
    if (!state.series[0].data || state.series[0].data.length === 0) return;
  
    const allX = state.series[0].data.map((item: any) => item[0]);
    const minX = Math.min(...allX);
    const maxX = Math.max(...allX);
  
    ApexCharts.exec("area-datetime", "updateOptions", {
      annotations: {
        xaxis: generateDayStartAnnotations(minX, maxX),
      },
    }, false, true);
  }, [state.series]);
  
  

  return (
    <div>
      <div id="chart">
        <div className="toolbar mt-4 mb-4 flex justify-start space-x-2">
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
                onClick={() => updateData(key as "one_day" | "one_week")}
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
