import Card from "components/card";
import { MdRemoveRedEye } from "react-icons/md";
import { useDisclosure } from "@chakra-ui/hooks";
import CustomModal from "components/modals";
import CustomButton from "components/button";
import { useQuery } from "@tanstack/react-query";
import { reqFunction } from "utils/API";
import SimpleTable from "components/tables/SimpleTable";
import { renderTimeJalali } from "utils/TimeUtiles";
// import UserForm from "components/forms/UserForm";
import { useState } from "react";
import CustomPagination from "components/pagination";
import { CountOption, countSelect } from "variables";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { vscDarkPlus } from "react-syntax-highlighter/dist/esm/styles/prism";
import Loading from "components/loading";

export type SystemLogObject = {
  all_system_logs: number;
  system_log_id: string;
  system_log_action: string;
  system_log_object_action_on: string;
  system_log_action_table: string;
  system_log_field_changes: {};
  system_log_message: string;
  system_log_create_time: string;
  system_log_admin: null | string;
  system_log_user: null | string;
};
type systemLogTable = Array<{
  logAction: string;
  logTable: string;
  logCreateTime: JSX.Element;
  logAdmin: string;
  logUser: string;
  logDetails: JSX.Element;
}>;
const SystemLogs = () => {
  const [page, setPage] = useState<number>(1);
  const [count, setCount] = useState<CountOption>(countSelect[0]);
  const [log, setLog] = useState<{} | string>("");
  const {
    data: systemLogData,
    isLoading: systemLogIsLoading,
    status: systemLogStatus,
    // refetch: usersRefetch,
  } = useQuery({
    queryFn: () =>
      reqFunction("Log/admin/sysetem/log/getAll", {
        page: page,
        count: count.value,
        system_log_action: null,
        system_log_action_table: null,
        system_log_object_action_on__search: null,
      }),
    queryKey: ["SystemLogsList", page, count],
  });
  const {
    isOpen: isLogOpen,
    onOpen: onLogOpen,
    onClose: onLogClose,
  } = useDisclosure();

  const TableHeader = [
    { title: "عملیات انجام شده", headerKey: "logAction" },
    { title: "جدول عملیات", headerKey: "logTable" },
    { title: "ساعت عملیات", headerKey: "logCreateTime" },
    { title: "ادمین مسئول", headerKey: "logAdmin" },
    { title: "کاربر مسئول", headerKey: "logUser" },
    { title: "عملیات", headerKey: "logDetails" },
  ];
  const tableData = () => {
    let logTableData: systemLogTable = [];
    if (!systemLogIsLoading && systemLogStatus === "success") {
      systemLogData.data.forEach((obj: SystemLogObject) =>
        logTableData.push({
          logAction: obj.system_log_action,
          logTable: obj.system_log_action_table,
          logCreateTime: renderTimeJalali(obj.system_log_create_time),
          logAdmin: obj.system_log_admin ? obj.system_log_admin : "__",
          logUser: obj.system_log_user ? obj.system_log_user : "__",
          logDetails: renderLogAction(obj),
        })
      );
    }
    return logTableData;
  };
  const renderLogAction = (data: SystemLogObject) => {
    return (
      <div className=" flex items-center justify-center">
        <CustomButton
          onClick={() => renderMessage(data)}
          icon={<MdRemoveRedEye />}
          color="blue"
          extra="!p-2"
        />
      </div>
    );
  };
  const renderMessage = (logObject: SystemLogObject) => {
    // //console.log(message);
    setLog(
      logObject.system_log_field_changes
        ? logObject.system_log_field_changes
        : logObject.system_log_message
    );
    onLogOpen();
  };
  return (
    <div className=" users-table-container">
      {!systemLogIsLoading && systemLogStatus === "success" ? (
        <>
          {" "}
          <CustomModal
            isOpen={isLogOpen}
            onClose={onLogClose}
            title={"لاگ"}
            modalType="confirmation"
            information={
              <SyntaxHighlighter
                language="json"
                style={vscDarkPlus}
                customStyle={{ maxWidth: "100%", minHeight: "100px" }}
              >
                {JSON.stringify(log, null, 2)}
                {/* {log} */}
              </SyntaxHighlighter>
            }
          />
          <Card extra="!h-[77vh]">
            <div className="relative flex items-center justify-between p-4">
              <div className="text-xl font-bold text-navy-700 dark:text-white">
                لاگ ها
              </div>
              <div className=" moldal-btns flex items-center justify-end"></div>
            </div>
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
                totalData={systemLogData.data[0].all_system_logs}
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
export default SystemLogs;
