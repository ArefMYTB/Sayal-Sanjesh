import { ApexOptions } from "apexcharts";
import Chart from "react-apexcharts";
import DownloadIcon from "../../assets/img/avatars/cloud-computing.png";
import { useContext } from "react";
import { ThemeContext } from "ThemeProvider";

type ChartProps = {
  chartData: { name: string; data: number[] }[];
  chartOptions: string[];
};

const MultiColumnsChart = (props: ChartProps) => {
  const { chartData, chartOptions } = props;
  const { isDark } = useContext(ThemeContext);
  let options: ApexOptions = {
    chart: {
      type: "bar",
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
    legend: {
      position: "top",
    },
    plotOptions: {
      bar: {
        horizontal: false,
        columnWidth: "55%",
        // endingShape: 'rounded'
      },
    },
    dataLabels: {
      enabled: false,
    },
    stroke: {
      show: true,
      width: 2,
      colors: ["transparent"],
    },
    xaxis: {
      categories: chartOptions,
      labels: {
        style: {
          cssClass: "chart-chart",
        },
      },
    },
    yaxis: {
      title: {
        text: "عدد",
      },
    },
    fill: {
      opacity: 1,
    },
    tooltip: {
      y: {
        formatter: function (val: any) {
          return val + " عدد";
        },
      },
    },
  };
  return (
    <Chart
      options={options}
      series={chartData}
      type="bar"
      width="100%"
      height="100%"
    />
  );
};

export default MultiColumnsChart;
