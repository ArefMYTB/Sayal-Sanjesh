import { ApexOptions } from "apexcharts";
import { DynamicOption } from "components/fields/SelectInput";
import Chart from "react-apexcharts";
import DownloadIcon from "../../assets/img/avatars/cloud-computing.png";
import { useContext } from "react";
import { ThemeContext } from "ThemeProvider";
import { renderUnit } from "utils/CommonFunctions";

type ChartProps = {
  chartData: { name: string; type: string; data: number[] }[];
  chartOptions: string[];
  chartTag: DynamicOption;
  isComparison?: boolean;
};

const MixChart = (props: ChartProps) => {
  const { chartData, chartOptions, chartTag, isComparison } = props;
  const { isDark } = useContext(ThemeContext);
  const renderColors = (chartTag: DynamicOption) => {
    let colors: string[] = [];
    chartTag.label === "آب"
      ? (colors = ["#3b82f6", "#f53939"])
      : chartTag.label === "برق"
      ? (colors = ["#f53939", "#17ad37"])
      : (colors = ["#f97316", "#3b82f6"]);
    return colors;
  };
  let options: ApexOptions = {
    chart: {
      stacked: isComparison ? true : false,
      stackOnlyBar: true,
      type: "line",
      height: 450,
      fontFamily: "Vazir",
      toolbar: {
        show: true,
        offsetX: 0,
        offsetY: 0,
        tools: {
          download: `<img src="${DownloadIcon}" class="w-16" width="64px">`,
          selection: false,
          zoom: false,
          zoomin: false,
          zoomout: false,
          pan: false,
          reset: false,
        },
        export: {
          png: {
            filename: undefined,
          },
        },
      },
      locales: [
        {
          name: "fa",
          options: {
            toolbar: {
              download: "دانلود نمودار",
              exportToSVG: "دریافت SVG",
              exportToPNG: "دریافت تصویر",
              exportToCSV: "دریافت اکسل",
            },
          },
        },
      ],
      defaultLocale: "fa",
    },
    colors: isComparison ? [] : renderColors(chartTag),
    markers: {
      size: [1, 2],
    },
    theme: {
      mode: isDark ? "dark" : "light",
      palette: "palette1",
      monochrome: {
        enabled: false,
        color: "#255aee",
        shadeTo: "light",
        shadeIntensity: 0.65,
      },
    },
    stroke: {
      width: isComparison ? [3, 5] : [0.5, 1],
    },
    // dataLabels: {
    //   enabled: true,
    //   enabledOnSeries: [1],
    // },
    legend: {
      position: "top",
    },
    dataLabels: {
      enabled: false,
    },
    xaxis: {
      categories: chartOptions,
      labels: {
        style: {
          fontFamily: "Vazir",
          cssClass: "axisXLabel",
        },
      },
    },
    yaxis: {
      title: {
        text: renderUnit(chartTag.label, false),
      },
    },
    fill: {
      opacity: 1,
    },
    tooltip: {
      y: {
        formatter: function (val: any) {
          return `${val.toLocaleString()} ${renderUnit(chartTag.label, false)}`;
        },
      },
    },
  };
  return (
    <Chart
      options={options}
      series={chartData}
      type="line"
      width="100%"
      height="100%"
    />
  );
};

export default MixChart;
