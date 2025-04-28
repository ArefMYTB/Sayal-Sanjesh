import Card from "components/card";
import { MdAdd, MdDelete } from "react-icons/md";
import { useDisclosure } from "@chakra-ui/hooks";
import CustomModal from "components/modals";
import CustomButton from "components/button";
import { useQuery } from "@tanstack/react-query";
import { reqFunction } from "utils/API";
import SimpleTable from "components/tables/SimpleTable";
import { toPersianDate } from "utils/TimeUtiles";
import EventTypeForm from "components/forms/EventTypeForm";
import { useState } from "react";
import { importanceSelectData } from "variables";
import { DynamicOption } from "components/fields/SelectInput";
import { renderToast } from "utils/globalUtils";

type EventTypeTableData = Array<{
  eventTypeName: string;
  eventTypeCode: string;
  eventTypeCreateDate: string;
  eventTypeImportance: JSX.Element;
  eventTypeActions: JSX.Element;
}>;
export type EventType = {
  event_type_admin: {};
  event_type_id: string;
  event_type_code: string;
  event_type_keyword: string;
  event_type_importance: "L" | "M" | "H";
  event_type_create_time: Date;
};
const EventTypesTable = () => {
  const [eventTypeName, setEventTypeName] = useState<string>("");
  const [importance, setImportance] = useState<DynamicOption>(null);
  const {
    data: eventTypeData,
    isLoading: eventTypeIsLoading,
    status: eventTypeStatus,
    refetch: eventTypeRefetch,
  } = useQuery({
    queryFn: () =>
      reqFunction("EventType/admin/getAll", {
        page: 1,
        count: 50,
      }),
    queryKey: ["eventTypeList"],
  });

  const {
    isOpen: isEventTypeOpen,
    onOpen: onEventTypeOpen,
    onClose: onEventTypeClose,
  } = useDisclosure();
  const deleteEventTypeClick = async (id: string) => {
    //console.log(id);
    const response = await reqFunction("EventType/admin/delete", {
      event_type_id: id,
    });
    if (response.code === 200) {
      renderToast("نوع رویداد با موفقیت حذف شد.", "success");
      eventTypeRefetch();
    } else {
      renderToast(
        response?.farsi_message
          ? response.farsi_message
          : "در حذف نوع رویداد مشکلی رخ داده",
        "err"
      );
    }
  };
  const renderEventTypeActions = (eventId: string) => {
    return (
      <div className=" flex items-center justify-center">
        <CustomButton
          onClick={() =>{
            if (window.confirm("آیا از حذف این نوع رخداد اطمینان دارید؟")) {
               deleteEventTypeClick(eventId)
            }
          }}
          icon={<MdDelete />}
          color="red"
          extra="!p-2"
        />
      </div>
    );
  };
  const renderImportance = (level: "M" | "H" | "L") => {
    return (
      <span
        className={`${
          level === "H"
            ? " bg-red-500"
            : level === "M"
            ? " bg-orange-500"
            : " bg-yellow-500"
        } rounded px-1 text-sm text-white`}
      >
        {level === "H" ? "زیاد" : level === "M" ? "متوسط" : "کم"}
      </span>
    );
  };
  const eventTypeTableHeader = [
    { title: "نام رخداد", headerKey: "eventTypeName" },
    { title: "کد رخداد", headerKey: "eventTypeCode" },
    { title: "اهمیت رخداد", headerKey: "eventTypeImportance" },
    { title: "تاریخ ایجاد", headerKey: "eventTypeCreateDate" },
    { title: "عملیات", headerKey: "eventTypeActions" },
  ];
  const tableData = () => {
    let eventTypesTableData: EventTypeTableData = [];
    if (!eventTypeIsLoading && eventTypeStatus !== "pending") {
      eventTypeData.data.forEach((obj: EventType) =>
        eventTypesTableData.push({
          eventTypeName: obj.event_type_keyword,
          eventTypeCode: obj.event_type_code,
          eventTypeImportance: renderImportance(obj.event_type_importance),
          eventTypeCreateDate: toPersianDate(obj.event_type_create_time),
          eventTypeActions: renderEventTypeActions(obj.event_type_id),
        })
      );
    }
    return eventTypesTableData;
  };
  return (
    <div className=" users-table-container">
      <CustomModal
        isOpen={isEventTypeOpen}
        onClose={onEventTypeClose}
        title={"نوع رخداد"}
        modalType="form"
        information={null}
        modalForm={
          <EventTypeForm
            importanceSelectData={importanceSelectData}
            importance={importance}
            setImportance={setImportance}
            eventTypeName={eventTypeName}
            setEventTypeName={setEventTypeName}
            onClose={onEventTypeClose}
            updateTable={eventTypeRefetch}
          />
        }
      />
      <Card extra="border-none h-max">
        <div className="relative flex items-center justify-between p-4">
          <div className="text-xl font-bold text-navy-700 dark:text-white">
            {`انواع رخداد (${
              eventTypeIsLoading ? "loading..." : eventTypeData?.data.length
            })`}
          </div>
          <div className=" moldal-btns flex items-center justify-end">
            <CustomButton
              text="ایجاد نوع رخداد"
              onClick={onEventTypeOpen}
              icon={<MdAdd />}
              color="green"
              extra="ml-4"
            />
          </div>
        </div>
        <SimpleTable
          header={eventTypeTableHeader}
          data={tableData()}
          hasIndex={true}
          extra="!h-[65vh]"
        />
      </Card>
      <div className="pagination my-4 py-4"></div>
    </div>
  );
};
export default EventTypesTable;
