import {
  CountOption,
  countSelect,
  counterTagSelect,
  reversedSelect,
  sortValueSelect,
  counterUnitSelect,
} from "variables";
import ProjectCountersFilter from "./ProjectCountersFilter";
// import { useState } from "react";
import { DynamicOption } from "components/fields/SelectInput";
import SimpleTable, { HeaderObject } from "components/tables/SimpleTable";
import { useQuery } from "@tanstack/react-query";
import { reqFunction } from "utils/API";
import { renderTimeJalali, toPersianDate } from "utils/TimeUtiles";
import CustomButton from "components/button";
import { MdRemoveRedEye } from "react-icons/md";
import { DeviceObj } from "views/counters";
import CustomPagination from "components/pagination";
import { Link } from "react-router-dom";
import Loading from "components/loading";
import {
  renderCounterStatus,
  renderSendingStatus,
  renderUnit,
} from "utils/CommonFunctions";
import { useState } from "react";
type CumulativeConsumption = {
  year: [number | null, string];
  month: [number | null, string];
  day: [number | null, string];
};
export type LastConsumptionInfo = {
  RelayStatus: boolean;
  DeviceOnTime: number;
  SignalQuality: number;
  voltage_detail: {
    RTC: number;
    Backup: number;
    Battery: number;
  };
  FirmwareVersion: string;
};
type LastConsumption = {
  consumption_id: string;
  create_time: string;
  value: number;
  cumulative_value: number;
  information?: LastConsumptionInfo | null;
  last_bill_created_time: null | string;
};

export type ConsumptionArray = [
  string,
  {
    cumulative_consumptions: CumulativeConsumption;
    last_consumption?: LastConsumption | null;
    total_value: number;
  }
];
type CounterConsumptionTableData = {
  counterName: JSX.Element;
  counterSerial: string;
  counterStatus: JSX.Element;
  lastConsumptionTime: JSX.Element;
  sendingStatus: JSX.Element;
  lastConsumptionValue: string;
  monthConsumptionValue: string;
  yearConsumptionValue: string;
  lastBillDate: string;
  consumptionValidation: JSX.Element;
  consumptionActions: JSX.Element;
};
interface ProjectCountersProps {
  projectId: string;
  projectDevices: DeviceObj[];
  tag: DynamicOption;
  setTag: React.Dispatch<any>;
  sortValue: DynamicOption;
  setSortValue: React.Dispatch<any>;
  reversed: DynamicOption;
  setReversed: React.Dispatch<any>;
  page: number;
  setPage: React.Dispatch<any>;
  count: CountOption;
  setCount: React.Dispatch<any>;
}
const ProjectCounters = (props: ProjectCountersProps) => {
  const {
    projectId,
    projectDevices,
    tag,
    setTag,
    sortValue,
    setSortValue,
    reversed,
    setReversed,
    page,
    setPage,
    count,
    setCount,
  } = props;
  // let navigate = useNavigate();
  const AdminPermissions: string[] = JSON.parse(
    window.localStorage.getItem("permissions")
  );
  const {
    data: consumptionData,
    isLoading: isConsumptionLoading,
    status: consumptionStatus,
    // refetch: consumptionRefetch,
  } = useQuery({
    queryFn: () =>
      reqFunction("watermeters/v2/admin/cumulative/consumption", {
        page: page,
        count: count.value,
        user_id: null,
        project_id: projectId,
        water_meter_serial: null,
        water_meter_tag: tag.value,
        sort_value: sortValue.value,
        reverse: reversed.value,
      }),
    queryKey: [
      "projectCounterConsumptionList",
      count,
      projectId,
      tag,
      page,
      sortValue,
      reversed,
    ],
  });

  const [unitFilter, setUnitFilter] = useState<DynamicOption>({
    label: "متر مکعب",
    value: "cubic_meter",
  });

  const tableHeader: HeaderObject[] = [
    { title: "نام کنتور", headerKey: "counterName" },
    { title: "شماره سریال", headerKey: "counterSerial" },
    { title: "بکاپ | سیگنال | باتری و برق", headerKey: "counterStatus" },
    { title: "ثبت آخرین مصرف", headerKey: "lastConsumptionTime" },
    { title: "وضعیت ارسال", headerKey: "sendingStatus" },
    {
      title: `آخرین مصرف`, // (${tag ? renderUnit(tag.label, true) : ""})
      headerKey: "lastConsumptionValue",
    },
    {
      title: `مصرف ماه جاری`, // (${tag ? renderUnit(tag.label, true) : ""})
      headerKey: "monthConsumptionValue",
    },
    { title: "آخرین صدور قبض", headerKey: "lastBillDate" },
  ];
  if (
    AdminPermissions.includes("ViewDevice") ||
    AdminPermissions.includes("CRUDDevice")
  ) {
    tableHeader.push({ title: "عملیات", headerKey: "consumptionActions" });
  }
  const deviceNumberPerTag = (tag: DynamicOption) => {
    let devicesPerTag = projectDevices.filter(
      (device) =>
        device.water_meter_type__water_meter_tag__water_meter_tag_id ===
        tag.value
    );
    return devicesPerTag.length;
  };
  const renderValidation = (consData: {
    cumulative_consumptions: CumulativeConsumption;
    last_consumption?: LastConsumption;
    total_value: number;
  }) => {
    return <></>;
  };
  const renderDeviceName = (name: string, serial: string) => {
    return (
      <>
        {AdminPermissions.includes("ViewDevice") ||
        AdminPermissions.includes("CRUDDevice") ? (
          <Link to={`/admin/counters/${serial}`} rel="noopener noreferrer">
            <span>{name}</span>
          </Link>
        ) : (
          <span>{name}</span>
        )}
      </>
    );
  };
  const renderConsumptionActions = (counterSerial: string) => {
    return (
      <div className="flex items-center justify-center">
        <Link to={`/admin/counters/${counterSerial}`} rel="noopener noreferrer">
          <CustomButton
            // onClick={() => routeChange(counterSerial)}
            onClick={null}
            icon={<MdRemoveRedEye />}
            color="blue"
            extra="!p-2 "
          />
        </Link>
      </div>
    );
  };
  const renderTableData = () => {
    let tableData: CounterConsumptionTableData[] = [];
    // console.log(consumptionData.data);
    consumptionData.data?.forEach((consumption: ConsumptionArray) => {
      tableData.push({
        counterName: renderDeviceName(
          projectDevices.filter(
            (device) => device.water_meter_serial === consumption[0]
          )[0].water_meter_name,
          projectDevices.filter(
            (device) => device.water_meter_serial === consumption[0]
          )[0].water_meter_serial
        ),
        counterSerial: consumption[0],
        counterStatus: renderCounterStatus(
          consumption[1]?.last_consumption?.information
        ),
        lastConsumptionTime: renderTimeJalali(
          consumption[1]?.last_consumption?.create_time,
          "chart"
        ),
        sendingStatus: renderSendingStatus(
          consumption[1]?.last_consumption?.create_time
        ),
        lastConsumptionValue: consumption[1]?.last_consumption?.value
          ? unitFilter.value === "cubic_meter"
            ? `${(
                consumption[1]?.last_consumption?.value / 1000
              ).toLocaleString(undefined, {
                minimumFractionDigits: 3,
                maximumFractionDigits: 3,
              })}`
            : `${(consumption[1]?.last_consumption?.value).toLocaleString(
                undefined,
                {
                  minimumFractionDigits: 0,
                  maximumFractionDigits: 0,
                }
              )}`
          : consumption[1]?.last_consumption?.value === 0
          ? "0,00"
          : "__",
        monthConsumptionValue: consumption[1]?.cumulative_consumptions?.month[0]
          ? unitFilter.value === "cubic_meter"
            ? `${(
                consumption[1]?.cumulative_consumptions?.month[0] / 1000
              ).toLocaleString(undefined, {
                minimumFractionDigits: 3,
                maximumFractionDigits: 3,
              })}`
            : `${(consumption[1]?.cumulative_consumptions?.month[0]).toLocaleString(
                undefined,
                {
                  minimumFractionDigits: 0,
                  maximumFractionDigits: 0,
                }
              )} `
          : "__",
        yearConsumptionValue: consumption[1]?.cumulative_consumptions?.year[0]
          ? unitFilter.value === "cubic_meter"
            ? `${(
                consumption[1].cumulative_consumptions.year[0] / 1000
              ).toLocaleString(undefined, {
                minimumFractionDigits: 3,
                maximumFractionDigits: 3,
              })} `
            : `${consumption[1].cumulative_consumptions.year[0].toLocaleString(
                undefined,
                {
                  minimumFractionDigits: 0,
                  maximumFractionDigits: 0,
                }
              )} `
          : "__",
        lastBillDate:
          consumption[1]?.last_consumption?.last_bill_created_time &&
          consumption[1]?.last_consumption?.last_bill_created_time !== "null" &&
          consumption[1]?.last_consumption?.last_bill_created_time !== "None"
            ? toPersianDate(
                consumption[1]?.last_consumption?.last_bill_created_time
              )
            : "__",
        consumptionValidation: renderValidation(consumption[1]),
        consumptionActions: renderConsumptionActions(consumption[0]),
      });
    });
    return tableData;
  };
  return (
    <div className="py-3">
      <div className="flex flex-col items-end justify-between md:flex-row">
        <div className="min-w-52 text-xl font-bold  text-navy-700 dark:text-white">
          {`کنتورهای ${tag.label} (${deviceNumberPerTag(tag)} عدد)`}
        </div>
        <div className=" w-full">
          <ProjectCountersFilter
            tagSelect={counterTagSelect}
            sortValueSelect={sortValueSelect}
            reversedSelect={reversedSelect}
            countSelect={countSelect}
            counterUnitSelect={counterUnitSelect}
            tag={tag}
            setTag={setTag}
            sortValue={sortValue}
            setSortValue={setSortValue}
            reversed={reversed}
            setReversed={setReversed}
            unitFilter={unitFilter}
            setUnitFilter={setUnitFilter}
          />
        </div>
      </div>
      {!isConsumptionLoading && consumptionStatus === "success" ? (
        <div className="table-container mx-auto  w-full ">
          <SimpleTable
            header={tableHeader}
            data={renderTableData()}
            hasIndex={true}
            extra="h-[55vh] !mt-2"
            page={page}
            count={count.value}
          />
        </div>
      ) : (
        // <div className="py-2  text-navy-700  dark:text-white">
        //   در حال بارگزاری !!!
        // </div>
        <Loading />
      )}
      {projectDevices ? (
        <div className="pagination ">
          <CustomPagination
            page={page}
            pageSize={count}
            totalData={deviceNumberPerTag(tag)}
            changePageFunc={setPage}
            changeCount={setCount}
          />
        </div>
      ) : (
        // <div className="py-2  text-navy-700  dark:text-white">
        //   در حال بارگزاری !!!
        // </div>
        <Loading />
      )}
    </div>
  );
};
export default ProjectCounters;
