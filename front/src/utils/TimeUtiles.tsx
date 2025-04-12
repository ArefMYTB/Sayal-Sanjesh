import moment from "moment-jalaali";
type ToPersianDate = (date: Date | string) => string;
type RenderJalaliTime = (
  date: null | string,
  type?: "normal" | "chart",
  tz?: string
) => JSX.Element;

export const toPersianDate: ToPersianDate = (date) => {
  return moment(date, "YYYY-M-D HH:mm:ss").format("jYYYY/jM/jD");
};
export const getToday = (
  date?: Date | string,
  type: "local" | "utc" = "local"
) => {
  return type === "local" ? moment(date) : moment(date).utc();
};
export const renderTimeJalali: RenderJalaliTime = (
  date,
  type: string = "normal",
  tz: string = "Asia/Tehran"
) => {
  if (date) {
    let converted = convertTZ(date, tz).split(",");
    // //console.log("converted :", converted);
    let convertedDate = converted[0].split("/"); //[month,day,year]

    let newDateFormat = `${convertedDate[2]}-${convertedDate[0]}-${convertedDate[1]}`;
    // //console.log("newDateFormat :", newDateFormat);
    let convertedTimeArray = converted[1].split(" ");
    // //console.log("convertedTimeArray :", convertedTimeArray);
    let convertedTime = converted[1].split(" ")[1];
    let newConvertedTime = "";
    const addPm = () => {
      let time = convertedTime.split(":");
      newConvertedTime = `${
        Number(time[0]) !== 12 ? Number(time[0]) + 12 : Number(time[0])
      }:${time[1]}:${time[2]}`;
    };
    const checkAm = () => {
      let time = convertedTime.split(":");
      newConvertedTime = `${
        Number(time[0]) === 12 ? Number(time[0]) - 12 : Number(time[0])
      }:${time[1]}:${time[2]}`;
    };
    convertedTimeArray[2] === "PM" ? addPm() : checkAm();
    // //console.log("convertedTimeNew :", newConvertedTime);
    let jalaliTime = moment(
      date
        ? type === "normal"
          ? date
          : `${newDateFormat}T${newConvertedTime}`
        : "2013-8-25T16:40:00",
      "YYYY-M-DTHH:mm:ss"
    ).format("jYYYY/jM/jDTHH:mm:ss");
    let timeArray = jalaliTime.split("T");
    return (
      <>
        <span style={{ whiteSpace: "nowrap" }}>{timeArray[0]}</span>
        <br />
        <span style={{ whiteSpace: "nowrap" }}>{timeArray[1]}</span>
      </>
    );
  } else {
    return <span>__</span>;
  }
};
export const convertTZ = (date: any, tzString: string) => {
  return new Date(date).toLocaleString("en-US", { timeZone: tzString });
};
export const getDatesBetween = (from: string, till: string) => {
  const dates: string[] = [];
  let currentDate = new Date(from);
  const endDateObj = new Date(till);

  while (currentDate <= endDateObj) {
    const formattedDate = currentDate.toISOString().split("T")[0];
    dates.push(formattedDate);
    currentDate.setDate(currentDate.getDate() + 1);
  }

  return dates;
};
function pad(d: number) {
  return d < 10 ? "0" + d.toString() : d.toString();
}
export const getDiffrenceInHours = (from: string, till: string) => {
  let fromDateObject = moment(from, "YYYY-MM-DD HH:mm:ss");
  let tillDateObject = moment(till, "YYYY-MM-DD HH:mm:ss");
  let duration = moment.duration(tillDateObject.diff(fromDateObject));
  let durationData: {
    days: number;
    hours: number;
    minutes: number;
    seconds: number;
  } = duration._data;
  let sampledTime = `${pad(durationData.days * 24 + durationData.hours)}:${pad(
    durationData.minutes
  )}:${pad(durationData.seconds)}`;
  return from && till ? sampledTime : "__";
};
