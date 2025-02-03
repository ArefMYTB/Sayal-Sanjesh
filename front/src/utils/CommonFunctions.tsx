import { LastConsumptionInfo } from "views/projectInformation/ProjectCounters";
import {
  MdBattery20,
  MdBattery60,
  MdBattery90,
  MdBatteryUnknown,
  MdNetworkWifi,
  MdNetworkWifi1Bar,
  MdNetworkWifi2Bar,
  MdNetworkWifi3Bar,
  MdOutlineSignalWifiBad,
  MdPower,
  // MdRemoveRedEye,
} from "react-icons/md";
import { Tooltip } from "@chakra-ui/react";
import { DeviceObj } from "views/counters";
import { ModuleObject } from "views/warehouse/ModuleStorage";
import { DynamicOption } from "components/fields/SelectInput";
import { convertTZ, getToday } from "./TimeUtiles";
import { UserObject } from "views/users/UsersTable";
import { ProjectObject } from "views/projects";
export const renderTags = (tagName: string) => {
  return (
    <span
      className={`${
        tagName === "آب"
          ? " bg-blue-500"
          : tagName === "برق"
          ? " bg-red-500"
          : tagName === "گاز"
          ? "bg-orange-500"
          : " bg-yellow-600"
      } rounded px-2 text-sm text-white`}
    >
      {tagName}
    </span>
  );
};
export const renderCounterStatus = (status: LastConsumptionInfo) => {
  // console.log(status);
  let battery: number =
    status && status?.voltage_detail ? status.voltage_detail.Battery : 0;
  let signal: number =
    status && status?.SignalQuality ? status.SignalQuality : 0;
  let backupBattery: number =
    status && status?.voltage_detail ? status.voltage_detail.Backup : 0;
  return (
    <div className=" flex items-center justify-around">
      <Tooltip label={`${battery !== 0 ? battery : "__"} ولت`} fontSize="sm">
        {battery > 3.85 ? (
          <span className=" mx-1 rotate-90 text-xl text-blue-600">
            <MdPower />
          </span>
        ) : battery <= 3.85 && battery > 3.5 ? (
          <span className=" mx-1 rotate-90 text-xl text-green-600">
            <MdBattery90 />
          </span>
        ) : battery <= 3.5 && battery > 3.3 ? (
          <span className=" mx-1 rotate-90 text-xl text-yellow-600">
            <MdBattery60 />
          </span>
        ) : battery <= 3.3 && battery !== 0 ? (
          <span className=" mx-1 rotate-90 text-xl text-red-600">
            <MdBattery20 />
          </span>
        ) : (
          <span className=" mx-1 text-xl">
            <MdBatteryUnknown />
          </span>
        )}
      </Tooltip>
      <Tooltip label={`${signal !== 0 ? signal : "__"}`} fontSize="sm">
        {signal <= 30 && signal > 25 ? (
          <span className="  mx-1 text-xl text-green-600">
            <MdNetworkWifi />
          </span>
        ) : signal <= 25 && signal > 20 ? (
          <span className="  mx-1 text-xl text-green-600">
            <MdNetworkWifi3Bar />
          </span>
        ) : signal <= 20 && signal > 13 ? (
          <span className="  mx-1 text-xl text-yellow-600">
            <MdNetworkWifi2Bar />
          </span>
        ) : signal <= 13 && signal !== 0 ? (
          <span className="  mx-1 text-xl text-red-600">
            <MdNetworkWifi1Bar />
          </span>
        ) : (
          <span className=" mx-1 text-xl">
            <MdOutlineSignalWifiBad />
          </span>
        )}
      </Tooltip>
      <Tooltip
        label={`${backupBattery !== 0 ? backupBattery : "__"} ولت`}
        fontSize="sm"
      >
        {backupBattery > 3.7 ? (
          <span className=" mx-1 rotate-90 text-xl text-blue-600">
            <MdPower />
          </span>
        ) : backupBattery <= 3.7 && backupBattery > 3.5 ? (
          <span className=" mx-1 rotate-90 text-xl text-green-600">
            <MdBattery90 />
          </span>
        ) : backupBattery <= 3.5 && backupBattery > 3.3 ? (
          <span className=" mx-1 rotate-90 text-xl text-yellow-600">
            <MdBattery60 />
          </span>
        ) : backupBattery <= 3.3 && backupBattery !== 0 ? (
          <span className=" mx-1 rotate-90 text-xl text-red-600">
            <MdBattery20 />
          </span>
        ) : (
          <span className=" mx-1 text-xl">
            <MdBatteryUnknown />
          </span>
        )}
      </Tooltip>
    </div>
  );
};
export const renderSelectData = (
  data: any[],
  selectDataType: "user" | "project" | "module" | "counter" | "tag" | "type"
) => {
  let selectData: DynamicOption[] = [];
  switch (selectDataType) {
    case "counter":
      let counters: DeviceObj[] = data;
      counters?.forEach((obj) => {
        selectData.push({
          label: obj.water_meter_name,
          value: obj.water_meter_serial,
        });
      });
      return selectData;
    case "module":
      let modules: ModuleObject[] = data;
      modules?.forEach((obj) => {
        selectData.push({
          label: obj.water_meter_module_name,
          value: obj.water_meter_module_id,
        });
      });
      return selectData;
    case "user":
      let users: UserObject[] = data;
      users?.forEach((user) => {
        selectData.push({
          value: user.user_id,
          label: `${user.user_name} ${user.user_lastname}`,
        });
      });
      return selectData;
    case "project":
      let projects: ProjectObject[] = data;
      projects?.forEach((project) => {
        selectData.push({
          value: project.water_meter_project_id,
          label: project.water_meter_project_name,
        });
      });
      return selectData;

    default:
      return selectData;
  }
};
export const renderSendingStatus = (sendingDate: string) => {
  // console.log(sendingDate);
  let sendDate = convertTZ(sendingDate, "Asia/Tehran").split(",")[0];
  let sendDateArr = sendDate.split("/"); //[month,day,year]
  let todayDateArr = getToday().format("YYYY/M/D").split("/"); //[year,month,day]
  let delay =
    (Number(todayDateArr[0]) - Number(sendDateArr[2])) * 365 +
    (Number(todayDateArr[1]) - Number(sendDateArr[0])) * 30 +
    (Number(todayDateArr[2]) - Number(sendDateArr[1]));
  return (
    <span
      className={`${
        !sendingDate
          ? "bg-yellow-600"
          : delay === 0
          ? " bg-green-500"
          : " bg-red-500"
      } rounded p-1 text-xs text-white `}
    >
      {!sendingDate
        ? "بدون داده"
        : delay === 0
        ? "به روز"
        : `عدم ارسال (${delay} روز)`}
    </span>
  );
};
export const renderUnit = (tag: string, isKilo: boolean) => {
  let unit = "";
  if (isKilo) {
    switch (tag) {
      case "آب":
        unit = "مترمکعب";
        break;
      case "برق":
        unit = "کیلووات";
        break;
      default:
        unit = "مترمکعب";
        break;
    }
  } else {
    switch (tag) {
      case "آب":
        unit = "لیتر";
        break;
      case "برق":
        unit = "وات";
        break;
      default:
        unit = "لیتر";
        break;
    }
  }
  return unit;
};
