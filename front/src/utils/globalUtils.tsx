import { Bounce, toast } from "react-toastify";
import {
  MdCloudDownload,
  MdCloudUpload,
  MdFiberSmartRecord,
  MdGpsFixed,
  // MdRemoveRedEye,
} from "react-icons/md";
import { Tooltip } from "@chakra-ui/tooltip";
import { getDatesBetween, toPersianDate } from "./TimeUtiles";

type ToastType = "err" | "info" | "success" | "warn";

export const renderToast = (message: string, type: ToastType) => {
  switch (type) {
    case "err":
      toast.error(message, {
        position: "top-left",
        autoClose: 5000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: false,
        progress: undefined,
        theme: "colored",
        transition: Bounce,
      });
      break;
    case "warn":
      toast.warn(message, {
        position: "top-left",
        autoClose: 5000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: false,
        progress: undefined,
        theme: "colored",
        transition: Bounce,
      });
      break;
    case "success":
      toast.success(message, {
        position: "top-left",
        autoClose: 5000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: false,
        progress: undefined,
        theme: "colored",
        transition: Bounce,
      });
      break;

    default:
      toast.info(message, {
        position: "top-left",
        autoClose: 5000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: false,
        progress: undefined,
        theme: "colored",
        transition: Bounce,
      });
      break;
  }
};
export const toEnglish = (persianNum: string) => {
  let numberPersian = persianNum.toString();
  let enNum = "";
  for (let i = 0; i < numberPersian.length; i++) {
    let char = numberPersian[i];
    switch (char) {
      case "۱":
        enNum += "1";
        break;
      case "۲":
        enNum += "2";
        break;
      case "۳":
        enNum += "3";
        break;
      case "۴" || "٤":
        enNum += "4";
        break;
      case "۵" || "٥":
        enNum += "5";
        break;
      case "۶" || "٦":
        enNum += "6";
        break;
      case "۷":
        enNum += "7";
        break;
      case "۸":
        enNum += "8";
        break;
      case "۹":
        enNum += "9";
        break;
      case "۰":
        enNum += "0";
        break;
      default:
        enNum += char;
    }
  }
  return enNum;
};
export const isPhoneValid = (phone: string) => {
  if (
    !isNaN(Number(toEnglish(phone))) &&
    phone.length === 11 &&
    (phone[0] === "0" || phone[0] === "۰")
  ) {
    return true;
  } else {
    return false;
  }
};
export const renderModuleAttr = (moduleAttrs: string[], uniqCode: string) => {
  return (
    <div className=" flex items-center justify-around">
      {moduleAttrs && moduleAttrs.length > 0 ? (
        <>
          {moduleAttrs.sort().map((attr, id) => (
            <Tooltip
              key={uniqCode + id}
              label={
                attr === "1"
                  ? "قابلیت ارسال اطلاعات"
                  : attr === "2"
                  ? "قابلیت دریافت اطلاعات (فرمان پذیری)"
                  : attr === "3"
                  ? "قابلیت ارسال اطلاعات مکانی (GPS)"
                  : attr === "4"
                  ? "پورت نوری"
                  : ""
              }
              fontSize="sm"
            >
              <span className=" text-lg ">
                {attr === "1" ? (
                  <MdCloudUpload color="green" />
                ) : attr === "2" ? (
                  <MdCloudDownload color="blue" />
                ) : attr === "3" ? (
                  <MdGpsFixed color="purple" />
                ) : attr === "4" ? (
                  <MdFiberSmartRecord color="orange" />
                ) : (
                  <></>
                )}
              </span>
            </Tooltip>
          ))}
        </>
      ) : (
        "__"
      )}
    </div>
  );
};
export const renderComplexChartData = (
  data: any,
  fromDate: any,
  tillDate: any
) => {
  let new_data = { ...data };
  let totalConsumption = data?.total;

  delete new_data.total;
  delete new_data.average;
  delete new_data.cumulative_consumptions;
  let chartData: { name: string; type: string; data: number[] }[] = [];
  const consumptions: number[] = [];
  const average: number[] = [];
  let datesBetween = getDatesBetween(
    fromDate.format("YYYY-MM-DD"),
    tillDate.format("YYYY-MM-DD")
  );
  let averageConsumption = totalConsumption / datesBetween.length;
  datesBetween.forEach((date) => {
    new_data[date]
      ? consumptions.push(Math.round(new_data[date]))
      : new_data[date] === 0
      ? consumptions.push(1)
      : consumptions.push(0);
    average.push(
      averageConsumption ? Math.round(Number(averageConsumption)) : 0
    );
  });
  chartData = [
    { name: "مصرف روزانه", type: "bar", data: consumptions },
    { name: "متوسط مصرف", type: "line", data: average },
  ];
  return chartData;
};
export const renderComplexChartOptions = (
  // data: any,
  fromDate: any,
  tillDate: any
) => {
  // let new_data = { ...data };
  // delete new_data.total;
  // delete new_data.average;
  // delete new_data.cumulative_consumptions;
  const chartOptions: string[] = [];
  let datesBetween = getDatesBetween(
    fromDate.format("YYYY-MM-DD"),
    tillDate.format("YYYY-MM-DD")
  );
  datesBetween.forEach((date) => {
    chartOptions.push(toPersianDate(date));
  });
  return chartOptions;
};
