import { useDisclosure } from "@chakra-ui/hooks";
import { useQuery } from "@tanstack/react-query";
import CustomButton from "components/button";
import Card from "components/card";
import InputField from "components/fields/InputField";
import Loading from "components/loading";
import CustomModal from "components/modals";
import CustomPagination from "components/pagination";
import SimpleTable from "components/tables/SimpleTable";
import { useState } from "react";
import { MdRemoveRedEye } from "react-icons/md";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { vscDarkPlus } from "react-syntax-highlighter/dist/esm/styles/prism";
import { reqFunction } from "utils/API";
import { renderTimeJalali } from "utils/TimeUtiles";
import { CountOption, countSelect } from "variables";
// import { renderToast } from "utils/globalUtils";

export type MqttLogObject = {
  log_id: string;
  topic_name: string;
  message: string;
  state: "Receive" | "Error";
  create_date: string;
  all_mqtt_logs: number;
};
type MqttLogTable = Array<{
  deviceSerial: string;
  topicName: string;
  messageCreateDate: JSX.Element;
  messageStatus: JSX.Element;
  messageAction: JSX.Element;
}>;
type MessageObject = {
  DevInfo?: {
    SerialNum: string;
    DataCounter: number;
    SignalQuality: number;
    DeviceOnTime: number;
    RelayStatus: boolean;
    FirmwareVersion: string;
    DateTime: string;
  };
  Volume?: {
    Cumulative: number;
    Type: string;
    Value: number;
  };
  Flow?: {};
  Voltage?: {
    Battery: number;
    Backup: number;
    RTC: number;
  };
  Temperature?: {};
};
const MqttLogs = () => {
  const [page, setPage] = useState<number>(1);
  const [count, setCount] = useState<CountOption>(countSelect[0]);
  const [message, setMessage] = useState<string | null>(null);
  const [searchInput, setSearchinput] = useState<string>("");
  const [topicFilter, setTopicFilter] = useState<string | null>(null);

  const {
    data: MqttLogData,
    isLoading: MqttLogIsLoading,
    status: MqttLogStatus,
    // refetch: MqttLogsRefetch,
  } = useQuery({
    queryFn: () =>
      reqFunction("Log/admin/mqttLog/getAll", {
        page: page,
        count: count.value,
        message__icontains: searchInput ? searchInput : null,
        topic_name: topicFilter ? topicFilter : null,
      }),
    queryKey: ["MqttLogsList", page, count, searchInput, topicFilter],
  });
  const {
    isOpen: isLogOpen,
    onOpen: onLogOpen,
    onClose: onLogClose,
  } = useDisclosure();

  const TableHeader = [
    { title: "سریال کنتور", headerKey: "deviceSerial" },
    { title: "نام تاپیک", headerKey: "topicName" },
    { title: "زمان دریافت", headerKey: "messageCreateDate" },
    { title: "وضعیت پیام", headerKey: "messageStatus" },
    { title: "عملیات", headerKey: "messageAction" },
  ];
  const tableData = () => {
    let logTableData: MqttLogTable = [];
    if (!MqttLogIsLoading && MqttLogStatus === "success") {
      MqttLogData?.data?.forEach((obj: MqttLogObject) => {
        logTableData.push({
          deviceSerial: showSerial(obj.message),
          // deviceSerial: "",
          topicName: obj.topic_name,
          messageCreateDate: renderTimeJalali(obj.create_date, "chart"),
          messageStatus: (
            <span
              className={`rounded ${
                obj.state === "Receive" ? "bg-green-600" : "bg-red-600"
              } px-1 text-sm text-white`}
            >
              {obj.state === "Receive"
                ? "پیام دریافتی دستگاه"
                : "پیام دریافت شده با خطا"}
            </span>
          ),
          messageAction: renderLogAction(obj.message, obj.log_id),
        });
      });
    }
    return logTableData;
  };

  // const deleteLogClick = async (logId: string) => {
  //   // const response = await reqFunction("Log/admin/mqttLog/getAll", {
  //   //   other_admin_id: logId,
  //   // });
  //   // if (response.code === 200) {
  //   //   renderToast("لاگ Mqtt با موفقیت حذف شد.", "success");
  //   //   MqttLogsRefetch();
  //   // } else {
  //   //   renderToast(
  //   //     response?.farsi_message
  //   //       ? response.farsi_message
  //   //       : "در حذف لاگ Mqtt مشکلی رخ داده",
  //   //     "err"
  //   //   );
  //   //console.log(logId);
  // };

  const renderLogAction = (message: string, logId: string) => {
    return (
      <div className=" flex items-center justify-center">
        <CustomButton
          onClick={() => renderMessage(message)}
          icon={<MdRemoveRedEye />}
          color="blue"
          extra="!p-2"
        />
        {/* <CustomButton
          onClick={() => deleteLogClick(logId)}
          icon={<MdDelete />}
          color="red"
          extra="!p-2"
        /> */}
      </div>
    );
  };
  const showSerial = (message: string) => {
    try {
      let correctMessage = message
        .replace(/\s/g, "")
        .replace(/\?/g, "")
        .replace(/\bnan\b/g, "null");
      let m: MessageObject = JSON.parse(correctMessage);
      return m ? m?.DevInfo?.SerialNum : "";
    } catch (error) {
      return "";
    }
  };
  const renderMessage = (message: string) => {
    try {
      let correctMessage = message
        .replace(/\s/g, "")
        .replace(/\?/g, "")
        .replace(/\bnan\b/g, "null");
      let parsed = JSON.parse(correctMessage) ?? null;
      setMessage(parsed ? parsed : message);
    } catch (error) {
      setMessage("");
    }
    onLogOpen();
  };
  return (
    <div className=" users-table-container">
      <div className="relative flex items-center justify-between px-4 pb-2 pt-0">
        <div className="text-xl font-bold text-navy-700 dark:text-white">
          پیام ها
        </div>
        <div className="moldal-btns flex items-start justify-end gap-2">
          <div className="w-[200px]">
            <InputField
              id="project-name"
              placeholder="جستجو در لاگ"
              type="text"
              state={searchInput}
              setState={setSearchinput}
            />
          </div>
          <div className="w-[200px]">
            <select
              value={topicFilter ?? ""}
              onChange={(e) => setTopicFilter(e.target.value || null)}
              className="mt-2 h-12 w-full rounded-xl border border-gray-200 bg-white/0 px-3 py-[10px] text-sm text-gray-700 outline-none dark:border-white/10 dark:bg-navy-700 dark:text-white"
            >
              <option value="">همه تاپیک‌ها</option>
              <option value="meters/data">meters/data</option>
              <option value="meters/events">meters/events</option>
            </select>
          </div>
        </div>
      </div>
      {!MqttLogIsLoading && MqttLogStatus === "success" ? (
        <>
          {" "}
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
          <Card extra="!h-[70vh] !mt-0">
            <div className="table-container mx-auto  w-full ">
              <SimpleTable
                header={TableHeader}
                data={tableData()}
                hasIndex={true}
                extra="h-[55vh]"
                page={page}
                count={count.value}
              />
            </div>
            <div className="pagination ">
              <CustomPagination
                page={page}
                pageSize={count}
                totalData={
                  MqttLogData?.data[0]?.all_mqtt_logs
                    ? MqttLogData.data[0].all_mqtt_logs
                    : 0
                }
                changePageFunc={setPage}
                changeCount={setCount}
              />
            </div>
          </Card>
        </>
      ) : (
        // <></>
        <Loading />
      )}
    </div>
  );
};
export default MqttLogs;
