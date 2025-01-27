// import { useParams } from "react-router-dom";
import { OneDeviceObj } from ".";
import { useQuery } from "@tanstack/react-query";
import { reqFunction } from "utils/API";
// import ConsumptionChartFilter from "./ConsumptionChartFilter";
// import CustomButton from "components/button";
// import { MdOutlineFileDownload } from "react-icons/md";
import SimpleTable from "components/tables/SimpleTable";
// import { UserObject } from "views/users/UsersTable";
// import { TagObject } from "views/counters";
// import { TypeObject } from "views/settings/DeviceTypesTable";
import { renderTimeJalali } from "utils/TimeUtiles";
// import { renderToast } from "utils/globalUtils";
// import { useState } from "react";
import { EventType } from "views/settings/EventTypesTable";
import CustomPagination from "components/pagination";
import { useState } from "react";
import { CountOption, countSelect } from "variables";
export type EventRecordObject = {
  all_event_numbers: number;
  event_id: string;
  event_type: EventType;
  event_module: {
    water_meter_module_id: string;
    water_meter_module_code: string;
    water_meter_module_name: string;
  };
  event_information: {};
  event_create_time: string;
  event_count: number;
  event_counter: null | number;
  event_last_occurrence: null | string;
};
type EventsTableData = {
  eventName: string;
  eventCode: string;
  eventTime: JSX.Element;
  reciveTime: JSX.Element;
  eventCount: number;
  eventCounter: number;
  eventImportance: JSX.Element;
};
interface DeviceEventsProps {
  deviceInfo: [OneDeviceObj];
  // fromDate: any;
  // setFromDate: React.Dispatch<any>;
  // tillDate: any;
  // setTillDate: React.Dispatch<any>;
}
const DeviceEvents = (props: DeviceEventsProps) => {
  // const { deviceSerial } = useParams();
  const { deviceInfo } = props;
  const [page, setPage] = useState<number>(1);
  const [count, setCount] = useState<CountOption>(countSelect[0]);
  const moduleCode =
    deviceInfo[0].water_meter_module_info?.water_meter_module_code;
  // moduleID = deviceInfo[0].water_meter_module_info?.water_meter_module_id;
  const {
    data: eventsData,
    isLoading: eventsIsLoading,
    status: eventsStatus,
    // refetch: eventsRefetch,
  } = useQuery({
    queryFn: () =>
      reqFunction(
        "Event/admin/getAll",
        {
          page: page,
          count: count.value,
          module_id: null,
          // module_code: null,
          // module_id: moduleID ? moduleID : null,
          module_code: moduleCode ? moduleCode : null,
        },
        "post"
      ),
    queryKey: ["eventsRecords", deviceInfo[0], page, count],
  });
  const tableHeader = [
    { title: "رخداد", headerKey: "eventName" },
    { title: "کد رخداد", headerKey: "eventCode" },
    { title: "زمان رخداد", headerKey: "eventTime" },
    { title: "زمان دریافت", headerKey: "reciveTime" },
    { title: "تعداد رخداد", headerKey: "eventCount" },
    { title: "شمارنده رخداد دستگاه", headerKey: "eventCounter" },
    { title: "اهمیت رخداد", headerKey: "eventImportance" },
  ];

  const tableData = () => {
    let tableData: EventsTableData[] = [];
    eventsData.data.forEach((event: EventRecordObject) => {
      tableData.push({
        eventName: event.event_type.event_type_keyword,
        eventCode: event.event_type.event_type_code,
        eventTime: event.event_last_occurrence ? (
          renderTimeJalali(event.event_last_occurrence, "chart")
        ) : (
          <span>نامشخص</span>
        ),
        reciveTime: renderTimeJalali(event.event_create_time, "chart"),
        eventCount: Math.floor(event.event_count),
        eventCounter: event.event_counter ?? 0,
        eventImportance: (
          <span
            className={`${
              event.event_type.event_type_importance === "H"
                ? " bg-red-500"
                : event.event_type.event_type_importance === "M"
                ? " bg-orange-500"
                : " bg-yellow-500"
            } rounded px-1 text-sm text-white`}
          >
            {event.event_type.event_type_importance === "H"
              ? "زیاد"
              : event.event_type.event_type_importance === "M"
              ? "متوسط"
              : "کم"}
          </span>
        ),
      });
    });
    return tableData;
  };
  return (
    <>
      <div className="projects-overview pt-4">
        <div className="  text-xl font-bold text-navy-700 dark:text-white">
          {`رخدادهای ${deviceInfo[0].water_meter_name}`}
        </div>
        {moduleCode ? (
          <>
            {" "}
            {!eventsIsLoading && eventsStatus === "success" ? (
              <div className="table-container mx-auto  w-full ">
                <div className="relative flex items-center justify-between py-1">
                  <div className="text-xl font-bold text-navy-700 dark:text-white">
                    {`رکوردها (${
                      eventsIsLoading
                        ? 0
                        : eventsData?.data[0]?.all_event_numbers
                    })`}
                  </div>
                  <div className=" moldal-btns flex items-center justify-end"></div>
                </div>
                <SimpleTable
                  header={tableHeader}
                  data={tableData()}
                  hasIndex={true}
                  extra="h-[54vh]"
                  page={page}
                  count={count.value}
                />
                <div className="pagination ">
                  <CustomPagination
                    page={page}
                    pageSize={count}
                    totalData={
                      eventsData?.data.length > 0
                        ? eventsData.data[0].all_event_numbers
                        : 0
                    }
                    changePageFunc={setPage}
                    changeCount={setCount}
                  />
                </div>
              </div>
            ) : (
              <div>table is loading</div>
            )}
          </>
        ) : (
          <div>ماژولی برای دریافت رخداد موجود نیست</div>
        )}
      </div>
    </>
  );
};
export default DeviceEvents;
