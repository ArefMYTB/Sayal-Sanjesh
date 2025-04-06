import { useQuery } from "@tanstack/react-query";
import { useDisclosure } from "@chakra-ui/hooks";
import CustomButton from "components/button";
import CustomPagination from "components/pagination";
import SimpleTable from "components/tables/SimpleTable";
import { useState } from "react";
import { MdDelete, MdOutlineFileDownload } from "react-icons/md";
import { MdRemoveRedEye } from "react-icons/md";
import { useParams } from "react-router-dom";
import { reqFunction } from "utils/API";
import { renderUnit } from "utils/CommonFunctions";
import { getDiffrenceInHours, renderTimeJalali } from "utils/TimeUtiles";
import { renderToast } from "utils/globalUtils";
import { CountOption, countSelect } from "variables";
import { TagObject } from "views/counters";
import { TypeObject } from "views/settings/DeviceTypesTable";
import { UserObject } from "views/users/UsersTable";
import { OneDeviceObj } from ".";
import ConsumptionChartFilter from "./ConsumptionChartFilter";
import CustomModal from "components/modals";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { vscDarkPlus } from "react-syntax-highlighter/dist/esm/styles/prism";
import { renderCounterStatus } from "utils/CommonFunctions";

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
export type ConsumptionRecordObject = {
  from_previous_record: string;
  to_current_record: string;
  consumption_id: string;
  log_time: string;
  log_message: string;
  information: LastConsumptionInfo;
  value: number;
  device_value: null | number;
  cumulative_value: number;
  create_time: string;
  water_meters_info: {
    water_meter_serial: string;
    water_meter_name: string;
  };
  type_info: TypeObject;
  tag_info: TagObject;
  all_consumptions: number;
  user_info: UserObject;
  project_info: {
    water_meter_project_id: string;
    water_meter_project_name: string;
  };
};
type RecordsTableData = {
  // projectName: string;
  // deviceSerial: string;
  dataCounter: string;
  logDate: JSX.Element;
  recordDate: JSX.Element;
  counterStatus: JSX.Element;
  recordValue: string;
  recordTimeSpan: string;
  consumptionInPeriod: string;
  cumulativeValue: string;
  recordActions: JSX.Element;
  messageAction: JSX.Element;
};
interface ConsumptionRecordsProps {
  deviceInfo: [OneDeviceObj];
  fromDate: any;
  setFromDate: React.Dispatch<any>;
  tillDate: any;
  setTillDate: React.Dispatch<any>;
}
const ConsumptionRecords = (props: ConsumptionRecordsProps) => {
  const { deviceSerial } = useParams();
  const { deviceInfo, fromDate, setFromDate, tillDate, setTillDate } = props;
  const [excelLoading, setExcelLoading] = useState<boolean>(false);
  const [page, setPage] = useState<number>(1);
  const [count, setCount] = useState<CountOption>(countSelect[0]);
  const [message, setMessage] = useState<string | null>(null);
  const AdminPermissions: string[] = JSON.parse(
    window.localStorage.getItem("permissions")
  );
  const {
    data: recordsData,
    isLoading: recordsIsLoading,
    status: recordsStatus,
    refetch: recordsRefetch,
  } = useQuery({
    queryFn: () =>
      reqFunction(
        "watermeters/admin/getAll/consumption",
        {
          page: page,
          count: count.value,
          start_time: fromDate.format("YYYY-M-D"),
          end_time: tillDate.format("YYYY-M-D"),
          water_meters: deviceSerial,
          water_meter_user: null,
          water_meter_project: null,
          water_meter_type: null,
        },
        "post"
      ),
    queryKey: ["consumptionRecords", deviceSerial, page, count],
  });
  let tableHeader = [
    // { title: "سریال دستگاه", headerKey: "deviceSerial" },
    { title: "دیتا کانتر", headerKey: "dataCounter" },
    { title: "زمان ایجاد", headerKey: "recordDate" },
    { title: "زمان دریافت", headerKey: "logDate" },
    { title: "بکاپ | سیگنال | باتری و برق", headerKey: "counterStatus" },
    { title: "آخرین مصرف ارسالی", headerKey: "recordValue" },
    { title: "بازه ارسال", headerKey: "recordTimeSpan" },
    { title: "مصرف در بازه ارسال", headerKey: "consumptionInPeriod" },
    { title: "مصرف تجمعی", headerKey: "cumulativeValue" },
  ];
  if (deviceInfo[0]?.water_meter_tag_info?.water_meter_tag_name === "برق") {
    tableHeader = [
      { title: "سریال دستگاه", headerKey: "deviceSerial" },
      { title: "زمان ایجاد", headerKey: "recordDate" },
      { title: "مصرف در بازه ارسال", headerKey: "consumptionInPeriod" },
    ];
  }
  if (AdminPermissions.includes("LogDetail")) {
    tableHeader.push({ title: "لاگ دستگاه", headerKey: "messageAction" });
  }
  if (AdminPermissions.includes("ConsumptionDelete")) {
    tableHeader.push({ title: "عملیات", headerKey: "recordActions" });
  }
  const getExcelFile = async () => {
    setExcelLoading(true);
    const response = await reqFunction(
      "watermeters/admin/getOne/csv",
      {
        water_meter_serial: deviceSerial,
        start_time: fromDate.format("YYYY-M-D"),
        end_time: tillDate.format("YYYY-M-D"),
      },
      "post"
    );
    if (response.code === 200) {
      let fileUrl =
        process.env.REACT_APP_SAYAL_API_ENDPOINT_MAIN + response.data.fileurl;
      let link = document.getElementById("download-xlsx-counter");
      link.setAttribute("href", fileUrl);
      link.setAttribute("download", fileUrl);
      link.click();
      setExcelLoading(false);
    } else {
      renderToast(
        response?.farsi_message
          ? response.farsi_message
          : "در دریافت فایل اکسل خطایی رخ داده",
        "err"
      );
      setExcelLoading(false);
    }
  };
  const deleteRecordClick = async (id: string) => {
    const response = await reqFunction("watermeters/admin/delete/consumption", {
      mode: "single_consumption",
      time: null,
      consumption_id: id,
      water_meter_serial: deviceSerial,
    });
    if (response.code === 200) {
      renderToast("میزان مصرف با موفقیت حذف شد.", "success");
      recordsRefetch();
    } else {
      renderToast(
        response?.farsi_message
          ? response.farsi_message
          : "در حذف میزان مصرف مشکلی رخ داده",
        "err"
      );
    }
  };
  const renderActions = (id: string) => {
    return (
      <div className=" flex items-center justify-center">
        {/* <CustomButton
          onClick={() => renderMessage(message)}
          icon={<MdRemoveRedEye />}
          color="blue"
          extra="!p-2"
        /> */}
        <CustomButton
          onClick={() => {
            if (window.confirm("آیا از حذف این رکورد اطمینان دارید؟")) {
              deleteRecordClick(id);
            }
          }}
          icon={<MdDelete />}
          color="red"
          extra="!p-2"
        />
      </div>
    );
  };
  const tableData = () => {
    let tableData: RecordsTableData[] = [];
    recordsData.data?.forEach((record: ConsumptionRecordObject) => {
      tableData.push({
        // projectName: record.project_info.water_meter_project_name,
        // deviceSerial: record.water_meters_info.water_meter_serial,
        dataCounter: (() => {
          try {
            const parsed = JSON.parse(
              record.log_message
                ?.replace(/\s/g, "")
                .replace(/\?/g, "")
                .replace(/\bnan\b/g, "null")
            );
            return parsed?.DevInfo?.DataCounter?.toString() ?? "__";
          } catch (e) {
            return "__";
          }
        })(),

        recordDate: renderTimeJalali(record.create_time, "chart"),
        logDate: (() => {
          try {
            return record.log_time ? (
              <>{renderTimeJalali(record.log_time, "chart")}</>
            ) : (
              <></>
            );
          } catch (error) {
            return <></>;
          }
        })(),
        counterStatus: renderCounterStatus(record.information),

        recordValue:
          record.device_value || record.device_value === 0
            ? `${Math.round(record.device_value).toLocaleString()} ${renderUnit(
                record.tag_info.water_meter_tag_name,
                false
              )}`
            : "__",
        recordTimeSpan: getDiffrenceInHours(
          record.from_previous_record,
          record.create_time
        ),
        consumptionInPeriod: `${Math.round(
          record.value
        ).toLocaleString()} ${renderUnit(
          record.tag_info.water_meter_tag_name,
          false
        )}`,
        cumulativeValue: `${record.cumulative_value.toLocaleString()} ${renderUnit(
          record.tag_info.water_meter_tag_name,
          false
        )}`,
        recordActions: renderActions(record.consumption_id),
        messageAction: renderLogAction(record.log_message),
      });
    });
    return tableData;
  };

  const renderLogAction = (message: string) => {
    return (
      <div className=" flex items-center justify-center">
        <CustomButton
          onClick={() => renderMessage(message)}
          icon={<MdRemoveRedEye />}
          color="blue"
          extra="!p-2"
        />
      </div>
    );
  };

  const {
    isOpen: isLogOpen,
    onOpen: onLogOpen,
    onClose: onLogClose,
  } = useDisclosure();

  const renderMessage = (message: string) => {
    // Check if message is empty or invalid before parsing
    if (!message.trim()) {
      setMessage(message); // Handle empty or whitespace-only messages
      onLogOpen();
      return;
    }

    // Replace unwanted characters
    let correctMessage = message
      .replace(/\s/g, "")
      .replace(/\?/g, "")
      .replace(/\bnan\b/g, "null");

    // Try parsing the message safely
    let parsed = null;
    try {
      parsed = JSON.parse(correctMessage);
    } catch (e) {
      // Handle cases where parsing fails (keep original message)
      parsed = null;
    }

    // Set the message (either parsed or original)
    setMessage(parsed ? parsed : message);
    onLogOpen();
  };

  return (
    <>
      <div className="projects-overview pt-4">
        <div className=" grid  grid-cols-1 gap-2 md:grid-cols-12">
          <div className="mt-1 space-y-1 py-2 font-bold text-navy-700 md:col-span-3 dark:text-white">
            <div>
              <span className="text-gray-500 dark:text-gray-300">
                نام دستگاه:{" "}
              </span>
              <span>{deviceInfo[0].water_meter_name}</span>
            </div>
            <div>
              <span className="text-gray-500 dark:text-gray-300">
                نام پروژه:{" "}
              </span>
              <span>
                {deviceInfo[0]?.water_meter_project_info?.project_name}
              </span>
            </div>
            <div>
              <span className="text-gray-500 dark:text-gray-300">
                سریال دستگاه:{" "}
              </span>
              <span>{deviceInfo[0].water_meter_serial}</span>
            </div>
          </div>

          <div className="chart-statistics flex items-end py-2 md:col-span-7">
            <ConsumptionChartFilter
              fromDate={fromDate}
              setFromDate={setFromDate}
              tillDate={tillDate}
              setTillDate={setTillDate}
              update={recordsRefetch}
              chartTag={{
                label: deviceInfo[0].water_meter_tag_info.water_meter_tag_name,
                value: deviceInfo[0].water_meter_tag_info.water_meter_tag_id,
              }}
              tab="records"
            />
          </div>
          <div className=" moldal-btns flex items-end justify-end md:col-span-2">
            <CustomButton
              text="دریافت اکسل"
              onClick={() => getExcelFile()}
              icon={<MdOutlineFileDownload />}
              color="green"
              isDisable={excelLoading}
            />
          </div>
        </div>
        {/* <div className="chart-statistics py-2">
          <ConsumptionChartFilter
            fromDate={fromDate}
            setFromDate={setFromDate}
            tillDate={tillDate}
            setTillDate={setTillDate}
            update={recordsRefetch}
            chartTag={{
              label: deviceInfo[0].water_meter_tag_info.water_meter_tag_name,
              value: deviceInfo[0].water_meter_tag_info.water_meter_tag_id,
            }}
            tab="records"
          />
        </div> */}
        {!recordsIsLoading && recordsStatus === "success" ? (
          <div className="table-container mx-auto  w-full ">
            <CustomModal
              isOpen={isLogOpen}
              onClose={onLogClose}
              title={"پیام"}
              modalType="confirmation"
              information={
                <SyntaxHighlighter
                  language="json"
                  style={vscDarkPlus}
                  customStyle={{ whiteSpace: "pre-wrap !important" }}
                >
                  {typeof message === "string"
                    ? message
                    : JSON.stringify(message, null, 2)}
                  {/* {message} */}
                </SyntaxHighlighter>
              }
            />
            <SimpleTable
              header={tableHeader}
              data={tableData()}
              hasIndex={true}
              extra="h-[50vh]"
              page={page}
              count={count.value}
            />
            <div className="pagination ">
              <CustomPagination
                page={page}
                pageSize={count}
                totalData={
                  recordsData?.data?.length > 0
                    ? recordsData.data[0].all_consumptions
                    : 0
                }
                changePageFunc={setPage}
                changeCount={setCount}
              />
            </div>
            <a
              id="download-xlsx-counter"
              href="/"
              rel="noopener noreferrer"
              style={{ display: "none" }}
            >
              exel file
            </a>
          </div>
        ) : (
          <div>table is loading</div>
        )}
      </div>
    </>
  );
};
export default ConsumptionRecords;
