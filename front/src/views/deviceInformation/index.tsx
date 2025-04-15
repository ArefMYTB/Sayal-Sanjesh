import { useQuery } from "@tanstack/react-query";
import Card from "components/card";
import CustomTabs from "components/tabs";
import { useParams } from "react-router-dom";
import { reqFunction } from "utils/API";
import DeviceInformation from "./DeviceInformation";
import { useState } from "react";
import { getToday } from "utils/TimeUtiles";
import CounterConsumptionChart from "./CounterConsumptionChart";
import ConsumptionRecords from "./ConsumptionRecords";
import CounterBills from "./CounterBills";
import DeviceEvents from "./DeviceEvents";
export type OneDeviceObj = {
  water_meter_name: string;
  water_meter_serial: string;
  water_meter_location:
    | string
    | null
    | { lat: string | number; lng: string | number };
  water_meter_validation: number | null;
  water_meter_activation: number | null;
  water_meter_condition: number | null;
  other_information: {
    description: string;
  };
  water_meter_create_date: Date;
  water_meter_bill: boolean;
  water_meter_manual_number: number | null;
  water_meter_order_mode: null | "" | "R" | "P";
  water_meter_type_info: {
    water_meter_type_name: string;
  };
  water_meter_tag_info: {
    water_meter_tag_name: string;
    water_meter_tag_id: string;
  };
  all_water_meters: number;
  water_meter_user_info: {
    user_id: string | null;
    user_name: string | null;
    user_lastname: string | null;
    user_phone: string | null;
  };
  water_meter_project_info: {
    project_id: string;
    project_name: string;
    project_title: string;
  };
  water_meter_module_info: {
    water_meter_module_id: string;
    water_meter_module_code: string;
    water_meter_module_name: string;
  };
};
const DeviceDetailsView = () => {
  const { deviceSerial } = useParams();
  const [fromDate, setFromDate] = useState(getToday().jDate(1));
  const [tillDate, setTillDate] = useState(getToday().add(1, "day"));
  const AdminPermissions: string[] = JSON.parse(
    window.localStorage.getItem("permissions")
  );
  const {
    data: deviceData,
    isLoading: deviceIsLoading,
    status: deviceStatus,
  } = useQuery({
    queryFn: () =>
      reqFunction("watermeters/admin/getOne", {
        water_meter_serial: deviceSerial,
      }),
    queryKey: ["tagsList", deviceSerial],
  });
  const tabsData = AdminPermissions.includes("Bills")
    ? [
        {
          label: "نمودار مصرف",
          content: (
            <CounterConsumptionChart
              deviceInfo={deviceData?.data}
              fromDate={fromDate}
              setFromDate={setFromDate}
              tillDate={tillDate}
              setTillDate={setTillDate}
            />
          ),
        },
        {
          label: "رکوردهای مصرف",
          content: (
            <ConsumptionRecords
              deviceInfo={deviceData?.data}
              fromDate={fromDate}
              setFromDate={setFromDate}
              tillDate={tillDate}
              setTillDate={setTillDate}
            />
          ),
        },
        {
          label: "مشخصات دستگاه",
          content: <DeviceInformation deviceInfo={deviceData?.data} />,
        },
        {
          label: "رخدادها",
          content: <DeviceEvents deviceInfo={deviceData?.data} />,
        },
        {
          label: "قبوض",
          content: <CounterBills deviceInfo={deviceData?.data} />,
        },
      ]
    : [
        {
          label: "نمودار مصرف",
          content: (
            <CounterConsumptionChart
              deviceInfo={deviceData?.data}
              fromDate={fromDate}
              setFromDate={setFromDate}
              tillDate={tillDate}
              setTillDate={setTillDate}
            />
          ),
        },
        {
          label: "رکوردهای مصرف",
          content: (
            <ConsumptionRecords
              deviceInfo={deviceData?.data}
              fromDate={fromDate}
              setFromDate={setFromDate}
              tillDate={tillDate}
              setTillDate={setTillDate}
            />
          ),
        },
        {
          label: "مشخصات دستگاه",
          content: <DeviceInformation deviceInfo={deviceData?.data} />,
        },
        {
          label: "رخدادها",
          content: <DeviceEvents deviceInfo={deviceData?.data} />,
        },
      ];
  return (
    <div className=" ">
      <Card>
        {!deviceIsLoading && deviceStatus === "success" ? (
          <CustomTabs tabsData={tabsData} />
        ) : (
          <div>essential page data loading</div>
        )}
      </Card>
    </div>
  );
};
export default DeviceDetailsView;
