import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { reqFunction } from "utils/API";
import SimpleTable from "components/tables/SimpleTable";
import { toPersianDate } from "utils/TimeUtiles";
import { MdRemoveRedEye } from "react-icons/md";
import CustomButton from "components/button";
import { useDisclosure } from "@chakra-ui/hooks";
import CustomModal from "components/modals";
import { BillObject } from "views/bills/ShowBills";
import { useParams } from "react-router-dom";
import { OneDeviceObj } from ".";
import BillComponent from "views/bills/BillComponent";
import moment from "moment";
import Loading from "components/loading";
import { renderUnit } from "utils/CommonFunctions";
interface CounterBillProps {
  deviceInfo: [OneDeviceObj];
}
type BillTableData = {
  billSerial: string;
  billFrom: string;
  billTill: string;
  startBillNumber: string;
  endBillNumber: string;
  consumptions: string;
  averageConsumption: string;
  price: string;
  deadLine: string;
  billActions: JSX.Element;
};
const CounterBills = (props: CounterBillProps) => {
  const { deviceSerial } = useParams();
  const { deviceInfo } = props;
  const [billInfo, setBillInfo] = useState<BillObject>(null);
  const {
    data: patternData,
    isLoading: patternIsLoading,
    status: patternStatus,
  } = useQuery({
    queryFn: () =>
      reqFunction("Pattern/admin/getAll", {
        page: 1,
        count: 10,
        project_id: deviceInfo[0]?.water_meter_project_info?.project_id
          ? deviceInfo[0].water_meter_project_info.project_id
          : null,
        tag_id: deviceInfo[0].water_meter_tag_info.water_meter_tag_id,
      }),
    queryKey: ["devicePatternList", deviceInfo],
  });
  const tagName = deviceInfo[0].water_meter_tag_info.water_meter_tag_name;
  const {
    data: billsData,
    isLoading: billsIsLoading,
    status: billsStatus,
  } = useQuery({
    queryFn: () =>
      reqFunction("bills/admin/getAll", {
        page: 1,
        count: 30,
        water_meter_serial: deviceSerial,
        bill_serial: null,
        bill_start_date: null,
        user_id: null,
        user_phone_number: null,
        project_id: null,
        bill_end_date: null,
        payment_dead_line: null,
        bill_create_date: null,
      }),
    queryKey: ["counterBills", deviceSerial],
  });
  const {
    isOpen: isBillOpen,
    onOpen: onBillOpen,
    onClose: onBillClose,
  } = useDisclosure();
  const showBillClick = (billInfo: BillObject) => {
    setBillInfo(billInfo);
    onBillOpen();
  };
  const renderBillActions = (billInfo: BillObject) => {
    return (
      <div className=" flex items-center justify-center">
        <CustomButton
          onClick={() => showBillClick(billInfo)}
          icon={<MdRemoveRedEye />}
          color="blue"
          extra="!p-2"
        />
      </div>
    );
  };
  const counterInfoTableHeader = [
    { title: "نام کنتور", headerKey: "counterName" },
    { title: "شماره سریال", headerKey: "counterSerial" },
    // { title: "دسته کنتور", headerKey: "counterTag" },
    { title: "نوع کنتور", headerKey: "counterType" },
    { title: "مالک کنتور", headerKey: "owner" },
  ];
  const billsTableHeader = [
    { title: "شناسه قبض", headerKey: "billSerial" },
    { title: "شروع دوره", headerKey: "billFrom" },
    { title: "پایان دوره", headerKey: "billTill" },
    {
      title: `قرائت شروع (${renderUnit(tagName, true)})`,
      headerKey: "startBillNumber",
    },
    {
      title: `قرائت پایان (${renderUnit(tagName, true)})`,
      headerKey: "endBillNumber",
    },
    {
      title: `میزان مصرف (${tagName ? renderUnit(tagName, true) : ""})`,
      headerKey: "consumptions",
    },
    {
      title: `میانگین مصرف (${tagName ? renderUnit(tagName, true) : ""})`,
      headerKey: "averageConsumption",
    },
    { title: "مبلغ قبض (ریال)", headerKey: "price" },
    { title: "مهلت پرداخت", headerKey: "deadLine" },
    { title: "مشاهده جزئیات", headerKey: "billActions" },
  ];
  const renderBillTable = () => {
    let billTableData: BillTableData[] = [];
    billsData?.data?.forEach((bill: BillObject) =>
      billTableData.push({
        billSerial: bill.bill_serial,
        billFrom: toPersianDate(bill.bill_start_date),
        // billTill: toPersianDate(bill.bill_end_date),
        billTill: toPersianDate(
          moment(bill.bill_end_date, "YYYY-M-D")
            .subtract(1, "day")
            .format("YYYY-M-D")
        ),
        startBillNumber: (
          bill.other_information.start_period_sum / 1000
        ).toLocaleString("fa-IR", {
          minimumFractionDigits: 3,
          maximumFractionDigits: 3,
        }),
        endBillNumber: (
          bill.other_information.end_period_sum / 1000
        ).toLocaleString("fa-IR", {
          minimumFractionDigits: 3,
          maximumFractionDigits: 3,
        }),
        consumptions: (bill.consumptions / 1000).toLocaleString("fa-IR", {
          minimumFractionDigits: 3,
          maximumFractionDigits: 3,
        }),
        averageConsumption: (
          (tagName !== "گاز" ? bill.consumptions / 1000 : bill.consumptions) /
          bill.other_information.period_days
        ).toLocaleString("fa-IR", {
          minimumFractionDigits: 3,
          maximumFractionDigits: 3,
        }),
        price: bill.bill_price.toLocaleString("fa-IR", {
          minimumFractionDigits: 0,
          maximumFractionDigits: 0,
        }),
        deadLine: toPersianDate(bill.payment_dead_line),
        billActions: renderBillActions(bill),
      })
    );
    return billTableData;
  };
  const renderCounterInfoTable = () => {
    let tableData = [
      {
        counterName: deviceInfo[0].water_meter_name,
        counterSerial: deviceInfo[0].water_meter_serial,
        counterType: deviceInfo[0].water_meter_type_info.water_meter_type_name,
        owner: `${deviceInfo[0].water_meter_user_info.user_name ?? "_"} ${
          deviceInfo[0].water_meter_user_info.user_lastname ?? "_"
        }`,
      },
    ];
    return tableData;
  };

  return (
    <div className="py-4">
      <CustomModal
        isOpen={isBillOpen}
        onClose={onBillClose}
        isBill={true}
        title={"قبض"}
        modalType="form"
        information={null}
        modalForm={
          <BillComponent
            onClose={onBillClose}
            billInfo={billInfo}
            patternSample={
              Array.isArray(patternData?.data) && patternData.data.length > 0
                ? patternData.data[0].pattern_list
                : []
            }
          />
        }
      />

      <SimpleTable
        header={counterInfoTableHeader}
        data={renderCounterInfoTable()}
      />
      {!billsIsLoading &&
      billsStatus === "success" &&
      !patternIsLoading &&
      patternStatus === "success" ? (
        <SimpleTable header={billsTableHeader} data={renderBillTable()} />
      ) : (
        <Loading />
      )}
    </div>
  );
};
export default CounterBills;
